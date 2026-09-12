#!/usr/bin/env python3
"""Capture symbol-addressed, LC_FUNCTION_STARTS-bounded lyric-cache evidence (Tier 2).

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
    'CExtraDatabaseEngine::getDB(', 'CExtraDatabaseEngine::getLyrics(', 'CExtraDatabaseEngine::saveLyrics(',
    'CExtraDatabaseEngine::deleteLyrics(', 'CAudioSignature::loadFromString(',
    'CAudioSignature::saveToString(', 'hash128(', 'CAudioSignature::getSignature(',
    'CAudioSignature::start(', 'CAudioSignature::process(', 'CAudioSignature::end(',
    'CLyricsFinder::setLyrics(', 'strToDbl(std::__1::basic_string_view', 'CLyricsFinder::getFromServerCache(',
    'CLyricsFinder::handleTask(', 'CLyricsEditor::onSave(', 'CLyricsEditor::onEditPosition(',
    'ACTION_has_lyrics::onQuery(', 'ACTION_get_lyrics_language::onQuery(',
    'SDBInfo* CDatabaseEngine::loadItemWithDbi<CXMLNode>(',
    'CDatabaseEngine::itemToXml(',
]
# Selected excerpts retain whole-function identity/bounds and explicitly name
# the capture interval; they are not represented as full function captures.
WINDOWS = {
    'SDBInfo* CDatabaseEngine::loadItemWithDbi<CXMLNode>(': (0x1003b8c44, 0x1003b8f44),
    'CDatabaseEngine::itemToXml(': (0x1005b56dc, 0x1005b5780),
}
LITERALS = {
    'extra_filename': 0x1040a2666, 'cache_prefix': 0x1040a265f,
    'select': 0x1040a2bc6, 'replace': 0x1040a303e, 'delete': 0x1040a2c20,
    'scan_element': 0x10409d5ff, 'audiosig_attribute': 0x10409d619,
    'audiosig_write': 0x1040b1c05, 'language_prefix': 0x1040b0af0,
    'custom_header': 0x1040c1cb5, 'segment_format': 0x1040c1cd4,
    'line_end_segment_format': 0x1040c1cbe, 'timestamp_end': 0x10408c0c4,
    'escaped_newline': 0x104075d67, 'default_language': 0x1040aac7c,
    'server_url': 0x1040b0b0e, 'request_lid': 0x1040b0af7,
    'request_ns': 0x1040b0afc, 'request_version': 0x1040b0b0a,
    'response_lyrics': 0x1040b0b49, 'response_upload': 0x1040b0b50,
}



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
        capture_start, capture_end = WINDOWS.get(prefix, (start, end))
        assert start <= capture_start < capture_end <= end
        for ins in md.disasm(read(capture_start, capture_end-capture_start), capture_start):
            row = {'pc': hex(ins.address), 'asm': f'{ins.mnemonic} {ins.op_str}'.rstrip()}
            if ins.mnemonic in ('bl', 'b') and ins.op_str.startswith('#'):
                target = int(ins.op_str[1:], 16)
                if target in symbols:
                    row['target'] = symbols[target]
            instructions.append(row)
        functions.append({'name': name, 'start': hex(start), 'end_exclusive': hex(end),
                          'sha256': hashlib.sha256(code).hexdigest(),
                          'capture_start': hex(capture_start), 'capture_end_exclusive': hex(capture_end),
                          'instructions': instructions})
    literals = {name: {'va': hex(va), 'text': read(va, 180).split(b'\0')[0].decode()}
                for name, va in LITERALS.items()}
    info = plistlib.loads((app / 'Contents/Info.plist').read_bytes())
    return {'schema_version': 1, 'evidence_tier': 2,
            'scope': 'Historical binary structure; no live application write/readback test.',
            'source': {'build': info['CFBundleVersion'], 'arch': 'arm64', 'binary_sha256': sha,
                       'extracted': datetime.date.today().isoformat()},
            'schema': {'lid': '16 packed histogram bytes + little-endian uint16 raw fingerprint count',
                       'xml': 'uncompressed UTF-8 timestamped text; column name does not imply XML',
                       'hash128': 'q[b]=floor(16*ones_at_bit_b/(N+1)); byte[i]=(q[2*i]<<4)|q[2*i+1]',
                       'audiosig': 'Base64url of lid bytes; special empty/count-zero and dash/count-one states',
                       'limitations': 'No live rendering, server request, or end-to-end audio matching test.'},
            'literals': literals,
            'numeric_constants': {'hash_bit_order_u32_le': read(0x103cb3240, 16).hex(),
                                  'timing_repair_float32_le': read(0x103c81ca4, 4).hex()},
            'functions': functions}



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(extract(args.app), indent=2))
