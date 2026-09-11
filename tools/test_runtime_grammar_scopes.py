import copy
import json
from pathlib import Path
import unittest
from fixtures import FixtureError
from runtime_grammar_scopes import SelectedSession, validate
from test_runtime_grammar_actions import Fake

class SelectionFake(Fake):
    def __init__(self):
        super().__init__(); self.broken_pfl=False
        self.state['deck 1 select']='yes';self.state['deck 1 pfl']='yes'
    def execute(self,s):
        if s.endswith(' select'):
            self.writes.append(s); d=s.split()[1];self.state['get_deck']=d
            for i in range(1,5):
                self.state[f'deck {i} select']='yes' if str(i)==d else 'no'
                if not self.broken_pfl: self.state[f'deck {i} pfl']='yes' if str(i)==d else 'no'
            return 'true'
        return super().execute(s)

class Tests(unittest.TestCase):
    def session(self,ch):
        cap={'summary':{},'cases':[],'journal':[],'baseline_checks':[],'restorations':[]}
        s=SelectedSession(ch,cap,None);s.snapshot();return s
    def test_scope_restores_selection_pfl(self):
        ch=SelectionFake();s=self.session(ch)
        self.assertEqual(s.sample_query(['2'],'get_deck',2),[['2'],['2']])
        self.assertEqual(ch.state['get_deck'],'1')
        self.assertEqual(ch.state['deck 1 pfl'],'yes')
        self.assertEqual(s.capture['summary']['restoration_status'],'verified')
    def test_collateral_pfl_is_not_repaired_by_guess(self):
        ch=SelectionFake();s=self.session(ch);ch.broken_pfl=True;ch.state['deck 3 pfl']='yes'
        with self.assertRaises(FixtureError):s.sample_query(['2'],'get_deck',2)
        self.assertTrue(s.capture['summary']['manual_restore_required'])
        self.assertFalse(any('pfl' in x for x in ch.writes))
    def test_scope_candidate_cannot_execute(self):
        x=json.loads(Path('tests/runtime-grammar-scope-cases.json').read_text());x['cases'][0]['script']='deck 2 select'
        with self.assertRaises(ValueError):validate(x)

if __name__=='__main__':unittest.main()
