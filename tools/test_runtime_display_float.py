"""Keep binary response evidence lossless and failed predictions inspectable."""
import json
import tempfile
import unittest
from pathlib import Path
from build_runtime_display_float_cases import build_suite, ROOT
from runtime_grammar_probes import check_capture, separation
from fixtures import build_fixtures


class DisplayFloatEvidence(unittest.TestCase):
    def test_fixture_never_mutates_live_state(self):
        fixture = build_fixtures(None)['parser_display_float']
        self.assertFalse(fixture.setup)
        self.assertFalse(fixture.teardown)
        self.assertFalse(fixture.needs_audio_file)

    def test_frozen_suite_and_independent_captures(self):
        suite = build_suite()
        self.assertEqual(suite, json.loads((ROOT / 'tests/runtime-grammar-display-float-cases.json').read_text()))
        for suffix in ('', '-confirmation'):
            path = ROOT / f'tests/runtime-grammar-display-float{suffix}-9598.json'
            check_capture(path)
            capture = json.loads(path.read_text())
            rows = {r['id']: r for r in capture['cases']}
            failed = rows['display-float-computed-text']
            self.assertEqual(failed['verdict'], 'prediction-not-held')
            self.assertEqual(separation(failed), 'matches-controls')
            self.assertEqual(separation(rows['display-float-leading-space']), 'matches-controls')
            for name, row in rows.items():
                if name not in ('display-float-computed-text', 'display-float-leading-space'):
                    self.assertEqual(row['verdict'], 'held-in-fixture')
                    self.assertEqual(separation(row), 'separates')

    def test_malformed_binary_sample_is_rejected(self):
        data = json.loads((ROOT / 'tests/runtime-grammar-display-float-9598.json').read_text())
        case = data['cases'][0]
        case['passes'][0][case['script']][0] = 'hex:FF'
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'capture.json'
            path.write_text(json.dumps(data))
            with self.assertRaises(AssertionError):
                check_capture(path)


if __name__ == '__main__':
    unittest.main()
