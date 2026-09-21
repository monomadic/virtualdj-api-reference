#!/usr/bin/env python3
"""Minimal synthetic conditional XML fixture; no transport or media actions."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct
import zlib

HERE = Path(__file__).resolve().parent
NAME = 'ZZ Schema Conditions 9644'
INSTALL = Path.home() / 'Library/Application Support/VirtualDJ/Skins' / NAME
ROWS = [
    ('pos-baseline', 'pos', ''),
    ('pos-false-first', 'pos', 'condition="off"'),
    ('pos-true-first', 'pos', 'condition="on"'),
    ('pos-attr-control', 'pos', 'zzcondition="off"'),
    ('size-false-first', 'size', 'condition="off"'),
    ('size-attr-control', 'size', 'zzcondition="off"'),
    ('up-false-first', 'up', 'condition="off"'),
    ('up-true-first', 'up', 'condition="on"'),
    ('up-attr-control', 'up', 'zzcondition="off"'),
]


def png(width, height):
    raw = (b'\0' + bytes((17, 23, 31)) * width) * height
    def chunk(tag, body):
        return struct.pack('>I', len(body)) + tag + body + struct.pack('>I', zlib.crc32(tag+body) & 0xffffffff)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b'')


def files():
    parts = ['<skin name="ZZ Schema Conditions 9644" version="8" width="1200" height="720">']
    parts.append('<textzone x="25" y="15" width="1100" height="35"><text font="Arial" size="20" color="#FFFFFF" format="XML CONDITION OWNERSHIP - synthetic test"/></textzone>')
    cases = []
    for n, (name, tag, attr) in enumerate(ROWS, 1):
        y = 65 + (n-1)*68
        parts.append(f'<textzone x="25" y="{y+8}" width="310" height="30"><text font="Arial" size="18" color="#FFFFFF" format="{n}. {name}"/></textzone>')
        parts.append(f'<button action="set \'$schema_condition_{n}\' 1">')
        if tag == 'pos':
            parts.append(f'<pos x="360" y="{y}" {attr}/>')
            if name != 'pos-baseline':
                parts.append(f'<pos x="660" y="{y}"/>')
            parts.append('<size width="150" height="44"/>')
        else:
            parts.append(f'<pos x="360" y="{y}"/>')
            parts.append(f'<size width="150" height="44" {attr if tag == "size" else ""}/>')
            if tag == 'size':
                parts.append('<size width="450" height="44"/>')
        if tag == 'up':
            parts.append(f'<up shape="square" color="#E03030" {attr}/><up shape="square" color="#20C060"/>')
        else:
            parts.append('<up shape="square" color="#3080D0"/>')
        parts.append('</button>')
        cases.append({'id': n, 'name': name, 'tag': tag, 'attribute': attr, 'skin_y': y+22,
                      'points': {'left': [430, y+22], 'right': [730, y+22]}})
    parts.append('</skin>')
    return {'skin.xml': ('\n'.join(parts)+'\n').encode(), 'skin.png': png(1200,720), 'preview.png': png(300,180),
            'cases.json': (json.dumps(cases,indent=2)+'\n').encode()}


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--install',action='store_true');p.add_argument('--uninstall',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
    data=files()
    if a.uninstall:
        # Remove only this generated fixture, and only if every installed byte matches.
        if {x.name for x in INSTALL.iterdir()} != {'skin.xml','skin.png','preview.png'}:
            raise ValueError('unexpected files in fixture install')
        for name in ('skin.xml','skin.png','preview.png'):
            if (INSTALL/name).read_bytes()!=data[name]:raise ValueError('installed fixture changed')
        shutil.rmtree(INSTALL)
    else:
        for name,raw in data.items():
            if a.check:
                if (HERE/name).read_bytes()!=raw:raise ValueError('fixture drift: '+name)
            else:(HERE/name).write_bytes(raw)
        if a.install:
            INSTALL.mkdir(exist_ok=False)
            for name in ('skin.xml','skin.png','preview.png'):(INSTALL/name).write_bytes(data[name])
    print(json.dumps({name:hashlib.sha256(raw).hexdigest() for name,raw in data.items()}))
