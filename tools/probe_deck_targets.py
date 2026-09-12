"""Bisect which deck-wrapper token makes VirtualDJ exit.

Read-only by construction: the payloads are `get_deck` and `constant 37`, so a
lost process leaves nothing to restore. One token per request on a FRESH
connection, the journal flushed to disk BEFORE the request is sent, and a
liveness check after every one. The token in flight when the process disappears
is named, and the run stops there rather than continuing into a dead app.

An exit here leaves no crash report (see the hazard section in
docs/Runtime Argument Grammar Tests.md), so process identity is the evidence:
the pid is recorded at the start and compared after every probe.
"""
import argparse
import json
import os
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path

PAYLOADS = ['get_deck', 'constant 37']
# Attested in Atomix's own shipped scripts (just attested-tails --verb deck),
# plus the wiki's nine, plus every extra target this repo has seen answer.
TOKENS = [
    '1', '2', '3', '4', 'left', 'right', 'all', 'default', 'active', 'master',
    'leftvideo', 'rightvideo',
    'playing', 'mixer1', 'mixer2', 'mixer3', 'mixer4',
    'sandbox',
    '[LEFTDECK]', '[RIGHTDECK]', '[SWAPDECK]', '[MINIDECK_LEFT]', '[MINIDECK_RIGHT]',
]


def pids():
    r = subprocess.run(['pgrep', '-f', 'MacOS/VirtualDJ'], capture_output=True, text=True)
    return sorted(x for x in r.stdout.split() if x)


def ask(endpoint, script, timeout):
    url = f'http://localhost/{endpoint}?' + urllib.parse.urlencode({'script': script})
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read().decode(errors='replace').strip()


def flush(path, state):
    tmp = path.with_suffix(path.suffix + '.tmp')
    with open(tmp, 'w') as f:
        json.dump(state, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(path)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, default=Path('tests/deck-target-exit-probe-9598.json'))
    p.add_argument('--timeout', type=float, default=6.0)
    p.add_argument('--settle', type=float, default=0.4, help='seconds between probes')
    p.add_argument('--resume', action='store_true', help='skip tokens already recorded ok')
    p.add_argument('--only', help='comma-separated tokens to probe instead of the full list')
    a = p.parse_args()

    alive = pids()
    if len(alive) != 1:
        raise SystemExit(f'expected exactly one VirtualDJ process, found {alive}')
    state = {'summary': {'mode': 'deck-target-exit-bisect', 'pid': alive[0],
                         'payloads': PAYLOADS, 'status': 'running',
                         'claim_scope': 'which deck-wrapper token was in flight at an exit; '
                                        'read-only payloads, no state to restore'},
             'probes': []}
    if a.resume and a.out.exists():
        prior = json.loads(a.out.read_text())
        state['probes'] = [r for r in prior['probes'] if r['status'] == 'answered']
        state['summary']['resumed_from_pid'] = prior['summary'].get('pid')
    done = {(r['token'], r['payload']) for r in state['probes']}

    state['summary']['build'] = ask('query', 'get_build', a.timeout)
    tokens = a.only.split(',') if a.only else TOKENS
    flush(a.out, state)

    for token in tokens:
        for payload in PAYLOADS:
            if (token, payload) in done:
                continue
            script = f'deck {token} {payload}'
            row = {'token': token, 'payload': payload, 'script': script, 'status': 'in-flight'}
            state['probes'].append(row)
            flush(a.out, state)           # On disk before the request leaves.
            print(f'-> {script}', flush=True)
            try:
                row['response'] = ask('query', script, a.timeout)
                row['status'] = 'answered'
            except Exception as e:
                row['status'] = 'no-response'
                row['error'] = repr(e)
            still = pids()
            row['pids_after'] = still
            if still != alive:
                row['status'] = 'process-gone' if not still else 'process-changed'
                state['summary'].update(status='exit-observed', exit_script=script,
                                        exit_token=token, exit_payload=payload,
                                        pids_after=still)
                flush(a.out, state)
                print(f'\nPROCESS LOST while probing: {script!r}\n'
                      f'  pid {alive} -> {still}\n'
                      f'  recorded in {a.out}', flush=True)
                return 2
            flush(a.out, state)
            time.sleep(a.settle)

    state['summary']['status'] = 'complete'
    flush(a.out, state)
    answered = [r for r in state['probes'] if r['status'] == 'answered']
    print(f'\n{len(answered)}/{len(state["probes"])} answered; process {alive[0]} survived all.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
