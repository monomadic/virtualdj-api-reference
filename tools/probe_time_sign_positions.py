#!/usr/bin/env python3
"""Stopped generated-audio sign fixture; journal writes, no action retries."""
import argparse
import hashlib
import http.client
import json
import os
from pathlib import Path
import time
from urllib.parse import urlencode
import wave

from extract_verb_table import BINARY

FORMS = ('', 'elapsed', 'remain', 'total', 'absolute', 'zzunknowna', 'zzunknownb')


def request(script, endpoint='query'):
    conn = http.client.HTTPConnection('localhost', timeout=5)
    try:
        conn.request('GET', '/' + endpoint + '?' + urlencode({'script': script}))
        response = conn.getresponse()
        value = response.read().decode()
        if response.status != 200:
            raise RuntimeError(f'HTTP {response.status}')
        return value
    finally:
        conn.close()


def q(script):
    return request('deck 1 ' + script)


def mode():
    modes = [m for m in ('elapsed', 'remain', 'total') if q(f"display_time '{m}'") == 'yes']
    if len(modes) != 1:
        raise RuntimeError('no unique display mode')
    return modes[0]


def state():
    return dict(loaded=q('loaded'), play=q('play'), pitch=q('pitch'), mode=mode())


def wait(script, predicate):
    deadline = time.monotonic() + 15
    while True:
        value = q(script)
        if predicate(value):
            return value
        if time.monotonic() >= deadline:
            raise RuntimeError(f'fixture readback failed: {script} = {value}')
        time.sleep(.1)


def validate(data):
    assert len(data['runs']) == 2
    assert data['requested_positions_ms'] in ([0, 1000], [0, -1000, 1000])
    for run in data['runs']:
        assert run['restored'] and run['before'] == run['after']
        assert len(run['phases']) == len(data['requested_positions_ms']) * 3
        assert {(p['requested_ms'], p['mode']) for p in run['phases']} == {
            (ms, mode) for ms in data['requested_positions_ms'] for mode in ('elapsed', 'remain', 'total')}
        for p in run['phases']:
            assert abs(float(p['position_ms']) - p['requested_ms']) < 2
            assert p['play'] == 'no'
            elapsed = (p['requested_ms'] > 0) - (p['requested_ms'] < 0)
            expected = {'elapsed': elapsed, 'remain': 1, 'total': 1,
                        'zzunknowna': elapsed, 'zzunknownb': elapsed}
            expected[''] = expected[p['mode']]
            expected['absolute'] = expected[p['mode']]
            assert set(p['readings']) == set(FORMS)
            for form, values in p['readings'].items():
                assert values == [str(expected[form])] * 2, (p['requested_ms'], p['mode'], form, values)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path)
    ap.add_argument('--check', type=Path)
    ap.add_argument('--include-negative', action='store_true', help='also attempt -1000ms; abort if position cannot be established')
    args = ap.parse_args()
    if args.check:
        data = json.loads(args.check.read_text())
        validate(data)
        journal = args.check.with_suffix('.journal.jsonl')
        assert hashlib.sha256(journal.read_bytes()).hexdigest() == data['journal_sha256']
        print('sign fixture: position, sign matrix, controls and restoration passed')
        return
    if not args.output:
        ap.error('--output or --check required')
    if args.output.exists():
        raise FileExistsError(args.output)
    audio = Path('/tmp/vdj-sign-fixture-60s.wav')
    if not audio.exists():
        with wave.open(str(audio), 'wb') as f:
            f.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
            f.writeframes(b'\0\0' * 480000)
    with wave.open(str(audio)) as f:
        assert f.getparams()[:4] == (1, 2, 8000, 480000)
        assert not any(f.readframes(480000)), 'fixture is not silence'
    data = dict(build=request('get_build'), binary_sha256=hashlib.sha256(Path(BINARY).read_bytes()).hexdigest(),
                fixture=dict(path=str(audio), sha256=hashlib.sha256(audio.read_bytes()).hexdigest(),
                             duration_ms=60000, position_oracle='get_position & param_multiply 60000'),
                channel='HTTP', captured_unix=time.time(), runs=[],
                requested_positions_ms=[0, -1000, 1000] if args.include_negative else [0, 1000])
    journal_path = args.output.with_suffix('.journal.jsonl')
    with journal_path.open('x') as journal:
        def log(event):
            journal.write(json.dumps(event) + '\n'); journal.flush(); os.fsync(journal.fileno())
        def execute(script):
            assert script.startswith(('load ', 'goto ', 'display_time ')) or script == 'unload'
            log(dict(event='intent', script='deck 1 ' + script))
            result = request('deck 1 ' + script, 'execute')
            log(dict(event='response', result=result))
            if result.startswith('error:'):
                raise RuntimeError(result)
        def set_mode(target):
            if mode() != target:
                execute(f"display_time '{target}'")
                wait(f"display_time '{target}'", lambda v: v == 'yes')
        try:
            for number in (1, 2):
                before = state()
                if before['loaded'] != 'no' or before['play'] != 'no':
                    raise RuntimeError('requires empty stopped deck 1')
                run = dict(number=number, before=before, phases=[])
                data['runs'].append(run)
                log(dict(event='before', state=before, build=data['build']))
                try:
                    execute(f"load '{audio}'")
                    wait('get_loaded_song "fullpath"', lambda v: v == str(audio))
                    wait('loaded', lambda v: v == 'yes')
                    settings = [(ms, m) for ms in data['requested_positions_ms'] for m in ('elapsed', 'remain', 'total')]
                    for ms, display in settings if number == 1 else reversed(settings):
                        execute('goto 0%')
                        wait('get_position', lambda v: abs(float(v)) < .00001)
                        if ms:
                            execute(f'goto {ms:+d}ms')
                        position = wait('get_position & param_multiply 60000', lambda v: abs(float(v) - ms) < 2)
                        set_mode(display)
                        if q('play') != 'no':
                            raise RuntimeError('unexpected playback')
                        readings = {f: [] for f in FORMS}
                        for order in (FORMS, tuple(reversed(FORMS))):
                            for form in order:
                                readings[form].append(q('get_time_sign' + (f" '{form}'" if form else '')))
                        phase = dict(requested_ms=ms, position_ms=position, mode=mode(), play=q('play'), readings=readings)
                        run['phases'].append(phase); log(dict(event='phase', **phase))
                finally:
                    execute('unload')
                    wait('loaded', lambda v: v == 'no')
                    set_mode(before['mode'])
                    run['after'] = state()
                    run['restored'] = run['after'] == before
                    log(dict(event='restore', state=run['after'], restored=run['restored']))
                    if not run['restored']:
                        raise RuntimeError('restore failed')
            validate(data)
        except Exception as exc:
            data['error'] = str(exc)
            args.output.with_suffix('.aborted.json').write_text(json.dumps(data, indent=2) + '\n')
            raise
    data['journal_sha256'] = hashlib.sha256(journal_path.read_bytes()).hexdigest()
    args.output.write_text(json.dumps(data, indent=2) + '\n')
    print('sign fixture completed; both runs restored and validated')


if __name__ == '__main__':
    main()
