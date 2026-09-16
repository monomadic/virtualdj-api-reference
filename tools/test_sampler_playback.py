"""Adversarial transport-oracle and playback cleanup regressions."""
import copy
import json
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from fixtures import FixtureError
from probe_sampler_playback import PlaybackRunner, load_plan
from sampler_playback_evidence import active, classify_case, claims_for, valid_capture


def state(players, seconds=0, witness=0, clock=0):
    slots = {str(s): {"playing": "yes" if s in players else "no"} for s in (1, 2, 3, 5, 9, 12)}
    for slot, value, duration in (("9", seconds, 10), ("12", witness, 13)):
        slots[slot].update(elapsed=f"00:{value:04.1f}", position=f"{100*value/duration:.2f}%")
    return {"start": clock, "end": clock + .1, "slots": slots, "counts": {"bare": str(len(players))}}


def case(outcome):
    before = state([9, 12], 1.4, 1.4)
    after, later = state([9, 12], 1.8, 1.8, .2), state([9, 12], 2.6, 2.6, 1)
    if outcome == "restart":
        after, later = state([9, 12], .1, 1.8, .2), state([9, 12], .9, 2.6, 1)
    elif outcome == "stop":
        after, later = state([12], 0, 1.8, .2), state([12], 0, 2.6, 1)
    elif outcome == "stop-all":
        after, later = state([], clock=.2), state([], clock=1)
    elif outcome == "start":
        before = state([])
        after, later = state([9], .1, clock=.2), state([9], .9, clock=1)
    elif outcome == "idle":
        before, after, later = state([]), state([], clock=.2), state([], clock=1)
    return {"initial": state([]), "before": before, "after": after, "later": later, "restored": state([])}


class PlaybackTests(unittest.TestCase):
    def test_oracle_distinguishes_transport_behaviors(self):
        for result in ("start", "stop", "stop-all", "restart", "continue", "idle"):
            with self.subTest(result=result):
                self.assertEqual(classify_case(case(result)), result)

    def test_boolean_success_without_position_movement_is_not_start(self):
        row = case("start")
        row["later"] = state([9], .1, clock=1)
        self.assertEqual(classify_case(row), "no-progress")

    def test_stalled_readback_cannot_turn_natural_eof_into_stop(self):
        row = case("stop-all")
        row["before"] = state([9, 12], 9.0, 12.0)
        self.assertEqual(classify_case(row), "end-of-file-ambiguous")
        row = case("stop-all")
        row["later"]["end"] += 10
        self.assertEqual(classify_case(row), "readbacks-disagree")

    def test_percent_time_disagreement_and_wrong_witness_block_proof(self):
        row = case("restart")
        row["after"]["slots"]["9"]["position"] = "90%"
        self.assertEqual(classify_case(row), "readbacks-disagree")
        row = case("stop")
        row["later"] = state([12], 0, 1.8, 1)
        self.assertEqual(classify_case(row), "witness-did-not-continue")

    def test_case_exception_runs_cleanup_without_replaying(self):
        runner = object.__new__(PlaybackRunner)
        runner.data = {"cases": []}
        runner.persist = Mock()
        runner.stopped = Mock(return_value=state([]))
        runner.snapshot = Mock(return_value=state([]))
        runner.execute = Mock(side_effect=TimeoutError("lost response"))
        runner.epoch = 0
        spec = next(c for c in load_plan()["cases"] if c["id"] == "sampler_play-start")
        with self.assertRaises(TimeoutError):
            runner.case(spec, 1)
        runner.execute.assert_called_once_with("sampler_play 9", "playback-probe")
        self.assertEqual(runner.stopped.call_count, 2)
        self.assertEqual(active(runner.data["cases"][0]["restored"]), set())

    def test_cleanup_stops_explicit_slots_not_unproven_all(self):
        runner = object.__new__(PlaybackRunner)
        runner.query = Mock(side_effect=lambda script: "VDJ Contract Fixture" if script == "get_sampler_bank"
                            else "yes" if script in ("sampler_play 9", "sampler_play 12") else "no")
        runner.execute = Mock()
        runner.snapshot = Mock(return_value=state([]))
        runner.stopped()
        self.assertEqual([c.args[0] for c in runner.execute.call_args_list], ["sampler_stop 9", "sampler_stop 12"])

    def test_bank_change_prevents_cleanup_mutation(self):
        runner = object.__new__(PlaybackRunner)
        runner.query = Mock(return_value="different bank")
        runner.execute = Mock()
        with self.assertRaises(FixtureError):
            runner.stopped()
        runner.execute.assert_not_called()


if __name__ == "__main__":
    unittest.main()
