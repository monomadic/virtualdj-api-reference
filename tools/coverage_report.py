#!/usr/bin/env python3
"""Contract coverage across every verb, computed from the artifacts at read time.

    just coverage
    just coverage --format=json
    just coverage --settled          # the verbs with nothing left open
    just coverage --frontier         # what each dimension is blocked on, by name

`verb-stats` counts the store's own `test_status` field, which answers one
question: has behaviour been confirmed live. That is a quarter of a verb's
calling contract. Task 10 wants four things per verb — what it returns in query
position, what arguments it accepts, what it does in execute position, and
whether any of that has been observed rather than inferred — and each lives in a
different artifact with a different denominator. This joins them.

Three rules the numbers here obey:

- **Denominators are per dimension.** A verb that cannot be queried has no
  return type to establish, so it is `n/a` there, not `open`. Reporting 578
  typed verbs against all 979 canonical names would understate the return-type
  sweep by counting execute-only verbs as gaps.
- **Nothing is read from a stored summary.** Every figure is recounted from the
  artifact's own records, because a stored summary goes stale the moment a probe
  appends to the data without regenerating the header — `verb-arg-forms.json`
  currently ships one that does. Where a summary disagrees with its own records,
  this says so instead of trusting either.
- **"Settled" is a claim about evidence, not about effort.** A probed verb where
  nothing separated from the nonsense controls is `open`, not settled: it means
  the state did not discriminate, which is not the same as the verb having no
  arguments. See docs/Evidence Standards.md.

Read-only. Touches no live instance and writes nothing.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verbdb import audit_pool, contract_names, load_store  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "tests"

DIMENSIONS = ("return_type", "arguments", "execute", "behaviour")

# States that close a dimension. `argument_less` is a real answer, not a gap: a
# verb probed against nonsense controls with no candidate token in the binary,
# the catalog or a shipped script takes no arguments on the evidence available.
# It is reported apart from `settled` because it rests on absence.
CLOSED = {"settled", "argument_less"}

# The execute channel writes to a live instance, so it is deliberately the
# slowest to fill and would otherwise mark every verb incomplete. The read-side
# contract — what it returns, what it accepts, whether behaviour was observed —
# is reported separately for that reason, and is the figure worth quoting.
READ_SIDE = ("return_type", "arguments", "behaviour")


def artifact(name: str, key: str | None = None):
    """A missing artifact is a smaller report, never a crash — several are
    regenerated from a live app or an app bundle that may not be present."""
    path = T / name
    if not path.exists():
        return {} if key else None
    try:
        data = json.load(open(path))
    except json.JSONDecodeError:
        return {} if key else None
    return data.get(key, {}) if key else data


def build_stamp() -> str:
    """The verb table's own stamp, copied rather than recalled — the phrase is
    evidence about one build and must not drift (see CLAUDE.md)."""
    table = artifact("verb-table.json")
    if not table:
        return "build unknown — tests/verb-table.json not extracted"
    s = table["summary"]
    return (f"{s['records']} records / {s['distinct_ids']} distinct verbs on build "
            f"{s['build']} ({s['arch']}, extracted {s['extracted']})")


def cross_check() -> tuple[dict, dict, str]:
    """Documented-vs-probed-vs-attested buckets, plus the confirmations that
    reached a verb through some channel other than the argument prober.

    Preferred live from the app bundle, because the tool carries the
    LOCAL_CONFIRMED / LOCAL_PLACEHOLDERS tables in its own source and those
    change with every probe session — the committed artifact lags them. Falls
    back to the artifact with the source named, so a stale number is never
    presented as a fresh one.
    """
    extra: dict[str, set[str]] = {}
    try:
        from extract_action_catalog import DEFAULT_APP, LANGUAGE, catalog
        from extract_action_catalog import cross_check as live_cross_check
        from extract_action_catalog import extra_confirmations
        extra = extra_confirmations()
        entries = catalog(DEFAULT_APP, LANGUAGE)
        checked = live_cross_check(entries)
        if checked:
            return checked, extra, "live from the app bundle"
    except (ImportError, OSError, KeyError):
        pass
    art = artifact("action-catalog.json")
    if art and art.get("cross_check"):
        return (art["cross_check"], extra,
                "tests/action-catalog.json (app bundle unavailable — may lag)")
    return {}, extra, "unavailable"


def collect() -> dict:
    store = load_store()
    canon = {n: r for n, r in store.items() if r.get("tier") != "alias"}

    contracts = artifact("action-contracts.json", "verbs")
    rtypes = artifact("verb-return-types.json", "verbs")
    argforms = artifact("verb-arg-forms.json", "verbs")
    execforms = artifact("verb-execute-forms.json", "verbs")
    positions = artifact("verb-arg-positions.json", "verbs")
    tails_art = artifact("attested-tails.json") or {}
    attested = tails_art.get("tails", {})
    shapes = tails_art.get("shapes", {})
    catalog_actions = artifact("action-catalog.json", "actions")
    checked, extra_confirmed, cc_source = cross_check()

    open_tokens = checked.get("documented_but_not_probe_confirmed", {})
    placeholders = checked.get("documented_example_placeholders", {})
    refuted = checked.get("documented_but_locally_refuted", {})

    verbs: dict[str, dict] = {}
    for name, rec in canon.items():
        c = contracts.get(name, {})
        queries, executes = bool(c.get("queries")), bool(c.get("executes"))
        rt = rtypes.get(name, {})
        observed = rt.get("observed_type")
        # Tails are settled by whichever channel could see them. The argument
        # prober is the general one, but several verbs were closed elsewhere —
        # the effect-introspection sweep, the known-position probe, the
        # purpose-built BPM-transition prober, execute-with-readback — and those
        # land in the catalog tool's LOCAL_CONFIRMED table. Reading only
        # verb-arg-forms.json would report those verbs as unprobed.
        af = argforms.get(name)
        recognized = {t[0] for t in (af or {}).get("recognized_tokens", []) if len(t) == 1}
        recognized |= set(extra_confirmed.get(name, ()))
        recognized = sorted(recognized)
        probed = (af is not None or name in positions or name in execforms
                  or name in extra_confirmed)

        # Every source that has ever named a candidate token for this verb,
        # minus the ones already disposed of. A verb with no candidate anywhere
        # and a probe behind it is argument-less on the evidence; a verb with
        # candidates left over is an open question however much has been probed.
        candidates = set(c.get("keyword_candidates") or [])
        candidates |= set(catalog_actions.get(name, {}).get("documented_parameters", []))
        candidates |= set(attested.get(name, {}))
        candidates -= {name}
        candidates -= set(placeholders.get(name, []))
        candidates -= set(refuted.get(name, []))
        unresolved = sorted((candidates - set(recognized)) | set(open_tokens.get(name, [])))

        dims = {}
        # 1. Return type — applies only where the verb answers a query at all.
        #    `untyped` and `unswept` are different failures: the first was asked
        #    and answered empty in all three contexts and needs a richer state,
        #    the second was never in the sweep's population.
        if not queries:
            dims["return_type"] = "n/a"
        elif observed and observed != "untyped":
            dims["return_type"] = "settled"
        elif name in rtypes:
            dims["return_type"] = "untyped"
        else:
            dims["return_type"] = "unswept"
        # 2. Arguments — applies to every verb; the question is what it accepts.
        #    A keyword prober can only settle a verb whose arguments ARE
        #    keywords. `get_effect_slider_count 'Echo'` takes a value, so no
        #    token sweep will ever separate it from nonsense; the only record of
        #    its shape is what Atomix wrote in a shipped script. That is Tier 2,
        #    so it gets its own state rather than being counted closed — but
        #    calling it `unprobed` would say the opposite of the truth.
        if unresolved:
            dims["arguments"] = "open"
        elif recognized:
            dims["arguments"] = "settled"
        elif probed and not candidates and not shapes.get(name):
            dims["arguments"] = "argument_less"
        elif shapes.get(name):
            dims["arguments"] = "shape_attested"
        elif not probed and rec.get("confidence") == "local_test" and rec.get("evidence"):
            # A live test settled something about this verb and the conclusion
            # went into the store's evidence prose without ever reaching an
            # argument artifact. `get_effect_slider_count` is the type case: its
            # name-instead-of-slot form was verified across 119 effects over
            # HTTP, and no structured row records it. Not closed — the prose may
            # be about behaviour rather than arguments — but reporting it as
            # `unprobed` would lose real work.
            dims["arguments"] = "evidence_in_prose"
        elif not probed:
            dims["arguments"] = "unprobed"
        else:
            dims["arguments"] = "open"
        # 3. Execute position — applies only where the verb executes. Writing to
        #    a live instance is the expensive channel, so this is the thin one.
        if not executes:
            dims["execute"] = "n/a"
        elif name in execforms:
            dims["execute"] = "settled"
        else:
            dims["execute"] = "open"
        # 4. Behaviour — the store's own claim, and the only one that needs
        #    evidence attached to count (`just check` enforces the pairing).
        status = rec.get("test_status", "Untested")
        if status == "Pass" and rec.get("evidence"):
            dims["behaviour"] = "settled"
        elif rec.get("blocked"):
            dims["behaviour"] = "blocked"
        else:
            dims["behaviour"] = "open"

        applicable = [d for d in DIMENSIONS if dims[d] != "n/a"]
        settled = [d for d in applicable if dims[d] in CLOSED]
        read_applicable = [d for d in READ_SIDE if dims[d] != "n/a"]
        read_settled = [d for d in read_applicable if dims[d] in CLOSED]
        verbs[name] = {
            "queries": queries, "executes": executes,
            "observed_type": observed, "test_status": status,
            "recognized_tails": recognized, "unresolved_tails": unresolved,
            "positions_probed": name in positions,
            "attested_shapes": sorted(shapes.get(name, {})),
            "dimensions": dims,
            "applicable": len(applicable), "settled": len(settled),
            "complete": len(settled) == len(applicable) and len(applicable) > 0,
            "read_side_complete": (len(read_settled) == len(read_applicable)
                                   and len(read_applicable) > 0),
        }

    return {
        "stamp": build_stamp(),
        "read_on": date.today().isoformat(),
        "cross_check_source": cc_source,
        "cross_check": {k: {"verbs": len(v), "tokens": sum(len(t) for t in v.values())}
                        for k, v in checked.items()},
        "population": population(canon, store, verbs),
        "dimensions": {d: tally(verbs, d) for d in DIMENSIONS},
        "ladder": ladder(verbs),
        "staleness": staleness(argforms, execforms, rtypes),
        "frontier": frontier(canon, verbs, store),
        "verbs": verbs,
    }


def population(canon: dict, store: dict, verbs: dict) -> dict:
    return {
        "store_records": len(store),
        "canonical": len(canon),
        "aliases": len(store) - len(canon),
        "query_capable": sum(1 for v in verbs.values() if v["queries"]),
        "execute_capable": sum(1 for v in verbs.values() if v["executes"]),
        "both": sum(1 for v in verbs.values() if v["queries"] and v["executes"]),
        "no_contract_row": sum(1 for v in verbs.values()
                               if not v["queries"] and not v["executes"]),
    }


def tally(verbs: dict, dim: str) -> dict:
    out: dict[str, int] = {}
    for v in verbs.values():
        out[v["dimensions"][dim]] = out.get(v["dimensions"][dim], 0) + 1
    applicable = sum(n for k, n in out.items() if k != "n/a")
    closed = sum(n for k, n in out.items() if k in CLOSED)
    out["_applicable"] = applicable
    out["_closed"] = closed
    out["_closed_pct"] = round(100 * closed / applicable, 1) if applicable else 0.0
    return out


def ladder(verbs: dict) -> dict:
    """Verbs by how much of their own contract is closed. Sorted by the fraction
    itself, so a 2/2 verb ranks above a 2/4 one rather than tying with it."""
    rungs: dict[str, int] = {}
    for v in verbs.values():
        rungs[f"{v['settled']}/{v['applicable']}"] = rungs.get(f"{v['settled']}/{v['applicable']}", 0) + 1

    def rank(key: str) -> tuple:
        got, tot = (int(x) for x in key.split("/"))
        return (-(got / tot if tot else 0), -got, -tot)

    return dict(sorted(rungs.items(), key=lambda kv: rank(kv[0])))


def staleness(argforms: dict, execforms: dict, rtypes: dict) -> list[str]:
    """A stored summary that no longer matches its own records. Worth printing:
    it is how a regenerated artifact silently keeps quoting the old figure."""
    notes = []
    for fname, records in (("verb-arg-forms.json", argforms),
                           ("verb-execute-forms.json", execforms),
                           ("verb-return-types.json", rtypes)):
        data = artifact(fname)
        if not data or not records:
            continue
        claimed = data.get("summary", {}).get("verbs")
        if isinstance(claimed, int) and claimed != len(records):
            notes.append(f"{fname}: summary says {claimed} verbs, the records hold "
                         f"{len(records)} — the header predates the last append")
    return notes


def frontier(canon: dict, verbs: dict, store: dict) -> dict:
    """What each dimension is actually blocked on, as names rather than a count."""
    known = contract_names()
    return {
        "return_type_untyped": sorted(n for n, v in verbs.items()
                                      if v["dimensions"]["return_type"] == "untyped"),
        "return_type_unswept": sorted(n for n, v in verbs.items()
                                      if v["dimensions"]["return_type"] == "unswept"),
        "arguments_open": sorted(n for n, v in verbs.items()
                                 if v["dimensions"]["arguments"] == "open"),
        "arguments_unprobed_with_candidates": sorted(
            n for n, v in verbs.items()
            if v["dimensions"]["arguments"] == "unprobed" and v["unresolved_tails"]),
        "execute_open": sorted(n for n, v in verbs.items()
                               if v["dimensions"]["execute"] == "open"),
        "no_tier1_row_at_all": sorted(n for n, r in canon.items()
                                      if n not in known and not r.get("blocked")),
        "audit_pool": sorted(r["name"] for r in audit_pool(store)),
        "blocked": sorted(n for n, r in canon.items() if r.get("blocked")),
    }


LABELS = {
    "return_type": ("Return type in query position", "sweep_return_types.py, live over HTTP"),
    "arguments":   ("Accepted argument tails",        "probe_arg_forms.py vs nonsense controls"),
    "execute":     ("Execute-position behaviour",     "probe_execute_forms.py, writes to a live app"),
    "behaviour":   ("Behaviour confirmed live",       "the store's test_status, evidence required"),
}
ORDER = ("settled", "argument_less", "shape_attested", "evidence_in_prose", "open",
         "untyped", "unswept", "unprobed", "blocked", "n/a")
GLOSS = {
    "argument_less": "takes none (probed, no candidate in any source)",
    "shape_attested": "takes values, not keywords — shape from a shipped script (Tier 2)",
    "evidence_in_prose": "live-tested, but the conclusion is only in store prose",
    "untyped": "swept, empty in every context",
    "unswept": "never in the sweep population",
    "unprobed": "never probed",
}


def bar(pct: float, width: int = 28) -> str:
    filled = round(pct / 100 * width)
    return "█" * filled + "·" * (width - filled)


def render(d: dict, show: str | None) -> str:
    L = ["VDJScript contract coverage", "=" * 27,
         d["stamp"], f"read {d['read_on']} from the artifacts; nothing here is stored", ""]

    p = d["population"]
    L.append(f"Population: {p['canonical']} canonical verbs ({p['aliases']} aliases folded away) — "
             f"{p['query_capable']} answer queries, {p['execute_capable']} execute, "
             f"{p['both']} do both")
    if p["no_contract_row"]:
        L.append(f"            {p['no_contract_row']} carry no capability row from the binary")
    L.append("")

    L.append("PER DIMENSION   (denominator is the verbs the dimension applies to)")
    for dim in DIMENSIONS:
        t = d["dimensions"][dim]
        title, how = LABELS[dim]
        L.append("")
        L.append(f"  {title}")
        L.append(f"    {bar(t['_closed_pct'])}  {t['_closed']}/{t['_applicable']}"
                 f"  ({t['_closed_pct']}%)")
        for k in ORDER:
            if k not in t or k in ("settled", "n/a"):
                continue
            gloss = f"   — {GLOSS[k]}" if k in GLOSS else ""
            L.append(f"      {t[k]:>4} {k}{gloss}")
        L.append(f"    via {how}")
    L.append("")

    L.append(f"CROSS-CHECK     documented vs probed vs written by Atomix — {d['cross_check_source']}")
    for k, v in d["cross_check"].items():
        L.append(f"  {k:<36} {v['tokens']:>4} tokens across {v['verbs']:>3} verbs")
    L.append("")

    L.append("COMPLETENESS LADDER   closed/applicable dimensions per verb")
    for rung, n in d["ladder"].items():
        got, tot = rung.split("/")
        L.append(f"  {rung:<6} {n:>4} verb" + ("" if n == 1 else "s") + ("   <- nothing left open" if got == tot else ""))
    read = sum(1 for v in d["verbs"].values() if v["read_side_complete"])
    full = sum(1 for v in d["verbs"].values() if v["complete"])
    L.append(f"  {full} {'verb is' if full == 1 else 'verbs are'} closed on every dimension "
             "including execute position;")
    L.append(f"  {read} {'is' if read == 1 else 'are'} closed on the read-side contract "
             "(return type, arguments, behaviour),")
    L.append("  which is the figure worth quoting while the execute channel is deliberately thin.")
    L.append("")

    f = d["frontier"]
    L.append("FRONTIER        what is actually left, by dimension")
    for label, key in (("query verbs never swept for a type", "return_type_unswept"),
                       ("swept but empty in every context", "return_type_untyped"),
                       ("verbs with an unresolved tail", "arguments_open"),
                       ("never probed, but candidates exist", "arguments_unprobed_with_candidates"),
                       ("execute-capable, never executed", "execute_open"),
                       ("no Tier-1 row of any kind", "no_tier1_row_at_all"),
                       ("hardware-blocked", "blocked")):
        L.append(f"  {label:<38} {len(f[key]):>4}")
    L.append("")

    if d["staleness"]:
        L.append("STALE HEADERS   (the records were recounted; these summaries were not regenerated)")
        for note in d["staleness"]:
            L.append(f"  {note}")
        L.append("")

    if show == "settled":
        done = sorted(n for n, v in d["verbs"].items() if v["read_side_complete"])
        L.append(f"SETTLED VERBS   read-side contract closed ({len(done)}); "
                 "* also measured in execute position")
        for n in done:
            v = d["verbs"][n]
            tails = ", ".join(v["recognized_tails"]) or "takes no arguments"
            mark = "*" if v["dimensions"]["execute"] == "settled" else " "
            L.append(f" {mark}{n:<34} {v['observed_type'] or 'execute-only':<8} {tails}")
    elif show == "frontier":
        L.append("FRONTIER, BY NAME")
        for key, names in f.items():
            if not names:
                continue
            L.append("")
            L.append(f"  {key} ({len(names)})")
            for i in range(0, len(names), 4):
                L.append("    " + "  ".join(f"{x:<28}" for x in names[i:i + 4]).rstrip())
    else:
        L.append("`--settled` lists the finished verbs, `--frontier` lists what each dimension "
                 "is waiting on, `--format=json` gives the per-verb rows.")
    return "\n".join(L)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--format", choices=("text", "json"), default="text")
    ap.add_argument("--settled", action="store_true", help="list the verbs with nothing open")
    ap.add_argument("--frontier", action="store_true", help="list what each dimension awaits")
    args = ap.parse_args(argv)

    data = collect()
    if args.format == "json":
        print(json.dumps(data, indent=1))
        return 0
    show = "settled" if args.settled else "frontier" if args.frontier else None
    print(render(data, show))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
