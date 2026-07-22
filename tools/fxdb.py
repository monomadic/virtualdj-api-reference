#!/usr/bin/env python3
"""Query API over the swept native effects catalog.

Reads `tests/fx-introspection-dump.json` (produced by
`tools/sweep_fx_introspection.py` against a running VirtualDJ) and answers
questions about effect controls directly, so nothing has to read the dump or a
Markdown copy of it. Effect structure is fully machine-derived — there are no
hand-authored facts here, so there is no `put`; re-run the sweep to refresh.

Usage:
    python3 tools/fxdb.py get <effect>
    python3 tools/fxdb.py search [term ...] [--min-sliders=N] [--max-sliders=N]
                                 [--min-buttons=N] [--has-slider=LABEL]
                                 [--has-button=LABEL] [--in-cycle] [--name-only]
                                 [--format=json] [--limit=N]
    python3 tools/fxdb.py stats
    python3 tools/fxdb.py check
"""
from __future__ import annotations

import difflib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DUMP = ROOT / "tests" / "fx-introspection-dump.json"


def load() -> dict:
    if not DUMP.exists():
        sys.exit(f"missing {DUMP.relative_to(ROOT)}; run "
                 "`python3 tools/sweep_fx_introspection.py > tests/fx-introspection-dump.json`")
    return json.loads(DUMP.read_text())


def find(effects: list[dict], name: str) -> dict | None:
    for e in effects:  # exact
        if e["effect"] == name:
            return e
    low = name.lower().replace(" ", "")
    for e in effects:  # case/space-insensitive
        if e["effect"].lower().replace(" ", "") == low:
            return e
    for e in effects:  # substring
        if low in e["effect"].lower().replace(" ", ""):
            return e
    return None


def fmt_effect(e: dict) -> str:
    lines = [f"{e['effect']}  (sliders={e['slider_count']} buttons={e['button_count']})"]
    reached = e.get("reached", {})
    tags = []
    if reached.get("in_cycle"):
        tags.append("in enabled cycle")
    if reached.get("by_name"):
        tags.append("name-selectable")
    if tags:
        lines.append("  " + ", ".join(tags))
    for s in e.get("sliders", []):
        lines.append(f"  S{s['index']} {s.get('full','')} / {s.get('short','')}"
                     f"   (current: {s.get('text','')})")
    for b in e.get("buttons", []):
        lines.append(f"  B{b['index']} {b.get('short','')}")
    return "\n".join(lines)


def cmd_get(args):
    if not args:
        sys.exit("usage: get <effect>")
    data = load()
    asked = " ".join(args)
    e = find(data["effects"], asked)
    if e is None:
        names = [x["effect"] for x in data["effects"]]
        near = difflib.get_close_matches(asked, names, n=5, cutoff=0.5)
        msg = f"no effect matching '{asked}'"
        if near:
            msg += "\ndid you mean: " + ", ".join(near)
        failed = data.get("failed_by_name", [])
        if any(asked.lower() == f.lower() for f in failed):
            msg += (f"\nnote: '{asked}' is recorded in failed_by_name — it did not "
                    "load into slot 1 during the sweep")
        sys.exit(msg)
    print(fmt_effect(e))


def label_hit(e: dict, needle: str, kind: str) -> bool:
    needle = needle.lower()
    items = e.get("sliders" if kind == "slider" else "buttons", [])
    for it in items:
        if needle in str(it.get("short", "")).lower() \
                or needle in str(it.get("full", "")).lower():
            return True
    return False


def cmd_search(args):
    terms, opts = [], {}
    fmt, limit = "table", 50
    for a in args:
        if a.startswith("--"):
            key, _, val = a[2:].partition("=")
            if key == "format":
                fmt = val
            elif key == "limit":
                limit = int(val) if val else 0
            elif key in {"in-cycle", "name-only"}:
                opts[key] = True
            elif key in {"min-sliders", "max-sliders", "min-buttons",
                         "max-buttons", "has-slider", "has-button"}:
                opts[key] = val
            else:
                sys.exit(f"unknown option --{key}")
        else:
            terms.append(a.lower())

    data = load()
    hits = []
    for e in data["effects"]:
        sc, bc = e.get("slider_count") or 0, e.get("button_count") or 0
        if "min-sliders" in opts and sc < int(opts["min-sliders"]):
            continue
        if "max-sliders" in opts and sc > int(opts["max-sliders"]):
            continue
        if "min-buttons" in opts and bc < int(opts["min-buttons"]):
            continue
        if "max-buttons" in opts and bc > int(opts["max-buttons"]):
            continue
        if "has-slider" in opts and not label_hit(e, opts["has-slider"], "slider"):
            continue
        if "has-button" in opts and not label_hit(e, opts["has-button"], "button"):
            continue
        reached = e.get("reached", {})
        if opts.get("in-cycle") and not reached.get("in_cycle"):
            continue
        if opts.get("name-only") and reached.get("in_cycle"):
            continue
        if terms:
            hay = json.dumps(e).lower()
            if not all(t in hay for t in terms):
                continue
        hits.append(e)

    hits.sort(key=lambda e: e["effect"].lower())
    shown = hits[:limit] if limit else hits
    if fmt == "json":
        print(json.dumps(shown, indent=1, ensure_ascii=False))
    else:
        for e in shown:
            print(f"{e['effect']:<22} sliders={e['slider_count']:<3} "
                  f"buttons={e['button_count']:<3} "
                  f"{'cycle' if e.get('reached',{}).get('in_cycle') else 'name-only'}")
    note = f"showing {len(shown)} of {len(hits)}" if len(shown) != len(hits) \
        else f"{len(hits)} match(es)"
    print(f"\n{note}", file=sys.stderr)


def cmd_stats(args):
    data = load()
    effects = data["effects"]
    no_ctrl = [e["effect"] for e in effects
               if not e.get("slider_count") and not e.get("button_count")]
    print(json.dumps({
        "vdj_version": data.get("vdj_version"),
        "reachable": len(effects),
        "in_enabled_cycle": data.get("cycle_enabled_count"),
        "name_only": len(effects) - sum(
            1 for e in effects if e.get("reached", {}).get("in_cycle")),
        "failed_by_name": data.get("failed_by_name", []),
        "max_sliders": max((e.get("slider_count") or 0 for e in effects), default=0),
        "max_buttons": max((e.get("button_count") or 0 for e in effects), default=0),
        "no_controls": no_ctrl,
    }, indent=1, ensure_ascii=False))


def cmd_check(args):
    data = load()
    errors = []
    effects = data.get("effects")
    if not effects:
        errors.append("dump has no effects")
    seen = set()
    for e in effects or []:
        name = e.get("effect")
        if not name:
            errors.append("record with no effect name")
            continue
        if name in seen:
            errors.append(f"duplicate effect record '{name}'")
        seen.add(name)
        for key in ("slider_count", "button_count"):
            if e.get(key) is None:
                continue
            listed = len(e.get("sliders" if key == "slider_count" else "buttons", []))
            if listed != e[key]:
                errors.append(f"{name}: {key}={e[key]} but {listed} entries listed")
    if errors:
        print("fxdb check FAILED:")
        for err in errors[:20]:
            print(f"  - {err}")
        sys.exit(1)
    print(f"fxdb check passed: {len(effects)} effects, "
          f"VirtualDJ {data.get('vdj_version')}")


COMMANDS = {"get": cmd_get, "search": cmd_search, "stats": cmd_stats,
            "check": cmd_check}


USAGE = """usage: fxdb.py <command> ... | fxdb.py <effect-name>

  <effect-name>          shorthand for `get <effect-name>`
  get <effect>           control map (spelling-tolerant)
  search [term] [--min-sliders=N --max-sliders=N --min-buttons=N
                 --max-buttons=N --has-slider=LABEL --has-button=LABEL
                 --in-cycle --name-only --format=json --limit=N]
  stats                  catalog summary
  check                  validate the sweep artifact"""


def main(argv):
    if not argv:
        sys.exit(USAGE)
    cmd, rest = argv[0], argv[1:]
    if cmd in {"-h", "--help", "help"}:
        print(USAGE)
        return
    if cmd in COMMANDS:
        COMMANDS[cmd](rest)
        return
    # Bare argument: treat as an effect lookup (`just get-fx Echo`).
    cmd_get(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
