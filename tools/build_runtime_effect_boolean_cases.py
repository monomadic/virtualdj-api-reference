"""Frozen getBoolParam consumer predictions; neither cache reuse nor native types are proved."""
import argparse
import json
from pathlib import Path

OUT = Path('tests/runtime-grammar-effect-boolean-cases.json')
CONFIRMATION = Path('tests/runtime-grammar-effect-boolean-confirmation-cases.json')


def build(confirmation=False):
    signatures = {'on': [['yes'], ['yes']], 'off': [['no'], ['no']],
                  'toggle': [['yes'], ['no']], 'unchanged': [['no'], ['yes']]}
    forms = [
        ('bare', '', 'toggle'), ('toggle', 'toggle', 'toggle'),
        ('integer-positive', '1', 'on'), ('integer-zero', '0', 'off'),
        ('integer-negative', '-1', 'toggle'), ('float-literal', '1.0', 'unchanged'),
        ('percent-literal', '25%', 'unchanged'), ('quoted-on', "'on'", 'unchanged'),
        ('boolean-true', '`on`', 'on'), ('boolean-false', '`off`', 'off'),
        ('computed-positive', '`constant 1`', 'on'), ('computed-zero', '`constant 0`', 'off'),
        ('computed-negative', '`constant -1`', 'toggle'),
        ('computed-float-one', '`constant 1.0`', 'unchanged'),
        ('computed-float-fraction', '`constant 0.25`', 'unchanged'),
        ('quoted-expression', "'`constant 1`'", 'on'),
        ('unclosed-expression', '`constant 1', 'on'),
        ('raw-action-text', "'constant 1'", 'unchanged')]
    if confirmation:
        forms += [('quoted-off', "'off'", 'unchanged'),
                  ('raw-action-zero', "'constant 0'", 'unchanged'),
                  ('unclosed-zero', '`constant 0', 'off')]
    cases = []
    for route, prefix in [('selected', 'deck 1 effect_active 1'),
                          ('named', "deck 1 effect_active 1 'Phaser'")]:
        for label, tail, prediction in forms:
            controls = ['`zzqqx`', '`vvnnz`']
            if confirmation and label in ('quoted-on', 'quoted-off', 'raw-action-text', 'raw-action-zero'):
                controls = ["'zzqqx'", "'vvnnz'"]
            if confirmation and label.startswith('unclosed-'):
                controls = ['`zzqqx', '`vvnnz']
            cases.append({
                'id': f'effect-bool-{route}-{label}', 'group': f'effect-bool-{route}',
                'fixture': 'parser_effect_boolean',
                'hypothesis': f'{route} Phaser effect activation with {label} has the {prediction} signature from off/on baselines; a consumer-specific prediction, not native type or cache coverage.',
                'script': prefix + (' ' + tail if tail else ''),
                'controls': [prefix + ' ' + control for control in controls],
                'expected': signatures[prediction],
                'contrasts': [{'script': prefix + ' on', 'expected': signatures['on']},
                              {'script': prefix + ' off', 'expected': signatures['off']}],
                'binary_sites': ['IAction::getBoolParam@0x1005987e4',
                                 'IAction::getBoolParam@0x10059894e']})
    return {'scope': 'Execute/readback on an already selected Phaser slot with four unloaded stopped decks. Frozen predictions from b9246; actual build recorded at run time. Fresh HTTP requests cannot prove compiled-action cache reuse.' +
                    (' Confirmation adds shape-matched quoted-text and unclosed-expression controls plus opposite-valued forms; initial failed predictions remain unchanged.' if confirmation else ''),
            'cases': cases}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', action='store_true')
    p.add_argument('--confirmation', action='store_true')
    args = p.parse_args()
    output = CONFIRMATION if args.confirmation else OUT
    text = json.dumps(build(args.confirmation), indent=2) + '\n'
    if args.check:
        assert output.read_text() == text, 'effect boolean predictions drifted'
    else:
        output.write_text(text)


if __name__ == '__main__':
    main()
