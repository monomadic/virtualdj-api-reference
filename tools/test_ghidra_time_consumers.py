import copy
import json
import unittest
from ghidra_time_consumers import CAPTURE, MANIFEST, verify_export


class GhidraEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.capture = json.loads(CAPTURE.read_text())
        self.manifest = json.loads(MANIFEST.read_text())

    def test_export_matches_independent_code_bounds(self):
        self.assertTrue(verify_export(self.capture, self.manifest)['function_guards_match'])

    def test_reject_changed_code_or_wrong_function(self):
        for key, value in [('guard_sha256', '0' * 64), ('guard_length', 4),
                           ('ghidra_name', 'unrelated'), ('body_max', 'fffffffff'),
                           ('warning', 'failed analysis'), ('decompiled_c', '')]:
            with self.subTest(key=key):
                data = copy.deepcopy(self.capture)
                data['functions'][0][key] = value
                with self.assertRaises(ValueError):
                    verify_export(data, self.manifest)


if __name__ == '__main__':
    unittest.main()
