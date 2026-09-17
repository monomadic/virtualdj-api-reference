"""Keep consumer-specific failures, controls, and fixture limits visible."""
import unittest
from pathlib import Path
from fixtures import build_fixtures
from runtime_grammar_probes import check_capture, separation

ROOT = Path(__file__).resolve().parents[1]


class SettingEvalEvidence(unittest.TestCase):
    def test_fixture_has_no_mutations_or_media_requirements(self):
        fixture = build_fixtures(None)['parser_setting_eval']
        self.assertFalse(fixture.setup or fixture.teardown or fixture.decks or fixture.needs_audio_file)
        self.assertTrue(fixture.assertions)

    def test_failed_predictions_are_not_promoted(self):
        capture = check_capture(ROOT / 'tests/runtime-grammar-setting-eval-discrimination-9598.json')
        failed = {c['id'] for c in capture['cases'] if c['verdict'] == 'prediction-not-held'}
        self.assertEqual(failed, {'setting-eval-discrimination-computed-number-one',
                                  'setting-eval-discrimination-computed-text-on'})
        for case in capture['cases']:
            if case['id'] in failed:
                self.assertEqual(separation(case), 'matches-controls')
            else:
                self.assertEqual(separation(case), 'separates')

    def test_initial_null_and_followup_discrimination_stay_distinct(self):
        capture = check_capture(ROOT / 'tests/runtime-grammar-setting-eval-9598.json')
        true_case = next(c for c in capture['cases'] if c['id'] == 'setting-eval-evaluated-true')
        self.assertEqual(separation(true_case), 'matches-controls')
        capture = check_capture(ROOT / 'tests/runtime-grammar-setting-eval-types-9598.json')
        for case in capture['cases']:
            self.assertEqual(case['verdict'], 'held-in-fixture')
            self.assertEqual(separation(case), 'separates')


if __name__ == '__main__':
    unittest.main()
