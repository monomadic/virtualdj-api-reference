#!/usr/bin/env python3
"""Capture symbol-addressed, LC_FUNCTION_STARTS-bounded SID evidence (Tier 2).

Requires capstone only during extraction. Intended for unstripped 18.0.9246;
constants with fixed addresses are guarded by the full executable SHA-256.
No private library contents are read or emitted.
"""
import argparse
import bisect
import datetime
import hashlib
import json
import plistlib
import subprocess
from pathlib import Path
from types import SimpleNamespace

from extract_verb_table import slice_offset, sections
from extract_skin_classes import function_starts

EXPECTED_SHA = '15ff1b26a8e6e2697726ce1f165a545cbab9580d4f349edc648adbaa60a0e240'
TARGETS = [
    'CExtraDatabaseEngine::addRelated(', 'CExtraDatabaseEngine::addTrackData(',
    'CExtraDatabaseEngine::getDBIFromSID(', 'CDatabaseEngine::findInfoFromSID(',
    'CDatabaseEngine::updateSidCache(bool)', 'SDBInfo::getSIDCleaned(',
    'CTagEngine::getCleanedCopy(', 'CTagEngine::cleanup(',
    'SDBInfo::getSID()', 'SDBInfo::getSIDString()', 'strAddReduced(', 'utfcanonical(',
]
TABLES = [('_utf8accent', 0x80, 256), ('_utf8translitgreek', 0x370, 101),
          ('_utf8translitrussian', 0x400, 96), ('_utf8translithebrew', 0x5d0, 27)]


def extract(app):
    from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
    data = (app / 'Contents/MacOS/VirtualDJ').read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    if sha != EXPECTED_SHA:
        raise ValueError('Unreviewed binary: fixed literal addresses require the recorded 18.0.9246 SHA-256')
    base = slice_offset(data)
    secs = sections(data, base)
    def read(va, length):
        sec = next(s for s in secs if s[2] <= va and va + length <= s[2] + s[3])
        off = base + sec[4] + va - sec[2]
        return data[off:off + length]
    raw = subprocess.check_output(['nm', '-arch', 'arm64', '-n', str(app / 'Contents/MacOS/VirtualDJ')], text=True)
    raw = subprocess.check_output(['c++filt'], input=raw, text=True)
    symbols = {}
    for line in raw.splitlines():
        parts = line.split(' ', 2)
        if len(parts) == 3:
            try:
                symbols[int(parts[0], 16)] = parts[2]
            except ValueError:
                pass
    names = {v: k for k, v in symbols.items()}
    starts = function_starts(SimpleNamespace(data=data, base=base))
    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    functions = []
    for prefix in TARGETS:
        matches = [(va, name) for va, name in symbols.items() if name.startswith(prefix) and name.endswith(")")]
        if len(matches) != 1:
            raise ValueError((prefix, matches))
        start, name = matches[0]
        if start not in starts:
            raise ValueError(f'{name} is not an LC_FUNCTION_STARTS entry')
        end = starts[bisect.bisect_right(starts, start)]
        code = read(start, end-start)
        instructions = []
        for ins in md.disasm(code, start):
            row = {'pc': hex(ins.address), 'asm': f'{ins.mnemonic} {ins.op_str}'.rstrip()}
            if ins.mnemonic in ('bl', 'b') and ins.op_str.startswith('#'):
                target = int(ins.op_str[1:], 16)
                if target in symbols:
                    row['target'] = symbols[target]
            instructions.append(row)
        functions.append({'name': name, 'start': hex(start), 'end_exclusive': hex(end),
                          'sha256': hashlib.sha256(code).hexdigest(), 'instructions': instructions})
    literals = {}
    for name, va in [('stop_characters', 0x1044b5998), ('web_prefix', 0x104084965),
                     ('sharp_s', 0x104080e79), ('related_insert', 0x1040a2ecc),
                     ('track_insert', 0x1040a2f02)]:
        literals[name] = {'va': hex(va), 'text': read(va, 180).split(b'\0')[0].decode()}
    tables = [{'symbol': name, 'va': hex(names[name]), 'first_codepoint': first,
               'bytes_hex': read(names[name], length).hex()} for name, first, length in TABLES]
    info = plistlib.loads((app / 'Contents/Info.plist').read_bytes())
    return {'schema_version': 1, 'evidence_tier': 2,
            'scope': 'Historical binary structure; no live application write/readback test.',
            'source': {'build': info['CFBundleVersion'], 'arch': 'arm64', 'binary_sha256': sha,
                       'extracted': datetime.date.today().isoformat()},
            'algorithm': {'offset_basis': 'cbf29ce484222325', 'prime': '100000001b3',
                          'order': 'multiply_then_xor', 'fields': ['artist', 'title', 'remix'],
                          'precondition': 'CTagEngine::cleanup(copy, false)',
                          'rejected_reduced_strings': ['', 'TRACK', 'UNKNOWNARTISTTRACK', 'VIDEOPLAYBACK'],
                          'remix_excluded_if_contains': ['.com', '.net', '.org', 'www.']},
            'literals': literals, 'unicode_tables': tables, 'functions': functions}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(extract(args.app), indent=2))
