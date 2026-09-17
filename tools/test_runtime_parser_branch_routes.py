"""Preserve the structural capture's provenance and bounded-writer evidence."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import runtime_parser_branch_routes as routes


class RouteEvidenceTests(unittest.TestCase):
    def test_report_remains_structural_and_mode_is_not_claimed_measured(self):
        result = routes.load_report()
        self.assertEqual(result['remote_entry']['status'], 'mode-establishment-not-measured')
        self.assertEqual(result['list_helper']['status'], 'reachability-not-established')
        self.assertTrue(result['remote_mode_writers'])
        callers = result['evaluation_callers']['functions']
        self.assertTrue(callers)
        self.assertTrue(all(c['verified_instruction'] for f in callers for c in f['calls']))
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
