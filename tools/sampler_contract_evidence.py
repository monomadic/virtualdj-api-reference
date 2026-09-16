"""Read bounded sampler captures without promoting parser acceptance to behavior."""
from __future__ import annotations

from collections import defaultdict
import math

SOURCE = "tests/sampler-contracts-9598.json"
SLOTS = ("1", "2", "3", "5", "9", "12")
GROUP = ("1", "2", "3")


def near(a, b):
    try:
        return math.isfinite(float(a)) and abs(float(a) - float(b)) < .0001
    except (ValueError, TypeError):
        return False


def levels_equal(a, b):
    return set(a) == set(b) == set(SLOTS) and all(near(a[k], b[k]) for k in SLOTS)


def valid_capture(capture):
    """Never join an aborted suite, uncertain mutation, or failed restore."""
    original = capture.get("original_restoration", {})
    if not (capture.get("schema") == 1 and capture.get("completed") is True
            and capture.get("restored") is True and not capture.get("error")
            and str(capture.get("summary", {}).get("build", "")).isdecimal()
            and original.get("bank_matches") is True and original.get("selection_matches") is True
            and original.get("sampler_used") == "0"):
        return False
    if not levels_equal(capture.get("initial_fixture_levels", {}),
                        capture.get("fixture_levels_restored", {})):
        return False
    cases = capture.get("cases", [])
    if not cases or not all(levels_equal(c.get("before", {}), c.get("restored", {}))
                            and set(c.get("after", {})) == set(SLOTS) for c in cases):
        return False
    journal = capture.get("journal", [])
    dispatched = {row.get("script") for row in journal if row.get("phase") == "probe"}
    return (bool(journal) and all(row.get("outcome") == "responded" for row in journal)
            and all(row.get("script") in dispatched for row in cases))


def claims_for(name, capture):
    if name not in {"sampler_volume", "sampler_volume_nogroup", "sampler_group_volume",
                    "sampler_select", "get_sampler_slot", "get_sample_name",
                    "sampler_loaded", "get_sample_info"}:
        return []
    if not valid_capture(capture):
        return []
    claims = []

    def add(dim, form, observation, evidence, channel):
        claims.append({"dimension": dim, "form": form, "status": "settled",
                       "observation": observation, "channel": channel,
                       "source": SOURCE, "build": capture["summary"]["build"],
                       "provenance": capture["summary"], "evidence": evidence})

    cases = defaultdict(dict)
    for row in capture["cases"]:
        if row["run"] in (1, 2):
            cases[row["script"]][row["run"]] = row
    if name in ("sampler_volume", "sampler_volume_nogroup", "sampler_group_volume"):
        # Exact finite predictions; controls and positive anchors must both hold.
        def expected(script, row):
            tail = script[len(name) + 1:]
            target, value = tail.rsplit(" ", 1)
            result = dict(row["before"])
            if target in ("all", "zzqqx", "vfnrbq") or (
                    name == "sampler_group_volume" and target == "current"):
                return result
            selected = "2" if target == "'ContractTone02'" else "1"
            affected = (selected,) if name == "sampler_volume_nogroup" else GROUP
            number = float(value.rstrip("%")) / (100 if value.endswith("%") else 1)
            if value.startswith("+"):
                number += float(row["before"][selected])
            for slot in affected:
                result[slot] = number
            return result

        def proved(script):
            named = "'Alpha'" if name == "sampler_group_volume" else "'ContractTone02'"
            allowed = {f"{name} {tail}" for tail in ("1 0.61", "1 37%", "1 +5%",
                       "current 0.61", "all 0.61", "zzqqx 0.61", "vfnrbq 0.61", named + " 0.61")}
            if script not in allowed:
                return False
            rows = cases.get(script, {})
            return set(rows) == {1, 2} and all(
                levels_equal(row["after"], expected(script, row)) for row in rows.values())

        anchors = [f"{name} {tail}" for tail in ("1 0.61", "zzqqx 0.61", "vfnrbq 0.61")]
        if all(proved(s) for s in anchors):
            for script, runs in sorted(cases.items()):
                if not script.startswith(name + " ") or not proved(script):
                    continue
                if "zzqqx" in script or "vfnrbq" in script:
                    continue
                tail = script[len(name) + 1:]
                affected = [k for k in SLOTS if not near(runs[1]["before"][k], runs[1]["after"][k])]
                obs = (f"HTTP execute {script}: changed slots {', '.join(affected)}"
                       if affected else f"HTTP execute {script}: no slot-level change")
                obs += "; repeated from unequal baselines, two inert nonsense selectors, every case restored"
                add("execute", tail, obs, list(runs.values()), "HTTP execute + separate slot-level queries")
                add("arguments", tail, obs, list(runs.values()), "HTTP execute + separate slot-level queries")

    query_runs = defaultdict(dict)
    for row in capture.get("queries", []):
        query_runs[row["run"]][row["script"]] = row["result"]
    baselines = {row["run"]: row["levels"] for row in capture.get("baselines", [])}
    if not all(run in query_runs and run in baselines for run in (1, 2)):
        return claims
    numeric_scripts = [f"{name} {s}" for s in (1, 2, 5, 9, 4)]
    if name in ("sampler_volume", "sampler_volume_nogroup"):
        if all(near(query_runs[r].get(f"{name} {s}"), baselines[r].get(str(s), 0))
               for r in (1, 2) for s in (1, 2, 5, 9, 4)):
            add("arguments", f"{name} NUM", "Query slot values match independently prepared unequal levels; "
                "empty slot 4 returns 0. Covers these query examples, not controller input.",
                {str(r): {s: query_runs[r][s] for s in numeric_scripts} for r in (1, 2)}, "HTTP query + prepared levels")
    if name in ("get_sample_name", "sampler_loaded", "sampler_volume", "sampler_volume_nogroup"):
        if all(query_runs[r].get(name + " all") == query_runs[r].get(name)
               and name in query_runs[r] and name + " all" in query_runs[r] for r in (1, 2)):
            add("arguments", "all", "Query-only: all matches bare in both fixture baselines. "
                "Parser acceptance does not establish aggregate semantics or any execute form.",
                {str(r): {s: query_runs[r][s] for s in (name, name + " all")} for r in (1, 2)},
                "HTTP query; no execute inference")
    if name in ("get_sample_name", "sampler_loaded"):
        values = {str(r): {s: query_runs[r].get(s) for s in numeric_scripts} for r in (1, 2)}
        wanted = {f"{name} {s}": ("yes" if name == "sampler_loaded" else f"ContractTone{s:02}")
                  for s in (1, 2, 5, 9)}
        wanted[f"{name} 4"] = "no" if name == "sampler_loaded" else "error:1"
        if all(values[str(r)] == wanted for r in (1, 2)):
            add("arguments", f"{name} NUM", "Loaded slots 1, 2, 5, 9 and empty slot 4 match the generated fixture; "
                "no claim about pad-page auto targeting.", values, "HTTP query + generated bank")
    if name == "get_sample_info":
        scripts = [f"get_sample_info {s} '{field}'" for s in (1, 2, 5, 9)
                   for field in ("group", "length", "pos", "zzqqx", "vfnrbq")]
        expected_groups = {1: "Alpha", 2: "Alpha", 5: "Beta", 9: ""}
        good = all(query_runs[r].get(f"get_sample_info {s} '{field}'") == expected
                   for r in (1, 2) for s in (1, 2, 5, 9)
                   for field, expected in (("group", expected_groups[s]), ("length", f"{(s+1)*1000}ms"),
                                           ("pos", "00:00.0"), ("zzqqx", ""), ("vfnrbq", "")))
        if good:
            evidence = {str(r): {s: query_runs[r][s] for s in scripts} for r in (1, 2)}
            add("arguments", "NUM KW position 1 (NUM)", "Distinct known groups and generated WAV durations "
                "discriminate slots 1, 2, 5, 9; nonsense fields are empty. Stopped position remains 00:00.0.",
                evidence, "HTTP query + generated WAV lengths and bank groups")

    selection = capture.get("selection_probe", {})
    if selection.get("before") == selection.get("restored") and selection.get("observations"):
        observations = selection["observations"]
        expected = {str(d): selection["before"].get(f"deck {d} get_sampler_slot") for d in (1, 2)}
        valid = True
        for row in observations:
            expected[row["script"].split()[1]] = row["script"].split()[-1]
            valid &= all(row["readback"].get(f"deck {d} get_sampler_slot") == expected[str(d)]
                         and row["names"].get(str(d)) == f"ContractTone{int(expected[str(d)]):02}"
                         for d in (1, 2))
        if valid and name in ("sampler_select", "get_sampler_slot", "get_sample_name"):
            add("execute" if name == "sampler_select" else "arguments",
                "NUM (deck-scoped selection)" if name == "sampler_select" else "bare (deck-scoped selection)",
                "Absolute selections 2, 5, 9 read back through get_sampler_slot and sample names; "
                "deck defaults differ and restore. sampler_select's own query is normalized, not a slot index.",
                observations, "HTTP execute + get_sampler_slot/get_sample_name readback")
    return claims
