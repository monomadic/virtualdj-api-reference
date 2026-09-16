"""Freeze position-controlled whitespace predictions from the b9246 parser leads."""
import argparse
import json
from pathlib import Path
from runtime_grammar_probes import validate_suite

OUT = Path('tests/runtime-grammar-boundary-cases.json')


def build_suite():
    manifest = json.loads(Path('tests/runtime-parser-9246/manifest.json').read_text())
    sites = [name + '@' + manifest['symbols'][name]['start'] for name in
             ('IAction::create', 'IAction::stringGetParam')]
    cases = []
    for label, byte in [('tab', '\t'), ('lf', '\n'), ('cr', '\r'),
                        ('vt', '\v'), ('ff', '\f'), ('nbsp', '\u00a0')]:
        for unit, suffix in [('integer', ''), ('percent', '%'), ('milliseconds', 'ms'), ('beats', 'bt')]:
            value = '37' + suffix
            tail = ' & param_cast float & param_add 5'
            base = 'constant ' + value
            expected_chain = '5.37' if suffix == '%' else '42'
            for position, script, expected in [
                ('terminal', base + byte, ''),
                ('before-space', base + byte + tail, ''),
                ('after-space', base + ' ' + byte + tail,
                 expected_chain if byte in '\t\n\r' else value),
            ]:
                cases.append({
                    'id': f'boundary-{unit}-{label}-{position}',
                    'fixture': 'parser_constants', 'group': 'boundary-placement',
                    'hypothesis': f'Does {label} at {position} after {value} produce {expected!r}, independently of the space before a following operator?',
                    'script': script, 'expected': expected,
                    'controls': [f'constant {value}zzboundary_{c}' + tail for c in ('a', 'b')],
                    'contrasts': [{'script': base + tail, 'expected': expected_chain},
                                  {'script': 'constant 83', 'expected': '83'}],
                    'binary_sites': sites,
                    'dimensions': {'byte': ord(byte), 'unit': unit, 'position': position},
                    'supersedes_confounded_family': 'number-end-* and suffix-boundary-* do not isolate the inserted byte from operator adjacency',
                })
    return validate_suite({'description': 'Position-controlled boundary predictions; blank readings remain null against malformed controls.', 'cases': cases})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = json.dumps(build_suite(), indent=2) + '\n'
    if args.check:
        assert OUT.read_text() == data, 'frozen boundary suite differs from generator'
    else:
        OUT.write_text(data)
