"""Regressions for the asymmetric-master fixture: pin, refuse, restore, verify."""
import json
from pathlib import Path
import tempfile
import unittest

from fixtures import FixtureError
from runtime_grammar_master import (BASELINES, MasterScopeSession, check_capture,
                                    separation, signatures, validate)
from test_runtime_grammar_scopes import SelectionFake


class MasterFake(SelectionFake):
    """Master is exclusive across decks, as the live app was observed to behave."""

    def __init__(self):
        super().__init__()
        self.state['deck 1 masterdeck'] = 'yes'
        self.state['masterdeck_auto'] = 'yes'
        self.pin_fails = False

    def execute(self, s):
        if s.endswith(' masterdeck on'):
            self.writes.append(s)
            if self.pin_fails:
                return 'true'  # Accepted, but the state does not move.
            deck = s.split()[1]
            for i in range(1, 5):
                self.state[f'deck {i} masterdeck'] = 'yes' if str(i) == deck else 'no'
            return 'true'
        return super().execute(s)


class Tests(unittest.TestCase):
    def session(self, ch, path=None):
        capture = {'summary': {}, 'cases': [], 'journal': [],
                   'baseline_checks': [], 'restorations': []}
        s = MasterScopeSession(ch, capture, path)
        s.snapshot()
        return s

    def test_asymmetric_baseline_is_restored(self):
        ch = MasterFake()
        s = self.session(ch)
        self.assertEqual(s.sample_queries(['1', '2'], ['get_deck'], 2), {'get_deck': [['1'], ['1']]})
        self.assertEqual(ch.state['deck 1 masterdeck'], 'yes')
        self.assertEqual(ch.state['deck 2 masterdeck'], 'no')
        self.assertEqual(ch.state['masterdeck_auto'], 'yes')
        self.assertEqual(ch.state['get_deck'], '1')
        self.assertEqual(s.capture['summary']['restoration_status'], 'verified')

    def test_master_auto_is_parked_and_put_back(self):
        ch = MasterFake()
        s = self.session(ch)
        s.sample_queries(['1', '2'], ['get_deck'], 2)
        self.assertIn('masterdeck_auto off', ch.writes)
        self.assertIn('masterdeck_auto on', ch.writes)
        self.assertEqual(ch.state['masterdeck_auto'], 'yes')

    def test_pin_that_does_not_hold_aborts(self):
        ch = MasterFake()
        s = self.session(ch)
        ch.pin_fails = True
        with self.assertRaises(FixtureError):
            s.sample_queries(['1', '2'], ['get_deck'], 2)

    def test_ambiguous_master_refuses_before_any_write(self):
        ch = MasterFake()
        ch.state['deck 3 masterdeck'] = 'yes'
        with self.assertRaises(FixtureError):
            self.session(ch)
        self.assertEqual(ch.writes, [])

    def test_loaded_deck_refuses_before_any_write(self):
        ch = MasterFake()
        ch.state['deck 2 loaded'] = 'yes'
        with self.assertRaises(FixtureError):
            self.session(ch)
        self.assertEqual(ch.writes, [])

    def test_candidate_cannot_execute(self):
        suite = json.loads(Path('tests/runtime-grammar-master-cases.json').read_text())
        suite['cases'][0]['script'] = 'deck 2 masterdeck on'
        with self.assertRaises(ValueError):
            validate(suite)

    def test_separation_flags_a_control_shaped_result(self):
        case = {'id': 'x', 'script': 'deck master get_deck',
                'controls': ['deck zzqqx get_deck', 'deck vvnnz get_deck'],
                'verdict': 'held-in-fixture',
                'passes': [{'deck master get_deck': [[['1']], [['2']]],
                            'deck zzqqx get_deck': [[['1']], [['2']]]}]}
        self.assertEqual(separation({'cases': [case]}), {'x': 'matches-controls'})
        case['passes'][0]['deck master get_deck'] = [[['2']], [['3']]]
        self.assertEqual(separation({'cases': [case]}), {'x': 'separates'})

    def test_signature_names_the_state_a_selector_tracks(self):
        def case(observed):
            return {'id': 'x', 'script': 'deck s get_deck', 'verdict': 'held-in-fixture',
                    'controls': ['deck zzqqx get_deck', 'deck vvnnz get_deck'],
                    'passes': [{'deck s get_deck': [[[v]] for v in observed]}]}
        # BASELINES is (selection, master) = (1, 2) then (2, 3).
        self.assertEqual(signatures({'cases': [case(['2', '3'])]}), {'x': 'tracks-master-deck'})
        self.assertEqual(signatures({'cases': [case(['1', '2'])]}), {'x': 'tracks-selected-deck'})
        self.assertEqual(signatures({'cases': [case(['4', '4'])]}), {'x': 'fixed-deck-4'})
        self.assertEqual(signatures({'cases': [case(['1', '4'])]}), {'x': 'unclassified'})
        self.assertEqual(signatures({'cases': [case(['x', 'x'])]}), {'x': 'unclassified'})

    def test_check_rejects_a_symmetric_baseline(self):
        capture = {'summary': {'suite': 'tests/runtime-grammar-master-cases.json',
                               'status': 'complete', 'rounds_requested': 2, 'rounds_completed': 2,
                               'repeat': 2, 'build': '9598', 'channel': 'HTTP', 'verdicts': {},
                               'separation': {}, 'signatures': {}},
                   'baselines': [['1', '1'], ['2', '2']], 'cases': [], 'journal': [],
                   'baseline_checks': [], 'restorations': []}
        suite = Path('tests/runtime-grammar-master-cases.json')
        capture['summary']['suite_sha256'] = __import__('hashlib').sha256(
            suite.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'capture.json'
            path.write_text(json.dumps(capture))
            with self.assertRaisesRegex(ValueError, 'baseline drift'):
                check_capture(path)

    def test_baselines_pull_selection_and_master_apart(self):
        # Without both properties the suite cannot separate "follows master"
        # from "constant deck N", which is the only reason this fixture exists.
        self.assertTrue(all(sel != master for sel, master in BASELINES))
        self.assertEqual(len({master for _, master in BASELINES}), len(BASELINES))


if __name__ == '__main__':
    unittest.main()
