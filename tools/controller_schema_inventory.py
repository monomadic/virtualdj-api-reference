#!/usr/bin/env python3
"""Inventory decoded controllers ZIP XML without promoting shipped syntax to behavior.

The baseline is the explicit vocabulary in Mapper XML.md's device-definition
summary, not a complete official schema or a parser acceptance allowlist.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

BASELINE_SOURCE = 'docs/Mapper XML.md, Device definitions / Root device MIDI and HID summaries'
ELEMENTS = set('device audio button toggle slider jog fulljog encoder fullencoder touchstrip sysexin led color bar digit text init exit ledsysex sysex page'.split())
# Global lexical comparison deliberately avoids claiming which element accepts an
# attribute. Only exact spellings explicitly printed in the summary are included.
ATTRIBUTES = set('name author description version type vid pid decks padColumns padRows padSides input output mixer asio note deck channel ccmsb cclsb sendsysex sysexid drivername singledeck motor platform cc value off inverted autoled nbdecks pitch min max zero zerorange ghost nozero full mask noteoff ccoff default values encoding reportsize outreportsize bit byte word dword nbbits size endian'.split())


def display_path(path):
    """Keep generated reports checkout-independent for repository examples."""
    try:
        return path.resolve().relative_to(Path(__file__).resolve().parents[1]).as_posix()
    except ValueError:
        return path.as_posix()


def inventory(zip_path, mapper_dir):
    paths = {}
    roots = Counter()
    definitions = defaultdict(list)
    mappers = defaultdict(list)
    types = Counter()
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            if member.is_dir():
                continue
            root = ET.fromstring(archive.read(member))
            roots[root.tag] += 1
            if root.tag == 'device':
                types[root.get('type', '')] += 1
                definitions[root.get('name', '')].append((member.filename, root))
            elif root.tag == 'mapper':
                mappers[root.get('device', '')].append((member.filename, root))

            def visit(element, parent=''):
                path = parent + '/' + element.tag
                row = paths.setdefault(path, {'count': 0, 'files': set(), 'attributes': {}})
                row['count'] += 1
                row['files'].add(member.filename)
                for key in element.attrib:
                    attr = row['attributes'].setdefault(key, {'count': 0, 'files': set()})
                    attr['count'] += 1
                    attr['files'].add(member.filename)
                for child in element:
                    visit(child, path)
            visit(root)
    path_rows = []
    for path, row in sorted(paths.items()):
        path_rows.append({
            'path': path, 'count': row['count'], 'file_count': len(row['files']),
            'example_files': sorted(row['files'])[:3],
            'element_absent_from_local_summary': path.startswith('/device') and path.rsplit('/', 1)[-1] not in ELEMENTS,
            'attributes': [{
                'name': key, 'count': val['count'], 'file_count': len(val['files']),
                'example_files': sorted(val['files'])[:3],
                'spelling_absent_from_local_summary': path.startswith('/device') and key not in ATTRIBUTES,
            } for key, val in sorted(row['attributes'].items())],
        })
    comparisons = []
    for path in sorted(mapper_dir.rglob('*.xml')):
        root = ET.parse(path).getroot()
        device = root.get('device', '')
        keys = {e.get('value') for e in root.findall('map') if e.get('value')}
        bundled_keys = {e.get('value') for _, tree in mappers[device] for e in tree.findall('map') if e.get('value')}
        controls = {e.get('name') for _, tree in definitions[device] for e in tree.iter() if e is not tree and e.get('name')}
        comparisons.append({
            'path': display_path(path), 'device': device,
            'provenance': 'personal/quarantined; syntax comparison only' if 'Quarantine' in path.parts else 'local factory mapping or export; see examples/Mappers/README.md',
            'root': root.tag, 'root_attributes': sorted(root.attrib),
            'map_count': len(root.findall('map')), 'unique_map_values': len(keys),
            'bundled_mapper_files': sorted(n for n, _ in mappers[device]),
            'bundled_definition_files': sorted(n for n, _ in definitions[device]),
            'keyboard_definition_not_expected': device == 'KEYBOARD',
            'values_absent_from_bundled_mapper': sorted(keys - bundled_keys),
            'values_absent_from_definition_names': None if device == 'KEYBOARD' else sorted(keys - controls),
            'comparison_limit': 'Exact lexical match only. Lifecycle, shifted, virtual and generated controls can be valid without a literal definition name; absence does not prove invalidity. Action text is not used as evidence.',
        })
    return {
        'schema_version': 1, 'source_zip_sha256': hashlib.sha256(zip_path.read_bytes()).hexdigest(),
        'evidence_tier': 'Tier 2: shipped XML vocabulary; no runtime acceptance or behavior inferred',
        'baseline': {'source': BASELINE_SOURCE, 'scope': 'Explicit vocabulary of local prose summary, not full official schema; case-sensitive', 'elements': sorted(ELEMENTS), 'attributes': sorted(ATTRIBUTES)},
        'root_counts': dict(sorted(roots.items())), 'device_type_counts': dict(sorted(types.items())),
        'paths': path_rows, 'local_mapper_comparisons': comparisons,
    }


VENDOR = Path(__file__).resolve().parents[1] / 'vendor/controllers'


def build_key(directory):
    """`18.0.9598-r2241` -> (18, 0, 9598, 2241), for newest-first ordering."""
    return tuple(int(n) for n in directory.name.replace('-r', '.').split('.') if n.isdigit())


def device_controls(members, bundle_version):
    """Control names in the device definition, from the decoded vendor tree.

    Prefers the manifest's build; otherwise the newest build extracted. The
    names are what a <map value=""> refers to. Tier 2: shipped vocabulary.
    """
    definitions = [m for m in members if m['root'] == 'device']
    if not definitions:
        return {'error': 'no device definition among the matched bundled members'}
    if not VENDOR.is_dir():
        return {'error': 'vendor/controllers/ is not extracted — run `just controllers-vendor`'}
    builds = sorted((d for d in VENDOR.iterdir() if d.is_dir()), key=build_key, reverse=True)
    builds.sort(key=lambda d: not d.name.startswith(bundle_version))
    out = []
    for definition in definitions:
        found = next((f for d in builds for f in sorted(d.glob('block-*/' + definition['name']))), None)
        if found is None:
            out.append({'definition': definition['name'], 'error': 'not in any extracted build'})
            continue
        root = ET.parse(found).getroot()
        controls = defaultdict(set)
        for element in root.iter():
            if element is not root and element.get('name') and element.tag in ELEMENTS:
                controls[element.tag].add(element.get('name'))
        out.append({
            'definition': definition['name'],
            'build': found.parts[-3],
            'device': dict(root.attrib),
            'controls': {tag: sorted(names) for tag, names in sorted(controls.items())},
            'scope': 'Names declared by the definition. Lifecycle (ONINIT/ONEXIT), SHIFT_ and '
                     'generated controls can be valid in a mapper without appearing here.',
        })
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('zip', type=Path, nargs='?', help='Decoded ZIP to regenerate the complete inventory')
    parser.add_argument('--read', type=Path, default=Path(__file__).resolve().parents[1] / 'tests/controller-schema-inventory.json', help='Saved inventory for offline queries')
    parser.add_argument('--path', help='XML path: exact match preferred, otherwise substring')
    parser.add_argument('--device', help='Built-in device identifier (case-insensitive; exact preferred, otherwise substring)')
    parser.add_argument('--manifest', type=Path, default=None, help='Decoded archive manifest for built-in device lookup (default: the installed build\'s under tests/controllers-manifests/, else the newest)')
    parser.add_argument('--controls', action='store_true', help='With --device: list the control names its definition declares')
    parser.add_argument('--match', help='With --controls: keep control names containing this text (case-insensitive)')
    parser.add_argument('--mappers', type=Path, default=Path(__file__).resolve().parents[1] / 'examples/Mappers')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.manifest is None:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from controller_archives import find_manifest, list_manifests, DEFAULT_APP
        rows = list_manifests()
        args.manifest = find_manifest(app=DEFAULT_APP) or (rows[-1]['path'] if rows else None)
        if args.manifest is None:
            parser.error('no manifest under tests/controllers-manifests/ — run `just controllers-vendor`')
    data = inventory(args.zip, args.mappers) if args.zip else json.loads(args.read.read_text(encoding='utf-8'))
    if args.path or args.device:
        result_data = {'source_zip_sha256': data['source_zip_sha256'], 'evidence_tier': data['evidence_tier']}
        if args.path:
            exact = [row for row in data['paths'] if row['path'] == args.path]
            result_data['paths'] = exact or [row for row in data['paths'] if args.path in row['path']]
        if args.device:
            result_data['local_mapper_comparisons'] = [row for row in data['local_mapper_comparisons'] if row['device'].casefold() == args.device.casefold()]
            manifest = json.loads(args.manifest.read_text(encoding='utf-8'))
            candidates = []
            for block in manifest['blocks']:
                for member in block['members']:
                    key = {'device': 'name', 'mapper': 'device'}.get(member['root'])
                    if key:
                        identifier = member['attributes'].get(key, '')
                        if args.device.casefold() in identifier.casefold():
                            candidates.append({**member, 'block_offset': block['offset'], 'block_revision': block['revision'], 'matched_identifier': identifier})
            exact = [row for row in candidates if row['matched_identifier'].casefold() == args.device.casefold()]
            result_data['bundled_members'] = exact or candidates
            result_data['manifest_source'] = {key: manifest[key] for key in ('source', 'bundle_version', 'source_sha256', 'app_binary_sha256')}
            result_data['manifest_matches_inventory_zip'] = any(block['zip_sha256'] == data['source_zip_sha256'] for block in manifest['blocks'])
            if args.controls:
                listed = device_controls(result_data['bundled_members'], manifest['bundle_version'])
                if args.match and isinstance(listed, list):
                    for row in listed:
                        row['controls'] = {tag: kept for tag, names in row.get('controls', {}).items()
                                           if (kept := [n for n in names if args.match.casefold() in n.casefold()])}
                # The device-level answer replaces the comparison detail.
                result_data = {'evidence_tier': data['evidence_tier'], 'device_controls': listed}
    elif args.zip:
        result_data = data
    else:
        result_data = {
            'source_zip_sha256': data['source_zip_sha256'],
            'evidence_tier': data['evidence_tier'],
            'baseline': {'source': data['baseline']['source'], 'scope': data['baseline']['scope']},
            'root_counts': data['root_counts'],
            'device_type_counts': data['device_type_counts'],
            'inventory_path_count': len(data['paths']),
            'local_mapper_count': len(data['local_mapper_comparisons']),
            'local_mapper_devices': sorted({row['device'] for row in data['local_mapper_comparisons']}),
            'queries': ['--path /device/settings', '--path packet', '--device DDJGRV6'],
        }
    result = json.dumps(result_data, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.write_text(result, encoding='utf-8')
    else:
        print(result, end='')


if __name__ == '__main__':
    main()
