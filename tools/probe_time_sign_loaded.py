#!/usr/bin/env python3
"""Boundary sign sweep using long_time; stopped, journaled, independently reloaded."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import time

from fixtures import Channel, FixtureError, build_fixtures, establish
from probe_long_time import SECONDS, audio, mode, q, set_mode, wait
from probe_time_sign_positions import request

FORMS = {'bare': '', 'elapsed': "'elapsed'", 'remain': "'remain'",
         'total': "'total'", 'elapsed absolute': "'elapsed' 'absolute'",
         'zzqqx': "'zzqqx'", 'vfnrbq': "'vfnrbq'",
         'elapsed zzqqx': "'elapsed' 'zzqqx'",
         'elapsed vfnrbq': "'elapsed' 'vfnrbq'"}
CONTROLS = ('zzqqx', 'vfnrbq')
POSITIONS = {'start': (0, 'goto 0%'), 'before-start-ms': (-1000, 'goto -1000ms'),
             'before-start-percent': (-1000, f'goto {-100 / SECONDS:.12f}%'),
             'end': (SECONDS * 1000, 'goto 100%')}
ORACLE = f'get_position & param_multiply {SECONDS * 1000}'


class JournalChannel(Channel):
    def __init__(self, path):
        super().__init__()
        self.journal = path.open('x')

    def log(self, event):
        self.journal.write(json.dumps(event) + '\n')
        self.journal.flush()
        os.fsync(self.journal.fileno())

    def query(self, script):
        for attempt in range(2):
            try:
                value = request(script).strip()
                break
            except (TimeoutError, OSError) as exc:
                self.log(dict(query=script, read_error=str(exc), attempt=attempt + 1))
                if attempt == 1:
                    raise
        self.log(dict(query=script, result=value))
        return value

    def execute(self, script):
        if not script.startswith('deck 1 ') or not (
                script[7:].startswith(('load ', 'goto ', 'pitch ', 'display_time '))
                or script[7:] in ('pause', 'unload')):
            raise FixtureError(f'write outside fixture allowlist: {script}')
        self.log(dict(intent=script))
        value = request(script, 'execute').strip()  # Never retry uncertain writes.
        self.log(dict(execute=script, result=value))
        if value.startswith('error:'):
            raise FixtureError(value)
        return value


def state(ch):
    return {**{v: q(ch, v) for v in ('loaded', 'play', 'pitch', 'loop')}, 'mode': mode(ch)}


def position(ch):
    return {v: q(ch, v) for v in (ORACLE, 'get_position',
            "get_time 'elapsed' 'absolute'", "get_time 'remain' 'absolute'", 'play', 'loaded')}


def verified(readback, target):
    return (readback['play'] == 'no' and readback['loaded'] == 'yes'
            and abs(float(readback["get_time 'elapsed' 'absolute'"]) - target) < 2
            and abs(float(readback["get_time 'remain' 'absolute'"]) - (SECONDS * 1000 - target)) < 2
            and abs(float(readback[ORACLE]) - max(0, target)) < 2)


def classify(runs):
    result = {}
    for form in ('elapsed', 'remain', 'total', 'elapsed absolute'):
        controls = ('elapsed zzqqx', 'elapsed vfnrbq') if form == 'elapsed absolute' else CONTROLS
        separated = []
        for run in runs:
            separated.append([p['id'] for p in run['phases'] if not p['skipped']
                and all(len(set(p['readings'][f])) == 1 for f in (form, *controls, *CONTROLS))
                and p['readings'][form][0] in ('-1', '0', '1')
                and all(p['readings'][form][0] != p['readings'][c][0]
                        for c in (*controls, *CONTROLS))])
        result[form] = dict(verdict='recognized' if all(separated) else 'UNDISCRIMINATED',
                            separates_in=separated, controls=list(controls))
    return result


def run(ch, path, number, repeat):
    fixture = build_fixtures(path)['long_time']
    for assertion in fixture.preconditions:
        if not assertion.check(ch)[0]:
            raise FixtureError(assertion.describes)
    before = state(ch)
    result = dict(number=number, before=before, started_at=datetime.now(timezone.utc).isoformat(), phases=[])
    try:
        establish(ch, fixture, verbose=False)
        ch.execute('deck 1 pitch 100%')
        wait(ch, 'get_pitch', lambda v: abs(float(v)) < .001)
        settings = [(name, display) for name in POSITIONS for display in ('elapsed', 'remain', 'total')]
        for name, display in settings if number == 1 else reversed(settings):
            target, action = POSITIONS[name]
            ch.execute('deck 1 goto 0%')
            wait(ch, ORACLE, lambda v: abs(float(v)) < 2)
            set_mode(ch, display)
            ch.execute('deck 1 ' + action)
            # Poll readbacks only. A failed seek is recorded and skipped, never replayed.
            deadline = time.monotonic() + 1
            while True:
                readback = position(ch)
                if verified(readback, target) or time.monotonic() >= deadline:
                    break
                time.sleep(.1)
            p = dict(id=f'{name}/{display}', requested_ms=target, action='deck 1 ' + action,
                     display_time=mode(ch), pitch_percent=q(ch, 'get_pitch'), before=readback,
                     skipped=not verified(readback, target))
            result['phases'].append(p)
            if readback['play'] != 'no' or readback['loaded'] != 'yes':
                raise FixtureError('fixture lost stopped/loaded state')
            if p['skipped']:
                p['reason'] = 'Requested position not verified; no sign queries performed'
                continue
            p['readings'] = {f: [] for f in FORMS}
            for index in range(repeat):
                order = list(FORMS)
                if (number + index) % 2 == 0:
                    order.reverse()
                for form in order:
                    p['readings'][form].append(q(ch, 'get_time_sign' + (' ' + FORMS[form] if FORMS[form] else '')))
            p['after'] = position(ch)
            if not verified(p['after'], target) or mode(ch) != display:
                raise FixtureError('position/display changed during sweep')
            print(f"run {number} {p['id']}: " + str({f: v[0] for f, v in p['readings'].items()}), flush=True)
    finally:
        ch.execute('deck 1 unload')
        wait(ch, 'loaded', lambda v: v == 'no')
        ch.execute(f"deck 1 pitch {before['pitch']}")
        set_mode(ch, before['mode'])
        wait(ch, 'pitch', lambda v: abs(float(v) - float(before['pitch'])) < .00001)
        result['after'] = state(ch)
        result['restored'] = result['after'] == before
        ch.log(dict(restoration=result))
        if not result['restored']:
            raise FixtureError('RESTORATION FAILED; abort')
    return result


def validate(data):
    assert data['summary']['build'] == '9644'
    assert len(data['runs']) == 2 and data['repeat'] >= 3
    assert data['verdicts'] == classify(data['runs'])
    for run_data in data['runs']:
        assert run_data['restored'] and run_data['before'] == run_data['after']
        assert {p['id'] for p in run_data['phases']} == {f'{n}/{m}' for n in POSITIONS for m in ('elapsed', 'remain', 'total')}
        for p in run_data['phases']:
            if p['skipped']:
                assert not verified(p['before'], p['requested_ms']) and 'readings' not in p
            else:
                assert verified(p['before'], p['requested_ms']) and verified(p['after'], p['requested_ms'])
                assert abs(float(p['pitch_percent'])) < .001
                assert set(p['readings']) == set(FORMS)
                assert all(len(v) == data['repeat'] and len(set(v)) == 1 for v in p['readings'].values())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path)
    ap.add_argument('--repeat', type=int, default=3)
    ap.add_argument('--check', type=Path)
    args = ap.parse_args()
    if args.check:
        validate(json.loads(args.check.read_text()))
        print('Boundary state, repeated readings, verdicts and restoration validated')
        return
    if not args.output or args.repeat < 3:
        ap.error('--output required and --repeat must be at least 3')
    if args.output.exists():
        raise FileExistsError(args.output)
    journal_path = args.output.with_suffix('.journal.jsonl')
    ch = JournalChannel(journal_path)
    data = dict(summary=ch.provenance(), repeat=args.repeat, runs=[],
                scripts={f: 'deck 1 get_time_sign' + (' ' + s if s else '') for f, s in FORMS.items()},
                session_scope='Two independent unload/reload runs in the same application session; fresh HTTP connection per request')
    try:
        if data['summary']['build'] != '9644':
            raise FixtureError('requires live build 9644')
        path = audio()
        data['fixture'] = dict(name='long_time', duration_seconds=SECONDS, path=str(path), position_oracle=ORACLE,
                               signed_position_oracle="get_time 'elapsed' 'absolute'",
                               negative_position_note='get_position reads zero before start; signed elapsed and remaining readbacks must both agree')
        for n in (1, 2):
            data['runs'].append(run(ch, path, n, args.repeat))
        data['verdicts'] = classify(data['runs'])
        validate(data)
    except Exception as exc:
        data['error'] = str(exc)
        args.output.with_suffix('.aborted.json').write_text(json.dumps(data, indent=2) + '\n')
        raise
    finally:
        ch.journal.close()
    data['journal'] = [json.loads(line) for line in journal_path.read_text().splitlines()]
    args.output.write_text(json.dumps(data, indent=2) + '\n')
    journal_path.unlink()  # Completed capture embeds the complete durable journal.
    print(json.dumps(data['verdicts'], indent=2))


if __name__ == '__main__':
    main()
