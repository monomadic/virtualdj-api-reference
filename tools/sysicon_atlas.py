#!/usr/bin/env python3
"""Join the dated wiki atlas with captured sysicon evidence. No live app calls.

Default: all cells; --cell H6, --unnamed, --format json for focused queries.
--extract captures the internal atlas consumers from an installed binary.
"""
import argparse
import hashlib
import json
import plistlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'tests/sysicon-atlas-wiki-2026-09-16.json'
CAPTURE = ROOT / 'tests/sysicon-atlas-consumers-9598'


def extract(app, output):
    from extract_skin_classes import Analysis, decoded
    from extract_action_contracts import rtti_graph
    a = Analysis(app)

    def anchor(*strings):
        groups = [{a.owner(pc) for va in a.img.by_text.get(s, [])
                   for pc in a.img.xrefs.get(va, [])} for s in strings]
        found = set.intersection(*groups)
        if len(found) != 1:
            raise ValueError(f'Ambiguous or missing anchors: {strings}')
        return found.pop()

    loader = anchor('Error in skin icon definition! (Icons file too small to fit all icons)\n')
    factory = anchor('customicons')
    if loader not in {target for _, target in a.calls(factory)}:
        raise ValueError('customicons factory no longer calls atlas loader')
    graph = rtti_graph(a.img.data, prefixes=('IFolder',))
    folder = graph['IFolder']
    # Slot is calibrated against the symbol-bearing b9246 IFolder::getIcon(bool).
    # Capture raw instructions; do not assume an unchanged contract on other builds.
    functions = {
        'atlas-loader': loader,
        'customicons-reader': factory,
        'file-icon-selector': anchor('search://', '.vdjsample', '.vdjedit', 'clouddrive://upload/'),
        'folder-icon-slot-5': folder['slots'][5],
    }
    existing = output / 'manifest.json'
    if existing.exists() and json.loads(existing.read_text())['binary_sha256'] != hashlib.sha256(a.img.data).hexdigest():
        raise ValueError('Preserve the old capture: choose a new --output for a different binary')
    output.mkdir(parents=True, exist_ok=True)
    captures = {}
    for label, fn in functions.items():
        refs = dict(a.refs.get(fn, []))
        body = '\n'.join(f'{i.address:#x}: {i.mnemonic} {i.op_str}' +
                         (f' ; {refs[i.address]!r}' if i.address in refs else '')
                         for i in decoded(a, fn)) + '\n'
        (output / f'{label}.asm').write_text(body)
        captures[label] = {'address': hex(fn), 'file': f'{label}.asm',
                           'sha256': hashlib.sha256(body.encode()).hexdigest()}
    data = {
        'build': plistlib.loads((app / 'Contents/Info.plist').read_bytes())['CFBundleVersion'],
        'architecture': 'arm64', 'evidence_tier': 2,
        'binary_sha256': hashlib.sha256(a.img.data).hexdigest(),
        'scope': 'Static atlas consumers; no live behavior or new sysicon acceptance established',
        'captures': captures,
        'folder_rtti': {k: folder[k] for k in ('typeinfo', 'vtable', 'slots')},
        'limitations': [
            'The file selector appends numeric identifiers, not sysicon strings.',
            'The folder slot uses a stored index; assignments to that field are not enumerated.',
            'Historical slot naming is a locator, not an assertion that every build shares the contract.',
            'Absence of a key from this inventory does not prove that no key exists.'],
    }
    (output / 'manifest.json').write_text(json.dumps(data, indent=2) + '\n')
    return data


def inventory():
    source = json.loads(SNAPSHOT.read_text())
    live_path = ROOT / 'tests/Skins/SysiconAtlasProbe/results.json'
    live = json.loads(live_path.read_text())
    resolver_path = ROOT / 'tests/sysicon-resolver-9598/manifest.json'
    resolver = json.loads(resolver_path.read_text())
    if live['build'] != resolver['build']:
        raise ValueError('Live and resolver builds differ; join requires review')
    rows = []
    # The vendor page labels the last physical row K, skipping J. Preserve that convention.
    letters = 'ABCDEFGHIK'
    for original in source['rows']:
        label = original['row_col']
        match = re.fullmatch(r'([A-IK])\s*(\d+)(?: to ([A-IK])\s*(\d+))?', label)
        if not match or (match[3] and match[3] != match[1]):
            raise ValueError(f'Unexpected wiki cell range: {label}')
        for col in range(int(match[2]), int(match[4] or match[2]) + 1):
            index = letters.index(match[1]) * 16 + col - 1
            if not 1 <= col <= 16:
                raise ValueError(f'Invalid column: {label}')
            row = {'cell': f'{match[1]}{col}', 'index': index,
                   'description': original['description'],
                   'wiki_sysicon_action': original['sysicon_action'],
                   'wiki_row': label, 'tested_keys': [], 'binary_candidates': []}
            for result in live['rows']:
                if result.get('index') == index and result['verdict'] == 'rendered-matching-atlas':
                    row['tested_keys'].append({'key': result['key'], 'build': live['build'],
                        'evidence_tier': 1, 'evidence': str(live_path.relative_to(ROOT))})
            rows.append(row)
    if len({r['index'] for r in rows}) != len(rows):
        raise ValueError('Overlapping wiki rows')
    # Manually interpreted branch records, tied to the checked-in assembly. These
    # are not generated by a string-pool guess and are deliberately not live keys.
    candidates = {
        84: {'form': 'context_menu', 'match': 'exact', 'role': 'state graphic at +0x260',
             'comparison_pc': '0x1004cf9f4', 'assignment_pc': '0x1004cfa60'},
        85: {'form': 'context_menu', 'match': 'exact', 'role': 'state graphic at +0x280',
             'comparison_pc': '0x1004cf9f4', 'assignment_pc': '0x1004cfa6c'},
        140: {'form': 'stop_button', 'match': 'exact',
              'role': 'primary icon at +0x2a8 when the option read at 0x1004d0380 is zero; otherwise I14',
              'comparison_pc': '0x1004cfc20', 'assignment_pc': '0x1004d0614'},
        117: {'form': 'sideview "', 'match': 'prefix', 'role': 'primary icon at +0x2a8',
              'comparison_pc': '0x1004d0500', 'assignment_pc': '0x1004d0698'},
        66: {'form': 'effect_active', 'match': 'exact', 'role': 'state graphic at +0x260',
             'comparison_pc': '0x1004d06d0', 'assignment_pc': '0x1004d0820'},
        67: {'form': 'effect_active', 'match': 'exact', 'role': 'state graphic at +0x270',
             'comparison_pc': '0x1004d06d0', 'assignment_pc': '0x1004d082c'},
    }
    if resolver['binary_sha256'] != '94f45962f8149410657589181f1c391287d0560919cbad623e5b920b4bf6af38':
        raise ValueError('Static branch annotations need review for changed binary')
    assembly = (resolver_path.parent / 'resolver.asm').read_text()
    if hashlib.sha256(assembly.encode()).hexdigest() != resolver['captures']['resolver']['sha256']:
        raise ValueError('Resolver assembly hash does not match its manifest')
    for index, candidate in candidates.items():
        line = next((line for line in assembly.splitlines()
                     if line.startswith(candidate['assignment_pc'] + ':')), '')
        if not re.search(rf'mov w[89], #{index * 160:#x}$', line):
            raise ValueError(f'Candidate offset changed at {candidate["assignment_pc"]}')
    for row in rows:
        if row['index'] in candidates:
            row['binary_candidates'].append({**candidates[row['index']],
                'build': resolver['build'], 'evidence_tier': 2,
                'evidence': 'tests/sysicon-resolver-9598/resolver.asm'})
        row['key_status'] = ('live-tested' if row['tested_keys'] else
                             'binary-candidate' if row['binary_candidates'] else
                             'wiki-listed' if row['wiki_sysicon_action'] != 'N/A' else 'unknown')
    return {'source': str(SNAPSHOT.relative_to(ROOT)), 'source_url': source['source_url'],
            'retrieved_date': source['retrieved_date'], 'build': resolver['build'],
            'limitations': 'Unknown means no key established here, not proof of no key. State graphics are not primary-icon aliases.',
            'rows': rows}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cell', type=str.upper)
    p.add_argument('--unnamed', action='store_true', help='Wiki N/A entries, including subsequently recovered keys')
    p.add_argument('--format', choices=('text', 'json'), default='text')
    p.add_argument('--extract', action='store_true')
    p.add_argument('--app', type=Path, default=Path('/Applications/VirtualDJ.app'))
    p.add_argument('--output', type=Path, default=CAPTURE)
    args = p.parse_args()
    if args.extract:
        print(json.dumps(extract(args.app, args.output), indent=2))
        return
    data = inventory()
    data['rows'] = [r for r in data['rows'] if (not args.cell or r['cell'] == args.cell)
                    and (not args.unnamed or r['wiki_sysicon_action'] == 'N/A')]
    if args.cell and not data['rows']:
        p.error('No matching cell; the wiki skips J and ends at K9')
    if args.format == 'json':
        print(json.dumps(data, indent=2))
    else:
        print(f"Wiki snapshot {data['retrieved_date']}; binary/live evidence build {data['build']}")
        print(data['limitations'])
        for row in data['rows']:
            keys = ', '.join(repr(k['key']) for k in row['tested_keys'])
            leads = '; '.join(f"{c['form']!r} ({c['match']}, {c['role']})" for c in row['binary_candidates'])
            print(f"{row['cell']:4} {row['key_status']:16} {row['description']} | wiki={row['wiki_sysicon_action']!r} | tested={keys or '-'} | candidate={leads or '-'}")


if __name__ == '__main__':
    main()
