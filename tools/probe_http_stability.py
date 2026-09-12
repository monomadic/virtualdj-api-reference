"""Does the HTTP channel itself destabilize VirtualDJ, independent of script?

The deck-target bisection cleared every token, including the one in flight at
the recorded exit, so the next variable is how the suites talk to the app rather
than what they say. The suites reuse ONE connection across hundreds of requests;
the bisector opened a fresh connection per request.

Two arms, same benign payload (`get_build`), same pacing:

    reuse  - one keep-alive connection for the whole arm (what the suites do)
    fresh  - a new connection per request

Read-only throughout: no execute endpoint, no state to restore. Liveness is
checked by process identity, because these exits leave no crash report.
"""
import argparse
import http.client
import json
import os
import subprocess
import time
import urllib.parse
from pathlib import Path

SCRIPT = 'get_build'


def pids():
    r = subprocess.run(['pgrep', '-f', 'MacOS/VirtualDJ'], capture_output=True, text=True)
    return sorted(x for x in r.stdout.split() if x)


def flush(path, state):
    tmp = path.with_suffix(path.suffix + '.tmp')
    with open(tmp, 'w') as f:
        json.dump(state, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(path)


def arm(mode, count, pace, timeout, alive, state, path):
    row = {'mode': mode, 'requested': count, 'pace': pace, 'completed': 0,
           'status': 'running', 'first_error_at': None, 'error': None}
    state['arms'].append(row)
    flush(path, state)
    conn = None
    try:
        for i in range(count):
            try:
                if conn is None:
                    conn = http.client.HTTPConnection('localhost', 80, timeout=timeout)
                conn.request('GET', '/query?' + urllib.parse.urlencode({'script': SCRIPT}))
                conn.getresponse().read()
            except Exception as e:
                row['first_error_at'] = i
                row['error'] = repr(e)
                row['status'] = 'transport-error'
                flush(path, state)
                break
            finally:
                if mode == 'fresh' and conn is not None:
                    conn.close()
                    conn = None
            row['completed'] = i + 1
            if (i + 1) % 50 == 0:
                row['pids_at_checkpoint'] = pids()
                flush(path, state)
                if row['pids_at_checkpoint'] != alive:
                    row['status'] = 'process-lost'
                    return False
            if pace:
                time.sleep(pace)
    finally:
        if conn is not None:
            conn.close()
    still = pids()
    row['pids_after'] = still
    if still != alive:
        row['status'] = 'process-lost'
        flush(path, state)
        return False
    if row['status'] == 'running':
        row['status'] = 'survived'
    flush(path, state)
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, default=Path('tests/http-stability-probe-9598.json'))
    p.add_argument('--count', type=int, default=300)
    p.add_argument('--pace', type=float, default=0.025, help='seconds between requests')
    p.add_argument('--timeout', type=float, default=6.0)
    p.add_argument('--modes', default='fresh,reuse')
    a = p.parse_args()

    alive = pids()
    if len(alive) != 1:
        raise SystemExit(f'expected exactly one VirtualDJ process, found {alive}')
    state = {'summary': {'mode': 'http-stability-arms', 'pid': alive[0], 'script': SCRIPT,
                         'count_per_arm': a.count, 'pace': a.pace, 'status': 'running',
                         'claim_scope': 'whether the request pattern alone precedes an exit; '
                                        'read-only, single benign query'},
             'arms': []}
    flush(a.out, state)
    for mode in a.modes.split(','):
        print(f'-- arm {mode}: {a.count} x {SCRIPT!r}', flush=True)
        if not arm(mode, a.count, a.pace, a.timeout, alive, state, a.out):
            state['summary'].update(status='exit-observed', exit_arm=mode, pids_after=pids())
            flush(a.out, state)
            print(f'\nPROCESS LOST during the {mode!r} arm; recorded in {a.out}', flush=True)
            return 2
        print(f'   {state["arms"][-1]["status"]} '
              f'({state["arms"][-1]["completed"]}/{a.count})', flush=True)
    state['summary']['status'] = 'complete'
    flush(a.out, state)
    print(f'\nprocess {alive[0]} survived every arm.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
