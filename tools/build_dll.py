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
import eh_metadata
import pefile

ROOT = support.ROOT
LOCK = json.loads((ROOT / 'tools/link-lock.json').read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['bts-dir', 'llvm-bin']:
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--deps-dir', type=Path, default=ROOT / 'tmp/dependencies',
                        help='dependencies prepared by prepare_dependencies.py')
    for name in ['vc71', 'windows-sdk']:
        parser.add_argument('--' + name, type=Path, help='override the prepared dependency path')
    parser.add_argument('--reference-dll', type=Path, required=True,
                        help='original mod DLL for additional export coverage')
    parser.add_argument('--icu70-dir', type=Path, help='required for the pinned Linux LLVM package')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'tmp/dll-build')
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--cmake', default='cmake')
    args = parser.parse_args()
    for name, path in support.dependency_paths(args.deps_dir).items():
        if getattr(args, name) is None:
            setattr(args, name, path)
    windows_host = sys.platform == 'win32'
    if not windows_host and args.icu70_dir is None:
        parser.error('--icu70-dir is required on Linux')
    if args.jobs < 1:
        parser.error('jobs must be positive')
    try:
        output = support.output_directory(args.output_dir)
    except ValueError as error:
        parser.error(str(error))
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
        for name in support.dependency_paths():
            if not getattr(args, name).exists():
                raise RuntimeError(f'missing {name.replace("_", "-")}: {getattr(args, name)}; '
                                   'run tools/prepare_dependencies.py or pass an explicit path')
        if pefile.__version__ != support.LOCK['pefile_version']:
            raise RuntimeError('pinned pefile version differs')
        tool_pins = json.loads((ROOT / 'tools/windows-toolchain-lock.json').read_text())['tools'] if windows_host else {
            **support.LOCK['tools'], **LOCK['tools']}
        for name, expected in tool_pins.items():
            if support.digest(args.llvm_bin / name) != expected:
                raise RuntimeError(f'pinned LLVM tool differs: {name}')
        if not windows_host:
            for name, expected in support.LOCK['icu70'].items():
                if support.digest(args.icu70_dir / name) != expected:
                    raise RuntimeError(f'pinned linker dependency differs: {name}')
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
                     '-DBRIDGED_WINDOWS_SDK=' + args.windows_sdk.resolve().as_posix()]
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
        system = {'kernel32.dll', 'user32.dll', 'winmm.dll', 'psapi.dll'}
        provider_hashes = {}
        provider_exports = {}
        for entry in image['imports']:
            name = entry['dll'].lower()
            if (name.startswith(('vcruntime', 'ucrtbase', 'api-ms-win-crt-')) or
                    (name.startswith(('msvcr', 'msvcp')) and name not in {'msvcr71.dll', 'msvcp71.dll'})):
                raise RuntimeError(f'supplemental modern CRT import is forbidden: {entry}')
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
        legacy_eh_names = {'__CxxFrameHandler', '_CxxThrowException', '?terminate@@YAXXZ'}
        legacy_eh_imports = [entry for entry in image['imports'] if entry['name'] in legacy_eh_names]
        missing_legacy_eh = legacy_eh_names - {entry['name'] for entry in legacy_eh_imports}
        if missing_legacy_eh:
            raise RuntimeError(f'missing legacy EH imports: {sorted(missing_legacy_eh)}')
        for entry in legacy_eh_imports:
            if entry['dll'].lower() != 'msvcr71.dll':
                raise RuntimeError(f'legacy EH import has unexpected provider: {entry}')
        database = json.loads((output / 'compile_commands.json').read_text())
        expected_sources = {path.resolve() for path in (ROOT / 'CvGameCoreDLL').glob('*.cpp')}
        adapter_sources = {ROOT / 'compat/msvc_eh.cpp', ROOT / 'compat/msvc_eh_x86.s'}
        adapter_sources = {path.resolve() for path in adapter_sources}
        rows_by_source = {Path(row['file']).resolve(): row for row in database}
        if len(rows_by_source) != len(database) or set(rows_by_source) != expected_sources | adapter_sources:
            raise RuntimeError('compile inventory differs from inherited Makefile direct sources')
        exception_metadata = {}
        for source, row in rows_by_source.items():
            flags = row.get('arguments') or shlex.split(row['command'], posix=not windows_host)
            compiler = args.llvm_bin / ('clang++.exe' if windows_host else 'clang++')
            if Path(flags[0].strip('"')).resolve() != compiler.resolve():
                raise RuntimeError(f'compile unit uses an unpinned driver: {source}: {flags[0]}; '
                                   'configure a fresh build directory with --output-dir')
            if source in expected_sources:
                required_flags = {'-std=c++23', '-O2', '-D_DLL', '-D_MT',
                                  '--target=i686-pc-windows-msvc', '-fms-compatibility-version=13.10',
                                  '-fno-sized-deallocation', '-fno-threadsafe-statics', '-fcheck-new',
                                  '-fno-wchar', '-fno-strict-aliasing', '-ffp-contract=off', '-Wall', '-Wextra', '-D_MOD_FRACTRADE'}
                if not required_flags.issubset(flags) or any(flag in flags for flag in ['-O3', '-ffast-math']):
                    raise RuntimeError('an SDK unit does not use the required target/language/helper configuration')
            elif source.suffix == '.cpp':
                required_flags = {'-std=c++23', '-pedantic-errors', '-Wall', '-Wextra', '-Werror',
                                  '-ffreestanding', '-fno-builtin', '-fno-exceptions', '-fno-rtti',
                                  '-fno-stack-protector', '-fms-extensions', '--target=i686-pc-windows-msvc'}
                if not required_flags.issubset(flags):
                    raise RuntimeError('EH adapter C++ unit lacks strict configuration')
            elif '--target=i686-pc-windows-msvc' not in flags:
                raise RuntimeError('EH adapter assembly lacks the i686 MSVC target')
            obj = Path(row['output'])
            if not obj.is_absolute():
                obj = Path(row['directory']) / obj
            if not obj.exists() or obj.read_bytes()[:2] != b'\x4c\x01':
                raise RuntimeError(f'missing/non-i386 object: {obj}')
            if source in expected_sources:
                exception_metadata[str(source.relative_to(ROOT))] = eh_metadata.inspect_object(obj)
        log = (attempt / 'build.log').read_text()
        libraries = [args.vc71 / 'lib' / name for name in ['msvcrt.lib', 'msvcprt.lib', 'oldnames.lib']]
        libraries += [args.windows_sdk / 'lib' / name for name in ['Kernel32.Lib', 'User32.Lib', 'WinMM.Lib', 'Psapi.Lib']]
        libraries += [ROOT / 'CvGameCoreDLL/Python24/libs/python24.lib',
                      ROOT / 'CvGameCoreDLL/Boost-1.32.0/libs/boost_python-vc71-mt-1_32.lib']
        report.update(mod_reference=reference, host=sys.platform, tool_sha256=tool_pins,
                      binary=image, required_exports=len(required), missing_exports=missing,
                      original_public_exports=len(reference['exports']), missing_public_exports=missing_public,
                      missing_stock_public_exports=missing_stock_public,
                      added_public_exports=sorted(set(image['exports']) - set(reference['exports'])),
                      units=len(expected_sources), adapter_units=len(adapter_sources),
                      exception_route='Static Clang EH3 to VC7.1 frame adapter; no supplemental CRT DLL',
                      legacy_eh_imports=legacy_eh_imports, provider_hashes=provider_hashes,
                      exception_metadata=exception_metadata,
                      exception_funcinfo_count=sum(row['funcinfo_count'] for row in exception_metadata.values()),
                      maximum_catch_clauses=max(row['max_catch_clauses'] for row in exception_metadata.values()),
                      link_library_sha256={str(path): support.digest(path) for path in libraries},
                      logs={name: {'path': str(attempt / name), 'sha256': support.digest(attempt / name)}
                            for name in ['configure.log', 'build.log']},
                      compiled_units_this_attempt=len(re.findall(r'Building CXX object .*CvGameCoreDLL', log)),
                      compiled_adapter_units_this_attempt=len(re.findall(r'Building (?:CXX|ASM) object .*msvc_eh', log)),
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
                           ROOT / 'compat/vc71_prelude.h', ROOT / 'compat/msvc_eh_abi.h',
                           ROOT / 'compat/msvc_eh.cpp', ROOT / 'compat/msvc_eh_x86.s',
                           ROOT / 'tools/prepare_headers.py',
                           ROOT / 'tools/link-lock.json', ROOT / 'tools/dependency-lock.json',
                           ROOT / 'tools/windows-toolchain-lock.json',
                           ROOT / 'tools/build_support.py', ROOT / 'tools/eh_metadata.py', Path(__file__)]})
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
