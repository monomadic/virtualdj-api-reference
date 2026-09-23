#!/usr/bin/env python3
"""Capture bounded factory/child-loader evidence, not an XML validity oracle.

Requires capstone/numpy. Pins each image independently; never attaches or calls
private routines. Write a new artifact, preserving previous captures.
"""
import argparse
import hashlib
import json
from pathlib import Path
import plistlib
import struct

from extract_action_vtables import demangled, symbol_maps
from extract_skin_classes import Analysis, decoded, literal_calls
from plugin_memory import verify

ROOT = Path(__file__).resolve().parent.parent


def capture(current, historical):
    anchor = json.loads((ROOT / 'tests/skin-schema-button-9644.json').read_text())
    memory = json.loads((ROOT / 'tests/plugin-memory-9644.json').read_text())
    verification = verify(memory, current / 'Contents/MacOS/VirtualDJ')
    if verification['binary_sha256'] != anchor['source']['binary_sha256']:
        raise ValueError('Current image differs from the inspected factory')
    old_symbols, _ = symbol_maps(demangled(historical / 'Contents/MacOS/VirtualDJ', 'arm64'))
    wanted = {
        'ISkinObject::createSkinObject(CXMLNode*, CImage*, CSkinWindow*)': 0x10036abcc,
        'CSkinPanel::loadChildren(CXMLNode*, CImage*, CSkinWindow*)': 0x1007bb7f4,
    }
    for symbol, address in wanted.items():
        if old_symbols.get(address) != symbol:
            raise ValueError('Historical symbol address changed: ' + symbol)
    images = []
    for app, symbols, selections in [
        (current, {}, [
            ('factory', 0x100396890, [(0x100396890, 0x100396964), (0x100396be8, 0x100396cc8), (0x1003975d0, 0x1003975f0)])]),
        (historical, old_symbols, [
            ('factory', 0x10036abcc, [(0x10036abcc, 0x10036acb8), (0x10036b110, 0x10036b164), (0x10036bfd4, 0x10036c014)]),
            ('panel_children', 0x1007bb7f4, [(0x1007bb7f4, 0x1007bbce4)])]),
    ]:
        a = Analysis(app)
        routines = []
        for role, address, ranges in selections:
            if a.owner(address) != address:
                raise ValueError('Not a function boundary')
            instructions = decoded(a, address)
            code = b''.join(struct.pack('<I', w) for _, w in a.words(address))
            routines.append({
                'role': role, 'address': hex(address), 'symbol': symbols.get(address),
                'end': hex(instructions[-1].address + 4), 'code_sha256': hashlib.sha256(code).hexdigest(),
                'literal_calls': [{**c, 'pc': hex(c['pc']), 'target': hex(c['target']),
                                   'target_symbol': symbols.get(c['target'])} for c in literal_calls(a, address)],
                'instructions': [{'pc': hex(i.address), 'mnemonic': i.mnemonic, 'operands': i.op_str,
                                  **({'callee_symbol': symbols.get(i.operands[0].imm)} if i.mnemonic == 'bl' else {})}
                                 for i in instructions if any(lo <= i.address < hi for lo, hi in ranges)],
            })
        images.append({'build': plistlib.loads((app / 'Contents/Info.plist').read_bytes())['CFBundleVersion'],
                       'binary_sha256': hashlib.sha256(a.img.data).hexdigest(), 'routines': routines})
    return {'schema': 1, 'evidence_tier': 2, 'architecture': 'arm64', 'images': images,
            'current_memory_anchor': 'tests/plugin-memory-9644.json',
            'limitations': ['Disk inspection, not runtime branch observation or rendering proof.',
                            'Historical symbols are not current-image addresses or an ABI guarantee.',
                            'Literal calls include attributes and helper operands, not only element names.',
                            'Selected paths do not exhaust skin surfaces, preprocessing or child readers.']}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--current', type=Path, default=Path('/Applications/VirtualDJ.app'))
    p.add_argument('--historical', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    if a.output.exists():
        raise ValueError('Output already exists')
    result = capture(a.current, a.historical)
    with a.output.open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(a.output)
