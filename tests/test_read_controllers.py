#!/usr/bin/env python3
"""Adversarial reader checks; optional real bundle regression via --app in reader."""
import importlib.util
from pathlib import Path
import struct
import unittest
from unittest.mock import patch
from Crypto.Cipher import Blowfish
import io
import zipfile

spec = importlib.util.spec_from_file_location('reader', Path(__file__).parents[1] / 'tools/read_controllers.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
KEY = b'test-fixture-only'


def block(entries, predecessor=0, revision=1):
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w') as z:
        for name, content in entries:
            z.writestr(name, content)
    plain = output.getvalue()
    padding = 8 - len(plain) % 8
    return (struct.pack('<III', len(plain), predecessor, revision) + bytes(128)
            + Blowfish.new(KEY, Blowfish.MODE_ECB).encrypt(plain + bytes(padding)))


class ReaderTests(unittest.TestCase):
    def test_real_rsa_envelope(self):
        data = Path('/Applications/VirtualDJ.app/Contents/Resources/controllers.dat').read_bytes()
        self.assertTrue(4 <= len(r.recover_key(data[12:140])) <= 56)
        for signature in (b'', bytes(128), b'\xff' * 128):
            with self.assertRaises(ValueError):
                r.recover_key(signature)

    @patch.object(r, 'recover_key', return_value=KEY)
    def test_multiblock_byte_preservation(self, _):
        content = b'<?xml version="1.0"?><device><!--preserve--></device>\r\n'
        first = block([('definition.xml', content)])
        second = block([('mapping.xml', b'<mapper device="X"/>')], 1, 2)
        decoded = r.decode(first + second)
        self.assertEqual(decoded[0][2][0][1], content)
        self.assertEqual(decoded[1][0]['offset'], len(first))
        self.assertEqual(decoded[1][0]['revision'], 2)

    @patch.object(r, 'recover_key', return_value=KEY)
    def test_rejects_truncation_chain_and_corruption(self, _):
        data = block([('a.xml', b'<device/>')])
        for invalid in (b'', data[:-1], data + b'junk', data + data,
                        data[:140] + bytes(len(data) - 140)):
            with self.assertRaises(ValueError):
                r.decode(invalid)

    @patch.object(r, 'recover_key', return_value=KEY)
    def test_rejects_unsafe_duplicate_and_invalid_xml(self, _):
        for entries in ([('../outside.xml', b'<device/>')],
                        [('/outside.xml', b'<device/>')],
                        [('a.xml', b'<device/>'), ('A.xml', b'<mapper/>')],
                        [('a.xml', b'<not-xml')], [('a.xml', b'<unexpected/>')]):
            with self.assertRaises((ValueError, r.ET.ParseError)):
                r.decode(block(entries))


if __name__ == '__main__':
    unittest.main()
