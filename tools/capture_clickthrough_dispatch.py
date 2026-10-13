#!/usr/bin/env python3
"""Capture the build-scoped clickthrough loader and container mouse-down path.

Uses the skin-class extractor's RTTI/vtable map and the binary string xrefs.
The captured instructions are Tier-2 structural evidence, not a runtime test.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import plistlib
import struct
from pathlib import Path

from extract_skin_classes import Analysis, decoded, generate

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_APP = Path('/Applications/VirtualDJ.app')
DEFAULT_CAPTURE = ROOT / 'tests/clickthrough-dispatch-9644.json'


def function_record(a: Analysis, start: int) -> dict:
    words = a.words(start)
    if not words:
        raise ValueError(f'no bounded function at {start:#x}')
    raw = b''.join(struct.pack('<I', word) for _, word in words)
    return {
        'start': hex(start),
        'end_exclusive': hex(start + len(raw)),
        'sha256': hashlib.sha256(raw).hexdigest(),
        'instructions': [f'{insn.address:#x}: {insn.mnemonic} {insn.op_str}'.rstrip()
                         for insn in decoded(a, start)],
    }


def capture(app: Path) -> dict:
    classes = generate(app)['classes']
    a = Analysis(app)
    binary = app / 'Contents/MacOS/VirtualDJ'
    build = plistlib.loads((app / 'Contents/Info.plist').read_bytes())['CFBundleVersion']
    owners = {a.owner(pc) for vm in a.img.by_text['clickthrough']
              for pc in a.img.xrefs.get(vm, [])}
    if len(owners) != 1 or None in owners:
        raise ValueError(f'clickthrough reader owner is not unique: {owners}')
    loader = owners.pop()
    loader_insns = decoded(a, loader)
    last_clickthrough_ref = max(pc for vm in a.img.by_text['clickthrough']
                                for pc in a.img.xrefs.get(vm, []))
    stores = [insn for insn in loader_insns if insn.address > last_clickthrough_ref
              and insn.mnemonic == 'str' and insn.op_str == 'w0, [x19, #0x38]']
    if len(stores) != 1:
        raise ValueError('clickthrough field store is not unique')
    calls = [insn for insn in loader_insns if last_clickthrough_ref < insn.address < stores[0].address
             and insn.mnemonic == 'bl']
    if len(calls) != 1:
        raise ValueError('boolean accessor call is not unique')
    boolean_accessor = calls[0].operands[0].imm
    panel = classes['CSkinPanel']['vtable_slots']
    window = classes['CSkinWindow']['vtable_slots']
    # Slot 8 is the virtual mouse-down entry in the historical named vtables.
    # Require the panel and window to share it before using it as the current lead.
    if panel[8] != window[8]:
        raise ValueError('panel/window container mouse-down slots differ')
    dispatch = int(panel[8], 16)
    adjacent_slots = (9, 10, 12, 13, 14)
    for slot in adjacent_slots:
        if panel[slot] != window[slot]:
            raise ValueError(f'panel/window adjacent slot {slot} differs')
    return {
        'source': {'build': build, 'arch': 'arm64',
                   'binary_sha256': hashlib.sha256(binary.read_bytes()).hexdigest(),
                   'evidence_tier': 2},
        'loader_selection': 'unique function owning clickthrough string xrefs',
        'boolean_accessor_selection': 'call between final clickthrough string reference and field store',
        'dispatch_selection': 'shared CSkinPanel and CSkinWindow vtable slot 8; historical named slot',
        'loader': function_record(a, loader),
        'boolean_accessor': function_record(a, boolean_accessor),
        'boolean_accessor_literals': {
            word: [hex(pc) for vm in a.img.by_text.get(word, [])
                   for pc in a.img.xrefs.get(vm, []) if a.owner(pc) == boolean_accessor]
            for word in ('yes', 'true', 'no', 'false')
        },
        'container_mouse_down': function_record(a, dispatch),
        'adjacent_container_slots': {
            str(slot): function_record(a, int(panel[slot], 16))
            for slot in adjacent_slots
        },
        'limitations': [
            'Class and method identities are structural cross-build inferences on the stripped image.',
            'Disassembly shows code paths, not which paths a running skin takes.',
            'Adjacent virtual slots are captured without method names; their event roles require caller evidence.',
            'This does not establish mouse-up, drag, alternate-button, or every nested-container behavior.',
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', type=Path, default=DEFAULT_APP)
    parser.add_argument('--output', type=Path, default=DEFAULT_CAPTURE)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = capture(args.app)
    if args.check:
        if result != json.loads(args.output.read_text()):
            raise SystemExit(f'capture differs from {args.output}')
        print(f'clickthrough dispatch capture matches {args.output}')
    else:
        with args.output.open('x') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
        print(args.output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
