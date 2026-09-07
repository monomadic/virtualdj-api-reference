#!/usr/bin/env python3
"""Which of Atomix's own source modules implements each verb.

Bundle 18.0.9246 ships STABS debug symbols alongside its symbol table — the
same escape-hatch build `extract_action_vtables.py` uses, reading a different
part of it. `dsymutil -symtab` emits N_OSO records naming each object file and
N_FUN records for the functions linked from it, so every `ACTION_` method can
be attributed to the translation unit it was compiled in.

The result is a complete partition: all 952 `ACTION_` classes across 37
`action_*.cpp` modules, each class in exactly one. It is Atomix's own build
metadata about where code lives — Tier 2 by Evidence Standards. It is strong
evidence of how the vendor GROUPS a verb, and no evidence at all that the verb
works; nothing here may set a test status.

The module is coarser than the store's `section` in several places, so it does
not translate to one mechanically. `action_audio` splits into Deck Management
and Audio Playback; `action_param` three ways; `action_get` is a grab-bag of
117 queries whose sectioned members land in three different sections. `--sections`
reports, per module, whether its sectioned members agree well enough to name a
section for the rest: `clean` (backfillable), `mixed` (they disagree — the store's
taxonomy is finer than the module), `too-few` (unanimous, but on too little to
extrapolate) and `no-evidence` (nothing sectioned at all). Only `clean` should be
backfilled.

Regeneration needs the unstripped build, which is not the installed app:

    pkgutil --expand-full install_virtualdj_2026_b9246_mac.pkg /tmp/b9246
    python3 tools/extract_action_modules.py \\
        --app '/tmp/b9246/vdj.pkg/Payload/VirtualDJ.app' > tests/action-modules-9246.json

Queries and `--check` read the committed artifact and need no binary.
"""

from __future__ import annotations

import argparse
import json
import os
import plistlib
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ARTIFACT = Path("tests/action-modules-9246.json")
STORE = Path("docs/vdjscript-verbs.json")

# `[  12] 000abc 24 (N_FUN ) 01 0000 0000000100002000 '__ZN20ACTION_play9onExecuteEv'`
STAB = re.compile(r"\((N_OSO|N_FUN)\s*\).*?'(.*)'$")
# Itanium mangling: the length prefix delimits the class name. Matching greedily
# instead runs past it into the method name and reports 3,901 classes, not 952.
MANGLED = re.compile(r"^_*_ZN(\d+)(.+)")

# A module may name a section for its unsectioned members only when its already
# sectioned ones agree this strongly. Below either bar the module is a grab-bag
# and the store's finer taxonomy wins.
CLEAN_FRACTION = 0.9
CLEAN_MINIMUM = 5


def stabs(binary: Path) -> str:
    return subprocess.check_output(["dsymutil", "-symtab", str(binary)],
                                   text=True, errors="replace")


def class_module_sets(dump: str, prefix: str = "ACTION_") -> dict[str, set[str]]:
    """Classes -> defining object files, preserving cross-module methods."""
    current = None
    found: dict[str, set[str]] = defaultdict(set)
    for line in dump.splitlines():
        match = STAB.search(line)
        if not match:
            continue
        kind, value = match.groups()
        if kind == "N_OSO":
            current = os.path.basename(value)
            continue
        if current is None:
            continue
        mangled = MANGLED.match(value)
        if not mangled:
            continue
        length, rest = int(mangled.group(1)), mangled.group(2)
        if len(rest) < length:
            continue
        name = rest[:length]
        if name.startswith(prefix):
            found[name].add(current)
    return dict(found)


def class_modules(dump: str, prefix: str = "ACTION_") -> dict[str, str]:
    """Class with the requested prefix -> its unique defining object file."""
    found = class_module_sets(dump, prefix)
    # Every class should live in exactly one module; a split would mean the
    # partition is not one, and silently taking the first would hide it.
    split = {c: sorted(m) for c, m in found.items() if len(m) > 1}
    if split:
        sys.exit(f"classes defined in more than one module: {split}")
    return {c: m.pop() for c, m in found.items()}


def load_store() -> tuple[dict, dict[str, str]]:
    verbs = json.loads(STORE.read_text())["verbs"]
    canonical: dict[str, str] = {}
    for name, record in verbs.items():
        canonical[name] = name
        for alias in record.get("aliases", []):
            canonical.setdefault(alias, name)
    return verbs, canonical


def section_report(modules: dict[str, list[str]]) -> dict:
    """Per module: can its sectioned members name a section for the rest?"""
    verbs, canonical = load_store()
    report = {}
    for module, members in sorted(modules.items()):
        sectioned: Counter[str] = Counter()
        unsectioned = []
        for verb in members:
            name = canonical.get(verb)
            if name is None:
                continue
            section = verbs[name].get("section")
            if section:
                sectioned[section] += 1
            else:
                unsectioned.append(name)
        known = sum(sectioned.values())
        top, count = sectioned.most_common(1)[0] if known else (None, 0)
        if not known:
            verdict = "no-evidence"          # nothing sectioned; nothing to generalise from
        elif count / known < CLEAN_FRACTION:
            verdict = "mixed"                # members genuinely disagree; the store is finer
        elif known < CLEAN_MINIMUM:
            verdict = "too-few"              # unanimous, but on too little to extrapolate
        else:
            verdict = "clean"
        report[module] = {
            "verdict": verdict,
            "section": top if verdict == "clean" else None,
            "sections": dict(sectioned.most_common()),
            "unsectioned": sorted(unsectioned),
        }
    return report


def build_artifact(app: Path) -> dict:
    binary = app / "Contents/MacOS/VirtualDJ"
    if not binary.exists():
        sys.exit(f"no binary at {binary}")
    mapping = class_modules(stabs(binary))
    if not mapping:
        sys.exit(f"no ACTION_ STABS in {binary} — this build carries no debug symbols")

    modules: dict[str, list[str]] = defaultdict(list)
    for cls, obj in mapping.items():
        modules[obj.removesuffix(".o")].append(cls[len("ACTION_"):])
    modules = {m: sorted(v) for m, v in sorted(modules.items())}

    _, canonical = load_store()
    unknown = sorted(verb for members in modules.values() for verb in members
                     if verb not in canonical)
    build = plistlib.loads((app / "Contents/Info.plist").read_bytes()).get("CFBundleVersion", "?")
    return {
        "summary": {
            "build": build,
            "classes": len(mapping),
            "modules": len(modules),
            "unknown_to_store": len(unknown),
        },
        "unknown_to_store": unknown,
        "modules": modules,
        "sections": section_report(modules),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", type=Path, help="unstripped .app to re-extract from")
    parser.add_argument("--get", help="which module implements this verb")
    parser.add_argument("--module", help="verbs implemented by this module")
    parser.add_argument("--sections", action="store_true",
                        help="per module, whether it can name a section")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.app:
        artifact = build_artifact(args.app)
        json.dump(artifact, sys.stdout, indent=1)
        print()
        return 0

    if not ARTIFACT.exists():
        sys.exit(f"{ARTIFACT} not extracted yet — see this file's docstring")
    artifact = json.loads(ARTIFACT.read_text())

    if args.get:
        _, canonical = load_store()
        wanted = canonical.get(args.get, args.get)
        for module, members in artifact["modules"].items():
            if wanted in members or args.get in members:
                print(json.dumps({
                    "verb": args.get,
                    "canonical": wanted,
                    "module": f"{module}.cpp",
                    "build": artifact["summary"]["build"],
                    "siblings": len(members),
                    "section_verdict": artifact["sections"][module]["verdict"],
                    "module_section": artifact["sections"][module]["section"],
                }, indent=1))
                return 0
        print(json.dumps({"verb": args.get, "module": None,
                          "note": "no ACTION_ class in the unstripped build"}, indent=1))
        return 0

    if args.module:
        key = args.module.removesuffix(".cpp").removesuffix(".o")
        members = artifact["modules"].get(key)
        if members is None:
            sys.exit(f"no module {args.module} — have: {', '.join(artifact['modules'])}")
        print(json.dumps({"module": f"{key}.cpp", "verbs": members,
                          **artifact["sections"][key]}, indent=1))
        return 0

    if args.sections:
        print(json.dumps(artifact["sections"], indent=1))
        return 0

    if args.check:
        summary = artifact["summary"]
        members = [v for group in artifact["modules"].values() for v in group]
        if len(members) != summary["classes"]:
            sys.exit(f"action modules check FAILED: summary says {summary['classes']} classes, "
                     f"modules hold {len(members)}")
        if len(set(members)) != len(members):
            duplicated = [v for v, n in Counter(members).items() if n > 1]
            sys.exit(f"action modules check FAILED: not a partition, {duplicated} repeat")
        _, canonical = load_store()
        stale = sorted(v for v in members
                       if v not in canonical and v not in artifact["unknown_to_store"])
        if stale:
            sys.exit(f"action modules check FAILED: {len(stale)} verbs left the store "
                     f"since extraction ({', '.join(stale[:5])}) — re-extract or restore them")
        print(f"action modules check passed: {summary['classes']} classes over "
              f"{summary['modules']} modules on build {summary['build']}, "
              f"{summary['unknown_to_store']} unknown to the store")
        return 0

    print(json.dumps(artifact["summary"], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
