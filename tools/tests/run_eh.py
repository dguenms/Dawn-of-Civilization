#!/usr/bin/env python3
"""Compare the static PE32 handler with original VC7.1 catches and native FH3."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_support as support
import pefile

ROOT = support.ROOT
SOURCE = Path(__file__).resolve().parent


def winpath(path):
    return 'Z:' + str(path.resolve()).replace('/', '\\')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['bts-dir', 'llvm-bin', 'icu70-dir', 'proton', 'steam-client']:
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--deps-dir', type=Path, default=ROOT / 'tmp/dependencies')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'tmp/eh-validation')
    parser.add_argument('--native-runtime', type=Path, help='optional pinned native-pair comparison')
    parser.add_argument('--prefix', type=Path, help='existing disposable prefix under repo tmp/')
    args = parser.parse_args()
    output = support.output_directory(args.output_dir)
    prefix = args.prefix.resolve() if args.prefix else output / 'proton-prefix'
    if not prefix.is_relative_to(ROOT / 'tmp') or prefix == ROOT / 'tmp':
        parser.error('prefix must be disposable and contained in repo tmp/')
    prefix.mkdir(exist_ok=True, parents=True)
    inputs = support.dependency_paths(args.deps_dir)
    vc = inputs['vc71']
    sdk = inputs['windows_sdk']
    compiler = args.llvm_bin / 'clang++'
    env = dict(os.environ, LD_LIBRARY_PATH=str(args.icu70_dir.resolve()))
    proton_env = dict(env, STEAM_COMPAT_DATA_PATH=str(prefix),
                      STEAM_COMPAT_CLIENT_INSTALL_PATH=str(args.steam_client.resolve()),
                      WINEDLLOVERRIDES='msvcr71,msvcp71=n;winedbg.exe=d', WINEDEBUG='-all')
    commands = []
    report = {'pass': False, 'commands': commands, 'runs': [],
              'scope': 'Original-provider exception and lifetime probes; no game gate',
              'source_sha256': {str(p.relative_to(ROOT)): support.digest(p) for p in
                  [*sorted(SOURCE.glob('eh_*')), ROOT / 'compat/msvc_eh.cpp',
                   ROOT / 'compat/msvc_eh_abi.h', ROOT / 'compat/msvc_eh_x86.s', Path(__file__)]}}
    report_path = output / 'report.json'
    report_path.unlink(missing_ok=True)

    def run(command, log, environment=env, expected=0):
        command = [str(x) for x in command]
        commands.append(command)
        with log.open('wb') as stream:
            result = subprocess.run(command, env=environment, cwd=output,
                                    stdout=stream, stderr=subprocess.STDOUT, timeout=60)
        if expected is not None and result.returncode != expected:
            raise RuntimeError(f'command exit {result.returncode}, expected {expected}: {log}')
        return result.returncode

    try:
        for name, identity in support.LOCK['tools'].items():
            support.require_hash(args.llvm_bin / name, identity)
        for name, identity in support.LOCK['icu70'].items():
            support.require_hash(args.icu70_dir / name, identity)
        support.require_hash(args.proton, support.LOCK['proton_launcher_sha256'])
        if (args.proton.parent / 'version').read_text().strip() != support.LOCK['proton_version']:
            raise RuntimeError('pinned Proton version differs')
        crt = args.bts_dir / 'msvcr71.dll'
        support.require_hash(crt, support.LOCK['installed_images']['msvcr71.dll']['sha256'])
        if args.native_runtime:
            support.require_hash(args.native_runtime,
                                 json.loads((ROOT / 'tools/link-lock.json').read_text())['exception_runtime_sha256'])
        definitions = output / 'kernel32.def'
        definitions.write_text('LIBRARY kernel32.dll\nEXPORTS\n' + ''.join(
            '  ' + name + '@' + str(size) + '\n' for name, size in {
                'LoadLibraryExA': 12, 'FreeLibrary': 4, 'GetProcAddress': 8,
                'GetEnvironmentVariableA': 12, 'GetModuleFileNameA': 12,
                'GetStdHandle': 4, 'CreateFileA': 28, 'WriteFile': 20, 'ExitProcess': 4}.items()))
        run([args.llvm_bin / 'llvm-dlltool', '-m', 'i386', '-k', '-d', definitions,
             '-l', output / 'kernel32.lib'], output / 'kernel-import.log')
        old_obj = output / 'legacy.obj'
        old_env = dict(proton_env, INCLUDE=winpath(vc / 'include'))
        run([args.proton, 'run', vc / 'bin/cl.exe', '/nologo', '/O2', '/MD', '/EHsc',
             '/c', '/Fo' + winpath(old_obj), winpath(SOURCE / 'eh_legacy.cpp')],
            output / 'legacy-compile.log', old_env)
        legacy = output / 'LegacyEH.dll'
        run([args.llvm_bin / 'lld-link', '/machine:x86', '/nodefaultlib', '/timestamp:0',
             '/dll', '/entry:_DllMainCRTStartup@12', '/out:' + str(legacy), old_obj,
             vc / 'lib/msvcrt.lib', sdk / 'lib/Kernel32.Lib'], output / 'legacy-link.log')
        report['legacy_compiler_sha256'] = support.digest(vc / 'bin/cl.exe')
        modes = ['static', 'native'] if args.native_runtime else ['static']
        for optimization in ['0', '2']:
            for mode in modes:
                target = output / (mode + '-O' + optimization)
                target.mkdir(exist_ok=True)
                modern = target / 'ModernEH.dll'
                helper = []
                flags = ['--target=i686-pc-windows-msvc', '-std=c++23', '-O' + optimization,
                         '-fms-extensions', '-fms-compatibility-version=13.10',
                         '-fno-sized-deallocation', '-fno-threadsafe-statics',
                         '-fcheck-new', '-fno-stack-protector', '-D_MT', '-D_DLL',
                         '-Wall', '-Wextra', '-Werror', '-isystem', vc / 'include']
                for name in ['eh_cases', 'eh_async']:
                    obj = target / (name + '.obj')
                    run([compiler, *flags, '-c', SOURCE / (name + '.cpp'), '-o', obj],
                        target / (name + '-compile.log'))
                    helper.append(obj)
                if mode == 'static':
                    strict = ['--target=i686-pc-windows-msvc', '-std=c++23', '-O' + optimization,
                              '-pedantic-errors', '-Wall', '-Wextra', '-Werror',
                              '-ffreestanding', '-fno-builtin', '-fno-exceptions',
                              '-fno-rtti', '-fno-stack-protector', '-fms-extensions']
                    run([compiler, *strict, '-c', ROOT / 'compat/msvc_eh.cpp', '-o', target / 'adapter.obj'], target / 'adapter-compile.log')
                    run([compiler, '--target=i686-pc-windows-msvc', '-c', ROOT / 'compat/msvc_eh_x86.s', '-o', target / 'adapter-asm.obj'], target / 'adapter-asm.log')
                    helper += [target / 'adapter.obj', target / 'adapter-asm.obj']
                else:
                    definition = target / 'native.def'
                    definition.write_text('LIBRARY vcruntime140.dll\nEXPORTS\n  __CxxFrameHandler3\n  _CxxThrowException@8\n')
                    run([args.llvm_bin / 'llvm-dlltool', '-m', 'i386', '-k', '-d', definition,
                         '-l', target / 'native.lib'], target / 'native-import.log')
                    helper += [target / 'native.lib']
                    (target / 'vcruntime140.dll').write_bytes(args.native_runtime.read_bytes())
                run([args.llvm_bin / 'lld-link', '/machine:x86', '/nodefaultlib', '/timestamp:0',
                     '/dll', '/entry:_DllMainCRTStartup@12', '/out:' + str(modern), *helper,
                     *(['/export:__CxxFrameHandler3'] if mode == 'static' else []),
                     vc / 'lib/msvcrt.lib', sdk / 'lib/Kernel32.Lib'], target / 'modern-link.log')
                _, metadata = support.pe_summary(modern)
                report.setdefault('binaries', {})[target.name] = metadata
                if mode == 'static' and any(e['dll'].lower().startswith(('vcruntime', 'ucrtbase', 'api-ms-win-crt-')) for e in metadata['imports']):
                    raise RuntimeError('static diagnostic imports a modern CRT')
                (target / 'eh_inputs.h').write_text('\n'.join(
                    'constexpr const char* ' + key + ' = ' + json.dumps(winpath(value) if value else '') + ';'
                    for key, value in {'crt_path': crt, 'native_path': target / 'vcruntime140.dll' if mode == 'native' else None,
                                       'legacy_path': legacy, 'modern_path': modern}.items()) + '\n')
                loader = target / 'loader.exe'
                run([compiler, '--target=i686-pc-windows-msvc', '-c', SOURCE / 'eh_audit.s',
                     '-o', target / 'audit.obj'], target / 'audit-compile.log')
                run([compiler, '--target=i686-pc-windows-msvc', '-std=c++23', '-O2',
                     '-pedantic-errors', '-Wall', '-Wextra', '-Werror', '-fms-extensions',
                     '-ffreestanding', '-fno-builtin', '-fno-exceptions', '-fno-rtti',
                     '-fno-stack-protector', '-I', target, '-c', SOURCE / 'eh_loader.cpp',
                     '-o', target / 'loader.obj'], target / 'loader-compile.log')
                run([args.llvm_bin / 'lld-link', '/machine:x86', '/nodefaultlib', '/timestamp:0',
                     '/entry:entry@0', '/subsystem:console', '/out:' + str(loader),
                     target / 'loader.obj', target / 'audit.obj', output / 'kernel32.lib'], target / 'loader-link.log')
                for case in ['suite', '0', '1', '2', '3']:
                    log = target / (case + '.log')
                    trace = target / (case + '.jsonl')
                    trace.unlink(missing_ok=True)
                    runtime_env = dict(proton_env, BRIDGED_EH_CASE=case, BRIDGED_EH_TRACE=winpath(trace))
                    if mode == 'native': runtime_env['WINEDLLOVERRIDES'] += ';vcruntime140=n'
                    exit_code = run([args.proton, 'run', loader], log, runtime_env, expected=None)
                    events = [json.loads(line) for line in trace.read_text().splitlines()] if trace.exists() else []
                    for event in events:
                        if 'provider' not in event: continue
                        path = Path(bytes.fromhex(event['path_hex']).decode()[2:].replace('\\', '/'))
                        expected = {'msvcr71.dll': crt, 'LegacyEH.dll': legacy, 'ModernEH.dll': modern,
                                    'static_handler': modern, 'vcruntime140.dll': target / 'vcruntime140.dll'}[event['provider']]
                        if path.resolve() != expected.resolve() or support.digest(path) != support.digest(expected):
                            raise RuntimeError('loaded provider path/bytes differ')
                        pe = pefile.PE(str(expected))
                        entry = {'msvcr71.dll': '__CxxFrameHandler', 'LegacyEH.dll': 'legacy_rethrow',
                                 'ModernEH.dll': 'eh_suite', 'static_handler': '__CxxFrameHandler3',
                                 'vcruntime140.dll': '__CxxFrameHandler3'}[event['provider']]
                        symbol = next(e for e in pe.DIRECTORY_ENTRY_EXPORT.symbols if e.name == entry.encode())
                        if symbol.forwarder or symbol.address != event['rva']:
                            raise RuntimeError('loaded export RVA differs')
                        pe.relocate_image(event['base'])
                        if pe.get_data(event['rva'], 32).hex() != event['code_hex']:
                            raise RuntimeError('loaded provider code differs')
                    values = {e['name']: e['value'] for e in events if 'name' in e}
                    required_providers = {'msvcr71.dll', 'LegacyEH.dll', 'ModernEH.dll',
                                          'static_handler' if mode == 'static' else 'vcruntime140.dll'}
                    if {e['provider'] for e in events if 'provider' in e} != required_providers:
                        raise RuntimeError('loaded provider evidence is incomplete')
                    passed = (exit_code == 0 and values.get('complete') == 1 and
                              all(v == 1 for v in values.values()) and
                              'asynchronous_cpp_caught' not in values) if case == 'suite' else (
                                  exit_code == 77 and values.get('terminate_handler') == 1 and
                                  'unexpected_survival' not in values)
                    row = dict(mode=mode, optimization=optimization, case=case, exit=exit_code,
                               pass_=passed, values=values, providers=[e for e in events if 'provider' in e],
                               log=str(log), log_sha256=support.digest(log))
                    # Native modern throws keep a different CRT's uncaught
                    # state. Preserve this observed stock-query mismatch rather
                    # than counting it as agreement or hiding other failures.
                    row['known_native_state_difference'] = (
                        mode == 'native' and case == 'suite' and exit_code == 95 and
                        values.get('legacy_uncaught_state') == 0 and values.get('complete') == 1 and
                        all(v == 1 for k, v in values.items() if k != 'legacy_uncaught_state') and
                        'asynchronous_cpp_caught' not in values)
                    report['runs'].append(row)
                    support.write_json(report_path, report)
                    print(json.dumps({k: row[k] for k in ['mode', 'optimization', 'case', 'exit', 'pass_', 'values']}), flush=True)
        report['static_stock_contract_pass'] = all(r['pass_'] for r in report['runs'] if r['mode'] == 'static')
        report['native_stock_query_differences'] = [dict(optimization=r['optimization'], query='legacy_uncaught_state')
            for r in report['runs'] if r['known_native_state_difference']]
        report['pass'] = report['static_stock_contract_pass'] and all(
            r['pass_'] or r['known_native_state_difference'] for r in report['runs'])
    except Exception as error:
        report['error'] = str(error)
        raise
    finally:
        support.write_json(report_path, report)
    if not report['pass']: raise SystemExit('Exception fixture failed; inspect ' + str(report_path))


if __name__ == '__main__':
    main()
