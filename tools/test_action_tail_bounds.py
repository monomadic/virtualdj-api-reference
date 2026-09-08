"""Regression: early returns and unknown entry addresses must not leak windows."""
import struct
import unittest
from types import SimpleNamespace
from extract_action_contracts import bounded_body
from extract_skin_classes import function_starts


class Bounds(unittest.TestCase):
    def test_ret_and_neighbour(self):
        data = struct.pack('<4I', 0xD65F03C0, 0x52800AE0, 0x72B000E0, 0xDEADBEEF)
        text = ('__TEXT', '__text', 0x2000, len(data), 0)
        self.assertEqual([w for _, w in bounded_body(data, 0, text, {0x2000: 0x200c}, 0x2000)],
                         [0xD65F03C0, 0x52800AE0, 0x72B000E0])
        self.assertEqual(bounded_body(data, 0, text, {0x2000: 0x200c}, 0x2004), [])

    def test_segment_base_and_slice_offset(self):
        data = bytearray(256)
        base = 8
        struct.pack_into('<I', data, base + 16, 2)
        p = base + 32
        struct.pack_into('<II16sQ', data, p, 0x19, 72, b'__TEXT', 0x200000000)
        struct.pack_into('<4I', data, p + 72, 0x26, 16, 160, 4)
        data[base + 160:base + 164] = bytes([0x80, 0x20, 4, 0])
        self.assertEqual(function_starts(SimpleNamespace(data=data, base=base)),
                         [0x200001000, 0x200001004])


if __name__ == '__main__':
    unittest.main()
