#!/usr/bin/env python3
"""Unknown attribute before/after a valid color or visibility attribute."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'element-validity-probe'))
import probe as runner

runner.HERE = HERE
runner.NAME = 'ZZ Attribute Order 9644'
runner.INSTALL = Path.home() / 'Library/Application Support/VirtualDJ/Skins' / runner.NAME
runner.STATE = Path('/tmp/vdj-attribute-order-state.json')
runner.JOURNAL = HERE / 'run-9644.jsonl'
CASES = [
    ('color baseline', 'color', 'color="#00FF00"'),
    ('alpha then color', 'color', 'zzinvalidalpha="#FF0000" color="#00FF00"'),
    ('color then alpha', 'color', 'color="#00FF00" zzinvalidalpha="#FF0000"'),
    ('beta then color', 'color', 'zzinvalidbeta="#FF0000" color="#00FF00"'),
    ('color then beta', 'color', 'color="#00FF00" zzinvalidbeta="#FF0000"'),
    ('visibility baseline', 'visibility', 'visibility="off"'),
    ('alpha then visibility', 'visibility', 'zzinvalidalpha="on" visibility="off"'),
    ('visibility then alpha', 'visibility', 'visibility="off" zzinvalidalpha="on"'),
    ('beta then visibility', 'visibility', 'zzinvalidbeta="on" visibility="off"'),
    ('visibility then beta', 'visibility', 'visibility="off" zzinvalidbeta="on"'),
]


def fixture(round_number):
    rows = CASES if round_number == 1 else list(reversed(CASES))
    parts = [f'<skin name="{runner.NAME}" version="8" width="1200" height="720">',
             runner.label(f'ATTRIBUTE ORDER - ROUND {round_number}', 25, 12)]
    for n, (name, kind, attrs) in enumerate(rows):
        y = 75 + n * 56
        parts.append(runner.label(name, 25, y))
        if kind == 'color':
            parts.append(f'<textzone x="530" y="{y}" width="450" height="32"><text {attrs} font="Arial" size="20" format="GREEN R{round_number} ROW {n+1}"/></textzone>')
        else:
            parts.append(f'<button {attrs} x="530" y="{y}" width="220" height="32"><up color="#00CCFF"/></button>')
    parts.append(runner.label('VISIBLE BUTTON CONTROL', 25, 665))
    parts.append('<button x="530" y="665" width="220" height="32"><up color="#00CCFF"/></button>')
    parts.append('</skin>')
    return ('\n'.join(parts) + '\n').encode()


runner.fixture = fixture
if __name__ == '__main__':
    runner.main()
