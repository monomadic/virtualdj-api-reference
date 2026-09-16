"""Read-only selector tests while one initially empty deck plays generated silence.

Only decks 3/4 receive fixture media or transport writes. Loaded decks 1/2 are
protected by independent readbacks. Master/selection/PFL/pitch are journaled,
restored and checked after each baseline. Mutation requests are never replayed.
"""
import hashlib
import json
from pathlib import Path
import tempfile
import time
import wave
from collections import Counter

from fixtures import FixtureError
from runtime_grammar_actions import OnceChannel, Session, classify, equal
from runtime_grammar_probes import write_capture

ROOT = Path(__file__).resolve().parents[1]

FIXTURE = 'parser_playing_scope'
BASELINES = [{'master': '3', 'playing': '4'}, {'master': '4', 'playing': '3'}]
ALLOWED = {'get_deck'} | {f'deck {s} get_deck' for s in
    ('1', '3', '4', 'active', 'master', 'playing', 'default', 'zzh4scope_a', 'zzh4scope_b')}
GUARDS = ['get_decks', 'get_deck', 'masterdeck_auto'] + [
    f'deck {d} {q}' for d in range(1, 5)
    for q in ('loaded', 'play', 'select', 'pfl', 'masterdeck', 'volume', 'pitch', 'loop')]
PROTECTED = [f'deck {d} {q}' for d in (1, 2)
             for q in ('loaded', 'play', 'get_position', 'volume', 'pitch', 'loop')]


def require(ok, message):
    if not ok:
        raise FixtureError(message)


def validate(suite):
    seen = set()
    for case in suite['cases']:
        require(case['id'] not in seen and case['fixture'] == FIXTURE, 'invalid case identity')
        seen.add(case['id'])
        require(case.get('hypothesis') and case.get('binary_sites'), 'missing prediction provenance')
        scripts = [case['script'], *case['controls'], *(c['script'] for c in case['contrasts'])]
        require(all(s in ALLOWED for s in scripts), 'query outside selector allowlist')
        require(len(case['controls']) == len(set(case['controls'])) == 2, 'two controls required')
        require(any(c['expected'] != case['expected'] for c in case['contrasts']), 'no discriminator')
        for expected in [case['expected'], *(c['expected'] for c in case['contrasts'])]:
            require(len(expected) == 2 and all(len(v) == 1 for v in expected), 'invalid signature')
    return suite


def silent_audio():
    handle = tempfile.NamedTemporaryFile(prefix='vdj-h4-silent-', suffix='.wav', delete=False)
    path = Path(handle.name)
    handle.close()
    with wave.open(str(path), 'wb') as wav:
        wav.setparams((1, 2, 8000, 0, 'NONE', 'not compressed'))
        wav.writeframes(bytes(8000 * 180 * 2))
    with wave.open(str(path), 'rb') as wav:
        require(wav.getnframes() == 1440000 and not any(wav.readframes(wav.getnframes())),
                'fixture is not verified digital silence')
    return path


class PlayingSession(Session):
    def __init__(self, channel, capture, path, audio):
        super().__init__(channel, capture, path)
        self.audio = audio
        self.ready = False

    def values(self, queries):
        return {q: self.channel.query(q) for q in queries}

    def snapshot(self):
        original = self.values(GUARDS)
        require(original['get_decks'] == '4' and original['get_deck'] == '1',
                'requires four decks with deck 1 selected')
        require(all(original[f'deck {d} play'] == 'no' for d in range(1, 5)), 'requires stopped decks')
        require(all(original[f'deck {d} loaded'] == 'no' and original[f'deck {d} loop'] == 'no'
                    for d in (3, 4)), 'fixture decks 3/4 must be empty and unlooped')
        masters = [str(d) for d in range(1, 5) if original[f'deck {d} masterdeck'] == 'yes']
        require(len(masters) == 1 and original['masterdeck_auto'] in ('yes', 'no'), 'master not restorable')
        require(all(original[f'deck {d} pfl'] in ('yes', 'no') for d in range(1, 5)), 'PFL not restorable')
        require(all(0 <= float(original[f'deck {d} pitch']) <= 2 for d in (3, 4)), 'pitch not restorable')
        self.original, self.master = original, masters[0]
        self.protected = self.values(PROTECTED)
        self.capture['initial_state'] = {'guards': original, 'protected': self.protected}
        self.ready = True
        write_capture(self.path, self.capture)

    def allowed_writes(self):
        allowed = {f'deck {d} {verb}' for d in (3, 4) for verb in ('play', 'pause', 'unload')}
        allowed |= {f'deck {d} load "{self.audio}"' for d in (3, 4)}
        allowed |= {'masterdeck_auto off', 'masterdeck_auto on', 'deck 1 select'}
        if self.ready:
            allowed |= {f'deck {d} masterdeck on' for d in (self.master, '3', '4')}
            allowed |= {f'deck {d} pfl {v}' for d in range(1, 5) for v in ('on', 'off')}
            allowed |= {f'deck {d} pitch {float(self.original[f"deck {d} pitch"]):.9f}' for d in (3, 4)}
        return allowed

    def write(self, script, purpose):
        require(script in self.allowed_writes(), 'mutation outside fixture allowlist')
        return super().write(script, purpose)

    def wait(self, query, expected, timeout=15):
        end = time.monotonic() + timeout
        while True:
            value = self.channel.query(query)
            if value == expected:
                return value
            require(time.monotonic() < end, 'fixture readback timed out: ' + query)
            time.sleep(.1)

    def verify_protected(self):
        actual = self.values(PROTECTED)
        require(all(equal([actual[q]], [self.protected[q]]) for q in PROTECTED),
                'protected deck state changed; refusing further probes')
        return actual

    def owns_audio(self, deck):
        # Do not persist private media paths if another source replaces the fixture.
        return self.channel.query(f'deck {deck} get_loaded_song "fullpath"') == str(self.audio)

    def restore(self):
        if not self.ready:
            return
        self.capture['summary']['restoration_status'] = 'started'
        write_capture(self.path, self.capture)
        try:
            for deck in ('3', '4'):
                if self.channel.query(f'deck {deck} loaded') == 'yes':
                    require(self.owns_audio(deck), 'foreign media on fixture deck; no unload attempted')
                    if self.channel.query(f'deck {deck} play') == 'yes':
                        self.write(f'deck {deck} pause', 'restore-stop-fixture')
                        self.wait(f'deck {deck} play', 'no')
                    self.write(f'deck {deck} unload', 'restore-unload-fixture')
                    self.wait(f'deck {deck} loaded', 'no')
                pitch = self.original[f'deck {deck} pitch']
                if not equal([self.channel.query(f'deck {deck} pitch')], [pitch]):
                    self.write(f'deck {deck} pitch {float(pitch):.9f}', 'restore-pitch')
            if self.channel.query('get_deck') != '1':
                self.write('deck 1 select', 'restore-selection')
            if self.channel.query(f'deck {self.master} masterdeck') != 'yes':
                self.write(f'deck {self.master} masterdeck on', 'restore-master')
            if self.channel.query('masterdeck_auto') != self.original['masterdeck_auto']:
                self.write('masterdeck_auto ' + {'yes': 'on', 'no': 'off'}[self.original['masterdeck_auto']], 'restore-auto-master')
            for d in range(1, 5):
                q = f'deck {d} pfl'
                if self.channel.query(q) != self.original[q]:
                    self.write(q + ' ' + {'yes': 'on', 'no': 'off'}[self.original[q]], 'restore-pfl')
            actual = self.values(GUARDS)
            require(all(equal([actual[q]], [v]) for q, v in self.original.items()), 'restoration guard mismatch')
            protected = self.verify_protected()
            self.capture['restorations'].append({'guards': actual, 'protected': protected, 'verified': True})
            self.capture['summary'].update(restoration_status='verified', manual_restore_required=False)
        except BaseException as error:
            self.capture['summary'].update(restoration_status='failed', manual_restore_required=True,
                                            restoration_error=repr(error))
            raise
        finally:
            write_capture(self.path, self.capture)

    def observed(self, baseline):
        flags = {q: self.channel.query(q) for q in
                 ['get_deck', 'masterdeck_auto'] + [f'deck {d} {v}' for d in range(1, 5) for v in ('play', 'masterdeck')]}
        self.capture['last_baseline_readback'] = {'expected': baseline, 'observed': flags}
        require(flags['get_deck'] == '1' and flags['masterdeck_auto'] == 'no', 'selection/auto changed')
        require(all(flags[f'deck {d} play'] == ('yes' if str(d) == baseline['playing'] else 'no')
                    and flags[f'deck {d} masterdeck'] == ('yes' if str(d) == baseline['master'] else 'no')
                    for d in range(1, 5)), 'asymmetric master/playback baseline lost')
        self.verify_protected()
        return flags

    def sample(self, baseline, scripts, repeat, round_index):
        phase = {'baseline': baseline, 'round': round_index, 'checks': [], 'reads': {}}
        self.capture['phases'].append(phase)
        try:
            self.verify_protected()
            if self.channel.query('masterdeck_auto') != 'no':
                self.write('masterdeck_auto off', 'fixture-auto-master')
            self.write(f'deck {baseline["master"]} masterdeck on', 'fixture-master')
            deck = baseline['playing']
            self.write(f'deck {deck} load "{self.audio}"', 'fixture-load-silence')
            self.wait(f'deck {deck} loaded', 'yes')
            require(self.owns_audio(deck), 'fixture path did not load')
            self.write(f'deck {deck} play', 'fixture-start')
            self.wait(f'deck {deck} play', 'yes')
            before = float(self.channel.query(f'deck {deck} get_position'))
            until = time.monotonic() + 5
            while True:
                after = float(self.channel.query(f'deck {deck} get_position'))
                if after > before:
                    break
                require(time.monotonic() < until, 'play flag set but position did not advance')
                time.sleep(.1)
            phase['advancing_position'] = [before, after]
            # Starting playback can auto-select its deck. Pin the intended
            # selection AFTER playback, then verify all independent controls.
            if self.channel.query('get_deck') != '1':
                self.write('deck 1 select', 'fixture-selection-after-play')
            if self.channel.query('masterdeck_auto') != 'no':
                self.write('masterdeck_auto off', 'fixture-auto-after-play')
            if self.channel.query(f'deck {baseline["master"]} masterdeck') != 'yes':
                self.write(f'deck {baseline["master"]} masterdeck on', 'fixture-master-after-play')
            for script in scripts:
                phase['checks'].append({'script': script, 'state': self.observed(baseline)})
                self.capture['summary']['pending_query'] = script
                write_capture(self.path, self.capture)
                phase['reads'][script] = [[self.channel.query(script)] for _ in range(repeat)]
            self.observed(baseline)
            phase['complete'] = True
            return phase['reads']
        finally:
            self.restore()


def run_suite(args):
    suite = validate(json.loads(args.grammar_playing.read_text()))
    if args.check or args.dry_run:
        print(json.dumps({'fixture': FIXTURE, 'baselines': BASELINES, 'cases': len(suite['cases']),
                          'preconditions': 'four stopped decks, deck 1 selected, decks 3/4 empty',
                          'audio': 'generated digital silence, independently verified before loading'}, indent=2))
        return 0
    require(args.rounds >= 2 and args.repeat >= 2 and args.out, 'requires repeated passes and capture path')
    audio = silent_audio()
    capture = {'summary': {'mode': 'playing-scope-queries', 'suite': str(args.grammar_playing),
        'suite_sha256': hashlib.sha256(args.grammar_playing.read_bytes()).hexdigest(),
        'repeat': args.repeat, 'rounds_requested': args.rounds, 'rounds_completed': 0, 'status': 'running',
        'claim_scope': 'selector outputs with one silent fixture deck playing and a different master pinned'},
        'fixture': FIXTURE, 'baselines': BASELINES, 'audio': {'path': str(audio),
        'sha256': hashlib.sha256(audio.read_bytes()).hexdigest(), 'digital_silence_verified': True,
        'duration_seconds': 180}, 'cases': [{**c, 'passes': [], 'verdict': 'not-run'} for c in suite['cases']],
        'journal': [], 'phases': [], 'restorations': []}
    channel = OnceChannel()
    session = PlayingSession(channel, capture, args.out, audio)
    try:
        capture['summary'].update(channel.provenance())
        session.snapshot()
        # A complete setup/play/stop/unload/restore round trip before candidates.
        session.sample(BASELINES[0], ['deck 4 get_deck'], args.repeat, 0)
        scripts = list(dict.fromkeys(s for c in suite['cases'] for s in
                    [*c['controls'], *(x['script'] for x in c['contrasts']), c['script']]))
        for r in range(args.rounds):
            batches = {}
            for i in ([0, 1] if r % 2 == 0 else [1, 0]):
                batches[i] = session.sample(BASELINES[i], scripts if r % 2 == 0 else list(reversed(scripts)), args.repeat, r + 1)
            for c in capture['cases']:
                required = [c['script'], *c['controls'], *(x['script'] for x in c['contrasts'])]
                c['passes'].append({s: [batches[i][s] for i in (0, 1)] for s in required})
                c['verdict'] = classify(c)
            capture['summary']['rounds_completed'] = r + 1
            require(channel.query('get_build') == capture['summary']['build'], 'build changed during run')
        capture['summary'].pop('pending_query', None)
        capture['summary']['status'] = 'complete'
    except BaseException as error:
        capture['summary'].update(status='aborted', error=repr(error))
        for case in capture['cases']:
            case['verdict'] = 'incomplete-run'
        raise
    finally:
        capture['summary']['verdicts'] = dict(Counter(c['verdict'] for c in capture['cases']))
        write_capture(args.out, capture)
        channel.close()
    print(json.dumps(capture['summary'], indent=2))
    return 0


def check_capture(path):
    capture = json.loads(Path(path).read_text())
    summary = capture['summary']
    # Captures record the suite repo-relative; resolve it against the repo, not the cwd.
    suite_path = ROOT / summary['suite']
    suite = validate(json.loads(suite_path.read_text()))
    require(hashlib.sha256(suite_path.read_bytes()).hexdigest() == summary['suite_sha256'], 'suite hash mismatch')
    require(summary['channel'] == 'HTTP' and summary['build'].isdecimal(), 'missing build/channel')
    require(summary['status'] in ('complete', 'aborted'), 'unfinished capture')
    require(capture['fixture'] == FIXTURE and capture['baselines'] == BASELINES, 'fixture drift')
    require(capture['audio']['digital_silence_verified'] is True, 'unverified fixture audio')
    complete = summary['status'] == 'complete'
    if 'initial_state' in capture:
        audit = PlayingSession(None, capture, None, Path(capture['audio']['path']))
        audit.original = capture['initial_state']['guards']
        holders = [str(d) for d in range(1, 5) if audit.original[f'deck {d} masterdeck'] == 'yes']
        require(len(holders) == 1, 'initial master not unique')
        audit.master, audit.ready = holders[0], True
        require(all(r['script'] in audit.allowed_writes() for r in capture['journal']), 'journal mutation outside allowlist')
    else:
        require(not capture['journal'], 'mutation before initial snapshot')
    require(len(suite['cases']) == len(capture['cases']), 'missing cases')
    for definition, case in zip(suite['cases'], capture['cases']):
        require(all(case[k] == v for k, v in definition.items()), 'case drift')
        if complete:
            require(len(case['passes']) == summary['rounds_requested'] >= 2, 'missing passes')
            for r, samples in enumerate(case['passes'], 1):
                required = {case['script'], *case['controls'], *(c['script'] for c in case['contrasts'])}
                require(set(samples) == required, 'missing script/control/contrast')
                for script, baselines in samples.items():
                    require(len(baselines) == 2, 'missing baseline')
                    for i, reads in enumerate(baselines):
                        require(len(reads) == summary['repeat'] >= 2, 'missing repeated read')
                        phase = [p for p in capture['phases'] if p['round'] == r and p['baseline'] == BASELINES[i]]
                        require(len(phase) == 1 and phase[0]['reads'][script] == reads, 'phase/case mismatch')
            require(case['verdict'] == classify(case), 'verdict drift')
        else:
            require(case['verdict'] == 'incomplete-run', 'aborted result promoted')
    require(summary['verdicts'] == dict(Counter(c['verdict'] for c in capture['cases'])), 'summary drift')
    if complete:
        require(summary['restoration_status'] == 'verified' and summary['manual_restore_required'] is False, 'restore not verified')
        require(summary['rounds_completed'] == summary['rounds_requested'], 'missing rounds')
        require(capture['phases'][0]['round'] == 0 and capture['phases'][0]['reads'] ==
                {'deck 4 get_deck': [['4']] * summary['repeat']}, 'calibration not established before candidates')
        require(len(capture['phases']) == 1 + 2 * summary['rounds_requested'], 'missing calibration or baseline')
        require(len(capture['restorations']) == len(capture['phases']), 'missing restore')
        require(all(row['status'] == 'response-received' for row in capture['journal']), 'uncertain write in complete run')
        for phase in capture['phases']:
            require(phase['complete'] and phase['advancing_position'][1] > phase['advancing_position'][0], 'playback not independently observed')
            baseline = phase['baseline']
            require(baseline in BASELINES, 'unknown baseline')
            require({c['script'] for c in phase['checks']} == set(phase['reads']), 'missing baseline checks')
            for check in phase['checks']:
                state = check['state']
                require(state['get_deck'] == '1' and state['masterdeck_auto'] == 'no', 'baseline selection/auto mismatch')
                require(all(state[f'deck {d} play'] == ('yes' if str(d) == baseline['playing'] else 'no')
                            and state[f'deck {d} masterdeck'] == ('yes' if str(d) == baseline['master'] else 'no')
                            for d in range(1, 5)), 'baseline not asymmetric')
    if summary.get('restoration_status') == 'verified':
        require(bool(capture['restorations']), 'verified restoration without readbacks')
        for restored in capture['restorations']:
            require(restored['verified'] is True, 'restore flag missing')
            for name in ('guards', 'protected'):
                initial = capture['initial_state'][name]
                require(set(restored[name]) == set(initial) and
                        all(equal([restored[name][q]], [v]) for q, v in initial.items()), 'restore state mismatch')
    manifest_path = ROOT / 'tests/runtime-parser-9246/manifest.json'
    manifest = json.loads(manifest_path.read_text())
    require(manifest['source']['bundle_version'] == '18.0.9246' and
            manifest['source']['architecture'] == 'x86_64', 'wrong historical binary')
    for case in suite['cases']:
        for site in case['binary_sites']:
            name, address = site.rsplit('@', 1)
            symbol = manifest['symbols'][name]
            require(int(symbol['start'], 16) <= int(address, 16) < int(symbol['end_exclusive'], 16), 'site outside symbol')
            require(hashlib.sha256((manifest_path.parent / symbol['file']).read_bytes()).hexdigest() == symbol['asm_sha256'], 'assembly hash mismatch')
    return capture
