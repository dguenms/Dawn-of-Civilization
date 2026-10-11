#!/usr/bin/env python3
"""Acquire the pinned Microsoft x86 VC runtime into ignored repo tmp/.

The installer is from Microsoft's latest supported VC redist page. This tool
extracts its embedded cabinets and keeps the first cabinet's license/support
payload intact beside the minimum-runtime payload. It never installs a package.
"""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess
import urllib.request

import pefile


ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "tmp"
URL = (
    "https://download.visualstudio.microsoft.com/download/pr/"
    "ece44298-3977-4f73-ab91-c13fe79cfea8/"
    "F0BAB33A302B3CDB2E11113760D016F54FD3D2632C65BA7834FAC4F0ABD7F1A3/"
    "VC_redist.x86.exe"
)
SOURCE_PAGE = "https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist/"
INSTALLER_SHA256 = "f0bab33a302b3cdb2e11113760d016f54fd3d2632c65ba7834fac4f0abd7f1a3"
RUNTIME_SHA256 = "2fa6efc053203460a23d3a25158f227d895d2dadc63acc1a372da97c3a4281c3"
EXPECTED_VERSION = "14.51.36247.0"
CABINET_SIZES = {"notices": 139414, "payload": 6301985}
RUNTIME_NAME = "vcruntime140.dll_x86"
REQUIRED_EXPORTS = ("__CxxFrameHandler3", "_CxxThrowException")


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require_hash(path, expected):
    actual = digest(path)
    if actual != expected:
        raise RuntimeError(f"SHA256 mismatch for {path}: {actual}, expected {expected}")


def output_directory(path):
    output = path.resolve()
    tmp = TMP.resolve()
    if output == tmp or tmp not in output.parents:
        raise ValueError(f"output must be a dedicated directory below {tmp}: {output}")
    output.mkdir(parents=True, exist_ok=True)
    return output


def acquire(installer, output):
    target = output / "VC_redist.x86.exe"
    if installer is not None:
        source = installer.resolve(strict=True)
        require_hash(source, INSTALLER_SHA256)
        if source != target:
            shutil.copyfile(source, target)
    elif not target.exists():
        partial = output / "VC_redist.x86.exe.partial"
        try:
            with urllib.request.urlopen(URL, timeout=60) as response, partial.open("wb") as stream:
                shutil.copyfileobj(response, stream)
            require_hash(partial, INSTALLER_SHA256)
            partial.replace(target)
        finally:
            partial.unlink(missing_ok=True)
    require_hash(target, INSTALLER_SHA256)
    return target


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
        if (size in CABINET_SIZES.values() and offset + size <= len(data)
                and 36 <= files_offset < size and folders and files):
            name = next(k for k, expected in CABINET_SIZES.items() if size == expected)
            if name in found:
                raise RuntimeError(f"more than one {name} cabinet in pinned installer")
            path = output / f"{name}.cab"
            path.write_bytes(data[offset:offset + size])
            found[name] = {"path": path, "installer_offset": offset,
                           "size": size, "sha256": digest(path),
                           "folders": folders, "files": files}
    if set(found) != set(CABINET_SIZES):
        raise RuntimeError(f"expected both embedded cabinets, found {sorted(found)}")
    return found


def extract(cabinet, destination, seven_zip):
    destination.mkdir(parents=True, exist_ok=True)
    command = [seven_zip, "x", "-y", "-bd", f"-o{destination}", str(cabinet)]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"7z extraction failed ({result.returncode}) for {cabinet}:\n"
                           + result.stdout[-2000:] + result.stderr[-2000:])
    return sorted(({"path": str(path.relative_to(destination)),
                    "size": path.stat().st_size, "sha256": digest(path)}
                   for path in destination.rglob("*") if path.is_file()),
                  key=lambda item: item["path"])


def runtime_metadata(path):
    require_hash(path, RUNTIME_SHA256)
    pe = pefile.PE(str(path), fast_load=False)
    if pe.FILE_HEADER.Machine != 0x14c or pe.OPTIONAL_HEADER.Magic != 0x10b:
        raise RuntimeError("pinned vcruntime is not an i386 PE32 image")
    fixed = pe.VS_FIXEDFILEINFO[0]
    version = ".".join(str(part) for part in (
        fixed.FileVersionMS >> 16, fixed.FileVersionMS & 0xffff,
        fixed.FileVersionLS >> 16, fixed.FileVersionLS & 0xffff))
    if version != EXPECTED_VERSION:
        raise RuntimeError(f"vcruntime file version {version}, expected {EXPECTED_VERSION}")
    exports = {symbol.name.decode("ascii"): symbol for symbol in pe.DIRECTORY_ENTRY_EXPORT.symbols
               if symbol.name}
    if not all(name in exports for name in REQUIRED_EXPORTS):
        raise RuntimeError("native runtime lacks a required EH export")
    if any(exports[name].forwarder for name in REQUIRED_EXPORTS):
        raise RuntimeError("required native EH export is a forwarder")
    return {"path": str(path), "sha256": digest(path), "version": version,
            "machine": pe.FILE_HEADER.Machine, "pe_magic": pe.OPTIONAL_HEADER.Magic,
            "exports": {name: {"ordinal": exports[name].ordinal,
                               "rva": exports[name].address}
                        for name in REQUIRED_EXPORTS}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--installer", type=Path,
                        help="use an existing pinned VC_redist.x86.exe; otherwise download if absent")
    parser.add_argument("--output-dir", type=Path, default=TMP / "s2-runtime-deps")
    parser.add_argument("--seven-zip", default="7z")
    args = parser.parse_args()
    output = output_directory(args.output_dir)
    installer = acquire(args.installer, output)
    cabinets = embedded_cabinets(installer, output)
    notices = extract(cabinets["notices"]["path"], output / "notices", args.seven_zip)
    payload = extract(cabinets["payload"]["path"], output / "payload", args.seven_zip)
    minimum_cab = output / "payload" / "a2"
    if not minimum_cab.is_file() or minimum_cab.read_bytes()[:4] != b"MSCF":
        raise RuntimeError("expected nested minimum-runtime cabinet payload/a2")
    minimum = extract(minimum_cab, output / "minimum", args.seven_zip)
    runtime = runtime_metadata(output / "minimum" / RUNTIME_NAME)
    report = {"schema": 1, "source_page": SOURCE_PAGE, "download_url": URL,
              "installer": {"path": str(installer), "sha256": digest(installer),
                            "size": installer.stat().st_size},
              "cabinets": {name: {k: v for k, v in item.items() if k != "path"} |
                            {"path": str(item["path"])}
                           for name, item in cabinets.items()},
              "notices": notices, "payload": payload, "minimum": minimum,
              "native_runtime": runtime}
    report_path = output / "report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(report_path)
    print(runtime["path"])


if __name__ == "__main__":
    main()
