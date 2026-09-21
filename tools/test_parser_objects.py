import json,tempfile,unittest
from pathlib import Path
from parser_objects import check

class ParserCaptureTests(unittest.TestCase):
    def test_capture(self):
        self.assertEqual(check(Path('tests/parser-objects-9644.jsonl'))[-1]['parameters'][-1], ('%',0.5))

    def test_rejects_damaged_capture(self):
        original=Path('tests/parser-objects-9644.jsonl').read_text().splitlines()
        for kind in ['truncated','guard','release','parameter','round']:
            with self.subTest(kind=kind),tempfile.TemporaryDirectory() as d:
                rows=[json.loads(s) for s in original]
                if kind=='truncated':rows.pop()
                if kind=='guard':rows[1]['event']='guards_failed'
                if kind=='release':rows[3]['released']=False
                if kind=='parameter':rows[3]['parameters'][0]['text']='zzwrong'
                if kind=='round':rows[11]['numeric_value']=1
                path=Path(d)/'capture.jsonl';path.write_text('\n'.join(json.dumps(r) for r in rows))
                with self.assertRaises(ValueError):check(path)

if __name__=='__main__':unittest.main()
