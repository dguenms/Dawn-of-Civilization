"""Exercise dependency reuse, partial recovery and the installer's prefix boundary."""
from contextlib import ExitStack
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_support
import prepare_dependencies as dependencies
import prepare_headers


class DependencyPreparationTest(unittest.TestCase):
    def setUp(self):
        stack = self.stack = ExitStack()
        self.addCleanup(stack.close)
        (build_support.ROOT / 'tmp').mkdir(exist_ok=True)
        directory = stack.enter_context(tempfile.TemporaryDirectory(dir=build_support.ROOT / 'tmp'))
        self.root = Path(directory) / 'mod'
        self.output = self.root / 'tmp/dependencies'
        self.output.mkdir(parents=True)
        self.sdk_output = self.output / 'sdk'
        self.runtime_output = self.output / 'runtime'
        self.proton = Path(directory) / 'proton'
        self.proton.write_bytes(b'test proton')
        (self.proton.parent / 'version').write_text('test version')
        (self.root / 'tools').mkdir()
        (self.root / 'tools/link-lock.json').write_text(json.dumps({'link_inputs': {}}))
        for module in [build_support, dependencies]:
            stack.enter_context(patch.object(module, 'ROOT', self.root))
        stack.enter_context(patch.object(dependencies, 'LOCK', {
            'proton_launcher_sha256': dependencies.digest(self.proton),
            'proton_version': 'test version',
        }))
        self.sdk_files = {
            'Microsoft Visual C++ Toolkit 2003/include/xstring': b'test xstring',
            'Microsoft Visual C++ Toolkit 2003/include/yvals.h': b'test yvals',
            'Microsoft Visual C++ Toolkit 2003/include/typeinfo': b'test typeinfo',
            'Microsoft Visual C++ Toolkit 2003/lib/msvcrt.lib': b'test msvcrt',
            'Microsoft Visual C++ Toolkit 2003/lib/msvcprt.lib': b'test msvcprt',
            'Microsoft Visual C++ Toolkit 2003/EULA.txt': b'test SDK license',
            'WindowsSDK/include/BaseTsd.h': b'test SDK header',
            'WindowsSDK/lib/Kernel32.Lib': b'test kernel import',
        }
        pins = {}
        trees = {'vc71': [], 'sdk': []}
        for name, data in self.sdk_files.items():
            tree, relative = name.split('/', 1)
            tree = 'sdk' if tree == 'WindowsSDK' else 'vc71'
            identity = hashlib.sha256(data).hexdigest()
            pins[tree + '/' + relative] = identity
            if relative.startswith('include/'):
                trees[tree].append((relative.split('/', 1)[1], identity))
        stack.enter_context(patch.object(prepare_headers, 'PINS', pins))
        stack.enter_context(patch.object(prepare_headers, 'HEADER_TREE_PINS', {
            tree: hashlib.sha256(json.dumps(sorted(rows), separators=(',', ':')).encode()).hexdigest()
            for tree, rows in trees.items()
        }))
        self.sdk_installer = Path(directory) / 'sdk-installer.exe'
        self.sdk_installer.write_bytes(b'test SDK installer')
        self.runtime_installer = Path(directory) / 'VC_redist.x86.exe'
        self.runtime_installer.write_bytes(b'test runtime installer')
        self.runtime_data = b'test runtime'
        stack.enter_context(patch.object(dependencies, 'SDK_INSTALLER_SHA256', dependencies.digest(self.sdk_installer)))
        stack.enter_context(patch.object(dependencies, 'SDK_LICENSE_SHA256',
            hashlib.sha256(self.sdk_files['Microsoft Visual C++ Toolkit 2003/EULA.txt']).hexdigest()))
        stack.enter_context(patch.object(dependencies, 'RUNTIME_INSTALLER_SHA256', dependencies.digest(self.runtime_installer)))
        stack.enter_context(patch.object(dependencies, 'RUNTIME_SHA256', hashlib.sha256(self.runtime_data).hexdigest()))
        self.download = stack.enter_context(patch.object(dependencies.urllib.request, 'urlopen',
                                                       side_effect=AssertionError('unexpected download')))
        stack.enter_context(patch('sys.stdout', new_callable=io.StringIO))

    def write_sdk_files(self):
        for name, data in self.sdk_files.items():
            path = self.sdk_output / 'installed' / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)

    def runtime_metadata(self, path):
        dependencies.require_hash(path, dependencies.RUNTIME_SHA256)
        return {'path': str(path), 'sha256': dependencies.digest(path)}

    def cabinets(self, installer, output):
        result = {}
        for name in ['notices', 'payload']:
            path = output / f'{name}.cab'
            path.write_bytes(b'MSCFtest cabinet')
            result[name] = {'path': path, 'sha256': dependencies.digest(path)}
        return result

    def extract(self, cabinet, destination, seven_zip):
        destination.mkdir(parents=True, exist_ok=True)
        if destination.name == 'notices':
            (destination / 'license.txt').write_bytes(b'test runtime license')
        elif destination.name == 'payload':
            (destination / 'a2').write_bytes(b'MSCFtest nested cabinet')
        elif destination.name == 'minimum':
            (destination / dependencies.RUNTIME_NAME).write_bytes(self.runtime_data)
        return dependencies.file_manifest(destination)

    def runtime_mocks(self):
        stack = ExitStack()
        stack.enter_context(patch.object(dependencies, 'embedded_cabinets', side_effect=self.cabinets))
        extract = stack.enter_context(patch.object(dependencies, 'extract', side_effect=self.extract))
        stack.enter_context(patch.object(dependencies, 'runtime_metadata', side_effect=self.runtime_metadata))
        return stack, extract

    @unittest.skipIf(dependencies.os.name == 'nt', 'Proton is only used on Linux')
    def test_installer_prefix_is_outside_mod_and_removed(self):
        prefixes = []

        def install(command, *, env, **kwargs):
            prefix = Path(env['STEAM_COMPAT_DATA_PATH'])
            prefixes.append(prefix)
            self.assertFalse(prefix.resolve().is_relative_to(self.root.resolve()))
            self.assertTrue(prefix.is_dir())
            devices = prefix / 'pfx/dosdevices'
            devices.mkdir(parents=True)
            (devices / 'z:').symlink_to('/')
            self.write_sdk_files()

        with patch.object(dependencies.subprocess, 'run', side_effect=install):
            report = dependencies.prepare_sdk(self.sdk_output, self.sdk_installer,
                                              self.proton, self.proton.parent)
        self.assertFalse(report['reused'])
        self.assertEqual(len(report['selected_identities']), 8)
        self.assertEqual(len(prefixes), 1)
        self.assertFalse(prefixes[0].exists())

    def test_complete_sdk_needs_no_installer_proton_or_network(self):
        self.write_sdk_files()
        with patch.object(dependencies.subprocess, 'run', side_effect=AssertionError('unexpected install')):
            report = dependencies.prepare_sdk(self.sdk_output)
        self.assertTrue(report['reused'])
        self.download.assert_not_called()

    def test_altered_sdk_is_rejected_without_running_installer(self):
        self.write_sdk_files()
        path = self.sdk_output / 'installed/Microsoft Visual C++ Toolkit 2003/include/xstring'
        path.write_bytes(b'altered header')
        (self.sdk_output / 'dependency-report.json').write_text('{"reused": true}')
        with patch.object(dependencies.subprocess, 'run') as install:
            with self.assertRaisesRegex(RuntimeError, 'pinned target dependency differs'):
                dependencies.prepare_sdk(self.sdk_output)
        install.assert_not_called()
        self.assertFalse((self.sdk_output / 'dependency-report.json').exists())

    def test_runtime_reuses_verified_payload_and_notices_without_extraction(self):
        mocks, extract = self.runtime_mocks()
        with mocks:
            first = dependencies.prepare_runtime(self.runtime_output, self.runtime_installer)
            self.assertFalse(first['reused'])
            extract.reset_mock()
            (self.runtime_output / 'VC_redist.x86.exe').unlink()
            second = dependencies.prepare_runtime(self.runtime_output, seven_zip='absent-7z')
            self.assertTrue(second['reused'])
            extract.assert_not_called()
        self.download.assert_not_called()

    def test_missing_runtime_notices_trigger_extraction(self):
        mocks, extract = self.runtime_mocks()
        with mocks:
            dependencies.prepare_runtime(self.runtime_output, self.runtime_installer)
            (self.runtime_output / 'notices/license.txt').unlink()
            extract.reset_mock()
            report = dependencies.prepare_runtime(self.runtime_output)
            self.assertFalse(report['reused'])
            self.assertEqual(extract.call_count, 3)
        self.assertTrue((self.runtime_output / 'notices/license.txt').is_file())

    def test_incomplete_runtime_report_triggers_extraction(self):
        mocks, extract = self.runtime_mocks()
        with mocks:
            dependencies.prepare_runtime(self.runtime_output, self.runtime_installer)
            (self.runtime_output / 'report.json').write_text('{"incomplete":')
            extract.reset_mock()
            report = dependencies.prepare_runtime(self.runtime_output)
            self.assertFalse(report['reused'])
            self.assertEqual(extract.call_count, 3)

    def test_altered_runtime_is_rejected_and_stale_success_removed(self):
        mocks, extract = self.runtime_mocks()
        with mocks:
            dependencies.prepare_runtime(self.runtime_output, self.runtime_installer)
            (self.runtime_output / 'minimum' / dependencies.RUNTIME_NAME).write_bytes(b'altered DLL')
            extract.reset_mock()
            with self.assertRaisesRegex(RuntimeError, 'SHA256 mismatch'):
                dependencies.prepare_runtime(self.runtime_output)
            extract.assert_not_called()
        self.assertFalse((self.runtime_output / 'report.json').exists())

    def test_only_runtime_does_not_require_sdk_or_proton(self):
        mocks, _ = self.runtime_mocks()
        with mocks, patch.object(dependencies, 'prepare_sdk', side_effect=AssertionError('unexpected SDK')):
            dependencies.main(['--only', 'runtime', '--output-dir', str(self.output),
                               '--runtime-installer', str(self.runtime_installer)])
        report = json.loads((self.output / 'report.json').read_text())
        self.assertTrue(report['pass'])
        self.assertEqual(set(report['dependencies']), {'runtime'})
        self.assertEqual(set(report['paths']), {'exception_runtime'})

    def test_complete_sdk_skips_while_runtime_is_extracted(self):
        self.write_sdk_files()
        mocks, _ = self.runtime_mocks()
        with mocks:
            dependencies.main(['--output-dir', str(self.output),
                               '--runtime-installer', str(self.runtime_installer)])
        report = json.loads((self.output / 'report.json').read_text())
        self.assertTrue(report['pass'])
        self.assertTrue(report['dependencies']['sdk']['reused'])
        self.assertFalse(report['dependencies']['runtime']['reused'])
        self.assertEqual(set(report['paths']), {'vc71', 'windows_sdk', 'exception_runtime'})

    @unittest.skipIf(dependencies.os.name == 'nt', 'Proton is only used on Linux')
    def test_missing_linux_sdk_records_failed_attempt(self):
        (self.output / 'report.json').write_text('{"pass": true}')
        with self.assertRaisesRegex(ValueError, '--proton and --steam-client are required'):
            dependencies.main(['--output-dir', str(self.output)])
        report = json.loads((self.output / 'report.json').read_text())
        self.assertFalse(report['pass'])
        self.assertIn('error', report)

    def test_unpinned_download_is_removed(self):
        target = self.output / 'download.exe'
        with patch.object(dependencies.urllib.request, 'urlopen', return_value=io.BytesIO(b'wrong download')):
            with self.assertRaisesRegex(RuntimeError, 'SHA256 mismatch'):
                dependencies.acquire(None, target, 'https://example.invalid/installer', '0' * 64)
        self.assertFalse(target.exists())
        self.assertFalse(target.with_suffix('.exe.partial').exists())

    def test_output_directory_cannot_escape_ignored_tmp(self):
        for path in [self.root / 'tmp', self.root / 'outside']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                build_support.output_directory(path)


if __name__ == '__main__':
    unittest.main()
