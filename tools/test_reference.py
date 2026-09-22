#!/usr/bin/env python3
"""Regression checks for the reference's skin data and template embedding contract."""
import unittest
from pathlib import Path
from urllib.parse import unquote

from render_reference import ROOT, TEMPLATE, skin_records
from xmldb import load, rows
from skin_attributes import attribute_rows, load as load_contracts, markdown


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

    def test_attribute_contracts_share_aliases_without_conflating_context(self):
        contracts = load_contracts()
        text = {r['name']: r for r in attribute_rows('text', {}, contracts)}
        button = {r['name']: r for r in attribute_rows('button', {}, contracts)}
        for a, b in [('size', 'fontsize'), ('overcolor', 'colorover')]:
            self.assertEqual(text[a]['contract_ref'], text[b]['contract_ref'])
        self.assertNotEqual(text['action']['contract_ref'], button['action']['contract_ref'])
        self.assertEqual(attribute_rows('font', {}, contracts), [])
        self.assertEqual(attribute_rows('textoverselected', {}, contracts), [])
        unknown = attribute_rows('font', {'unresolved': 1}, contracts)[0]
        self.assertEqual(unknown['value'], 'Unknown')
        self.assertIsNone(unknown['value_spec'])
        self.assertIsNone(unknown['default'])
        self.assertIsNone(unknown['constraints'])
        self.assertIn(r'left \| center \| right', markdown(list(text.values())))

    def test_attribute_table_projection_retains_observed_fields(self):
        for record in self.records:
            projected = {a['name']: a for a in record['attributeRows']}
            for attribute in record['attributes']:
                self.assertEqual(projected[attribute['name']]['uses'], attribute['uses'])
        template = TEMPLATE.read_text()
        for label in ('Attribute', 'Value', 'Description'):
            self.assertIn('<th scope="col">' + label + '</th>', template)
        for field in ('name', 'value', 'description', 'context'):
            self.assertIn('esc(a.' + field + ')', template)

    def test_payload_placeholders_occur_once(self):
        template = TEMPLATE.read_text()
        for token in ('__RECORDS__', '__SKIN_RECORDS__'):
            self.assertEqual(template.count(token), 1, token)

    def test_categories_and_nesting_keep_family_and_source_context(self):
        records = {r['name']: r for r in self.records}
        self.assertEqual(records['font']['categories']['skins']['id'], 'assets')
        self.assertEqual(records['define']['categories']['skins']['id'], 'directives')
        self.assertNotEqual(records['item']['categories']['skins'],
                            records['item']['categories']['video_skins'])
        for record in self.records:
            for direction, other in (('parents', 'parent'), ('children', 'child')):
                for edge in record['relationships'][direction]:
                    self.assertIn(edge[other], records)
                    self.assertEqual(edge['tier'], 2)
                    self.assertEqual(edge['evidence'], 'observed_vendor_xml')
                    for loc in edge['locations']:
                        path = (self.out.parent / unquote(loc['url'])).resolve()
                        self.assertEqual(path, ROOT / loc['path'])
                        self.assertGreaterEqual(loc['line'], loc['parent_line'])


if __name__ == '__main__':
    unittest.main()
