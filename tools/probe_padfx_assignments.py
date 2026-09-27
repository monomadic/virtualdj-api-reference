#!/usr/bin/env python3
"""Fixed, stopped-deck padfx assignment probes with journaled writes and restoration.

Explicit final on avoids relying on padfx's saved-state/toggle lifecycle. No
stem routing, media loading, playback, or broad effect reset is performed.
"""
import argparse
import datetime
import http.client
import json
from pathlib import Path
from urllib.parse import urlencode

EFFECTS = {'Echo Out': 0, 'Flanger': 2, 'Reverb': 2}
CASES = [
    ('named_percent', 'Echo Out', "'Feedback:37%' 'Color:62%' 'Reverb:23%'"),
    ('named_decimal', 'Echo Out', "'Feedback:0.37' 'Color:0.62' 'Reverb:0.23'"),
    ('named_alias_case', 'Echo Out', "'fbck:37%' 'col:62%' 'rvb:23%'"),
    ('named_reordered', 'Echo Out', "'Reverb:23%' 'Feedback:37%' 'Color:62%'"),
    ('length_beats', 'Echo Out', "'Length:2bt'"),
    ('length_milliseconds', 'Echo Out', "'Length:500ms'"),
    ('unit_redirect', 'Echo Out', "'Feedback:2bt'"),
    ('named_unknown_a', 'Echo Out', "'zzunknowna:37%'"),
    ('named_unknown_b', 'Echo Out', "'zzunknownb:37%'"),
    ('malformed_value_a', 'Echo Out', "'Feedback:zzunknowna'"),
    ('malformed_value_b', 'Echo Out', "'Feedback:zzunknownb'"),
    ('duplicate_forward', 'Echo Out', "'Feedback:23%' 'Feedback:61%'"),
    ('duplicate_reverse', 'Echo Out', "'Feedback:61%' 'Feedback:23%'"),
    ('mixed_named_numeric', 'Echo Out', "'Color:61%' 0.23"),
    ('mixed_numeric_named', 'Echo Out', "0.23 'Color:61%'"),
    ('full_named', 'Echo Out', "'Feedback:80%' 'Length:1bt' 'Color:50%' 'Reverb:78%'"),
    ('flanger_positional', 'Flanger', '0.5 8bt 0.5 0.5'),
    ('reverb_positional', 'Reverb', '0.4 0.1 0.3 0.4'),
    ('button_on', 'Flanger', "'Tone:on'"),
    ('button_off', 'Flanger', "'Tone:off'"),
    ('button_unknown_a', 'Flanger', "'Tone:zzunknowna'"),
    ('button_unknown_b', 'Flanger', "'Tone:zzunknownb'"),
]


class Probe:
    def __init__(self, journal):
        self.journal = journal

    def request(self, endpoint, script):
        self.journal.write(json.dumps({'event': 'intent', 'endpoint': endpoint, 'script': script}) + '\n')
        self.journal.flush()
        connection = http.client.HTTPConnection('localhost', timeout=5)
        try:
            connection.request('GET', '/' + endpoint + '?' + urlencode({'script': script}))
            response = connection.getresponse()
            value = response.read().decode().strip()
            if response.status != 200 or value.startswith('error:'):
                raise ValueError(f'{endpoint} {script}: HTTP {response.status}, {value}')
        finally:
            connection.close()
        self.journal.write(json.dumps({'event': 'result', 'endpoint': endpoint, 'script': script, 'value': value}) + '\n')
        self.journal.flush()
        return value

    def query(self, script):
        return self.request('query', script)

    def execute(self, script):
        return self.request('execute', script)  # Never retry an uncertain write.

    def state(self, effect):
        return {'active': self.query(f"deck 2 effect_active '{effect}'"),
                'sliders': [float(self.query(f"deck 2 effect_slider '{effect}' {n} & param_multiply 1000000")) / 1000000 for n in range(1, 5)],
                'texts': [self.query(f"deck 2 get_effect_slider_text '{effect}' {n}") for n in range(1, 5)],
                'buttons': [self.query(f"deck 2 effect_button '{effect}' {n}") for n in range(1, EFFECTS[effect] + 1)]}

    def boundary(self):
        scripts = [f'deck {d} {v}' for d in range(1, 5) for v in ('play', 'loaded')]
        scripts += [f"deck {d} effect_active '{e}'" for d in (1, 3, 4) for e in EFFECTS]
        scripts += ['deck 2 get_bpm', 'deck 2 pitch']
        scripts += [f'deck 2 get_effect_name {n}' for n in range(1, 4)]
        return {s: self.query(s) for s in scripts}

    def restore(self, effect, original):
        self.execute(f"deck 2 effect_active '{effect}' off")
        for n, value in enumerate(original['sliders'], 1):
            self.execute(f"deck 2 effect_slider '{effect}' {n} {value:.12g}")
        for n, value in enumerate(original['buttons'], 1):
            self.execute(f"deck 2 effect_button '{effect}' {n} " + ('on' if value == 'yes' else 'off'))
        restored = self.state(effect)
        if not same(restored, original):
            raise ValueError(f'{effect} restoration failed')
        return restored


def same(left, right):
    return all(abs(a - b) < 0.00001 for a, b in zip(left['sliders'], right['sliders'])) and all(
        left[k] == right[k] for k in ('active', 'buttons', 'texts'))


def run(output):
    output = output.resolve()
    journal_path = output.with_suffix('.journal.jsonl')
    if output.exists() or journal_path.exists():
        raise FileExistsError('output or journal exists')
    result = {'date': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'channel': 'HTTP', 'context': 'Deck 2 stopped; existing loaded state retained; no audio-output claim.',
              'scope': 'Assignments with explicit final on; separate off and control restoration. Stem routing and automatic padfx restoration not tested.',
              'cases': [], 'journal': journal_path.name,
              'screenshot_provenance': 'Not applicable: HTTP journal and independent effect-control readbacks.'}
    with journal_path.open('x') as journal:
        probe = Probe(journal)
        try:
            result['build'] = probe.query('get_build')
            if result['build'] != '9644':
                raise ValueError('this suite requires live build 9644')
            result['before'] = probe.boundary()
            if any(result['before'][f'deck {d} play'] != 'no' for d in range(1, 5)):
                raise ValueError('all decks must be stopped')
            if float(result['before']['deck 2 get_bpm']) <= 0:
                raise ValueError('positive deck BPM required for millisecond case')
            originals = {e: probe.state(e) for e in EFFECTS}
            result['originals'] = originals
            if any(s['active'] != 'no' for s in originals.values()):
                raise ValueError('target effects must initially be inactive')
            # Establish one independent write/read/restore round trip first.
            try:
                probe.execute("deck 2 effect_slider 'Echo Out' 1 0.314")
                calibration = probe.state('Echo Out')
                result['calibration'] = calibration
                if abs(calibration['sliders'][0] - 0.314) > 0.00001:
                    raise ValueError('slider calibration failed')
                result['calibration'] = calibration
            finally:
                result['calibration_restored'] = probe.restore('Echo Out', originals['Echo Out'])
            for round_number in (1, 2):
                for name, effect, tail in (CASES if round_number == 1 else reversed(CASES)):
                    if probe.query('deck 2 play') != 'no':
                        raise ValueError('playback started; stopping probes')
                    row = {'round': round_number, 'name': name, 'effect': effect,
                           'script': f"deck 2 padfx '{effect}' {tail} on"}
                    result['cases'].append(row)
                    try:
                        # Make the off/invalid button-value cases discriminate.
                        if name.startswith('button_') and name != 'button_on':
                            probe.execute("deck 2 effect_button 'Flanger' 1 on")
                        row['before'] = probe.state(effect)
                        probe.execute(row['script'])
                        row['after'] = probe.state(effect)
                        if row['after']['active'] != 'yes':
                            raise ValueError('padfx did not activate the observed effect')
                    finally:
                        row['restored'] = probe.restore(effect, originals[effect])
            result['after'] = probe.boundary()
            if result['after'] != result['before']:
                raise ValueError('boundary state changed')
            result['complete'] = True
        except Exception as error:
            result['complete'] = False
            result['error'] = str(error)
            raise
        finally:
            with output.open('x') as f:
                json.dump(result, f, indent=2); f.write('\n')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    r = run(args.output)
    print(json.dumps({'complete': r['complete'], 'build': r['build'], 'boundary_restored': r['before'] == r['after']}))
