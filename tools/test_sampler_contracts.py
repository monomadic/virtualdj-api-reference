"""Regression checks for bounded sampler proof and restoration failures."""
import copy
import json
import unittest
import warnings
from pathlib import Path
from unittest.mock import Mock, patch

from sampler_contract_evidence import claims_for, valid_capture
from probe_sampler_contracts import Runner, FixtureError
from coverage_report import assess, load_context

ROOT = Path(__file__).resolve().parents[1]


class SamplerTests(unittest.TestCase):
    def setUp(self):
        self.capture = json.loads((ROOT / "tests/sampler-contracts-9598.json").read_text())

    def test_current_capture_and_known_failed_runs(self):
        self.assertTrue(valid_capture(self.capture))
        for suffix in ("initial", "timeout"):
            failed = json.loads((ROOT / f"tests/sampler-contracts-9598-{suffix}.json").read_text())
            self.assertFalse(valid_capture(failed))
            self.assertEqual(claims_for("sampler_volume", failed), [])

    def test_partial_or_uncertain_or_wrong_restore_cannot_close(self):
        for change in (lambda c: c.pop("completed"),
                       lambda c: c.update(restored=False),
                       lambda c: c["journal"][0].update(outcome="uncertain"),
                       lambda c: c["cases"][0]["restored"].update({"2": "0.9"}),
                       lambda c: c["cases"][0].update(script="sampler_volume 12 0.99")):
            c = copy.deepcopy(self.capture)
            change(c)
            self.assertFalse(valid_capture(c))
            self.assertEqual(claims_for("sampler_volume", c), [])

    def test_execute_requires_agreeing_controls_and_positive_change(self):
        for script in ("sampler_volume zzqqx 0.61", "sampler_volume 1 0.61"):
            c = copy.deepcopy(self.capture)
            row = next(r for r in c["cases"] if r["run"] == 2 and r["script"] == script)
            row["after"]["1"] = "0.99"
            self.assertFalse(any(cl["dimension"] == "execute" for cl in claims_for("sampler_volume", c)))

    def test_second_run_is_required_and_stop_gets_no_volume_evidence(self):
        c = copy.deepcopy(self.capture)
        c["cases"] = [r for r in c["cases"] if r["run"] != 2]
        self.assertFalse(any(cl["dimension"] == "execute" for cl in claims_for("sampler_volume", c)))
        self.assertEqual(claims_for("sampler_stop", self.capture), [])

    def test_selection_claim_checks_unaffected_deck(self):
        c = copy.deepcopy(self.capture)
        c["selection_probe"]["observations"][0]["readback"]["deck 2 get_sampler_slot"] = "2"
        self.assertEqual(claims_for("sampler_select", c), [])

    def test_join_is_scoped_and_preserves_remaining_obligations(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            ctx = load_context()
        result = assess("sampler_volume", ctx.store["sampler_volume"], ctx)
        self.assertEqual(result["dimensions"]["execute"], "partial")
        scoped = [c for c in result["claims"] if c.get("source") == "tests/sampler-contracts-9598.json"]
        self.assertTrue(any(c["dimension"] == "execute" and c["form"] == "all 0.61" for c in scoped))
        self.assertTrue(any(c["status"] == "open" and c["form"] == "touchrelative" for c in result["claims"]))
        all_query = next(c for c in scoped if c["form"] == "all")
        self.assertIn("Query-only", all_query["observation"])
        self.assertTrue(all(c["build"] == self.capture["summary"]["build"] for c in scoped))
        self.assertTrue(any(c["dimension"] == "return_type" and c["channel"] == "HTTP sampler fixture"
                            for c in scoped))
        loaded = assess("sampler_loaded", ctx.store["sampler_loaded"], ctx)
        self.assertNotEqual(loaded["dimensions"]["arguments"], "settled")
        self.assertTrue(any(c["status"] == "open" and c["form"] == "NUM auto (pad-page context)"
                            for c in loaded["claims"]))

    def test_selection_restore_uses_slot_not_normalized_query(self):
        runner = object.__new__(Runner)
        before = {"deck 1 get_sampler_slot": "9", "deck 1 sampler_select": "0.8",
                  "deck 2 get_sampler_slot": "5", "deck 2 sampler_select": "0.6"}
        runner.selection = Mock(return_value=before)
        runner.execute = Mock()
        runner.query = Mock(return_value="fixture")
        runner.persist = Mock()
        runner.data = {}
        runner.selection_probe()
        scripts = [call.args[0] for call in runner.execute.call_args_list]
        self.assertEqual(scripts[-2:], ["deck 1 sampler_select 9", "deck 2 sampler_select 5"])

    def test_case_exception_still_restores_and_persists(self):
        runner = object.__new__(Runner)
        runner.silent = Mock()
        runner.levels = Mock(return_value={"1": ".5"})
        runner.execute = Mock(side_effect=TimeoutError("uncertain"))
        runner.restore_levels = Mock(return_value={"1": ".5"})
        runner.persist = Mock()
        runner.data = {"cases": []}
        with self.assertRaises(TimeoutError):
            runner.measure("sampler_volume 1 .4", 1, "test")
        runner.restore_levels.assert_called_once_with({"1": ".5"})
        self.assertEqual(runner.data["cases"][0]["restored"], {"1": ".5"})

    def test_mutation_timeout_is_not_replayed_and_private_bank_is_redacted_before_write(self):
        runner = object.__new__(Runner)
        runner.ch = Mock()
        runner.ch.execute.side_effect = TimeoutError("uncertain")
        runner.data = {"journal": []}
        saved = []
        runner.persist = lambda: saved.append(copy.deepcopy(runner.data))
        with self.assertRaises(TimeoutError):
            runner.execute("sampler_bank 'PrivateBank'", "restore-original-bank")
        runner.ch.execute.assert_called_once_with("sampler_bank 'PrivateBank'")
        self.assertTrue(all("PrivateBank" not in json.dumps(s) for s in saved))
        self.assertEqual(runner.data["journal"][0]["outcome"], "uncertain")

    def test_bank_wait_uses_readback_without_reissuing_action(self):
        runner = object.__new__(Runner)
        runner.query = Mock(side_effect=["old", "old", "fixture"])
        runner.execute = Mock()
        with patch("probe_sampler_contracts.time.sleep"):
            self.assertEqual(runner.wait_bank("fixture"), {"matches": True, "queries": 3})
        runner.execute.assert_not_called()

    def test_external_bank_switch_blocks_level_writes(self):
        runner = object.__new__(Runner)
        runner.query = Mock(return_value="another bank")
        runner.ch = Mock()
        with self.assertRaisesRegex(FixtureError, "fixture bank changed"):
            runner.execute("sampler_volume_nogroup 1 0.5", "restore-level")
        runner.ch.execute.assert_not_called()


if __name__ == "__main__":
    unittest.main()
