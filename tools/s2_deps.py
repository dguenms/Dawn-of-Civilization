#!/usr/bin/env python3
"""Acquire the user-selected VC7.1 header bundle into ignored local storage."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
URL = ('https://downloads.sourceforge.net/project/beyond-the-sword-sdk/'
       'Install%20Civ4%20Microsoft%20Windows%20SDK%20Visual%20C%20Toolkit.exe')
SHA256 = 'bf37b18eb095de7dad3b7e8508bbfbab23c0d5db21c8f0371502eb61914481a3'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def winpath(path):
    if os.name == 'nt':
        return str(path.resolve())
    return 'Z:' + str(path.resolve()).replace('/', '\\')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--proton', type=Path, help='required on Linux')
    parser.add_argument('--steam-client', type=Path, help='required on Linux')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'tmp/s2-deps')
    args = parser.parse_args()
    if os.name != 'nt' and (args.proton is None or args.steam_client is None):
        parser.error('--proton and --steam-client are required on Linux')
    output = args.output_dir.resolve()
    if not output.is_relative_to(ROOT / 'tmp') or output == ROOT / 'tmp':
        parser.error('output-dir must be a dedicated directory under ignored tmp/')
    output.mkdir(parents=True, exist_ok=True)
    report = output / 'dependency-report.json'
    report.unlink(missing_ok=True)
    installer = output / 'civ4-sdk-setup.exe'
    if not installer.exists():
        pending = output / 'download.partial'
        with urllib.request.urlopen(URL, timeout=90) as source, pending.open('wb') as destination:
            while block := source.read(1024 * 1024):
                destination.write(block)
        if digest(pending) != SHA256:
            raise RuntimeError('download differs from the pinned checksum')
        pending.rename(installer)
    if digest(installer) != SHA256:
        raise RuntimeError('SDK installer differs from the pinned checksum')
    if os.name != 'nt':
        # Pin Proton exactly as S1 does before executing the dependency installer.
        lock = json.loads((ROOT / 'tools/s1-lock.json').read_text())
        if digest(args.proton) != lock['proton_launcher_sha256'] or (
                args.proton.parent / 'version').read_text().strip() != lock['proton_version']:
            raise RuntimeError('pinned Proton differs')
    install = output / 'installed'
    prefix = output / 'proton-prefix'
    command = [str(installer), '/VERYSILENT', '/SP-',
               '/SUPPRESSMSGBOXES', '/NORESTART', '/NOICONS', '/NOCLOSEAPPLICATIONS',
               '/DIR=' + winpath(install), '/LOG=' + winpath(output / 'setup.log')]
    env = os.environ.copy()
    if os.name != 'nt':
        prefix.mkdir(exist_ok=True)
        command = [str(args.proton.resolve()), 'run', *command]
        env.update(STEAM_COMPAT_DATA_PATH=str(prefix),
                   STEAM_COMPAT_CLIENT_INSTALL_PATH=str(args.steam_client.resolve()), WINEDEBUG='-all')
    with (output / 'setup-proton.log').open('wb') as log:
        subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT,
                       timeout=180, check=True)
    toolkit = install / 'Microsoft Visual C++ Toolkit 2003'
    expected = [toolkit / 'include/xstring', toolkit / 'include/yvals.h',
                toolkit / 'include/typeinfo', toolkit / 'lib/msvcrt.lib',
                toolkit / 'lib/msvcprt.lib', toolkit / 'EULA.txt',
                install / 'WindowsSDK/include/BaseTsd.h', install / 'WindowsSDK/lib/Kernel32.Lib']
    identities = {str(path.relative_to(output)): digest(path) for path in expected}
    report.write_text(json.dumps({'schema': 1, 'url': URL, 'installer_sha256': SHA256,
        'proton_sha256': digest(args.proton) if os.name != 'nt' else None,
        'command': command, 'selected_identities': identities,
        'scope': 'Local target headers/import libraries. Clang remains the compiler. No dependency material is committed.'},
        indent=2, sort_keys=True) + '\n')
    print(report)


if __name__ == '__main__':
    main()
