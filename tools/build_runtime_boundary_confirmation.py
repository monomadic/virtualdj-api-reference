"""Independent values and quoted controls for the boundary-placement follow-up."""
import argparse
import json
from pathlib import Path
from runtime_grammar_probes import validate_suite

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / Path('tests/runtime-grammar-boundary-confirmation-cases.json')


def build_suite():
    cases = []
    for label, byte in [('tab', '\t'), ('lf', '\n'), ('cr', '\r'),
                        ('vt', '\v'), ('ff', '\f'), ('nbsp', '\u00a0')]:
        for kind, argument, expected, normal in [
            ('integer', '53', '53', '62'),
            ('percent', '53%', '53%', '9.53'),
            ('milliseconds', '53ms', '53ms', '62'),
            ('beats', '53bt', '53bt', '62'),
            ('single-quote', "'53'", '53', '62'),
            ('double-quote', '"53"', '53', '62'),
        ]:
            base = 'constant ' + argument
            tail = ' & param_cast float & param_add 9'
            case = {
                'id': f'boundary-confirm-{kind}-{label}',
                'fixture': 'parser_constants', 'group': 'boundary-confirmation',
                'hypothesis': f'Does {label} after a space following {argument} leave the original rendered value, unlike the calculation without that byte?',
                'script': base + ' ' + byte + tail, 'expected': expected,
                'controls': ['constant 53zzboundary_a' + tail, 'constant 53zzboundary_b' + tail],
                'contrasts': [{'script': base + tail, 'expected': normal},
                              {'script': 'constant 83', 'expected': '83'}],
                'binary_sites': ['IAction::stringGetParam@0x10059961c', 'IAction::create@0x100597c58'],
                'dimensions': {'byte': ord(byte), 'kind': kind, 'position': 'after-space'},
            }
            if kind in ('integer', 'percent', 'milliseconds', 'beats'):
                case['prior_case'] = f'boundary-{kind}-{label}-after-space'
            cases.append(case)
    return validate_suite({'description': 'Follow-up to the frozen boundary run, with new values and quoted forms; no universal whitespace rule.', 'cases': cases})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.dumps(build_suite(), indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'frozen confirmation suite differs from generator'
    else:
        OUT.write_text(data)
