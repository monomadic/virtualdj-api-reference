"""Safety boundaries for playback fixture setup and cleanup."""
import copy
import json
import tempfile
from pathlib import Path
import unittest
from fixtures import FixtureError
from runtime_grammar_playing import GUARDS, PROTECTED, PlayingSession, validate, check_capture


class FakeChannel:
    def __init__(self):
        self.state = {q: 'no' for q in GUARDS + PROTECTED}
        self.state.update({'get_decks': '4', 'get_deck': '1', 'masterdeck_auto': 'yes',
                           'deck 1 masterdeck': 'yes', 'deck 1 select': 'yes'})
        for d in range(1, 5):
            for q in ('volume', 'pitch', 'get_position'):
                self.state[f'deck {d} {q}'] = '0.5'
        self.sent = []

    def query(self, script):
        return self.state.get(script, '')

    def execute(self, script):
        self.sent.append(script)
        raise TimeoutError('response uncertain')


class PlayingSafetyTests(unittest.TestCase):
    def setUp(self):
        self.channel = FakeChannel()
        self.capture = {'summary': {}, 'journal': [], 'restorations': [], 'cases': []}
        self.session = PlayingSession(self.channel, self.capture, None, Path('/tmp/h4-test-silence.wav'))

    def test_refuses_loaded_fixture_deck_before_writes(self):
        self.channel.state['deck 3 loaded'] = 'yes'
        with self.assertRaises(FixtureError):
            self.session.snapshot()
        self.assertEqual(self.channel.sent, [])

    def test_refuses_playing_protected_deck_before_writes(self):
        self.channel.state['deck 2 play'] = 'yes'
        with self.assertRaises(FixtureError):
            self.session.snapshot()
        self.assertEqual(self.channel.sent, [])

    def test_foreign_media_is_never_unloaded(self):
        self.session.snapshot()
        self.channel.state['deck 3 loaded'] = 'yes'
        self.channel.state['deck 3 get_loaded_song "fullpath"'] = '/unrelated.wav'
        with self.assertRaises(FixtureError):
            self.session.restore()
        self.assertEqual(self.channel.sent, [])
        self.assertTrue(self.capture['summary']['manual_restore_required'])

    def test_write_allowlist_excludes_protected_transport_and_arbitrary_files(self):
        self.session.snapshot()
        for script in ('deck 1 play', 'deck 2 unload', 'deck 3 load "/unrelated.wav"', 'system'):
            with self.assertRaises(FixtureError):
                self.session.write(script, 'test')
        self.assertEqual(self.channel.sent, [])

    def test_uncertain_mutation_is_journaled_and_not_repeated(self):
        self.session.snapshot()
        with self.assertRaises(TimeoutError):
            self.session.write('deck 3 play', 'test')
        self.assertEqual(self.channel.sent, ['deck 3 play'])
        self.assertEqual(self.capture['journal'][0]['status'], 'response-uncertain')

    def test_suite_refuses_execute_payloads_in_query_cases(self):
        suite = json.loads(Path('tests/runtime-grammar-playing-cases.json').read_text())
        validate(suite)
        suite['cases'][0]['script'] = 'deck 1 load "x"'
        with self.assertRaises(FixtureError):
            validate(suite)


class PlayingEvidenceTests(unittest.TestCase):
    def test_complete_and_aborted_captures_remain_checkable(self):
        for name in ('playing', 'playing-initial'):
            check_capture(Path(f'tests/runtime-grammar-{name}-9598.json'))

    def test_rejects_unverified_movement_context_restore_and_journal(self):
        capture = json.loads(Path('tests/runtime-grammar-playing-9598.json').read_text())
        for mutate in (
            lambda c: c['phases'][0].update(advancing_position=[0, 0]),
            lambda c: c['phases'][0]['checks'][0]['state'].update({'deck 3 play': 'yes'}),
            lambda c: c['restorations'][0]['guards'].update({'deck 4 loaded': 'yes'}),
            lambda c: c['summary'].update(manual_restore_required=True),
            lambda c: c['journal'][0].update(script='deck 1 unload'),
            lambda c: c['journal'][0].update(status='response-uncertain'),
        ):
            changed = copy.deepcopy(capture)
            mutate(changed)
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'capture.json'
                path.write_text(json.dumps(changed))
                with self.assertRaises(FixtureError):
                    check_capture(path)


if __name__ == '__main__':
    unittest.main()
