#!/usr/bin/env python3
"""Prepare pinned Windows header views and bounded non-analysis SAL metadata."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PINS = {
    'vc71/include/xstring': 'c715ae6f152ca41d73e701c5d77dd5da0b61832250c967d2a8376b9471656943',
    'vc71/include/yvals.h': 'b9340f3de0fd2f1c0e0b81b99e9f42252a0ec5652267536e9c62b0b4f1bf8980',
    'vc71/include/typeinfo': 'edb88288e3a86e6ea5b2ef96af0a399ae2c84cff81a9b2c874b24288b970aa9b',
    'vc71/lib/msvcrt.lib': 'e888617fbd2e153645b92122deab1c6ec437905431243c43aa7310164c0e7779',
    'vc71/lib/msvcprt.lib': 'b481ce2150f0a0dc747f2811a94de18ed5f2c4e3cf7a09e4d64141f07ffc502c',
    'vc71/lib/oldnames.lib': 'ace6ebf2ef319936a64b7e1a27f508a2c03c4838908f12e790b6c198845cc6cb',
    'sdk/include/specstrings.h': 'aa3a45dc75111ee97ff4fbf10643b6999f893380eacda9b1597ff85d14b0cbe2',
    'sdk/include/specstrings_strict.h': 'ffa3606ab8c816a797cfe3f9d2ff5d48941b08e91a623d3683ef1e21bc986573',
    'sdk/include/Rpcsal.h': 'c54f4904a2863d8a3e652dd614ffaad4a51a047c04f336835af24ab3b709bb6c',
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_if_changed(path, data):
    if not path.exists() or path.read_bytes() != data:
        path.write_bytes(data)


def generate_sal(sdk, output):
    # Read annotation names/signatures only, never Microsoft's macro bodies.
    # The acquired SDK requires a missing sal.h, although its chosen VC7.1
    # non-PREFAST declarations use these tokens solely as erased annotations.
    source_defined = set()
    for name in ['specstrings.h', 'Rpcsal.h']:
        source_defined.update(re.findall(r'^#define\s+(__[A-Za-z0-9_$]+)',
                                        (sdk / name).read_text(), re.M))
    signatures = {}
    for match in re.finditer(r'^#define\s+(__[A-Za-z0-9_$]+)(\([^\n)]*\))?',
                            (sdk / 'specstrings_strict.h').read_text(), re.M):
        name, args = match.group(1), match.group(2) or ''
        if (name.startswith('__$') or name in {'__allowed', '__override'}
                or name[2:].isupper() or name in source_defined):
            continue
        signatures.setdefault(name, args)
    if len(signatures) != 210:
        raise RuntimeError('pinned SAL annotation vocabulary differs')
    lines = ['#pragma once',
             '/* Authored SAL annotation erasure: Clang VC7.1 non-analysis only. */',
             '#if !defined(__clang__) || !defined(_MSC_VER) || _MSC_VER != 1310',
             '#error "SAL compatibility requires Clang VC7.1 mode"', '#endif',
             '#if defined(_PREFAST_) || defined(_MSC_ANALYSIS)',
             '#error "SAL compatibility has no analysis semantics"', '#endif',
             '#define __SAL_H_FULL_VER 140050727',
             '#define __inner_checkReturn', '#define __inner_control_entrypoint(kind)',
             # Ole2.h uses this annotation absent from the pinned strict vocabulary.
             '#define __deref_opt_out_z']
    for name, args in sorted(signatures.items()):
        lines.extend([f'#ifndef {name}', f'#define {name}{args}', '#endif'])
    write_if_changed(output / 'sal.h', ('\n'.join(lines) + '\n').encode())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vc71', type=Path, required=True)
    parser.add_argument('--sdk', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if not output.is_relative_to(ROOT / 'tmp') or output == ROOT / 'tmp':
        parser.error('output must be a dedicated ignored directory under repo tmp/')
    output.mkdir(parents=True, exist_ok=True)
    inputs = {}
    for name, expected in PINS.items():
        tree, relative = name.split('/', 1)
        path = (args.vc71 if tree == 'vc71' else args.sdk) / relative
        if digest(path) != expected:
            raise RuntimeError(f'pinned target dependency differs: {path}')
    for base, expected in [
        (args.vc71 / 'include', '85a92fc7e2678f7f8a6d3e09c568215cad126b87652358b2145245ce205fa6f6'),
        (args.sdk / 'include', 'fce75d4031c5d5b411173cee2cb198d690c3c861c3d78ada3e3bb67b2e066a9f')]:
        # Pin the same spelling and ordering on Windows and Linux hosts.
        rows = sorted((path.relative_to(base).as_posix(), digest(path))
                      for path in base.rglob('*') if path.is_file())
        if hashlib.sha256(json.dumps(rows, separators=(',', ':')).encode()).hexdigest() != expected:
            raise RuntimeError(f'pinned target header tree differs: {base}')
    generate_sal(args.sdk / 'include', output)
    roots = []
    # Include the inherited tree in the case-insensitive view. This preserves
    # its Windows include spelling without unnecessary case-only source edits.
    for index, include in enumerate([args.vc71 / 'include', args.sdk / 'include',
                                     ROOT / 'CvGameCoreDLL']):
        include = include.resolve()
        virtual = output / f'include-{index}'

        def directory(path):
            contents, seen = [], set()
            for child in sorted(path.iterdir()):
                key = child.name.casefold()
                if key in seen:
                    raise RuntimeError(f'ambiguous Windows include spelling: {child}')
                seen.add(key)
                if child.is_dir():
                    contents.append({'type': 'directory', 'name': child.name,
                                     'contents': directory(child)})
                elif child.is_file():
                    external = child
                    if index == 0 and child == include / 'xstring':
                        data = child.read_bytes()
                        old = b'(basic_string<_Elem, _Traits, _Alloc>::size_type)'
                        if data.count(old) != 1:
                            raise RuntimeError('expected one xstring dependent npos type')
                        external = output / 'vc71-xstring'
                        write_if_changed(external, data.replace(old, b'(typename basic_string<_Elem, _Traits, _Alloc>::size_type)'))
                    inputs[str(child)] = digest(child)
                    contents.append({'type': 'file', 'name': child.name,
                                     'external-contents': str(external)})
            return contents

        roots.append({'type': 'directory', 'name': str(virtual),
                      'contents': directory(include)})
    # Canonical external names keep Ninja dependencies on real input paths.
    # Lookup remains case-insensitive, including legacy misspelled includes.
    write_if_changed(output / 'overlay.json', (json.dumps({'version': 0, 'case-sensitive': False,
        'use-external-names': True, 'roots': roots}, indent=2) + '\n').encode())
    write_if_changed(output / 'inputs.json', (json.dumps(inputs, sort_keys=True, indent=2) + '\n').encode())
    print(output / 'overlay.json')


if __name__ == '__main__':
    main()
