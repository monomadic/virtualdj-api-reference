#!/usr/bin/env python3
"""Build a bounded H4 runtime-parser frontier report.

This consumes the structural manifest emitted by extract_runtime_parser.py and
optionally resolves target addresses with nm from the same binary.  It reports
call sites and review queues only: classifications are triage labels, never
claims about parser behavior or exhaustive call-graph coverage.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

import bisect
import sys

sys.path.insert(0, str(Path(__file__).parent))
import extract_runtime_parser as runtime_parser


ARGUMENT_CALLERS = (
    "IAction::create",
    "IAction::stringGetParam",
    "IAction::getParamEval",
    "IAction::getFloatParamEval",
    "IAction::getBoolParam",
    "IAction::getListParam",
    "IAction::query",
    "IAction::queryText",
    "IAction::execute",
    "IParamValuesAction::getValues",
    "ACTION_param_add::onQuery",
)


def nm_symbols(binary: Path) -> dict[int, list[str]]:
    raw = subprocess.check_output(["nm", "-arch", "x86_64", str(binary)], text=True)
    rows = []
    for line in raw.splitlines():
        m = re.match(r"^([0-9a-fA-F]+)\s+([tTuUwW])\s+(\S+)$", line)
        if m and m.group(2).lower() == "t":
            rows.append((int(m.group(1), 16), m.group(3)))
    if not rows:
        return {}
    demangled = subprocess.check_output(
        ["c++filt"], input="\n".join(name for _, name in rows), text=True
    ).splitlines()
    out: dict[int, list[str]] = defaultdict(list)
    for (address, _), pretty in zip(rows, demangled):
        out[address].append(pretty)
    return {address: sorted(set(names)) for address, names in out.items()}


def caller_matches(caller: str, prefixes: tuple[str, ...] = ARGUMENT_CALLERS) -> bool:
    return any(caller.startswith(prefix) for prefix in prefixes)


def classify(names: list[str]) -> tuple[str, str]:
    """Return a triage class and why it was assigned (not a proof)."""
    joined = " ".join(names)
    if not names:
        return "unresolved_target", "no nm symbol at target address"
    if ("std::__1::" in joined or "fmt::" in joined or "___clang_" in joined
            or joined.startswith("_") or "operator new" in joined
            or "operator delete" in joined):
        return "known_library", "stdlib/runtime-looking symbol; review label only"
    if any(token in joined for token in ("destroy", "destruct", "allocator", "CAutoThreadSync")):
        return "known_allocation_or_cleanup", "allocation/cleanup-looking symbol; review label only"
    if any(token in joined for token in (
        "createAction_combine_query", "queryValue", "getDeckSafe", "numberMatch",
        "matchStringWithFlag", "isLeft", "isRight", "strIsEqual", "canComplete",
        "getParam", "stringGetParam", "paramToString",
    )):
        return "potential_argument_consuming_helper", "parser-adjacent name; review queue, not behavior"
    return "other_direct_target", "unexpanded direct target; inspect bounded body before claims"


def named_target(binary: Path, starts: list[int], wanted: str, pretty_to_mangled: dict[str, tuple[str, int]]):
    matches = [(name, pair[0]) for name, pair in pretty_to_mangled.items()
               if name == wanted or name.startswith(wanted + "(")]
    if not matches:
        return {"requested": wanted, "status": "unresolved_named_symbol",
                "note": "fresh nm did not expose this exact method; no behavior inferred"}
    actual, mangled = matches[0]
    start = pretty_to_mangled[actual][1]
    index = bisect.bisect_left(starts, start)
    if index >= len(starts) or starts[index] != start or index + 1 >= len(starts):
        return {"requested": wanted, "status": "unbounded", "symbol": actual,
                "mangled": mangled, "start": hex(start)}
    end = starts[index + 1]
    body = runtime_parser.bounded_disassembly(binary, mangled, start, end)
    _, address_names = runtime_parser.symbols(binary)
    pretty_map = pretty_mangled(binary)
    demangled_by_address = defaultdict(list)
    for pretty, (_, address) in pretty_map.items():
        demangled_by_address[address].append(pretty)
    mangled_addresses = {symbol: address for address, names in address_names.items() for symbol in names}
    direct, indirect, _ = runtime_parser.sites(body, demangled_by_address, mangled_addresses)
    return {"requested": wanted, "status": "bounded", "symbol": actual,
            "mangled": mangled, "start": hex(start), "end_exclusive": hex(end),
            "direct_calls": direct, "indirect_calls": indirect,
            "evidence": "fresh bounded disassembly; structural target inventory only"}


def pretty_mangled(binary: Path) -> dict[str, tuple[str, int]]:
    raw = subprocess.check_output(["nm", "-arch", "x86_64", str(binary)], text=True)
    rows = []
    for line in raw.splitlines():
        m = re.match(r"^([0-9a-fA-F]+)\s+([tTuUwW])\s+(\S+)$", line)
        if m and m.group(2).lower() == "t":
            rows.append((int(m.group(1), 16), m.group(3)))
    names = subprocess.check_output(["c++filt"], input="\n".join(n for _, n in rows), text=True).splitlines()
    return {pretty: (mangled, address) for (address, mangled), pretty in zip(rows, names)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", action="store_true", help="read the stored frontier summary")
    parser.add_argument("--manifest", type=Path, default=Path("tests/runtime-parser-9246/manifest.json"))
    parser.add_argument("--binary", type=Path)
    parser.add_argument("--output", type=Path, default=Path("tests/runtime-parser-frontier.json"))
    args = parser.parse_args()
    if args.report:
        stored = json.loads(args.output.read_text())
        print(json.dumps({"source": stored["source"], "counts": stored["counts"],
            "review_queues": stored["review_queues"]}, indent=2))
        return 0
    manifest = json.loads(args.manifest.read_text())
    address_names = nm_symbols(args.binary) if args.binary else {}
    fresh_targets = []
    if args.binary:
        starts = runtime_parser.function_starts(args.binary)
        pretty_to_mangled = pretty_mangled(args.binary)
        for wanted in ("ACTION_zoom::onExecute", "ACTION_beatlock::onExecute",
                       "getDeckSafe", "getDeck"):
            fresh_targets.append(named_target(args.binary, starts, wanted, pretty_to_mangled))
        # The beatlock constructor is a useful bounded entry when its onExecute
        # override is absent from nm; this is an inventory fallback only.
        if fresh_targets[1]["status"] == "unresolved_named_symbol":
            fresh_targets.append(named_target(args.binary, starts, "createAction_beatlock", pretty_to_mangled))

    direct_by_target: dict[str, dict] = {}
    for entry in manifest.get("coverage", {}).get("direct_unexpanded_targets", []):
        target = entry["target"]
        address = int(target, 16)
        # Prefer fresh demangled names; the older manifest stores mangled names.
        names = sorted(set(address_names.get(address, []) or entry.get("symbols", [])))
        sites = []
        # Re-read selected bodies so the report retains exact call instruction sites.
        for label, selected in manifest.get("symbols", {}).items():
            for call in selected.get("direct_calls", []):
                if int(call["target"], 16) == address:
                    sites.append({
                        "site": call["site"],
                        "caller_label": label,
                        "caller_symbol": selected.get("demangled", label),
                        "target": target,
                    })
        triage, basis = classify(names)
        direct_by_target[target] = {
            "target": target,
            "symbols": names,
            "classification": triage,
            "classification_basis": basis,
            "call_sites": sorted(sites, key=lambda x: (x["caller_symbol"], x["site"])),
        }

    indirect = []
    for item in manifest.get("unresolved", {}).get("indirect_call_sites", []):
        caller = item["function"]
        priority = "strong" if caller_matches(caller) else "context"
        indirect.append({**item, "review_priority": priority,
                         "classification": "indirect_call_site",
                         "classification_basis": "target depends on runtime object/vtable/register state"})
    indirect.sort(key=lambda x: (x["review_priority"] != "strong", x["function"], x["site"]))

    potential = [entry for entry in direct_by_target.values()
                 if entry["classification"] == "potential_argument_consuming_helper"]
    potential.sort(key=lambda x: (not any(caller_matches(s["caller_symbol"]) for s in x["call_sites"]),
                                  x["target"]))
    report = {
        "source": {
            "manifest": str(args.manifest),
            "binary": str(args.binary) if args.binary else None,
            "evidence_tier": "Tier-2 bounded binary structure; no behavioral claim",
        },
        "scope": manifest.get("scope"),
        "call_graph_boundary": manifest.get("call_graph_boundary"),
        "direct_unexpanded_targets": sorted(direct_by_target.values(), key=lambda x: int(x["target"], 16)),
        "indirect_sites": indirect,
        "fresh_named_targets": fresh_targets,
        "review_queues": {
            "potential_argument_consumers": potential,
            "strongest_omitted_targets": [
                {"target": e["target"], "symbols": e["symbols"],
                 "call_sites": e["call_sites"]}
                for e in potential[:12]
            ],
            "indirect_argument_path_sites": [e for e in indirect if e["review_priority"] == "strong"],
        },
        "counts": {
            "direct_targets": len(direct_by_target),
            "indirect_sites": len(indirect),
            "potential_argument_consumers": len(potential),
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
