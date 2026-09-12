#!/usr/bin/env python3
"""Check recovered key construction against executed historical-binary vectors."""
import json
import unittest
from pathlib import Path
from lyrics_cache import lid_from_words, lid_from_audiosig, describe_lid, parse_payload

ROOT = Path(__file__).resolve().parents[1]


class LyricsCacheTests(unittest.TestCase):
    def test_original_instruction_hash_vectors(self):
        data = json.loads((ROOT/'tests/lyrics-binary-vectors.json').read_text())
        for row in data['hash_vectors']:
            raw = lid_from_words(row['words'])
            self.assertEqual(raw.hex(), row['lid_hex'])
            self.assertEqual(describe_lid(raw)['audiosig'], row['audiosig'])
            self.assertEqual(lid_from_audiosig(row['audiosig']), raw)

    def test_sentinel_and_encoding_bounds(self):
        self.assertEqual(describe_lid(lid_from_audiosig(''))['fingerprint_word_count'], 0)
        self.assertEqual(describe_lid(lid_from_audiosig('-'))['fingerprint_word_count'], 1)
        for words in ([], [0], [0, -1], [0, 1 << 32], [0, True]):
            with self.assertRaises(ValueError):
                lid_from_words(words)
        with self.assertRaises(ValueError):
            lid_from_audiosig('invalid')
        with self.assertRaises(ValueError):
            lid_from_audiosig('////////////////////////')

    def test_storage_parser_preserves_native_edge_cases(self):
        cases = json.loads((ROOT/'tests/lyrics-binary-vectors.json').read_text())['payload_vectors']
        for row in cases:
            parsed = parse_payload(row['payload'])
            self.assertFalse(parsed['unparsed_lines'])
            if row['payload'].startswith('[-1'):
                self.assertEqual(parsed['segments'][0]['start'], -1)
                self.assertEqual(row['native_segments'][0]['start'], 0)
            if row['payload'] == '#LANG=eng':
                self.assertEqual(parsed['language'], 'eng')
                self.assertFalse(parsed['segments'])
            if row['payload'] == '#NOLYRICS':
                self.assertTrue(parsed['no_lyrics'])
        parsed = parse_payload('[0.1-0.2] alpha\\n\nUNKNOWN\n')
        self.assertTrue(parsed['segments'][0]['line_break_after'])
        self.assertEqual(parsed['segments'][0]['text'], 'alpha\\n')
        self.assertEqual(parsed['unparsed_lines'][0]['text'], 'UNKNOWN')


if __name__ == '__main__':
    unittest.main()
