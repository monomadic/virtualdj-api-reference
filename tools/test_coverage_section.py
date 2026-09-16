"""Offline regressions for section-scoped coverage and alias membership."""
import contextlib
import io
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import coverage_report as report


def context():
    store = {
        "sample": {"name": "sample", "section": "Sampler", "needs_test": True},
        "other": {"name": "other", "section": "Other", "needs_test": True},
        "sample_alias": {"name": "sample_alias", "tier": "alias", "canonical": "sample",
                         "needs_test": True},
        # A stale alias section must not override the canonical's membership.
        "other_alias": {"name": "other_alias", "tier": "alias", "canonical": "other",
                        "section": "Sampler", "needs_test": True},
    }
    return SimpleNamespace(store=store,
                           canon={n: r for n, r in store.items() if r.get("tier") != "alias"},
                           checked={"candidates": {"sample": ["a"], "sample_alias": ["b"],
                                                   "other": ["c", "d"], "unknown": ["e"]}},
                           cc_source="fixture", argforms={}, execforms={}, raw_rtypes={})


def assessment(name, rec, ctx):
    return {"queries": True, "executes": True,
            "dimensions": {d: "open" for d in report.DIMENSIONS},
            "settled": 0, "applicable": 4, "unresolved_tails": [],
            "read_side_complete": False, "complete": False}


class SectionTests(unittest.TestCase):
    def setUp(self):
        for name, value in (("load_context", context()), ("build_stamp", "fixture stamp"),
                            ("contract_names", set()), ("staleness", [])):
            patcher = patch.object(report, name, return_value=value)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = patch.object(report, "assess", side_effect=assessment)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_section_filters_every_population_and_inherits_aliases(self):
        result = report.collect("sampler")
        self.assertEqual(result["section"], "Sampler")
        self.assertEqual(set(result["verbs"]), {"sample"})
        self.assertEqual(result["population"]["store_records"], 2)
        self.assertEqual(result["population"]["aliases"], 1)
        self.assertEqual(result["population"]["canonical"], 1)
        self.assertEqual(result["cross_check"]["candidates"], {"verbs": 2, "tokens": 2})
        self.assertEqual(result["ladder"], {"0/4": 1})
        for dim in report.DIMENSIONS:
            self.assertEqual(result["dimensions"][dim]["_applicable"], 1)
        for names in result["frontier"].values():
            self.assertTrue(set(names) <= {"sample", "sample_alias"})
        self.assertEqual(result["frontier"]["audit_pool"], ["sample", "sample_alias"])
        text = report.render(result, "frontier")
        self.assertIn("Section: Sampler", text)
        self.assertNotIn("other_alias", text)

    def test_unfiltered_preserves_global_cross_check(self):
        result = report.collect()
        self.assertIsNone(result["section"])
        self.assertEqual(result["population"]["store_records"], 4)
        self.assertEqual(result["cross_check"]["candidates"], {"verbs": 4, "tokens": 5})

    def test_unknown_section_fails_instead_of_reporting_zero(self):
        with self.assertRaisesRegex(ValueError, "unknown section.*list-verb-categories"):
            report.collect("Sampl")
        with contextlib.redirect_stderr(io.StringIO()) as err:
            with self.assertRaises(SystemExit) as raised:
                report.main(["--section", "Sampl"])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("unknown section", err.getvalue())


if __name__ == "__main__":
    unittest.main()
