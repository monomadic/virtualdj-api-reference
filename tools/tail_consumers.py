#!/usr/bin/env python3
"""Memory-anchored named parameter-consumer pilot. Structural leads, not a grammar."""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'tests/tail-consumers-shared-9246.json'
PILOT = ('is_using', 'filter_label', 'get_song_event', 'get_time', 'get_time_sign',
         'get_time_hour', 'get_time_min', 'get_time_sec', 'get_time_ms', 'get_time_msf')
SHARED = 'ACTION_get_time::getTime(long long&, SActionParam*&)'


def comparison_kind(symbol):
    if symbol.startswith(('strIsEqualCI(', 'bool SActionParam::isTxt<')):
        return 'exact'
    if symbol.startswith('bool isLeftCIL<'):
        return 'prefix'
    return None


def flow(instructions, get_param):
    # Reuse the conservative constant/call transfer and bounded join used by the
    # XML pilot; add only this experiment's named getParam and +8 text models.
    from skin_schema import UNKNOWN, merge, transfer
    code = {i.address: i for i in instructions}
    states = {instructions[0].address: {'x0': frozenset({('action', 0)})}}
    queue = deque(states)
    steps = 0
    while queue:
        steps += 1
        if steps > 100000:
            raise ValueError('flow budget exceeded')
        pc = queue.popleft()
        i, state = code[pc], states[pc]
        out = transfer(i, state, {})
        op = i.operands
        if i.mnemonic == 'mov' and op[0].type == 1 and i.reg_name(op[0].reg).startswith('w'):
            if op[1].type == 2:
                out['x' + i.reg_name(op[0].reg)[1:]] = frozenset({('constant', op[1].imm & 0xffffffff)})
        if i.mnemonic == 'add' and len(op) == 3 and op[2].type == 2 and op[2].imm == 8 and not op[2].shift.value:
            values = state.get(i.reg_name(op[1].reg), UNKNOWN)
            if any(k == 'param' for k, _ in values):
                out[i.reg_name(op[0].reg)] = frozenset(
                    ('param_text', v) if k == 'param' else ('unknown', '') for k, v in values)
        if i.mnemonic == 'bl' and op[0].imm == get_param:
            receiver, index = state.get('x0', UNKNOWN), state.get('x1', UNKNOWN)
            if receiver == frozenset({('action', 0)}):
                out['x0'] = frozenset(('param', v) if k == 'constant' and 0 <= v < 16
                                       else ('unknown', '') for k, v in index)
        if i.mnemonic in ('ret', 'br'):
            following = []
        elif i.mnemonic == 'b':
            following = [op[0].imm]
        elif i.mnemonic in ('cbz', 'cbnz', 'tbz', 'tbnz') or i.mnemonic.startswith('b.'):
            following = [pc + 4, op[-1].imm]
        else:
            following = [pc + 4]
        for nxt in following:
            if nxt not in code:
                continue
            joined = merge(states[nxt], out) if nxt in states else out
            if states.get(nxt) != joined:
                states[nxt] = joined
                queue.append(nxt)
    return [(i, states[i.address]) for i in instructions
            if i.address in states and i.mnemonic in ('bl', 'blr', 'br', 'b')
            and not (i.mnemonic == 'b' and i.operands[0].imm in code)]


def extract(binary, memory_path):
    from extract_action_vtables import demangled, symbol_maps
    from extract_skin_classes import Analysis, decoded
    from plugin_memory import verify
    memory = json.loads(memory_path.read_text())
    verification = verify(memory, binary)
    if memory['build'] != '18.0.9246':
        raise ValueError('pilot models are scoped to build 9246')
    a = Analysis(binary.parent.parent.parent)
    if hashlib.sha256(a.img.data).hexdigest() != verification['binary_sha256']:
        raise ValueError('binary changed')
    symbols, _ = symbol_maps(demangled(binary, 'arm64'))
    get_param = next(p for p, n in symbols.items() if n == 'IAction::getParam(int)')
    def routine(fn):
        raw = b''.join(w.to_bytes(4, 'little') for _, w in a.words(fn))
        if not raw:
            raise ValueError('symbol is not a bounded routine')
        return {'symbol': symbols.get(fn), 'end': hex(fn + len(raw)),
                'sha256': hashlib.sha256(raw).hexdigest()}
    routines, sites, frontier, bindings = {}, [], [], []
    shared = next(p for p, n in symbols.items() if n == SHARED)
    for fn, name in sorted(symbols.items()):
        if not any(name.startswith('ACTION_' + verb + '::') for verb in PILOT) or '::~' in name:
            continue
        if fn not in a.starts:
            continue
        routines[hex(fn)] = routine(fn)
        for i, state in flow(decoded(a, fn), get_param):
            target = i.operands[0].imm if i.mnemonic in ('bl', 'b') else None
            callee = symbols.get(target, '')
            literals = {r: sorted({a.img.strings[v] for k, v in values
                                  if k == 'constant' and v in a.img.strings})
                        for r, values in state.items() if r in ('x0', 'x1', 'x2', 'x3')}
            literals = {k: v for k, v in literals.items() if v}
            inputs = sorted([list(v) for v in state.get('x0', [])])
            match_kind = comparison_kind(callee)
            comparison = match_kind is not None
            if target == shared:
                bindings.append({'caller': hex(fn), 'pc': hex(i.address), 'target': hex(target),
                                 'receiver': inputs,
                                 'action_receiver_preserved': state.get('x0') == frozenset({('action', 0)})})
            if literals:
                sites.append({'function': hex(fn), 'pc': hex(i.address), 'target': hex(target) if target else None,
                              'callee': callee or None, 'literal_arguments': literals,
                              'comparison': comparison, 'match_kind': match_kind, 'receiver': inputs,
                              'parameter_indices': sorted({v for k, v in state.get('x0', []) if k in ('param', 'param_text')}),
                              'receiver_unresolved': not inputs or any(k not in ('param', 'param_text') for k, v in inputs)})
            else:
                frontier.append({'function': hex(fn), 'pc': hex(i.address), 'callee': callee or None,
                                 'target': hex(target) if target else None,
                                 'reason': 'expanded shared consumer' if target == shared and state.get('x0') == frozenset({('action', 0)}) else 'no resolved literal at comparison' if comparison else 'parameter read' if target == get_param else 'unexpanded call',
                                 'registers': {k: sorted([list(v) for v in values]) for k, values in state.items() if k in ('x0', 'x1')}})
            if (comparison or target == get_param) and target in a.starts:
                routines[hex(target)] = routine(target)
    helpers = {p: n for p, n in symbols.items() if n.startswith(('IAction::get', 'SActionParam::', 'bool SActionParam::isTxt<')) and p in a.starts}
    callers = {hex(p): {'symbol': n, 'direct_action_calls': []} for p, n in helpers.items()}
    for fn, name in sorted(symbols.items()):
        if name.startswith('ACTION_'):
            for pc, target in a.calls(fn):
                if target in helpers:
                    callers[hex(target)]['direct_action_calls'].append({'function': hex(fn), 'symbol': name, 'pc': hex(pc)})
    interesting = {hex(p): n for p, n in sorted(symbols.items())
                   if n.startswith(('SActionParam::serialize', 'SActionParam::unserialize', 'IAction::setSource',
                                    'IAction::create(', 'DLGActionWizard::update', 'DLGActionWizard::getCurrentWord'))
                   or n.endswith('::deckArguments')}
    if not bindings or not all(b['action_receiver_preserved'] for b in bindings):
        raise ValueError('shared time reader binding is unresolved')
    return {'schema': 2, 'source': {'build': memory['build'], 'arch': memory['arch'],
            'image_uuid': memory['image_uuid'], 'binary_sha256': verification['binary_sha256'], 'evidence_tier': 2},
            'memory_anchor': {'capture_sha256': hashlib.sha256(memory_path.read_bytes()).hexdigest(), 'verification': verification},
            'callback_symbols': [{**r, 'symbol': symbols.get(int(r['unslid_address'], 16)) if r['unslid_address'] else None}
                                 for r in memory['callback_slots']],
            'routines': routines, 'literal_sites': sites, 'frontier': frontier,
            'shared_bindings': bindings,
            'shared_consumer': {'function': hex(shared), 'symbol': SHARED,
                'instructions': [{'pc': hex(i.address), 'mnemonic': i.mnemonic, 'operands': i.op_str}
                                 for i in decoded(a, shared)]},
            'parameter_helpers': callers, 'other_symbol_leads': interesting,
            'limitations': ['Named arm64 build-9246 routines only. This is disk analysis anchored to a verified live image, not traced execution.',
                'getParam index and parameter +8 string model are structural ABI leads. No private function is called.',
                'Both branch edges are followed; reachability is not proven. Stack spills, heap loads, inlining and unmodeled helper results lose provenance.',
                'Only selected ACTION class methods and the named shared getTime consumer are analyzed. Shared-call binding requires preserved action receiver; deeper calls remain unexpanded.',
                'Helper caller inventory covers direct BL from named ACTION routines only; no callers does not mean unused.',
                'A literal compared with an unresolved receiver may be an internal name rather than a script argument. No complete vocabulary or behavior claim.']}


def summary(data, verb):
    functions = {p for p, r in data['routines'].items() if r['symbol'] and r['symbol'].startswith('ACTION_' + verb + '::')}
    bindings = [b for b in data.get('shared_bindings', []) if b['caller'] in functions and b['action_receiver_preserved']]
    functions.update(b['target'] for b in bindings)
    return {'source': data['source'], 'verb': verb,
            'shared_bindings': bindings,
            'sites': [s for s in data['literal_sites'] if s['function'] in functions],
            'frontier': [s for s in data['frontier'] if s['function'] in functions], 'limitations': data['limitations']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('verb', nargs='?', choices=PILOT, default='filter_label')
    p.add_argument('--capture', type=Path, default=DEFAULT)
    p.add_argument('--binary', type=Path)
    p.add_argument('--memory-capture', type=Path, default=ROOT / 'tests/tail-probe-9246-memory.json')
    p.add_argument('--output', type=Path)
    p.add_argument('--check', action='store_true')
    p.add_argument('--helpers', action='store_true', help='compact named parameter-helper inventory')
    p.add_argument('--leads', action='store_true', help='other named discovery targets')
    p.add_argument('--format', choices=('table', 'json'), default='table')
    args = p.parse_args()
    if args.binary:
        data = extract(args.binary, args.memory_capture)
        if args.check and data != json.loads(args.capture.read_text()):
            raise ValueError('consumer extraction drift')
        if args.output:
            with args.output.open('x') as f:
                json.dump(data, f, indent=2); f.write('\n')
    else:
        if args.check or args.output:
            p.error('--check/--output requires --binary')
        data = json.loads(args.capture.read_text())
    result = summary(data, args.verb)
    if args.helpers:
        result = {'source': data['source'], 'helpers': {p: {'symbol': r['symbol'], 'direct_action_call_sites': len(r['direct_action_calls'])}
                  for p, r in data['parameter_helpers'].items()}, 'limitations': data['limitations']}
    if args.leads:
        result = {'source': data['source'], 'leads': data['other_symbol_leads'], 'limitations': data['limitations']}
    if args.format == 'json':
        print(json.dumps(result, indent=2))
        return
    print(f"{data['source']['build']} arm64 — Tier 2 named consumer analysis")
    if args.helpers:
        for address, row in result['helpers'].items():
            print(f"{row['direct_action_call_sites']:4} direct ACTION call sites  {row['symbol']}")
    elif args.leads:
        for address, name in result['leads'].items():
            print(address, name)
    else:
        print(f"{args.verb}: parameter indices below are zero-based")
        for site in result['sites']:
            words = ', '.join(sorted({v for values in site['literal_arguments'].values() for v in values}))
            role = ('parameter ' + '/'.join(map(str, site['parameter_indices']))
                    if site['comparison'] and not site['receiver_unresolved'] else
                    'unresolved comparison' if site['comparison'] else 'other literal use')
            if site.get('match_kind') == 'prefix':
                role += ' [prefix family; suffix grammar unresolved]'
            print(f"  {words:32} {role} ({site['pc']})")
        frontier = sorted({s['callee'] or s['target'] or 'indirect call' for s in result['frontier']
                           if s['reason'] == 'unexpanded call'})
        if frontier:
            print('Unexpanded callees (details in --format=json):')
            for name in frontier:
                print('  ' + name)
    print('No completeness or behavior claim; unknown receiver/call paths stay unresolved.')


if __name__ == '__main__':
    main()
