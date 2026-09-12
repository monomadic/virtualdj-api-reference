"""Deck-scope keywords under an ASYMMETRIC master deck, reached over HTTP.

The earlier selected-scope suites pinned nothing but the selection, so `master`
and `active` returning deck 1 could not be told apart from a constant. This
fixture drives selection and the master deck to DIFFERENT decks in each
baseline, which gives every hypothesis its own signature:

    baselines            (selection, master) = (1, 2) then (2, 3)
    follows master       -> ['2', '3']
    follows selection    -> ['1', '2']
    constant deck 1      -> ['1', '1']
    constant deck 2      -> ['2', '2']

Mutations are literal `deck N select`, `deck N masterdeck on` and
`masterdeck_auto on|off`, every one journaled, restored and independently
verified. Candidate scripts are query-only `get_deck` forms from an allowlist.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from fixtures import FixtureError
from runtime_grammar_actions import GUARDS, OnceChannel, classify, equal
from runtime_grammar_probes import write_capture
from runtime_grammar_scopes import SelectedSession

FIXTURE = 'parser_master_scope'
# (selected deck, master deck). Master never equals the selection, and the
# master differs between baselines, so "follows master" and "constant" split.
BASELINES = [['1', '2'], ['2', '3']]
DECKS = ('1', '2', '3', '4')
SELECTORS = ['1', '2', '3', '4', 'default', 'active', 'master', 'playing',
             'left', 'right', 'leftvideo', 'rightvideo',
             'mixer1', 'mixer2', 'mixer3', 'mixer4', 'zzqqx', 'vvnnz']
ALLOWED = {'get_deck'} | {'deck ' + s + ' get_deck' for s in SELECTORS}
MASTER_QUERIES = [f'deck {d} masterdeck' for d in DECKS]


def require(test, message):
    if not test:
        raise ValueError(message)


def validate(suite):
    seen = set()
    for c in suite['cases']:
        require(c['fixture'] == FIXTURE and c['id'] not in seen, 'fixture or duplicate case')
        seen.add(c['id'])
        require(all(q in GUARDS and isinstance(v, str)
                    for q, v in c.get('required_context', {}).items()), 'invalid context guard')
        require(bool(c.get('hypothesis')) and bool(c.get('binary_sites')), 'missing evidence link')
        require(len(c['controls']) == 2 and len(set(c['controls'])) == 2, 'two controls required')
        require(all(s in ALLOWED for s in [c['script'], *c['controls'],
                    *(x['script'] for x in c['contrasts'])]), 'script outside read-only allowlist')
        require(any(x['expected'] != c['expected'] for x in c['contrasts']), 'no contrasting prediction')
        for expected in [c['expected'], *(x['expected'] for x in c['contrasts'])]:
            require(len(expected) == len(BASELINES) and all(len(x) == 1 for x in expected),
                    'signature dimensions')
    return suite


def separation(capture):
    """Did the script's signature differ from the junk controls' signature?

    A prediction that reproduces the fallback the controls already show is not
    evidence that the keyword was recognized.
    """
    rows = {}
    for c in capture['cases']:
        if not c['passes'] or c['verdict'] == 'incomplete-run':
            rows[c['id']] = 'not-run'
            continue
        p = c['passes'][0]
        script = [reads[0] for reads in p[c['script']]]
        control = [reads[0] for reads in p[c['controls'][0]]]
        rows[c['id']] = 'separates' if script != control else 'matches-controls'
    return rows


class MasterScopeSession(SelectedSession):
    """Selection plus a pinned master deck, both restored and verified."""

    def snapshot(self):
        super().snapshot()
        g = dict(zip(GUARDS, self.guards))
        self.master_auto = g['masterdeck_auto']
        masters = [d for d in DECKS if g[f'deck {d} masterdeck'] == 'yes']
        if len(masters) != 1 or self.master_auto not in ('yes', 'no'):
            raise FixtureError('master deck not uniquely restorable; refusing to mutate')
        self.master = masters[0]
        self.capture['original_master'] = {'deck': self.master, 'auto': self.master_auto}

    def master_now(self):
        flags = [self.channel.query(q) for q in MASTER_QUERIES]
        holders = [d for d, v in zip(DECKS, flags) if v == 'yes']
        if len(holders) != 1 or any(v not in ('yes', 'no') for v in flags):
            raise FixtureError(f'master deck ambiguous: {flags!r}')
        return holders[0]

    def set_master(self, deck):
        # Auto master would compete with the pin, so it is parked for the run.
        if self.channel.query('masterdeck_auto') != 'no':
            self.write('masterdeck_auto off', 'fixture-master-auto')
        if self.master_now() != deck:
            self.write(f'deck {deck} masterdeck on', 'fixture-master')
        actual = self.master_now()
        if actual != deck:
            raise FixtureError(f'master pin did not hold: {actual!r} != {deck!r}')

    def restore_master(self):
        if self.master_now() != self.master:
            self.write(f'deck {self.master} masterdeck on', 'restore-master')
        if self.channel.query('masterdeck_auto') != self.master_auto:
            self.write('masterdeck_auto ' + {'yes': 'on', 'no': 'off'}[self.master_auto],
                       'restore-master-auto')
        # The parent then re-reads every guard, master flags included.

    def restore(self):
        self.capture['summary']['restoration_status'] = 'started'
        write_capture(self.path, self.capture)
        try:
            self.restore_master()
        except BaseException as e:
            self.capture['summary'].update(restoration_status='failed', manual_restore_required=True)
            self.capture.setdefault('restoration_events', []).append(
                {'status': 'failure', 'error': repr(e)})
            write_capture(self.path, self.capture)
            raise
        super().restore()

    def observed(self):
        return [self.channel.query('get_deck'), self.master_now()]

    def sample_queries(self, baseline, scripts, repeat):
        selected, master = baseline
        try:
            if self.channel.query('get_deck') != selected:
                self.write('deck ' + selected + ' select', 'baseline-selection')
            self.set_master(master)
            actual = self.observed()
            if actual != list(baseline):
                raise FixtureError(f'asymmetric baseline did not hold: {actual!r}')
            for q, expected in getattr(self, 'required_context', {}).items():
                observed = self.channel.query(q)
                self.capture.setdefault('context_checks', []).append(
                    {'baseline': baseline, 'script': q, 'expected': expected, 'observed': observed})
                require(observed == expected, 'required context changed after setup: ' + q)
            result = {}
            for script in scripts:
                self.capture['summary']['pending_query'] = {'script': script, 'baseline': baseline}
                self.capture['baseline_checks'].append(
                    {'script': script, 'expected': list(baseline), 'observed': self.observed()})
                if self.capture['baseline_checks'][-1]['observed'] != list(baseline):
                    raise FixtureError('selection or master changed during read-only batch')
                write_capture(self.path, self.capture)
                result[script] = [[self.channel.query(script)] for _ in range(repeat)]
                self.capture.setdefault('query_measurements', []).append(
                    {'script': script, 'baseline': baseline, 'reads': result[script]})
                write_capture(self.path, self.capture)
            return result
        finally:
            self.restore()


def run_suite(args):
    suite = validate(json.loads(args.suite.read_text()))
    if args.dry_run:
        print(json.dumps({'fixture': FIXTURE, 'baselines': BASELINES, 'cases': len(suite['cases']),
                          'mutations': 'deck N select, deck N masterdeck on, masterdeck_auto on|off; '
                                       'all restored and verified'}, indent=2))
        return 0
    require(args.repeat >= 2 and args.rounds >= 2 and args.out, 'requires --repeat 2 --rounds 2 --out')
    capture = {'summary': {
        'mode': 'asymmetric-master-scope-queries', 'suite': str(args.suite),
        'suite_sha256': hashlib.sha256(args.suite.read_bytes()).hexdigest(),
        'rounds_requested': args.rounds, 'rounds_completed': 0, 'repeat': args.repeat,
        'status': 'running',
        'claim_scope': 'exact readbacks with selection and master pinned apart; '
                       'no universal selector claim'},
        'fixture': FIXTURE, 'baselines': BASELINES,
        'cases': [{**c, 'passes': [], 'verdict': 'not-run'} for c in suite['cases']],
        'journal': [], 'baseline_checks': [], 'restorations': []}
    channel = OnceChannel()
    session = MasterScopeSession(channel, capture, args.out)
    try:
        capture['summary'].update(channel.provenance())
        session.snapshot()
        session.required_context = {q: v for c in suite['cases']
                                    for q, v in c.get('required_context', {}).items()}
        for q, expected in session.required_context.items():
            require(channel.query(q) == expected, 'required fixture context failed: ' + q)
        for i in range(args.rounds):
            scripts = list(dict.fromkeys(s for c in suite['cases'] for s in
                           [*c['controls'], *(x['script'] for x in c['contrasts']), c['script']]))
            ordered = scripts if i % 2 == 0 else list(reversed(scripts))
            batches = [session.sample_queries(b, ordered, args.repeat) for b in BASELINES]
            samples = {script: [batch[script] for batch in batches] for script in scripts}
            for c in capture['cases']:
                required = {c['script'], *c['controls'], *(x['script'] for x in c['contrasts'])}
                c['passes'].append({s: samples[s] for s in sorted(required)})
                c['verdict'] = classify(c)
            capture['summary']['rounds_completed'] = i + 1
            write_capture(args.out, capture)
            require(channel.query('get_build') == capture['summary']['build'], 'live build changed')
        session.restore()
        capture['summary'].pop('pending_query', None)
        capture['summary']['status'] = 'complete'
        capture['summary']['separation'] = separation(capture)
    except BaseException as e:
        capture['summary']['status'] = 'aborted'
        capture['summary']['error'] = repr(e)
        for c in capture['cases']:
            c['verdict'] = 'incomplete-run'
        raise
    finally:
        write_capture(args.out, capture)
        channel.close()
    print(json.dumps(capture['summary'], indent=2))
    return 0


def check_capture(path):
    capture = json.loads(Path(path).read_text())
    s = capture['summary']
    p = Path(s['suite'])
    suite = validate(json.loads(p.read_text()))
    require(hashlib.sha256(p.read_bytes()).hexdigest() == s['suite_sha256'], 'suite drift')
    complete = s['status'] == 'complete'
    require(s['status'] in ('complete', 'aborted'), 'unfinished capture')
    require(s['rounds_requested'] >= 2 and 0 <= s['rounds_completed'] <= s['rounds_requested'],
            'invalid rounds')
    if complete:
        require(s['rounds_completed'] == s['rounds_requested'], 'incomplete rounds')
        require(s.get('separation') == separation(capture), 'separation drift')
    require(capture['baselines'] == BASELINES, 'baseline drift')
    # The point of this fixture: selection never equals master, and master moves
    # between baselines, so "follows master" and "constant deck N" cannot agree.
    require(all(selected != master for selected, master in BASELINES), 'baseline is not asymmetric')
    require(len({master for _, master in BASELINES}) == len(BASELINES),
            'master is constant across baselines')
    require(len(capture['cases']) == len(suite['cases']), 'missing cases')
    for spec, c in zip(suite['cases'], capture['cases']):
        require(all(c[k] == v for k, v in spec.items()), 'case drift')
        if complete:
            require(len(c['passes']) == s['rounds_requested'], 'missing passes')
        scripts = {c['script'], *c['controls'], *(x['script'] for x in c['contrasts'])}
        for samples in c['passes']:
            require(set(samples) == scripts, 'missing script')
            for bs in samples.values():
                require(len(bs) == len(BASELINES) and all(len(x) == s['repeat'] >= 2 for x in bs),
                        'missing repeats')
        require(c['verdict'] == (classify(c) if complete else 'incomplete-run'), 'incorrect verdict')
    manifest_path = Path('tests/runtime-parser-9246/manifest.json')
    manifest = json.loads(manifest_path.read_text())
    for spec in suite['cases']:
        for site in spec['binary_sites']:
            name, addr = site.rsplit('@', 1)
            sym = manifest['symbols'][name]
            require(int(sym['start'], 16) <= int(addr, 16) < int(sym['end_exclusive'], 16),
                    'binary bounds')
            require(hashlib.sha256((manifest_path.parent / sym['file']).read_bytes()).hexdigest()
                    == sym['asm_sha256'], 'binary hash')
    required_context = {(q, v) for c in suite['cases']
                        for q, v in c.get('required_context', {}).items()}
    if required_context:
        checked = {(r['script'], r['expected']) for r in capture.get('context_checks', [])
                   if r['expected'] == r['observed']}
        require(required_context <= checked, 'missing required context checks')
        require(all(r['expected'] == r['observed'] for r in capture['context_checks']),
                'failed context')
    require(all(b['expected'] == b['observed'] for b in capture['baseline_checks']), 'failed baseline')
    require(bool(capture.get('original_master')) and
            capture['original_master']['deck'] in DECKS, 'missing master snapshot')
    if complete:
        require(s.get('restoration_status') == 'verified', 'final restoration missing')
    require(s['verdicts'] == dict(Counter(c['verdict'] for c in capture['cases'])), 'summary drift')
    require(bool(capture['restorations']) and all(
        r['verified'] and r['guards'] == list(capture['initial_state']['guards'].values()) and
        equal(r['resources'], list(capture['initial_state']['resources'].values()))
        for r in capture['restorations']), 'missing or failed restoration')
    if complete:
        require(bool(capture.get('restoration_events')) and
                capture['restoration_events'][-1]['status'] == 'success',
                'missing final restoration event')
    if s.get('restoration_status') == 'failed':
        require(s.get('manual_restore_required'), 'failed restoration missing marker')
    require(s['build'].isdecimal() and s['channel'] == 'HTTP', 'missing live provenance')
    if complete:
        require(all(j['status'] == 'response-received' for j in capture['journal']), 'uncertain write')
    return capture


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--artifact', type=Path, default=Path('tests/runtime-grammar-master-9598.json'))
    p.add_argument('--suite', type=Path, default=Path('tests/runtime-grammar-master-cases.json'))
    p.add_argument('--run', action='store_true')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--out', type=Path)
    p.add_argument('--repeat', type=int, default=2)
    p.add_argument('--rounds', type=int, default=2)
    p.add_argument('--check', action='store_true')
    a = p.parse_args()
    if a.run or a.dry_run:
        raise SystemExit(run_suite(a))
    c = check_capture(a.artifact) if a.check else json.loads(a.artifact.read_text())
    print(json.dumps(c['summary'], indent=2))
