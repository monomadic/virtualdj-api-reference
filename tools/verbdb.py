#!/usr/bin/env python3
"""Verb record store + query API for the VirtualDJ VDJScript reference.

The store (`docs/vdjscript-verbs.json`) is the authored home for per-verb facts:
tier, aliases, surfaces, kind, doc coverage, and — the part that used to be
scattered across the tracker and topical docs — local-test status, confidence,
and evidence. It is hand-editable through `put`, so the record is edited once
instead of promoted into three Markdown files.

The storage format is deliberately behind this CLI. Agents use the stable verbs
(`get`, `put`, `next-incomplete`, `stats`, `search`, `check`); the JSON layout
underneath can change (e.g. to one file per verb) without retraining them.

Bootstrap seeds the store from the existing generated index plus the coverage
audit and the local-test tracker. It is merge-safe: it never overwrites a field
that already carries an authored value.

Usage:
    python3 tools/verbdb.py get <name>
    python3 tools/verbdb.py put <name> field=value [field=value ...]
    python3 tools/verbdb.py next-incomplete
    python3 tools/verbdb.py stats
    python3 tools/verbdb.py search [term ...] [--surface=X] [--section=X]
                                   [--tier=X] [--status=X] [--kind=X]
                                   [--needs-test] [--format=json] [--limit=N]
    python3 tools/verbdb.py bootstrap [--merge | --force]
    python3 tools/verbdb.py check
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "docs" / "vdjscript-verbs.json"
INDEX = ROOT / "docs" / "vdjscript-verb-index.json"
AUDIT = ROOT / "docs" / "Official VDJScript Coverage Audit.md"
TRACKER = ROOT / "docs" / "VDJScript Local Test Tracker.md"

# ---- schema -----------------------------------------------------------------

TEST_STATUSES = {"Untested", "Partial", "Pass", "Fail", "N/A"}
LIST_FIELDS = {"aliases", "surfaces", "evidence"}
# Comma-splittable list fields. `evidence` is excluded on purpose: its entries are
# prose sentences that contain commas, so one `evidence=` is one entry.
CSV_FIELDS = {"aliases", "surfaces"}
# Fields that accumulate instead of replacing, so recording a second observation
# does not silently discard the first.
APPEND_FIELDS = {"evidence"}
BOOL_FIELDS = {"official", "needs_test", "blocked"}
# Fields settable via `put`. `forms`/nested contract detail are hand-edited in JSON.
SETTABLE = {
    "tier", "section", "canonical", "kind", "description", "example",
    "confidence", "test_status", "note",
} | LIST_FIELDS | BOOL_FIELDS

# The 17 hardware-gated Needs-Local-Test names from the coverage audit; these are
# blocked (cannot be closed without hardware) and are skipped by next-incomplete.
HARDWARE_BLOCKED = {
    "controllerscreen_deck", "controller_battery", "gemini_waveform_zoomlevel",
    "phase_movement", "phase_position", "phase_active", "v7_status",
    "rzx_touch", "rzx_touch_x", "rzx_touch_y",
    "djc_shift", "djc_button", "djc_button_popup", "djc_button_slider",
    "djc_button_select", "djc_panel", "denon_platter",
}


def default_record(name: str, *, official: bool = True) -> dict:
    return {
        # `official` defaults True because bootstrap only ever seeds names that
        # came from the official appendix. A record minted by `put --new` is not
        # in the index by definition, so it passes official=False.
        "name": name,
        "tier": "official-name-only" if official else "unofficial",
        "official": official,
        "aliases": [],
        "surfaces": [],
        "test_status": "Untested",
        "needs_test": False,
        "blocked": False,
        "evidence": [],
    }


# ---- store IO ---------------------------------------------------------------

def load_store() -> dict:
    if not STORE.exists():
        return {}
    return json.loads(STORE.read_text())["verbs"]


def counts(store: dict) -> dict:
    by_tier: dict[str, int] = {}
    by_status: dict[str, int] = {}
    documented = tested = needs = blocked = 0
    for rec in store.values():
        by_tier[rec.get("tier", "?")] = by_tier.get(rec.get("tier", "?"), 0) + 1
        st = rec.get("test_status", "Untested")
        by_status[st] = by_status.get(st, 0) + 1
        if rec.get("description"):
            documented += 1
        if st == "Pass":
            tested += 1
        if rec.get("needs_test"):
            needs += 1
        if rec.get("blocked"):
            blocked += 1
    return {
        "total": len(store),
        "by_tier": dict(sorted(by_tier.items())),
        "by_test_status": dict(sorted(by_status.items())),
        "documented": documented,
        "tested_pass": tested,
        "needs_test": needs,
        "blocked": blocked,
        "active_incomplete": needs - blocked - tested_and_needs(store),
    }


def tested_and_needs(store: dict) -> int:
    return sum(1 for r in store.values()
              if r.get("needs_test") and r.get("test_status") == "Pass")


def save_store(store: dict) -> None:
    payload = {
        "_meta": {
            "generated_by": "tools/verbdb.py",
            "note": "Authoritative per-verb record store. Edit via `just put-verb`, "
                    "not by hand-writing tables. Seeded by `verbdb.py bootstrap`.",
            "counts": counts(store),
        },
        "verbs": {k: store[k] for k in sorted(store)},
    }
    STORE.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n")


# ---- source parsers (bootstrap) ---------------------------------------------

def parse_audit_needs_test() -> set[str]:
    text = AUDIT.read_text()
    m = re.search(r"^## Needs Local Test\b.*?(?=^## )", text, re.S | re.M)
    if not m:
        return set()
    return set(re.findall(r"`([^`]+)`", m.group(0)))


def parse_tracker_results() -> dict[str, dict]:
    """Map verb -> {result, note, build, hardware} from the tracker status tables.

    Verb cells may hold several slash-separated backticked names; each maps to
    the row's result. A later Pass row wins over an earlier non-Pass one.

    The status tables share an 8-column layout ending `… | build | hardware |
    Result | Notes |`, so build and hardware sit two and one cells left of the
    result cell. Capturing them keeps the record's provenance (which build, what
    hardware) instead of discarding it into free-text prose.
    """
    rank = {"Untested": 0, "Partial": 1, "Fail": 1, "N/A": 1, "Pass": 2}
    out: dict[str, dict] = {}
    for line in TRACKER.read_text().splitlines():
        if not line.startswith("| `"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        result_idx = next((i for i, c in enumerate(cells[1:], 1)
                           if c in TEST_STATUSES), None)
        if result_idx is None:
            continue
        result = cells[result_idx]
        note = cells[result_idx + 1] if result_idx + 1 < len(cells) else ""
        # build/hardware are the two cells before result in the standard layout
        build = cells[result_idx - 2] if result_idx >= 2 else ""
        hardware = cells[result_idx - 1] if result_idx >= 1 else ""
        names = re.findall(r"`([^`]+)`", cells[0])
        for raw in names:
            name = raw.split()[0]  # strip arg examples like `sampler_loaded 8 'auto'`
            prev = out.get(name)
            if prev is None or rank[result] >= rank[prev["result"]]:
                out[name] = {"result": result, "note": note,
                             "build": build, "hardware": hardware}
    return out


def tracker_evidence(row: dict) -> str:
    """One provenance-carrying evidence sentence from a parsed tracker row."""
    build = row.get("build") or ""
    # the build column sometimes carries prose like "build not recorded"
    where = build if build and build.upper() != "TBD" else "build not recorded"
    hw = row.get("hardware") or ""
    tag = f"Local test ({where}"
    if hw and hw.lower() not in {"none required", "none recorded", "none", ""}:
        tag += f", hardware: {hw}"
    tag += ")"
    note = row.get("note") or ""
    return f"{tag}: {note}".strip() if note else tag


def bootstrap(mode: str) -> None:
    if STORE.exists() and mode not in {"--merge", "--force"}:
        sys.exit("store exists; pass --merge (safe: fill gaps only) or --force (rebuild)")
    index = json.loads(INDEX.read_text())["verbs"]
    needs = parse_audit_needs_test()
    results = parse_tracker_results()

    existing = {} if mode == "--force" else load_store()
    store: dict[str, dict] = {}

    for name, idx in index.items():
        rec = existing.get(name) or default_record(name)
        # merge-safe fill: set derived fields only when the current value is empty/default
        def fill(field, value):
            if value in (None, "", [], "official-name-only"):
                return
            cur = rec.get(field)
            if cur in (None, "", [], "Untested", False, "official-name-only") \
                    or (field == "tier" and cur == "official-name-only"):
                rec[field] = value

        fill("tier", idx.get("tier"))
        fill("section", idx.get("section"))
        fill("description", idx.get("description"))
        fill("example", idx.get("example"))
        fill("kind", idx.get("kind"))
        if idx.get("surfaces") and not rec.get("surfaces"):
            rec["surfaces"] = idx["surfaces"]
        if idx.get("aliases") and not rec.get("aliases"):
            rec["aliases"] = idx["aliases"]
        if idx.get("canonical"):
            rec.setdefault("canonical", idx["canonical"])
        rec["official"] = idx.get("official", rec.get("official", True))

        if name in needs and not rec.get("_authored_needs_test"):
            rec["needs_test"] = True
        if name in HARDWARE_BLOCKED:
            rec["blocked"] = True
        if name in results:
            row = results[name]
            # never downgrade an authored Pass
            if rec.get("test_status", "Untested") != "Pass":
                rec["test_status"] = row["result"]
            if row["note"] and "note" not in rec:
                rec["note"] = row["note"][:400]
            # Only an actually-tested row is evidence. A tracker row whose result
            # is Untested/N/A is a test *plan*, not a result — stamping it
            # `Local test` would be a false claim. A tested status must then
            # carry structured evidence + confidence (the `just check` gate),
            # filled only when empty so a hand-authored entry is never clobbered.
            if row["result"] in {"Pass", "Fail", "Partial"}:
                if not rec.get("evidence"):
                    rec["evidence"] = [tracker_evidence(row)[:400]]
                if not rec.get("confidence"):
                    rec["confidence"] = "local_test"

        store[name] = rec

    # preserve any authored records not present in the index
    for name, rec in existing.items():
        store.setdefault(name, rec)

    save_store(store)
    c = counts(store)
    print(f"bootstrapped {c['total']} records: "
          f"needs_test={c['needs_test']} (blocked={c['blocked']}), "
          f"documented={c['documented']}, tested_pass={c['tested_pass']}")


# ---- commands ---------------------------------------------------------------

def joined_view(name: str, rec: dict) -> dict:
    """One-stop contract answer: join the extraction/observation artifacts at
    read time (never copied into the store — the artifacts stay authoritative).
    Missing artifacts degrade silently to the bare store record."""
    out = dict(rec)

    def artifact(path):
        try:
            return json.load(open(ROOT / path))
        except (OSError, json.JSONDecodeError):
            return None

    table = artifact("tests/verb-table.json")
    if table:
        t = table["verbs"].get(name)
        if t:
            siblings = [n for n, r in table["verbs"].items()
                        if r["id"] == t["id"] and n != name]
            out["verb_table"] = {**t, "canonical_spelling": t["flags"] != 1,
                                 "editor_hidden": t["flags"] == 256,
                                 **({"same_id_as": siblings} if siblings else {})}
        else:
            out["verb_table"] = {"present": False,
                                 "meaning": "NOT a verb on this build (rule 1b)"}
    contracts = artifact("tests/action-contracts.json")
    if contracts and name in contracts["verbs"]:
        out["contract"] = contracts["verbs"][name]
    sweep = artifact("tests/verb-existence-sweep.json")
    if sweep and name in sweep["verbs"]:
        s = sweep["verbs"][name]
        out["http_probe"] = {k: s[k] for k in ("status", "kind") if k in s}
    rtypes = artifact("tests/verb-return-types.json")
    if rtypes and name in rtypes["verbs"]:
        r = rtypes["verbs"][name]
        out["observed_return"] = {"type": r["observed_type"],
                                  "sample": next(iter(r["samples"].values()), None)}
    return out


def cmd_get(args):
    if not args:
        sys.exit("usage: get <name> [--raw]")
    raw = "--raw" in args
    args = [a for a in args if a != "--raw"]
    store = load_store()
    name = args[0]
    rec = store.get(name)
    view = (lambda n, r: r) if raw else joined_view

    # An alias record carries little but a pointer; follow it to the canonical.
    if rec is not None and rec.get("tier") == "alias" and rec.get("canonical"):
        canon = store.get(rec["canonical"])
        if canon:
            print(f"# '{name}' is an alias of '{rec['canonical']}'")
            print(json.dumps(view(rec["canonical"], canon), indent=1,
                             ensure_ascii=False))
            return
    if rec is not None:
        print(json.dumps(view(name, rec), indent=1, ensure_ascii=False))
        return

    # not a record name: maybe it is listed as someone's alias
    for n, r in store.items():
        if name in r.get("aliases", []):
            print(f"# '{name}' is an alias of '{n}'")
            print(json.dumps(view(n, r), indent=1, ensure_ascii=False))
            return

    pool = set(store) | {a for r in store.values() for a in r.get("aliases", [])}
    near = difflib.get_close_matches(name, sorted(pool), n=5, cutoff=0.6)
    msg = f"no record for '{name}'"
    if near:
        msg += "\ndid you mean: " + ", ".join(near)
    msg += f"\nor try: just find-verbs {name}"
    sys.exit(msg)


def coerce(field: str, value: str):
    if field in BOOL_FIELDS:
        return value.lower() in {"1", "true", "yes", "on"}
    if field in CSV_FIELDS:
        return [v.strip() for v in value.split(",") if v.strip()]
    if field in LIST_FIELDS:
        return [value.strip()] if value.strip() else []
    if field == "test_status" and value not in TEST_STATUSES:
        sys.exit(f"test_status must be one of {sorted(TEST_STATUSES)}")
    return value


def cmd_put(args):
    args = list(args)
    allow_new = "--new" in args
    if allow_new:
        args.remove("--new")
    if len(args) < 2:
        sys.exit("usage: put <name> field=value [field=value ...] [--new]")
    store = load_store()
    name = args[0]
    rec = store.get(name)
    if rec is None:
        # Minting a record for an unknown name must be deliberate: otherwise a
        # typo silently becomes a junk record claiming to be an official verb.
        if not allow_new:
            msg = (f"'{name}' has no record and is not in the official index.\n"
                   "If that is a typo, fix it. If the name is real but unofficial "
                   "(a scope wrapper, a hidden candidate), record it explicitly:\n"
                   f"  just put-verb {name} --new field=value ...")
            near = difflib.get_close_matches(name, list(store), n=5, cutoff=0.6)
            if near:
                msg += "\ndid you mean: " + ", ".join(near)
            sys.exit(msg)
        rec = default_record(name, official=False)
    for pair in args[1:]:
        if "=" not in pair:
            sys.exit(f"bad assignment '{pair}' (want field=value)")
        field, _, value = pair.partition("=")
        if field not in SETTABLE:
            sys.exit(f"field '{field}' not settable; allowed: {sorted(SETTABLE)}")
        new = coerce(field, value)
        if field in APPEND_FIELDS:
            kept = [v for v in rec.get(field, []) if v not in new]
            rec[field] = kept + new
        else:
            rec[field] = new
        if field == "needs_test":
            rec["_authored_needs_test"] = True
    store[name] = rec
    save_store(store)
    print(json.dumps(rec, indent=1, ensure_ascii=False))


def priority(rec: dict) -> tuple:
    # lower sorts first: prefer documented, higher-tier, non-blocked
    tier_rank = {"curated": 0, "catalog": 1, "alias": 2, "official-name-only": 3}
    return (
        0 if rec.get("description") else 1,
        tier_rank.get(rec.get("tier"), 9),
        rec.get("name", ""),
    )


def cmd_next_incomplete(args):
    store = load_store()
    candidates = [
        r for r in store.values()
        if r.get("needs_test") and not r.get("blocked")
        and r.get("test_status") != "Pass"
    ]
    if not candidates:
        print("no active (non-blocked) incomplete verbs; "
              "check `stats` for the blocked/hardware queue")
        return
    candidates.sort(key=priority)
    print(json.dumps(candidates[0], indent=1, ensure_ascii=False))
    if len(candidates) > 1:
        rest = ", ".join(r["name"] for r in candidates[1:8])
        print(f"\n# {len(candidates)-1} more active: {rest}"
              f"{' ...' if len(candidates) > 9 else ''}", file=sys.stderr)


def cmd_stats(args):
    print(json.dumps(counts(load_store()), indent=1, ensure_ascii=False))


FILTERS = {"surface", "section", "tier", "status", "kind"}


def cmd_search(args):
    """Filtered query. Terms AND with filters; category listings are just an
    unfiltered query, so no grouped dump needs to exist on disk."""
    terms, opts = [], {}
    fmt, limit = "table", 50
    for a in args:
        if a.startswith("--"):
            key, _, val = a[2:].partition("=")
            if key == "format":
                fmt = val
            elif key == "limit":
                limit = int(val) if val else 0
            elif key == "needs-test":
                opts["needs_test"] = True
            elif key in FILTERS:
                opts[key] = val
            else:
                sys.exit(f"unknown option --{key}; filters: "
                         f"{sorted(FILTERS)} + --needs-test, --format, --limit")
        else:
            terms.append(a.lower())

    if not terms and not opts:
        sys.exit("search needs a term or a filter (e.g. --surface=Pad, "
                 "--needs-test).\nFor the VDJScript verb named `search`, use: "
                 "just get-verb search")

    store = load_store()
    hits = []
    for name, rec in store.items():
        if opts.get("needs_test") and not rec.get("needs_test"):
            continue
        if "surface" in opts and opts["surface"].lower() not in \
                [s.lower() for s in rec.get("surfaces", [])]:
            continue
        for key, field in (("section", "section"), ("tier", "tier"),
                           ("status", "test_status"), ("kind", "kind")):
            if key in opts and opts[key].lower() not in \
                    str(rec.get(field, "")).lower():
                break
        else:
            hay = " ".join([
                name, rec.get("description", ""),
                " ".join(rec.get("aliases", [])), rec.get("section", ""),
            ]).lower()
            if all(t in hay for t in terms):
                hits.append(rec)

    hits.sort(key=priority)
    shown = hits[:limit] if limit else hits
    if fmt == "json":
        print(json.dumps(shown, indent=1, ensure_ascii=False))
    else:
        for rec in shown:
            al = f"  aliases={','.join(rec['aliases'])}" if rec.get("aliases") else ""
            print(f"{rec['name']:<28} [{rec.get('tier','?')}/"
                  f"{rec.get('test_status','?')}] {rec.get('description','')}{al}")
    where = " ".join(terms) + " " + " ".join(f"--{k}={v}" for k, v in opts.items())
    note = f"showing {len(shown)} of {len(hits)}" if len(shown) != len(hits) \
        else f"{len(hits)} match(es)"
    print(f"\n{note} for [{where.strip()}]", file=sys.stderr)


def cmd_check(args):
    if not STORE.exists():
        sys.exit("store missing; run `python3 tools/verbdb.py bootstrap`")
    store = load_store()
    index = json.loads(INDEX.read_text())["verbs"]
    errors = []

    # coverage: every official index name has a record
    missing = set(index) - set(store)
    if missing:
        errors.append(f"{len(missing)} index names missing from store: "
                      f"{sorted(missing)[:5]}...")

    # coverage: every verb-table name has a record, and every record absent
    # from the verb table must say why it is in a *verb* store at all
    # (disproven, or a non-verb construct kept for discoverability).
    table_path = ROOT / "tests" / "verb-table.json"
    if table_path.exists():
        table = set(json.loads(table_path.read_text())["verbs"])
        known = set(store) | {a for r in store.values() for a in r.get("aliases", [])}
        gap = table - known
        if gap:
            errors.append(f"{len(gap)} verb-table names missing from store: "
                          f"{sorted(gap)[:5]}...")
        for name in sorted(set(store) - table):
            rec = store[name]
            if rec.get("test_status") == "Fail":
                continue  # disproven names stay, carrying their disproof
            if rec.get("kind") in {"modifier", "special-control"}:
                continue  # grammar/mapper constructs, not verbs
            if "scope wrapper" in (rec.get("note") or ""):
                continue
            errors.append(f"{name}: not in the verb table and not marked as a "
                          f"disproven name or non-verb construct (rule 1b)")

    for name, rec in store.items():
        if rec.get("name") != name:
            errors.append(f"{name}: record 'name' mismatch ({rec.get('name')})")
        st = rec.get("test_status", "Untested")
        if st not in TEST_STATUSES:
            errors.append(f"{name}: invalid test_status '{st}'")
        # A tested status must carry its proof as structured evidence, not just a
        # free-text note. This is the gate that keeps status and evidence from
        # drifting apart the way the bootstrap-seeded records once did.
        if st in {"Pass", "Fail", "Partial"} and not rec.get("evidence"):
            errors.append(f"{name}: test_status '{st}' but no evidence "
                          f"(record the proof with `just put-verb {name} "
                          f"evidence=\"…\"`)")
        canon = rec.get("canonical")
        if canon and canon not in store:
            errors.append(f"{name}: canonical '{canon}' has no record")
        for al in rec.get("aliases", []):
            if al not in store and al not in index:
                errors.append(f"{name}: alias '{al}' unresolved")

    # staleness: store counts must match what save would write
    payload = json.loads(STORE.read_text())
    if payload["_meta"]["counts"] != counts(store):
        errors.append("stored _meta.counts is stale; re-save via any put or bootstrap --merge")

    if errors:
        print("verbdb check FAILED:")
        for e in errors[:40]:
            print(f"  - {e}")
        sys.exit(1)
    c = counts(store)
    print(f"verbdb check passed: {c['total']} records, "
          f"needs_test={c['needs_test']} (blocked={c['blocked']}), "
          f"tested_pass={c['tested_pass']}")


COMMANDS = {
    "get": cmd_get,
    "put": cmd_put,
    "next-incomplete": cmd_next_incomplete,
    "stats": cmd_stats,
    "search": cmd_search,
    "check": cmd_check,
}


USAGE = """usage: verbdb.py <command> ... | verbdb.py <verb-name>

  <verb-name>            shorthand for `get <verb-name>`
  get <name>             one record (follows aliases)
  put <name> f=v ...     set fields
  search [term] [--surface= --section= --tier= --status= --kind=
                  --needs-test --format=json --limit=N]
  next-incomplete        next active (non-hardware-blocked) work item
  stats                  counts by tier / test status
  check                  validate the store
  bootstrap [--merge|--force]

Note: `search` is also a VDJScript verb name. Commands win; use
`verbdb.py get search` for the verb record."""


def main(argv):
    if not argv:
        sys.exit(USAGE)
    cmd, rest = argv[0], argv[1:]
    if cmd in {"-h", "--help", "help"}:
        print(USAGE)
        return
    if cmd == "bootstrap":
        bootstrap(rest[0] if rest else "")
        return
    if cmd in COMMANDS:
        COMMANDS[cmd](rest)
        return
    # Not a command: treat a bare argument as a verb lookup, for direct
    # `python3 tools/verbdb.py leftdeck` use. The `just` recipes are flat
    # (get-verb / find-verbs / ...) and always pass an explicit subcommand.
    cmd_get(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
