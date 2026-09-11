#!/usr/bin/env python3
"""Separate predictions after the selected-scope run; originals stay frozen."""
import json
from pathlib import Path
from runtime_grammar_scopes import validate,FIXTURE

rows=[
 ('master','deck master get_deck',[['1'],['1']],
  'With deck 1 independently observed as master, does master stay on 1 when selection changes?',
  {'deck 1 masterdeck':'yes'},None),
 ('active-observation','deck active get_deck',[['1'],['1']],
  'Does the earlier active-deck observation repeat under the observed master-1 context?',
  {'deck 1 masterdeck':'yes'},'scope-active'),
 ('backtick-observation','deck `constant 2` get_deck',[['error:-2147467259']]*2,
  'Does the earlier computed-prefix error repeat across both selected contexts?',{},'scope-backtick'),
]
cases=[]
for name,script,expected,hypothesis,context,prior in rows:
 c=dict(id='scope-followup-'+name,fixture=FIXTURE,group='scope-followup',script=script,expected=expected,
    hypothesis=hypothesis,required_context=context,controls=['deck zzqqx get_deck','deck vvnnz get_deck'],
    contrasts=[dict(script='deck 3 get_deck',expected=[['3'],['3']])],
    binary_sites=['getDeck@0x10047d9ff','IAction::deckMatch@0x10059978c'])
 m=json.loads(Path('tests/runtime-parser-9246/manifest.json').read_text())
 c['binary_sites']=[label+'@'+m['symbols'][label]['start'] for label in ['getDeck','IAction::deckMatch']]
 if prior:c['prior_case']=prior
 cases.append(c)
Path('tests/runtime-grammar-scope-followup-cases.json').write_text(json.dumps(validate({'cases':cases}),indent=2)+'\n')
