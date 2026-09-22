"""Check conservative provenance and independent native/control agreement."""
import hashlib
import json
from pathlib import Path
import unittest

from tail_consumers import flow
from test_skin_schema import Instruction as I, imm, reg

ROOT = Path(__file__).resolve().parents[1]


class TailTests(unittest.TestCase):
    def test_parameter_index_and_text_member(self):
        code = [I(0, 'mov', [reg('w1'), imm(2)], ['w1']),
                I(4, 'bl', [imm(200)]),
                I(8, 'add', [reg('x0'), reg('x0'), imm(8)], ['x0']),
                I(12, 'bl', [imm(300)])]
        self.assertEqual(flow(code, 200)[-1][1]['x0'], frozenset({('param_text', 2)}))

    def test_unknown_receiver_does_not_become_parameter(self):
        code = [I(0, 'bl', [imm(999)]), I(4, 'mov', [reg('w1'), imm(0)], ['w1']),
                I(8, 'bl', [imm(200)]), I(12, 'bl', [imm(300)])]
        self.assertNotIn('x0', flow(code, 200)[-1][1])

    def test_branch_unknown_is_retained(self):
        code = [I(0, 'mov', [reg('w1'), imm(0)], ['w1']), I(4, 'bl', [imm(200)]),
                I(8, 'cbz', [reg('x8'), imm(16)]), I(12, 'ldr', [reg('x0')], ['x0']),
                I(16, 'bl', [imm(300)])]
        self.assertEqual(flow(code, 200)[-1][1]['x0'], frozenset({('param', 0), ('unknown', '')}))

    def test_localization_is_not_argument_provenance(self):
        data = json.loads((ROOT / 'tests/tail-consumers-9246.json').read_text())
        sites = [s for s in data['literal_sites'] if data['routines'][s['function']]['symbol'].startswith('ACTION_filter_label::')]
        args = {v for s in sites if s['comparison'] and not s['receiver_unresolved']
                for v in s['literal_arguments'].get('x1', [])}
        self.assertEqual(args, {'name', 'clean'})
        localized = {v for s in sites if s['callee'] and s['callee'].startswith('CMessageEngine::getMessage(')
                     for values in s['literal_arguments'].values() for v in values}
        self.assertEqual(localized, {'Skin', 'BASS', 'FILTER'})

    def test_native_controls_and_capture_provenance(self):
        journal = json.loads((ROOT / 'tests/tail-probe-9246.json').read_text())
        self.assertTrue(journal['complete'])
        self.assertEqual(journal['before'], journal['after'])
        self.assertEqual(set(journal['before'].values()), {'no'})
        self.assertEqual(journal['execute_calls'], [])
        for name in ('VDJMemoryProbe', 'VDJKeywordProbe'):
            row = journal[name]
            self.assertEqual(hashlib.sha256((ROOT / row['capture']).read_bytes()).hexdigest(), row['sha256'])
        rows = [json.loads(s) for s in (ROOT / journal['VDJKeywordProbe']['capture']).read_text().splitlines()]
        self.assertEqual(rows[0]['build'], 9246)
        self.assertEqual(rows[-1], {'event': 'complete'})
        groups = [{r['script']: {k: v for k, v in r.items() if k not in ('round', 'event', 'script')}
                   for r in rows if r.get('round') == n} for n in (1, 2)]
        suite = json.loads((ROOT / 'tests/is-using-keyword-cases.json').read_text())['scripts']
        self.assertEqual(list(groups[0]), suite)
        self.assertEqual(groups[0], groups[1])
        self.assertEqual(groups[0]['is_using cue']['numeric_hresult'], 0)
        self.assertEqual(groups[0]['is_using zzunknowna'], groups[0]['is_using zzunknownb'])
        self.assertEqual(groups[0]['is_using inaudible'], groups[0]['is_using zzunknowna'])
        self.assertEqual(groups[0]['is_using zzunknowna']['numeric_hresult'], -2147467263)
        for a, b in [('is_using cue inaudible', 'is_using cue zzunknowna'),
                     ('is_using cue 1000ms inaudible', 'is_using cue 1000ms zzunknowna')]:
            self.assertEqual(groups[0][a], groups[0][b])
        http = [{r['script']: r['result'] for r in journal['results'] if r['round'] == n} for n in (1, 2)]
        self.assertEqual(http[0], http[1])
        self.assertEqual(http[0]["deck 1 filter_label 'clean'"], 'OFF')
        self.assertEqual(http[0]["deck 1 filter_label 'zzunknowna'"], 'DELAY')


if __name__ == '__main__':
    unittest.main()
