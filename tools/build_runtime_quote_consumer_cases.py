"""Freeze empty-quote consumer predictions before live measurement."""
import argparse
import json
from pathlib import Path
from runtime_grammar_probes import validate_suite

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests/runtime-grammar-quote-consumer-cases.json'


def build_suite(arity_controls=False):
    cases = []
    for label, marker, yes, no in [('first', 'H4Q', 37, 83), ('second', 'H4R', 53, 91)]:
        for quote_name, q in [('single', "'"), ('double', '"')]:
            empty, word = q + q, q + marker + q
            controls = [f'param_equal {word} {q}{junk}{q} ? constant {yes} : constant {no}'
                        for junk in ('zzqqx', 'vfnrbq')]
            # The asymmetric rows must disagree with the omission contrast;
            # equality of two empty strings by itself could be the bare fallback.
            rows = [
                ('both-empty', f'{empty} {empty}', yes,
                 f'{empty} {word}', no,
                 'Do two empty quoted operands select the equal branch, unlike an empty/nonempty pair?'),
                ('empty-first', f'{empty} {word} {word}', no,
                 f'{word} {word}', yes,
                 'Does an empty first operand change the result relative to omitting that operand?'),
                ('empty-second', f'{word} {empty} {word}', no,
                 f'{word} {word}', yes,
                 'Does an empty second operand change the result relative to omitting that operand?'),
            ]
            if arity_controls:
                rows = [
                    ('triple-equal', f'{word} {word} {word}', yes,
                     f'{word} {empty} {word}', no,
                     'Does a same-length all-nonempty comparison select the equal branch where the empty-middle comparison does not?'),
                    ('empty-tail', f'{word} {word} {empty}', yes,
                     f'{empty} {word} {word}', no,
                     'Does moving the empty operand from first to third change the result while retaining the same argument count?'),
                ]
            for kind, tail, expected, contrast, contrast_value, question in rows:
                cases.append({
                    'id': f'quote-consumer-{label}-{quote_name}-{kind}',
                    'fixture': 'parser_constants', 'group': 'quote-consumer-arity' if arity_controls else 'quote-consumer',
                    'hypothesis': question,
                    'binary_sites': ['IAction::stringGetParam@0x10059957f'],
                    'script': f'param_equal {tail} ? constant {yes} : constant {no}',
                    'expected': str(expected), 'controls': controls,
                    'contrasts': [{'script': f'param_equal {contrast} ? constant {yes} : constant {no}',
                                   'expected': str(contrast_value)}],
                    'scope': ('Exact param_equal query output; same-length contrasts test operand position without changing argument count. Nonsense operands are quoted strings, not claims of unrecognized grammar.' if arity_controls else
                              'Exact param_equal query output; nonsense operands are quoted strings, not claims of unrecognized grammar. The omission contrast is the discriminating test for operand position.'),
                })
    description = ('Same-length comparisons to test the argument-count alternative to empty-operand position.' if arity_controls
                   else 'Empty-quote consumer predictions with positional omission contrasts and two marker/value baselines.')
    return validate_suite({'description': description, 'cases': cases})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--arity-controls', action='store_true')
    args = parser.parse_args()
    if args.arity_controls:
        OUT = ROOT / 'tests/runtime-grammar-quote-consumer-arity-cases.json'
    data = json.dumps(build_suite(args.arity_controls), indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'frozen quote-consumer suite differs from generator'
    else:
        OUT.write_text(data)
