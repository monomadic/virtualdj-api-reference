"""Evidence checker must reject missing phases, altered values and failed restore."""
import copy
import json
from pathlib import Path
import unittest
from probe_time_sign_positions import validate


class SignEvidenceTests(unittest.TestCase):
    def test_capture_and_corruptions(self):
        data = json.loads((Path(__file__).resolve().parents[1] / 'tests/time-sign-positions-9644.json').read_text())
        validate(data)
        for change in ('missing', 'duplicate', 'sign', 'position', 'restore'):
            with self.subTest(change=change):
                bad = copy.deepcopy(data)
                run = bad['runs'][0]
                if change == 'missing': run['phases'].pop()
                if change == 'duplicate': run['phases'][0] = copy.deepcopy(run['phases'][1])
                if change == 'sign': run['phases'][0]['readings']['elapsed'] = ['1', '1']
                if change == 'position': run['phases'][0]['position_ms'] = '200'
                if change == 'restore': run['restored'] = False
                with self.assertRaises(AssertionError): validate(bad)


if __name__ == '__main__': unittest.main()
