#!/usr/bin/env python3
"""Explicit revised predictions; retains and links the original failed suite."""
import json
from pathlib import Path
from runtime_grammar_actions import validate

source=json.loads(Path('tests/runtime-grammar-action-fallback-cases.json').read_text())
for c in source['cases']:
 c['prior_case']=c['id'];c['id']=c['id'].replace('zoom-fallback-','zoom-default-check-')
 if c['prior_case']!='zoom-fallback-separated-percent':c['expected']=[['0.2'],['0.2']]
 c['hypothesis']='Does the revised expected signature repeat, with bare zoom as an explicit comparison?'
 if c['script']!='zoom':c['contrasts'].append({'script':'zoom','expected':[['0.2'],['0.2']]})
source['description']='Revised predictions after the initial fallback capture; original failures are retained separately.'
Path('tests/runtime-grammar-action-default-cases.json').write_text(json.dumps(validate(source),indent=2)+'\n')
