"""Frozen interpolation boundary questions for get_text, separate from tokenization."""
import argparse
import json
from pathlib import Path
from runtime_grammar_probes import validate_suite

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tests/runtime-grammar-text-reader-cases.json'


def build_suite():
    rows = [
        ('paired', 'A`constant 37`B', 'A37B', 'Does paired interpolation insert the integer between literal sentinels?'),
        ('unclosed', 'A`constant 37 B', 'A`constant 37 B', 'Does an unmatched backtick remain literal with the remaining text?'),
        ('empty-pair', 'A``B', 'AB', 'Does an empty backtick pair contribute no text?'),
        ('empty-pairs-around-text', 'A``constant 37``B', 'Aconstant 37B', 'Do empty pairs leave the intervening action-looking text literal?'),
        ('adjacent', 'A`constant 37``constant 5`B', 'A375B', 'Do adjacent expressions each contribute text?'),
        ('separated', 'A`constant 37`C`constant 5`B', 'A37C5B', 'Do multiple expressions preserve the intervening literal text?'),
        ('leading-expression-space', 'A` constant 37`B', 'A37B', 'Does leading space inside the expression retain its integer result?'),
        ('trailing-expression-space', 'A`constant 37 `B', 'A37B', 'Does trailing space inside the expression retain its integer result?'),
        ('unknown-expression', 'A`h4_unknown_text_reader`B', 'AB', 'Does an unknown expression leave only the literal sentinels?'),
        ('empty-result', 'A`constant`B', 'AB', 'Does an empty constant result leave only the literal sentinels?'),
        ('boolean-on', 'A`on`B', 'AonB', 'Does the true boolean expression insert on?'),
        ('boolean-off', 'A`off`B', 'AoffB', 'Does the false boolean expression insert off?'),
        ('fraction', 'A`constant 0.37`B', 'A37%B', 'Does a fractional value insert its percentage representation?'),
        ('percent', 'A`constant 37%`B', 'A37%B', 'Does a percentage operand insert the percentage text?'),
        ('beats', 'A`constant 37bt`B', 'AB', 'Does an evaluated beat value leave only the sentinels in this text consumer?'),
        ('newline-escape', r'A\nB', 'A\r\nB', 'Does backslash-n insert CRLF between the sentinels?'),
        ('tab-escape', r'A\tB', 'A\tB', 'Does backslash-t insert a tab?'),
        ('decimal-character', r'A\65B', 'AAB', 'Does a decimal character escape insert the requested byte?'),
        ('double-backslash', r'A\\B', 'A\\B', 'Does a doubled backslash insert one backslash?'),
        ('backslash-before-backtick', r'A\`constant 37`B', 'A\\37B', 'Does a backslash remain literal while the following paired backticks still interpolate?'),
        ('double-percent', 'A%%B', 'A%B', 'Does a doubled percent sign insert one percent sign?'),
        ('unknown-escape', r'A\qB', 'A\\qB', 'Does an unknown backslash escape preserve both characters?'),
    ]
    cases = []
    for name, text, expected, question in rows:
        cases.append({
            'id': 'text-reader-' + name, 'fixture': 'parser_constants', 'group': 'text-reader',
            'hypothesis': question,
            'binary_sites': ['actionGetText@0x100423013', 'actionGetText@0x1004230c1',
                             'actionGetText@0x100423462', 'actionGetText@0x1004235d8'],
            'script': "get_text '" + text + "'", 'expected': expected,
            'controls': ["get_text 'A`" + junk + "`B'" for junk in ('zzqqx', 'vfnrbq')],
            'contrasts': [{'script': "get_text 'A`constant 83`B'", 'expected': 'A83B'}],
            'scope': 'Exact whitespace-preserving HTTP text in parser_constants. No skin rendering, outer-token escape rule, cache branch or universal result-type claim.',
        })
    return validate_suite({'description': 'Sentinel-controlled get_text interpolation, result formatting and escape questions.', 'cases': cases})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.dumps(build_suite(), indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'frozen text-reader suite differs from generator'
    else:
        OUT.write_text(data)
