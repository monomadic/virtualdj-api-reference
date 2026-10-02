#!/usr/bin/env python3
"""Recover the fixed 9246 parser host's guards from same-build named arm64 code.

Needs capstone and numpy for extraction only. Does not execute vendor code.
The reviewed layout patterns below are scoped to the pinned binary, not a general
C++ layout inference algorithm. Preserve full bounded instructions as evidence.
"""
import argparse
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'tests/parser-object-layout-9246.json'


def prepare(app):
    from capstone import Cs, CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN
    from extract_verb_table import sections, slice_offset
    from extract_skin_classes import function_starts
    from extract_action_vtables import demangled, symbol_maps
    from extract_action_contracts import rtti_graph
    from plugin_memory import verify

    binary = app / 'Contents/MacOS/VirtualDJ'
    raw = binary.read_bytes()
    source = json.loads((ROOT / 'tests/tail-consumers-9246.json').read_text())['source']
    if hashlib.sha256(raw).hexdigest() != source['binary_sha256']:
        raise ValueError('not the previously anchored symbol-rich binary')
    memory_path = ROOT / 'tests/plugin-memory-9246.json'
    memory = json.loads(memory_path.read_text())
    verified = verify(memory, binary)
    symbols, vtables = symbol_maps(demangled(binary, 'arm64'))
    base = slice_offset(raw)
    text = next(s for s in sections(raw, base) if s[1] == '__text')
    starts = function_starts(SimpleNamespace(data=raw, base=base))
    ends = dict(zip(starts, starts[1:]))
    graph = rtti_graph(raw, prefixes=('ACTION_is_using',))['ACTION_is_using']
    if graph['vtable'] != vtables['ACTION_is_using'] + 16 or graph['bases'] != ['IAction']:
        raise ValueError('named vtable and RTTI disagree')
    md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)

    def unique(name):
        matches = [a for a, n in symbols.items() if n == name]
        if len(matches) != 1:
            raise ValueError('ambiguous or absent symbol: '+name)
        return matches[0]

    def routine(address):
        if address not in ends:
            raise ValueError('symbol not at bounded function start')
        size = ends[address] - address
        offset = base + text[4] + address - text[2]
        body = raw[offset:offset+size]
        decoded = list(md.disasm(body, address))
        if sum(i.size for i in decoded) != size:
            raise ValueError('incomplete bounded decoding')
        ins = []
        for i in decoded:
            row = {'pc': hex(i.address), 'instruction': i.mnemonic + (' '+i.op_str if i.op_str else '')}
            if i.mnemonic in ('bl', 'b') and i.op_str.startswith('#0x'):
                row['target'] = i.op_str[1:]
                row['target_symbol'] = symbols.get(int(i.op_str[1:], 16))
            ins.append(row)
        return {'symbol': symbols.get(address), 'start': hex(address), 'end': hex(ends[address]),
                'sha256': hashlib.sha256(body).hexdigest(), 'instructions': ins}

    targets = {
        'create_candidate': unique('IAction::create(char const*, char const**, int)'),
        'parameter_reader': unique('IAction::getParam(int)'),
        'constructor': unique('IAction::IAction()'),
        'delete_destructor': graph['slots'][1],
        'complete_destructor': graph['slots'][0],
        'consumer': graph['slots'][3],
        'GetInfo': unique('CPlugin::GetInfo(char const*, double*)'),
        'parameter_destructor': unique('SActionParam::~SActionParam()'),
        'parameter_float': unique('SActionParam::toFloat()'),
        'parameter_text': unique('SActionParam::toString()'),
        'vector_push': unique('std::__1::vector<SActionParam, std::__1::allocator<SActionParam>>::push_back[abi:ne200100](SActionParam&&)'),
    }
    delete = routine(targets['delete_destructor'])
    bases = {int(i['target'], 16) for i in delete['instructions'] if i.get('target_symbol') == 'IAction::~IAction()'}
    if len(bases) != 1 or delete['symbol'] != 'ACTION_is_using::~ACTION_is_using()':
        raise ValueError('deleting destructor chain unresolved')
    targets['base_destructor'] = bases.pop()
    routines = {key: routine(address) for key, address in targets.items()}

    def require(key, *patterns):
        evidence = []
        for pattern in patterns:
            matches = [i for i in routines[key]['instructions'] if i['instruction'] == pattern]
            if not matches:
                raise ValueError('reviewed pattern changed: '+key+' '+pattern)
            evidence.extend(matches)
        return evidence

    evidence = {
        'vector_begin_end_and_stride': require('parameter_reader', 'ldp x9, x8, [x0, #0x20]', 'mov w8, #0x28', 'smaddl x0, w1, w8, x9'),
        'vector_end_capacity': require('vector_push', 'ldp x8, x9, [x0, #8]', 'cmp x8, x9', 'add x0, x8, #0x28', 'str x0, [x19, #8]'),
        'initial_reference': require('constructor', 'mov w8, #1', 'str w8, [x0, #8]'),
        'release': require('GetInfo', 'add x8, x21, #8', 'ldaddal w9, w8, [x8]', 'ldr x8, [x8, #8]', 'blr x8'),
        'argument_abi': require('GetInfo', 'mov x0, x1', 'mov x1, #0', 'mov w2, #0', f'bl #{hex(targets["create_candidate"])}'),
        'parameter_tag_and_payload': require('parameter_float', 'ldr w8, [x0]', 'ldr s0, [x0, #4]'),
        'string_storage': require('parameter_text', 'ldrsb w8, [x0, #0x1f]', 'ldur q0, [x0, #8]', 'ldur x8, [x0, #0x18]'),
        'string_destruction': require('parameter_destructor', 'ldrsb w8, [x0, #0x1f]', 'ldr x0, [x19, #8]'),
    }
    return {
        'build': '18.0.9246', 'arch': 'arm64', 'image_uuid': memory['image_uuid'],
        'binary_sha256': verified['binary_sha256'], 'evidence_tier': 2,
        'memory_anchor_sha256': hashlib.sha256(memory_path.read_bytes()).hexdigest(),
        'routines': routines, 'expected_vtable': hex(graph['vtable']),
        'named_vtable_symbol_address': hex(vtables['ACTION_is_using']),
        'layout_leads': {'refcount_offset': 8, 'parameter_begin_offset': 32,
                         'parameter_end_offset': 40, 'parameter_capacity_offset': 48, 'parameter_stride': 40},
        'layout_evidence': evidence,
        'scope': 'Same-build named methods and RTTI with reviewed bounded instruction patterns. Fixed is_using suite only; not live behavior proof. No 9644 addresses used.',
        'limits': ['C++ string representation is reviewed for this build; fixed suite uses short text only.',
                   'Reference release follows the named GetInfo callback and named deleting destructor.',
                   'No same-build live parser-object capture; compare offline fields with the separately labeled 9644 baseline.'],
    }


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--app', type=Path, required=True)
    p.add_argument('--output', type=Path, default=DEFAULT)
    p.add_argument('--check', action='store_true')
    a = p.parse_args()
    result = prepare(a.app)
    if a.check:
        if json.loads(a.output.read_text()) != result:
            raise SystemExit('named parser guards differ')
        print('9246 named parser guards reproduce')
    else:
        with a.output.open('x') as f:
            f.write(json.dumps(result, indent=2)+'\n')
        print('Wrote '+str(a.output))
