#!/usr/bin/env python3
"""Reuse the guarded nesting runner for unknown attributes versus invalid values."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'element-validity-probe'))
import probe as runner

runner.HERE = HERE
runner.NAME = 'ZZ Attribute Validity 9644'
runner.INSTALL = Path.home() / 'Library/Application Support/VirtualDJ/Skins' / runner.NAME
runner.STATE = Path('/tmp/vdj-attribute-validity-state.json')
runner.JOURNAL = HERE / 'run-9644.jsonl'
CASES = [
    ('baseline', ''),
    ('unknown-alpha', 'zzinvalidalpha="off"'),
    ('unknown-beta', 'zzinvalidbeta="0"'),
    ('visibility-on', 'visibility="on"'),
    ('visibility-off', 'visibility="off"'),
    ('misspelled-visibility', 'zzvisibility="off"'),
    ('invalid-value-alpha', 'visibility="zzinvalidalpha"'),
    ('invalid-value-beta', 'visibility="zzinvalidbeta"'),
]


def fixture(round_number):
    rows = CASES if round_number == 1 else list(reversed(CASES))
    parts = [f'<skin name="{runner.NAME}" version="8" width="1200" height="720">',
             runner.label(f'ATTRIBUTE CANARY - ROUND {round_number}', 25, 12),
             runner.label('Case', 25, 52), runner.label('Button drawing', 450, 52)]
    for n, (name, attrs) in enumerate(rows):
        y = 100 + n * 68
        parts.append(runner.label(name, 25, y))
        parts.append(f'<button x="450" y="{y}" width="220" height="32" {attrs}><up color="#00CCFF"/></button>')
    parts.append(runner.label('END CONTROL', 25, 665))
    parts.append('</skin>')
    return ('\n'.join(parts) + '\n').encode()


runner.fixture = fixture
if __name__ == '__main__':
    runner.main()
