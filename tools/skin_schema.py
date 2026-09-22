#!/usr/bin/env python3
"""Build-scoped button XML ownership pilot. Queries use stdlib; extraction needs capstone/numpy.

Tracks possible XML-node receivers through bounded ARM64 control flow and direct
calls. A structural read is not runtime support, and absence is never rejection.
"""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'tests/skin-schema-button-conditional-9644.json'
UNKNOWN = frozenset({('unknown', '')})
OVERFLOW = frozenset({('overflow', '')})


def merge(left, right):
    """Unknown on either path must remain unknown, never silently prove ownership."""
    result = {}
    for key in left.keys() | right.keys():
        value = left.get(key, UNKNOWN) | right.get(key, UNKNOWN)
        result[key] = value if len(value) <= 8 and not any(k == 'overflow' for k, _ in value) else OVERFLOW
    return result


def node_paths(value):
    return sorted(v for kind, v in value if kind == 'node')


def transfer(insn, state, getters, strings=None, conditional_select=False):
    """Transfer only understood 64-bit copies/constants; invalidate all other writes.

    No stack/heap alias model. Callee-saved registers survive calls; x0-x18 do not.
    Getter roles are calibrated by the existing structural extractor.
    """
    op = insn.operands
    def reg(operand):
        return insn.reg_name(operand.reg)
    def value(operand):
        if operand.type == 1:
            return state.get(reg(operand), UNKNOWN)
        if operand.type == 2:
            return frozenset({('constant', operand.imm)})
        return UNKNOWN
    result = dict(state)
    computed = UNKNOWN
    if insn.mnemonic in ('adr', 'adrp', 'mov') and len(op) == 2:
        computed = value(op[1])
    elif insn.mnemonic == 'add' and len(op) == 3 and op[2].type == 2:
        shift = getattr(op[2], 'shift', None)
        amount = op[2].imm << (shift.value if shift else 0)
        computed = frozenset(('constant', v + amount) if k == 'constant'
                             else ('unknown', '') for k, v in value(op[1]))
    elif conditional_select and insn.mnemonic == 'csel' and len(op) == 3:
        computed = value(op[1]) | value(op[2])
        if len(computed) > 8 or any(k == 'overflow' for k, _ in computed):
            computed = OVERFLOW
    _, writes = insn.regs_access()
    for r in writes:
        name = insn.reg_name(r)
        result.pop('x' + name[1:] if name.startswith('w') else name, None)
    if op and op[0].type == 1 and reg(op[0]).startswith('x') and computed != UNKNOWN:
        result[reg(op[0])] = computed
    if insn.mnemonic in ('bl', 'blr'):
        for n in range(19):
            result.pop('x' + str(n), None)
        target = op[0].imm if insn.mnemonic == 'bl' else None
        model = getters.get(target, {})
        if model.get('role') in ('child_node', 'conditional_child_node'):
            strings = strings or {}
            receiver = state.get(model.get('node_register', 'x0'), UNKNOWN)
            name_values = state.get(model.get('name_register', 'x1'), UNKNOWN)
            names = frozenset(('literal', strings[v]) if k == 'constant' and v in strings
                              else (k, v) for k, v in name_values)
            children = {('node', p + '/' + n) for p in node_paths(receiver)
                        for k, n in names if k == 'literal'}
            if children:
                if any(k != 'node' for k, _ in receiver) or any(k != 'literal' for k, _ in names):
                    children.add(('unknown', ''))
                result['x0'] = frozenset(children)
        elif model.get('role') == 'matching_sibling_node':
            parents = state.get(model['parent_register'], UNKNOWN)
            nodes = state.get(model['node_register'], UNKNOWN)
            # Same-name sibling retains its XML path, but only under a proven parent.
            paths = {('node', path) for path in node_paths(nodes)
                     if path.rsplit('/', 1)[0] in node_paths(parents)}
            if paths:
                if any(k != 'node' for k, _ in parents | nodes) or len(paths) != len(node_paths(nodes)):
                    paths.add(('unknown', ''))
                result['x0'] = frozenset(paths)
    return result


def analyze(instructions, initial, getters, strings, conditional_select=False):
    """Monotone may-analysis. Follow both branch edges; never infer runtime reachability."""
    code = {i.address: i for i in instructions}
    if not code:
        raise ValueError('empty function')
    entry = instructions[0].address
    states, todo = {entry: initial}, deque([entry])
    steps = 0
    while todo:
        steps += 1
        if steps > 100000:
            raise ValueError('control-flow budget exceeded')
        pc = todo.popleft()
        i, state = code[pc], dict(states[pc])
        out = transfer(i, state, getters, strings, conditional_select)
        if i.mnemonic in ('ret', 'br'):
            successors = []
        elif i.mnemonic == 'b':
            successors = [i.operands[0].imm]
        elif i.mnemonic in ('cbz', 'cbnz', 'tbz', 'tbnz') or i.mnemonic.startswith('b.'):
            successors = [pc + 4, i.operands[-1].imm]
        else:
            successors = [pc + 4]
        for nxt in successors:
            if nxt not in code:
                continue
            new = merge(states[nxt], out) if nxt in states else out
            if nxt not in states or new != states[nxt]:
                states[nxt] = new
                todo.append(nxt)
    calls = []
    for pc, state in sorted(states.items()):
        i = code[pc]
        if i.mnemonic not in ('bl', 'blr', 'br', 'b'):
            continue
        target = i.operands[0].imm if i.mnemonic in ('bl', 'b') else None
        if i.mnemonic == 'b' and target in code:
            continue
        calls.append((i, target, state))
    return calls


def follow_models_for(data, binary_hash, routine_bytes):
    """Validate a bounded, manually reviewed traversal extension."""
    if data['source']['binary_sha256'] != binary_hash:
        raise ValueError('follow manifest belongs to another binary')
    if not 1 <= data['max_depth'] <= 6:
        raise ValueError('invalid follow depth')
    result = {}
    for address, model in data['targets'].items():
        fn = int(address, 16)
        if model['node_register'] not in {'x'+str(n) for n in range(8)}:
            raise ValueError('invalid node argument register')
        if hashlib.sha256(routine_bytes(fn)).hexdigest() != model['sha256']:
            raise ValueError('follow routine code changed')
        result[fn] = model
    return result


def extract(app, memory_capture, structural=None, node_manifest=None, reader_audit=None, color_manifest=None, follow_manifest=None):
    from extract_skin_classes import Analysis, decoded, generate
    from plugin_memory import verify
    binary = app / 'Contents/MacOS/VirtualDJ'
    memory = json.loads(memory_capture.read_text())
    verification = verify(memory, binary)
    source = structural if structural is not None else generate(app)
    if source['source']['binary_sha256'] != verification['binary_sha256']:
        raise ValueError('structural and memory capture binaries differ')
    a = Analysis(app)
    if hashlib.sha256(a.img.data).hexdigest() != verification['binary_sha256']:
        raise ValueError('binary changed during extraction')
    dispatch = [d for d in source['factory']['dispatch'] if d['element'] == 'button']
    constructors = {int(c['constructor'], 16) for d in dispatch for c in d['constructors']
                    if c['class'] == 'CSkinButton'}
    if len(constructors) != 1 or any(d['traversal_exhausted'] for d in dispatch):
        raise ValueError('button constructor is ambiguous')
    constructor = constructors.pop()
    getters = {int(k, 16): v for k, v in source['xml_reader_anchors'].items()}
    from skin_node_helpers import models, MANIFEST
    node_manifest = node_manifest or MANIFEST
    node_models, node_evidence = models(a, node_manifest)
    getters.update(node_models)
    if reader_audit:
        from skin_reader_audit import reader_models
        audit = json.loads(reader_audit.read_text())
        named = reader_models(audit, verification['binary_sha256'],
                              lambda fn: b''.join(w.to_bytes(4, 'little') for _, w in a.words(fn)))
        for fn, model in named.items():
            getters.setdefault(fn, model)
    color_bindings, used_color_bindings = {}, set()
    if color_manifest:
        from skin_color_helpers import bindings
        color_bindings, color_evidence = bindings(a, color_manifest)
    follow_models = {}
    if follow_manifest:
        follow_evidence = json.loads(follow_manifest.read_text())
        follow_models = follow_models_for(follow_evidence, verification['binary_sha256'],
                                          lambda fn: b''.join(w.to_bytes(4, 'little') for _, w in a.words(fn)))
    factory = int(source['factory']['function'], 16)
    factory_code = decoded(a, factory)
    factory_calls = analyze(factory_code, {'x0': frozenset({('node', '/button')})}, getters, a.img.strings)
    constructor_sites = {int(c['call_pc'], 16) for d in dispatch for c in d['constructors']}
    forwarding = [(i, target, state) for i, target, state in factory_calls if i.address in constructor_sites]
    if len(forwarding) != 1 or forwarding[0][2].get('x1') != frozenset({('node', '/button')}):
        raise ValueError('factory no longer forwards its XML receiver to constructor x1')
    base_functions = {a.owner(int(g['call_pc'], 16)) for g in getters.values() if g.get('anchor') == 'clickthrough'}
    queue = deque([(constructor, {'x1': frozenset({('node', '/button')})}, 0)])
    seen, routines, reads, frontier, bindings = set(), {}, [], [], []
    while queue:
        fn, initial, depth = queue.popleft()
        key = (fn, tuple(sorted((r, tuple(sorted(v))) for r, v in initial.items())))
        if key in seen:
            continue
        if len(seen) >= 128:
            raise ValueError('context budget exceeded')
        seen.add(key)
        insns = decoded(a, fn)
        raw = b''.join(w.to_bytes(4, 'little') for _, w in a.words(fn))
        if sum(i.size for i in insns) != len(raw):
            raise ValueError('incomplete routine decoding')
        routines[hex(fn)] = {'end': hex(fn + len(raw)), 'sha256': hashlib.sha256(raw).hexdigest()}
        calls = analyze(insns, initial, getters, a.img.strings, conditional_select=fn in follow_models)
        for i, target, state in calls:
            if i.address in color_bindings:
                binding = color_bindings[i.address]
                if hex(fn) != binding['caller'] or hex(target) != binding['target']:
                    raise ValueError('color call-site binding mismatch')
                receiver = state.get(binding['node_register'], UNKNOWN)
                reads.append({'function': hex(fn), 'pc': hex(i.address), 'getter': hex(target),
                              'origin': 'button_constructor', 'role': 'attribute_color_key_candidate',
                              'names': binding['names'], 'node_paths': node_paths(receiver),
                              'receiver_unresolved': any(k != 'node' for k, _ in receiver),
                              'name_unresolved': False, 'depth': depth,
                              'internal_fallback_literals': binding['internal_fallback_literals']})
                used_color_bindings.add(i.address)
                continue
            role = getters.get(target, {}).get('role')
            model = getters.get(target, {})
            name_values = state.get(model.get('name_register', 'x1'), UNKNOWN) if role != 'matching_sibling_node' else frozenset()
            receiver = state.get(model.get('node_register', 'x0'), UNKNOWN)
            names = sorted({a.img.strings[v] for k, v in name_values
                            if k == 'constant' and v in a.img.strings})
            paths = node_paths(receiver)
            if role:
                reads.append({'function': hex(fn), 'pc': hex(i.address), 'getter': hex(target),
                              'origin': 'shared_base_reader' if fn in base_functions else 'button_constructor' if fn == constructor else 'helper',
                              'role': role, 'names': names, 'node_paths': paths,
                              'receiver_unresolved': any(k != 'node' for k, _ in receiver),
                              'name_unresolved': any(k != 'constant' or v not in a.img.strings
                                                     for k, v in name_values),
                              'depth': depth})
                continue
            args = {r: v for r, v in state.items() if r in {'x'+str(n) for n in range(8)}
                    and node_paths(v)}
            if not args:
                continue
            binding = {'caller': hex(fn), 'pc': hex(i.address),
                       'target': hex(target) if target else None,
                       'literal_arguments': {r: sorted({a.img.strings[v] for k, v in values if k == 'constant' and v in a.img.strings})
                                             for r, values in sorted(state.items()) if r in {'x'+str(n) for n in range(8)}
                                             and any(k == 'constant' and v in a.img.strings for k, v in values)},
                       'node_arguments': {r: node_paths(v) for r, v in sorted(args.items())}}
            text_paths = {'/button/' + name for name in
                          ('text', 'textover', 'textdown', 'textselected', 'textoverselected')}
            follow = depth == 0 or (depth < 3 and any(
                path in text_paths for values in args.values() for path in node_paths(values)))
            explicit_follow = target in follow_models and depth < follow_evidence['max_depth']
            if target in a.starts and (follow or explicit_follow):
                bindings.append(binding)
                # Carry constants too, so a helper's dynamic name argument can resolve.
                inputs = {r: v for r, v in state.items() if r in {'x'+str(n) for n in range(8)}
                          and any(k == 'node' or (k == 'constant' and value in a.img.strings)
                                  for k, value in v)}
                if explicit_follow:
                    node_register = follow_models[target]['node_register']
                    inputs = {r: v for r, v in inputs.items()
                              if r == node_register or not node_paths(v)}
                queue.append((target, inputs, depth + 1))
            else:
                frontier.append(dict(binding, reason='scope/depth limit or indirect/external target'))
    if set(color_bindings) != used_color_bindings:
        raise ValueError("color binding not reached by ownership analysis")
    def unique(rows):
        return [json.loads(s) for s in sorted({json.dumps(r, sort_keys=True) for r in rows})]
    # Retain exact code for the small binding proof, including the constructor thunk.
    binding_code = [i for i in factory_code if i.address <= forwarding[0][0].address]
    thunk = forwarding[0][1]
    if thunk != constructor:
        thunk_code = decoded(a, thunk)
        if len(thunk_code) != 1 or thunk_code[0].mnemonic != 'b' or thunk_code[0].operands[0].imm != constructor:
            raise ValueError('constructor thunk changed')
        binding_code += thunk_code
    return {'schema_version': 2, 'element': 'button', 'evidence_tier': 2,
            **({'follow_models': {'path': str(follow_manifest.relative_to(ROOT)) if follow_manifest.is_relative_to(ROOT) else str(follow_manifest),
                                 'sha256': hashlib.sha256(follow_manifest.read_bytes()).hexdigest(),
                                 **follow_evidence}} if follow_manifest else {}),
            **({'color_key_models': {'path': str(color_manifest.relative_to(ROOT)) if color_manifest.is_relative_to(ROOT) else str(color_manifest),
                                     'sha256': hashlib.sha256(color_manifest.read_bytes()).hexdigest(),
                                     'scope': color_evidence['interpretation']}} if color_manifest else {}),
            **({'named_reader_audit': {'path': str(reader_audit.relative_to(ROOT)) if reader_audit.is_relative_to(ROOT) else str(reader_audit),
                                      'sha256': hashlib.sha256(reader_audit.read_bytes()).hexdigest(),
                                      'scope': 'Named const XML reader first-key arguments only; fallback and extra-name arguments remain open.'}} if reader_audit else {}),
            'conditional_node_models': {'path': str(node_manifest.relative_to(ROOT)) if node_manifest.is_relative_to(ROOT) else str(node_manifest), 'sha256': hashlib.sha256(node_manifest.read_bytes()).hexdigest(),
                                        'models': node_evidence['models'], 'scope': node_evidence['scope']},
            'source': source['source'], 'memory_anchor': {'path': str(memory_capture.relative_to(ROOT)) if memory_capture.is_relative_to(ROOT) else str(memory_capture),
                'sha256': hashlib.sha256(memory_capture.read_bytes()).hexdigest(),
                'image_uuid': memory['image_uuid'], 'verification': verification,
                'scope': 'Existing live image identity only; no skin object was read in this run.'},
            'factory_dispatch': dispatch, 'constructor': hex(constructor),
            'root_binding': {'method': 'Factory x0 XML receiver forwarded to constructor x1; child lookups calibrate the XML role. Structural evidence, not a public ABI.',
                             'factory': hex(factory), 'callsite': hex(forwarding[0][0].address),
                             'instructions': [{'pc': hex(i.address), 'mnemonic': i.mnemonic, 'operands': i.op_str} for i in binding_code]},
            'xml_reader_anchors': ({hex(k): v for k, v in getters.items()} if reader_audit else source['xml_reader_anchors']), 'routines': routines,
            'reads': unique(reads), 'helper_bindings': unique(bindings), 'frontier': unique(frontier),
            'limits': {'call_depth': follow_evidence['max_depth'] if follow_manifest else 3, 'contexts': 128, 'values_per_register': 8,
                       'scope': 'Direct constructor callees; deeper traversal only for named button text-state child receivers.' + (' Additional named readers and their node registers are allowlisted in follow_models.' if follow_manifest else '')},
            'limitations': [
                'Tier 2 possible read paths; branches are not proven feasible and no runtime support is established.',
                'Only constructor-reachable direct calls carrying a tracked XML node, to the stated depth. Other lifecycle methods and indirect calls are not exhausted.',
                'Stack spills, heap aliases and unmodeled helper return values lose provenance. Unknown paths stay unresolved.',
                'Getter roles inherit structural anchor calibration, not an independently recovered XML API.',
                'Child getters may return null; paths describe possible non-null receivers.',
                'Conditional node models retain matching sibling paths, not individual node identity or condition feasibility; a listed path is not an exclusive owner.',
                'No absent name is rejected. Template parameters remain open. Not an XSD or a complete schema.']}


def summary(data):
    owners = {}
    for read in data['reads']:
        if read['role'] in ('child_node', 'conditional_child_node', 'matching_sibling_node'):
            continue
        for path in read['node_paths']:
            row = owners.setdefault(path, {'attributes': set(), 'partial_attributes': set()})
            row['partial_attributes' if read['receiver_unresolved'] or read['name_unresolved'] else 'attributes'].update(read['names'])
    from skin_condition_evidence import live_summary, CAPTURE
    live = live_summary(data['source']['build']) if CAPTURE.exists() else None
    return {'element': data['element'], 'build': data['source']['build'], 'tier': 2,
            'live_evidence': live,
            'owners': {p: {k: sorted(v) for k, v in row.items()} for p, row in sorted(owners.items())},
            'shared_outer_attributes': sorted({name for r in data['reads'] if r['origin'] == 'shared_base_reader'
                                              and '/button' in r['node_paths'] and r['role'].startswith('attribute_') for name in r['names']}),
            'unresolved_reads': sum(r['receiver_unresolved'] or r['name_unresolved'] for r in data['reads']),
            'frontier_calls': len(data['frontier']), 'limitations': data['limitations']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('element', nargs='?', default='button', choices=['button'])
    p.add_argument('--capture', type=Path, default=DEFAULT)
    p.add_argument('--extract', action='store_true')
    p.add_argument('--app', type=Path, default=Path('/Applications/VirtualDJ.app'))
    p.add_argument('--memory-capture', type=Path, default=ROOT / 'tests/plugin-memory-9644.json')
    p.add_argument('--node-manifest', type=Path, help='explicit matching-build conditional-node models')
    p.add_argument('--follow-manifest', type=Path, help='explicit hash-guarded additional reader traversal')
    p.add_argument('--color-manifest', type=Path, help='optional guarded constructor color-name bindings')
    p.add_argument('--reader-audit', type=Path, help='optional matching-image named getter audit')
    p.add_argument('--structural-capture', type=Path, help='optional same-image structural extraction')
    p.add_argument('--output', type=Path)
    p.add_argument('--check', action='store_true', help='re-extract and compare every retained field')
    p.add_argument('--format', choices=['json', 'table'], default='table')
    args = p.parse_args()
    if args.output and not args.extract:
        p.error('--output requires --extract')
    if args.output and args.output.exists():
        p.error('output already exists')
    if args.extract or args.check:
        source = json.loads(args.structural_capture.read_text()) if args.structural_capture else None
        data = extract(args.app, args.memory_capture, source, args.node_manifest, args.reader_audit, args.color_manifest, args.follow_manifest)
        if args.check and data != json.loads(args.capture.read_text()):
            raise ValueError('schema evidence drift')
        if args.output:
            with args.output.open('x') as stream:
                json.dump(data, stream, indent=2)
                stream.write('\n')
    else:
        data = json.loads(args.capture.read_text())
    report = summary(data)
    if args.format == 'json':
        print(json.dumps(report, indent=2))
    else:
        print(f"<{report['element']}> — build {report['build']}, Tier 2 structural pilot")
        for path, row in report['owners'].items():
            print(path + ': ' + ', '.join(row['attributes']))
            if row['partial_attributes']:
                print('  partial/ambiguous: ' + ', '.join(row['partial_attributes']))
        print('Shared outer reads: ' + ', '.join(report['shared_outer_attributes']))
        if report['live_evidence']:
            print('Live fixture (Tier 1): condition on /button/pos, /button/size, /button/up')
            print('  ' + report['live_evidence']['capture'])
        print(f"Unresolved reads: {report['unresolved_reads']}; frontier calls: {report['frontier_calls']}")
        print('Possible reads only, not confirmed support. Unknown names are not rejected.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
