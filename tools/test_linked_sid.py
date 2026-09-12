#!/usr/bin/env python3
"""Regression against synthetic vectors executed by the historical ARM64 code."""
import json
import unittest
from pathlib import Path
from linked_sid import calculate, load_evidence

ROOT = Path(__file__).resolve().parents[1]


class LinkedSIDTests(unittest.TestCase):
    def test_binary_vectors(self):
        capture = json.loads((ROOT / 'tests/linked-sid-vectors.json').read_text())
        for key in ('build', 'arch', 'binary_sha256'):
            self.assertEqual(capture['source'][key], load_evidence()['source'][key])
        for row in capture['cases']:
            with self.subTest(artist=row['artist'], title=row['title'], remix=row['remix']):
                actual = calculate(row['artist'], row['title'], row['remix'])
                for key in ('sid_hex', 'sid_signed', 'reduced_utf8_hex'):
                    self.assertEqual(actual[key], row[key])

    def test_rejected_names_from_disassembly(self):
        for artist, title in [('', ''), ('', 'Track'), ('Unknown Artist', 'Track'), ('', 'Video Playback')]:
            self.assertEqual(calculate(artist, title)['sid_signed'], 0)

    def test_signed_conversion(self):
        cases = json.loads((ROOT / 'tests/linked-sid-vectors.json').read_text())['cases']
        negative = [c for c in cases if c['sid_signed'] < 0]
        self.assertTrue(negative)
        for row in negative:
            self.assertEqual(row['sid_signed'] + (1 << 64), int(row['sid_hex'], 16))


if __name__ == '__main__':
    unittest.main()
