"""Frozen floating-evaluator predictions against pre-candidate binary literals."""
import argparse
import hashlib
import json
from pathlib import Path
from runtime_grammar_probes import validate_suite

ROOT = Path(__file__).resolve().parents[1]
CALIBRATION = ROOT / 'tests/runtime-grammar-display-float-calibration-9598.json'
OUT = ROOT / 'tests/runtime-grammar-display-float-cases.json'


def build_suite():
    calibration = json.loads(CALIBRATION.read_text())
    values = {}
    for key, row in calibration['literals'].items():
        assert len(row['samples']) >= 3 and len(set(row['samples'])) == 1
        values[key] = row['samples'][0]
    assert len(set(values.values())) == 3
    prefix = "deck 3 get_pioneer_display 'cuepoints' 'rx3' "
    rows = [
        ('computed-integer', '`constant 2`', '2', 'Does a computed integer match the literal-2 binary frame?'),
        ('single-quoted', "'`constant 2`'", '2', 'Does a single-quoted computed argument match literal 2?'),
        ('double-quoted', '"`constant 2`"', '2', 'Does a double-quoted computed argument match literal 2?'),
        ('missing-final-backtick', "'`constant 2'", '2', 'Does the outer-quoted form without its final backtick match literal 2?'),
        ('leading-space', "' `constant 2`'", '0', 'Does leading space in the quoted argument match literal 0 rather than literal 2?'),
        ('computed-float', '`constant 2.0`', '2', 'Does a computed float match the literal-2 binary frame?'),
        ('computed-percent', '`constant 200%`', '2', 'Does computed 200 percent match literal 2?'),
        ('computed-ms', '`constant 2ms`', '2', 'Does a computed 2ms argument match literal 2 in this consumer?'),
        ('computed-bool', '`on`', '1', 'Does computed on match literal 1?'),
        ('computed-text', '`constant "2"`', '2', 'Does computed text 2 match literal 2?'),
        ('relative-zero-baseline', '`constant +2`', '2', 'Does computed signed 2 match literal 2 with this zero-initialized consumer input?'),
    ]
    cases = []
    for name, argument, literal, question in rows:
        other = '1' if literal == '2' else '2'
        cases.append({
            'id': 'display-float-' + name, 'fixture': 'parser_display_float',
            'group': 'display-float', 'hypothesis': question,
            'binary_sites': ['IAction::getFloatParamEval@0x100596d13', 'IAction::getFloatParamEval@0x100596ecb'],
            'script': prefix + argument, 'response_encoding': 'hex', 'expected': values[literal],
            'controls': [prefix + '`zzqqx`', prefix + '`vfnrbq`'],
            'contrasts': [{'script': prefix + other, 'expected': values[other]},
                          {'script': prefix + literal, 'expected': values[literal]}],
            'literal_equivalence': literal,
            'scope': 'Exact binary HTTP response in the calibrated empty-deck/current-mapping context; no physical display validation, cache-reuse claim, or proof of relative addition to a nonzero input.',
        })
    return validate_suite({'description': 'Predictions of equality to pre-candidate literal binary frames.',
                          'calibration': str(CALIBRATION.relative_to(ROOT)),
                          'calibration_sha256': hashlib.sha256(CALIBRATION.read_bytes()).hexdigest(), 'cases': cases})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.dumps(build_suite(), indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'frozen display suite differs from generator/calibration'
    else:
        OUT.write_text(data)
