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
        self.assertEqual({e['fixture'] for e in rows['backtick-float-evaluator']['evidence']}, {'parser_display_float'})
        self.assertTrue({'backtick-numeric-consumer', 'backtick-numeric-consumer-quoted',
                         'math-reader-first-operand-1-raw-action-text'} <=
                        {e['case'] for e in rows['backtick-math-reader']['evidence']})
        self.assertEqual({e['fixture'] for e in rows['backtick-math-reader']['evidence']}, {'parser_constants'})
        self.assertTrue({'backtick-text-eval', 'backtick-text-interpolation', 'text-reader-unclosed'} <=
                        {e['case'] for e in rows['backtick-text-reader']['evidence']})
        self.assertEqual({e['fixture'] for e in rows['backtick-text-reader']['evidence']}, {'parser_constants'})

    def test_rejects_invalid_external_caller(self):
        plan = json.loads(audit.PLAN.read_text())
        row = next(r for r in plan['obligations'] if r['id'] == 'backtick-consumers')
        row['caller_evidence'][0]['site'] = '0x1'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'plan.json'
            path.write_text(json.dumps(plan))
            with patch.object(audit, 'PLAN', path), self.assertRaises(AssertionError):
                audit.report()

    def test_rejects_invalid_entry_route(self):
        plan = json.loads(audit.PLAN.read_text())
        row = next(r for r in plan['obligations'] if r['id'] == 'backtick-float-evaluator')
        row['entry_evidence'][0]['site'] = '0x1'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'plan.json'
            path.write_text(json.dumps(plan))
            with patch.object(audit, 'PLAN', path), self.assertRaises(AssertionError):
                audit.report()

    def test_evaluator_partition_is_bounded_and_not_live_coverage(self):
        result = audit.report()['evaluator_branch_review']
        self.assertFalse(result['live_branch_coverage_claim'])
        self.assertEqual({f['symbol'] for f in result['functions']},
                         {'IAction::getParamEval', 'IAction::getFloatParamEval'})
        for function in result['functions']:
            self.assertEqual(sum(function['classification_counts'].values()),
                             len(function['conditional_branches']))

    def test_rejects_incomplete_or_duplicated_evaluator_partition(self):
        for mutation in ('missing', 'duplicate', 'unknown-site', 'unknown-category', 'missing-function'):
            plan = json.loads(audit.PLAN.read_text())
            functions = plan['evaluator_branch_review']['functions']
            group = functions[0]['groups'][0]
            if mutation == 'missing':
                functions[0]['groups'].pop()
            elif mutation == 'duplicate':
                group['sites'].append(group['sites'][0])
            elif mutation == 'unknown-site':
                group['sites'][0] = '0x1'
            elif mutation == 'unknown-category':
                group['classification'] = 'proven-live'
            else:
                functions.pop()
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
