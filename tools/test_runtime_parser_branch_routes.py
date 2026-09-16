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

    def test_rejects_changed_source_assembly_or_bounds(self):
        for mutate in (
            lambda d: d['source'].update(binary_sha256='wrong'),
            lambda d: d['remote_mode_writers'][0]['assembly'].append('invented'),
            lambda d: d['remote_mode_writers'][0].update(end_exclusive='0x1'),
        ):
            data = json.loads(routes.OUT.read_text())
            mutate(data)
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / 'capture.json'
                path.write_text(json.dumps(data))
                with patch.object(routes, 'OUT', path), self.assertRaises(AssertionError):
                    routes.load_report()


if __name__ == '__main__':
    unittest.main()
