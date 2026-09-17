"""Frozen incoming getParam predictions with independent zoom state readback."""
import argparse
import json
from pathlib import Path
from runtime_grammar_actions import validate

OUT = Path('tests/runtime-grammar-incoming-action-cases.json')
PIPELINE_OUT = Path('tests/runtime-grammar-incoming-pipeline-cases.json')
BOUNDED_OUT = Path('tests/runtime-grammar-incoming-pipeline-bounded-cases.json')
FRESH_OUT = Path('tests/runtime-grammar-incoming-pipeline-fresh-cases.json')
CONFIRMATION_OUT = Path('tests/runtime-grammar-incoming-pipeline-confirmation-cases.json')


def build(pipeline=False, bounded=False, fresh=False, confirmation=False):
    cases = []
    for source in (('0.41', '0.79') if fresh else ('0.37', '0.83')):
        prefix = f'constant {source}' + (' & param_cast float' if pipeline else '') + ' & zoom'
        for label, tail, expected in (
                ('omitted', '', [[source], [source]]),
                ('explicit', '0.25', [['0.25'], ['0.25']]),
                ('explicit-zero', '0.0', [['0.0'], ['0.0']]),
                ('explicit-relative', '+0.25', [['0.5'], ['0.9']]),
                ('default', 'default', [[source], [source]])):
            if bounded and label == 'default':
                continue  # Exclude the uncertain write; do not replay it.
            cases.append({
                'id': f'incoming-zoom-{source}-{label}', 'group': 'incoming-zoom',
                'fixture': 'parser_zoom_levels',
                'script': prefix + (' ' + tail if tail else ''),
                'controls': [prefix + ' ' + t for t in ('zzqqx', 'vvnnz')],
                'expected': expected,
                'contrasts': [
                    {'script': prefix + ' 0.25', 'expected': [['0.25'], ['0.25']]},
                    {'script': prefix + ' 0.0', 'expected': [['0.0'], ['0.0']]}],
                'hypothesis': f'With incoming decimal {source}, {label} selects the frozen zoom signature from two independent baselines; explicit overrides must discriminate source propagation.',
                'binary_sites': ['ACTION_zoom::onExecute@0x1005c931c',
                                 'IAction::getParam@0x100596c6d',
                                 'IAction::execute@0x100596111']})
            if confirmation:
                cases[-1]['contrasts'].append({
                    'script': f'constant {source} & zoom',
                    'expected': [['0.2'], ['0.2']]})
    return validate({'scope': 'Historical b9246 incoming-parameter route tested through HTTP execute and independent zoom readback on the recorded live build. No native type, second incoming slot, flag-bit or instruction coverage claim.', 'cases': cases})


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', action='store_true')
    p.add_argument('--pipeline', action='store_true')
    p.add_argument('--bounded', action='store_true')
    p.add_argument('--fresh', action='store_true')
    p.add_argument('--confirmation', action='store_true')
    args = p.parse_args()
    fresh = args.fresh or args.confirmation
    output = CONFIRMATION_OUT if args.confirmation else FRESH_OUT if fresh else BOUNDED_OUT if args.bounded else PIPELINE_OUT if args.pipeline else OUT
    text = json.dumps(build(args.pipeline or args.bounded or fresh,
                           args.bounded or fresh, fresh, args.confirmation), indent=2) + '\n'
    if args.check:
        assert output.read_text() == text, 'incoming action predictions drifted'
    else:
        output.write_text(text)
