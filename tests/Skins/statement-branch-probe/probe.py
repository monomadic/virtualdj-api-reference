#!/usr/bin/env python3
"""Visible button calibration for the exact debug branch probe."""
from pathlib import Path
import sys
from xml.sax.saxutils import quoteattr

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'element-validity-probe'))
import probe as runner
runner.HERE = HERE
runner.NAME = 'ZZ Statement Branch 9644'
runner.INSTALL = Path.home() / 'Library/Application Support/VirtualDJ/Skins' / runner.NAME
runner.STATE = Path('/tmp/vdj-statement-branch-state.json')
runner.JOURNAL = HERE / 'run-9644.jsonl'
CASES = [
    ('direct debug', 'debug 42'),
    ('valid false exact', "get_text 'hi' ? nothing : debug"),
    ('typo exact', "gettext 'hi' ? nothing : debug"),
    ('unknown alpha exact', 'zzinvalidalpha ? nothing : debug'),
    ('unknown beta exact', 'zzinvalidbeta ? nothing : debug'),
    ('known true tagged', "true ? debug 'TRUE' : debug 'FALSE'"),
    ('valid false tagged', "get_text 'hi' ? debug 'TRUE' : debug 'FALSE'"),
    ('typo tagged', "gettext 'hi' ? debug 'TRUE' : debug 'FALSE'"),
]


def fixture(round_number):
    rows = CASES if round_number == 1 else list(reversed(CASES))
    parts = [f'<skin name="{runner.NAME}" version="8" width="1200" height="720">',
             runner.label(f'STATEMENT BRANCH - ROUND {round_number}', 25, 12)]
    for n, (name, script) in enumerate(rows):
        y = 100 + n * 68
        parts.append(runner.label(name, 25, y))
        parts.append(f'<button action={quoteattr(script)} x="530" y="{y}" width="240" height="32"><up color="#00CCFF"/></button>')
    parts.append(runner.label('END CONTROL', 25, 665))
    parts.append('</skin>')
    return ('\n'.join(parts) + '\n').encode()


runner.fixture = fixture
if __name__ == '__main__':
    runner.main()
