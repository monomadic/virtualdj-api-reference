"""Guard evidence joins against accidentally manufacturing exposed icon names."""
import hashlib
import json
import unittest

from sysicon_atlas import CAPTURE, ROOT, inventory


class AtlasEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {r['cell']: r for r in inventory()['rows']}

    def test_vendor_row_notation_maps_to_physical_cells(self):
        self.assertEqual(self.rows['F7']['index'], 86)
        self.assertEqual(self.rows['F7']['wiki_row'], 'F1 to F7')
        self.assertEqual(self.rows['I16']['index'] + 1, self.rows['K1']['index'])
        self.assertEqual(self.rows['K9']['index'], 152)
        self.assertFalse(any(cell.startswith('J') for cell in self.rows))

    def test_live_join_does_not_promote_blank_observations(self):
        self.assertEqual([k['key'] for k in self.rows['C1']['tested_keys']], ['folder'])
        self.assertFalse(self.rows['K1']['tested_keys'])
        self.assertEqual(self.rows['K1']['key_status'], 'wiki-listed')
        self.assertEqual(self.rows['A1']['key_status'], 'unknown')

    def test_state_graphics_do_not_become_tested_primary_keys(self):
        for cell in ('E3', 'E4', 'F5', 'F6'):
            row = self.rows[cell]
            self.assertFalse(row['tested_keys'])
            self.assertTrue(row['binary_candidates'][0]['role'].startswith('state graphic'))
        self.assertEqual(self.rows['H6']['binary_candidates'][0]['match'], 'prefix')

    def test_consumer_capture_integrity_and_build_join(self):
        data = json.loads((CAPTURE / 'manifest.json').read_text())
        resolver = json.loads((ROOT / 'tests/sysicon-resolver-9598/manifest.json').read_text())
        self.assertEqual(data['binary_sha256'], resolver['binary_sha256'])
        for capture in data['captures'].values():
            self.assertEqual(hashlib.sha256((CAPTURE / capture['file']).read_bytes()).hexdigest(),
                             capture['sha256'])


if __name__ == '__main__':
    unittest.main()
