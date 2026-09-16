#!/usr/bin/env python3
"""Frozen editor-help predictions; no span/acceptance predictions are implied."""
import json
from pathlib import Path
from runtime_grammar_probes import validate_suite
m=json.loads(Path('tests/runtime-parser-9246/manifest.json').read_text())
rows=[
 ('valid-number','constant 37 & param_add 5','42','param_add'),
 ('malformed-number','constant 37zzqqx & param_add 5','','param_add'),
 ('lowercase-unit','constant 37ms','37ms','constant'),
 ('uppercase-unit','constant 37MS','','constant'),
]
cases=[]
for name,script,expected,help_for in rows:
 cases.append(dict(id='editor-help-'+name,fixture='parser_editor_help',group='editor-help',
  hypothesis='Does the editor show the predicted current-statement help while HTTP returns the independently predicted value?',
  script=script,expected=expected,controls=['zzh4_editor_a','zzh4_editor_b'],
  contrasts=[dict(script='constant 37',expected='37')],
  editor_prediction={'help_for':help_for,'control_help':'none','contrast_help':'constant'},
  binary_sites=[n+'@'+m['symbols'][n]['start'] for n in ['DLGActionWizard::getCurrentWord','DLGActionWizard::onChanged','IAction::stringGetParam']]))
suite=validate_suite({'description':'Paired help-display/HTTP predictions, not an editor token grammar.', 'cases':cases})
Path('tests/runtime-grammar-editor-help-cases.json').write_text(json.dumps(suite,indent=2)+'\n')
