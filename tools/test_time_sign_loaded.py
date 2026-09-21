"""Reject false boundary promotions and distinguish negative time from position."""
import copy
import unittest

from probe_time_sign_loaded import FORMS, ORACLE, classify, verified


class SignEvidenceTest(unittest.TestCase):
    def runs(self):
        phase = dict(id='start/elapsed', skipped=False,
                     readings={f: ['0'] * 3 for f in FORMS})
        phase['readings']['remain'] = ['1'] * 3
        return [dict(phases=[copy.deepcopy(phase)]) for _ in range(2)]

    def test_both_controls_and_both_runs_required(self):
        runs = self.runs()
        self.assertEqual(classify(runs)['remain']['verdict'], 'recognized')
        runs[1]['phases'][0]['readings']['vfnrbq'] = ['1'] * 3
        self.assertEqual(classify(runs)['remain']['verdict'], 'UNDISCRIMINATED')

    def test_unstable_or_skipped_phase_cannot_promote(self):
        for variant in ('drift', 'skip'):
            runs = self.runs()
            phase = runs[1]['phases'][0]
            if variant == 'drift':
                phase['readings']['remain'][1] = '0'
            else:
                phase['skipped'] = True
            self.assertEqual(classify(runs)['remain']['verdict'], 'UNDISCRIMINATED')

    def test_absolute_requires_second_slot_controls(self):
        runs = self.runs()
        for run in runs:
            values = run['phases'][0]['readings']
            values['elapsed absolute'] = ['1'] * 3
            values['elapsed zzqqx'] = ['1'] * 3
        self.assertEqual(classify(runs)['elapsed absolute']['verdict'], 'UNDISCRIMINATED')

    def test_negative_signed_time_with_zero_position(self):
        reading = {ORACLE: '0', 'play': 'no', 'loaded': 'yes',
                   "get_time 'elapsed' 'absolute'": '-1000',
                   "get_time 'remain' 'absolute'": '7501000'}
        self.assertTrue(verified(reading, -1000))
        reading["get_time 'remain' 'absolute'"] = '7500000'
        self.assertFalse(verified(reading, -1000))


if __name__ == '__main__':
    unittest.main()
