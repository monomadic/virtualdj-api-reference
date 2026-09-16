"""The audit must not turn association or null observations into completion."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import runtime_grammar_audit as audit


class AuditTests(unittest.TestCase):
    def test_preserves_gaps_and_null_readings(self):
        result = audit.report()
        self.assertFalse(result['completion_claim'])
        self.assertTrue(result['symbols_without_family_mapping'])
        rows = {r['id']: r for r in result['obligations']}
        self.assertEqual(rows['remote-entry']['evidence'], [])
        self.assertTrue(any(e['separation'] == 'matches-controls' for r in rows.values() for e in r['evidence']))
        self.assertTrue(all(c['status'].startswith('needs-screenshot') for c in result['editor_corpus']))

    def test_rejects_invalid_anchor_and_missing_case_family(self):
        for field, value in [('site', '0x1'), ('sources', [{'capture': 'tests/runtime-grammar-confirmation-9598.json', 'group': 'missing'}])]:
            plan = json.loads(audit.PLAN.read_text())
            plan['obligations'][0][field] = value
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'plan.json'
                path.write_text(json.dumps(plan))
                with patch.object(audit, 'PLAN', path), self.assertRaises(AssertionError):
                    audit.report()


if __name__ == '__main__':
    unittest.main()
