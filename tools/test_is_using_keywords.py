import json,unittest
from pathlib import Path
from unittest.mock import patch
from is_using_keywords import check

class KeywordCaptureTests(unittest.TestCase):
    def test_real_captures(self):
        self.assertEqual(check()['first_argument_matches_nonsense'],['inaudible'])

    def test_rejects_corruption(self):
        read=Path.read_text
        for kind in ['truncated','hresult','restore','compiled_cases']:
            with self.subTest(kind=kind):
                def altered(path,*args,**kwargs):
                    text=read(path,*args,**kwargs)
                    if path.name=='is-using-keywords-9644-run1.jsonl':
                        if kind=='truncated':return '\n'.join(text.splitlines()[:-1])
                        if kind=='hresult':return text.replace('"numeric_hresult":0','"numeric_hresult":-1',1)
                    if path.name=='is-using-keyword-run-9644.json' and kind=='restore':
                        x=json.loads(text);x['state_checks_match']=False;return json.dumps(x)
                    if path.name=='is_using_cases.h' and kind=='compiled_cases':return text+'// drift\n'
                    return text
                with patch.object(Path,'read_text',altered),self.assertRaises(ValueError):check()

if __name__=='__main__':unittest.main()
