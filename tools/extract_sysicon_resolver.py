#!/usr/bin/env python3
"""Capture the sysicon comparison chain, not a string-pool adjacency list.

Generation: --extract --app /Applications/VirtualDJ.app --output DIR
Offline lookup: --artifact DIR/manifest.json --get folder
All output is Tier 2; no application code is executed.
"""
import argparse
import hashlib
import json
import plistlib
from pathlib import Path


def extract(app, output):
    from extract_skin_classes import Analysis, decoded, literal_calls

    a = Analysis(app)
    anchors = ('context_menu', 'chevronup', 'sampler_drop', 'arrowleft')
    owners = [{a.owner(pc) for va in a.img.by_text.get(s, [])
               for pc in a.img.xrefs.get(va, [])} for s in anchors]
    common = set.intersection(*owners)
    if len(common) != 1:
        raise ValueError('sysicon resolver anchors do not identify one function')
    resolver = common.pop()
    readers = {a.owner(pc) for va in a.img.by_text.get('sysicon', [])
               for pc in a.img.xrefs.get(va, [])}
    callers = [(fn, pc) for fn in readers for pc, target in a.calls(fn)
               if target == resolver]
    if not callers:
        raise ValueError('no sysicon XML reader calls the anchored resolver')
    captures = {'resolver': resolver}
    captures.update({f'xml-reader-{n}': fn for n, fn in enumerate(sorted({f for f, _ in callers}))})
    # x2 literals are suffix predicates; capture their helpers and direct callees.
    predicates = literal_calls(a, resolver, 'x2')
    for n, target in enumerate(sorted({r['target'] for r in predicates})):
        captures[f'predicate-{n}'] = target
        # Tail-called helper is still part of the predicate contract.
        for i in decoded(a, target):
            if i.mnemonic == 'b' and i.operands[0].imm in a.starts:
                captures[f'predicate-{n}-tail'] = i.operands[0].imm
    output.mkdir(parents=True, exist_ok=True)
    files = {}
    for label, fn in captures.items():
        refs = dict(a.refs.get(fn, []))
        body = '\n'.join(f'{i.address:#x}: {i.mnemonic} {i.op_str}' +
                         (f' ; {refs[i.address]!r}' if i.address in refs else '')
                         for i in decoded(a, fn)) + '\n'
        path = output / f'{label}.asm'
        path.write_text(body)
        files[label] = {'address': hex(fn), 'file': path.name,
                        'sha256': hashlib.sha256(body.encode()).hexdigest()}
    records = []
    for register, role in [('x1', 'comparison literal'), ('x2', 'suffix predicate'),
                           ('x0', 'action construction; not an icon key')]:
        for row in literal_calls(a, resolver, register):
            records.append({**row, 'argument_register': register, 'role': role})
    result = {
        'evidence_tier': 2,
        'scope': 'Static arm64 resolver capture; no rendering or live behavior test',
        'build': plistlib.loads((app / 'Contents/Info.plist').read_bytes())['CFBundleVersion'],
        'binary_sha256': hashlib.sha256(a.img.data).hexdigest(),
        'architecture': 'arm64',
        'resolver': hex(resolver),
        'xml_calls': [{'reader': hex(fn), 'call_pc': hex(pc)} for fn, pc in callers],
        'captures': files,
        'literal_calls': sorted(records, key=lambda r: r['pc']),
        'limitations': [
            'Conservative register tracking can omit literals; assembly is the audit source.',
            'Comparison literals include prefix matches and special cases, not just exact keys.',
            'No universal absence claim about other icon consumers or other builds.'],
    }
    (output / 'manifest.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--extract', action='store_true')
    p.add_argument('--app', type=Path, default=Path('/Applications/VirtualDJ.app'))
    p.add_argument('--output', type=Path, default=Path('tests/sysicon-resolver-9598'))
    p.add_argument('--artifact', type=Path, default=Path('tests/sysicon-resolver-9598/manifest.json'))
    p.add_argument('--get')
    args = p.parse_args()
    data = extract(args.app, args.output) if args.extract else json.loads(args.artifact.read_text())
    if args.get:
        data = {'build': data['build'], 'evidence_tier': data['evidence_tier'],
                'matches': [r for r in data['literal_calls'] if r['name'] == args.get]}
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
