"""Freeze read-only setting comparison tests for a captured getParamEval caller."""
import argparse
import json
from pathlib import Path
from runtime_grammar_probes import validate_suite

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests/runtime-grammar-setting-eval-cases.json'


def build_suite(discrimination=False, types=False):
    prefix = "setting 'videoRandomTransition' "
    rows = [
        ('bare-false', '`off`', 'no', 'Does the evaluated false value differ from the current true setting?'),
        ('single-quoted-false', "'`off`'", 'no', 'Does a single-quoted backtick expression produce the false comparison?'),
        ('double-quoted-false', '"`off`"', 'no', 'Does a double-quoted backtick expression produce the false comparison?'),
        ('quoted-without-final-backtick', "'`off'", 'no', 'Does the outer-quoted argument evaluate without a final backtick?'),
        ('quoted-leading-space', "' `on`'", 'no', 'Does a leading space prevent this argument from comparing equal, unlike the unpadded computed true value?'),
        ('evaluated-zero', '`constant 0`', 'no', 'Does evaluated numeric zero compare unequal to the current true setting?'),
        ('evaluated-text-off', '`constant "off"`', 'no', 'Does evaluated text off compare unequal to the current true setting?'),
        ('evaluated-true', '`on`', 'yes', 'Does the computed true value compare equal, while the literal false contrast does not?'),
    ]
    if discrimination:
        rows = [
            ('computed-equality', '`param_equal 37 37`', 'yes', 'Does a true computed comparison differ from plain nonsense text and the literal false comparison?'),
            ('computed-number-one', '`constant 1`', 'yes', 'Does computed numeric one differ from plain nonsense text and literal false?'),
            ('computed-text-on', '`constant "on"`', 'yes', 'Does computed text on differ from plain nonsense text and literal false?'),
            ('missing-final-backtick-true', "'`param_equal 53 53'", 'yes', 'Does a true computed comparison without its final backtick differ from plain nonsense text and literal false?'),
        ]
    if types:
        rows = [
            ('literal-number-one', '1', 'no', 'Does literal numeric one also compare unequal, like its evaluated counterpart?'),
            ('literal-text-on', "'on'", 'no', 'Does literal quoted text on also compare unequal, like its evaluated counterpart?'),
            ('computed-bool-on', '`constant on`', 'yes', 'Does the computed constant on form compare equal where computed numeric one does not?'),
            ('computed-bool-off', '`constant off`', 'no', 'Does the computed constant off form compare unequal where computed constant on compares equal?'),
        ]
    cases = []
    for name, argument, expected, question in rows:
        cases.append({
            'id': ('setting-eval-types-' if types else 'setting-eval-discrimination-' if discrimination else 'setting-eval-') + name, 'fixture': 'parser_setting_eval',
            'group': 'setting-eval-types' if types else 'setting-eval-discrimination' if discrimination else 'setting-eval', 'hypothesis': question,
            'binary_sites': ['IAction::getParamEval@0x100598552', 'IAction::getParamEval@0x1005986d9'],
            'script': prefix + argument, 'expected': expected,
            'controls': [prefix + "'zzqqx'", prefix + "'vfnrbq'"] if discrimination else [prefix + '`zzqqx`', prefix + '`vfnrbq`'],
            'contrasts': [{'script': prefix + ('off' if expected == 'yes' else 'on'),
                           'expected': 'no' if expected == 'yes' else 'yes'}],
            'scope': 'Read-only HTTP comparison against an existing true setting; no setting writes, no claim of observed machine-code execution or persistent action-cache reuse.',
        })
        if discrimination:
            cases[-1]['contrasts'].append({'script': prefix + '`param_equal 37 83`', 'expected': 'no'})
        if types:
            cases[-1]['controls'] = ([prefix + "'zzqqx'", prefix + "'vfnrbq'"] if expected == 'yes'
                                     else [prefix + '`zzqqx`', prefix + '`vfnrbq`'])
            if expected == 'yes':
                cases[-1]['contrasts'].append({'script': prefix + '`constant 1`', 'expected': 'no'})
            else:
                cases[-1]['contrasts'].append({'script': prefix + '`constant on`', 'expected': 'yes'})
    return validate_suite({'description': 'Generic evaluated-parameter consumer questions, with literal on/off oracles and failed-expression controls.', 'cases': cases})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--discrimination', action='store_true')
    parser.add_argument('--types', action='store_true')
    args = parser.parse_args()
    if args.discrimination:
        OUT = ROOT / 'tests/runtime-grammar-setting-eval-discrimination-cases.json'
    if args.types:
        assert not args.discrimination, 'choose one follow-up suite'
        OUT = ROOT / 'tests/runtime-grammar-setting-eval-types-cases.json'
    data = json.dumps(build_suite(args.discrimination, args.types), indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'frozen setting-eval suite differs from generator'
    else:
        OUT.write_text(data)
