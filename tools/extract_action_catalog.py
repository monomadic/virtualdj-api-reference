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
# Examples are quoted in the prose: 'fadeout 10000ms 3000ms `loop`', 'loop & fadeout
# 10000ms 3000ms', 'action_deck 1 ? actionA : actionB'. The character class must admit
# chains, ternaries and backtick expressions or the multi-token examples are lost
# (2026-09-03: every `fadeout` example was, and 114 verbs with them).
# Scanned SEPARATELY per quote type. One combined pattern desynchronises on the
# catalog's nested quoting — in `'get time_min "absolute"'` the inner `"` closes
# the outer `'` span, and the scanner then resumes mid-example, silently dropping
# the real parameters that follow ("elapsed", "remain", "total"). Two passes let
# the outer example and the inner keyword both come out.
QUOTED_SINGLE = re.compile(r"'([a-z0-9_ +\-&?:`.%$#\"]{2,80})'")
QUOTED_DOUBLE = re.compile(r"\"([a-z0-9_ +\-&?:`.%$#']{2,80})\"")
# A documented PARAMETER is a bare keyword ('red', 'absolute'); values and
# expressions are examples, not vocabulary.
KEYWORD = re.compile(r"^[a-z0-9_+-]{2,40}$")
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
        quoted = list(dict.fromkeys(QUOTED_SINGLE.findall(text)
                                    + QUOTED_DOUBLE.findall(text)))
        tokens = [t for t in quoted if " " not in t and KEYWORD.match(t)]
        phrases = [t for t in quoted if " " in t]
        out[name] = {
            "text": text,
            "documented_parameters": sorted(tokens),
            "quoted_phrases": sorted(phrases),
            "multi_argument": bool(MULTI_ARG.search(text)),
            "lines": len(text.splitlines()),
        }
    return out


def binary_blob() -> str | None:
    """The binary's whole string pool as one searchable blob, or None.

    Used only to DISPROVE: a keyword the parser compares has to exist in the
    binary somewhere. A documented "parameter" that appears nowhere in it is an
    example placeholder the doc author invented (`loop_load "myloop"`,
    `os2l_scene "myscene"`), not vocabulary — no amount of probing will ever
    confirm one, so it does not belong in the worklist.

    SUBSTRING, not whole-string, and the difference matters: `stutter` and
    `unmute` are real, probe-confirmed `sampler_mode` keywords that appear only
    inside longer strings, and a whole-string test wrongly called them
    placeholders. Erring permissive keeps a real token in the worklist; erring
    strict silently deletes work.
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from extract_binary_vocabularies import Image  # noqa: PLC0415
        return "\n".join(Image(DEFAULT_APP).by_text)
    except Exception:  # noqa: BLE001 — absence of the binary is not an error here
        return None


# Tokens a focused local test measured directly, outside the arg-form capture.
# Each entry names the run that established it. Confirmations stop the worklist
# sending the next agent to re-probe settled ground; REFUTATIONS stop it sending
# them after a token that has already been shown to behave like nonsense.
LOCAL_CONFIRMED: dict[str, set[str]] = {
    # 2026-09-06, pitched fixture: elapsed/remain/total/absolute all separated
    # from two agreeing nonsense controls on the seconds/minutes/ms variants.
    "get_time_sec": {"elapsed", "remain", "total", "absolute"},
    "get_time_min": {"elapsed", "remain", "total", "absolute"},
    "get_time_ms": {"elapsed", "remain", "total", "absolute"},
    # 2026-09-06, sampler slot 1 (shipped sample), slot-first shape:
    # get_sample_info <slot> <field>. Two nonsense controls both returned ''.
    "get_sample_info": {"group", "length", "pos"},
    # 2026-09-06, a 32-beat loop saved on a disposable track. `pos` is NOT here:
    # it equals the bare/default value, so it never separated from the floor.
    # 2026-09-07, a library track with saved loops: `next` (a nonsense selector
    # errors where `next` answers) and the undocumented `len` (seconds, where
    # `length` answers in beats) — tracker "Old Appendix Keywords Re-Probed".
    "get_saved_loop": {"length", "name", "next", "len"},
    # 2026-09-07, library track on deck 1 — tracker "Documented Parameters Taken
    # Live 2026-09-07". Nonsense fields raise E_INVALIDARG; named fields answer.
    "get_loaded_song": {"album", "title", "artist", "playcount"},
    # `harmonic` answered 08A where bare, `musical` and both controls answered
    # Am (keyDisplay already musical, so `musical` stays undiscriminated).
    "get_key": {"harmonic"},
    # `'absolute' 5%` yes at +4.17% pitch where bare 5% and nonsense-selector 5% no.
    "get_pitch_zero": {"absolute"},
    # 2026-09-07, second batch — tracker "Documented Parameters Taken Live
    # 2026-09-07 (second batch)". Browser selection as found; nonsense fields
    # raise E_INVALIDARG where named fields answer.
    "get_browsed_song": {"title", "playcount", "artist"},
    # In query position `browsed_song 'rating' <n>` is an equality predicate:
    # yes at the browsed track's rating, no at another value or a nonsense field.
    "browsed_song": {"rating"},
    # `sampler_loop 'current'` answers like bare (`yes`); nonsense → E_INVALIDARG.
    "sampler_loop": {"current"},
    # `get_time 'to_lyrics'` → 0 on a track with no lyrics where an unrecognized
    # tail falls back to elapsed (44), so the tail is read even when it has
    # nothing to say.
    "get_time": {"to_lyrics"},
}

# Catalog tokens a local test showed to be the doc's own example rather than
# vocabulary, where the binary-string test cannot tell (the word exists in the
# binary for other reasons). Read like LOCAL_REFUTED: documented, tried, and
# not a keyword — but for a different reason, so they land in
# `documented_example_placeholders` rather than the refuted bucket.
LOCAL_PLACEHOLDERS: dict[str, set[str]] = {
    # 2026-09-07: get_date takes a strftime-style format string ('%Y' → 2026,
    # '%A' → Monday); a tail without a % directive is echoed verbatim, and
    # 'format' echoed itself exactly as the nonsense controls did.
    "get_date": {"format"},
    # 2026-09-07: the prose quotes an example RESULT ("such as \"2026\""); bare,
    # '2026' and a nonsense tail all returned 2026.
    "get_version": {"2026"},
    # get_text echoes its argument; 'title', 'on', 'off' are the prose's own
    # words and echoed exactly as a nonsense tail was.
    "get_text": {"title", "on", "off"},
    # "with 'featuring' stripped" describes the behavior, not a parameter; bare,
    # 'featuring' and nonsense all returned the same artist.
    "get_artist_before_feat": {"featuring"},
}
LOCAL_REFUTED: dict[str, set[str]] = {
    # 2026-09-06: `display_time` returned exactly what both nonsense controls
    # returned on every variant. The catalog only names the SETTING in prose
    # ("depending on \"display_time\""); it was never a parameter.
    "get_time_hour": {"display_time"}, "get_time_min": {"display_time"},
    "get_time_ms": {"display_time"}, "get_time_msf": {"display_time"},
    "get_time_sec": {"display_time"}, "get_time_sign": {"display_time"},
    "get_time": {"display_time"},
}


def extra_confirmations() -> dict[str, set[str]]:
    """Local-test confirmations that live outside the arg-form capture.

    A focused probe writes its own artifact — the known-position fixture proved
    `get_time cue1/loopin/loopout` against oracles the arg-form sweep has no way
    to build — and without this the cross-check keeps listing those tokens as
    unconfirmed and sends the next agent to re-probe settled ground.
    """
    out: dict[str, set[str]] = {k: set(v) for k, v in LOCAL_CONFIRMED.items()}
    positions = Path("tests/get-time-positions.json")
    if positions.exists():
        art = json.load(open(positions))
        confirmed = {tail for tail, rec in art["summary"]["targets"].items()
                     if rec["verdict"].startswith("reads_its_position")}
        # The floors are confirmed by the same run: they are what the nonsense
        # controls fall back to, measured in every phase.
        confirmed |= {"elapsed", "short"}
        if confirmed:
            out.setdefault("get_time", set()).update(confirmed)
    return out


def cross_check(entries: dict[str, dict]) -> dict:
    """Where the catalog and the probe agree, and where each is alone."""
    if not ARG_FORMS.exists():
        return {}
    probed = json.load(open(ARG_FORMS))["verbs"]
    attested_path = Path("tests/attested-tails.json")
    attested = json.load(open(attested_path))["tails"] if attested_path.exists() else {}
    blob = binary_blob()
    extra = extra_confirmations()
    both, catalog_only, probe_only = {}, {}, {}
    three_ways, placeholders, refuted = {}, {}, {}
    for verb, rec in entries.items():
        documented = set(rec["documented_parameters"])
        # The catalog quotes whole examples, so the verb's own name comes out of
        # the tokenizer as if it were one of its parameters.
        documented.discard(verb)
        gone = documented & LOCAL_REFUTED.get(verb, set())
        if gone:
            refuted[verb] = sorted(gone)
            documented -= gone
        found = {t[0] for t in probed.get(verb, {}).get("recognized_tokens", []) if len(t) == 1}
        found |= extra.get(verb, set())
        # A token any other source vouches for is never a placeholder, whatever
        # the binary search says.
        vouched = found | set(attested.get(verb, {}))
        known_placeholders = documented & LOCAL_PLACEHOLDERS.get(verb, set())
        if known_placeholders:
            placeholders[verb] = sorted(known_placeholders)
            documented -= known_placeholders
        if blob is not None:
            # A signed token (`browser_sort "+bpm"`) is a real key wearing a
            # direction prefix; the binary stores the bare field, so strip the
            # sign before asking. Without this the sort keys were called
            # placeholders, which is the one direction of error that deletes
            # real work.
            absent = {t for t in documented - vouched
                      if t.lstrip("+-") not in blob}
            if absent:
                placeholders[verb] = sorted(set(placeholders.get(verb, [])) | absent)
                documented -= absent
        if not documented and not found:
            continue
        if documented & found:
            both[verb] = sorted(documented & found)
        if documented - found:
            catalog_only[verb] = sorted(documented - found)
        if found - documented:
            probe_only[verb] = sorted(found - documented)
        # Attested = written by Atomix in a shipped script. A token carried by
        # all three sources is as settled as this project can make it.
        written = set(attested.get(verb, {}))
        if documented & found & written:
            three_ways[verb] = sorted(documented & found & written)
    return {
        "confirmed_by_both": both,
        "documented_but_not_probe_confirmed": catalog_only,
        "probe_confirmed_but_undocumented": probe_only,
        "confirmed_by_all_three": three_ways,
        # Not a worklist: quoted names the binary never carries as strings, so
        # they are the doc's own examples rather than vocabulary to confirm.
        "documented_example_placeholders": placeholders,
        # Also not a worklist: tokens a local test measured behaving exactly like
        # its nonsense controls. Documented, tried, and not vocabulary.
        "documented_but_locally_refuted": refuted,
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
