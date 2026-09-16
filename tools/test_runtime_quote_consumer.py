"""Keep empty-quote evidence distinct from its control-shaped readings."""
import unittest
from pathlib import Path
from runtime_grammar_probes import check_capture, separation

ROOT = Path(__file__).resolve().parents[1]


class QuoteConsumerEvidence(unittest.TestCase):
    def test_same_length_controls_separate(self):
        initial = check_capture(ROOT / 'tests/runtime-grammar-quote-consumer-arity-initial-9598.json')
        self.assertIn('scope wording', initial['summary']['retention_note'])
        capture = check_capture(ROOT / 'tests/runtime-grammar-quote-consumer-arity-9598.json')
        for case in capture['cases']:
            self.assertEqual(case['verdict'], 'held-in-fixture')
            self.assertEqual(separation(case), 'separates')
            for readings in case['passes']:
                self.assertNotEqual(readings[case['script']], readings[case['contrasts'][0]['script']])

    def test_omission_contrast_discriminates_without_relabelling_controls(self):
        capture = check_capture(ROOT / 'tests/runtime-grammar-quote-consumer-9598.json')
        for case in capture['cases']:
            self.assertEqual(case['verdict'], 'held-in-fixture')
            for readings in case['passes']:
                self.assertNotEqual(readings[case['script']], readings[case['contrasts'][0]['script']])
            expected_separation = 'separates' if case['id'].endswith('both-empty') else 'matches-controls'
            self.assertEqual(separation(case), expected_separation)


if __name__ == '__main__':
    unittest.main()
