#!/usr/bin/env python3
"""Bounded Tier-2 trace of get_time_sign and its direct shared reader.

No private execution: resolve the current RTTI slot, require a single direct
call, and preserve its routine plus locally formed string/call sites.
"""
import argparse
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

from extract_action_contracts import rtti_graph
from extract_skin_classes import function_starts
from extract_verb_table import BINARY, build_identity, sections, slice_offset


def extract():
    from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
    raw = Path(BINARY).read_bytes()
    base = slice_offset(raw)
    secs = sections(raw, base)
    text = next(s for s in secs if s[1] == '__text')
    strings = next(s for s in secs if s[1] == '__cstring')
    starts = function_starts(SimpleNamespace(data=raw, base=base))
    ends = dict(zip(starts, starts[1:]))
    decoder = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

    def routine(address):
        size = ends[address] - address
        if not 0 < size <= 16384:
            raise ValueError('routine exceeds bound')
        offset = base + text[4] + address - text[2]
        code = raw[offset:offset + size]
        ops = list(decoder.disasm(code, address))
        if sum(i.size for i in ops) != size:
            raise ValueError('incomplete decode')
        return ops, dict(start=hex(address), end=hex(ends[address]),
                        sha256=hashlib.sha256(code).hexdigest(),
                        instructions=[dict(address=hex(i.address), mnemonic=i.mnemonic,
                                           operands=i.op_str) for i in ops])

    graph = rtti_graph(raw, prefixes=('ACTION_get_time_sign',))['ACTION_get_time_sign']
    ops, root = routine(graph['slots'][3])
    calls = [int(i.op_str.removeprefix('#'), 0) for i in ops if i.mnemonic == 'bl']
    if len(calls) != 1:
        raise ValueError('expected single direct shared-reader call')
    ops, reader = routine(calls[0])
    sites, helpers = [], {}
    for a, b, c, d in zip(ops, ops[1:], ops[2:], ops[3:]):
        if not (a.mnemonic == 'adrp' and a.op_str.startswith('x1, #')
                and b.mnemonic == 'add' and b.op_str.startswith('x1, x1, #')
                and c.mnemonic == 'mov' and c.op_str.startswith('x0, x')
                and d.mnemonic == 'bl'):
            continue
        address = int(a.op_str.split('#')[1], 0) + int(b.op_str.split('#')[1], 0)
        if not strings[2] <= address < strings[2] + strings[3]:
            continue
        offset = base + strings[4] + address - strings[2]
        end = raw.find(b'\0', offset, offset + 80)
        if end < 0:
            raise ValueError('unbounded literal')
        literal = raw[offset:end].decode('ascii')
        target = int(d.op_str.removeprefix('#'), 0)
        _, helpers[hex(target)] = routine(target)
        sites.append(dict(literal=literal, literal_address=hex(address),
                          callsite=hex(d.address), helper=hex(target),
                          argument_register=c.op_str.split(', ')[1]))
    return dict(source={**build_identity(BINARY), 'binary_sha256': hashlib.sha256(raw).hexdigest()},
                evidence_tier=2, verb='get_time_sign', vtable=hex(graph['vtable']),
                consumer=root, shared_reader=reader, sites=sites, helpers=helpers,
                limitations=['Local literal/call patterns only; not an exhaustive argument schema.',
                             'Shared-reader interpretation is structural, not live behavior proof.',
                             'An unloaded deck exits before argument processing; use a prepared fixture.'])


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path)
    p.add_argument('--check', type=Path)
    args = p.parse_args()
    result = extract()
    if args.check:
        previous = json.loads(args.check.read_text())
        previous['source']['extracted'] = result['source']['extracted']
        if previous != result:
            raise ValueError('consumer extraction drift')
    if args.output:
        with args.output.open('x') as f:
            json.dump(result, f, indent=2)
            f.write('\n')
    print(json.dumps(result['sites'], indent=2))
