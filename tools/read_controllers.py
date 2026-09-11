#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pycryptodome==3.23.0"]
# ///
"""Read VirtualDJ controllers.dat: RSA-recovered Blowfish key, ECB-encrypted ZIP.

Tier 2 extraction, not hardware behavior proof. No installed files are modified.
Run with `uv run tools/read_controllers.py --help` (PEP 723 dependency).
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import plistlib
import struct
import xml.etree.ElementTree as ET
import zipfile

# Public verification modulus, recovered from _controllersPublicKey in 18.0.9246.
# Its bytes are checked against the selected app, so key rotation fails explicitly.
PUBLIC_MODULUS = bytes.fromhex(
    '00c795f9764019d905f00e1caae033f48a50fe4e1870b88e8970480898a4696eeeb'
    '1ae12e3f78aefa4f129ea7ff67a9fac2c8ede70dbb95fd4343b3050aa69663f3fa'
    'e5f9b08070a535a5bcff92145bda05b5a43d00efbdbf22625de7acc0612ac87d460'
    '19c0b4ee10a65073e962b8710ed70b98f760f4c64d63105d17ab82d435')
PUBLIC_EXPONENT = 65537
MAX_MEMBER_SIZE = 64 * 1024 * 1024
MAX_TOTAL_SIZE = 512 * 1024 * 1024


def sha(data):
    return hashlib.sha256(data).hexdigest()


def recover_key(signature):
    if len(signature) != 128:
        raise ValueError('truncated RSA block')
    value = int.from_bytes(signature, 'big')
    modulus = int.from_bytes(PUBLIC_MODULUS, 'big')
    if value >= modulus:
        raise ValueError('RSA representative outside modulus')
    decoded = pow(value, PUBLIC_EXPONENT, modulus).to_bytes(128, 'big')
    marker = decoded.find(b'\x00', 2)
    if (not decoded.startswith(b'\x00\x01') or marker < 10
            or decoded[2:marker] != b'\xff' * (marker - 2)):
        raise ValueError('invalid RSA PKCS#1 type-1 padding')
    payload = decoded[marker + 1:]
    if not payload.startswith(b'VDJ') or not 4 <= len(payload[3:]) <= 56:
        raise ValueError('invalid VDJ key envelope')
    return payload[3:]


def decode(data):
    from Crypto.Cipher import Blowfish
    if not data:
        raise ValueError('empty controllers.dat')
    offset, previous, blocks = 0, 0, []
    while offset < len(data):
        if len(data) - offset < 148:
            raise ValueError(f'truncated block header at {offset}')
        length, predecessor, revision = struct.unpack_from('<III', data, offset)
        if predecessor != previous:
            raise ValueError(f'broken revision chain at {offset}: {predecessor} != {previous}')
        # Loader advances by (length & ~7) + 0x94, including a full final block.
        padded = (length & ~7) + 8
        end = offset + 140 + padded
        if length == 0 or end > len(data):
            raise ValueError(f'invalid payload length at {offset}')
        key = recover_key(data[offset + 12:offset + 140])
        plain = Blowfish.new(key, Blowfish.MODE_ECB).decrypt(data[offset + 140:end])[:length]
        if not plain.startswith(b'PK\x03\x04'):
            raise ValueError(f'not a ZIP archive at {offset}')
        members = []
        with zipfile.ZipFile(io.BytesIO(plain)) as archive:
            infos = archive.infolist()
            if sum(i.file_size for i in infos) > MAX_TOTAL_SIZE:
                raise ValueError('expanded archive exceeds safety limit')
            seen = set()
            for info in infos:
                name = info.filename
                path = PurePosixPath(name)
                if (path.is_absolute() or '..' in path.parts or '\\' in name
                        or not path.parts or ':' in name or info.is_dir()):
                    raise ValueError(f'unsafe/non-file member name: {name!r}')
                if name.casefold() in seen:
                    raise ValueError(f'duplicate member name: {name!r}')
                seen.add(name.casefold())
                if info.file_size > MAX_MEMBER_SIZE:
                    raise ValueError(f'oversize member: {name!r}')
                content = archive.read(info)  # independently checks ZIP CRC
                root = ET.fromstring(content)
                if root.tag not in ('device', 'mapper', 'audio'):
                    raise ValueError(f'unexpected XML root {root.tag!r}: {name}')
                members.append((name, content, root))
        blocks.append(({'offset': offset, 'zip_bytes': length,
                        'predecessor': predecessor, 'revision': revision,
                        'zip_sha256': sha(plain), 'member_count': len(members)}, plain, members))
        offset, previous = end, revision
    return blocks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', type=Path, default=Path('/Applications/VirtualDJ.app'))
    parser.add_argument('--input', type=Path, help='defaults to selected app Resources/controllers.dat')
    parser.add_argument('--output-dir', type=Path, help='new directory; raw XML and ZIP for every block')
    parser.add_argument('--json', type=Path, help='write reproducible manifest here')
    args = parser.parse_args()
    source = args.input or args.app / 'Contents/Resources/controllers.dat'
    binary = (args.app / 'Contents/MacOS/VirtualDJ').read_bytes()
    if PUBLIC_MODULUS not in binary:
        raise ValueError('public modulus absent from selected app; inspect key rotation before decoding')
    info = plistlib.loads((args.app / 'Contents/Info.plist').read_bytes())
    data = source.read_bytes()
    blocks = decode(data)
    # Validate everything before creating any output.
    report = {'evidence_tier': 2, 'source': str(source),
              'bundle_version': info['CFBundleVersion'], 'source_sha256': sha(data),
              'source_bytes': len(data), 'app_binary_sha256': sha(binary),
              'public_modulus_sha256': sha(PUBLIC_MODULUS), 'blocks': [], 'roots': {}}
    roots = Counter()
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=False)
    for index, (metadata, plain, members) in enumerate(blocks):
        block = dict(metadata, members=[])
        for name, content, root in members:
            roots[root.tag] += 1
            block['members'].append({'name': name, 'root': root.tag, 'attributes': dict(root.attrib),
                                     'bytes': len(content), 'sha256': sha(content)})
            if args.output_dir:
                target = args.output_dir / f'block-{index:03d}' / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
        if args.output_dir:
            (args.output_dir / f'block-{index:03d}.zip').write_bytes(plain)
        report['blocks'].append(block)
    report['roots'] = dict(sorted(roots.items()))
    if args.json:
        args.json.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'blocks'} |
                     {'blocks': [b[0] for b in blocks]}, indent=2))


if __name__ == '__main__':
    main()
