#!/usr/bin/env python3
"""Capture named historical and current clickthrough press/release paths."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from binary_source import CURRENT, build, sources
from capture_clickthrough_dispatch import function_record
from extract_action_vtables import demangled, symbol_maps
from extract_skin_classes import Analysis, decoded

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'tests/clickthrough-release-9644.json'
NAMES = (
    'CSkinEngine::onMouseDown(CSkinWindow*, int, int, int, int, int)',
    'CSkinEngine::onMouseUp(CSkinWindow*, int, int, int, int, int)',
    'CSkinButton::onMouseUp(int, int, int)',
)


def select_current(old: Analysis, current: Analysis, address: int) -> tuple[int, str]:
    old_words = old.words(address)
    old_insns = decoded(old, address)
    if len(old_insns) < 14:
        raise ValueError('historical function too short for matching')
    if len(old_insns) < 40:
        fingerprint = old.fingerprint(address)
        matches = [fn for fn in current.starts if current.fingerprint(fn) == fingerprint]
        method = 'unique normalized whole-function fingerprint'
    else:
        prefix = [(insn.mnemonic, insn.op_str) for insn in old_insns[:14]]
        matches = [fn for fn in current.starts
                   if abs(len(current.words(fn)) - len(old_words)) <= 25
                   and [(insn.mnemonic, insn.op_str) for insn in decoded(current, fn)[:14]] == prefix]
        method = 'unique 14-instruction prologue plus bounded function length'
    if len(matches) != 1:
        raise ValueError(f'current counterpart not unique for {address:#x}: {matches}')
    return matches[0], method


def capture(historical_app: Path, current_app: Path) -> dict:
    historical_build, current_build = build(historical_app), build(current_app)
    if (historical_build, current_build) != ('18.0.9246', '18.0.9644'):
        raise ValueError(f'capture expects builds 18.0.9246 and 18.0.9644; got {historical_build} and {current_build}')
    old = Analysis(historical_app)
    current = Analysis(current_app)
    symbols, _ = symbol_maps(demangled(historical_app / 'Contents/MacOS/VirtualDJ', 'arm64'))
    methods = {}
    for name in NAMES:
        matches = [address for address, symbol in symbols.items() if symbol == name]
        if len(matches) != 1:
            raise ValueError(f'historical symbol not unique: {name}: {matches}')
        old_address = matches[0]
        current_address, method = select_current(old, current, old_address)
        methods[name] = {'match_method': method,
                         'historical': function_record(old, old_address),
                         'current': function_record(current, current_address)}
    return {
        'historical_source': {'app': str(historical_app),
                              'binary_sha256': hashlib.sha256((historical_app / 'Contents/MacOS/VirtualDJ').read_bytes()).hexdigest(),
                              'build': historical_build, 'arch': 'arm64'},
        'current_source': {'app': str(current_app),
                           'binary_sha256': hashlib.sha256((current_app / 'Contents/MacOS/VirtualDJ').read_bytes()).hexdigest(),
                           'build': current_build, 'arch': 'arm64'},
        'evidence_tier': 2,
        'methods': methods,
        'limitations': [
            'Current method identities are cross-build structural matches, not current symbols.',
            'The ordinary pointer path and the separate touch path must not be conflated.',
            'Disassembly does not establish live release or drag behavior.',
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--historical-app', type=Path)
    parser.add_argument('--current-app', type=Path, default=CURRENT)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    named = [row for row in sources() if row['arm64_skin_symbols']]
    if not named and args.historical_app is None:
        parser.error('no symbol-rich historical bundle found')
    historical = args.historical_app or Path(max(named, key=lambda row: tuple(map(int, row['build'].split('.'))))['app'])
    result = capture(historical, args.current_app)
    if args.check:
        if result != json.loads(args.output.read_text()):
            raise SystemExit(f'capture differs from {args.output}')
        print(f'clickthrough release capture matches {args.output}')
    else:
        with args.output.open('x') as stream:
            json.dump(result, stream, indent=2)
            stream.write('\n')
        print(args.output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
