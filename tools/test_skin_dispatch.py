"""Keep reviewed dispatch rules, mechanical sites and open items distinct."""
import unittest
from skin_dispatch import DEFAULT, check, describe, load


class DispatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load(DEFAULT)

    def test_saved_capture_passes_its_own_check(self):
        self.assertEqual(check(self.data), [])

    def test_factory_directives_create_no_object_and_say_what_they_do(self):
        branches = self.data["dispatch"]["factory"]["branches"]
        for name in ("window", "define", "onload", "font"):
            self.assertEqual(branches[name]["role"], "directive")
            self.assertIn("rule", branches[name]["effect"])
        self.assertEqual(branches["button"]["role"], "object")
        self.assertEqual(branches["text"]["classes"], ["CSkinTextGroup", "CSkinText"])

    def test_a_tag_keeps_every_context_it_plays_a_role_in(self):
        # `group` is a flattening wrapper in the panel loader and a CSkinPanel in the factory.
        group = describe(self.data, "group")
        self.assertEqual(group["factory"]["classes"], ["CSkinPanel"])
        self.assertIn("wrapper", group["roles"])
        # `panel` under a rack unit is a different class from the factory's panel.
        panel = describe(self.data, "panel")
        rack = [r for r in panel["loaders"] if r["loader"] == "CSkinRack::addUnitChildren"]
        self.assertIn("CSkinResizePanel", rack[0]["rule"])

    def test_child_slots_carry_a_role_and_an_address(self):
        lookups = describe(self.data, "clipmask")["child_lookups"]
        self.assertTrue(lookups)
        self.assertTrue(all(row["pc"].startswith("0x") and row["role"] for row in lookups))

    def test_computed_names_are_listed_not_dropped(self):
        self.assertTrue(self.data["unresolved"]["computed_names"])
        self.assertFalse(any(s["name"] for s in self.data["unresolved"]["computed_names"]
                             if "name" in s))


if __name__ == "__main__":
    unittest.main()
