#!/usr/bin/env python3
"""Verify a bounded in-process verb-table capture against the matching host image.

Does not promote verb behaviour or overwrite the canonical verb-table artifact.
"""
import argparse
import hashlib
import json
import struct
from pathlib import Path

from extract_verb_table import ARM64, BINARY, build, slice_offset


def image_uuid(data):
    base = slice_offset(data, ARM64)
    pos = base + 32
    for _ in range(struct.unpack_from('<I', data, base + 16)[0]):
        cmd, size = struct.unpack_from('<II', data, pos)
        if cmd == 0x1b:
            return data[pos + 8:pos + 24].hex()
        pos += size
    raise ValueError('host binary has no LC_UUID')


def verify(capture, binary):
    raw = binary.read_bytes()
    if capture['schema'] != 1 or capture['channel'] != 'in-process-memory' or capture['arch'] != 'arm64':
        raise ValueError('unsupported capture')
    if image_uuid(raw) != capture['image_uuid']:
        raise ValueError('loaded image UUID differs from disk; retain capture and locate its matching binary')
    disk = build(str(binary), ARM64)
    if disk['summary']['build'] != capture['build']:
        raise ValueError('loaded build differs from disk')
    expected = {name: {k: row[k] for k in ('id', 'flags')} for name, row in disk['verbs'].items()}
    if capture['verbs'] != expected:
        raise ValueError('live verb records differ from disk')
    if int(capture['table_unslid_address'], 16) != int(disk['summary']['address'], 16):
        raise ValueError('live table location differs from disk')
    return {
        'binary_sha256': hashlib.sha256(raw).hexdigest(),
        'image_uuid_matches': True,
        'build_matches': True,
        'table_address_matches': True,
        'all_name_id_flags_records_match': True,
        'records': len(expected),
        'claim': 'Loaded structured verb table reproduces same-build disk extraction; not independent behaviour proof.',
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('capture', type=Path)
    p.add_argument('--binary', type=Path, default=Path(BINARY))
    p.add_argument('--output', type=Path, help='new evidence artifact; refuses to overwrite')
    args = p.parse_args()
    capture = json.loads(args.capture.read_text())
    capture['verification'] = verify(capture, args.binary)
    text = json.dumps(capture, indent=2) + '\n'
    if args.output:
        with args.output.open('x') as f:
            f.write(text)
    print(json.dumps(capture['verification'], indent=2))


if __name__ == '__main__':
    main()
