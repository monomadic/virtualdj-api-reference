"""Preserve exact float-pair outputs, failed predictions and matched controls."""
import json
from pathlib import Path
import unittest

from build_runtime_pair_float_cases import build, OUT
from runtime_grammar_probes import check_capture, separation


class PairFloatEvidence(unittest.TestCase):
    def test_frozen_suite(self):
        self.assertEqual(OUT.read_text(), json.dumps(build(), indent=2) + '\n')

    def test_both_operands_repeat_exact_outputs_without_rewriting_predictions(self):
        outputs = {
            'integer': '21', 'decimal': '7.5', 'percent': '75%',
            'beats': 'error:1', 'milliseconds': '21ms', 'raw-action': '21',
            'paired': '21', 'computed-decimal': '7.5', 'computed-beats': '21bt',
            'computed-text': '0', 'quoted-number': '0', 'unclosed': '0',
            'trailing-only': '0', 'long-action': '21',
        }
        failed = {'percent', 'beats', 'milliseconds', 'computed-beats', 'trailing-only'}
        matched = {'computed-text', 'quoted-number', 'unclosed', 'trailing-only'}
        captures = [check_capture(Path(f'tests/runtime-grammar-pair-float{suffix}-9628.json'))
                    for suffix in ('', '-confirmation')]
        previous = {}
        for capture in captures:
            self.assertEqual(capture['summary']['status'], 'complete')
            self.assertEqual(capture['summary']['build'], '9628')
            self.assertEqual({row['id'] for row in capture['cases']},
                             {f'pair-float-{slot}-{label}' for slot in (1, 2) for label in outputs})
            for row in capture['cases']:
                label = row['id'].split('-', 3)[3]
                with self.subTest(case=row['id'], captured_at=capture['summary']['captured_at']):
                    self.assertEqual(row['verdict'], 'prediction-not-held' if label in failed
                                     else 'held-in-fixture')
                    self.assertEqual(separation(row), 'matches-controls' if label in matched
                                     else 'separates')
                    for samples in row['passes']:
                        self.assertEqual(set(samples[row['script']]), {outputs[label]})
                        for control in row['controls']:
                            self.assertEqual(set(samples[control]), {'0'})
                        for contrast in row['contrasts']:
                            self.assertEqual(set(samples[contrast['script']]), {'33'})
                    if row['id'] in previous:
                        self.assertEqual(row['passes'], previous[row['id']])
                    previous[row['id']] = row['passes']


if __name__ == '__main__':
    unittest.main()
