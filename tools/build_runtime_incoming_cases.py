"""Frozen incoming-parameter predictions for the captured constant/getParam route."""
import argparse
import json
from pathlib import Path
from runtime_grammar_probes import validate_suite

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests/runtime-grammar-incoming-cases.json'


def build_suite():
    cases = []
    sites = ['ACTION_constant::onQuery@0x100990c36', 'IAction::getParam@0x100596c6d',
             'IAction::query@0x10059650d', 'IAction::query@0x1005966e0']
    def add(label, script, expected, controls, contrasts, question):
        cases.append({'id': 'incoming-' + label, 'group': 'incoming-constant',
                      'fixture': 'parser_constants', 'binary_sites': sites,
                      'hypothesis': question, 'script': script, 'expected': expected,
                      'controls': controls,
                      'contrasts': [{'script': s, 'expected': v} for s,v in contrasts],
                      'scope': 'Exact HTTP query-chain output only. Historical buffer/reader associations are Tier 2; no live branch, flag-bit, execute-input or native-type proof.'})
    for seed in (37, 83):
        prefix = f'constant {seed} & constant'
        controls = [prefix + ' ' + token for token in ('zzqqx', 'vvnnz')]
        for label, tail, expected in [('omitted', '', str(seed)),
                                      ('explicit', '9', '9'), ('zero', '0', '0'),
                                      ('negative', '-7', '-7'), ('decimal', '0.25', '0.25'),
                                      ('default', 'default', str(seed)),
                                      ('empty-text', "''", ''), ('malformed-number', '9zzqqx', '')]:
            add(f'{seed}-{label}', prefix + (' ' + tail if tail else ''), expected,
                controls, [(prefix + ' 11', '11')],
                f'Does constant after incoming {seed}, with {label} operand, return {expected!r}?')
        add(f'{seed}-downstream', prefix + ' & param_add 5', str(seed + 5),
            [c + ' & param_add 5' for c in controls],
            [(prefix + ' 9 & param_add 5', '14')],
            'Does a later arithmetic consumer observe the omitted-operand result?')
    for label, literal, expected in [('zero', '0', '0'), ('negative', '-7', '-7'),
                                     ('decimal', '0.25', '0.25'), ('percent', '37%', '37%'),
                                     ('milliseconds', '37ms', '37ms'), ('beats', '37bt', '37bt'),
                                     ('text', "'incoming_sentinel'", 'incoming_sentinel')]:
        prefix = f'constant {literal} & constant'
        add(f'typed-{label}', prefix, expected,
            [prefix + ' ' + token for token in ('zzqqx', 'vvnnz')],
            [(prefix + ' 11', '11')],
            'Does omitting the final constant operand preserve the source observable, including its displayed unit/text?')
    add('no-source', 'constant', '', ['constant zzqqx', 'constant vvnnz'],
        [('constant 11', '11')], 'Does an omitted operand without a source remain blank?')
    add('replacement-chain', 'constant 37 & constant 83 & constant', '83',
        ['constant 37 & constant 83 & constant ' + t for t in ('zzqqx', 'vvnnz')],
        [('constant 83 & constant 37 & constant', '37')],
        'Does the nearest explicit replacement, rather than the first source, supply the final omitted operand?')
    return validate_suite({'description': 'Read-only incoming constant/getParam comparisons. Predictions frozen before live measurement.', 'cases': cases})


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', action='store_true')
    args = p.parse_args()
    text = json.dumps(build_suite(), indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == text, 'incoming predictions drifted'
    else:
        OUT.write_text(text)
