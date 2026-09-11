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
    # Am (keyDisplay already musical, so `musical` was undiscriminated there);
    # 2026-09-07, with keyDisplay flipped to Harmonic, bare and a nonsense tail
    # both returned 02A where `musical` returned Ebm. Setting restored. One
    # entry, not two: a duplicate dict key silently dropped `harmonic`.
    "get_key": {"harmonic", "musical"},
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
    # 2026-09-07, deck2_playing fixture — tracker "Documented Parameters Taken
    # Live 2026-09-07 (fixtures)". current/next answer differently (volume 1 vs
    # 0.74, hasbeats yes vs no); a nonsense selector or field returns ''.
    "get_song_event": {"current", "next", "volume", "hasbeats", "remaining"},
    # 2026-09-07, query-position pass with no fixture at all — `param_cast` is a
    # pipeline verb, so a chained expression IS the state. Input 12.7 through
    # `get_var … & param_cast <type>`: integer 13 vs int_trunc 12 (the
    # documented rounding/truncation split), frac 0.7, 000 -> 013,
    # percentage 1270%, ms 13ms, beats 12.7bt, boolean yes (0 -> no), float and
    # text 12.7; `text 5` truncated 'Chapter & Verse' to 'Chapt' and `text 3`
    # to 'Cha'. Bare and both nonsense types raise E_INVALIDARG.
    # 2026-09-08: `absolute` and `relative` are accepted where a nonsense type
    # raises E_INVALIDARG, and they answer in a class of their own — '' where
    # every cast type returns S_FALSE — which is what the doc describes (they
    # change how the value is applied, they do not cast it). Acceptance is the
    # evidence here because param_cast REJECTS what it does not know, so its
    # vocabulary is directly enumerable: `int` and `percent` are accepted too,
    # `inte`/`perc`/`intx` are not (exact match, not prefix), and the digit
    # format generalises past the documented `000` to `0`, `00`, `0000`, `00.0`.
    "param_cast": {"integer", "int_trunc", "frac", "float", "percentage", "ms",
                   "boolean", "beats", "text", "000", "absolute", "relative"},
    # 2026-09-07: with the filter knob at 0.75, `name` returned MOBIUS TRI where
    # bare and both controls returned '> 50%'; at the centre `clean` returned
    # OFF where bare and both controls returned the name. Each token separates
    # in the knob position where it can.
    "filter_label": {"name", "clean"},
    # 2026-09-07, execute + readback with the zone restored: each token made
    # exactly its own zone active, junk changed nothing. automix/sidelist/
    # sampler additionally activate `sideview` — they are panes inside it.
    "browser_window": {"folders", "songs", "sideview", "automix", "sidelist",
                       "sampler"},
    # 2026-09-07, query position: each answers where bare and two agreeing
    # nonsense controls do not (E_INVALIDARG), or answers differently from both.
    "auto_cue": {"on", "off"},
    "cross_assign": {"left"},
    "prelisten_output": {"auto"},
    "search_options": {"composer"},
    # `sidelist` is NOT here: it failed exactly as the controls did, and panel
    # names are skin-dependent, so that is a fact about the loaded skin.
    "show_splitpanel": {"sideview"},
    # 2026-09-08, query position, no fixture — tracker "Documented Parameters
    # Taken Live 2026-09-08". `browser_sort`/`sideview_sort` answer `no` for a
    # real sort field and `yes` for anything else, so in query position they are
    # a membership oracle for the sort-field enumeration: 36 names separate from
    # five agreeing nonsense controls AND from plausible near-misses
    # (`play_count`, `date`, `added`, `random`, `folder`, `user1`,
    # `linkedvideo`). One leading `+`/`-` is accepted, `++`/`*`/`~` is not, and
    # matching is case-insensitive. Both verbs accept exactly the same set.
    "browser_sort": {"+bpm", "-bpm", "artist", "lastplay"},
    "sideview_sort": {"artist", "lastplay"},
    # 2026-09-08, slip engaged on deck 1 with the shadow playhead past 1 minute:
    # bare 65387 ms, `min` 1, `sec` 5, `msec` 437, where both nonsense controls
    # returned the bare value. min*60000+sec*1000+msec reproduces bare to within
    # the ~12 ms the shadow clock drifts between two queries, which is the check
    # that clinches it — the value moves, so three agreeing runs were taken.
    # `get_slip_time` raises E_FAIL when slip is not engaged.
    "get_slip_time": {"min", "sec", "msec"},
    # 2026-09-08: with a master effect on and no deck effect, `master` answered
    # yes where bare, `deck` and both controls answered no. `deck` is in
    # LOCAL_DEFAULT_ALIASES — bare IS the deck scope, so nothing can separate it.
    "effects_used": {"master"},
    # 2026-09-08, execute + readback on the fixture track (120 BPM): `pitch 130
    # bpm` landed the deck on 130 BPM and `pitch 100 bpm` on 100, where
    # `pitch 130 zzqqx`, `pitch 130 wubfar` AND the bare `pitch 130` all
    # returned false and left the deck at 120/0.5. A two-token form whose second
    # token is required, not optional.
    "pitch": {"bpm"},
    # 2026-09-08: `loaded_song 'rating' <n>` is an equality predicate like
    # `browsed_song` — yes at the loaded track's rating (0, read independently
    # through get_loaded_song), no at every other value and no for two nonsense
    # fields at any value.
    "loaded_song": {"rating"},
    # 2026-09-08: the catalog's `stems` is prose (LOCAL_PLACEHOLDERS); the real
    # vocabulary is in the sentence the tokenizer could not see, "Accepted stem
    # names are Vocal, HiHat, Bass, Instru, Kick". All five confirmed: in query
    # position instru/kick/hihat/bass answered no where bare, `vocal` and four
    # nonsense controls answered yes, and executing a stem's own token toggled
    # exactly that stem (kick no->yes, vocal yes->no) with the arm restored
    # after. The documented `+` combinator holds — `kick+bass` toggles both,
    # case-insensitively — but takes NO surrounding space (`kick + bass` is a
    # no-op), an unknown member is dropped while known ones still apply
    # (`kick+zzqqx` toggles kick), and in query position `+` is a conjunction
    # (`vocal+kick` no with only vocal armed, `vocal+vocal` yes).
    "effect_arm_stem": {"vocal", "instru", "kick", "hihat", "bass"},
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
    # 2026-09-07, fx_slot_1_on fixture (Phaser in slot 1): the NAME argument is
    # confirmed — effect_active 'Phaser' yes / 'flanger' no / nonsense no, and
    # effect_select [slot] 'Phaser' yes / 'echo' no / nonsense no, likewise
    # effect_select_multi. The quoted names are members of the FX catalog used
    # as examples, not keywords; confirm a specific one by loading it.
    "effect_active": {"flanger"},
    "effect_select": {"echo"},
    "effect_select_multi": {"echo"},
    # 2026-09-07: `artist` is the doc example's argument to get_browsed_song
    # ("get_browsed_song 'artist' & param_cast 'text' 5"), not a cast type —
    # it raises E_INVALIDARG exactly as the nonsense types do.
    "param_cast": {"artist"},
    # `param_equal` is a plain string compare: 'zzqqx' equals 'zzqqx' and
    # 'audio' does not equal 'zzqqx', so audio/string/type are the doc
    # example's operands rather than vocabulary. The documented backtick shape
    # does hold: param_equal `get_browsed_song 'type'` 'audio' -> yes, 'video' -> no.
    "param_equal": {"audio", "string", "type"},
    # 2026-09-07: `siren` is the doc's example sample FILE ("sampler_volume
    # 'siren'" sets the volume of siren.vdjsample), not vocabulary — it returns
    # 0 exactly as a nonsense name does. The name form itself is confirmed with
    # a sample that is actually loaded: `sampler_volume 'Dystopia Breaks'` -> 1.
    "sampler_volume": {"siren"},
    "sampler_pad_volume": {"siren"},
    # 2026-09-08: "if no cue point is set, or if 'cue', 'cue_stop' or 'cue_play'
    # is pressed" names OTHER BUTTONS whose press makes hot_cue set a cue — it
    # is not hot_cue's own tail. Measured on the fixture track: all three set
    # cue 1 at the playhead and left the deck paused, exactly as both nonsense
    # controls did.
    "hot_cue": {"cue", "cue_play", "cue_stop"},
    # 2026-09-08: "to be used with \"stems\" as slot for effect_ actions" quotes
    # the SLOT name, not a stem name. The real vocabulary is the five stem names
    # in LOCAL_CONFIRMED; `stems` answers exactly as four nonsense controls do.
    "effect_arm_stem": {"stems"},
}

# Tokens a local test showed to be indistinguishable from the bare form because
# they NAME THE DEFAULT the verb already uses. Real vocabulary, documented, and
# permanently unconfirmable by value comparison: no state can separate a tail
# that selects what the verb does anyway. Recording them stops the worklist
# sending the next agent after a separation that cannot exist.
LOCAL_DEFAULT_ALIASES: dict[str, set[str]] = {
    # 2026-09-08: bare `effects_used` IS the deck scope — it answered no with a
    # master effect on and yes with a deck effect on, tracking `deck` in both.
    # `master` is the token that separates, and it is confirmed.
    "effects_used": {"deck"},
    # 2026-09-06, re-measured 2026-09-07: bare `get_saved_loop` returns the
    # loop-in position and so do both nonsense controls, so `pos` names the
    # floor and no fixture can separate it. It is real vocabulary, not a
    # placeholder: `name`, `length` and the undocumented `len` each separate
    # from that fallback, which is what makes the fallback visible.
    "get_saved_loop": {"pos"},
    # 2026-09-08: this machine runs the internal mixer, so bare, `internal` and
    # both nonsense controls answer yes; `external` answers no and is confirmed.
    # Separating `internal` would mean switching the audio config to an external
    # mixer, which is the user's setup, not a fixture.
    "mixermode": {"internal"},
    # 2026-09-07, tests/bpm-transition-forms.json: bare, both nonsense controls
    # and `target_original` all land the pair on 120 — the default target — where
    # `source_original` lands on 100 and `target_current` on 132. Retested with
    # smart_play off, same default.
    "auto_bpm_transition": {"target_original"},
}
# Documented tokens a live test TRIED and could not separate from its nonsense
# controls, because the state on hand made every form read the same. Still on
# the worklist — undiscriminated is not refuted — but recorded here so the next
# agent is sent to build the named state rather than to re-run the same probe.
# Source: tracker, "Documented Parameters Taken Live 2026-09-07".
LOCAL_UNDISCRIMINATED: dict[str, dict[str, str]] = {
    "get_key": {"musical": "bare, musical and both controls all `Am`: keyDisplay was already musical"},
    "get_saved_loop": {"pos": "what an unrecognized tail falls back to, so nothing separates it"},
    "get_limiter": {t: "everything `0` with nothing playing" for t in ("master", "booth", "headphones")},
    "get_time_sign": {t: "`1` at 43 ms and 14,812 ms for every tail; a negative sign needs a state not built"
                      for t in ("elapsed", "remain", "total")},
    "get_time_hour": {t: "`0` throughout on a 2:26 track; needs a track longer than an hour"
                      for t in ("elapsed", "remain")},
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
    transition = Path("tests/bpm-transition-forms.json")
    if transition.exists():
        forms = json.load(open(transition))["summary"]["forms"]
        # `recognized-…` only: a parameter naming the DEFAULT landing lands
        # where an ignored tail lands, so this run cannot confirm it and must
        # not claim to. It stays on the worklist, correctly.
        confirmed = {f for f, rec in forms.items()
                     if rec["verdict"].startswith("recognized")}
        if confirmed:
            out.setdefault("auto_bpm_transition", set()).update(confirmed)
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
    three_ways, placeholders, refuted, defaults, undiscriminated = {}, {}, {}, {}, {}
    for verb, rec in entries.items():
        documented = set(rec["documented_parameters"])
        # The catalog quotes whole examples, so the verb's own name comes out of
        # the tokenizer as if it were one of its parameters.
        documented.discard(verb)
        tried = {t: n for t, n in LOCAL_UNDISCRIMINATED.get(verb, {}).items() if t in documented}
        if tried:
            undiscriminated[verb] = tried
        gone = documented & LOCAL_REFUTED.get(verb, set())
        if gone:
            refuted[verb] = sorted(gone)
            documented -= gone
        default = documented & LOCAL_DEFAULT_ALIASES.get(verb, set())
        if default:
            defaults[verb] = sorted(default)
            documented -= default
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
        # Also not a worklist: real vocabulary that names the default the verb
        # already uses, so no state can separate it from the bare form.
        "documented_but_names_the_default": defaults,
        # A worklist entry with its reason attached: tried live, every form read
        # the same because of the state on hand. token -> what the state lacked.
        "documented_but_undiscriminated_here": undiscriminated,
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
        # The action count alone cannot see the tables above moving. Recording
        # a token in LOCAL_CONFIRMED or LOCAL_DEFAULT_ALIASES, or re-probing an
        # argument form, changes which verbs the cross-check calls unconfirmed
        # while every description stays identical — so the artifact silently
        # keeps sending the next agent to re-probe settled ground. Recompute it.
        fresh = cross_check(live)
        stored = data.get("cross_check", {})
        drift = [f"{k}: {len(stored.get(k, {}))} -> {len(v)} verbs"
                 for k, v in sorted(fresh.items()) if stored.get(k) != v]
        if drift:
            sys.exit("action catalog check FAILED: the cross-check no longer matches the "
                     "artifact (" + "; ".join(drift) + ") — re-extract with "
                     "`python3 tools/extract_action_catalog.py > tests/action-catalog.json`")
        print(f"action catalog check passed: {summary['actions']} descriptions, "
              f"{summary['with_parameters']} documenting parameters, "
              f"{summary['multi_argument']} promising more than one argument, "
              f"cross-check reproduced")
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
