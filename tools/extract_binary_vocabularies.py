#!/usr/bin/env python3
"""Recover argument vocabularies — GROUPS of keywords — from the app binary.

Every other argument source in this repo is per verb: the catalog documents
parameters on one verb, the corpus attests a tail on one verb, and the
contracts extractor lists literals referenced from one verb's own methods
(`keyword_candidates`). But a vocabulary is usually shared. Stem names are
matched by a helper that `stem_color`, `stems_split` and `effect_stems` all
call; colour names live in one table the whole app reads. Those helpers are
invisible to per-verb analysis, which is why 35 of the corpus's 114 novel tails
were in the binary yet outside their verb's code.

Three signals, weakest to strongest, and each one is recorded separately:

1. **run** — the keywords are adjacent in the string pool. Pools cluster by
   compilation unit, so neighbours are *related*, but adjacency is not a
   structure and a run can straddle two enumerations.
2. **code region** — one stretch of `__text` references several members
   (ADRP+ADD pairs). That is a comparison function or a switch walking the
   enumeration; every other string it references is a candidate member. This
   is the signal that finds hidden options: the function knows the words the
   docs never mention.
3. **pointer table** — a `const char *[]` in `__DATA_CONST` whose entries
   point at the members, in order. The genuine serialised structure, when it
   exists. Its full entry list is the enumeration, nothing more or less.

Per group the artifact records the members from each signal, which verbs are
known to take any of them (attested tails, catalog parameters, keyword
candidates), and the members that no per-verb source knows: the probe queue.

Evidence tier: 2, structural. A member is a *lead*. Verbs silently ignore
unknown words, so confirming one needs a fixture where the forms would differ
(Evidence Standards, and the arg-forms prober's nonsense controls).

    python3 tools/extract_binary_vocabularies.py > tests/binary-vocabularies.json
    python3 tools/extract_binary_vocabularies.py --get stems
    python3 tools/extract_binary_vocabularies.py --verb stem_color
    python3 tools/extract_binary_vocabularies.py --tails      # where each attested tail lives
"""

from __future__ import annotations

import argparse
import json
import plistlib
import re
import struct
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_action_contracts import sections, slice_offset  # noqa: E402

DEFAULT_APP = Path("/Applications/VirtualDJ.app")
ARTIFACT = Path("tests/binary-vocabularies.json")
TAILS = Path("tests/attested-tails.json")
CONTRACTS = Path("tests/action-contracts.json")
CATALOG = Path("tests/action-catalog.json")
VERB_TABLE = Path("tests/verb-table.json")

# A keyword the parser could match: lowercase identifier-ish, short. UI labels
# ("Kick (Drums)"), format strings and paths end a run.
KEYWORD = re.compile(r"^[a-z][a-z0-9_]{1,31}$")
# Pointer-table entries may carry spaces and `+` ("loop roll", "stems+fx"): a
# table is already structure, so its entries need only look like values.
TABLE_ENTRY = re.compile(r"^[a-z][a-z0-9_+ .-]{0,31}$")
# Words that are keywords by shape but end a run because they are prose or
# generic — the colour table sits right after the month names.
NOISE = {"true", "false", "yes", "no", "on", "off", "and", "or", "not", "the",
         "null", "error", "warning", "ok", "cancel"}

# Named seeds. Two or three members each; the binary supplies the rest. A seed
# names the group, it does not fix its membership — a member that the binary
# does not corroborate is reported as `seed_unconfirmed`.
SEEDS = {
    # name: (seed words, verbs known or suspected to take the enumeration)
    "stems": (["vocal", "hihat", "instru", "kick"],
              ["stem_color", "stems_split", "effect_stems", "stem_pad", "stem_volume",
               "mute_stem", "only_stem", "effect_stems_color"]),
    "stem_modes": (["acapella", "instrumental", "isolate"], ["stem_pad", "stems_split"]),
    "colors": (["cyan", "magenta", "orange", "yellow", "darkred"],
               ["color", "get_loaded_song_color", "browsed_file_color", "get_browsed_color",
                "cue_color", "loop_color", "sampler_color", "pad_color"]),
    "effect_gui": (["audioonlyvisualisation", "colorfx", "releasefx", "melovocal", "mixfx"],
                   ["effect_show_gui", "effect_dock_gui"]),
    "sideview": (["sidelist", "automix", "karaoke", "remixes"], ["sideview", "browser_window"]),
    "settings_pages": (["audio", "skins", "controllers", "performance", "automation"],
                       ["settings"]),
    "browser_roots": (["itunes", "rekordbox", "traktor", "history", "geniusdj"],
                      ["browser_gotofolder", "browser_window", "browser_folder"]),
    "browser_view": (["showmusic", "showvideo", "showkaraoke"], ["view_options"]),
    "loop_menu": (["quantized", "notquantized", "loopsize"], ["dump"]),
    "bpm_reference": (["absolute", "ghost"], ["get_bpm"]),
    "time_modes": (["elapsed", "remain", "total", "loopin"], ["display_time", "get_time"]),
    "eq_modes": (["frequency", "stems"], ["eq_mode"]),
    "audio_channels": (["master", "headphones", "booth", "auxin", "deckfxsend"],
                       ["effect_arm_deck", "effect_fxsendreturndeck", "effect_disable_all",
                        "sampler_rec", "record"]),
    "song_fields": (["artist", "title", "remix", "album", "composer"],
                    ["get_karaoke_background_song", "get_next_karaoke_song", "browser_sort"]),
    "pad_pages": (["hotcues", "slicer", "keycue", "cueloop", "scratchbank"], ["pad_page"]),
    "waveform_options": (["upsidedown", "opposite", "mirror", "rhythm"], []),
    "search_folder": (["dialog", "clear", "focus"], ["search_folder"]),
}
# Words too generic to relate a verb to a group on their own.
GENERIC = {"all", "deck", "active", "default", "none", "master", "sampler", "video",
           "audio", "key", "title", "name", "file", "folder"}
# An auto-seeded group bigger than this is a compilation unit, not an enumeration.
MAX_AUTO_MEMBERS = 40
# A named group that code regions push past this keeps its tables and drops
# the regions: `artist`/`title` are compared by every tag parser in the app.
MAX_GROUP_MEMBERS = 60
# Code-region clustering: xrefs to members closer than this are one function.
REGION_GAP = 0x600
REGION_PAD = 0x100
MAX_REGIONS = 6
MAX_TABLES = 4
# A switch over an enumeration references mostly that enumeration. A region
# referencing far more strings than it hits is a skin builder or a dispatcher.
MAX_REGION_REFS = 48
# The verb table is 1,032 pointers; no argument enumeration is anywhere near.
MAX_TABLE_ENTRIES = 64
POINTER_STRIDES = (8, 16, 24, 32)


class Image:
    def __init__(self, app: Path):
        path = app / "Contents/MacOS/VirtualDJ"
        self.data = data = path.read_bytes()
        self.base = base = slice_offset(data)
        self.secs = secs = sections(data, base)
        self.text = next(s for s in secs if s[0] == "__TEXT" and s[1] == "__text")
        self.cstr = next(s for s in secs if s[1] == "__cstring")
        blob = data[base + self.cstr[4]: base + self.cstr[4] + self.cstr[3]]
        self.strings: dict[int, str] = {}      # vm -> string
        self.by_text: dict[str, list[int]] = defaultdict(list)
        self.order: list[int] = []
        pos = 0
        while pos < len(blob):
            end = blob.find(b"\0", pos)
            if end < 0:
                break
            if end > pos:
                try:
                    s = blob[pos:end].decode()
                except UnicodeDecodeError:
                    s = None
                if s is not None:
                    vm = self.cstr[2] + pos
                    self.strings[vm] = s
                    self.by_text[s].append(vm)
                    self.order.append(vm)
            pos = end + 1
        self.index = {vm: i for i, vm in enumerate(self.order)}
        self._xrefs = None
        self._ptrs = None

    def file_offset(self, vm: int) -> int:
        return vm - self.cstr[2] + self.cstr[4]

    # -- signal 1: string-pool runs ------------------------------------------
    def run(self, vm: int) -> list[int]:
        i = self.index[vm]
        lo = i
        while lo - 1 >= 0 and self.keyword(self.strings[self.order[lo - 1]]):
            lo -= 1
        hi = i
        while hi + 1 < len(self.order) and self.keyword(self.strings[self.order[hi + 1]]):
            hi += 1
        return self.order[lo:hi + 1]

    @staticmethod
    def keyword(s: str) -> bool:
        return bool(KEYWORD.match(s)) and s not in NOISE

    # -- signal 2: code references (ADRP+ADD) -------------------------------
    @property
    def xrefs(self) -> dict[int, list[int]]:
        """string vm -> [pc of referencing ADRP]"""
        if self._xrefs is not None:
            return self._xrefs
        seg, name, vaddr, size, fileoff = self.text
        raw = self.data[self.base + fileoff: self.base + fileoff + (size & ~3)]
        w = np.frombuffer(raw, dtype="<u4")
        pcs = vaddr + np.arange(len(w), dtype=np.int64) * 4
        is_adrp = (w & 0x9F000000) == 0x90000000
        immlo = (w >> 29) & 3
        immhi = (w >> 5) & 0x7FFFF
        imm = ((immhi << 2) | immlo).astype(np.int64)
        imm = np.where(imm & (1 << 20), imm - (1 << 21), imm)
        page = (pcs & ~0xFFF) + (imm << 12)
        rd = w & 0x1F
        out: dict[int, list[int]] = defaultdict(list)
        lo, hi = self.cstr[2], self.cstr[2] + self.cstr[3]
        for skip in (1, 2):
            nxt = np.roll(w, -skip)
            is_add = (nxt & 0xFF800000) == 0x91000000
            rn = (nxt >> 5) & 0x1F
            ok = is_adrp & is_add & (rn == rd)
            ok[-skip:] = False
            target = page + ((nxt >> 10) & 0xFFF).astype(np.int64)
            hit = ok & (target >= lo) & (target < hi)
            for pc, t in zip(pcs[hit].tolist(), target[hit].tolist()):
                if t in self.strings:
                    out[t].append(pc)
        self._xrefs = out
        return out

    def regions(self, members: list[int]) -> list[dict]:
        """Clusters of code that reference >= 2 distinct members."""
        pcs = sorted({pc: vm for vm in members for pc in self.xrefs.get(vm, [])}.items())
        clusters, cur = [], []
        for pc, vm in pcs:
            if cur and pc - cur[-1][0] > REGION_GAP:
                clusters.append(cur)
                cur = []
            cur.append((pc, vm))
        if cur:
            clusters.append(cur)
        by_pc = defaultdict(set)
        for vm, refs in self.xrefs.items():
            for pc in refs:
                by_pc[pc].add(vm)
        out = []
        for c in clusters:
            found = {vm for _, vm in c}
            if len(found) < 2:
                continue
            lo, hi = c[0][0] - REGION_PAD, c[-1][0] + REGION_PAD
            referenced = sorted({vm for pc in by_pc if lo <= pc <= hi for vm in by_pc[pc]})
            words = [self.strings[vm] for vm in referenced if self.keyword(self.strings[vm])]
            if len(set(words)) > MAX_REGION_REFS:
                continue
            out.append({"text_range": [hex(c[0][0]), hex(c[-1][0])],
                        "members_hit": sorted({self.strings[vm] for vm in found}),
                        "referenced": sorted(set(words))})
        # `automix` and `sidelist` are compared in twenty functions; keep the
        # regions that hit a set of members no other region strictly contains.
        out.sort(key=lambda r: (-len(r["members_hit"]), r["text_range"]))
        kept = []
        for r in out:
            hit = set(r["members_hit"])
            if any(hit < set(k["members_hit"]) for k in kept):
                continue
            kept.append(r)
        return kept[:MAX_REGIONS]

    # -- signal 3: pointer tables ---------------------------------------------
    @property
    def ptrs(self) -> tuple[np.ndarray, np.ndarray]:
        if self._ptrs is None:
            vals, addrs = [], []
            for s in self.secs:
                if s[0] in ("__DATA_CONST", "__DATA") and s[1] in ("__const", "__data"):
                    raw = self.data[self.base + s[4]: self.base + s[4] + (s[3] & ~7)]
                    v = np.frombuffer(raw, dtype="<u8") & 0xFFFFFFFFFF
                    vals.append(v)
                    addrs.append(s[2] + np.arange(len(v), dtype=np.int64) * 8)
            self._ptrs = (np.concatenate(vals), np.concatenate(addrs))
        return self._ptrs

    def tables(self, members: list[int]) -> list[dict]:
        vals, addrs = self.ptrs
        mset = set(members)
        seen, out = set(), []
        hits = np.nonzero(np.isin(vals, np.array(members, dtype=np.uint64)))[0]
        for i in hits.tolist():
            best = None
            for stride in POINTER_STRIDES:
                step = stride // 8
                lo = i
                while lo - step >= 0 and int(vals[lo - step]) in self.strings:
                    lo -= step
                hi = i
                while hi + step < len(vals) and int(vals[hi + step]) in self.strings:
                    hi += step
                entries = [int(vals[k]) for k in range(lo, hi + 1, step)]
                got = sum(1 for e in entries if e in mset)
                if len(entries) > MAX_TABLE_ENTRIES:
                    continue
                if got >= 2 and (best is None or len(entries) > len(best[1])):
                    best = (stride, entries, lo)
            if best is None:
                continue
            stride, entries, lo = best
            key = (int(addrs[lo]), stride)
            if key in seen:
                continue
            seen.add(key)
            names = [self.strings[e] for e in entries]
            # A tag-format map (`WM/AlbumArtist` -> `album_artist`) or the ID3
            # genre list is a table, but not an enumeration of script words.
            if sum(1 for n in names if TABLE_ENTRY.match(n)) * 10 < len(names) * 6:
                continue
            out.append({"address": hex(int(addrs[lo])), "stride": stride,
                        "members_hit": sum(1 for e in entries if e in mset),
                        "entries": names})
        out.sort(key=lambda t: (-t["members_hit"], t["address"]))
        return out[:MAX_TABLES]


def load_sources():
    verbs = set(json.load(open(VERB_TABLE))["verbs"]) if VERB_TABLE.exists() else set()
    tails = json.load(open(TAILS)) if TAILS.exists() else {"tails": {}}
    contracts = json.load(open(CONTRACTS))["verbs"] if CONTRACTS.exists() else {}
    catalog = json.load(open(CATALOG))["actions"] if CATALOG.exists() else {}
    known: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for verb, toks in tails["tails"].items():
        known[verb]["attested"] |= set(toks)
    for verb, rec in contracts.items():
        known[verb]["keyword_candidates"] |= set(rec.get("keyword_candidates") or [])
        for strs in (rec.get("method_strings") or {}).values():
            known[verb]["method_strings"] |= set(strs)
    for verb, rec in catalog.items():
        known[verb]["catalog"] |= set(rec.get("documented_parameters") or [])
    return tails, known, verbs


def locate_tails(img: Image, tails: dict, known) -> dict:
    """Where each attested tail lives: absent / in_method / shared."""
    out = {}
    for verb, toks in sorted(tails["tails"].items()):
        rec = {}
        for tok in sorted(toks):
            vms = img.by_text.get(tok, [])
            if not vms:
                rec[tok] = {"where": "absent"}
            elif tok in known[verb]["method_strings"]:
                rec[tok] = {"where": "in_method"}
            else:
                rec[tok] = {"where": "shared", "offsets": [img.file_offset(v) for v in vms],
                            "run": [img.strings[v] for v in img.run(vms[0])][:24]}
        out[verb] = rec
    return out


def build_group(img: Image, name: str, seed: list[str], known, verbs: set[str],
                verbs_hint=()) -> dict | None:
    seed_vms = [vm for s in seed for vm in img.by_text.get(s, [])]
    if not seed_vms:
        return None
    # Signal 3 first: a table holding two seeds fixes the enumeration.
    # Two seeds fix a short enumeration; a longer seed list must hit three, or
    # the settings-page table (which holds `karaoke` and `automix`) joins the
    # sideview group through shared words.
    need = 2 if len(seed) <= 3 else 3
    tables = [t for t in img.tables(seed_vms) if t["members_hit"] >= need]
    table_words = {e for t in tables for e in t["entries"] if TABLE_ENTRY.match(e)}
    # Signal 2: code that compares against two seeds (or table entries). A word
    # that is also a verb (`sampler`, `automix`) is referenced by every skin
    # builder and dispatcher in the app, so it probes nothing on its own.
    probe_words = {w for w in set(seed) | table_words if w not in verbs}
    if len(probe_words) < 2:
        probe_words = set(seed) | table_words
    probe_vms = [vm for w in probe_words for vm in img.by_text.get(w, [])]
    # A region must compare against two seeds, or three table entries — one
    # seed plus one table word is how a stems switch joins the pad-page group.
    regions = [r for r in img.regions(sorted(set(probe_vms)))
               if len(set(r["members_hit"]) & set(seed)) >= 2 or len(r["members_hit"]) >= 3]
    region_words = {w for r in regions for w in r["referenced"] if len(w) >= 3}
    regions_dropped = False
    if len(table_words | region_words) > MAX_GROUP_MEMBERS and table_words:
        regions_dropped, regions, region_words = True, [], set()
    # Signal 1: pool neighbours of a seed — reported, never promoted alone.
    runs = {}
    for vm in seed_vms:
        r = img.run(vm)
        if sum(1 for v in r if img.strings[v] in seed) >= 2:
            runs[r[0]] = r
    run_words = {img.strings[v] for r in runs.values() for v in r}

    members = table_words | region_words
    signals = {}
    for w in sorted(members | run_words):
        tags = []
        if w in table_words:
            tags.append("table")
        if w in region_words:
            tags.append("region")
        if w in run_words:
            tags.append("run")
        signals[w] = tags
    related = {}
    for verb, srcs in known.items():
        hit = {src: sorted(set(v) & members) for src, v in srcs.items() if set(v) & members}
        specific = (set().union(*hit.values()) if hit else set()) - GENERIC - verbs
        if len(specific) >= 2 or (hit and verb in verbs_hint):
            related[verb] = hit
    known_words = set()
    for hit in related.values():
        for v in hit.values():
            known_words |= set(v)
    return {
        "seed": seed,
        "seed_unconfirmed": sorted(set(seed) - members),
        "regions_dropped": regions_dropped,
        "members": sorted(members),
        "novel": sorted(members - known_words),
        "pool_neighbours_only": sorted(run_words - members),
        "member_signals": {w: t for w, t in signals.items() if w in members},
        "signals": {
            "pointer_tables": tables,
            "code_regions": regions,
            "runs": [{"offset": img.file_offset(vm0), "strings": [img.strings[v] for v in r]}
                     for vm0, r in sorted(runs.items())],
        },
        "verbs": {v: {k: sorted(x) for k, x in h.items()} for v, h in sorted(related.items())},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", type=Path, default=DEFAULT_APP)
    ap.add_argument("--get", help="one named group")
    ap.add_argument("--verb", help="groups a verb is known to draw from")
    ap.add_argument("--tails", action="store_true", help="where each attested tail lives")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if (args.get or args.verb) and ARTIFACT.exists():
        art = json.load(open(ARTIFACT))
        if args.get:
            print(json.dumps(art["groups"].get(args.get) or {"error": f"no group {args.get}"}, indent=1))
        else:
            hits = {g: rec["verbs"][args.verb] for g, rec in art["groups"].items()
                    if args.verb in rec["verbs"]}
            print(json.dumps({"verb": args.verb, "groups": hits,
                              "tails": art["attested_tail_locations"].get(args.verb, {})}, indent=1))
        return 0

    img = Image(args.app)
    tails, known, verbs = load_sources()
    locations = locate_tails(img, tails, known)
    # Seeds: the named ones, plus an auto-group per shared attested tail —
    # seeded by its pool neighbours, kept only when a table or code region
    # backs the group. Generic words (`get`, `x`, `deck`) seed nothing.
    groups = {}
    for name, (seed, hint) in SEEDS.items():
        g = build_group(img, name, seed, known, verbs, verbs_hint=tuple(hint))
        if g:
            groups[name] = g
    covered = {w for g in groups.values() for w in g["members"]}
    for verb, toks in locations.items():
        for tok, rec in toks.items():
            if rec["where"] != "shared" or len(tok) < 4 or tok in covered:
                continue
            run = img.run(img.by_text[tok][0])
            seed = [img.strings[v] for v in run
                    if len(img.strings[v]) >= 4 and img.strings[v] not in verbs][:6]
            if len(seed) < 3 or tok not in seed:
                continue
            g = build_group(img, tok, seed, known, verbs, verbs_hint=(verb,))
            if not g or not (g["signals"]["pointer_tables"] or g["signals"]["code_regions"]):
                continue
            if not 3 <= len(g["members"]) <= MAX_AUTO_MEMBERS:
                continue
            groups[f"auto:{tok}"] = g
            covered |= set(g["members"])

    where = defaultdict(int)
    for toks in locations.values():
        for rec in toks.values():
            where[rec["where"]] += 1

    if args.tails:
        print(json.dumps({"summary": dict(where), "tails": locations}, indent=1))
        return 0

    with open(args.app / "Contents/Info.plist", "rb") as fh:
        build = plistlib.load(fh).get("CFBundleVersion", "?")
    summary = {
        "build": build,
        "groups": len(groups),
        "named": sum(1 for g in groups if not g.startswith("auto:")),
        "members": sum(len(g["members"]) for g in groups.values()),
        "novel_members": sum(len(g["novel"]) for g in groups.values()),
        "attested_tail_locations": dict(where),
        "signals": {"code_regions": sum(len(g["signals"]["code_regions"]) for g in groups.values()),
                    "pointer_tables": sum(len(g["signals"]["pointer_tables"]) for g in groups.values())},
    }
    if args.check:
        if not ARTIFACT.exists():
            print("binary vocabularies check skipped: artifact not extracted yet")
            return 0
        stored = json.load(open(ARTIFACT))["summary"]
        if stored["groups"] != summary["groups"] or stored["members"] != summary["members"]:
            sys.exit(f"binary vocabularies check FAILED: artifact has {stored['groups']} groups / "
                     f"{stored['members']} members, re-extraction finds {summary['groups']} / "
                     f"{summary['members']} — re-extract")
        print(f"binary vocabularies check passed: {stored['groups']} groups, {stored['members']} "
              f"members, {stored['novel_members']} unknown to any per-verb source")
        return 0

    json.dump({"summary": summary, "groups": groups, "attested_tail_locations": locations},
              sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
