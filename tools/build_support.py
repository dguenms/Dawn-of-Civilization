"""Pinned input identities, hashing and PE metadata used by the DLL build."""
import hashlib
import json
from pathlib import Path

import pefile

ROOT = Path(__file__).resolve().parents[1]
LOCK = json.loads((ROOT / 'tools/s1-lock.json').read_text())


def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def pe_summary(path):
    pe = pefile.PE(str(path))
    versions = {}
    for group in getattr(pe, 'FileInfo', []):
        for info in group:
            if info.Key == b'StringFileInfo':
                for table in info.StringTable:
                    versions.update({k.decode(): v.decode(errors='replace')
                                     for k, v in table.entries.items()})
    imports = []
    for kind, attribute in [('ordinary', 'DIRECTORY_ENTRY_IMPORT'),
                            ('delay', 'DIRECTORY_ENTRY_DELAY_IMPORT')]:
        for module in getattr(pe, attribute, []):
            for entry in module.imports:
                imports.append({'kind': kind, 'dll': module.dll.decode(),
                                'name': entry.name.decode() if entry.name else None,
                                'ordinal': entry.ordinal,
                                'iat_va': entry.address})
    exports = {s.name.decode(): {'rva': s.address, 'ordinal': s.ordinal,
                                'forwarder': s.forwarder.decode() if s.forwarder else None}
               for s in getattr(getattr(pe, 'DIRECTORY_ENTRY_EXPORT', None), 'symbols', [])
               if s.name}
    return pe, {'sha256': digest(path), 'size': path.stat().st_size,
                'machine': pe.FILE_HEADER.Machine, 'magic': pe.OPTIONAL_HEADER.Magic,
                'image_base': pe.OPTIONAL_HEADER.ImageBase, 'versions': versions,
                'imports': imports, 'exports': exports}
