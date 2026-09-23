#!/usr/bin/env python3
"""Test valid and unknown sibling elements inside known containers."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'element-validity-probe'))
import probe as runner

runner.HERE = HERE
runner.NAME = 'ZZ Sibling Validity 9644'
runner.INSTALL = Path.home() / 'Library/Application Support/VirtualDJ/Skins' / runner.NAME
runner.STATE = Path('/tmp/vdj-sibling-validity-state.json')
runner.JOURNAL = HERE / 'run-9644.jsonl'
CASES = [
    ('panel baseline', 'panel', None, False),
    ('panel valid then alpha', 'panel', 'zzinvalidalpha', False),
    ('panel alpha then valid', 'panel', 'zzinvalidalpha', True),
    ('panel valid then beta', 'panel', 'zzinvalidbeta', False),
    ('panel beta then valid', 'panel', 'zzinvalidbeta', True),
    ('group alpha then valid', 'group', 'zzinvalidalpha', True),
    ('group valid then beta', 'group', 'zzinvalidbeta', False),
]


def fixture(round_number):
    rows = CASES if round_number == 1 else list(reversed(CASES))
    parts = [f'<skin name="{runner.NAME}" version="8" width="1200" height="720">',
             runner.label(f'SIBLING CANARY - ROUND {round_number}', 25, 12)]
    for n, (name, container, unknown, first) in enumerate(rows):
        y = 100 + n * 75
        parts.append(runner.label(name, 25, y))
        valid = runner.label(f'VALID R{round_number} ROW {n+1}', 530, y, '#00FFFF')
        invalid = f'<{unknown}/>' if unknown else ''
        children = invalid + valid if first else valid + invalid
        parts.append(f'<{container} x="0" y="0" width="1200" height="720">{children}</{container}>')
    parts.append(runner.label('END CONTROL', 25, 665))
    parts.append('</skin>')
    return ('\n'.join(parts) + '\n').encode()


runner.fixture = fixture
if __name__ == '__main__':
    runner.main()
