#!/usr/bin/env python3
"""Check the optional Markdown projection without changing the source docs."""
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch
from urllib.parse import unquote

from reference_guides import ROOT, guide_records, connect_skin_docs
from render_reference import skin_records


class HTML(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.tags = [], [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a':
            self.links.append(attrs.get('href', ''))


class GuideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = ROOT / 'build/reference-guides/index.html'
        cls.guides = guide_records(cls.out)

    def test_source_and_heading_routes(self):
        for guide in self.guides:
            html = HTML(guide['html'])
            self.assertEqual(len(html.ids), len(set(html.ids)), guide['name'])
            for heading in guide['headings']:
                self.assertIn(heading['id'], html.ids)
                self.assertTrue((ROOT / guide['source']).read_text().splitlines()[heading['line']-1].startswith('#'))
            self.assertEqual((self.out.parent / unquote(guide['sourceUrl'])).resolve(), ROOT / guide['source'])

    def test_skin_docs_resolve_to_exact_heading(self):
        skins = skin_records(self.out)
        connect_skin_docs(skins, self.guides)
        by_source = {g['source']: g for g in self.guides}
        for skin in skins:
            for doc in skin['docs']:
                guide = by_source[doc['doc']]
                heading = next(h for h in guide['headings'] if h['line'] == doc['line'])
                self.assertEqual(unquote(doc['url']), f"#docs/{guide['id']}/{heading['id']}")

    def test_markdown_features_and_explicit_alias(self):
        grammar = next(g for g in self.guides if g['id'] == 'vdjscript-grammar')
        html = HTML(grammar['html'])
        self.assertIn('backticks-are-a-surface-feature-not-a-parser-feature', html.ids)
        skin = next(g for g in self.guides if g['id'] == 'skin-sdk')
        self.assertIn('table', HTML(skin['html']).tags)
        self.assertIn('&lt;skin', skin['html'])
        self.assertNotIn('<skin ', skin['html'])

    def test_internal_document_links(self):
        targets = {g['id']: HTML(g['html']).ids for g in self.guides}
        for guide in self.guides:
            for link in HTML(guide['html']).links:
                if link.startswith('#docs/'):
                    parts = unquote(link).split('/', 2)
                    self.assertIn(parts[1], targets)
                    if len(parts) == 3:
                        self.assertIn(parts[2], targets[parts[1]], f"{guide['name']}: {link}")

    def test_duplicate_headings_and_html_escaping(self):
        sample = '# Guide\n\n## Same\n\nOne\n\n## Same\n\n<script>alert(1)</script>\n\n[local](#same-1)'
        with patch('reference_guides.GUIDES', [('Sample', 'Test')]), patch.object(Path, 'read_text', return_value=sample):
            guide = guide_records(self.out)[0]
        self.assertEqual([h['id'] for h in guide['headings']], ['guide', 'same', 'same-1'])
        self.assertNotIn('<script>', guide['html'])
        self.assertIn('#docs/sample/same-1', guide['html'])


if __name__ == '__main__':
    unittest.main()
