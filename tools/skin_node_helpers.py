#!/usr/bin/env python3
"""Build-9644 guarded structural return models for conditional XML node selection."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'tests/skin-node-helpers-9644.json'


def verify_guards(data, binary_hash, routine_bytes):
    if data['binary_sha256'] != binary_hash:
        raise ValueError('conditional-node model belongs to a different binary')
    for name, row in data['routines'].items():
        body = routine_bytes(int(row['start'], 16))
        if len(body) != int(row['end'], 16) - int(row['start'], 16) or hashlib.sha256(body).hexdigest() != row['sha256']:
            raise ValueError('conditional-node code guard failed: ' + name)


def models(analysis):
    data = json.loads(MANIFEST.read_text())
    verify_guards(data, hashlib.sha256(analysis.img.data).hexdigest(),
                  lambda fn: b''.join(w.to_bytes(4, 'little') for _, w in analysis.words(fn)))
    return {int(data['routines'][name]['start'], 16): model for name, model in data['models'].items()}, data


def record():
    from extract_skin_classes import Analysis, decoded, literal_calls
    from plugin_memory import verify
    app = Path('/Applications/VirtualDJ.app')
    memory = json.loads((ROOT / 'tests/plugin-memory-9644.json').read_text())
    verification = verify(memory, app / 'Contents/MacOS/VirtualDJ')
    a = Analysis(app)
    if memory['build'] != '18.0.9644' or hashlib.sha256(a.img.data).hexdigest() != verification['binary_sha256']:
        raise ValueError('this bounded model is for build 9644 only')
    # Locate through current literal call sites, not historical addresses.
    base_owners = {a.owner(pc) for vm in a.img.by_text['clickthrough'] for pc in a.img.xrefs[vm]}
    if len(base_owners) != 1:
        raise ValueError('base reader is ambiguous')
    base = base_owners.pop()
    calls = [c for c in literal_calls(a, base, 'x2') if c['name'] in ('size', 'pos')]
    if {c['name'] for c in calls} != {'size', 'pos'} or len({c['target'] for c in calls}) != 1:
        raise ValueError('conditional-child anchor changed')
    named = calls[0]['target']
    named_calls = a.calls(named)
    if len(named_calls) != 2:
        raise ValueError('conditional-child call structure changed')
    name_compare, predicate = [t for _, t in named_calls]
    # Shape reader is independently anchored by its literal shape getter.
    shape_owners = {a.owner(pc) for vm in a.img.by_text['outterradius'] for pc in a.img.xrefs[vm]}
    candidates = [fn for fn in shape_owners if any(c['name'] == 'shape' for c in literal_calls(a, fn))]
    if len(candidates) != 1:
        raise ValueError('shape reader is ambiguous')
    shape = candidates[0]
    shape_calls = a.calls(shape)
    if shape_calls[0][1] != predicate:
        raise ValueError('shape predicate changed')
    sibling = shape_calls[1][1]
    sibling_calls = a.calls(sibling)
    if len(sibling_calls) != 2 or sibling_calls[1][1] != predicate:
        raise ValueError('sibling selector changed')
    targets = {'named_child': named, 'matching_sibling': sibling, 'condition': predicate,
               'name_compare': name_compare, 'node_name_compare': sibling_calls[0][1], 'shape_reader': shape}
    routines = {}
    for name, fn in targets.items():
        body = b''.join(w.to_bytes(4, 'little') for _, w in a.words(fn))
        instructions = decoded(a, fn)
        if sum(i.size for i in instructions) != len(body):
            raise ValueError('incomplete decode')
        routines[name] = {'start': hex(fn), 'end': hex(fn+len(body)), 'sha256': hashlib.sha256(body).hexdigest(),
                          'instructions': [{'pc': hex(i.address), 'mnemonic': i.mnemonic, 'operands': i.op_str} for i in instructions]}
    return {'schema_version': 1, 'build': memory['build'], 'binary_sha256': verification['binary_sha256'],
            'evidence_tier': 2, 'anchor_calls': [{k: hex(v) if isinstance(v, int) else v for k, v in c.items()} for c in calls],
            'routines': routines,
            'models': {'named_child': {'role': 'conditional_child_node', 'node_register': 'x1', 'name_register': 'x2'},
                       'matching_sibling': {'role': 'matching_sibling_node', 'parent_register': 'x1', 'node_register': 'x2'}},
            'interpretation': [
                'named_child iterates pointers from node+0x30..+0x38, compares each child name to x2, checks the shared condition predicate, and returns the matching child or null.',
                'matching_sibling iterates that same parent child-vector, excludes the input child pointer, compares node-leading name strings and checks the shared predicate; it returns a same-name sibling or null.',
                'The predicate reads condition, parses/evaluates nonempty script, and defaults true for an empty condition. Script behavior is not proven by this structural analysis.',
                'Path models retain possible non-null ownership only. They do not establish branch feasibility, child identity, ordering contracts or runtime behavior.'],
            'scope': 'Manually interpreted current-build instructions; exact binary and routine guards are mandatory before applying these models.'}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path)
    p.add_argument('--check', action='store_true')
    args = p.parse_args()
    result = record()
    if args.check and result != json.loads(MANIFEST.read_text()):
        raise ValueError('conditional-node evidence drift')
    if args.output:
        with args.output.open('x') as f:
            json.dump(result, f, indent=2)
            f.write('\n')
    print(json.dumps({name: r['start'] for name, r in result['routines'].items()}))
