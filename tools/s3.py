#!/usr/bin/env python3
"""Build DoC in C++23 and verify its original PE32 imports and exports."""
import argparse
import collections
import datetime
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

sys.dont_write_bytecode = True
import build_support as support
import pefile

ROOT = support.ROOT
LOCK = json.loads((ROOT / 'tools/s3-lock.json').read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['bts-dir', 'llvm-bin', 'vc71', 'windows-sdk', 'exception-runtime']:
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--reference-dll', type=Path, required=True, help='original mod DLL for additional export coverage')
    parser.add_argument('--icu70-dir', type=Path, help='required for the pinned Linux LLVM package')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'tmp/s3-build')
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--cmake', default='cmake')
    args = parser.parse_args()
    windows_host = sys.platform == 'win32'
    if not windows_host and args.icu70_dir is None:
        parser.error('--icu70-dir is required on Linux')
    if args.jobs < 1:
        parser.error('jobs must be positive')
    output = args.output_dir.resolve()
    if not output.is_relative_to(ROOT / 'tmp') or output == ROOT / 'tmp':
        parser.error('output-dir must be a dedicated ignored directory under repo tmp/')
    output.mkdir(parents=True, exist_ok=True)
    report_path = output / 'report.json'
    attempt = output / 'attempts' / datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    attempt.mkdir(parents=True)
    if report_path.exists():
        (attempt / 'previous-report.json').write_bytes(report_path.read_bytes())
    report_path.unlink(missing_ok=True)
    commands = []
    report = {'pass': False, 'scope': 'DoC C++23 build and original symbol coverage only',
              'commands': commands, 'runtime_tested': False}
    try:
        if support.digest(args.reference_dll) != LOCK['mod_reference_sha256']:
            raise RuntimeError('original DoC DLL differs from the pinned mod baseline')
        if pefile.__version__ != support.LOCK['pefile_version']:
            raise RuntimeError('pinned pefile version differs')
        tool_pins = json.loads((ROOT / 'tools/s3-windows-lock.json').read_text())['tools'] if windows_host else {
            **support.LOCK['tools'], **LOCK['tools']}
        for name, expected in tool_pins.items():
            if support.digest(args.llvm_bin / name) != expected:
                raise RuntimeError(f'pinned LLVM tool differs: {name}')
        if not windows_host:
            for name, expected in support.LOCK['icu70'].items():
                if support.digest(args.icu70_dir / name) != expected:
                    raise RuntimeError(f'pinned linker dependency differs: {name}')
        if support.digest(args.exception_runtime) != LOCK['exception_runtime_sha256']:
            raise RuntimeError('pinned native exception provider differs')
        library_paths = {'source/python24.lib': ROOT / 'CvGameCoreDLL/Python24/libs/python24.lib',
                         'source/boost_python-vc71-mt-1_32.lib': ROOT / 'CvGameCoreDLL/Boost-1.32.0/libs/boost_python-vc71-mt-1_32.lib'}
        for name, expected in LOCK['link_inputs'].items():
            path = library_paths.get(name) if name.startswith('source/') else args.windows_sdk / 'lib' / name.split('/', 1)[1]
            if support.digest(path) != expected:
                raise RuntimeError(f'pinned import library differs: {name}')
        for name, pin in support.LOCK['installed_images'].items():
            if support.digest(args.bts_dir / name) != pin['sha256']:
                raise RuntimeError(f'pinned original differs: {name}')
        env = dict(os.environ)
        if not windows_host:
            env['LD_LIBRARY_PATH'] = str(args.icu70_dir.resolve())
        configure = [args.cmake, '-S', ROOT, '-B', output, '-G', 'Ninja',
                     '-DCMAKE_TOOLCHAIN_FILE=' + (ROOT / 'cmake/windows-x86-clang.cmake').as_posix(),
                     '-DCMAKE_BUILD_TYPE=Release', '-DPython3_EXECUTABLE=' + Path(sys.executable).as_posix(),
                     '-DBRIDGED_LLVM_BIN=' + args.llvm_bin.resolve().as_posix(),
                     '-DBRIDGED_VC71=' + args.vc71.resolve().as_posix(),
                     '-DBRIDGED_WINDOWS_SDK=' + args.windows_sdk.resolve().as_posix(),
                     '-DBRIDGED_EXCEPTION_RUNTIME=' + args.exception_runtime.resolve().as_posix()]
        for command, name in [(configure, 'configure.log'),
                              ([args.cmake, '--build', output, '--parallel', str(args.jobs)], 'build.log')]:
            command = [str(item) for item in command]
            commands.append(command)
            with (attempt / name).open('w') as log:
                subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
        binary = output / 'CvGameCoreDLL.dll'
        pe, image = support.pe_summary(binary)
        if (image['machine'], image['magic']) != (0x14c, 0x10b):
            raise RuntimeError('SDK output is not PE32/i386')
        original_exe = pefile.PE(str(args.bts_dir / 'Civ4BeyondSword.exe'))
        required = {item.name.decode() for entry in original_exe.DIRECTORY_ENTRY_DELAY_IMPORT
                    if entry.dll.lower() == b'cvgamecoredll.dll' for item in entry.imports if item.name}
        missing = sorted(required - set(image['exports']))
        if missing:
            raise RuntimeError(f'missing stock exports: {missing}')
        _, stock = support.pe_summary(args.bts_dir / 'Assets/CvGameCoreDLL.dll')
        missing_stock_public = sorted(set(stock['exports']) - set(image['exports']))
        _, reference = support.pe_summary(args.reference_dll)
        missing_public = sorted(set(reference['exports']) - set(image['exports']))
        if missing_public:
            raise RuntimeError(f'missing original public exports: {missing_public}')
        providers = {path.name.lower(): path for path in args.bts_dir.iterdir() if path.is_file()}
        providers['vcruntime140.dll'] = args.exception_runtime
        system = {'kernel32.dll', 'user32.dll', 'winmm.dll', 'psapi.dll'}
        provider_hashes = {}
        provider_exports = {}
        for entry in image['imports']:
            name = entry['dll'].lower()
            if name in system:
                continue
            if name not in providers:
                raise RuntimeError(f'unaccounted runtime provider: {name}')
            path = providers[name]
            if name not in provider_exports:
                _, target = support.pe_summary(path)
                provider_hashes[name] = target['sha256']
                provider_exports[name] = set(target['exports'])
            if entry['name'] not in provider_exports[name]:
                raise RuntimeError(f'import missing from pinned provider: {entry}')
            if name == 'vcruntime140.dll' and entry['name'] not in {'__CxxFrameHandler3', '_CxxThrowException'}:
                raise RuntimeError('supplemental runtime supplies more than the measured EH pair')
        if support.digest(output / 'vcruntime140.dll') != LOCK['exception_runtime_sha256']:
            raise RuntimeError('copied native exception provider differs')
        database = json.loads((output / 'compile_commands.json').read_text())
        expected_sources = {path.resolve() for path in (ROOT / 'CvGameCoreDLL').glob('*.cpp')}
        if {Path(row['file']).resolve() for row in database} != expected_sources:
            raise RuntimeError('compile inventory differs from inherited Makefile direct sources')
        for row in database:
            flags = row.get('arguments') or shlex.split(row['command'], posix=not windows_host)
            required_flags = {'-std=c++23', '-O2', '-D_DLL', '-D_MT',
                              '--target=i686-pc-windows-msvc', '-fms-compatibility-version=13.10',
                              '-fno-sized-deallocation', '-fno-threadsafe-statics', '-fcheck-new',
                              '-fno-wchar', '-fno-strict-aliasing', '-ffp-contract=off', '-Wall', '-Wextra', '-D_MOD_FRACTRADE'}
            if not required_flags.issubset(flags) or any(flag in flags for flag in ['-O3', '-ffast-math']):
                raise RuntimeError('a unit does not use the required target/language/helper configuration')
            obj = Path(row['output'])
            if not obj.is_absolute():
                obj = Path(row['directory']) / obj
            if not obj.exists() or obj.read_bytes()[:2] != b'\x4c\x01':
                raise RuntimeError(f'missing/non-i386 object: {obj}')
        log = (attempt / 'build.log').read_text()
        libraries = [args.vc71 / 'lib' / name for name in ['msvcrt.lib', 'msvcprt.lib', 'oldnames.lib']]
        libraries += [args.windows_sdk / 'lib' / name for name in ['Kernel32.Lib', 'User32.Lib', 'WinMM.Lib', 'Psapi.Lib']]
        libraries += [ROOT / 'CvGameCoreDLL/Python24/libs/python24.lib',
                      ROOT / 'CvGameCoreDLL/Boost-1.32.0/libs/boost_python-vc71-mt-1_32.lib',
                      output / 'vcruntime-handler.lib']
        report.update(mod_reference=reference, host=sys.platform, tool_sha256=tool_pins,
                      binary=image, required_exports=len(required), missing_exports=missing,
                      original_public_exports=len(reference['exports']), missing_public_exports=missing_public,
                      missing_stock_public_exports=missing_stock_public,
                      added_public_exports=sorted(set(image['exports']) - set(reference['exports'])),
                      units=len(database), provider_hashes=provider_hashes,
                      link_library_sha256={str(path): support.digest(path) for path in libraries},
                      logs={name: {'path': str(attempt / name), 'sha256': support.digest(attempt / name)}
                            for name in ['configure.log', 'build.log']},
                      compiled_units_this_attempt=len(re.findall(r'Building CXX object ', log)),
                      warning_scope='This invocation only; retained earlier logs cover earlier compilations',
                      compile_database_sha256=support.digest(output / 'compile_commands.json'),
                      header_inputs_sha256=support.digest(output / 'compat-headers/inputs.json'),
                      generated_header_sha256={str(output / 'compat-headers' / name):
                                              support.digest(output / 'compat-headers' / name)
                                              for name in ['overlay.json', 'sal.h', 'vc71-xstring']},
                      warnings=dict(collections.Counter(re.findall(r'\[(-W[^\]]+)\]', log))),
                      source_sha256={str(path): support.digest(path) for path in
                          [*(ROOT / 'CvGameCoreDLL').glob('*.cpp'), *(ROOT / 'CvGameCoreDLL').glob('*.h'),
                           ROOT / 'CMakeLists.txt', ROOT / 'cmake/windows-x86-clang.cmake',
                           ROOT / 'compat/vc71_prelude.h', ROOT / 'tools/s3_headers.py',
                           ROOT / 'tools/s3-lock.json', ROOT / 'tools/s1-lock.json',
                           ROOT / 'tools/s3-windows-lock.json',
                           ROOT / 'tools/build_support.py', Path(__file__)]})
        report['pass'] = True
    except Exception as error:
        report['error'] = str(error)
        raise
    finally:
        support.write_json(report_path, report)
    print(json.dumps({'build_pass': report['pass'], 'runtime_tested': False,
                      'units': report['units'], 'required_exports': report['required_exports'],
                      'report': str(report_path)}, indent=2))


if __name__ == '__main__':
    main()
