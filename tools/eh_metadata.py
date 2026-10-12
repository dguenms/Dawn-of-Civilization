"""Validate Clang 23 i386 COFF C++ FuncInfo before accepting the stock DLL.

This accepts ordinary COFF objects from the pinned compiler. BigObj, extended
relocations and other exception metadata formats require a separate audit.
"""

import hashlib
from pathlib import Path
import struct


MAGIC = 0x19930522  # LLVM's VC8 FuncInfo emitted for __CxxFrameHandler3.
DIR32 = 6


class Coff:
    def __init__(self, path):
        self.path = Path(path)
        self.data = self.path.read_bytes()
        machine, nsec, _, symptr, nsym, optional, _ = self.read('HHLLLHH', 0)
        if machine != 0x14c or optional or not nsec or not nsym:
            raise ValueError(f'{path}: unsupported ordinary i386 COFF header')
        section_end = 20 + nsec * 40
        symbol_end = symptr + nsym * 18
        self.bounds(0, section_end)
        self.bounds(symptr, nsym * 18)
        if symptr < section_end:
            raise ValueError(f'{path}: symbol table overlaps section headers')
        string_size, = self.read('L', symbol_end)
        if string_size < 4:
            raise ValueError(f'{path}: malformed COFF string table')
        self.bounds(symbol_end, string_size)
        strings = self.data[symbol_end:symbol_end + string_size]
        self.sections = [None]
        for index in range(nsec):
            off = 20 + index * 40
            name = self.data[off:off + 8].rstrip(b'\0')
            if name.startswith(b'/'):
                try:
                    name_offset = int(name[1:])
                except ValueError as error:
                    raise ValueError(f'{path}: malformed long section name') from error
                if not 4 <= name_offset < string_size:
                    raise ValueError(f'{path}: section name string offset out of bounds')
                end = strings.find(b'\0', name_offset)
                if end < 0:
                    raise ValueError(f'{path}: unterminated section name')
                name = strings[name_offset:end]
            _, _, size, raw, reloc, _, count, _, characteristics = self.read('LLLLLLHHI', off + 8)
            if count == 0xffff or characteristics & 0x01000000:
                raise ValueError(f'{path}: extended relocations are unsupported')
            if size and raw:
                self.bounds(raw, size)
                if raw < section_end:
                    raise ValueError(f'{path}: section data overlaps headers')
            elif size and (not characteristics & 0x80 or count):
                raise ValueError(f'{path}: missing initialized section data')
            if count:
                self.bounds(reloc, count * 10)
                if reloc < section_end:
                    raise ValueError(f'{path}: relocations overlap headers')
            relocations = {}
            for number in range(count):
                address, symbol, kind = self.read('LLH', reloc + number * 10)
                width = 2 if kind in (1, 2, 10) else 4
                if address in relocations or address + width > size or symbol >= nsym:
                    raise ValueError(f'{path}: malformed relocation in section {index + 1}')
                relocations[address] = (symbol, kind)
            self.sections.append((name, self.data[raw:raw + size] if raw else b'', relocations))
        self.symbols = {}
        index = 0
        while index < nsym:
            off = symptr + index * 18
            raw_name = self.data[off:off + 8]
            zero, name_offset = struct.unpack('<LL', raw_name)
            if zero == 0:
                if not 4 <= name_offset < string_size:
                    raise ValueError(f'{path}: COFF symbol string offset out of bounds')
                end = strings.find(b'\0', name_offset)
                if end < 0:
                    raise ValueError(f'{path}: unterminated COFF symbol name')
                name = strings[name_offset:end]
            else:
                name = raw_name.rstrip(b'\0')
            value, section, _, _, aux = self.read('LhHBB', off + 8)
            if index + aux >= nsym or section > nsec or section < -2:
                raise ValueError(f'{path}: malformed COFF symbol or auxiliary records')
            self.symbols[index] = (name, value, section)
            index += 1 + aux
        for section in self.sections[1:]:
            for symbol, _ in section[2].values():
                if symbol not in self.symbols:
                    raise ValueError(f'{path}: relocation targets an auxiliary symbol')

    def bounds(self, offset, length):
        if offset < 0 or length < 0 or offset > len(self.data) or length > len(self.data) - offset:
            raise ValueError(f'{self.path}: COFF data range out of bounds')

    def read(self, fmt, offset):
        size = struct.calcsize('<' + fmt)
        self.bounds(offset, size)
        return struct.unpack_from('<' + fmt, self.data, offset)

    def word(self, section, offset):
        data = self.sections[section][1]
        if offset < 0 or offset + 4 > len(data):
            raise ValueError(f'{self.path}: section word out of bounds')
        return struct.unpack_from('<L', data, offset)[0]

    def pointer(self, section, offset, count, stride):
        data, relocations = self.sections[section][1:]
        if offset + 4 > len(data):
            raise ValueError(f'{self.path}: map pointer out of bounds')
        if not count:
            if self.word(section, offset) or offset in relocations:
                raise ValueError(f'{self.path}: nonnull empty map at {section}:{offset}')
            return None
        if offset not in relocations:
            raise ValueError(f'{self.path}: missing map relocation at {section}:{offset}')
        symbol, kind = relocations[offset]
        if kind != DIR32:
            raise ValueError(f'{self.path}: unsupported map relocation kind {kind}')
        _, value, target = self.symbols[symbol]
        if target <= 0:
            raise ValueError(f'{self.path}: map points outside object')
        start = value + self.word(section, offset)
        if start > len(self.sections[target][1]) or count * stride > len(self.sections[target][1]) - start:
            raise ValueError(f'{self.path}: map exceeds section bounds')
        return target, start


def inspect_object(path, catch_slots=64):
    """Return bounded FuncInfo counts, or raise ValueError on unsupported ABI."""
    if not isinstance(catch_slots, int) or catch_slots < 1:
        raise ValueError('catch_slots must be a positive integer')
    coff = Coff(path)
    tables = []
    raw_magics = 0
    handler_relocs = 0
    for section_number, (name, data, relocations) in enumerate(coff.sections[1:], 1):
        handler_relocs += sum(coff.symbols[symbol][0] == b'___CxxFrameHandler3'
                              for symbol, _ in relocations.values())
        if name != b'.xdata':
            continue
        for offset in range(0, len(data) - 3, 4):
            if coff.word(section_number, offset) != MAGIC:
                continue
            raw_magics += 1
            if offset + 36 > len(data):
                raise ValueError(f'{path}: truncated FuncInfo')
            _, states, _, tries, _, ips, _, expected, flags = struct.unpack_from('<9L', data, offset)
            if flags not in (0, 1) or expected or offset + 28 in relocations:
                raise ValueError(f'{path}: unsupported FuncInfo flags or expected list')
            if tries > catch_slots:
                raise ValueError(f'{path}: try blocks exceed {catch_slots} adapter slots')
            coff.pointer(section_number, offset + 8, states, 8)
            try_map = coff.pointer(section_number, offset + 16, tries, 20)
            coff.pointer(section_number, offset + 24, ips, 8)
            catches = 0
            if try_map:
                target, start = try_map
                for index in range(tries):
                    entry = start + index * 20
                    count = coff.word(target, entry + 12)
                    catches += count
                    if catches > catch_slots:
                        raise ValueError(f'{path}: catch clauses exceed {catch_slots} adapter slots')
                    catch_map = coff.pointer(target, entry + 16, count, 16)
                    if catch_map:
                        catch_section, catch_start = catch_map
                        catch_relocs = coff.sections[catch_section][2]
                        for clause in range(count):
                            handler = catch_start + clause * 16 + 12
                            if handler not in catch_relocs or catch_relocs[handler][1] != DIR32:
                                raise ValueError(f'{path}: missing catch-handler relocation')
                            type_ptr = handler - 8
                            if coff.word(catch_section, type_ptr) and type_ptr not in catch_relocs:
                                raise ValueError(f'{path}: missing catch-type relocation')
            tables.append((tries, catches, flags))
    if len(tables) != raw_magics or len(tables) != handler_relocs:
        raise ValueError(f'{path}: FuncInfo/magic/Handler3 relocation counts disagree: '
                         f'{len(tables)}/{raw_magics}/{handler_relocs}')
    return {'funcinfo_count': len(tables), 'raw_xdata_magic_count': raw_magics,
            'handler3_relocation_count': handler_relocs,
            'max_try_blocks': max((row[0] for row in tables), default=0),
            'max_catch_clauses': max((row[1] for row in tables), default=0),
            'flags_counts': {str(flag): sum(row[2] == flag for row in tables)
                             for flag in (0, 1) if any(row[2] == flag for row in tables)},
            'sha256': hashlib.sha256(coff.data).hexdigest()}
