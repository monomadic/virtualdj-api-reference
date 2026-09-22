#!/usr/bin/env python3
"""Guarded 9246 button color-name bindings; structural evidence, not support."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'tests/skin-color-helpers-9246.json'


def bindings(analysis, manifest):
    from skin_node_helpers import verify_guards
    data = json.loads(manifest.read_text())
    verify_guards(data, hashlib.sha256(analysis.img.data).hexdigest(),
                  lambda fn: b''.join(w.to_bytes(4, 'little') for _, w in analysis.words(fn)))
    return {int(row['pc'], 16): row for row in data['bindings']}, data


def record(app):
    from extract_skin_classes import Analysis, decoded
    from extract_action_vtables import demangled, symbol_maps
    from skin_schema import analyze, UNKNOWN
    from plugin_memory import verify
    baseline = json.loads((ROOT / 'tests/skin-schema-button-expanded-9246.json').read_text())
    verified = verify(json.loads((ROOT / 'tests/plugin-memory-9246.json').read_text()), app / 'Contents/MacOS/VirtualDJ')
    if verified['binary_sha256'] != baseline['source']['binary_sha256']:
        raise ValueError('this reviewed model requires the historical baseline image')
    a = Analysis(app)
    if hashlib.sha256(a.img.data).hexdigest() != verified['binary_sha256']:
        raise ValueError('binary changed during extraction')
    symbols, _ = symbol_maps(demangled(app / 'Contents/MacOS/VirtualDJ', 'arm64'))
    caller = int(baseline['constructor'], 16)
    helper = [fn for fn, name in symbols.items() if name.startswith('ISkinObject::getColorParam(CXMLNode*,') and name.endswith(', unsigned int)')]
    if len(helper) != 1:
        raise ValueError('color helper ambiguous')
    helper = helper[0]
    code = decoded(a, caller)
    states = {i.address: state for i, _, state in analyze(code, {}, {}, a.img.strings, conditional_select=True)}
    branches = {i.operands[-1].imm for i in code if i.mnemonic in ('b', 'cbz', 'cbnz', 'tbz', 'tbnz') or i.mnemonic.startswith('b.')}
    rows, constructors = [], set()
    for idx, ins in enumerate(code):
        if ins.mnemonic != 'bl' or ins.operands[0].imm != helper:
            continue
        j = idx - 1
        while j >= 0 and code[j].mnemonic != 'bl':
            j -= 1
        between = code[j+1:idx]
        # Only the observed straight-line, same-SP lifetime. No generic alias model.
        expected = [('mov','x2, sp'), ('mov','x0, x19'), ('mov','x1, x22')]
        actual = [(i.mnemonic, i.op_str) for i in between]
        if actual not in [expected + [('mov','w3, #0')], [('ldr','w3, [x19, #0x2e0]')] + expected,
                          [('ldr','w3, [x19, #0x2ec]')] + expected]:
            raise ValueError('temporary color-string binding changed')
        if any(i.address in branches for i in code[j+1:idx+1]):
            raise ValueError('branch bypasses string construction')
        if j < 1 or (code[j-1].mnemonic,code[j-1].op_str) != ('mov','x0, sp'):
            raise ValueError('string destination is not the reviewed stack object')
        ctor = code[j].operands[0].imm
        if 'basic_string' not in symbols.get(ctor,'') or not symbols[ctor].endswith('(char const*)'):
            raise ValueError('unexpected string construction')
        constructors.add(ctor)
        values = states[code[j].address].get('x1', UNKNOWN)
        if any(k != 'constant' or v not in a.img.strings for k,v in values):
            raise ValueError('color-name alternative unresolved')
        literals = sorted({a.img.strings[v] for k,v in values})
        rows.append({'pc': hex(ins.address), 'caller': hex(caller), 'target': hex(helper),
                     'string_constructor_pc': hex(code[j].address), 'node_register': 'x1',
                     'names': [n for n in literals if n != 'dontfindme'],
                     'internal_fallback_literals': [n for n in literals if n == 'dontfindme'],
                     'literal_addresses': {hex(v): a.img.strings[v] for k,v in sorted(values)},
                     'binding_instructions': [{'pc':hex(i.address),'mnemonic':i.mnemonic,'operands':i.op_str} for i in code[j-1:idx+1]]})
    if not rows:
        raise ValueError('no color bindings recovered')
    routines = {}
    for fn in sorted({caller,helper}|constructors):
        raw = b''.join(w.to_bytes(4,'little') for _,w in a.words(fn))
        routines[symbols[fn]] = {'start':hex(fn),'end':hex(fn+len(raw)),'sha256':hashlib.sha256(raw).hexdigest()}
    return {'schema_version':1,'build':baseline['source']['build'],'binary_sha256':verified['binary_sha256'],
            'evidence_tier':2,'routines':routines,'bindings':rows,
            'interpretation':'Reviewed string constructor copies x1 into the string object at x0. These guarded straight-line sites construct at SP and pass that object as x2 to getColorParam, which reads the first XML key on node x1. CSEL unions alternatives without proving branch feasibility. dontfindme is retained separately as an internal fallback, not a supported attribute.',
            'limitations':['Only these constructor call sites are modeled; no general stack or heap tracking.',
                           'Names are possible reader keys, not runtime behavior or precedence proof.']}


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--app',type=Path,required=True)
    p.add_argument('--output',type=Path)
    p.add_argument('--check',action='store_true')
    args=p.parse_args()
    data=record(args.app)
    if args.check and data != json.loads(DEFAULT.read_text()):
        raise ValueError('color helper evidence drift')
    if args.output:
        with args.output.open('x') as f:
            json.dump(data,f,indent=2); f.write('\n')
    print(json.dumps(data['bindings'],indent=2))
