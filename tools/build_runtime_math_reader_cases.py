"""Frozen two-operand arithmetic-reader questions; no generic-evaluator claims."""
import argparse
import json
from pathlib import Path
from runtime_grammar_probes import validate_suite

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests/runtime-grammar-math-reader-cases.json'


def build_suite():
    cases = []
    for marker, numbers in [('first', (37, 5)), ('second', (53, 9))]:
        for slot in (0, 1):
            value, other = numbers[slot], numbers[1 - slot]
            variants = [
                ('raw-action-text', f"'constant {value}'", sum(numbers), 'Can a quoted action string without backticks supply this operand?'),
                ('paired-backticks', f'`constant {value}`', sum(numbers), 'Does a paired backtick expression supply this operand?'),
                ('missing-final-backtick', f"'`constant {value}'", other, 'Does an outer-quoted expression missing its final backtick contribute zero instead of its numeric value?'),
                ('trailing-backtick-only', f"'constant {value}`'", sum(numbers), 'Does action text with only a trailing backtick retain the numeric value?'),
                ('leading-space', f"' `constant {value}`'", other, 'Does a leading space before paired backticks prevent the numeric contribution?'),
                ('quoted-number', f"'{value}'", other, 'Does quoted numeric text contribute zero instead of being coerced into a number?'),
                ('computed-text', f'`constant "{value}"`', str(numbers[1]) + str(numbers[0]), 'Does computed numeric text yield second-then-first text concatenation instead of arithmetic addition?'),
                ('direct-beats', f'{value}bt', sum(numbers), 'Does a direct beat-valued operand contribute its numeric magnitude?'),
                ('computed-beats', f'`constant {value}bt`', sum(numbers), 'Does an evaluated beat-valued operand contribute its numeric magnitude?'),
                ('long-action-text', f"'constant {value} & param_add 0 & param_add 0'", sum(numbers), 'Does longer quoted action text without backticks contribute its computed value?'),
                ('long-paired-backticks', f'`constant {value} & param_add 0 & param_add 0`', sum(numbers), 'Does the longer paired-backtick expression contribute its computed value?'),
            ]
            def script(arg):
                operands = [str(n) for n in numbers]
                operands[slot] = arg
                return 'param_add ' + ' '.join(operands)
            for name, argument, expected, question in variants:
                cases.append({
                    'id': f'math-reader-{marker}-operand-{slot + 1}-{name}',
                    'fixture': 'parser_constants', 'group': 'math-reader',
                    'hypothesis': question,
                    'binary_sites': ['IParamValuesAction::getValues(SActionParam*, SActionParam*)@0x100992ec3',
                                     'IParamValuesAction::getValues(SActionParam*, SActionParam*)@0x1009930af',
                                     'ACTION_param_add::onQuery@0x100992a83'],
                    'script': script(argument), 'expected': str(expected),
                    'controls': [script("'" + junk + "'") for junk in ('zzqqx', 'vfnrbq')],
                    'contrasts': [{'script': f'param_add {numbers[0]} {numbers[1] + 1}',
                                   'expected': str(sum(numbers) + 1)}],
                    'scope': 'Exact HTTP output in the read-only constant fixture. Operand-specific nonsense controls preserve arity. Does not establish instruction execution, cache reuse, implicit input or every arithmetic verb.',
                })
    return validate_suite({'description': 'Position-controlled arithmetic reader predictions with asymmetric constants.', 'cases': cases})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.dumps(build_suite(), indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'frozen math-reader suite differs from generator'
    else:
        OUT.write_text(data)
