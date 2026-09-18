"""The audit must not turn association or null observations into completion."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import runtime_grammar_audit as audit


class AuditTests(unittest.TestCase):
    def test_triage_keeps_family_gaps_and_has_no_live_claim(self):
        result = audit.report()
        triage = result['unmapped_symbol_triage']
        self.assertFalse(triage['live_coverage_claim'])
        self.assertEqual(triage['symbols_without_triage'], [])
        self.assertEqual({s['symbol'] for g in triage['groups'] for s in g['symbols']},
                         set(result['symbols_without_family_mapping']))
        folded = {r['symbol'] for o in result['obligations'] for r in o.get('related_symbols', [])}
        self.assertEqual(folded, {s['symbol'] for g in triage['groups'] for s in g['symbols']
                                  if g['disposition'] == 'review-with-existing-family'})
        self.assertTrue(folded <= set(result['symbols_without_family_mapping']))

    def test_triage_rejects_invalid_review_and_exposes_new_gaps(self):
        manifest_path = audit.ROOT / 'tests/runtime-parser-9246/manifest.json'
        manifest = json.loads(manifest_path.read_text())
        for mutation in ('duplicate', 'unknown', 'mapped', 'site', 'disposition', 'obligation',
                         'related-missing', 'related-extra', 'related-evidence',
                         'out-of-scope-missing', 'out-of-scope-extra'):
            plan = json.loads(audit.PLAN.read_text())
            group = plan['unmapped_symbol_triage']['groups'][0]
            obligations = {o['id']: o for o in plan['obligations']}
            groups = {g['disposition']: g for g in plan['unmapped_symbol_triage']['groups']}
            if mutation == 'related-missing':
                obligations[group['related_obligations'][0]]['related_symbols'].pop()
            elif mutation == 'related-extra':
                obligations['scope-resolution']['related_symbols'].append(
                    {'symbol': groups['context-fixture-needed']['symbols'][0]['symbol'],
                     'triage_group': groups['context-fixture-needed']['id']})
            elif mutation == 'related-evidence':
                obligations[group['related_obligations'][0]]['related_symbols'][0]['evidence'] = []
            elif mutation == 'out-of-scope-missing':
                del groups['support-only']['symbols'][0]['out_of_scope']
            elif mutation == 'out-of-scope-extra':
                group['symbols'][0]['out_of_scope'] = 'not support-only'
            elif mutation == 'duplicate':
                group['symbols'].append(group['symbols'][0])
            elif mutation == 'unknown':
                group['symbols'][0]['symbol'] = 'not captured'
            elif mutation == 'mapped':
                group['symbols'][0]['symbol'] = 'IAction::create'
            elif mutation == 'site':
                group['symbols'][0]['site'] = '0x1005987e5'
            elif mutation == 'disposition':
                group['disposition'] = 'proven-live'
            else:
                group['related_obligations'] = ['missing']
            with self.subTest(mutation=mutation), self.assertRaises(AssertionError):
                audit.symbol_triage(plan, manifest, manifest_path)
        plan = json.loads(audit.PLAN.read_text())
        removed = plan['unmapped_symbol_triage']['groups'].pop(0)
        omitted = sorted(row['symbol'] for row in removed['symbols'])
        for obligation in plan['obligations']:
            obligation['related_symbols'] = [r for r in obligation.get('related_symbols', [])
                                             if r['triage_group'] != removed['id']]
        self.assertEqual(audit.symbol_triage(plan, manifest, manifest_path)['symbols_without_triage'],
                         omitted)

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
        effect = rows['boolean-cache-consumer']
        self.assertEqual({e['fixture'] for e in effect['evidence']}, {'parser_effect_boolean'})
        self.assertEqual({e['build'] for e in effect['evidence']}, {'9628'})
        self.assertEqual({e['symbol'] for e in effect['caller_evidence']},
                         {'__ZN20ACTION_effect_active9onExecuteEv'})
        self.assertTrue(any(e['verdict'] == 'prediction-not-held' for e in effect['evidence']))
        self.assertTrue(any(e['separation'] == 'matches-controls' for e in effect['evidence']))
        incoming = rows['incoming-parameter-selection']
        self.assertEqual(incoming['symbol'], 'IAction::getParam')
        self.assertEqual({e['fixture'] for e in incoming['evidence']},
                         {'parser_constants', 'parser_zoom_levels'})
        self.assertTrue(any(e['verdict'] == 'inconclusive-oracle' for e in incoming['evidence']))
        self.assertTrue(any(e['verdict'] == 'incomplete-run' and e['separation'] == 'not-run'
                            for e in incoming['evidence']))
        self.assertTrue(any(e['verdict'] == 'held-in-fixture' and e['separation'] == 'separates'
                            for e in incoming['evidence']))

    def test_rejects_invalid_external_caller(self):
        plan = json.loads(audit.PLAN.read_text())
        row = next(r for r in plan['obligations'] if r['id'] == 'backtick-consumers')
        row['caller_evidence'][0]['site'] = '0x1'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'plan.json'
            path.write_text(json.dumps(plan))
            with patch.object(audit, 'PLAN', path), self.assertRaises(AssertionError):
                audit.report()

    def test_pair_overloads_keep_distinct_evidence_and_reject_byte_candidates(self):
        rows = {r['id']: r for r in audit.report()['obligations']}
        self.assertNotEqual(rows['pair-typed-consumer']['symbol'],
                            rows['pair-float-consumer']['symbol'])
        floating = rows['pair-float-consumer']
        self.assertEqual({e['build'] for e in floating['evidence']}, {'9628'})
        self.assertTrue(all(e['case'].startswith('pair-float-') for e in floating['evidence']))
        self.assertTrue(any(e['verdict'] == 'prediction-not-held' for e in floating['evidence']))
        routes = json.loads((audit.ROOT / 'tests/runtime-parser-branch-routes.json').read_text())
        caller = next(f for f in routes['evaluation_callers']['functions']
                      if any(not c['verified_instruction'] for c in f['calls']))
        call = next(c for c in caller['calls'] if not c['verified_instruction'])
        plan = json.loads(audit.PLAN.read_text())
        row = next(r for r in plan['obligations'] if r['id'] == 'pair-typed-consumer')
        row['caller_evidence'] = [{'symbol': caller['symbol'], 'site': call['site']}]
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

    def test_empty_obligations_are_named_limits_not_passes(self):
        rows = {r['id']: r for r in audit.report()['obligations']}
        for name in ('remote-entry', 'list-conversion', 'editor-structure'):
            self.assertEqual(rows[name]['evidence'], [])
            self.assertEqual(rows[name]['limit']['status'], 'blocked')
        self.assertIn('not a finding', rows['remote-entry']['limit']['scope'])
        self.assertIn('does not prove dead code', rows['list-conversion']['limit']['no_direct_reference'])
        self.assertIn('Banned', rows['editor-structure']['limit']['coordinate_clicking'])
        for mutation in ('drop-limit', 'drop-field', 'limit-on-evidence'):
            plan = json.loads(audit.PLAN.read_text())
            rows = {r['id']: r for r in plan['obligations']}
            if mutation == 'drop-limit':
                del rows['remote-entry']['limit']
            elif mutation == 'drop-field':
                del rows['list-conversion']['limit']['affects']
            else:
                rows['head-delimiters']['limit'] = rows['remote-entry']['limit']
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'plan.json'
                path.write_text(json.dumps(plan))
                with self.subTest(mutation=mutation), patch.object(audit, 'PLAN', path), \
                        self.assertRaises(AssertionError):
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
