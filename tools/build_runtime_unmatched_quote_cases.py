"""Frozen quote-termination questions with a numeric prefix and chain readback."""
import argparse
import json
from pathlib import Path
from runtime_grammar_probes import validate_suite

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests/runtime-grammar-unmatched-quote-cases.json'


def build_suite():
    cases = []
    for baseline, value, increment, marker in [('first', 37, 5, 'H4Q'), ('second', 53, 9, 'H4R')]:
        for name, q, other in [('single', "'", '"'), ('double', '"', "'")]:
            controls = [f'constant {value} {q}{junk}{q} & param_add {increment}'
                        for junk in ('zzqqx', 'vfnrbq')]
            closed = f'constant {value} {q}{marker}{q} & param_add {increment}'
            rows = [
                ('open-only', f'constant {value} {q} & param_add {increment}', value,
                 'Does an unmatched opening quote leave the numeric prefix unchanged instead of applying the following addition?'),
                ('open-word', f'constant {value} {q}{marker} & param_add {increment}', value,
                 'Does an unmatched quoted word leave the numeric prefix unchanged, unlike the matched-quote contrast?'),
                ('opposite-closer', f'constant {value} {q}{marker}{other} & param_add {increment}', value,
                 'Does the opposite quote still leave the numeric prefix unchanged rather than restoring the following addition?'),
                ('late-matching-closer', f'constant {value} {q}{marker} & param_add {increment}{q} & param_add {increment * 2}', value + increment * 2,
                 'Does a matching quote after the inner addition allow only the outer addition to determine this result?'),
            ]
            for kind, script, expected, question in rows:
                cases.append({
                    'id': f'unmatched-quote-{baseline}-{name}-{kind}',
                    'fixture': 'parser_constants', 'group': 'unmatched-quote-chain',
                    'hypothesis': question,
                    'binary_sites': ['IAction::stringGetParam@0x10059958d'],
                    'script': script, 'expected': str(expected), 'controls': controls,
                    'contrasts': [{'script': closed, 'expected': str(value + increment)}],
                    'scope': 'Exact constant/param_add HTTP output with a parsed numeric prefix. Quoted nonsense-value controls have matching delimiters. No claim about internal cursor position, discarded argument representation, or every consumer.',
                })
    return validate_suite({'description': 'Unmatched and matching quote predictions separated by a chain result, not blank-value equality.', 'cases': cases})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.dumps(build_suite(), indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'frozen unmatched-quote suite differs from generator'
    else:
        OUT.write_text(data)
