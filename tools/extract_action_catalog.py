#!/usr/bin/env python3
"""Extract the Button Editor's own action descriptions, and the parameters in them.

`Resources/languages.zip` -> `English.xml` -> `<Actions>` is the source the
Button Editor shows and the same prose the official verbs appendix publishes at
virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html — checked
verbatim against that page for `auto_bpm_transition`. So this is an OFFICIAL
source available offline, and until now the repo read this file only for verb
NAMES, throwing away every description.

The prose carries what no probe can recover: what a parameter MEANS.

    auto_bpm_transition   "When using parameter 'source_original',
                           'target_original' or 'target_current' you can force
                           which bpm it will transition to"
    get_song_event        "The first parameter is "current" or "next" ...
                           The second parameter can be "hasbeats", "volume", ..."

Quoted words inside a description are extracted as documented parameters, which
gives an independent check on the probe artifacts: a token that separates from
nonsense AND appears quoted in the catalog is settled from two directions, and
the difference in either direction is a worklist.

    python3 tools/extract_action_catalog.py > tests/action-catalog.json
    python3 tools/extract_action_catalog.py --get get_song_event
    python3 tools/extract_action_catalog.py --cross-check
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from zipfile import ZipFile

DEFAULT_APP = Path("/Applications/VirtualDJ.app")
ARTIFACT = Path("tests/action-catalog.json")
ARG_FORMS = Path("tests/verb-arg-forms.json")
LANGUAGE = "English.xml"

ACTION_BLOCK = re.compile(r"<Actions>(.*?)</Actions>", re.S)
ACTION_ENTRY = re.compile(r"<([a-z0-9_]+)>(.*?)</\1>", re.S)
# 'single' or "double" quoted words — how the catalog spells every parameter.
QUOTED = re.compile(r"['\"]([a-z0-9_ +-]{2,40})['\"]")
# Prose that promises more than one positional argument.
MULTI_ARG = re.compile(r"\b(second|third|two|first and second) parameter\b", re.I)


def unescape(text: str) -> str:
    for entity, char in (("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'),
                         ("&apos;", "'"), ("&amp;", "&")):
        text = text.replace(entity, char)
    return text.strip()


def catalog(app: Path, language: str) -> dict[str, dict]:
    with ZipFile(app / "Contents/Resources/languages.zip") as bundle:
        xml = bundle.read(language).decode("utf-8", errors="replace")
    block = ACTION_BLOCK.search(xml)
    if not block:
        sys.exit(f"no <Actions> block in {language}")
    out = {}
    for name, body in ACTION_ENTRY.findall(block.group(1)):
        text = unescape(body)
        if not text:
            continue
        tokens = [t for t in dict.fromkeys(QUOTED.findall(text)) if " " not in t]
        phrases = [t for t in dict.fromkeys(QUOTED.findall(text)) if " " in t]
        out[name] = {
            "text": text,
            "documented_parameters": sorted(tokens),
            "quoted_phrases": sorted(phrases),
            "multi_argument": bool(MULTI_ARG.search(text)),
            "lines": len(text.splitlines()),
        }
    return out


def cross_check(entries: dict[str, dict]) -> dict:
    """Where the catalog and the probe agree, and where each is alone."""
    if not ARG_FORMS.exists():
        return {}
    probed = json.load(open(ARG_FORMS))["verbs"]
    both, catalog_only, probe_only = {}, {}, {}
    for verb, rec in entries.items():
        documented = set(rec["documented_parameters"])
        found = {t[0] for t in probed.get(verb, {}).get("recognized_tokens", []) if len(t) == 1}
        if not documented and not found:
            continue
        if documented & found:
            both[verb] = sorted(documented & found)
        if documented - found:
            catalog_only[verb] = sorted(documented - found)
        if found - documented:
            probe_only[verb] = sorted(found - documented)
    return {
        "confirmed_by_both": both,
        "documented_but_not_probe_confirmed": catalog_only,
        "probe_confirmed_but_undocumented": probe_only,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", type=Path, default=DEFAULT_APP)
    parser.add_argument("--language", default=LANGUAGE)
    parser.add_argument("--get", metavar="NAME")
    parser.add_argument("--cross-check", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.check:
        if not ARTIFACT.exists():
            print("action catalog check skipped: tests/action-catalog.json not extracted yet")
            return 0
        data = json.load(open(ARTIFACT))
        summary = data["summary"]
        live = catalog(args.app, args.language)
        if len(live) != summary["actions"]:
            sys.exit(f"action catalog check FAILED: artifact has {summary['actions']} actions, "
                     f"the installed build has {len(live)} — re-extract")
        print(f"action catalog check passed: {summary['actions']} descriptions, "
              f"{summary['with_parameters']} documenting parameters, "
              f"{summary['multi_argument']} promising more than one argument")
        return 0

    entries = catalog(args.app, args.language)

    if args.get:
        record = entries.get(args.get)
        if record is None:
            print(json.dumps({"name": args.get, "documented": False}, indent=1))
            return 0
        print(json.dumps({"name": args.get, **record}, indent=1))
        return 0

    checked = cross_check(entries)
    if args.cross_check:
        print(json.dumps(checked, indent=1))
        return 0

    json.dump({
        "summary": {
            "actions": len(entries),
            "with_parameters": sum(1 for r in entries.values() if r["documented_parameters"]),
            "multi_argument": sum(1 for r in entries.values() if r["multi_argument"]),
            "language": args.language,
            "cross_check_counts": {k: len(v) for k, v in checked.items()},
        },
        "cross_check": checked,
        "actions": entries,
    }, sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
