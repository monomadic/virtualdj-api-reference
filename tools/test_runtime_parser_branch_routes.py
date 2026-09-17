"""Preserve the structural capture's provenance and bounded-writer evidence."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import runtime_parser_branch_routes as routes


class RouteEvidenceTests(unittest.TestCase):
    def test_compact_pair_caller_reports_keep_rejected_candidates_and_no_live_claim(self):
        reports = [routes.caller_report(target) for target in (
            'IParamValuesAction::getValues(float*, float*)',
            'IParamValuesAction::getValues(SActionParam*, SActionParam*)')]
        for report, consumer in zip(reports, ('param_multiply7onQuery', 'param_add7onQuery')):
            self.assertFalse(report['live_coverage_claim'])
            self.assertTrue(any(consumer in call['caller'] and call['verified_instruction']
                                and call['instruction'] for call in report['calls']))
        rejected = [call for report in reports for call in report['calls']
                    if not call['verified_instruction']]
        self.assertEqual([call['site'] for call in rejected], ['0x10217e5b3'])

    def test_compact_report_rejects_captured_but_unscanned_target(self):
        with self.assertRaises(ValueError):
            routes.caller_report('IAction::getParam')

    def test_report_remains_structural_and_mode_is_not_claimed_measured(self):
        result = routes.load_report()
        self.assertEqual(result['remote_entry']['status'], 'mode-establishment-not-measured')
        self.assertEqual(result['list_helper']['status'], 'reachability-not-established')
        self.assertTrue(result['remote_mode_writers'])
        callers = result['evaluation_callers']['functions']
        self.assertTrue(callers)
        pair_calls = [(f['symbol'], c) for f in callers for c in f['calls']
                      if 'getValues' in c['target']]
        self.assertTrue(any('param_multiply7onQuery' in name and c['verified_instruction']
                            and c['target'].endswith('(float*, float*)')
                            for name, c in pair_calls))
        self.assertTrue(any('param_add7onQuery' in name and c['verified_instruction']
                            and c['target'].endswith('(SActionParam*, SActionParam*)')
                            for name, c in pair_calls))
        rejected = [(name, c) for name, c in pair_calls if not c['verified_instruction']]
        self.assertEqual([c['site'] for _, c in rejected], ['0x10217e5b3'])
        self.assertTrue(all(c['verified_instruction'] for f in callers for c in f['calls']
                            if 'getValues' not in c['target']))
        cache = result['boolean_cache_arguments']['calls']
        self.assertTrue(cache)
        nonnull = [r for r in cache if r['cache_argument'] == 'object-relative-address']
        self.assertEqual({r['caller'] for r in nonnull}, {'__ZN20ACTION_effect_active9onExecuteEv'})
        self.assertEqual({r['call_site'] for r in nonnull}, {'0x1008a16ea', '0x1008a179c'})
        self.assertNotIn('unresolved', {r['cache_argument'] for r in cache})

    def test_rejects_changed_source_assembly_or_bounds(self):
        for mutate in (
            lambda d: d['boolean_cache_arguments']['calls'][0].update(cache_argument='object-relative-address'),
            lambda d: d['evaluation_entrypoints'][0]['assembly'].append('invented'),
            lambda d: d['evaluation_entrypoints'][0]['routes'][0].update(site='0x1'),
            lambda d: d['evaluation_entrypoints'][0]['routes'][0].update(target='0x1'),
            lambda d: d['source'].update(binary_sha256='wrong'),
            lambda d: d['remote_mode_writers'][0]['assembly'].append('invented'),
            lambda d: d['remote_mode_writers'][0].update(end_exclusive='0x1'),
            lambda d: d['evaluation_callers']['functions'][0]['assembly'].append('invented'),
            lambda d: d['evaluation_callers']['functions'][0]['calls'][0].update(site='0x1'),
            lambda d: d['evaluation_callers']['functions'][0]['calls'][0].update(verified_instruction=False),
        ):
            data = json.loads(routes.OUT.read_text())
            mutate(data)
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / 'capture.json'
                path.write_text(json.dumps(data))
                with patch.object(routes, 'OUT', path), self.assertRaises(AssertionError):
                    routes.load_report()

    def test_cache_review_does_not_follow_an_intervening_call(self):
        functions = [{'symbol': 'caller', 'assembly': [
            'caller:', '0000000000000010\txorl\t%r8d, %r8d',
            '0000000000000013\tcallq\tother', '0000000000000018\tcallq\tgetBoolParam'],
            'calls': [{'target': 'IAction::getBoolParam', 'site': '0x18', 'verified_instruction': True}]}]
        self.assertEqual(routes.boolean_cache_arguments(functions)['calls'][0]['cache_argument'], 'unresolved')


if __name__ == '__main__':
    unittest.main()
