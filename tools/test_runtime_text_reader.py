"""Keep interpolation outputs byte-exact and failed formatting predictions frozen."""
import json
import unittest
from build_runtime_text_reader_cases import ROOT, OUT, build_suite
from runtime_grammar_probes import check_capture, separation


class TextReaderEvidence(unittest.TestCase):
    def test_frozen_suite_and_captures(self):
        self.assertEqual(build_suite(), json.loads(OUT.read_text()))
        for suffix in ('', '-confirmation'):
            capture = check_capture(ROOT / f'tests/runtime-grammar-text-reader{suffix}-9598.json')
            for row in capture['cases']:
                name = row['id'].removeprefix('text-reader-')
                observed = {v for p in row['passes'] for v in p[row['script']]}
                if name in ('fraction', 'beats'):
                    self.assertEqual(row['verdict'], 'prediction-not-held')
                    self.assertEqual(observed, {'A0.37B' if name == 'fraction' else 'A37 btB'})
                else:
                    self.assertEqual(row['verdict'], 'held-in-fixture')
                null = name in ('empty-pair', 'unknown-expression', 'empty-result')
                self.assertEqual(separation(row), 'matches-controls' if null else 'separates')
                if name == 'newline-escape':
                    self.assertEqual(observed, {'A\r\nB'})
                elif name == 'tab-escape':
                    self.assertEqual(observed, {'A\tB'})


if __name__ == '__main__':
    unittest.main()
