#!/usr/bin/env python3
"""Name a schema capture's unresolved call frontier without claiming closure."""
import argparse
import hashlib
import json
from pathlib import Path


def review(app, capture):
    from extract_skin_classes import Analysis
    from extract_action_vtables import demangled, symbol_maps
    data = json.loads(capture.read_text())
    a = Analysis(app)
    if hashlib.sha256(a.img.data).hexdigest() != data['source']['binary_sha256']:
        raise ValueError('frontier capture belongs to another binary')
    symbols, _ = symbol_maps(demangled(app / 'Contents/MacOS/VirtualDJ', 'arm64'))
    groups = {}
    for row in data['frontier']:
        target = row['target']
        if target not in groups:
            fn = int(target, 16) if target else None
            raw = b''.join(w.to_bytes(4, 'little') for _, w in a.words(fn)) if fn else b''
            groups[target] = {'target': target, 'symbol': symbols.get(fn),
                              'sha256': hashlib.sha256(raw).hexdigest() if raw else None,
                              'direct_xml_calls': [{'pc': hex(pc), 'target': hex(t), 'symbol': symbols[t]}
                                                   for pc,t in (a.calls(fn) if fn else [])
                                                   if symbols.get(t, '').startswith('CXMLNode::')],
                              'incoming': []}
        groups[target]['incoming'].append(row)
    return {'schema_version': 1, 'source': data['source'],
            'capture_name': capture.name, 'capture_sha256': hashlib.sha256(capture.read_bytes()).hexdigest(),
            'targets': sorted(groups.values(), key=lambda row: row['target'] or ''),
            'limitations': ['Direct XML calls are a prioritization signal, not a supported-attribute or closure verdict.',
                           'Incoming node registers may be ignored by the callee; signatures alone do not prove consumption.',
                           'No direct XML calls does not exclude indirect calls, tail calls, inline accesses or deeper readers.',
                           'The input traversal frontier does not cover every lifecycle method or template route.']}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('capture', type=Path)
    p.add_argument('--app', type=Path, required=True)
    p.add_argument('--output', type=Path)
    p.add_argument('--check', type=Path, help='compare against an existing review')
    args = p.parse_args()
    data = review(args.app, args.capture)
    if args.check and data != json.loads(args.check.read_text()):
        raise ValueError('frontier review drift')
    if args.output:
        with args.output.open('x') as stream:
            json.dump(data, stream, indent=2)
            stream.write('\n')
    print(json.dumps({'source': data['source'], 'targets': [
        {k: v for k,v in row.items() if k != 'incoming'} for row in data['targets']],
        'limitations': data['limitations']}, indent=2))
