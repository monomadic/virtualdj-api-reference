#!/usr/bin/env python3
"""Evidence-boundary regressions for skin categories and literal XML nesting."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import mcp_server
import skin_categories
import skin_relations

ROOT = Path(__file__).resolve().parents[1]


class NestingScannerTests(unittest.TestCase):
    def test_script_operators_inside_both_quote_styles(self):
        source = '''<skin>
<button action="a < 2 & b > 1 && c" query='d < 3 & e > 0'>
<text text="</button><fake/>"/>
</button></skin>'''
        edges, errors = skin_relations.scan(source)
        self.assertEqual(errors, [])
        self.assertEqual(edges, [
            {"parent": "skin", "child": "button", "parent_line": 1, "line": 2},
            {"parent": "button", "child": "text", "parent_line": 2, "line": 3},
        ])

    def test_comments_cdata_and_processing_instructions_are_not_elements(self):
        source = '''<?xml version="1.0"?>
<skin><!-- <fake><broken> -->
<![CDATA[ <fake></skin> & ]]> <?instruction <fake> ?>
<button/>
</skin>'''
        edges, errors = skin_relations.scan(source)
        self.assertEqual(errors, [])
        self.assertEqual(edges, [
            {"parent": "skin", "child": "button", "parent_line": 2, "line": 4}
        ])

    def test_selfclosing_siblings_keep_direct_parent_and_locations(self):
        edges, errors = skin_relations.scan(
            '<skin>\n<panel>\n<button/>\n<text/>\n</panel>\n<slider/>\n</skin>')
        self.assertEqual(errors, [])
        self.assertEqual(edges, [
            {"parent": "skin", "child": "panel", "parent_line": 1, "line": 2},
            {"parent": "panel", "child": "button", "parent_line": 2, "line": 3},
            {"parent": "panel", "child": "text", "parent_line": 2, "line": 4},
            {"parent": "skin", "child": "slider", "parent_line": 1, "line": 6},
        ])

    def test_uncertain_file_discards_preceding_valid_edges(self):
        tails = [
            '<panel></button></skin>', '<panel></skin>', '<panel>',
            '<panel', '<panel x="unterminated></panel></skin>',
            '<!-- unfinished', '<![CDATA[ unfinished', '<?unfinished',
            '</skin><second/>', '<panel <button/>', '</skin bad>',
        ]
        for tail in tails:
            with self.subTest(tail=tail):
                edges, errors = skin_relations.scan('<skin>\n<button/>\n' + tail)
                self.assertEqual(edges, [])
                self.assertTrue(errors)
                self.assertTrue(all(e['line'] >= 1 and e['reason'] for e in errors))

    def test_exactly_one_root_is_required(self):
        for source in ('', '<!-- only comment -->', '<skin/><skin/>'):
            with self.subTest(source=source):
                edges, errors = skin_relations.scan(source)
                self.assertEqual(edges, [])
                self.assertIn('expected one root', errors[0]['reason'])
        self.assertEqual(skin_relations.scan('<skin/>'), ([], []))

    def test_unsupported_declaration_is_diagnostic(self):
        for source in ('<!DOCTYPE skin><skin><button/></skin>',
                       '<skin><button/><!ENTITY x "y"></skin>'):
            with self.subTest(source=source):
                edges, errors = skin_relations.scan(source)
                self.assertEqual(edges, [])
                self.assertIn('unsupported declaration', errors[0]['reason'])

    def test_template_definitions_remain_literal_not_expanded(self):
        source = '<skin><define class="x"><button/></define><panel class="x"/></skin>'
        edges, errors = skin_relations.scan(source)
        self.assertEqual(errors, [])
        self.assertEqual([(e['parent'], e['child']) for e in edges],
                         [('skin', 'define'), ('define', 'button'), ('skin', 'panel')])
        self.assertNotIn(('panel', 'button'), [(e['parent'], e['child']) for e in edges])

    def test_query_preserves_family_provenance_and_unknown_semantics(self):
        edges = [
            {'family': 'skins', 'parent': 'skin', 'child': 'button', 'tier': 2},
            {'family': 'skins', 'parent': 'button', 'child': 'text', 'tier': 2},
            {'family': 'video_skins', 'parent': 'panel', 'child': 'button', 'tier': 2},
        ]
        data = {'note': skin_relations.NOTE, 'relationships': edges}
        result = skin_relations.relationships('button', 'skins', data)
        self.assertEqual(result['parents'], [edges[0]])
        self.assertEqual(result['children'], [edges[1]])
        self.assertEqual(len(skin_relations.relationships('button', data=data)['parents']), 2)
        unknown = skin_relations.relationships('unknown', data=data)
        self.assertEqual(unknown['parents'], [])
        self.assertEqual(unknown['children'], [])
        self.assertIn('support unknown', skin_relations.render(unknown))


class CategoryMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads((ROOT / 'docs/skin-xml-inventory.json').read_text())

    def test_agreed_categories_and_family_override(self):
        for name in ('font', 'customicons'):
            self.assertEqual(skin_categories.category(name, 'skins')['id'], 'assets')
        self.assertEqual(skin_categories.category('define', 'skins')['id'], 'directives')
        self.assertEqual(skin_categories.category('item', 'skins')['id'], 'controls-interaction')
        self.assertEqual(skin_categories.category('item', 'video_skins')['id'], 'structure-layout')

    def test_future_elements_and_non_skin_families_remain_unknown(self):
        for name, family in [('future_tag', 'skins'), ('font', 'pads')]:
            self.assertEqual(skin_categories.category(name, family)['id'], 'uncategorized')
        expanded = copy.deepcopy(self.inventory)
        expanded['families']['skins']['elements']['future_tag'] = {}
        skin_categories.validate(expanded)

    def test_current_metadata_matches_inventory(self):
        skin_categories.validate(self.inventory)
        for family in skin_categories.SKIN_FAMILIES:
            for name in self.inventory['families'][family]['elements']:
                self.assertNotEqual(skin_categories.category(name, family)['id'], 'uncategorized')

    def test_invalid_metadata_fails_loudly(self):
        mutations = {
            'invalid ID': lambda d: d['categories'].append({'id': 'Bad ID', 'label': 'Bad'}),
            'duplicate ID': lambda d: d['categories'].append(dict(d['categories'][0])),
            'unknown ID': lambda d: d['assignments'].update({'missing-category': ['font']}),
            'conflicting assignment': lambda d: d['assignments']['directives'].append('font'),
            'duplicate assignment': lambda d: d['assignments']['assets'].append('font'),
            'stale shared name': lambda d: d['assignments']['assets'].append('future_tag'),
            'stale override': lambda d: d['family_overrides']['video_skins'].update({'assets': ['customicons']}),
            'non-skin override': lambda d: d['family_overrides'].update({'pads': {'assets': ['font']}}),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                metadata = copy.deepcopy(skin_categories._metadata())
                mutate(metadata)
                with patch.object(skin_categories, '_metadata', return_value=metadata):
                    with self.assertRaises(ValueError):
                        skin_categories.validate(self.inventory)


class QuerySurfaceTests(unittest.TestCase):
    @staticmethod
    def mcp_json(output):
        # The established MCP wrapper appends successful CLI stderr diagnostics.
        payload, _, _diagnostics = output.partition('\n\n[stderr] ')
        return json.loads(payload)

    def cli(self, *args):
        result = subprocess.run([sys.executable, str(ROOT / 'tools/xmldb.py'), *args],
                                cwd=ROOT, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    def test_category_cli_mcp_equivalence(self):
        cli = self.cli('search', '--category=assets', '--family=skins', '--format=json')
        mcp = self.mcp_json(mcp_server.t_list_xml_elements(
            {'category': 'assets', 'family': 'skins', 'format': 'json'}))
        self.assertEqual(cli, mcp)
        self.assertIn('font', {r['element'] for r in cli})
        self.assertTrue(all(r['category']['id'] == 'assets' for r in cli))
        self.assertEqual({r['family'] for r in cli}, {'skins'})
        video = self.cli('search', '--category=assets', '--family=video_skins', '--format=json')
        self.assertEqual({r['family'] for r in video}, {'video_skins'})
        combined = self.cli('search', '--category=assets', '--family=skin', '--format=json')
        self.assertEqual({r['family'] for r in combined}, {'skins', 'video_skins'})
        self.assertEqual(self.cli('categories', '--format=json'),
                         self.mcp_json(mcp_server.t_skin_categories({'format': 'json'})))

    def test_parent_child_filters_cli_mcp_equivalence(self):
        data = skin_relations.load()['relationships']
        for direction, tag, other in [('parent', 'button', 'child'), ('child', 'text', 'parent')]:
            with self.subTest(direction=direction):
                cli = self.cli('search', f'--{direction}={tag}', '--family=skins', '--format=json')
                mcp = self.mcp_json(mcp_server.t_list_xml_elements(
                    {direction: tag, 'family': 'skins', 'format': 'json'}))
                self.assertEqual(cli, mcp)
                self.assertTrue(cli)
                self.assertEqual({r['family'] for r in cli}, {'skins'})
                for row in cli:
                    self.assertTrue(any(edge['family'] == row['family'] and edge[direction] == tag
                                        and edge[other] == row['element'] for edge in data))


if __name__ == '__main__':
    unittest.main()
