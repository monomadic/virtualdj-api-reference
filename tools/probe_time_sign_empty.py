#!/usr/bin/env python3
"""Read-only empty-deck control for the shared time-reader investigation."""
import argparse
import datetime
import hashlib
import http.client
import json
from pathlib import Path
from urllib.parse import urlencode

from extract_verb_table import BINARY

ROOT = Path(__file__).resolve().parents[1]
TAILS = ('', 'elapsed', 'remain', 'total', 'loopin', 'loopout', 'absolute',
         'cue', 'cue1', 'to_lyrics', 'zzunknowna', 'zzunknownb')


def query(script):
    conn = http.client.HTTPConnection('localhost', timeout=5)
    try:
        conn.request('GET', '/query?' + urlencode({'script': script}))
        response = conn.getresponse()
        value = response.read().decode()
        if response.status != 200:
            raise RuntimeError(f'HTTP {response.status}')
        return value
    finally:
        conn.close()


def state():
    return {f'deck {d} {v}': query(f'deck {d} {v}')
            for d in range(1, 5) for v in ('play', 'loaded')}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    source = ROOT / 'tests/time-sign-consumer-9644.json'
    static = json.loads(source.read_text())
    binary_hash = hashlib.sha256(Path(BINARY).read_bytes()).hexdigest()
    build = query('get_build')
    if build != '9644' or binary_hash != static['source']['binary_sha256']:
        raise RuntimeError('build differs from structural evidence')
    before = state()
    if set(before.values()) != {'no'}:
        raise RuntimeError('requires stopped, unloaded decks')
    rows = []
    for repeat in range(1, 3):
        for tail in TAILS:
            script = 'deck 1 get_time_sign' + (f" '{tail}'" if tail else '')
            value = query(script)
            if value not in ('', '-1', '0', '1') and not value.startswith('error:'):
                raise RuntimeError('unexpected response; not retained')
            rows.append(dict(round=repeat, script=script, result=value))
    after = state()
    result = dict(build=build, binary_sha256=binary_hash,
                  captured_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  channel='HTTP query only', fixture='stopped-unloaded-decks-1-through-4',
                  structural_source=str(source.relative_to(ROOT)),
                  structural_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  before=before, after=after, unchanged=before == after, results=rows,
                  conclusion='Empty-deck control only; argument recognition and negative-sign behavior remain unresolved.')
    with args.output.open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(json.dumps(dict(build=build, unchanged=result['unchanged'],
                          results=sorted({r['result'] for r in rows}))))
    if before != after:
        raise RuntimeError('deck state changed during read-only sweep')
