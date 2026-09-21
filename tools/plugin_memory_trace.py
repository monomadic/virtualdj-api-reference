#!/usr/bin/env python3
"""Trace two live-located SDK callbacks in the matching disk image (Tier 2).

Requires capstone only for this optional disassembly command. Addresses come from
verified captures, never from a different build. No process attachment or calls.
"""
import argparse
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

from extract_verb_table import BINARY, sections, slice_offset
from extract_skin_classes import function_starts
from plugin_memory import verify


def trace(capture, binary):
    from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
    verification = verify(capture, binary)
    raw = binary.read_bytes()
    if hashlib.sha256(raw).hexdigest() != verification['binary_sha256']:
        raise ValueError('binary changed after verification')
    base = slice_offset(raw)
    text = next(s for s in sections(raw, base) if s[1] == '__text')
    starts = function_starts(SimpleNamespace(data=raw, base=base))
    ends = dict(zip(starts, starts[1:] + [text[2] + text[3]]))
    decoder = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

    def routine(address):
        if address not in ends or not text[2] <= address < ends[address] <= text[2] + text[3]:
            raise ValueError('callback/callee does not match function-start bounds')
        size = ends[address] - address
        if size > 16384:
            return {'start': hex(address), 'end': hex(ends[address]), 'status': 'exceeds-limit'}
        offset = base + text[4] + address - text[2]
        code = raw[offset:offset + size]
        instructions = list(decoder.disasm(code, address))
        if sum(i.size for i in instructions) != size:
            raise ValueError('decoder did not consume complete function')
        return dict(start=hex(address), end=hex(ends[address]), status='decoded',
                    code_sha256=hashlib.sha256(code).hexdigest(),
                    instructions=[dict(address=hex(i.address), mnemonic=i.mnemonic, operands=i.op_str) for i in instructions],
                    direct_calls=sorted({i.op_str.removeprefix('#') for i in instructions if i.mnemonic == 'bl'}))

    roots = {}
    for slot, label in [(1, 'GetInfo'), (2, 'GetStringInfo')]:
        row = next(r for r in capture['callback_slots'] if r['slot'] == slot)
        if not row['in_host_executable']:
            raise ValueError('callback is outside the host image')
        roots[label] = routine(int(row['unslid_address'], 16))
        if roots[label]['status'] != 'decoded':
            raise ValueError('callback exceeds limit')
    targets = {int(a, 16) for r in roots.values() for a in r['direct_calls']}
    callees = {hex(a): routine(a) for a in sorted(targets) if a in ends}
    return dict(schema=1, evidence_tier=2, build=capture['build'], arch=capture['arch'],
                image_uuid=capture['image_uuid'], binary_sha256=verification['binary_sha256'],
                bounds='LC_FUNCTION_STARTS', maximum_function_bytes=16384, callee_depth=1,
                roots=roots, callees=callees,
                limitations=['Disk disassembly rooted in live callback addresses; no private routine was called.',
                             'Direct calls only; does not identify every parser path or establish private ABI or object lifetime.'])


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('capture', type=Path)
    p.add_argument('--binary', type=Path, default=Path(BINARY))
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    result = trace(json.loads(args.capture.read_text()), args.binary)
    with args.output.open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps({label: row['direct_calls'] for label, row in result['roots'].items()}, indent=2))
