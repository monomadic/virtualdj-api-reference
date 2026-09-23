#!/usr/bin/env python3
"""Calibrate VDJScript statement recognition through independent branch markers.

Fixed read-only predicates only. /execute writes just a temporary numeric marker;
the predicate is never used as a top-level action. No automatic request retries.
NO_BRANCH is an observation, not a universal invalid-syntax verdict.
"""
import argparse
from datetime import datetime, timezone
import json
import math
import os
import time
from pathlib import Path
import urllib.parse
import urllib.request

CASES = [
    ('true', 'true'), ('false', 'false'), ('on', 'on'), ('off', 'off'),
    ('text', "get_text 'hi'"), ('empty-text', "get_text ''"),
    ('misspelled-text', "gettext 'hi'"),
    ('unknown-alpha', 'zzinvalidalpha'), ('unknown-beta', 'zzinvalidbeta'),
    ('version', 'get_version'), ('nothing', 'nothing'),
    ('missing-text-argument', 'get_text'),
    ('on-unknown-tail', 'on zzinvalidalpha'),
    ('text-unknown-tail', "get_text 'hi' zzinvalidalpha"),
]
VARIABLE = '$statement_branch_probe_9644'


def classify(value, true_code, false_code):
    return 'TRUE_BRANCH' if value == str(true_code) else 'FALSE_BRANCH' if value == str(false_code) else 'NO_BRANCH' if value == '0' else 'UNEXPECTED_MARKER'


def check_capture(path):
    data = json.loads(path.read_text())
    if not data['complete'] or not data.get('restoration', {}).get('verified'):
        raise ValueError('Capture is incomplete or restoration unverified')
    expected = {(n, name) for n in (1, 2) for name, _ in CASES}
    seen = set()
    predicates = dict(CASES)
    outcomes = {}
    for row in data['cases']:
        key = row['round'], row['case']
        if key in seen or key not in expected or row['predicate'] != predicates[row['case']]:
            raise ValueError('Unexpected or duplicate case')
        seen.add(key)
        codes = (1, 2) if row['round'] == 1 else (2, 1)
        if (row['true_code'], row['false_code']) != codes:
            raise ValueError('Wrong round code assignment')
        outcome = classify(row['marker'], *codes)
        if outcome != row['outcome'] or outcome == 'UNEXPECTED_MARKER':
            raise ValueError('Invalid marker classification')
        outcomes.setdefault(row['case'], set()).add(outcome)
    if seen != expected or any(len(v) != 1 for v in outcomes.values()):
        raise ValueError('Missing cases or rounds disagree')
    for name, outcome in [('true', 'TRUE_BRANCH'), ('on', 'TRUE_BRANCH'), ('false', 'FALSE_BRANCH'), ('off', 'FALSE_BRANCH')]:
        if outcomes[name] != {outcome}:
            raise ValueError('Positive/negative calibration failed')
    print('Statement branch capture: complete, controls calibrated, rounds agree, restoration verified')


def run(output):
    journal = output.with_suffix('.jsonl')
    if output.exists() or journal.exists():
        raise ValueError('Capture or journal already exists')
    output.parent.mkdir(parents=True, exist_ok=True)
    stream = journal.open('x')

    def log(**row):
        stream.write(json.dumps({'utc': datetime.now(timezone.utc).isoformat(), **row}) + '\n')
        stream.flush()
        os.fsync(stream.fileno())

    def request(script, kind='query'):
        log(intent={'channel': kind, 'script': script})
        with urllib.request.urlopen('http://localhost/' + kind + '?' + urllib.parse.urlencode({'script': script}), timeout=20) as response:
            value = response.read().decode().strip()
        log(response={'channel': kind, 'script': script, 'value': value})
        time.sleep(0.05)
        return value

    def marker():
        return request(f"get_var '{VARIABLE}'")

    def context():
        return {f'deck {n} {v}': request(f'deck {n} {v}') for n in range(1, 5) for v in ('loaded', 'play')}

    result = {'schema': 1, 'channel': 'HTTP query and execute with independent numeric marker readback',
              'variable': VARIABLE, 'cases': [], 'complete': False,
              'limitations': ['Fixed simple predicates only; not a general grammar validator.',
                              'NO_BRANCH does not identify syntax error versus missing evaluation capability or state.',
                              'A taken branch does not prove all arguments were consumed.',
                              'An initially unset temporary variable is restored to zero, not deleted.']}
    dirty = False
    try:
        result['build'] = request('get_build')
        result['version'] = request('get_version')
        if result['build'] != '9644':
            raise ValueError('Calibration is pinned to build 9644')
        result['context_before'] = context()
        if any(v not in ('no', 'off', '0', 'false') for v in result['context_before'].values()):
            raise ValueError('Calibration requires empty stopped decks')
        result['marker_before'] = marker()
        if not math.isfinite(float(result['marker_before'] or '0')):
            raise ValueError('Cannot restore marker')
        log(baseline=result.copy())
        dirty = True
        for code in (1, 2, 0):
            request(f"set '{VARIABLE}' {code}", 'execute')
            if marker() != str(code):
                raise ValueError('Marker round trip failed')
        for round_number in (1, 2):
            true_code, false_code = (1, 2) if round_number == 1 else (2, 1)
            rows = CASES if round_number == 1 else list(reversed(CASES))
            for name, predicate in rows:
                request(f"set '{VARIABLE}' 0", 'execute')
                if marker() != '0':
                    raise ValueError('Marker reset failed')
                script = f"{predicate} ? set '{VARIABLE}' {true_code} : set '{VARIABLE}' {false_code}"
                returned = request(script, 'execute')
                observed = marker()
                query_script = f"{predicate} ? get_text 'TRUE_BRANCH' : get_text 'FALSE_BRANCH'"
                query_result = request(query_script)
                row = {'round': round_number, 'case': name, 'predicate': predicate,
                       'execute_script': script, 'execute_return': returned,
                       'marker': observed, 'true_code': true_code, 'false_code': false_code,
                       'outcome': classify(observed, true_code, false_code),
                       'query_script': query_script, 'query_result': query_result}
                result['cases'].append(row)
                log(observation=row)
                if row['outcome'] == 'UNEXPECTED_MARKER':
                    raise ValueError('Unexpected marker')
        result['complete'] = True
    except Exception as exc:
        result['error'] = str(exc)
        raise
    finally:
        try:
            if dirty:
                expected = result['marker_before'] or '0'
                request(f"set '{VARIABLE}' {expected}", 'execute')
                observed = marker()
                after = context()
                ok = float(observed) == float(expected) and after == result['context_before']
                result['restoration'] = {'expected_marker': expected, 'observed_marker': observed,
                                         'context_after': after, 'verified': ok,
                                         'exact_marker_restoration': observed == result['marker_before']}
                log(restoration=result['restoration'])
                if not ok:
                    raise ValueError('Restoration failed')
        finally:
            with output.open('x') as f:
                json.dump(result, f, indent=2)
                f.write('\n')
            stream.close()
    for row in result['cases']:
        print(row['round'], row['case'], row['outcome'], 'query=' + row['query_result'])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run', action='store_true')
    p.add_argument('--output', type=Path)
    p.add_argument('--check', type=Path, help='validate a completed capture offline')
    a = p.parse_args()
    if a.check:
        check_capture(a.check)
    elif a.run:
        if not a.output:
            p.error('--run requires a fresh --output path')
        run(a.output)
    else:
        print(json.dumps({'variable': VARIABLE, 'predicates': CASES}, indent=2))


if __name__ == '__main__':
    main()
