#!/usr/bin/env python3
"""Named skin/XML routine audit; structural leads, never a supported XML schema."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'tests/skin-reader-audit-9246.json'


def button_constructor(a, symbols, targets):
    from extract_skin_classes import decoded
    from skin_schema import analyze, node_paths, UNKNOWN
    constructors = [fn for fn, name in symbols.items()
                    if name.startswith('CSkinButton::CSkinButton(CXMLNode*') and fn in a.starts]
    aliases = {}
    for candidate in constructors:
        code = decoded(a, candidate)
        if len(code) == 1 and code[0].mnemonic == 'b' and code[0].operands[0].imm in constructors:
            aliases[hex(candidate)] = hex(code[0].operands[0].imm)
    bodies = [fn for fn in constructors if hex(fn) not in aliases]
    if len(bodies) != 1 or any(target != hex(bodies[0]) for target in aliases.values()):
        raise ValueError('named button constructor is not unique')
    fn = bodies[0]
    getters = {addr: {'role': 'child_node' if name.startswith('CXMLNode::getChild(')
                     else 'attribute_named_reader_candidate'}
               for addr, name in targets.items()
               if name.startswith(('CXMLNode::get', 'CXMLNode::has', 'CXMLNode::is'))
               and name.endswith(' const')}
    reads, frontier = [], []
    for insn, target, state in analyze(decoded(a, fn),
            {'x1': frozenset({('node', '/button')})}, getters, a.img.strings):
        if target in getters:
            receiver, name = state.get('x0', UNKNOWN), state.get('x1', UNKNOWN)
            reads.append({'pc': hex(insn.address), 'getter': hex(target),
                          'symbol': symbols[target], 'role': getters[target]['role'],
                          'node_paths': node_paths(receiver),
                          'names': sorted({a.img.strings[v] for k, v in name
                                           if k == 'constant' and v in a.img.strings}),
                          'receiver_unresolved': any(k != 'node' for k, v in receiver),
                          'name_unresolved': any(k != 'constant' or v not in a.img.strings for k, v in name)})
        else:
            nodes = {reg: node_paths(value) for reg, value in state.items()
                     if reg in {'x'+str(n) for n in range(8)} and node_paths(value)}
            if nodes:
                frontier.append({'pc': hex(insn.address), 'target': hex(target) if target else None,
                                 'symbol': symbols.get(target), 'node_arguments': nodes})
    raw = b''.join(w.to_bytes(4, 'little') for _, w in a.words(fn))
    return {'function': hex(fn), 'symbol': symbols[fn], 'sha256': hashlib.sha256(raw).hexdigest(),
            'single_branch_aliases': aliases,
            'reads': reads, 'frontier': frontier,
            'scope': 'Constructor-only may-analysis. /button labels its CXMLNode* x1 argument from the named signature and arm64 member-call ABI. Factory forwarding is not re-proven here. Direct getChild returns extend paths. Shared helpers are retained in frontier, not traversed. Getter names describe candidates, not runtime support. Only the first name argument is tracked; fallback names and indirect reads remain open.'}


def reader_models(audit, binary_hash, routine_bytes):
    """First-key structural models; refuse another image or changed routine."""
    if audit['source']['binary_sha256'] != binary_hash:
        raise ValueError('named-reader audit belongs to a different binary')
    result = {}
    for address, row in audit['routines'].items():
        if not row['xml_reader_candidate'] or row['symbol'].startswith('CXMLNode::getChild('):
            continue
        fn = int(address, 16)
        raw = routine_bytes(fn)
        if not row['bounded'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
            raise ValueError('named-reader code guard failed')
        result[fn] = {'role': 'attribute_named_reader_candidate',
                      'anchor': row['symbol'], 'node_register': 'x0', 'name_register': 'x1'}
    return result


def extract(app, memory_path):
    from extract_skin_classes import Analysis
    from extract_action_vtables import demangled, symbol_maps
    from plugin_memory import verify
    binary = app / 'Contents/MacOS/VirtualDJ'
    memory = json.loads(memory_path.read_text())
    verified = verify(memory, binary)
    a = Analysis(app)
    if hashlib.sha256(a.img.data).hexdigest() != verified['binary_sha256']:
        raise ValueError('binary changed during extraction')
    symbols, _ = symbol_maps(demangled(binary, 'arm64'))
    # Keep every named XML method, including writers, so filtering cannot silently
    # erase a family. Signatures classify leads, not ABI or behavior contracts.
    targets = {fn: name for fn, name in symbols.items()
               if name.startswith('CXMLNode::') or
               (name.startswith(('CSkin', 'ISkinObject::')) and '(CXMLNode*' in name)}
    starts = set(a.starts)
    routines = {}
    for fn, name in sorted(targets.items()):
        words = a.words(fn)
        raw = b''.join(w.to_bytes(4, 'little') for _, w in words)
        routines[hex(fn)] = {
            'symbol': name,
            'bounded': fn in starts,
            'end': hex(fn + len(raw)) if raw else None,
            'sha256': hashlib.sha256(raw).hexdigest() if raw else None,
            'xml_reader_candidate': name.startswith(('CXMLNode::get', 'CXMLNode::has', 'CXMLNode::is')) and name.endswith(' const'),
            'direct_skin_calls': [],
        }
    skin_functions = {fn: name for fn, name in symbols.items()
                      if fn in starts and name.startswith(('CSkin', 'ISkinObject::'))}
    for fn, name in sorted(skin_functions.items()):
        for pc, target in a.calls(fn):
            if target in targets:
                routines[hex(target)]['direct_skin_calls'].append(
                    {'caller': hex(fn), 'caller_symbol': name, 'pc': hex(pc)})
    return {
        'schema_version': 1,
        'source': {'build': memory['build'], 'arch': 'arm64',
                   'binary_sha256': verified['binary_sha256'], 'image_uuid': memory['image_uuid'],
                   'evidence_tier': 2},
        'memory_verification': verified,
        'routines': routines,
        'button_constructor': button_constructor(a, symbols, targets),
        'limitations': [
            'Symbols and direct BL call sites are structural leads, not behavior proof.',
            'Method signatures do not establish XML node ownership or argument register models.',
            'Callers cover named CSkin/ISkinObject routines at LC_FUNCTION_STARTS boundaries only.',
            'Indirect calls, tail branches, unnamed callers, inlining and template expansion remain outside this audit.',
            'Address aliases use the existing symbol parser shortest-name rule; this is not a complete symbol listing.',
            'Missing callers never establish that a reader is unused or that an attribute is unsupported.',
        ],
    }


def report(data, term):
    rows = {address: row for address, row in data['routines'].items()
            if term.lower() in row['symbol'].lower()}
    return {'source': data['source'], 'routines': rows,
            'summary': {'routines': len(rows),
                        'reader_candidates': sum(r['xml_reader_candidate'] for r in rows.values()),
                        'direct_skin_calls': sum(len(r['direct_skin_calls']) for r in rows.values())},
            'limitations': data['limitations']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('term', nargs='?', default='CXMLNode::get')
    p.add_argument('--capture', type=Path, default=DEFAULT)
    p.add_argument('--app', type=Path)
    p.add_argument('--memory-capture', type=Path, default=ROOT / 'tests/plugin-memory-9246.json')
    p.add_argument('--output', type=Path)
    p.add_argument('--check', action='store_true')
    p.add_argument('--button', action='store_true', help='show constructor-only ownership and helper frontier')
    p.add_argument('--format', choices=['table', 'json'], default='table')
    args = p.parse_args()
    if (args.output or args.check) and not args.app:
        p.error('--output/--check requires --app')
    if args.output and args.output.exists():
        p.error('output already exists')
    data = extract(args.app, args.memory_capture) if args.app else json.loads(args.capture.read_text())
    if args.check and data != json.loads(args.capture.read_text()):
        raise ValueError('named reader audit drift')
    if args.output:
        with args.output.open('x') as f:
            json.dump(data, f, indent=2)
            f.write('\n')
    result = report(data, args.term)
    if args.button:
        print(json.dumps({'source': data['source'], **data['button_constructor']}, indent=2))
        return
    if args.format == 'json':
        print(json.dumps(result, indent=2))
    else:
        print(f"Build {data['source']['build']}, arm64; Tier 2 named-reader audit")
        for address, row in result['routines'].items():
            print(f"{address}  {len(row['direct_skin_calls'])} direct skin calls  {row['symbol']}")
        print('No ownership, support, or completeness claim. --format=json retains call sites and limits.')


if __name__ == '__main__':
    main()
