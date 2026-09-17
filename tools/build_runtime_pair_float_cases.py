"""Frozen float-pair consumer predictions; distinct from typed param_add evidence."""
import argparse
import json
from pathlib import Path
from runtime_grammar_probes import validate_suite

OUT = Path('tests/runtime-grammar-pair-float-cases.json')


def build():
    cases = []
    for slot in (0, 1):
        for label, argument, expected, controls in (
            ('integer', '7', '21', ('zzqqx', 'vvnnz')),
            ('decimal', '2.5', '7.5', ('zzqqx', 'vvnnz')),
            ('percent', '25%', '0.75', ('zzqqx', 'vvnnz')),
            ('beats', '7bt', '21', ('zzqqx', 'vvnnz')),
            ('milliseconds', '7ms', '21', ('zzqqx', 'vvnnz')),
            ('raw-action', "'constant 7'", '21', ("'zzqqx'", "'vvnnz'")),
            ('paired', '`constant 7`', '21', ('`zzqqx`', '`vvnnz`')),
            ('computed-decimal', '`constant 2.5`', '7.5', ('`zzqqx`', '`vvnnz`')),
            ('computed-beats', '`constant 7bt`', '21', ('`zzqqx`', '`vvnnz`')),
            ('computed-text', '`constant "7"`', '0', ('`zzqqx`', '`vvnnz`')),
            ('quoted-number', "'7'", '0', ("'zzqqx'", "'vvnnz'")),
            ('unclosed', "'`constant 7'", '0', ("'`zzqqx'", "'`vvnnz'")),
            ('trailing-only', "'constant 7`'", '21', ("'zzqqx`'", "'vvnnz`'")),
            ('long-action', "'constant 7 & param_add 0 & param_add 0'", '21', ("'zzqqx'", "'vvnnz'")),
        ):
            def script(value):
                args = ['3', '3']
                args[slot] = value
                return 'param_multiply ' + ' '.join(args)
            cases.append({
                'id': f'pair-float-{slot+1}-{label}', 'group': 'pair-float',
                'fixture': 'parser_constants',
                'hypothesis': f'Float-pair multiplication with {label} in operand {slot+1} returns {expected}; controls retain operand position and quoting shape.',
                'script': script(argument), 'expected': expected,
                'controls': [script(c) for c in controls],
                'contrasts': [{'script': script('11'), 'expected': '33'}],
                'binary_sites': ['IParamValuesAction::getValues(float*, float*)@0x1009918fc',
                                 'IParamValuesAction::getValues(float*, float*)@0x100991992'],
                'scope': 'Exact HTTP query output only; historical verified param_multiply caller uses the float overload. No native-type, cache reuse, implicit-input, execute or all-consumer claim.'})
    return validate_suite({'description': 'Position-controlled float-pair reader predictions with asymmetric constants and shaped controls.', 'cases': cases})


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', action='store_true')
    args = p.parse_args()
    text = json.dumps(build(), indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == text, 'float-pair predictions changed'
    else:
        OUT.write_text(text)
