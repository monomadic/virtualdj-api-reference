"""Preserve consumer-specific activation results and the controls that limit them."""
import json
import unittest
from pathlib import Path
from build_runtime_effect_boolean_cases import build, OUT, CONFIRMATION
from runtime_grammar_actions import validate, check_capture
from runtime_grammar_probes import separation


class EffectBooleanEvidence(unittest.TestCase):
    def test_frozen_suites_preserve_failures_and_control_shapes(self):
        for confirmation, path in ((False, OUT), (True, CONFIRMATION)):
            suite = build(confirmation)
            self.assertEqual(suite, json.loads(path.read_text()))
            validate(suite)
        old = {c['id']: c for c in build()['cases']}
        for row in build(True)['cases']:
            if row['id'] in old:
                self.assertEqual(row['expected'], old[row['id']]['expected'])
            if row['id'].endswith(('quoted-on', 'quoted-off', 'raw-action-text', 'raw-action-zero')):
                self.assertTrue(all(c.endswith(("'zzqqx'", "'vvnnz'")) for c in row['controls']))
            if 'unclosed-' in row['id']:
                self.assertTrue(all(c.endswith(('`zzqqx', '`vvnnz')) for c in row['controls']))

    def test_shared_scripts_repeat_but_plain_text_is_not_evaluation_proof(self):
        initial = check_capture(Path('tests/runtime-grammar-effect-boolean-initial-9628.json'))
        confirmation = check_capture(Path('tests/runtime-grammar-effect-boolean-9628.json'))
        self.assertEqual(initial['summary']['build'], '9628')
        self.assertEqual(confirmation['summary']['build'], '9628')
        old = {c['id']: c for c in initial['cases']}
        for row in confirmation['cases']:
            self.assertIn(row['verdict'], ('held-in-fixture', 'prediction-not-held'))
            if row['id'] in old:
                self.assertEqual(row['passes'][0][row['script']],
                                 old[row['id']]['passes'][0][row['script']])
            label = row['id']
            if label.endswith(('computed-positive', 'computed-zero', 'computed-negative',
                               'boolean-true', 'boolean-false', 'quoted-expression')):
                self.assertEqual(row['verdict'], 'held-in-fixture')
                self.assertEqual(separation(row), 'separates')
            elif label.endswith(('float-literal', 'percent-literal',
                                 'computed-float-one', 'computed-float-fraction')):
                self.assertEqual(row['verdict'], 'held-in-fixture')
                self.assertEqual(separation(row), 'matches-controls')
            elif label.endswith(('quoted-on', 'quoted-off', 'raw-action-text', 'raw-action-zero')):
                self.assertEqual(separation(row), 'matches-controls')
                self.assertEqual(row['verdict'], 'prediction-not-held' if '-selected-' in label
                                 else 'held-in-fixture')
            elif 'unclosed-' in label:
                self.assertEqual(row['verdict'], 'prediction-not-held')
                self.assertEqual(separation(row), 'matches-controls')
            else:
                self.assertEqual(row['verdict'], 'held-in-fixture')
                self.assertEqual(separation(row), 'separates')


if __name__ == '__main__':
    unittest.main()
