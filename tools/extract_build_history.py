#!/usr/bin/env python3
"""Compare unpacked historical installers without installing or launching them.

python3 tools/extract_build_history.py --root /tmp/vdj-history-20260906 \
    --output tests/build-history-2026-09-06
The root contains BUILD/vdj.pkg/Payload/*.app from pkgutil --expand-full.
Outputs binary evidence only, never runtime behavior or verb-store conclusions.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess

from extract_verb_table import build

BUILDS = ('5308', '7607', '9246', '9583')
# Each target lists its candidate mangled names; the first one present is captured.
# The boolean attribute parser changed signature across builds: 5308's
# ISkinObject::load calls the NS variant, the later builds the string_view one.
TARGETS = {
    'object-load': ('__ZN11ISkinObject4loadEP8CXMLNodeP6CImage',),
    'panel-constructor': ('__ZN10CSkinPanelC2EP8CXMLNodeP6CImageP11CSkinWindow',),
    'panel-children': ('__ZN10CSkinPanel12loadChildrenEP8CXMLNodeP6CImageP11CSkinWindow',),
    'bool-param': ('__ZNK8CXMLNode12getBoolParamENSt3__117basic_string_viewIcNS0_11char_traitsIcEEEEb',
                   '__ZNK8CXMLNode14getBoolParamNSEPKcib'),
}


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def routine(binary, symbol, low, high):
    # otool -p can continue beyond the requested function without a label.
    # Bound by the next distinct text-symbol address, not printed labels.
    process = subprocess.Popen(
        ['otool', '-arch', 'x86_64', '-tV', '-p', symbol, str(binary)],
        stdout=subprocess.PIPE, text=True,
    )
    lines = []
    bounded = False
    try:
        for line in process.stdout:
            match = re.match(r'^([0-9a-f]{16})\s', line)
            if not match:
                continue
            address = int(match[1], 16)
            if address >= high:
                bounded = True
                break
            if address >= low:
                lines.append(line)
    finally:
        if bounded:
            process.terminate()
        process.stdout.close()
        code = process.wait()
    if not lines or (not bounded and code != 0):
        raise RuntimeError(f'Could not disassemble {symbol}: {code}')
    return symbol + ':\n' + ''.join(lines)


def capture_routine(binary, symbols, key, name, candidates, output):
    symbol = next((c for c in candidates if c in symbols), None)
    if symbol is None:
        return {'status': 'named symbol unavailable'}
    low = symbols[symbol]
    high = min(a for a in symbols.values() if a > low)
    body = routine(binary, symbol, low, high)
    filename = f'{key}-{name}.asm'
    (output / filename).write_text(body)
    return {
        'symbol': symbol, 'start': hex(low), 'end_exclusive': hex(high),
        'file': filename,
        'literals': sorted(set(re.findall(r'literal pool for: "([^"]*)"', body))),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = {'extracted': datetime.date.today().isoformat(), 'evidence': 'binary structure; no runtime tests',
              'builds': {}, 'transitions': []}
    previous = None
    for key in BUILDS:
        apps = list((args.root / key).glob('vdj.pkg/Payload/*.app'))
        if len(apps) != 1:
            raise RuntimeError(f'Expected one app for {key}, found {len(apps)}')
        binary = apps[0] / 'Contents/MacOS/VirtualDJ'
        arches = subprocess.check_output(['lipo', '-archs', str(binary)], text=True).split()
        table = build(str(binary), 0x01000007)
        write_json(args.output / f'{key}-verbs.json', table)
        with binary.open('rb') as stream:
            digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        entry = {'identity': table['summary'], 'architectures': arches,
                 'sha256': digest,
                 'routines': {}}
        if 'arm64' in arches:
            arm = build(str(binary))
            normalize = lambda data: {n: (r['id'], r['flags']) for n, r in data['verbs'].items()}
            entry['arm64_name_id_flags_equal'] = normalize(arm) == normalize(table)
            entry['arm64_summary'] = arm['summary']
            if not entry['arm64_name_id_flags_equal']:
                raise RuntimeError(f'Architecture tables differ: {key}')
        raw = subprocess.check_output(['nm', '-arch', 'x86_64', str(binary)], text=True)
        entry['nm_lines_x86_64'] = len(raw.splitlines())
        symbols = {s: int(a, 16) for a, s in re.findall(
            r'^([0-9a-f]{16}) [tT] (\S+)$', raw, re.M)}
        for name, candidates in TARGETS.items():
            entry['routines'][name] = capture_routine(binary, symbols, key, name, candidates, args.output)
        report['builds'][key] = entry
        if previous:
            old_key, old = previous
            old, new = old['verbs'], table['verbs']
            common = old.keys() & new.keys()
            report['transitions'].append({
                'from': old_key, 'to': key,
                'added': sorted(new.keys() - old.keys()),
                'removed': sorted(old.keys() - new.keys()),
                'flag_changes': {n: [old[n]['flags'], new[n]['flags']] for n in sorted(common)
                                 if old[n]['flags'] != new[n]['flags']},
                'alias_peers_after_flag_change': {
                    n: sorted(p for p, rec in new.items() if rec['id'] == new[n]['id'])
                    for n in sorted(common) if old[n]['flags'] != new[n]['flags']
                },
            })
        previous = key, table
        print(key, table['summary']['build'], 'extracted', flush=True)
    write_json(args.output / 'summary.json', report)


if __name__ == '__main__':
    main()
