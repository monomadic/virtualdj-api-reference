"""Evidence-boundary tests for the bounded XML receiver analysis (stdlib only)."""
import json
from pathlib import Path
from types import SimpleNamespace as NS
import unittest

from skin_schema import UNKNOWN, OVERFLOW, analyze, merge, node_paths, summary, transfer


def reg(name):
    return NS(type=1, reg=name)


def imm(value):
    return NS(type=2, imm=value, shift=NS(type=0, value=0))


class Instruction:
    def __init__(self, address, mnemonic, operands, writes=()):
        self.address, self.mnemonic, self.operands = address, mnemonic, operands
        self.writes = writes

    def reg_name(self, name):
        return name

    def regs_access(self):
        return [], self.writes


NODE = frozenset({('node', '/button')})
GETTERS = {200: {'role': 'child_node'}}


class OwnershipTests(unittest.TestCase):
    def test_join_retains_unknown_alternative(self):
        result = merge({'x0': NODE}, {})
        self.assertEqual(result['x0'], NODE | UNKNOWN)
        self.assertEqual(node_paths(result['x0']), ['/button'])

    def test_widening_is_absorbing(self):
        values = frozenset(('constant', n) for n in range(9))
        result = merge({'x0': values}, {'x0': NODE})
        self.assertEqual(result['x0'], OVERFLOW)
        self.assertEqual(merge(result, {'x0': NODE})['x0'], OVERFLOW)

    def test_child_return_and_call_clobbers(self):
        state = {'x0': NODE, 'x1': frozenset({('constant', 1000)}), 'x8': NODE, 'x21': NODE}
        out = transfer(Instruction(0, 'bl', [imm(200)]), state, GETTERS, {1000: 'icon'})
        self.assertEqual(out['x0'], frozenset({('node', '/button/icon')}))
        self.assertNotIn('x8', out)
        self.assertEqual(out['x21'], NODE)

    def test_unknown_child_name_cannot_create_path(self):
        out = transfer(Instruction(0, 'bl', [imm(200)]), {'x0': NODE}, GETTERS)
        self.assertNotIn('x0', out)

    def test_unknown_helper_return_cannot_inherit_receiver(self):
        out = transfer(Instruction(0, 'bl', [imm(300)]), {'x0': NODE}, GETTERS)
        self.assertNotIn('x0', out)

    def test_narrow_write_destroys_pointer(self):
        out = transfer(Instruction(0, 'mov', [reg('w0'), imm(1)], ['w0']), {'x0': NODE}, GETTERS)
        self.assertNotIn('x0', out)

    def test_unmodeled_load_destroys_pointer(self):
        out = transfer(Instruction(0, 'ldr', [reg('x0')], ['x0']), {'x0': NODE}, GETTERS)
        self.assertNotIn('x0', out)

    def test_both_branch_receivers_survive_join(self):
        instructions = [
            Instruction(0, 'cbz', [reg('x5'), imm(12)]),
            Instruction(4, 'mov', [reg('x0'), reg('x21')], ['x0']),
            Instruction(8, 'b', [imm(16)]),
            Instruction(12, 'mov', [reg('x0'), reg('x22')], ['x0']),
            Instruction(16, 'bl', [imm(300)]),
            Instruction(20, 'ret', []),
        ]
        calls = analyze(instructions, {'x21': NODE, 'x22': frozenset({('node', '/button/icon')})}, GETTERS, {})
        self.assertEqual(node_paths(calls[0][2]['x0']), ['/button', '/button/icon'])

    def test_unreachable_instructions_are_not_reads(self):
        instructions = [Instruction(0, 'b', [imm(8)]), Instruction(4, 'bl', [imm(200)]), Instruction(8, 'ret', [])]
        self.assertEqual(analyze(instructions, {'x0': NODE}, GETTERS, {}), [])

    def test_call_preserves_saved_literal_address(self):
        literal = frozenset({('constant', 1000)})
        instructions = [Instruction(0, 'bl', [imm(300)]), Instruction(4, 'mov', [reg('x1'), reg('x21')], ['x1']),
                        Instruction(8, 'bl', [imm(200)]), Instruction(12, 'ret', [])]
        calls = analyze(instructions, {'x21': literal}, GETTERS, {1000: 'icon'})
        self.assertEqual(calls[1][2]['x1'], literal)


class CaptureTests(unittest.TestCase):
    def test_recorded_ownership_keeps_children_separate(self):
        path = Path(__file__).resolve().parents[1] / 'tests/skin-schema-button-9644.json'
        data = json.loads(path.read_text())
        report = summary(data)
        self.assertIn('sysicon', report['owners']['/button/icon']['attributes'])
        self.assertNotIn('sysicon', report['owners']['/button']['attributes'])
        self.assertIn('r', report['owners']['/button/mousecircle']['attributes'])
        self.assertIn('clickthrough', report['shared_outer_attributes'])
        self.assertTrue(data['frontier'])
        self.assertTrue(any(r['receiver_unresolved'] for r in data['reads']))
        self.assertEqual(data['evidence_tier'], 2)

    def test_partial_ownership_stays_labelled_in_query(self):
        data = {'element': 'button', 'source': {'build': 'test'}, 'frontier': [], 'limitations': [],
                'reads': [{'role': 'attribute_string', 'node_paths': ['/button'], 'names': ['maybe'],
                           'receiver_unresolved': True, 'name_unresolved': False, 'origin': 'helper'}]}
        report = summary(data)
        self.assertEqual(report['owners']['/button']['attributes'], [])
        self.assertEqual(report['owners']['/button']['partial_attributes'], ['maybe'])


if __name__ == '__main__':
    unittest.main()
