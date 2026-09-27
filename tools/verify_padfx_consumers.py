#!/usr/bin/env python3
"""Verify saved padfx decompiles against the original universal executable."""
import argparse
import hashlib
import json
import struct
from pathlib import Path
from ghidra_time_consumers import arm64_slice
from extract_skin_classes import Analysis
from extract_action_vtables import demangled, symbol_maps

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', type=Path, required=True)
    args = parser.parse_args()
    binary = args.app / 'Contents/MacOS/VirtualDJ'
    raw = binary.read_bytes()
    capture = json.loads((ROOT / 'tests/ghidra-padfx-consumers-9246.json').read_text())
    if hashlib.sha256(raw).hexdigest() != '15ff1b26a8e6e2697726ce1f165a545cbab9580d4f349edc648adbaa60a0e240':
        raise ValueError('wrong executable')
    if hashlib.sha256(arm64_slice(raw)).hexdigest() != capture['program_sha256']:
        raise ValueError('wrong imported slice')
    symbols, _ = symbol_maps(demangled(binary, 'arm64'))
    analysis = Analysis(args.app)
    for row in capture['functions']:
        address = int(row['address'], 16)
        words = analysis.words(address)
        code = b''.join(struct.pack('<I', word) for _, word in words)
        if len(code) != row['guard_length'] or hashlib.sha256(code).hexdigest() != row['guard_sha256']:
            raise ValueError('independent function bounds or bytes differ')
        if row['ghidra_name'] not in symbols.get(address, ''):
            raise ValueError('function symbol differs')
        if int(row['body_min'], 16) != address or int(row['body_max'], 16) >= address + len(code):
            raise ValueError('Ghidra body outside independent bounds')
        if row['warning'] or not row['decompiled_c'].strip():
            raise ValueError('missing or warned decompilation')
    print('Verified build 9246 binary, arm64 import, symbols, function bounds and code hashes; Tier 2 only.')

if __name__ == '__main__':
    main()
