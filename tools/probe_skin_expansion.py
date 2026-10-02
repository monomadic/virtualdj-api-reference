#!/usr/bin/env python3
"""Paired native fixtures for skin class, placeholder and condition expansion (9246, Tier 2).

Each case pairs a rule with its control and states, before the run, which button
rectangles the rule predicts. The rules come from the disassembly read for TODO
task K3 (docs/Skin Expansion.md); this probe is how they meet the native code.
It reuses the composition host: the copied 9246 image loads the fixture through
CSkinWindow::load in a sandboxed worker, and the host reads back the object tree.
Nothing is rendered and the host evaluates nothing itself, but conditions are
evaluated by the native loader as it would at skin load.

  prepare --app APP --work DIR      build the host with these cases (needs capstone)
  run --work DIR --output FILE      one sandboxed worker per case
  check [--capture FILE]            compare a saved capture with the predictions
"""
import argparse
import json
import sys
from pathlib import Path

import probe_skin_composition as composition

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "tests" / "skin-expansion-9246.json"


def button(x, y, w, h):
    return [x, y, w, h]


# (name, rule under test, XML inside <skin>, predicted CSkinButton rects in tree order)
CASES = [
    # Placeholders: whole-value by default, substring only when a `*` entry exists.
    ("placeholder_value", "an element attribute named by a placeholder replaces `[NAME]`",
     '<define class="t" placeholders="W=50"><size width="[W]" height="20"/></define>'
     '<button class="t" W="70"><pos x="10" y="10"/></button>',
     [button(10, 10, 70, 20)]),
    ("placeholder_default", "control: without the attribute the default after `=` is used",
     '<define class="t" placeholders="W=50"><size width="[W]" height="20"/></define>'
     '<button class="t"><pos x="10" y="10"/></button>',
     [button(10, 10, 50, 20)]),
    ("placeholder_substring_off", "without a `*` entry, `[NAME]` inside a longer value is not replaced",
     '<define class="t" placeholders="W=5"><size width="1[W]" height="20"/></define>'
     '<button class="t" W="7"><pos x="10" y="10"/></button>',
     "not:" + json.dumps([button(10, 10, 17, 20)])),
    ("placeholder_substring_on", "control: a `*` entry turns on substring replacement",
     '<define class="t" placeholders="*W=5"><size width="1[W]" height="20"/></define>'
     '<button class="t" W="7"><pos x="10" y="10"/></button>',
     [button(10, 10, 17, 20)]),
    ("placeholder_case", "the token must be written in upper case: `[w]` is not `[W]`",
     '<define class="t" placeholders="W=50"><size width="[w]" height="20"/></define>'
     '<button class="t" W="70"><pos x="10" y="10"/></button>',
     "not:" + json.dumps([button(10, 10, 70, 20)])),
    # Class variants: the first definition, in order, whose classdeck is absent or equal wins.
    ("classdeck_specific_first", "a deck-specific definition made first wins for its deck only",
     '<define class="t" classdeck="2"><size width="20" height="20"/></define>'
     '<define class="t"><size width="30" height="30"/></define>'
     '<button class="t" deck="2"><pos x="10" y="10"/></button>'
     '<button class="t" deck="1"><pos x="60" y="10"/></button>',
     [button(10, 10, 20, 20), button(60, 10, 30, 30)]),
    ("classdeck_generic_first", "control: a generic definition made first shadows the deck-specific one",
     '<define class="t"><size width="30" height="30"/></define>'
     '<define class="t" classdeck="2"><size width="20" height="20"/></define>'
     '<button class="t" deck="2"><pos x="10" y="10"/></button>',
     [button(10, 10, 30, 30)]),
    ("class_redefined", "redefining the same class and deck replaces the earlier definition",
     '<define class="t"><size width="10" height="10"/></define>'
     '<define class="t"><size width="40" height="40"/></define>'
     '<button class="t"><pos x="10" y="10"/></button>',
     [button(10, 10, 40, 40)]),
    # Children merge by name and occurrence: the element's n-th `size` absorbs the class's n-th.
    # A plain append would leave the class's first size passing and give 80x24.
    ("class_children_by_occurrence", "the element's first `size` merges with the class's first; the rest append",
     '<define class="t"><size width="80" height="24"/><size width="90" height="30"/></define>'
     '<button class="t"><pos x="10" y="10"/><size condition="false" width="5"/></button>',
     [button(10, 10, 90, 30)]),
    ("class_children_copied", "control: with no `size` of its own the element gets the class's, first one passing",
     '<define class="t"><size width="80" height="24"/><size width="90" height="30"/></define>'
     '<button class="t"><pos x="10" y="10"/></button>',
     [button(10, 10, 80, 24)]),
    ("class_on_child_ignored", "`class` applies only to objects and windows: on a `size` child it does nothing",
     '<define class="s"><size width="30" height="30"/></define>'
     '<button><pos x="10" y="10"/><size class="s"/></button>',
     [button(10, 10, 0, 0)]),
    ("class_on_object", "control: the same definition applied through the object takes effect",
     '<define class="s"><size width="30" height="30"/></define>'
     '<button class="s"><pos x="10" y="10"/></button>',
     [button(10, 10, 30, 30)]),
    # Conditions: evaluated once at load; a failing slot falls back to the next same-named one.
    ("condition_size_fallback", "a `size` whose condition fails yields to the next `size`",
     '<button><pos x="10" y="10"/><size condition="false" width="10" height="10"/>'
     '<size width="20" height="20"/></button>',
     [button(10, 10, 20, 20)]),
    ("condition_size_first", "control: the first `size` is used when its condition passes",
     '<button><pos x="10" y="10"/><size condition="true" width="10" height="10"/>'
     '<size width="20" height="20"/></button>',
     [button(10, 10, 10, 10)]),
    ("condition_object", "a factory object whose condition fails is not created",
     '<button condition="false"><pos x="10" y="10"/><size width="10" height="10"/></button>'
     '<button condition="true"><pos x="60" y="10"/><size width="20" height="20"/></button>',
     [button(60, 10, 20, 20)]),
    # The os gate: present only when exactly `mac` (case-sensitive) or absent.
    ("os_gate", "`os` must be exactly `mac`; `win` and `MAC` drop the object",
     '<button os="mac"><pos x="10" y="10"/><size width="10" height="10"/></button>'
     '<button os="win"><pos x="30" y="10"/><size width="10" height="10"/></button>'
     '<button os="MAC"><pos x="50" y="10"/><size width="10" height="10"/></button>'
     '<button><pos x="70" y="10"/><size width="10" height="10"/></button>',
     [button(10, 10, 10, 10), button(70, 10, 10, 10)]),
    # Group wrapper: condition gates its children; x/y offset relative positions.
    ("group_condition", "a plain `group` whose condition fails drops its children",
     '<group condition="false"><button><pos x="10" y="10"/><size width="10" height="10"/></button></group>'
     '<group><button><pos x="60" y="10"/><size width="20" height="20"/></button></group>',
     [button(60, 10, 20, 20)]),
    ("group_offset", "a plain `group`'s x/y offset its children's relative positions",
     '<group x="30" y="20"><button><pos x="+1" y="+2"/><size width="10" height="10"/></button></group>',
     [button(31, 22, 10, 10)]),
]


def fixtures():
    return [(name, '<skin name="Expansion probe" version="8" width="320" height="200">' + xml + "</skin>")
            for name, _, xml, _ in CASES]


def buttons(tree):
    out = []
    def walk(node):
        if node["class"] == "CSkinButton":
            out.append([round(v) for v in node["current_rect"]])
        for child in node.get("children", []):
            walk(child)
    walk(tree)
    return out


def check(capture: Path) -> int:
    data = json.loads(capture.read_text())
    runs = {r["name"]: r for r in data["runs"]}
    failures = 0
    for name, rule, _, expected in CASES:
        row = runs.get(name)
        if not row or not row.get("completed"):
            print(f"INCOMPLETE {name}: worker did not finish ({rule})")
            failures += 1
            continue
        tree = next(e["tree"] for e in row["events"] if e["event"] == "composition" and e["stage"] == "loaded")
        got = buttons(tree)
        if isinstance(expected, str) and expected.startswith("not:"):
            ok = got != json.loads(expected[4:])
        else:
            ok = got == expected
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {name}: {got}  — {rule}")
    print(f"skin expansion check {'passed' if not failures else 'FAILED'}: "
          f"build {data['preparation']['build']}, {len(CASES) - failures}/{len(CASES)} predictions held")
    return 1 if failures else 0


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("mode", choices=["prepare", "run", "check"])
    p.add_argument("--app", type=Path)
    p.add_argument("--work", type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--capture", type=Path, default=DEFAULT)
    a = p.parse_args(argv)
    if a.mode == "check":
        return check(a.capture)
    if a.work is None:
        p.error("--work is required")
    if a.mode == "prepare":
        if a.app is None:
            p.error("--app is required")
        composition.probe_skin_host.prepare(a.app.resolve(), a.work.resolve())
        composition.finish_prepare(a.work.resolve(), cases=fixtures())
        return 0
    if a.output is None:
        p.error("--output is required")
    composition.run(a.work.resolve(), a.output.resolve(), cases=fixtures())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
