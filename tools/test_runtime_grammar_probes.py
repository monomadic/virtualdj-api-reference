"""Regression checks for evidence classification, independent of a live app."""
import copy
import unittest
from runtime_grammar_probes import validate_suite, verdict


class GrammarVerdicts(unittest.TestCase):
    def setUp(self):
        self.case = dict(id='test', fixture='parser_constants', hypothesis='test',
                         binary_sites=['test'], script='constant 37', expected='37',
                         controls=['constant #zzqqx', 'constant #vfnrbq'],
                         contrasts=[dict(script='constant 83', expected='83')])
        self.samples = {'constant 37': ['37', '37'], 'constant 83': ['83', '83'],
                        'constant #zzqqx': ['', ''], 'constant #vfnrbq': ['', '']}

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


if __name__ == '__main__':
    unittest.main()
