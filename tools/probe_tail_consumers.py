#!/usr/bin/env python3
"""Read-only build-9246 memory/native tail calibration; new artifacts only."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re

from plugin_memory import verify
from probe_time_sign_empty import query, state

ROOT = Path(__file__).resolve().parents[1]
WORK = Path.home() / 'Library/Application Support/VirtualDJ/VDJIntrospect'
SUITE = ROOT / 'tests/is-using-keyword-cases.json'


def run(binary, output):
    if output.exists():
        raise FileExistsError(output)
    stem = output.with_suffix('')
    memory_out = Path(str(stem) + '-memory.json')
    native_out = Path(str(stem) + '-native.jsonl')
    if memory_out.exists() or native_out.exists():
        raise FileExistsError('companion output exists')
    before = state()
    build = query('get_build')
    if build != '9246' or set(before.values()) != {'no'}:
        raise ValueError('requires build 9246, stopped/unloaded decks 1-4')
    record = {'captured_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'build': build, 'before': before, 'channel': 'HTTP query + memory plugin + public SDK keyword plugin',
              'execute_calls': [], 'triggers': [], 'results': [],
              'context': 'Decks 1-4 stopped and unloaded. Hardware/account not inventoried. No private parser calls.',
              'screenshot_provenance': 'Not applicable: HTTP responses and plugin-written captures.'}
    try:
        for name, pattern, dest in [('VDJMemoryProbe', 'memory-*.json', memory_out),
                                     ('VDJKeywordProbe', 'keywords-*.jsonl', native_out)]:
            existing = set(WORK.glob(pattern))
            script = "get_effect_title '" + name + "'"
            value = query(script)
            files = sorted(set(WORK.glob(pattern)) - existing)
            record['triggers'].append({'script': script, 'result': value,
                                       'new_capture_names': [f.name for f in files]})
            if len(files) != 1:
                raise ValueError('expected one fresh capture; cached/absent plugin needs separate investigation')
            raw = files[0].read_bytes()
            if name == 'VDJMemoryProbe':
                capture = json.loads(raw)
                record['memory_verification'] = verify(capture, binary)
            else:
                rows = [json.loads(line) for line in raw.splitlines()]
                suite = json.loads(SUITE.read_text())['scripts']
                if rows[0].get('build') != 9246 or rows[0].get('build_hresult') != 0 or rows[-1] != {'event': 'complete'}:
                    raise ValueError('native capture incomplete or wrong build')
                if len(rows) != 2 + 2 * len(suite):
                    raise ValueError('native case count differs')
                for round in (1, 2):
                    group = rows[1 + (round - 1) * len(suite):1 + round * len(suite)]
                    if [r['script'] for r in group] != suite or any(r['round'] != round for r in group):
                        raise ValueError('native case order differs')
                record['native_suite_sha256'] = hashlib.sha256(SUITE.read_bytes()).hexdigest()
            with dest.open('xb') as f:
                f.write(raw)
            record[name] = {'capture': str(dest.relative_to(ROOT)), 'sha256': hashlib.sha256(raw).hexdigest(),
                            'installed_plugin_sha256': hashlib.sha256((WORK.parent / 'PluginsMacArm/SoundEffect' /
                                (name + '.bundle/Contents/MacOS/' + name)).read_bytes()).hexdigest()}
        for round in (1, 2):
            for tail in ('', 'name', 'clean', 'Skin', 'BASS', 'FILTER', 'filter', 'zzunknowna', 'zzunknownb'):
                script = 'deck 1 filter_label' + (" '" + tail + "'" if tail else '')
                value = query(script)
                # Do not retain arbitrary labels that might come from personal effects.
                if value not in ('', 'FILTER', 'BASS', 'DELAY', 'OFF') and not re.fullmatch(r'[-+0-9.% HzKk]+', value):
                    raise ValueError('unexpected label; not retained')
                record['results'].append({'round': round, 'script': script, 'result': value})
        record['complete'] = True
    except Exception as e:
        record['complete'] = False
        record['error'] = str(e)
        raise
    finally:
        record['after'] = state()
        record['state_checks_match'] = record['before'] == record['after']
        with output.open('x') as f:
            json.dump(record, f, indent=2); f.write('\n')
    if not record['state_checks_match']:
        raise ValueError('state changed during read-only probe')
    return record


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--binary', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    result = run(args.binary, args.output.resolve())
    print(json.dumps({'complete': result['complete'], 'state_checks_match': result['state_checks_match'],
                      'results': result['results']}, indent=2))
