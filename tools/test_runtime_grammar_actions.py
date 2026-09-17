"""Regression tests for mutation/restoration and discriminating verdicts."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from fixtures import FixtureError
from runtime_grammar_actions import (Session, FIXTURES, GUARDS, RESOURCES, OnceChannel,
                                     EFFECT_FIXTURES, EFFECT_GUARDS, EFFECT_RESOURCES,
                                     allowed_scripts, classify, validate)

class Fake:
    def __init__(self):
        self.state = dict.fromkeys(GUARDS, 'no')
        self.state.update({'get_decks': '4', 'get_deck': '1', 'zoom': '0.31'})
        self.state.update({q: 'no' for q in RESOURCES[1:]})
        self.writes = []
        self.ignore_restore = False
        self.fail_restore = False
        self.fail_probe = False
    def query(self, q):
        return self.state[q]
    def execute(self, s):
        self.writes.append(s)
        q, value = s.rsplit(' ', 1)
        if self.fail_probe and s == 'zoom +0.25':
            raise ConnectionResetError('response lost')
        if self.ignore_restore and s == 'zoom 0.310000000':
            return 'false'
        if self.fail_restore and s == 'zoom 0.310000000':
            raise ConnectionResetError('restore response lost')
        self.state[q] = {'on':'yes', 'off':'no'}.get(value,value)
        return 'false' # Return is not the readback.

class Tests(unittest.TestCase):
    def test_incoming_zoom_chains_are_finite_and_zoom_only(self):
        expected = {
            f'constant {source}{bridge} & zoom' + (f' {tail}' if tail else '')
            for source in ('0.37', '0.83', '0.41', '0.79')
            for bridge in ('', ' & param_cast float')
            for tail in ('', '0.25', '0.0', '+0.25', 'default', 'zzqqx', 'vvnnz')
        }
        zoom = allowed_scripts('parser_zoom_levels')
        self.assertEqual({script for script in zoom if '&' in script}, expected)
        for fixture in ('parser_beatlock_levels', 'parser_all_decks_asymmetric',
                        'parser_effect_boolean'):
            with self.subTest(fixture=fixture):
                self.assertFalse(expected & allowed_scripts(fixture))
                self.assertFalse(any('&' in script for script in allowed_scripts(fixture)))

    def test_incoming_zoom_rejects_unbounded_sources_consumers_and_casts(self):
        rejected = (
            'constant 0.38 & zoom',
            'constant `get_var x` & zoom',
            'get_var x & zoom',
            'constant 0.37 & play',
            'constant 0.37 & deck 1 beatlock',
            'constant 0.37 & deck 1 effect_active 1',
            'constant 0.37 & zoom & play',
            'constant 0.37 & param_cast float & zoom & play',
            'constant 0.37 & param_cast integer & zoom',
            'constant 0.37 & param_cast text & zoom',
            'constant 0.37 & param_cast float & param_cast float & zoom',
            'constant 0.37 & zoom 0.37',
            'constant 0.37 & zoom `constant 0.25`',
        )
        for fixture in (*FIXTURES, *EFFECT_FIXTURES):
            allowed = allowed_scripts(fixture)
            for script in rejected:
                with self.subTest(fixture=fixture, script=script):
                    self.assertNotIn(script, allowed)

    def effect_session(self):
        ch = Fake()
        ch.state.update(dict.fromkeys(EFFECT_GUARDS, 'no'))
        ch.state.update({'get_decks': '4', 'get_deck': '1',
                         'deck 1 get_effect_name 1': 'Phaser', EFFECT_RESOURCES[0]: 'no'})
        session = self.session(ch)
        session.capture['fixtures'] = EFFECT_FIXTURES
        return ch, Session(ch, session.capture, None)

    def test_effect_requires_existing_phaser_without_selecting_it(self):
        ch, session = self.effect_session()
        ch.state['deck 1 get_effect_name 1'] = 'Echo'
        with self.assertRaises(FixtureError):
            session.snapshot()
        self.assertEqual(ch.writes, [])

    def test_effect_restores_target_and_rejects_collateral_change(self):
        ch, session = self.effect_session()
        session.snapshot()
        fixture = EFFECT_FIXTURES['parser_effect_boolean']
        reads = session.sample(fixture, ['no'], 'deck 1 effect_active 1 on', 2)
        self.assertEqual(reads, [['yes'], ['yes']])
        self.assertEqual(ch.state[EFFECT_RESOURCES[0]], 'no')
        ch.state['deck 1 effect_slider 1 1'] = '0.9'
        with self.assertRaises(FixtureError):
            session.restore()

    def test_effect_guard_drift_prevents_new_probe(self):
        ch, session = self.effect_session()
        session.snapshot()
        ch.state['deck 1 loaded'] = 'yes'
        with self.assertRaises(FixtureError):
            session.sample(EFFECT_FIXTURES['parser_effect_boolean'], ['yes'],
                           'deck 1 effect_active 1 off', 2)
        self.assertEqual(ch.writes, [])

    def test_effect_identity_drift_prevents_restore_to_replacement(self):
        ch, session = self.effect_session()
        session.snapshot()
        ch.state['deck 1 get_effect_name 1'] = 'Echo'
        ch.state[EFFECT_RESOURCES[0]] = 'yes'
        with self.assertRaises(FixtureError):
            session.restore()
        self.assertEqual(ch.writes, [])
        self.assertEqual(session.capture['summary']['restoration_status'], 'failed')
        self.assertTrue(session.capture['summary']['manual_restore_required'])

    def test_effect_rejects_other_slots_effects_nested_writes_and_mixed_profiles(self):
        from build_runtime_effect_boolean_cases import build
        for script in ('deck 1 effect_active 2 on', "deck 1 effect_active 1 'Echo' on",
                       'deck 1 effect_active 1 `play`', 'deck 1 effect_active 1 on & play'):
            suite = build()
            suite['cases'][0]['script'] = script
            with self.assertRaises(ValueError):
                validate(suite)
        suite = build()
        suite['cases'].append(json.loads(Path('tests/runtime-grammar-action-cases.json').read_text())['cases'][0])
        with self.assertRaises(ValueError):
            validate(suite)

    def session(self, ch):
        cap = {'summary': {}, 'cases': [], 'journal': [], 'restorations': [], 'baseline_checks': []}
        return Session(ch,cap,None)
    def test_precondition_before_write(self):
        ch = Fake(); ch.state['deck 4 loaded']='yes'
        with self.assertRaises(FixtureError): self.session(ch).snapshot()
        self.assertEqual(ch.writes, [])
    def test_failed_restore_aborts(self):
        ch=Fake(); s=self.session(ch); s.snapshot(); ch.ignore_restore=True
        with self.assertRaises(FixtureError):
            s.sample(FIXTURES['parser_zoom_levels'], ['0.25'], 'zoom 0.0', 2)
    def test_uncertain_probe_restores_without_replay(self):
        ch=Fake(); s=self.session(ch); s.snapshot(); ch.fail_probe=True
        with self.assertRaises(ConnectionResetError):
            s.sample(FIXTURES['parser_zoom_levels'], ['0.25'], 'zoom +0.25', 2)
        self.assertEqual(ch.writes.count('zoom +0.25'),1)
        self.assertEqual(float(ch.state['zoom']),0.31)

    def test_successful_write_is_persisted(self):
        ch=Fake();
        with tempfile.TemporaryDirectory() as d:
            path=Path(d) / 'capture.json'
            s=self.session(ch); s.path=path; s.snapshot()
            s.write('zoom 0.25', 'probe')
            saved=json.loads(path.read_text())
            self.assertEqual(saved['journal'][-1]['status'], 'response-received')

    def test_uncertain_restore_is_durable_and_flagged(self):
        ch=Fake(); s=self.session(ch); s.snapshot(); ch.fail_restore=True
        with self.assertRaises(ConnectionResetError):
            s.sample(FIXTURES['parser_zoom_levels'], ['0.25'], 'zoom 0.0', 2)
        self.assertEqual(s.capture['restoration_events'][-1]['status'], 'failure')
        self.assertEqual(s.capture['summary']['restoration_status'], 'failed')
        self.assertTrue(s.capture['summary']['manual_restore_required'])
    def test_transport_never_retries(self):
        with patch('runtime_grammar_actions.http.client.HTTPConnection') as ctor:
            ctor.return_value.getresponse.side_effect=ConnectionResetError()
            channel = OnceChannel()
            with self.assertRaises(ConnectionResetError): channel.execute('zoom +0.25')
            self.assertEqual(ctor.call_count, 1)
            self.assertEqual(ctor.return_value.request.call_count,1)
            ctor.return_value.close.assert_called_once_with()
            self.assertIsNone(channel._conn)
    def test_transport_closes_previous_connection_before_each_write(self):
        channel = OnceChannel()
        stale = Mock()
        channel._conn = stale
        events = []
        stale.close.side_effect = lambda: events.append('close-stale')
        first, second = Mock(), Mock()
        for connection in (first, second):
            connection.getresponse.return_value.read.return_value = b'false'
        first.request.side_effect = lambda *args: events.append('send-first')
        first.close.side_effect = lambda: events.append('close-first')
        second.request.side_effect = lambda *args: events.append('send-second')
        with patch('runtime_grammar_actions.http.client.HTTPConnection',
                   side_effect=[first, second]) as ctor:
            self.assertEqual(channel.execute('zoom 0.25'), 'false')
            self.assertEqual(channel.execute('zoom 0.65'), 'false')
            self.assertEqual(ctor.call_count, 2)
        self.assertEqual(events, ['close-stale', 'send-first', 'close-first', 'send-second'])
        stale.request.assert_not_called()
        first.request.assert_called_once()
        second.request.assert_called_once()
    def test_collateral_change_aborts(self):
        ch=Fake(); s=self.session(ch); s.snapshot(); ch.state['get_deck']='2'
        with self.assertRaises(FixtureError): s.restore()
    def test_reject_arbitrary_action(self):
        suite=json.loads(Path('tests/runtime-grammar-action-cases.json').read_text())
        suite['cases'][0]['script']='zoom 0.25 & play'
        with self.assertRaises(ValueError): validate(suite)
    def test_bad_oracle_cannot_hold(self):
        c=copy.deepcopy(json.loads(Path('tests/runtime-grammar-action-cases.json').read_text())['cases'][0])
        scripts=[c['script'], *c['controls'], *(x['script'] for x in c['contrasts'])]
        c['passes']=[{s:[[['0.25'],['0.25']], [['0.25'],['0.25']]] for s in scripts}]*2
        self.assertEqual(classify(c),'inconclusive-oracle')

if __name__=='__main__': unittest.main()
