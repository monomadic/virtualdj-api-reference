"""The audit must not turn association or null observations into completion."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import runtime_grammar_audit as audit


class AuditTests(unittest.TestCase):
    def test_preserves_gaps_and_null_readings(self):
        result = audit.report()
        self.assertFalse(result['completion_claim'])
        self.assertTrue(result['symbols_without_family_mapping'])
        rows = {r['id']: r for r in result['obligations']}
        self.assertEqual(rows['remote-entry']['evidence'], [])
        self.assertTrue(any(e['separation'] == 'matches-controls' for r in rows.values() for e in r['evidence']))
        self.assertTrue(all(c['status'].startswith('needs-screenshot') for c in result['editor_corpus']))

    def test_backtick_results_do_not_cover_unlinked_generic_helpers(self):
        rows = {r['id']: r for r in audit.report()['obligations']}
        self.assertTrue(rows['backtick-consumers']['evidence'])
        self.assertEqual({e['fixture'] for e in rows['backtick-consumers']['evidence']}, {'parser_setting_eval'})
        self.assertEqual(rows['backtick-float-evaluator']['evidence'], [])
        self.assertEqual({e['case'] for e in rows['backtick-math-reader']['evidence']},
                         {'backtick-numeric-consumer', 'backtick-numeric-consumer-quoted'})
        self.assertEqual({e['case'] for e in rows['backtick-text-reader']['evidence']},
                         {'backtick-text-eval', 'backtick-text-interpolation'})

    def test_rejects_invalid_external_caller(self):
        plan = json.loads(audit.PLAN.read_text())
        row = next(r for r in plan['obligations'] if r['id'] == 'backtick-consumers')
        row['caller_evidence'][0]['site'] = '0x1'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'plan.json'
            path.write_text(json.dumps(plan))
            with patch.object(audit, 'PLAN', path), self.assertRaises(AssertionError):
                audit.report()

    def test_rejects_wrong_consumer_edge_or_unknown_selected_case(self):
        for change_edge in (True, False):
            plan = json.loads(audit.PLAN.read_text())
            row = next(r for r in plan['obligations'] if r['id'] == 'backtick-math-reader')
            if change_edge:
                row['structural_edges'][0]['callee'] = 'IAction::getParamEval'
            else:
                row['sources'][0]['case_ids'].append('missing-case')
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'plan.json'
                path.write_text(json.dumps(plan))
                with patch.object(audit, 'PLAN', path), self.assertRaises(AssertionError):
                    audit.report()

    def test_rejects_invalid_anchor_and_missing_case_family(self):
        for field, value in [('site', '0x1'), ('sources', [{'capture': 'tests/runtime-grammar-confirmation-9598.json', 'group': 'missing'}])]:
            plan = json.loads(audit.PLAN.read_text())
            plan['obligations'][0][field] = value
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'plan.json'
                path.write_text(json.dumps(plan))
                with patch.object(audit, 'PLAN', path), self.assertRaises(AssertionError):
                    audit.report()


if __name__ == '__main__':
    unittest.main()
