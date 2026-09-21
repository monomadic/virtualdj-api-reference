#!/usr/bin/env python3
"""Validate and query the recorded conditional-node fixture (no live writes)."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'tests/Skins/schema-condition-probe'
CAPTURE = HERE / 'result-9644.json'
COORDINATES = {'left_x':440, 'right_x':748, 'row_y':[89,159,228,298,368,437,507,577,646]}


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def derive():
    rows=[json.loads(line) for line in (HERE/'run-9644.jsonl').read_text().splitlines()]
    begin=next(r['begin'] for r in rows if 'begin' in r)
    observations=[r['observation'] for r in rows if 'observation' in r]
    if [(o['round'],o['side']) for o in observations]!=[(1,'left'),(1,'right'),(2,'right'),(2,'left')]:
        raise ValueError('missing or reordered observation phases')
    if [r['loaded_round'] for r in rows if 'loaded_round' in r]!=[1,2]:raise ValueError('missing independent loads')
    restores=[r for r in rows if 'restoration' in r]
    if not restores or not restores[-1]['verified']:raise ValueError('restoration not verified')
    restore=restores[-1]
    if restore['restoration']['skin']!=begin['skin_before'] or restore['restoration']['context']!=begin['context_before']:
        raise ValueError('restoration values differ')
    expected_vars={k:v or '0' for k,v in begin['variables_before'].items()}
    if restore['restoration']['variables']!=expected_vars:raise ValueError('probe variable reset differs')
    for name,digest in begin['fixture_hashes'].items():
        if sha(HERE/name)!=digest:raise ValueError('fixture hash mismatch: '+name)
    cases=[]
    for case in json.loads((HERE/'cases.json').read_text()):
        key=f"$schema_condition_{case['id']}"
        runs={str(n):{o['side']:o['values'][key] for o in observations if o['round']==n} for n in (1,2)}
        if runs['1']!=runs['2']:raise ValueError('rounds disagree: '+case['name'])
        expected = ('0','1') if case['name']=='pos-false-first' else ('1','1') if case['name']=='size-false-first' else ('1','0')
        if (runs['1']['left'],runs['1']['right'])!=expected:raise ValueError('hit-area controls did not discriminate: '+case['name'])
        cases.append({'name':case['name'],'id':case['id'],'click_results':runs})
    return {'schema_version':1,'build':begin['build'],'surface':'desktop skin button children',
            'evidence_tier':1,'scope':'Two independent fixture loads in the same app session, with reversed phase and row click order.',
            'fixture_hashes':begin['fixture_hashes'],'journal_sha256':sha(HERE/'run-9644.jsonl'),
            'screenshots':{f'round-{n}.png':sha(HERE/f'round-{n}.png') for n in (1,2)},
            'click_coordinates':COORDINATES,'cases':cases,
            'restoration':{'skin_and_decks_verified':True,'probe_variables_reset':True,
                           'exact_variable_restoration':restore['exact_variable_restoration'],
                           'note':restore['note'],'installed_fixture_removed':any(r.get('fixture_uninstalled') for r in rows)},
            'live_confirmed_attributes':{'/button/pos':['condition'],'/button/size':['condition'],'/button/up':['condition']},
            'limitations':['Observed conditional selection for these literal on/off cases only; not every condition expression or skin surface.',
                           'Position and size conclusions use independent HTTP hit flags after CUA clicks; up-state selection uses retained screenshots.',
                           'This does not establish precedence against outer attributes, dynamic reevaluation without reload, or every XML reader.']}


def pixels():
    from PIL import Image
    out={}
    for n in (1,2):
        with Image.open(HERE/f'round-{n}.png') as image:
            rgb=image.convert('RGB')
            out[str(n)]={'dimensions':list(image.size),'samples':{
                name:{'xy':[440,y],'rgb':list(rgb.getpixel((440,y)))}
                for name,y in [('up-false-first',507),('up-true-first',577),('up-attr-control',646)]}}
    return out


def validate(data, verify_pixels=False):
    expected=derive()
    if {k:v for k,v in data.items() if k!='pixel_samples'}!=expected:raise ValueError('fixture evidence drift')
    if verify_pixels and data['pixel_samples']!=pixels():raise ValueError('screenshot sample drift')
    if set(data['pixel_samples'])!={'1','2'}:raise ValueError('missing screenshot round')
    # The shape-selection evidence must discriminate its controls in both captures.
    for row in data['pixel_samples'].values():
        samples=row['samples']
        if samples['up-false-first']['rgb']!=[32,192,96] or any(samples[n]['rgb']!=[224,48,48] for n in ('up-true-first','up-attr-control')):
            raise ValueError('shape colors do not discriminate the controls')
    return data


def live_summary(build):
    data=validate(json.loads(CAPTURE.read_text()))
    if data['build']!=build:return None
    return {'capture':str(CAPTURE.relative_to(ROOT)),'tier':1,'attributes':data['live_confirmed_attributes'],'scope':data['scope']}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);p.add_argument('--check',action='store_true');p.add_argument('--pixels',action='store_true');a=p.parse_args()
    if a.output:
        data={**derive(),'pixel_samples':pixels()}
        with a.output.open('x') as f:json.dump(data,f,indent=2);f.write('\n')
    else:data=validate(json.loads(CAPTURE.read_text()),a.pixels)
    print(json.dumps({'cases':data['cases'],'live_confirmed_attributes':data['live_confirmed_attributes'],'restoration':data['restoration']},indent=2))
