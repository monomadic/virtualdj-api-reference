#!/usr/bin/env python3
"""Compare button action binding with text action output; no buttons are clicked."""
from pathlib import Path
import sys
from xml.sax.saxutils import quoteattr

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'element-validity-probe'))
import probe as runner

runner.HERE = HERE
runner.NAME = 'ZZ Script Validity 9644'
runner.INSTALL = Path.home() / 'Library/Application Support/VirtualDJ/Skins' / runner.NAME
runner.STATE = Path('/tmp/vdj-script-validity-state.json')
runner.JOURNAL = HERE / 'run-9644.jsonl'
CASES = [
    ('button-baseline', 'button', None),
    ('button-nothing', 'button', 'nothing'),
    ('button-invalid-alpha', 'button', 'zzinvalidalpha'),
    ('button-invalid-beta', 'button', 'zzinvalidbeta'),
    ('text-literal', 'text', "get_text 'VALID TEXT'"),
    ('text-valid-empty', 'text', "get_text ''"),
    ('text-invalid-alpha', 'text', 'zzinvalidalpha'),
    ('text-invalid-beta', 'text', 'zzinvalidbeta'),
]


def fixture(round_number):
    rows = CASES if round_number == 1 else list(reversed(CASES))
    parts = [f'<skin name="{runner.NAME}" version="8" width="1200" height="720">',
             runner.label(f'SCRIPT CANARY - ROUND {round_number}', 25, 12)]
    for n, (name, kind, script) in enumerate(rows):
        y = 100 + n * 68
        parts.append(runner.label(name, 25, y))
        attr = '' if script is None else 'action=' + quoteattr(script)
        if kind == 'button':
            parts.append(f'<button x="450" y="{y}" width="220" height="32" {attr}><up color="#00CCFF"/></button>')
        else:
            parts.append(f'<textzone x="450" y="{y}" width="500" height="32"><text font="Arial" size="20" color="#00CCFF" {attr}/></textzone>')
    parts.append(runner.label('END CONTROL', 25, 665))
    parts.append('</skin>')
    return ('\n'.join(parts) + '\n').encode()


runner.fixture = fixture
if __name__ == '__main__':
    runner.main()
