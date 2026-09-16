#!/usr/bin/env python3
"""Frozen editor-help predictions; no span/acceptance predictions are implied."""
import argparse
import json
from pathlib import Path
from runtime_grammar_probes import validate_suite

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests/runtime-grammar-editor-help-cases.json'
MANIFEST = ROOT / 'tests/runtime-parser-9246/manifest.json'

ROWS = [
    ('valid-number', 'constant 37 & param_add 5', '42', 'param_add'),
    ('malformed-number', 'constant 37zzqqx & param_add 5', '', 'param_add'),
    ('lowercase-unit', 'constant 37ms', '37ms', 'constant'),
    ('uppercase-unit', 'constant 37MS', '', 'constant'),
]
SYMBOLS = ['DLGActionWizard::getCurrentWord', 'DLGActionWizard::onChanged', 'IAction::stringGetParam']


def build_suite():
    manifest = json.loads(MANIFEST.read_text())
    sites = [n + '@' + manifest['symbols'][n]['start'] for n in SYMBOLS]
    cases = []
    for name, script, expected, help_for in ROWS:
        cases.append({
            'id': 'editor-help-' + name, 'fixture': 'parser_editor_help', 'group': 'editor-help',
            'hypothesis': 'Does the editor show the predicted current-statement help while HTTP returns the independently predicted value?',
            'script': script, 'expected': expected, 'controls': ['zzh4_editor_a', 'zzh4_editor_b'],
            'contrasts': [{'script': 'constant 37', 'expected': '37'}],
            'editor_prediction': {'help_for': help_for, 'control_help': 'none', 'contrast_help': 'constant'},
            'binary_sites': sites,
        })
    return validate_suite({'description': 'Paired help-display/HTTP predictions, not an editor token grammar.', 'cases': cases})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.dumps(build_suite(), indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'frozen editor-help suite differs from generator'
    else:
        OUT.write_text(data)
