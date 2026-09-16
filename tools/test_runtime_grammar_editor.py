"""Prevent incomplete or mismatched editor observations from becoming evidence."""
import copy
import json
import unittest
from runtime_grammar_editor import ROOT, HTTP, UI, compare


class EditorEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.http = json.loads(HTTP.read_text())
        self.ui = json.loads(UI.read_text())

    def test_failed_control_prediction_is_retained(self):
        for row in compare(self.http, self.ui)['cases']:
            self.assertEqual(row['runtime_verdict'], 'held-in-fixture')
            self.assertEqual(row['editor_predictions']['control_help'], 'prediction-not-held')
            self.assertEqual(row['combined_verdict'], 'prediction-not-held')

    def test_report_exposes_unrecoverable_screenshots(self):
        evidence = compare(self.http, self.ui)['ui_evidence']
        self.assertIs(evidence['screenshots_persisted'], False)
        self.assertIn('unrecoverable', evidence['screenshot_provenance'])

    def test_new_pass_checks_durable_images_and_keeps_failed_prediction(self):
        from runtime_grammar_probes import check_capture
        http = check_capture(ROOT / 'tests/runtime-grammar-editor-help-http-2026-09-17-9598.json')
        ui = json.loads((ROOT / 'tests/runtime-grammar-editor-help-ui-2026-09-17-9598.json').read_text())
        result = compare(http, ui)
        self.assertTrue(result['ui_evidence']['screenshots_persisted'])
        self.assertTrue(all(r['editor_predictions']['control_help'] == 'prediction-not-held'
                            for r in result['cases']))
        for field, value in [('path', 'tests/missing-editor-screenshot.jpg'), ('sha256', 'wrong')]:
            bad = copy.deepcopy(ui)
            bad['passes'][0][0]['evidence'][field] = value
            with self.assertRaises(AssertionError):
                compare(http, bad)

    def test_rejects_missing_provenance_or_restoration(self):
        for mutate in (
            lambda u: u['summary'].pop('screenshots_persisted'),
            lambda u: u['summary'].pop('screenshot_provenance'),
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
