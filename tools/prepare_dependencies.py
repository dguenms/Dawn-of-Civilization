#!/usr/bin/env python3
"""Prepare pinned VC7.1 SDK inputs and the x86 exception runtime in repo tmp/.

Verified dependencies are reused independently. The SDK installer runs only
when SDK files are missing; the redist is extracted without installation,
retaining its license/support payload beside the minimum-runtime payload.
"""

import argparse
from contextlib import ExitStack
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import urllib.request

from build_support import (ROOT, LOCK, dependency_paths, digest, output_directory,
                           require_hash, write_json)
import prepare_headers


SDK_URL = ('https://downloads.sourceforge.net/project/beyond-the-sword-sdk/'
           'Install%20Civ4%20Microsoft%20Windows%20SDK%20Visual%20C%20Toolkit.exe')
SDK_INSTALLER_SHA256 = 'bf37b18eb095de7dad3b7e8508bbfbab23c0d5db21c8f0371502eb61914481a3'
SDK_LICENSE_SHA256 = '8c6e5d64b09966dee7ae9f1d96dec0beec621fa13d6f9e0ba048e8aa06038c0f'
RUNTIME_URL = (
    "https://download.visualstudio.microsoft.com/download/pr/"
    "ece44298-3977-4f73-ab91-c13fe79cfea8/"
    "F0BAB33A302B3CDB2E11113760D016F54FD3D2632C65BA7834FAC4F0ABD7F1A3/"
    "VC_redist.x86.exe"
)
RUNTIME_SOURCE_PAGE = "https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist/"
RUNTIME_INSTALLER_SHA256 = "f0bab33a302b3cdb2e11113760d016f54fd3d2632c65ba7834fac4f0abd7f1a3"
RUNTIME_SHA256 = "2fa6efc053203460a23d3a25158f227d895d2dadc63acc1a372da97c3a4281c3"
RUNTIME_VERSION = "14.51.36247.0"
RUNTIME_CABINET_SIZES = {"notices": 139414, "payload": 6301985}
RUNTIME_NAME = "vcruntime140.dll_x86"
RUNTIME_EXPORTS = ("__CxxFrameHandler3", "_CxxThrowException")


def acquire(installer, target, url, expected):
    """Download or copy once, and check the pin before executing or extracting."""
    if installer is not None:
        source = installer.resolve(strict=True)
        require_hash(source, expected)
        if source != target:
            shutil.copyfile(source, target)
    elif not target.exists():
        partial = target.with_suffix(target.suffix + '.partial')
        try:
            with urllib.request.urlopen(url, timeout=60) as response, partial.open("wb") as stream:
                shutil.copyfileobj(response, stream)
            require_hash(partial, expected)
            partial.replace(target)
        finally:
            partial.unlink(missing_ok=True)
    require_hash(target, expected)
    return target


def winpath(path):
    if os.name == 'nt':
        return str(path.resolve())
    return 'Z:' + str(path.resolve()).replace('/', '\\')


def sdk_identities(install):
    toolkit = install / 'Microsoft Visual C++ Toolkit 2003'
    sdk = install / 'WindowsSDK'
    prepare_headers.verify_inputs(toolkit, sdk)
    require_hash(toolkit / 'EULA.txt', SDK_LICENSE_SHA256)
    link_pins = json.loads((ROOT / 'tools/link-lock.json').read_text())['link_inputs']
    for name, expected in link_pins.items():
        if name.startswith('sdk/'):
            require_hash(sdk / 'lib' / name.split('/', 1)[1], expected)
    expected = [toolkit / 'include/xstring', toolkit / 'include/yvals.h',
                toolkit / 'include/typeinfo', toolkit / 'lib/msvcrt.lib',
                toolkit / 'lib/msvcprt.lib', toolkit / 'EULA.txt',
                sdk / 'include/BaseTsd.h', sdk / 'lib/Kernel32.Lib']
    return {str(path.relative_to(install.parent)): digest(path) for path in expected}


def prepare_sdk(output, installer=None, proton=None, steam_client=None):
    output.mkdir(parents=True, exist_ok=True)
    report_path = output / 'dependency-report.json'
    install = output / 'installed'
    report_path.unlink(missing_ok=True)
    cached_installer = output / 'civ4-sdk-setup.exe'
    if installer is not None:
        require_hash(installer, SDK_INSTALLER_SHA256)
    if cached_installer.exists():
        require_hash(cached_installer, SDK_INSTALLER_SHA256)
    try:
        identities = sdk_identities(install)
        reused = True
    except FileNotFoundError:
        if os.name != 'nt':
            if proton is None or steam_client is None:
                raise ValueError('--proton and --steam-client are required to install missing SDK files on Linux')
            require_hash(proton, LOCK['proton_launcher_sha256'])
            if (proton.parent / 'version').read_text().strip() != LOCK['proton_version']:
                raise RuntimeError('pinned Proton version differs')
        installer = acquire(installer, cached_installer, SDK_URL, SDK_INSTALLER_SHA256)
        command = [str(installer), '/VERYSILENT', '/SP-', '/SUPPRESSMSGBOXES',
                   '/NORESTART', '/NOICONS', '/NOCLOSEAPPLICATIONS',
                   '/DIR=' + winpath(install), '/LOG=' + winpath(output / 'setup.log')]
        env = os.environ.copy()
        with ExitStack() as stack:
            if os.name != 'nt':
                # Keep Wine's dosdevices/z: -> / outside the playable mod.
                # BtS recursively scans mods, including symlink targets.
                prefix = stack.enter_context(tempfile.TemporaryDirectory(prefix='civ4-sdk-proton-'))
                command = [str(proton.resolve()), 'run', *command]
                env.update(STEAM_COMPAT_DATA_PATH=prefix,
                           STEAM_COMPAT_CLIENT_INSTALL_PATH=str(steam_client.resolve()),
                           WINEDEBUG='-all')
            with (output / 'setup-proton.log').open('wb') as log:
                subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT,
                               timeout=180, check=True)
        identities = sdk_identities(install)
        reused = False
    report = {'schema': 1, 'url': SDK_URL, 'installer_sha256': SDK_INSTALLER_SHA256,
              'reused': reused, 'selected_identities': identities,
              'scope': 'Local target headers/import libraries. Clang remains the compiler. No dependency material is committed.'}
    if not reused:
        report.update(command=command, proton_sha256=digest(proton) if os.name != 'nt' else None)
    write_json(report_path, report)
    return report


def embedded_cabinets(installer, output):
    data = installer.read_bytes()
    found = {}
    start = 0
    while (offset := data.find(b"MSCF", start)) != -1:
        start = offset + 4
        if offset + 36 > len(data):
            continue
        size = struct.unpack_from("<I", data, offset + 8)[0]
        files_offset = struct.unpack_from("<I", data, offset + 16)[0]
        folders = struct.unpack_from("<H", data, offset + 26)[0]
        files = struct.unpack_from("<H", data, offset + 28)[0]
        if (size in RUNTIME_CABINET_SIZES.values() and offset + size <= len(data)
                and 36 <= files_offset < size and folders and files):
            name = next(k for k, expected in RUNTIME_CABINET_SIZES.items() if size == expected)
            if name in found:
                raise RuntimeError(f"more than one {name} cabinet in pinned installer")
            path = output / f"{name}.cab"
            path.write_bytes(data[offset:offset + size])
            found[name] = {"path": path, "installer_offset": offset,
                           "size": size, "sha256": digest(path),
                           "folders": folders, "files": files}
    if set(found) != set(RUNTIME_CABINET_SIZES):
        raise RuntimeError(f"expected both embedded cabinets, found {sorted(found)}")
    return found


def extract(cabinet, destination, seven_zip):
    destination.mkdir(parents=True, exist_ok=True)
    command = [seven_zip, "x", "-y", "-bd", f"-o{destination}", str(cabinet)]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"7z extraction failed ({result.returncode}) for {cabinet}:\n"
                           + result.stdout[-2000:] + result.stderr[-2000:])
    return file_manifest(destination)


def file_manifest(destination):
    return sorted(({"path": path.relative_to(destination).as_posix(),
                    "size": path.stat().st_size, "sha256": digest(path)}
                   for path in destination.rglob("*") if path.is_file()),
                  key=lambda item: item["path"])


def runtime_metadata(path):
    import pefile

    require_hash(path, RUNTIME_SHA256)
    pe = pefile.PE(str(path), fast_load=False)
    if pe.FILE_HEADER.Machine != 0x14c or pe.OPTIONAL_HEADER.Magic != 0x10b:
        raise RuntimeError("pinned vcruntime is not an i386 PE32 image")
    fixed = pe.VS_FIXEDFILEINFO[0]
    version = ".".join(str(part) for part in (
        fixed.FileVersionMS >> 16, fixed.FileVersionMS & 0xffff,
        fixed.FileVersionLS >> 16, fixed.FileVersionLS & 0xffff))
    if version != RUNTIME_VERSION:
        raise RuntimeError(f"vcruntime file version {version}, expected {RUNTIME_VERSION}")
    exports = {symbol.name.decode("ascii"): symbol for symbol in pe.DIRECTORY_ENTRY_EXPORT.symbols
               if symbol.name}
    if not all(name in exports for name in RUNTIME_EXPORTS):
        raise RuntimeError("native runtime lacks a required EH export")
    if any(exports[name].forwarder for name in RUNTIME_EXPORTS):
        raise RuntimeError("required native EH export is a forwarder")
    return {"path": str(path), "sha256": digest(path), "version": version,
            "machine": pe.FILE_HEADER.Machine, "pe_magic": pe.OPTIONAL_HEADER.Magic,
            "exports": {name: {"ordinal": exports[name].ordinal,
                               "rva": exports[name].address}
                        for name in RUNTIME_EXPORTS}}


def cached_runtime(output, report):
    if (not isinstance(report, dict) or report.get('schema') != 1 or
            report.get('installer', {}).get('sha256') != RUNTIME_INSTALLER_SHA256 or
            report.get('native_runtime', {}).get('sha256') != RUNTIME_SHA256 or
            set(report.get('cabinets', {})) != set(RUNTIME_CABINET_SIZES)):
        return False
    for name in ['notices', 'payload', 'minimum']:
        rows = report.get(name)
        if not isinstance(rows, list) or not rows:
            return False
        for row in rows:
            if not isinstance(row, dict) or not {'path', 'sha256', 'size'}.issubset(row):
                return False
            path = (output / name / row['path']).resolve()
            if not path.is_relative_to((output / name).resolve()):
                raise RuntimeError('runtime manifest path escapes its extraction directory')
            if not path.is_file():
                return False
            require_hash(path, row['sha256'])
        if file_manifest(output / name) != rows:
            raise RuntimeError(f'cached runtime {name} file inventory differs')
    return True


def prepare_runtime(output, installer=None, seven_zip='7z'):
    output.mkdir(parents=True, exist_ok=True)
    report_path = output / 'report.json'
    try:
        report = json.loads(report_path.read_text()) if report_path.exists() else {}
    except json.JSONDecodeError:
        report = {}
    report_path.unlink(missing_ok=True)
    target = output / 'VC_redist.x86.exe'
    if installer is not None:
        require_hash(installer, RUNTIME_INSTALLER_SHA256)
    if target.exists():
        require_hash(target, RUNTIME_INSTALLER_SHA256)
    if cached_runtime(output, report):
        report['native_runtime'] = runtime_metadata(output / 'minimum' / RUNTIME_NAME)
        report['installer']['path'] = str(target)
        for name, cabinet in report['cabinets'].items():
            cabinet['path'] = str(output / f'{name}.cab')
        report['reused'] = True
        write_json(report_path, report)
        return report
    installer = acquire(installer, target, RUNTIME_URL, RUNTIME_INSTALLER_SHA256)
    cabinets = embedded_cabinets(installer, output)
    notices = extract(cabinets["notices"]["path"], output / "notices", seven_zip)
    payload = extract(cabinets["payload"]["path"], output / "payload", seven_zip)
    minimum_cab = output / "payload" / "a2"
    if not minimum_cab.is_file() or minimum_cab.read_bytes()[:4] != b"MSCF":
        raise RuntimeError("expected nested minimum-runtime cabinet payload/a2")
    minimum = extract(minimum_cab, output / "minimum", seven_zip)
    runtime = runtime_metadata(output / "minimum" / RUNTIME_NAME)
    report = {"schema": 1, "source_page": RUNTIME_SOURCE_PAGE, "download_url": RUNTIME_URL,
              "installer": {"path": str(installer), "sha256": digest(installer),
                            "size": installer.stat().st_size},
              "cabinets": {name: {k: v for k, v in item.items() if k != "path"} |
                            {"path": str(item["path"])}
                           for name, item in cabinets.items()},
              "notices": notices, "payload": payload, "minimum": minimum,
              "native_runtime": runtime}
    report['reused'] = False
    write_json(report_path, report)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only', choices=['sdk', 'runtime'], help='prepare just one dependency group')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'tmp/dependencies')
    parser.add_argument('--sdk-installer', type=Path, help='use an existing pinned SDK installer')
    parser.add_argument('--runtime-installer', type=Path, help='use an existing pinned VC_redist.x86.exe')
    parser.add_argument('--proton', type=Path, help='required to install missing SDK files on Linux')
    parser.add_argument('--steam-client', type=Path, help='required to install missing SDK files on Linux')
    parser.add_argument('--seven-zip', default='7z', help='7-Zip executable for runtime extraction')
    args = parser.parse_args(argv)
    try:
        output = output_directory(args.output_dir)
    except ValueError as error:
        parser.error(str(error))
    report_path = output / 'report.json'
    report_path.unlink(missing_ok=True)
    report = {'schema': 1, 'pass': False, 'dependencies': {}}
    try:
        if args.only != 'runtime':
            report['dependencies']['sdk'] = prepare_sdk(
                output / 'sdk', args.sdk_installer, args.proton, args.steam_client)
            print('SDK: ' + ('reused verified files' if report['dependencies']['sdk']['reused'] else 'installed'))
        if args.only != 'sdk':
            report['dependencies']['runtime'] = prepare_runtime(
                output / 'runtime', args.runtime_installer, args.seven_zip)
            print('Runtime: ' + ('reused verified files' if report['dependencies']['runtime']['reused'] else 'extracted'))
        paths = dependency_paths(output)
        report['paths'] = {name: str(path) for name, path in paths.items()
                           if (args.only != 'runtime' and name != 'exception_runtime') or
                              (args.only != 'sdk' and name == 'exception_runtime')}
        report['pass'] = True
    except Exception as error:
        report['error'] = str(error)
        raise
    finally:
        write_json(report_path, report)
    print(report_path)


if __name__ == "__main__":
    main()
