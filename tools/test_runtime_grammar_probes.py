"""Regression checks for evidence classification, independent of a live app."""
import copy
import unittest
from runtime_grammar_probes import (validate_suite, verdict, separation,
                                    separation_report, ExactQueryChannel)
from unittest.mock import patch


class GrammarVerdicts(unittest.TestCase):
    def setUp(self):
        self.case = dict(id='test', fixture='parser_constants', hypothesis='test',
                         binary_sites=['test'], script='constant 37', expected='37',
                         controls=['constant #zzqqx', 'constant #vfnrbq'],
                         contrasts=[dict(script='constant 83', expected='83')])
        self.samples = {'constant 37': ['37', '37'], 'constant 83': ['83', '83'],
                        'constant #zzqqx': ['', ''], 'constant #vfnrbq': ['', '']}

    def test_raw_body_whitespace_is_not_stripped(self):
        with patch("runtime_grammar_probes.http.client.HTTPConnection") as conn:
            conn.return_value.getresponse.return_value.read.return_value = b" \t\r\n "
            channel = ExactQueryChannel()
            self.assertEqual(channel.query("constant \' \'"), " \t\r\n ")
            channel.close()

    def test_held(self):
        self.assertEqual(verdict(self.case, [self.samples, self.samples]), 'held-in-fixture')

    def test_wrong_prediction_is_retained(self):
        self.case['expected'] = '38'
        self.assertEqual(verdict(self.case, [self.samples]), 'prediction-not-held')

    def test_drift_within_and_between_rounds(self):
        changed = copy.deepcopy(self.samples)
        changed['constant 37'] = ['38', '38']
        self.assertEqual(verdict(self.case, [self.samples, changed]), 'inconclusive-drift')
        changed['constant 37'] = ['37', '38']
        self.assertEqual(verdict(self.case, [changed]), 'inconclusive-drift')

    def test_bad_oracle_and_controls_cannot_pass(self):
        self.samples['constant 83'] = ['37', '37']
        self.assertEqual(verdict(self.case, [self.samples]), 'inconclusive-oracle')
        self.samples['constant #vfnrbq'] = ['x', 'x']
        self.assertEqual(verdict(self.case, [self.samples]), 'inconclusive-controls')

    def test_absence_of_samples(self):
        self.assertEqual(verdict(self.case, []), 'not-run')

    def test_non_discriminating_suite_is_rejected(self):
        self.case['contrasts'][0]['expected'] = '37'
        with self.assertRaisesRegex(ValueError, 'discriminating'):
            validate_suite({'cases': [self.case]})

    def test_mutating_fixture_is_rejected(self):
        self.case['fixture'] = 'one_deck_loaded'
        with self.assertRaisesRegex(ValueError, 'read-only'):
            validate_suite({'cases': [self.case]})

    def test_separation_flags_a_null_reading(self):
        """A held prediction whose output equals the junk controls is not evidence."""
        case = {**self.case, 'passes': [self.samples]}
        self.assertEqual(separation(case), 'separates')
        blind = copy.deepcopy(case)
        blind['passes'][0]['constant 37'] = ['', '']
        for control in blind['controls']:
            blind['passes'][0][control] = ['', '']
        self.assertEqual(separation(blind), 'matches-controls')

    def test_separation_reads_per_baseline_vectors(self):
        """Action and scope captures nest a readback vector under each baseline."""
        case = {**self.case, 'passes': [{
            'constant 37': [[['0.25'], ['0.25']], [['0.25'], ['0.25']]],
            'constant #zzqqx': [[['0.25'], ['0.25']], [['0.65'], ['0.65']]],
            'constant #vfnrbq': [[['0.25'], ['0.25']], [['0.65'], ['0.65']]]}]}
        self.assertEqual(separation(case), 'separates')
        case['passes'][0]['constant 37'] = [[['0.25'], ['0.25']], [['0.65'], ['0.65']]]
        self.assertEqual(separation(case), 'matches-controls')

    def test_separation_report_counts_only_held_cases_as_blind(self):
        held = {**self.case, 'verdict': 'held-in-fixture',
                'passes': [{s: ['', ''] for s in
                            ['constant 37', *self.case['controls']]}]}
        missed = {**held, 'id': 'other', 'verdict': 'prediction-not-held'}
        report = separation_report([held, missed])
        self.assertEqual(report['held_but_matches_controls'], 1)
        self.assertEqual(report['cases'], ['test'])

    def test_separation_without_samples(self):
        self.assertEqual(separation({**self.case, 'passes': []}), 'not-run')


if __name__ == '__main__':
    unittest.main()
