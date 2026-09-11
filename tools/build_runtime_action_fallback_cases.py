#!/usr/bin/env python3
"""Frozen malformed-argument predictions from binary branches, not observations."""
import json
from pathlib import Path
from runtime_grammar_actions import validate

cases=[]
for name,tail,expected,question in [
 ('bare','',[['0.5'],['0.5']], 'Does missing zoom input take its default branch?'),
 ('quoted-default',"'default'",[['0.5'],['0.5']], 'Does quoted default reach the textual zoom default branch?'),
 ('numeric-junk','0.25zzqqx',[['0.5'],['0.5']], 'Does malformed numeric input leave zoom without a parameter and take its default branch?'),
 ('numeric-tab','0.25\t',[['0.5'],['0.5']], 'Does a tab after numeric input prevent that parameter reaching zoom?'),
 ('numeric-newline','0.25\n',[['0.5'],['0.5']], 'Does a newline after numeric input prevent that parameter reaching zoom?'),
 ('uppercase-ms','25MS',[['0.5'],['0.5']], 'Does uppercase MS fail numeric tokenization and reach default behavior?'),
 ('uppercase-bt','25BT',[['0.5'],['0.5']], 'Does uppercase BT fail numeric tokenization and reach default behavior?'),
 ('exponent','1e-1',[['0.5'],['0.5']], 'Does exponent syntax leave no zoom parameter?'),
 ('hex','0x1',[['0.5'],['0.5']], 'Does hexadecimal syntax leave no zoom parameter?'),
 ('punctuation','#zzqqx',[['0.5'],['0.5']], 'Does punctuation before an argument leave zoom on the default branch, unlike ordinary text?'),
 ('separated-percent','25 %',[['0.25'],['0.65']], 'Does separated percent leave an integer first parameter that zoom rejects?'),
 ('no-leading-digit','.25',[['0.25'],['0.65']], 'Does a decimal without leading integer become text and leave zoom unchanged?'),
]:
 cases.append(dict(id='zoom-fallback-'+name,fixture='parser_zoom_levels',group='argument-fallback',
  hypothesis=question,script='zoom'+(' '+tail if tail else ''),expected=expected,
  controls=['zoom zzqqx','zoom vvnnz'], contrasts=[{'script':'zoom 0.0','expected':[['0'],['0']]}],
  binary_sites=['IAction::stringGetParam@0x100599250','ACTION_zoom::onExecute@0x1005c9310']))
suite=validate({'description':'Frozen fallback predictions; no prior live result read by generator.', 'cases':cases})
Path('tests/runtime-grammar-action-fallback-cases.json').write_text(json.dumps(suite,indent=2)+'\n')
