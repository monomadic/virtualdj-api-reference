#!/usr/bin/env python3
"""Untrimmed-output quote predictions. Separate from historical trimmed captures."""
import json
from pathlib import Path
from runtime_grammar_probes import validate_suite

cases=[]
for name,script,expected in [
 ('single-leading',"constant ' A'",' A'),('single-trailing',"constant 'A '",'A '),
 ('single-spaces',"constant '  '",'  '),('double-both','constant " A "',' A '),
 ('tab-only',"constant '\t'",'\t'),('newline-only',"constant '\n'",'\n'),
 ('cr-only',"constant '\r'",'\r'),('get-text-spaces',"get_text ' A '",' A '),
 ('get-text-escaped-newline',"get_text '\\n'",'\r\n'),
 ('constant-literal-slash-n',"constant '\\n'",'\\n'),
]:
 cases.append(dict(id='raw-quote-'+name,fixture='parser_constants',group='untrimmed-quotes',
  hypothesis='Does this exact quoted input preserve the predicted boundary bytes in the raw HTTP body?',
  script=script,expected=expected,controls=['constant zzqqx','constant vvnnz'],
  contrasts=[{'script':"constant 'A'",'expected':'A'}],
  binary_sites=['IAction::stringGetParam@0x100599250']))
# Controls must be unrelated but have the same independent output.
for c in cases: c['controls']=['constant 83 zzqqx','constant 83 vvnnz']
suite=validate_suite(dict(description='Frozen predictions requiring untrimmed HTTP response bodies.',cases=cases))
Path('tests/runtime-grammar-whitespace-cases.json').write_text(json.dumps(suite,indent=2)+'\n')
