#!/usr/bin/env python3
"""Verify the read-only Ghidra time-reader export against independently bounded code."""
import argparse
import hashlib
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
CAPTURE = ROOT / 'tests/ghidra-time-consumers-9246.json'
MANIFEST = ROOT / 'tests/tail-consumers-shared-9246.json'
TARGETS = {'0x1004d63b4': 'ACTION_get_time::onQueryText',
           '0x1004d65d0': 'ACTION_get_time::getTime'}


def arm64_slice(raw):
    magic, count = struct.unpack_from('>II', raw)
    if magic not in (0xcafebabe, 0xcafebabf):
        raise ValueError('expected the verified universal executable')
    stride = 20 if magic == 0xcafebabe else 32
    for n in range(count):
        fields = struct.unpack_from('>IIIII' if stride == 20 else '>IIQQII', raw, 8 + n * stride)
        cpu, _, start, length = fields[:4]
        if cpu == 0x100000c:
            if start + length > len(raw):
                raise ValueError('slice exceeds file')
            return raw[start:start + length]
    raise ValueError('no arm64 slice')


def verify_export(capture, manifest):
    if capture['language'] != 'AARCH64:LE:64:AppleSilicon':
        raise ValueError('wrong processor language')
    rows = capture['functions']
    if len(rows) != len(TARGETS) or {r['address'] for r in rows} != set(TARGETS):
        raise ValueError('target functions differ')
    for row in rows:
        address = row['address']
        guard = manifest['routines'][address]
        if (row['ghidra_name'] != TARGETS[address] or row['guard_sha256'] != guard['sha256']
                or row['guard_length'] != int(guard['end'], 16) - int(address, 16)):
            raise ValueError('function identity or code guard differs')
        if int(row['body_min'], 16) != int(address, 16) or not (
                int(address, 16) <= int(row['body_max'], 16) < int(guard['end'], 16)):
            raise ValueError('Ghidra function body exceeds independent interval')
        if not row['decompiled_c'].strip() or row['warning']:
            raise ValueError('missing decompilation or decompiler warning')
    return {'build': manifest['source']['build'], 'ghidra_version': capture['ghidra_version'],
            'function_guards_match': True, 'body_bounds_match': True,
            'evidence_tier': 2, 'scope': 'Code identity and decompiler export only; no runtime behavior proof.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--capture', type=Path, default=CAPTURE)
    p.add_argument('--binary', type=Path, help='also verify the universal executable and imported thin-slice hash')
    p.add_argument('--show', choices=('reader', 'formatter'))
    args = p.parse_args()
    capture, manifest = json.loads(args.capture.read_text()), json.loads(MANIFEST.read_text())
    result = verify_export(capture, manifest)
    if args.binary:
        from plugin_memory import verify
        from extract_verb_table import sections, slice_offset
        verify(json.loads((ROOT / 'tests/tail-probe-9246-memory.json').read_text()), args.binary)
        raw = args.binary.read_bytes()
        if hashlib.sha256(raw).hexdigest() != manifest['source']['binary_sha256']:
            raise ValueError('executable hash differs')
        if hashlib.sha256(arm64_slice(raw)).hexdigest() != capture['program_sha256']:
            raise ValueError('Ghidra imported a different arm64 image')
        base = slice_offset(raw)
        section = next(s for s in sections(raw, base) if s[1] == '__text')
        for row in capture['functions']:
            offset = base + section[4] + int(row['address'], 16) - section[2]
            if hashlib.sha256(raw[offset:offset + row['guard_length']]).hexdigest() != row['guard_sha256']:
                raise ValueError('exported memory differs from executable')
        result['disk_and_imported_slice_match'] = True
    print(json.dumps(result, indent=2))
    if args.show:
        address = '0x1004d65d0' if args.show == 'reader' else '0x1004d63b4'
        print(next(r['decompiled_c'] for r in capture['functions'] if r['address'] == address))


if __name__ == '__main__':
    main()
