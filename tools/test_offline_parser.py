"""Safety boundaries and comparison failures for the copied-image parser pilot."""
import copy
import json
from pathlib import Path
import struct
import tempfile
import unittest

from offline_parser import commands, convert, baseline_rows, validate_run, guard_header, manifest_for, check_capture

ROOT = Path(__file__).resolve().parents[1]


def fixture(first=4096):
    zero = struct.pack('<II16sQQQQiiII', 0x19, 72, b'__PAGEZERO', 0, 0x100000000, 0, 0, 0, 0, 0, 0)
    text = struct.pack('<II16sQQQQiiII', 0x19, 152, b'__TEXT', 0x100000000, 8192, 0, 8192, 7, 5, 1, 0)
    section = struct.pack('<16s16sQQIIIIIIII', b'__text', b'__TEXT', 0x100000000+first, 64, first, 2, 0, 0, 0, 0, 0, 0)
    dyld = struct.pack('<12I', 0x80000022, 48, *([0]*10))
    main = struct.pack('<IIQQ', 0x80000028, 24, first, 0)
    rows = zero+text+section+dyld+main
    h = struct.pack('<IiiIIIII', 0xfeedfacf, 0x100000c, 0, 2, 4, len(rows), 0x200085, 0)
    data = bytearray(8192);data[:32]=h;data[32:32+len(rows)]=rows
    data[first:first+64]=bytes(range(64))
    return bytes(data)


class ConverterTests(unittest.TestCase):
    def test_preserves_body_and_segment_indices(self):
        source=fixture();output, report=convert(source)
        h, rows=commands(output)
        self.assertEqual(h[3],6)
        self.assertFalse(h[6]&0x200000)
        self.assertEqual(output[4096:],source[4096:])
        self.assertEqual([r[8:24].rstrip(b'\0') for k,r in rows if k==0x19], [b'__PAGEZERO',b'__TEXT'])
        self.assertEqual(struct.unpack_from('<QQQQ',rows[0][1],24),(0x100000000,0,0,0))
        self.assertNotIn(0x80000028,[k for k,_ in rows])
        self.assertEqual([k for k,_ in rows].count(0xd),1)
        self.assertTrue(report['section_bytes_preserved'])

    def test_rejects_unknown_layout_and_truncation(self):
        for offset,value in [(0,0),(4,0x1000007),(12,6),(36,0),(32+72+64,2)]:
            with self.subTest(offset=offset):
                data=bytearray(fixture());struct.pack_into('<I',data,offset,value)
                with self.assertRaises(ValueError):convert(data)
        with self.assertRaises(ValueError):convert(fixture()[:100])

    def test_header_growth_cannot_overwrite_code(self):
        with self.assertRaisesRegex(ValueError,'header space'):
            convert(fixture(first=328))

    def test_rejects_already_converted_image(self):
        output,_=convert(fixture())
        with self.assertRaises(ValueError):convert(output)


class CaptureTests(unittest.TestCase):
    def setUp(self):
        _,self.baseline=baseline_rows()
        self.rows=json.loads((ROOT/'tests/offline-parser-9644-sandbox-initial.json').read_text())['runs']

    def test_first_offline_run_matches_saved_live_fields(self):
        for row in self.rows:validate_run(row,self.baseline)

    def test_zero_exit_is_not_enough(self):
        row={'mode':'--load-only','returncode':0,'stdout':''}
        with self.assertRaises(ValueError):validate_run(row,self.baseline)

    def test_changed_value_and_missing_release_fail(self):
        for key,value in [('released',False),('class','different'),('parameters',[])]:
            row=copy.deepcopy(self.rows[-1])
            events=[json.loads(x) for x in row['stdout'].splitlines()]
            events[4][key]=value
            row['stdout']='\n'.join(json.dumps(x) for x in events)
            with self.assertRaises(ValueError):validate_run(row,self.baseline)

    def test_sandbox_check_is_required(self):
        row=copy.deepcopy(self.rows[0]);row['stdout']=row['stdout'].replace('true','false',1)
        with self.assertRaises(ValueError):validate_run(row,self.baseline)


class SymbolBuildTests(unittest.TestCase):
    def test_guards_are_selected_from_each_build(self):
        old=json.loads(manifest_for('18.0.9246').read_text())
        new=json.loads(manifest_for('18.0.9644').read_text())
        header=guard_header(old)
        self.assertIn(old['routines']['create_candidate']['start']+'ULL',header)
        self.assertNotIn(new['routines']['create_candidate']['start']+'ULL',header)
        self.assertIn(old['image_uuid'],header)
        self.assertNotIn(new['image_uuid'],header)
        with self.assertRaises(ValueError):manifest_for('18.0.9999')

    def test_cross_build_capture_cannot_claim_same_build(self):
        capture=json.loads((ROOT/'tests/offline-parser-9246-initial.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'capture.json'
            path.write_text(json.dumps(capture))
            result=check_capture(path)
            self.assertIn('cross-build',result['comparison'])
            capture['comparison_kind']='same_build'
            path.write_text(json.dumps(capture))
            with self.assertRaisesRegex(ValueError,'mislabeled'):check_capture(path)

    def test_named_manifest_has_local_layout_and_release_evidence(self):
        manifest=json.loads(manifest_for('18.0.9246').read_text())
        evidence=manifest['layout_evidence']
        for key in ('vector_begin_end_and_stride','vector_end_capacity','initial_reference','release','argument_abi','string_storage'):
            self.assertTrue(evidence[key])
        self.assertEqual(manifest['routines']['create_candidate']['symbol'],'IAction::create(char const*, char const**, int)')
        self.assertEqual(int(manifest['expected_vtable'],16),int(manifest['named_vtable_symbol_address'],16)+16)


if __name__=='__main__':unittest.main()
