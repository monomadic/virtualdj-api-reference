"""Reject mismatched host identity and corrupted memory captures."""
import copy
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from plugin_memory import verify


class MemoryVerificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.binary = Path(self.temp.name) / 'host'
        self.uuid = bytes(range(16))
        header = struct.pack('<8I', 0xfeedfacf, 0x0100000c, 0, 2, 1, 24, 0, 0)
        self.binary.write_bytes(header + struct.pack('<II', 0x1b, 24) + self.uuid)
        self.capture = dict(schema=1, channel='in-process-memory', arch='arm64',
                            build='18.0.0', image_uuid=self.uuid.hex(),
                            table_unslid_address='0x1000',
                            verbs={'hot_cue': {'id': 7, 'flags': 0}})
        self.disk = dict(summary={'build': '18.0.0', 'address': '0x1000'},
                         verbs=copy.deepcopy(self.capture['verbs']))
        mock = patch('plugin_memory.build', return_value=self.disk)
        mock.start()
        self.addCleanup(mock.stop)

    def test_matching_image_and_records(self):
        self.assertTrue(verify(self.capture, self.binary)['all_name_id_flags_records_match'])

    def test_different_uuid(self):
        self.capture['image_uuid'] = 'ff' * 16
        with self.assertRaisesRegex(ValueError, 'UUID'):
            verify(self.capture, self.binary)

    def test_different_build(self):
        self.capture['build'] = '18.0.1'
        with self.assertRaisesRegex(ValueError, 'build'):
            verify(self.capture, self.binary)

    def test_different_record(self):
        self.capture['verbs']['hot_cue']['flags'] = 1
        with self.assertRaisesRegex(ValueError, 'records'):
            verify(self.capture, self.binary)

    def test_different_location(self):
        self.capture['table_unslid_address'] = '0x2000'
        with self.assertRaisesRegex(ValueError, 'location'):
            verify(self.capture, self.binary)


if __name__ == '__main__':
    unittest.main()
