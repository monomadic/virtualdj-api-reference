#!/usr/bin/env python3
"""Regression checks for the reference's skin data and template embedding contract."""
import unittest
from pathlib import Path
from urllib.parse import unquote

from render_reference import ROOT, TEMPLATE, skin_records
from xmldb import load, rows


class SkinReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = ROOT / 'build/reference/index.html'
        cls.records = skin_records(cls.out)

    def test_inventory_parity_and_attribute_totals(self):
        source = [(f, n, e) for f, n, e in rows(load())
                  if f in {'skins', 'video_skins'}]
        self.assertEqual({r['name'] for r in self.records}, {n for _, n, _ in source})
        self.assertEqual(len(self.records), len({r['name'] for r in self.records}))
        for record in self.records:
            expected = {}
            families = {}
            for family, name, entry in source:
                if name != record['name']:
                    continue
                families[family] = entry
                for attr, count in entry['attributes'].items():
                    expected[attr] = expected.get(attr, 0) + count
            self.assertEqual(record['families'], families)
            self.assertEqual({a['name']: a['uses'] for a in record['attributes']}, expected)

    def test_doc_routes_and_evidence_are_preserved(self):
        circle = next(r for r in self.records if r['name'] == 'mousecircle')
        self.assertIn('radius', circle['description'])
        self.assertIn('build 18.0.9598', circle['description'])
        for record in self.records:
            self.assertEqual(record['status'], 'unverified')
            for doc in record['docs']:
                path = (self.out.parent / unquote(doc['url'])).resolve()
                self.assertEqual(path, ROOT / doc['doc'])
                self.assertTrue(path.read_text().splitlines()[doc['line'] - 1].startswith('#'))

    def test_payload_placeholders_occur_once(self):
        template = TEMPLATE.read_text()
        for token in ('__RECORDS__', '__SKIN_RECORDS__'):
            self.assertEqual(template.count(token), 1, token)


if __name__ == '__main__':
    unittest.main()
