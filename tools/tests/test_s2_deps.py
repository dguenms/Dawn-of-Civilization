"""Keep the SDK installer's Wine drive mappings out of the playable mod."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    's2_deps', Path(__file__).resolve().parents[1] / 's2_deps.py')
s2_deps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s2_deps)


@unittest.skipIf(s2_deps.os.name == 'nt', 'Proton is only used on Linux')
class InstallerPrefixTest(unittest.TestCase):
    def test_installer_drive_mapping_is_outside_mod_and_cleaned_up(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'mod'
            output = root / 'tmp/s2-deps'
            output.mkdir(parents=True)
            installer = output / 'civ4-sdk-setup.exe'
            installer.write_bytes(b'test installer')
            proton = Path(directory) / 'proton'
            proton.write_bytes(b'test proton')
            (proton.parent / 'version').write_text('test version')
            (root / 'tools').mkdir()
            (root / 'tools/s1-lock.json').write_text(json.dumps({
                'proton_launcher_sha256': s2_deps.digest(proton),
                'proton_version': 'test version',
            }))
            prefixes = []

            def install(command, *, env, **kwargs):
                prefix = Path(env['STEAM_COMPAT_DATA_PATH'])
                prefixes.append(prefix)
                self.assertFalse(prefix.resolve().is_relative_to(root.resolve()))
                self.assertTrue(prefix.is_dir())
                devices = prefix / 'pfx/dosdevices'
                devices.mkdir(parents=True)
                (devices / 'z:').symlink_to('/')
                files = [
                    'Microsoft Visual C++ Toolkit 2003/include/xstring',
                    'Microsoft Visual C++ Toolkit 2003/include/yvals.h',
                    'Microsoft Visual C++ Toolkit 2003/include/typeinfo',
                    'Microsoft Visual C++ Toolkit 2003/lib/msvcrt.lib',
                    'Microsoft Visual C++ Toolkit 2003/lib/msvcprt.lib',
                    'Microsoft Visual C++ Toolkit 2003/EULA.txt',
                    'WindowsSDK/include/BaseTsd.h',
                    'WindowsSDK/lib/Kernel32.Lib',
                ]
                for name in files:
                    path = output / 'installed' / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(b'test dependency')

            with patch.object(s2_deps, 'ROOT', root), \
                    patch.object(s2_deps, 'SHA256', hashlib.sha256(installer.read_bytes()).hexdigest()), \
                    patch.object(s2_deps.subprocess, 'run', side_effect=install), \
                    patch('sys.argv', ['s2_deps.py', '--proton', str(proton),
                                       '--steam-client', directory]):
                s2_deps.main()

            self.assertEqual(len(prefixes), 1)
            self.assertFalse(prefixes[0].exists())
            report = json.loads((output / 'dependency-report.json').read_text())
            self.assertEqual(len(report['selected_identities']), 8)
            self.assertFalse((output / 'proton-prefix').exists())


if __name__ == '__main__':
    unittest.main()
