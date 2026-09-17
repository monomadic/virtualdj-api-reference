"""Preserve operand-specific arithmetic results, failures and null controls."""
import json
import unittest
from build_runtime_math_reader_cases import ROOT, OUT, build_suite
from runtime_grammar_probes import check_capture, separation


class MathReaderEvidence(unittest.TestCase):
    def test_frozen_suite_and_captures(self):
        suite = build_suite()
        self.assertEqual(suite, json.loads(OUT.read_text()))
        for suffix in ('', '-confirmation'):
            capture = check_capture(ROOT / f'tests/runtime-grammar-math-reader{suffix}-9598.json')
            for row in capture['cases']:
                name = row['id']
                samples = {v for p in row['passes'] for v in p[row['script']]}
                if name.endswith('direct-beats'):
                    self.assertEqual(row['verdict'], 'prediction-not-held')
                    self.assertEqual(samples, {'error:1'})
                    self.assertEqual(separation(row), 'separates')
                elif name.endswith('trailing-backtick-only'):
                    self.assertEqual(row['verdict'], 'prediction-not-held')
                    self.assertEqual(separation(row), 'matches-controls')
                else:
                    self.assertEqual(row['verdict'], 'held-in-fixture')
                    null = name.endswith(('missing-final-backtick', 'leading-space', 'quoted-number'))
                    self.assertEqual(separation(row), 'matches-controls' if null else 'separates')
                if name.endswith('computed-text'):
                    self.assertEqual(samples, {'537' if '-first-' in name else '953'})

    def test_controls_preserve_operand_position(self):
        for row in build_suite()['cases']:
            slot = int(row['id'].split('-operand-')[1][0])
            for control in row['controls']:
                parts = control.split()
                self.assertEqual(len(parts), 3)
                self.assertTrue(parts[slot].startswith("'"))
                self.assertTrue(parts[3 - slot].isdigit())


if __name__ == '__main__':
    unittest.main()
