#!/usr/bin/env python3
"""Recover named child readers and composition call sites from symbol-rich 9246."""
import argparse
import bisect
import json
import plistlib
from pathlib import Path
import offline_parser as base

DEFAULT = base.ROOT / 'tests/skin-child-readers-9246.json'


def generate(app, output):
    import numpy as np
    from extract_skin_classes import Analysis, literal_calls, decoded
    from extract_action_vtables import demangled, symbol_maps
    from extract_action_contracts import rtti_graph
    if output.exists():
        raise ValueError('capture already exists')
    a = Analysis(app)
    build = plistlib.loads((app / 'Contents/Info.plist').read_bytes())['CFBundleVersion']
    expected = json.loads(base.manifest_for('18.0.9246').read_text())
    if build != '18.0.9246' or base.digest(a.img.data) != expected['binary_sha256']:
        raise ValueError('requires reviewed symbol-rich 9246 source')
    a.symbols, _ = symbol_maps(demangled(app / 'Contents/MacOS/VirtualDJ', 'arm64'))
    graph = rtti_graph(a.img.data, ('CSkin', 'ISkin'))
    def inherits(name, target, seen=()):
        return name == target or (name not in seen and any(inherits(b, target, (*seen, name)) for b in graph.get(name, {}).get('bases', [])))
    classes = {n: dict(r, container_base=inherits(n, 'ISkinContainer')) for n, r in graph.items() if inherits(n, 'ISkinObject')}
    targets = {addr: name for addr, name in a.symbols.items() if name.startswith(('ISkinObject::createSkinObject(', 'CSkinPanel::loadChildren(', 'CSkinRack::loadChildren('))}
    # Decode only aligned direct B/BL instructions in __text, then assign real function bounds.
    sec = a.img.text
    words = np.frombuffer(a.img.data, dtype='<u4', count=sec[3] // 4, offset=a.img.base + sec[4])
    ix = np.nonzero((words & 0x7c000000) == 0x14000000)[0]
    imm = (words[ix] & 0x3ffffff).astype(np.int64)
    imm = np.where(imm & 0x2000000, imm - 0x4000000, imm)
    pcs = sec[2] + ix * 4
    dests = pcs + imm * 4
    dispatch_calls = []
    for target, name in targets.items():
        for j in np.nonzero(dests == target)[0]:
            pc = int(pcs[j]); owner = a.owner(pc)
            dispatch_calls.append(dict(pc=hex(pc), function=hex(owner), caller=a.symbols.get(owner), target=hex(target), callee=name, instruction='bl' if int(words[ix[j]]) & 0x80000000 else 'b'))
    named_reads, constructor_calls, tag_comparisons, helper_reads, comparisons = [], [], [], [], []
    reviewed = set()
    for fn, name in sorted(a.symbols.items()):
        if not name.startswith(('CSkin', 'ISkin')) or fn not in a.starts:
            continue
        calls = a.calls(fn)
        interesting = any(a.symbols.get(t, '').startswith(('CXMLNode::getChild(', 'ISkinObject::getCondition(', 'CSkin')) for _, t in calls)
        if not interesting and fn not in targets:
            continue
        for pc, target in calls:
            callee = a.symbols.get(target, '')
            cls = callee.split('::')[0]
            if cls in classes and callee.startswith(cls + '::' + cls + '('):
                constructor_calls.append(dict(pc=hex(pc), function=hex(fn), caller=name, callee=callee, child_class=cls))
        for register in ['x1', 'x2']:
            for call in literal_calls(a, fn, register):
                callee = a.symbols.get(call['target'], '')
                row = dict(caller=name, function=hex(fn), pc=hex(call['pc']), name=call['name'], target=hex(call['target']), callee=callee, argument_register=register)
                if (register == 'x1' and callee.startswith('CXMLNode::getChild(')) or (register == 'x2' and callee.startswith('ISkinObject::getCondition(')):
                    named_reads.append(row); reviewed.add(fn)
                if register == 'x1' and callee.startswith('CSkinButton::addTextObject('):
                    helper_reads.append(row); reviewed.add(fn)
                if register == 'x1' and callee.startswith('strIsEqualCI('):
                    comparisons.append(row)
                if register == 'x1' and fn in targets and callee.startswith('strIsEqualCI('):
                    tag_comparisons.append(row); reviewed.add(fn)
    # Keep bounded instructions for the recursive loaders and direct factory callers.
    reviewed.update(targets)
    reviewed.update(int(r['function'], 16) for r in dispatch_calls)
    routines = []
    for fn in sorted(reviewed):
        raw = b''.join(w.to_bytes(4, 'little') for _, w in a.words(fn))
        routines.append(dict(address=hex(fn), symbol=a.symbols.get(fn), size=len(raw), sha256=base.digest(raw), instructions=[dict(pc=hex(i.address), instruction=i.mnemonic + ' ' + i.op_str) for i in decoded(a, fn)] if fn in targets or any(r['function'] == hex(fn) for r in dispatch_calls) else []))
    result = dict(source=dict(build=build, architecture='arm64', binary_sha256=base.digest(a.img.data), evidence_tier=2), classes=classes, dispatch_calls=dispatch_calls, named_child_reads=named_reads, constructor_calls=constructor_calls, loader_tag_comparisons=tag_comparisons, literal_comparisons=comparisons, named_child_helper_calls=helper_reads, routines=routines, limitations=['RTTI inheritance is not XML child acceptance.', 'A named lookup may read a nested configuration node; method ownership alone does not establish its XML parent.', 'Constructor calls may create generated objects or invoke base constructors; they do not by themselves establish containment.', 'Only direct B/BL dispatch calls and straight-line recoverable literal arguments are captured; indirect dispatch and dynamic child names remain unresolved.', 'Tier 2 binary evidence; pair with native fixtures, then same-build live-app observations.'])
    output.write_text(json.dumps(result, indent=2) + '\n')
    return result


def show(data, name):
    prefix = name + '::'
    return dict(source=data['source'], native_class=data['classes'].get(name), named_child_reads=[r for r in data['named_child_reads'] if r['caller'].startswith(prefix)], dispatch_calls=[r for r in data['dispatch_calls'] if (r['caller'] or '').startswith(prefix)], named_child_helper_calls=[r for r in data['named_child_helper_calls'] if r['caller'].startswith(prefix)], literal_comparisons=[r for r in data['literal_comparisons'] if r['caller'].startswith(prefix)], constructor_calls=[r for r in data['constructor_calls'] if r['caller'].startswith(prefix)], limitations=data['limitations'])


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--app', type=Path)
    p.add_argument('--output', type=Path, default=DEFAULT)
    p.add_argument('--class', dest='class_name', default='CSkinPanel')
    args = p.parse_args()
    data = generate(args.app, args.output) if args.app else json.loads(args.output.read_text())
    print(json.dumps(show(data, args.class_name), indent=2))
