#!/usr/bin/env python3
"""Controlled desktop nesting canary. Explicit install/load/restore steps; no media actions."""
import argparse
import hashlib
import json
from pathlib import Path
import plistlib
import sys
import time
import urllib.parse
import urllib.request

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'schema-condition-probe'))
from generate import png

NAME = 'ZZ Element Validity 9644'
INSTALL = Path.home() / 'Library/Application Support/VirtualDJ/Skins' / NAME
STATE = Path('/tmp/vdj-element-validity-state.json')
JOURNAL = HERE / 'run-9644.jsonl'
TAGS = ['bare', 'panel', 'group', 'pannel', 'zzinvalidalpha', 'zzinvalidbeta', 'button', 'textzone']


def log(**row):
    with JOURNAL.open('a') as f:
        f.write(json.dumps(row) + '\n')
        f.flush()


def request(script, kind='query'):
    if kind == 'execute':
        log(intent=script)
    with urllib.request.urlopen('http://localhost/' + kind + '?' + urllib.parse.urlencode({'script': script}), timeout=15) as r:
        value = r.read().decode().strip()
    log(**{kind: script, 'result': value})
    if value.startswith('error:'):
        raise ValueError(value)
    return value


def context():
    return {f'deck {n} {v}': request(f'deck {n} {v}') for n in range(1, 5) for v in ('loaded', 'play')}


def wait_skin(name):
    for _ in range(30):
        if request('load_skin') == name:
            return
        time.sleep(.2)
    raise ValueError('Skin readback mismatch; do not retry the write')


def label(text, x, y, color='#FFFFFF'):
    return f'<textzone x="{x}" y="{y}" width="350" height="32"><text font="Arial" size="20" color="{color}" format="{text}"/></textzone>'


def fixture(round_number):
    tags = TAGS if round_number == 1 else list(reversed(TAGS))
    parts = [f'<skin name="{NAME}" version="8" width="1200" height="720">',
             label(f'NESTING CANARY - ROUND {round_number}', 25, 12),
             label('Wrapper', 25, 52), label('Nested child', 450, 52), label('Leaf own drawing', 820, 52)]
    for n, tag in enumerate(tags):
        y = 100 + n * 68
        parts.append(label(tag, 25, y))
        child = label(f'CHILD {tag} R{round_number}', 450, y, '#00FFFF')
        if tag == 'bare':
            parts.append(child)
        elif tag == 'button':
            parts.append(f'<button x="820" y="{y}" width="220" height="32"><up color="#E03030"/>{child}</button>')
        elif tag == 'textzone':
            parts.append(f'<textzone x="820" y="{y}" width="350" height="32"><text font="Arial" size="20" color="#FFFF00" format="OWN TEXT"/>{child}</textzone>')
        else:
            parts.append(f'<{tag} x="0" y="0" width="1200" height="720">{child}</{tag}>')
    parts.append(label('END CONTROL', 25, 665))
    parts.append('</skin>')
    return ('\n'.join(parts) + '\n').encode()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('step', choices=['begin', 'install', 'load', 'restore', 'uninstall'])
    p.add_argument('--round', type=int, choices=[1, 2], default=1)
    a = p.parse_args()
    if a.step == 'begin':
        if STATE.exists() or JOURNAL.exists():
            raise ValueError('Capture already exists')
        build = plistlib.loads(Path('/Applications/VirtualDJ.app/Contents/Info.plist').read_bytes())['CFBundleVersion']
        before = context()
        if build != '18.0.9644' or any(v not in ('no', 'off', '0', 'false') for v in before.values()):
            raise ValueError('Requires build 9644 and empty stopped decks')
        skin = request('load_skin')
        if not skin or "'" in skin:
            raise ValueError('Unquotable original skin')
        STATE.write_text(json.dumps({'build': build, 'skin': skin, 'context': before}))
        log(begin={'build': build, 'context': before})
    elif a.step == 'install':
        if a.round == 1:
            INSTALL.mkdir(exist_ok=False)
            for name, data in [('skin.png', png(1200, 720)), ('preview.png', png(300, 180))]:
                (HERE / name).write_bytes(data)
                (INSTALL / name).write_bytes(data)
        elif (INSTALL / 'skin.xml').read_bytes() != fixture(1):
            raise ValueError('Unexpected installed fixture')
        raw = fixture(a.round)
        (HERE / f'round-{a.round}.xml').write_bytes(raw)
        (INSTALL / 'skin.xml').write_bytes(raw)
        log(installed_round=a.round, xml_sha256=hashlib.sha256(raw).hexdigest())
    elif a.step == 'load':
        request(f"load_skin '{NAME}/:skin'", 'execute')
        wait_skin(NAME + '/:skin')
        log(loaded_round=a.round)
    elif a.step == 'restore':
        before = json.loads(STATE.read_text())
        request("load_skin '" + before['skin'] + "'", 'execute')
        wait_skin(before['skin'])
        after = context()
        verified = after == before['context']
        log(restored=True, context=after, verified=verified)
        if not verified:
            raise ValueError('Context changed')
    else:
        before = json.loads(STATE.read_text())
        if request('load_skin') != before['skin']:
            raise ValueError('Restore original first')
        expected = {'skin.xml': fixture(a.round), 'skin.png': png(1200, 720), 'preview.png': png(300, 180)}
        if {f.name for f in INSTALL.iterdir()} != set(expected):
            raise ValueError('Unexpected install files')
        for name, data in expected.items():
            if (INSTALL / name).read_bytes() != data:
                raise ValueError('Installed bytes changed')
        for name in expected:
            (INSTALL / name).unlink()
        INSTALL.rmdir()
        log(uninstalled=True)
    print(a.step, 'ok')


if __name__ == '__main__':
    main()
