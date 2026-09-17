"""Keep incoming-parameter results separate from failed fixtures and uncertain writes."""
import unittest
from pathlib import Path
from runtime_grammar_actions import check_capture as check_actions, equal
from runtime_grammar_probes import check_capture as check_queries, separation

PREFIX = 'tests/runtime-grammar-incoming-'


class IncomingEvidence(unittest.TestCase):
    def test_query_contrast_failure_is_not_propagation_evidence(self):
        capture = check_queries(Path(PREFIX + 'query-initial-9628.json'))
        for row in capture['cases']:
            self.assertIn(row['verdict'], ('inconclusive-oracle', 'inconclusive-controls'))

    def test_direct_action_chain_does_not_supply_the_omitted_value(self):
        capture = check_actions(Path(PREFIX + 'actions-initial-9628.json'))
        for row in capture['cases']:
            if row['id'].endswith('-omitted'):
                self.assertEqual(row['verdict'], 'prediction-not-held')
                self.assertEqual(row['passes'][0][row['script']],
                                 [[['0.2'], ['0.2']], [['0.2'], ['0.2']]])
            elif row['id'].endswith('-default'):
                self.assertEqual(row['verdict'], 'prediction-not-held')
                self.assertEqual(separation(row), 'matches-controls')
            else:
                self.assertEqual(row['verdict'], 'held-in-fixture')

    def test_aborted_runs_are_incomplete_and_uncertain_scripts_not_replayed(self):
        uncertain = set()
        for suffix in ('pipeline-aborted-9628.json', 'pipeline-bounded-aborted-9628.json'):
            capture = check_actions(Path(PREFIX + suffix))
            self.assertEqual(capture['summary']['status'], 'aborted')
            self.assertEqual(capture['summary']['restoration_status'], 'verified')
            self.assertFalse(capture['summary']['manual_restore_required'])
            self.assertTrue(all(c['verdict'] == 'incomplete-run' for c in capture['cases']))
            uncertain.update(j['script'] for j in capture['journal']
                             if j['status'] == 'response-uncertain')
        self.assertTrue(uncertain)
        for suffix in ('pipeline-9628.json', 'pipeline-confirmation-9628.json'):
            capture = check_actions(Path(PREFIX + suffix))
            self.assertFalse(uncertain & {j['script'] for j in capture['journal']})

    def test_independent_pipeline_runs_match_expected_readback(self):
        captures = [check_actions(Path(PREFIX + suffix)) for suffix in
                    ('pipeline-9628.json', 'pipeline-confirmation-9628.json')]
        self.assertNotEqual(captures[0]['summary']['captured_at'],
                            captures[1]['summary']['captured_at'])
        for capture in captures:
            self.assertEqual(capture['summary']['status'], 'complete')
            self.assertEqual(capture['summary']['build'], '9628')
            for row in capture['cases']:
                self.assertEqual(row['verdict'], 'held-in-fixture')
                self.assertEqual(separation(row), 'separates')
                for samples in row['passes']:
                    for reads, expected in zip(samples[row['script']], row['expected']):
                        self.assertTrue(all(equal(read, expected) for read in reads))


if __name__ == '__main__':
    unittest.main()
