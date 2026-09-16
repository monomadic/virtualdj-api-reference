"""Prevent incomplete or mismatched editor observations from becoming evidence."""
import copy
import json
import unittest
from runtime_grammar_editor import HTTP, UI, compare


class EditorEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.http = json.loads(HTTP.read_text())
        self.ui = json.loads(UI.read_text())

    def test_failed_control_prediction_is_retained(self):
        for row in compare(self.http, self.ui)['cases']:
            self.assertEqual(row['runtime_verdict'], 'held-in-fixture')
            self.assertEqual(row['editor_predictions']['control_help'], 'prediction-not-held')
            self.assertEqual(row['combined_verdict'], 'prediction-not-held')

    def test_rejects_missing_provenance_or_restoration(self):
        for mutate in (
            lambda u: u['passes'].pop(),
            lambda u: u['passes'][1].reverse(),
            lambda u: u['passes'][0][0].update(source_verified_visually=False),
            lambda u: u['summary'].update(build='9246'),
            lambda u: u['summary'].update(suite_sha256='wrong'),
            lambda u: u['restoration'].update(reopened_verified=False),
        ):
            ui = copy.deepcopy(self.ui)
            mutate(ui)
            with self.assertRaises(AssertionError):
                compare(self.http, ui)


if __name__ == '__main__':
    unittest.main()
