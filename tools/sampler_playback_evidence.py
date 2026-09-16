"""Recompute sampler transport findings from timed independent readbacks."""
from __future__ import annotations

import math
import re
from collections import defaultdict

from sampler_contract_evidence import levels_equal

SOURCE = "tests/sampler-playback-9598.json"
SLOTS = {"1", "2", "3", "5", "9", "12"}
VERBS = {"sampler_play", "sampler_stop", "sampler_play_stop", "sampler_play_stutter"}


def elapsed(value):
    match = re.fullmatch(r"(\d+):(\d+(?:\.\d+)?)", str(value))
    return 60 * int(match[1]) + float(match[2]) if match else None


def active(state):
    slots = state.get("slots", {})
    if set(slots) != SLOTS or any(v.get("playing") not in ("yes", "no") for v in slots.values()):
        return None
    result = {int(s) for s, v in slots.items() if v["playing"] == "yes"}
    if state.get("counts", {}).get("bare") != str(len(result)):
        return None
    return result


def positions_agree(state):
    try:
        span = state["end"] - state["start"]
        if not 0 <= span < 1.5:
            return False
        for s, duration in (("9", 10), ("12", 13)):
            row = state["slots"][s]
            value = row["position"]
            if not str(value).endswith("%"):
                return False
            position_seconds = float(value[:-1]) * duration / 100
            seconds = elapsed(row["elapsed"])
            if (seconds is None or not math.isfinite(position_seconds)
                    or abs(seconds - position_seconds) > .25 + span):
                return False
        return True
    except (ValueError, TypeError, KeyError):
        return False


def classify_case(row):
    if any(k not in row for k in ("initial", "before", "after", "later", "restored")):
        return "incomplete"
    if active(row["initial"]) != set() or active(row["restored"]) != set():
        return "restore-failed"
    states = [row[k] for k in ("before", "after", "later")]
    sets = [active(state) for state in states]
    if None in sets or not all(positions_agree(state) for state in states):
        return "readbacks-disagree"
    before, after, later = sets
    if after != later or not (before | after) <= {9, 12}:
        return "unstable-activity"
    if states[1]["start"] < states[0]["end"] or states[2]["start"] <= states[1]["end"]:
        return "invalid-timing"
    pre, post, final = [elapsed(s["slots"]["9"]["elapsed"]) for s in states]
    witness = [elapsed(s["slots"]["12"]["elapsed"]) for s in states]
    # Natural sample endings cannot prove stop or restart. Reject a slow call
    # that could have crossed either known generated file's end.
    window = states[2]["end"] - states[0]["start"]
    if (9 in before and pre + window >= 9.5) or (12 in before and witness[0] + window >= 12.5):
        return "end-of-file-ambiguous"
    if 12 in after and (witness[2] <= witness[1] + .1 or witness[1] < witness[0] - .2):
        return "witness-did-not-continue"
    if before == {9, 12} and after == set():
        return "stop-all" if abs(final - post) < .15 and abs(witness[2] - witness[1]) < .15 else "position-not-stopped"
    if (12 in before) != (12 in after):
        return "wrong-target"
    if 9 not in before and 9 not in after:
        return "idle" if abs(final - post) < .15 else "idle-position-moved"
    if 9 not in before and 9 in after:
        return "start" if final > post + .1 else "no-progress"
    if 9 in before and 9 not in after:
        return "stop" if abs(final - post) < .15 else "position-not-stopped"
    if final <= post + .1:
        return "no-progress"
    if pre >= 1 and post < pre - .6 and post < 1:
        return "restart"
    if post >= pre - .2:
        return "continue"
    return "ambiguous-position"


def valid_capture(capture):
    original = capture.get("original_restoration", {})
    if not (capture.get("kind") == "sampler-playback" and capture.get("completed") is True
            and capture.get("restored") is True and not capture.get("error")
            and str(capture.get("summary", {}).get("build", "")).isdecimal()
            and original.get("bank_matches") is True and original.get("selection_matches") is True
            and original.get("sampler_used") == "0"
            and levels_equal(capture.get("initial_fixture_levels", {}), capture.get("fixture_levels_restored", {}))
            and capture.get("initial_fixture_selection")
            and capture.get("initial_fixture_selection") == capture.get("fixture_selection_restored")
            and capture.get("deck_guard_before") == capture.get("deck_guard_after")
            and capture.get("deck_guard_before")):
        return False
    journal = capture.get("journal", [])
    dispatched = {r.get("script") for r in journal if r.get("phase") == "playback-probe"}
    cases = capture.get("cases", [])
    return (bool(cases) and bool(journal) and all(r.get("outcome") == "responded" for r in journal)
            and active(capture.get("fixture_stopped", {})) == set()
            and all(active(r.get("restored", {})) == set() for r in capture.get("count_probes", []))
            and all(active(r.get("restored", {})) == set() and r.get("script") in dispatched for r in cases))


def claims_for(name, capture, source=SOURCE):
    if name not in VERBS | {"sampler_position", "sampler_used", "get_sample_info"} or not valid_capture(capture):
        return []
    pairs = defaultdict(dict)
    for row in capture["cases"]:
        if row["run"] in (1, 2):
            pairs[row["id"]][row["run"]] = row
    claims = []

    def consistent(id, allowed):
        rows = pairs.get(id, {})
        return set(rows) == {1, 2} and len({classify_case(r) for r in rows.values()}) == 1 and classify_case(rows[1]) in allowed

    def add(dim, form, observation, ids):
        claims.append({"dimension": dim, "form": form, "status": "settled", "observation": observation,
                       "channel": "HTTP execute + timed activity/elapsed/percent/count readbacks",
                       "source": source, "build": capture["summary"]["build"], "provenance": capture["summary"],
                       "evidence": {"case_ids": ids, "runs": [1, 2], "audio_captured": False}})

    if name in VERBS:
        controls = [name + "-" + t for t in ("zzqqx", "vfnrbq")]
        expected_control = "idle" if name == "sampler_play" else "continue"
        if not all(consistent(c, {expected_control}) for c in controls):
            return []
        for id, rows in pairs.items():
            if set(rows) != {1, 2} or rows[1].get("control"):
                continue
            script = rows[1]["script"]
            parts = script.split()
            verb = parts[2] if parts[0] == "deck" else parts[0]
            if verb != name or rows[2]["script"] != script or not consistent(id, {"start", "stop", "stop-all", "restart", "continue", "idle"}):
                continue
            observed = classify_case(rows[1])
            form = "bare (deck 1 default 9)" if parts[0] == "deck" else " ".join(parts[1:]) or "bare"
            obs = f"{script}: {observed}; states {sorted(active(rows[1]['before']))} -> {sorted(active(rows[1]['after']))}. "
            obs += "Repeated with two nonsense selectors; position/count readbacks and cleanup verified. HTTP transport only."
            # Same numeric form can have stopped/running preconditions; keep
            # those as separate claims rather than overwriting one another.
            form += " [playing]" if active(rows[1]["before"]) else " [stopped]"
            for dim in ("execute", "arguments"):
                add(dim, form, obs, [id, *controls])
            if len(parts) > 1 and parts[0] != "deck" and parts[1] == "9" and not any(
                    c["form"] == name + " NUM" for c in claims):
                add("arguments", name + " NUM", "Numeric selector shape measured with absolute slot 9; "
                    "concrete stopped/playing preconditions are listed separately. No whole-range claim.", [id, *controls])
            if name == "sampler_stop" and parts[-1] == "all" and observed == "stop-all":
                add("arguments", "all", "Execute: stopped both independently advancing samples in different groups; "
                    "two nonsense selectors left both progressing. This is aggregate behavior on the tested fixture.", [id, *controls])
    if name in {"sampler_position", "get_sample_info"} and all(
            consistent(id, allowed) for id, allowed in (("sampler_play-start", {"start"}),
                                                      ("sampler_play_stutter-running", {"restart"}),
                                                      ("stop-one", {"stop"}))):
        add("arguments", "NUM (timed transport, slots 9/12)" if name == "sampler_position" else "NUM pos (timed transport)",
            "Slots 9/12: percent positions agree with elapsed strings and known 10s/13s WAV lengths during "
            "start, progress, restart and stop; independent witness continues. No loop/routing/audio claim.",
            ["sampler_play-start", "sampler_play_stutter-running", "stop-one"])
    if name == "sampler_used":
        states = defaultdict(list)
        ids = []
        for id, rows in pairs.items():
            if consistent(id, {"start", "stop", "stop-all", "restart", "continue", "idle"}):
                ids.append(id)
                for run, row in rows.items():
                    states[run].extend(row[k] for k in ("before", "after", "later", "restored"))
        for row in capture.get("count_probes", []):
            if (row.get("run") in (1, 2) and active(row.get("initial", {})) == set()
                    and active(row.get("restored", {})) == set()
                    and all(active(row.get(k, {})) == set(row["playing"])
                            and positions_agree(row[k]) for k in ("after", "later"))):
                states[row["run"]].extend(row[k] for k in ("after", "later"))
        if all({len(active(s)) for s in states[run]} >= set(range(5)) for run in (1, 2)):
            if all(s["counts"].get(str(n)) == ("yes" if len(active(s)) == n else "no")
                   and s["counts"].get(f"predicate_{n}") == ("1" if len(active(s)) == n else "0")
                   for run in (1, 2) for s in states[run] for n in range(5)):
                add("arguments", "sampler_used NUM", "For N=0..4 and independently observed active counts 0..4, "
                    "query returns yes exactly at N and no otherwise; conditional use agrees. Bare returns the count. "
                    "Both runs include separate three/four-player fixtures.", [*ids, "count_probes"])
                add("return_type", "NUM=0..4 (HTTP)", "Argument forms return rendered booleans yes/no; "
                    "the bare form returns the active-sample count. Direct queries and conditional predicates agree.",
                    [*ids, "count_probes"])
    return claims


DEFAULT_SOURCE = "tests/sampler-default-playback-9598.json"

def default_claims_for(name, capture):
    """Close only unwrapped transport under the repeatedly observed context."""
    if name not in VERBS or not valid_capture(capture):
        return []
    expected = {"get_deck": "1", "get_sampler_slot": "9"}
    if any(row.get("default_context_before") != expected or row.get("default_context_after") != expected
           for row in capture["cases"]):
        return []
    claims = [c for c in claims_for(name, capture, DEFAULT_SOURCE) if c["form"].startswith("bare [")]
    forms = {c["form"] for c in claims if c["dimension"] == "execute"}
    if forms != {"bare [stopped]", "bare [playing]"}:
        return []
    observed = " ".join(c["observation"] for c in claims if c["dimension"] == "execute")
    summary = dict(claims[0], dimension="execute", form="bare",
                   observation="Unwrapped HTTP default context get_deck=1, get_sampler_slot=9, checked before/after each case. " + observed,
                   evidence={"case_ids": sorted({id for c in claims for id in c["evidence"]["case_ids"]}),
                             "runs": [1, 2], "audio_captured": False})
    return [*claims, summary]
