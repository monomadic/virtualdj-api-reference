"""Selected-deck grammar hypotheses with reversible selection and PFL guards.

This mode only executes literal deck 1..4 select for fixture setup/restoration.
Candidate scripts are query-only get_deck forms from an explicit allowlist.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from fixtures import FixtureError
from runtime_grammar_actions import Session, OnceChannel, classify, GUARDS, equal
from runtime_grammar_probes import write_capture

FIXTURE = 'parser_selected_scope'
BASELINES = [['1'], ['2']]
SELECTORS = ['1', '2', '3', '4', '99', '0', '-1', 'default', 'active', 'left', 'right',
             'master', 'playing', 'leftvideo', 'rightvideo', 'mixer1', 'mixer2', 'mixer3', 'mixer4',
             'zzqqx', 'vvnnz', '"2"', "'2'", '`constant 2`', "'`constant 2`'", '2zzqqx', '2.0']
ALLOWED = {'get_deck'} | {prefix + ' ' + selector + ' get_deck'
                         for prefix in ('deck', 'zone') for selector in SELECTORS}


def require(test, message):
    if not test: raise ValueError(message)


def validate(suite):
    seen = set()
    for c in suite['cases']:
        require(c['fixture'] == FIXTURE and c['id'] not in seen, 'fixture or duplicate case')
        seen.add(c['id'])
        require(all(q in GUARDS and isinstance(v,str) for q,v in c.get('required_context',{}).items()), 'invalid context guard')
        require(bool(c.get('hypothesis')) and bool(c.get('binary_sites')), 'missing evidence link')
        require(len(c['controls']) == 2 and len(set(c['controls'])) == 2, 'two controls required')
        require(all(s in ALLOWED for s in [c['script'], *c['controls'],
                    *(x['script'] for x in c['contrasts'])]), 'script outside read-only allowlist')
        require(any(x['expected'] != c['expected'] for x in c['contrasts']), 'no contrasting prediction')
        for expected in [c['expected'], *(x['expected'] for x in c['contrasts'])]:
            require(len(expected) == 2 and all(len(x) == 1 for x in expected), 'signature dimensions')
    return suite


class SelectedSession(Session):
    def snapshot(self):
        super().snapshot()
        self.selected = self.channel.query('get_deck')
        if self.selected not in ('1','2','3','4'):
            raise FixtureError('selection not independently restorable')
        self.capture['original_selection'] = self.selected

    def restore(self):
        self.capture["summary"]["restoration_status"] = "started"
        write_capture(self.path, self.capture)
        try:
            self.restore_selection()
            super().restore()
        except BaseException as e:
            self.capture["summary"].update(restoration_status="failed", manual_restore_required=True)
            self.capture.setdefault("restoration_events", []).append({"status":"failure", "error":repr(e)})
            write_capture(self.path,self.capture)
            raise

    def restore_selection(self):
        if self.channel.query('get_deck') != self.selected:
            self.write('deck ' + self.selected + ' select', 'restore-selection')
        # Parent restoration independently checks select/PFL/master/transport.

    def sample_query(self, baseline, script, repeat):
        return self.sample_queries(baseline, [script], repeat)[script]

    def sample_queries(self, baseline, scripts, repeat):
        try:
            if self.channel.query('get_deck') != baseline[0]:
                self.write('deck ' + baseline[0] + ' select', 'baseline-selection')
            actual = [self.channel.query('get_deck')]
            if actual != baseline:
                raise FixtureError(f'selection baseline did not hold: {actual}')
            for q, expected in getattr(self,'required_context',{}).items():
                observed=self.channel.query(q)
                self.capture.setdefault('context_checks',[]).append(
                    {'baseline':baseline,'script':q,'expected':expected,'observed':observed})
                require(observed==expected,'required context changed after selection: '+q)
            result = {}
            for script in scripts:
                self.capture['summary']['pending_query'] = {'script': script, 'baseline': baseline}
                self.capture['baseline_checks'].append({'script': script, 'expected': baseline,
                    'observed': [self.channel.query('get_deck')]})
                if self.capture['baseline_checks'][-1]['observed'] != baseline:
                    raise FixtureError('selection changed during read-only batch')
                write_capture(self.path,self.capture)
                result[script] = [[self.channel.query(script)] for _ in range(repeat)]
                self.capture.setdefault('query_measurements', []).append(
                    {'script': script, 'baseline': baseline, 'reads': result[script]})
                write_capture(self.path,self.capture)
            return result
        finally:
            self.restore()


def run_suite(args):
    suite = validate(json.loads(args.grammar_scopes.read_text()))
    if args.check or args.dry_run:
        print(json.dumps({'fixture': FIXTURE, 'baselines': BASELINES, 'cases': len(suite['cases']),
                          'mutations': 'deck 1..4 select only; restores selection and verifies PFL'},indent=2))
        return 0
    require(args.repeat >= 2 and args.rounds >= 2 and args.out, 'requires --repeat 2 --rounds 2 --out')
    capture = {'summary': {'mode': 'selected-scope-queries', 'suite':str(args.grammar_scopes),
        'suite_sha256':hashlib.sha256(args.grammar_scopes.read_bytes()).hexdigest(),
        'rounds_requested':args.rounds,'rounds_completed':0,'repeat':args.repeat,'status':'running',
        'claim_scope':'exact readbacks in selected-deck fixture; no universal selector claim'},
        'fixture':FIXTURE,'baselines':BASELINES,
        'cases':[{**c,'passes':[],'verdict':'not-run'} for c in suite['cases']],
        'journal':[],'baseline_checks':[],'restorations':[]}
    channel = OnceChannel()
    session = SelectedSession(channel,capture,args.out)
    try:
        capture['summary'].update(channel.provenance())
        session.snapshot()
        session.required_context={q:v for c in suite['cases'] for q,v in c.get('required_context',{}).items()}
        for q, expected in session.required_context.items():
            require(channel.query(q)==expected, 'required fixture context failed: '+q)
        for baseline in BASELINES:
            session.sample_query(baseline,'get_deck',args.repeat)
        for i in range(args.rounds):
            # Query-only scripts share each selected baseline. Check selection
            # before every query, restore after the batch, reverse the next pass.
            scripts = list(dict.fromkeys(s for c in suite['cases'] for s in
                [*c['controls'], *(x['script'] for x in c['contrasts']), c['script']]))
            ordered = scripts if i % 2 == 0 else list(reversed(scripts))
            batches = [session.sample_queries(b, ordered, args.repeat) for b in BASELINES]
            samples = {script: [batch[script] for batch in batches] for script in scripts}
            for c in capture['cases']:
                required={c['script'],*c['controls'],*(x['script'] for x in c['contrasts'])}
                c['passes'].append({s:samples[s] for s in sorted(required)})
                c['verdict']=classify(c)
            capture['summary']['rounds_completed']=i+1
            write_capture(args.out,capture)
            require(channel.query('get_build') == capture['summary']['build'],'live build changed')
        session.restore()
        capture['summary'].pop('pending_query',None)
        capture['summary']['status']='complete'
    except BaseException as e:
        capture['summary']['status']='aborted'
        capture['summary']['error']=repr(e)
        for c in capture['cases']: c['verdict']='incomplete-run'
        raise
    finally:
        write_capture(args.out,capture)
        channel.close()
    print(json.dumps(capture['summary'],indent=2))
    return 0


def check_capture(path):
    capture=json.loads(path.read_text()); s=capture['summary']
    p=Path(s['suite']); suite=validate(json.loads(p.read_text()))
    require(hashlib.sha256(p.read_bytes()).hexdigest()==s['suite_sha256'],'suite drift')
    complete=s['status']=='complete'
    require(s['status'] in ('complete','aborted'),'unfinished capture')
    require(s['rounds_requested']>=2 and 0<=s['rounds_completed']<=s['rounds_requested'],'invalid rounds')
    if complete: require(s['rounds_completed']==s['rounds_requested'],'incomplete rounds')
    require(len(capture['cases'])==len(suite['cases']),'missing cases')
    for spec,c in zip(suite['cases'],capture['cases']):
        require(all(c[k]==v for k,v in spec.items()),'case drift')
        if complete: require(len(c['passes'])==s['rounds_requested'],'missing passes')
        scripts={c['script'],*c['controls'],*(x['script'] for x in c['contrasts'])}
        for samples in c['passes']:
            require(set(samples)==scripts,'missing script')
            for bs in samples.values():
                require(len(bs)==2 and all(len(x)==s['repeat']>=2 for x in bs),'missing repeats')
        require(c['verdict']==(classify(c) if complete else 'incomplete-run'),'incorrect verdict')
    manifest_path=Path('tests/runtime-parser-9246/manifest.json')
    manifest=json.loads(manifest_path.read_text())
    for spec in suite['cases']:
        for site in spec['binary_sites']:
            name,addr=site.rsplit('@',1); sym=manifest['symbols'][name]
            require(int(sym['start'],16)<=int(addr,16)<int(sym['end_exclusive'],16),'binary bounds')
            require(hashlib.sha256((manifest_path.parent/sym['file']).read_bytes()).hexdigest()==sym['asm_sha256'],'binary hash')
    required_context={(q,v) for c in suite['cases'] for q,v in c.get('required_context',{}).items()}
    if required_context:
        checked={(r['script'],r['expected']) for r in capture.get('context_checks',[]) if r['expected']==r['observed']}
        require(required_context <= checked,'missing required context checks')
        require(all(r['expected']==r['observed'] for r in capture['context_checks']),'failed context')
    require(all(b['expected']==b['observed'] for b in capture['baseline_checks']),'failed baseline')
    if complete: require(s.get('restoration_status')=='verified','final restoration missing')
    require(s['verdicts']==dict(Counter(c['verdict'] for c in capture['cases'])),'summary drift')
    require(bool(capture['restorations']) and all(r['verified'] and
        r['guards']==list(capture['initial_state']['guards'].values()) and
        equal(r['resources'],list(capture['initial_state']['resources'].values())) for r in capture['restorations']),
        'missing or failed restoration')
    if complete:
        require(bool(capture.get('restoration_events')) and capture['restoration_events'][-1]['status']=='success','missing final restoration event')
    if s.get('restoration_status')=='failed': require(s.get('manual_restore_required'), 'failed restoration missing marker')
    require(s['build'].isdecimal() and s['channel']=='HTTP','missing live provenance')
    if complete: require(all(j['status']=='response-received' for j in capture['journal']),'uncertain write')
    return capture


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--artifact',type=Path,default=Path('tests/runtime-grammar-scopes-9598.json'))
    p.add_argument('--check',action='store_true')
    a=p.parse_args()
    c=check_capture(a.artifact) if a.check else json.loads(a.artifact.read_text())
    print(json.dumps(c['summary'],indent=2))
