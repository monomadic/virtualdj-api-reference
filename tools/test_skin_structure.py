"""Keep broad structural identities separate from behavior and descendants."""
import json
import unittest
from skin_structure import DEFAULT, describe


class StructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(DEFAULT.read_text())

    def test_aliases_reference_one_reader_definition(self):
        refs=[describe(self.data,t)['reader_refs'] for t in ('panel','group','pannel')]
        self.assertEqual(refs[0],refs[1])
        self.assertEqual(refs[0],refs[2])

    def test_button_knows_text_children_without_inheriting_text_attributes(self):
        row=describe(self.data,'button')
        self.assertIn('text',row['direct_child_candidates'])
        self.assertIn('textdown',row['direct_child_candidates'])
        self.assertEqual(self.data['elements']['textdown']['kind'],'reader_child_identity')
        self.assertNotIn('coloroverselected',row['own_attribute_candidates'])
        self.assertIn('clickthrough',row['own_attribute_candidates'])
        self.assertEqual(row['status'],'partial_structure')

    def test_nonstandard_binding_and_unknown_initialization_stay_distinct(self):
        edit=self.data['elements']['edit']['variants']
        self.assertTrue(all(v['factory_binding_verified'] and v['xml_register']=='x2' for v in edit))
        window=self.data['elements']['window']['variants']
        self.assertTrue(any(not v['factory_binding_verified'] and v['binding_gap'] for v in window))

    def test_parent_observation_does_not_promote_behavior(self):
        button=describe(self.data,'button')
        self.assertIn('panel',button['observed_vendor_parents'])
        self.assertIn('Observed',button['parent_evidence'])
        self.assertTrue(button['parent_source_matches_capture'])
        self.assertEqual(describe(self.data,'font')['own_attribute_candidates'],[])


if __name__=='__main__':unittest.main()
