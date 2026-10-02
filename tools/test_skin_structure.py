"""Keep broad structural identities separate from behavior and descendants."""
import hashlib
import json
import unittest
from skin_structure import DEFAULT, RELATIONS, describe


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

    def test_nonstandard_bindings_are_explicit(self):
        edit=self.data['elements']['edit']['variants']
        self.assertTrue(all(v['factory_binding_verified'] and v['xml_register']=='x2' for v in edit))
        # The window is default-constructed and receives its node through CSkinWindow::load,
        # so its binding is that call, not the constructor.
        window=self.data['elements']['window']['variants']
        self.assertTrue(all(v['factory_binding_verified'] and v['binding_gap'] is None for v in window))
        self.assertEqual({v['initializer']['symbol'] for v in window},
                         {'CSkinWindow::load(CXMLNode*, CImage*, char const*)'})
        self.assertTrue(all('initializer' not in v for t,e in self.data['elements'].items()
                            if t!='window' for v in e['variants']))

    def test_parent_observation_does_not_promote_behavior(self):
        button=describe(self.data,'button')
        self.assertIn('panel',button['observed_vendor_parents'])
        self.assertIn('Observed',button['parent_evidence'])
        # The flag must report whether the relations corpus still matches the one the
        # capture pinned; observed parents always come from the current vendor XML report.
        current=hashlib.sha256(RELATIONS.read_bytes()).hexdigest()
        self.assertEqual(button['parent_source_matches_capture'],
                         current==self.data['anchors']['tests/skin-xml-relations.json'])
        self.assertEqual(describe(self.data,'font')['own_attribute_candidates'],[])


if __name__=='__main__':unittest.main()
