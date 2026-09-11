"""Offline regressions for false closure in the shared contract assessment."""
import unittest
import json
import tempfile
import warnings
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from coverage_report import assess, load_context, focused_fx_claims
from fixtures import Channel, FixtureError
import probe_execute_forms as execute


def context():
    ctx = SimpleNamespace(**{key: {} for key in (
        "contracts", "rtypes", "argforms", "execforms", "positions",
        "extra_confirmed", "catalog_actions", "attested", "shapes",
        "placeholders", "refuted", "names_default", "open_tokens", "tried", "bpm_transition")})
    ctx.disputed = set()
    ctx.arg_fixtures = []
    ctx.contracts["example"] = {"queries": True, "executes": True}
    return ctx


class AssessmentTests(unittest.TestCase):
    def test_long_time_capture_closes_hour_with_live_provenance(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            ctx = load_context()
        result = assess("get_time_hour", ctx.store["get_time_hour"], ctx)
        self.assertEqual(result["dimensions"]["arguments"], "settled")
        for claim in result["claims"]:
            if claim["dimension"] in ("arguments", "return_type"):
                self.assertEqual(claim["source"], "tests/long-time-forms.json")
                self.assertEqual(claim["build"], ctx.long_time["summary"]["build"])
        self.assertEqual(ctx.long_time["verbs"]["get_time_sign"]["remain"]["verdict"],
                         "undiscriminated")

    def test_display_mode_restore_does_not_toggle_current_mode(self):
        from probe_long_time import set_mode
        with patch("probe_long_time.mode", return_value="remain"), patch("probe_long_time.wait"):
            ch = unittest.mock.Mock()
            set_mode(ch, "remain")
            ch.execute.assert_not_called()

    def test_fx_join_requires_the_verb_measurement(self):
        for verb, fields in (
                ("get_effect_slider_default", {"sliders": []}),
                ("get_effect_button_name", {"buttons": []}),
                ("get_effect_slider_count", {}),
                ("get_effect_slider_count", {"slider_count": 0}),
                ("get_effect_slider_default", {"sliders": [{"index": 1}]}),
                ("get_effect_slider_default", {"sliders": [{"index": 1, "default": "error:1"}]}),
                ("get_effect_slider_default", {"sliders": [{"index": 1, "default": ""}]}),
                ("get_effect_button_name", {"buttons": [{"index": 1, "full": "error:1"}]})):
            with self.subTest(verb=verb, fields=fields):
                dump = {"effects": [{"effect": "Empty", "introspected_via": "title", **fields}]}
                self.assertEqual(focused_fx_claims(verb, dump), [])

    def test_fx_join_selects_valid_measurements_and_preserves_legitimate_blank(self):
        dump = {"effects": [
            {"effect": "Empty", "introspected_via": "title", "sliders": []},
            {"effect": "Measured", "introspected_via": "title", "sliders": [
                {"index": 1, "default": "error:1"},
                {"index": 2, "default": "0", "skip_length_label": ""}]}]}
        claim, = focused_fx_claims("get_effect_slider_default", dump)
        self.assertEqual(claim["example"], {"effect": "Measured", "index": 2, "value": "0"})
        self.assertEqual(claim["excluded_results"]["error"], 1)
        self.assertIn("across 1 effects", claim["observation"])
        blank, = focused_fx_claims("get_effect_slider_label_skip_length", dump)
        self.assertEqual(blank["example"]["value"], "")

    def test_prose_filter_miss_does_not_claim_no_prior_test(self):
        rec = {"confidence": "local_test", "evidence": [
            "HTTP: example opposite answered yes; nonsense answered no."]}
        result = assess("example", rec, context())
        claim = next(c for c in result["claims"] if c["dimension"] == "arguments")
        self.assertIn("prose filter found no explicit", claim["observation"])
        self.assertNotIn("never probed", claim["observation"])

    def test_live_build_provenance_does_not_accept_error_or_empty(self):
        for value in ("", "error:1", "not-a-build"):
            with patch.object(Channel, "query", return_value=value):
                with self.assertRaises(FixtureError):
                    Channel().provenance()
        with patch.object(Channel, "query", return_value="1234") as query:
            stamp = Channel().provenance()
            self.assertEqual(stamp["build"], "1234")
            query.assert_called_once_with("get_build")

    def test_real_focused_execute_and_catalog_value_obligations(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            ctx = load_context()
        bpm = assess("auto_bpm_transition", ctx.store["auto_bpm_transition"], ctx)
        self.assertEqual(bpm["dimensions"]["execute"], "settled")
        for form in ("source_original", "target_current"):
            claims = [c for c in bpm["claims"] if c["dimension"] == "execute" and c["form"] == form]
            self.assertEqual(len(claims), 1)
            self.assertEqual(claims[0]["status"], "settled")
            self.assertEqual(claims[0]["source"], "tests/bpm-transition-forms.json")
        curve = assess("crossfader_curve", ctx.store["crossfader_curve"], ctx)
        self.assertEqual(curve["dimensions"]["arguments"], "open")
        obligations = {c["form"] for c in curve["claims"] if c["status"] == "open"}
        self.assertTrue({"catalog: numeric value", "catalog: drawn curve"} <= obligations)

    def test_fx_dump_join_closes_name_form_verbs_with_unstamped_provenance(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            ctx = load_context()
        r = assess("get_effect_slider_count", ctx.store["get_effect_slider_count"], ctx)
        self.assertEqual(r["dimensions"]["arguments"], "settled")
        fx = [c for c in r["claims"] if c.get("source") == "tests/fx-introspection-dump.json"]
        self.assertEqual(len(fx), 1)
        self.assertEqual(fx[0]["form"], "get_effect_slider_count 'NAME'")
        self.assertIsNone(fx[0]["build"])
        # A verb the sweep never called by name gains nothing from the join.
        r2 = assess("get_effect_slider_name", ctx.store["get_effect_slider_name"], ctx)
        self.assertFalse(any(c.get("source") == "tests/fx-introspection-dump.json"
                             for c in r2["claims"]))

    def test_behaviour_only_prose_is_not_argument_evidence(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            ctx = load_context()
        for verb in ("deck_has_error", "video_fx_clear"):  # "verb returned true" is not a form
            behaviour = assess(verb, ctx.store[verb], ctx)
            self.assertEqual(behaviour["dimensions"]["arguments"], "unprobed", verb)
        wrapper = assess("all_decks", ctx.store["all_decks"], ctx)  # "all_decks get_version" is
        self.assertEqual(wrapper["dimensions"]["arguments"], "evidence_in_prose")
        about_args = assess("get_date", ctx.store["get_date"], ctx)
        self.assertEqual(about_args["dimensions"]["arguments"], "evidence_in_prose")

    def test_binary_demand_without_known_form_stays_open(self):
        ctx = context()
        ctx.contracts["example"]["arg_demand_slots"] = [3]
        result = assess("example", {}, ctx)
        self.assertEqual(result["dimensions"]["arguments"], "open")
        self.assertTrue(any(c["form"] == "binary argument-demand slots" for c in result["claims"]))

    def test_measured_shape_can_discharge_named_obligation(self):
        ctx = context()
        ctx.shapes["example"] = {"NUM NUM": {}}
        ctx.positions["example"] = {"shape": "NUM NUM", "stable": True,
            "positions": [{"index": i, "class": "NUM", "verdict": "reads",
                           "baseline": "1", "variant": "2"} for i in (1, 2)]}
        self.assertEqual(assess("example", {}, ctx)["dimensions"]["arguments"], "settled")

    def test_catalog_value_obligation_can_be_discharged(self):
        ctx = context()
        ctx.catalog_actions["example"] = {"text": "Enter a value to adjust the slope."}
        self.assertEqual(assess("example", {}, ctx)["dimensions"]["arguments"], "open")
        ctx.argforms["example"] = {"recognized_tokens": [["25%"]], "forms": []}
        self.assertEqual(assess("example", {}, ctx)["dimensions"]["arguments"], "settled")

    def test_known_keyword_contract_can_close(self):
        ctx = context()
        ctx.extra_confirmed["example"] = ["named"]
        result = assess("example", {}, ctx)
        self.assertEqual(result["dimensions"]["arguments"], "settled")
        self.assertFalse(result["complete"])

    def test_failed_or_unstable_position_never_closes(self):
        for stable, verdict, reason in ((False, "reads", "conflicting"),
                                        (True, "no-answer", "unavailable"),
                                        (True, "rejects-nonsense-only", "undiscriminated")):
            with self.subTest(stable=stable, verdict=verdict):
                ctx = context()
                ctx.positions["example"] = {"shape": "NUM NUM", "stable": stable,
                    "positions": [{"index": 1, "class": "NUM", "verdict": verdict,
                                   "baseline": "1", "variant": "2"}]}
                claims = assess("example", {}, ctx)["claims"]
                claim = next(c for c in claims if "position 1" in c["form"])
                self.assertEqual((claim["status"], claim["reason"]), ("open", reason))

    def test_keyword_does_not_close_value_shape(self):
        ctx = context()
        ctx.extra_confirmed["example"] = ["named"]
        ctx.shapes["example"] = {"NUM KW": {}}
        result = assess("example", {}, ctx)
        self.assertEqual(result["dimensions"]["arguments"], "open")
        self.assertTrue(any(c["form"] == "example NUM KW" and c["status"] == "open"
                            for c in result["claims"]))

    def test_query_confirmation_does_not_close_execute(self):
        ctx = context()
        ctx.extra_confirmed["example"] = ["query_only"]
        ctx.contracts["example"]["keyword_candidates"] = ["query_only", "on"]
        ctx.execforms["example"] = {"verdict": "has-execute-tokens",
                                    "recognized": [{"tokens": ["on"]}], "signatures": {}}
        result = assess("example", {}, ctx)
        self.assertEqual(result["dimensions"]["execute"], "partial")
        self.assertTrue(any(c["dimension"] == "execute" and c["form"] == "query_only"
                            and c.get("reason") == "not_measured" for c in result["claims"]))

    def test_missing_capability_has_open_reasons(self):
        ctx = context()
        ctx.contracts = {}
        result = assess("example", {}, ctx)
        for dimension, state in result["dimensions"].items():
            self.assertNotEqual(state, "n/a")
            self.assertTrue(any(c["dimension"] == dimension and c.get("reason")
                                for c in result["claims"]))

    def test_aborted_execute_preserves_previous_capture(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "capture.json"
            target.write_text('{"previous": true}\n')
            plan = {"example": {"family": "toggle", "candidates": []}}
            with patch("sys.argv", ["probe", "--out", str(target), "--quiet"]), \
                 patch.object(execute, "targets", return_value=plan), \
                 patch.object(execute, "Channel") as channel, \
                 patch.object(execute, "probe", side_effect=execute.FixtureError("restore failed")):
                channel.return_value.reachable.return_value = True
                channel.return_value.provenance.return_value = {"build": "1234", "channel": "HTTP"}
                self.assertEqual(execute.main(), 1)
            self.assertEqual(json.loads(target.read_text()), {"previous": True})
            failed = json.loads(target.with_name("capture.aborted.json").read_text())
            self.assertIn("restore failed", failed["summary"]["aborted"])


if __name__ == "__main__":
    unittest.main()
