#!/usr/bin/env python3
"""Drive the read-only VDJIntrospect plugin and turn its raw capture into an artifact.

Task 10a. The HTTP control interface renders every answer to text, so a verb's
real type has to be inferred from the rendering. The plugin channel does not:
`GetInfo` hands back a `double` and `GetStringInfo` a UTF-8 buffer, each with its
own HRESULT, so *which channel a verb answers on* is observed rather than
guessed. This script prepares the probe list, then normalizes what the plugin
wrote back.

The plugin never calls `SendCommand` — everything here is query position.

    python3 tools/plugin_introspect.py prepare          # write probes.txt (all verbs)
    python3 tools/plugin_introspect.py prepare --verbs get_bpm,crossfader
    python3 tools/plugin_introspect.py status           # what is in the plugin's workdir
    python3 tools/plugin_introspect.py collect > tests/plugin-introspection.json
    python3 tools/plugin_introspect.py --get master_beat_num
    python3 tools/plugin_introspect.py --check

Workflow: `just plugin-build --install`, restart VirtualDJ, `just plugin-prepare`,
restart again (the sweep runs at plugin load), then `just plugin-collect`.
"""
import argparse
import json
import os
import sys

VERB_TABLE = "tests/verb-table.json"
CONTRACTS = "tests/action-contracts.json"
SWEEP = "tests/verb-existence-sweep.json"
ARTIFACT = "tests/plugin-introspection.json"
LEADS_ARTIFACT = "tests/plugin-introspection-leads.json"
BOGUS = "zzznotakeyword"
WORKDIR = os.path.expanduser(
    "~/Library/Application Support/VirtualDJ/VDJIntrospect")
PROBES = os.path.join(WORKDIR, "probes.txt")
RESULTS = os.path.join(WORKDIR, "results.json")
# The delayed second sweep: same plugin, run from a timer thread ~40s after load
# instead of during it. Its reason for existing is that `OnLoad` fires while
# VirtualDJ is still starting up, so anything not yet initialized (the browser)
# looks like it does not answer at all.
LATE_PROBES = os.path.join(WORKDIR, "probes-late.txt")
LATE_RESULTS = os.path.join(WORKDIR, "results-late.json")
SONGBUFFER = os.path.join(WORKDIR, "songbuffer.txt")
SONGBUFFER_RESULTS = os.path.join(WORKDIR, "results-songbuffer.json")
GO = os.path.join(WORKDIR, "go.txt")
LOG = os.path.join(WORKDIR, "plugin.log")

# Signed 32-bit HRESULTs, as the plugin writes them.
HRESULTS = {
    0: "S_OK",
    1: "S_FALSE",
    -1: "CLASS_E_CLASSNOTAVAILABLE",
    -2147467263: "E_NOTIMPL",
    -2147467259: "E_FAIL",
    -2147024809: "E_INVALIDARG",
    -2147024891: "E_ACCESSDENIED",
    -2147467262: "E_NOINTERFACE",
    -2147024882: "E_OUTOFMEMORY",
}


def hresult_name(code):
    return HRESULTS.get(code, f"0x{code & 0xffffffff:08x}")


def leads_probes():
    """The follow-up probe list: deck context, and keyword-vs-nonsense pairs.

    Two questions the bare-verb capture could not ask.

    1. Deck context. 50 verbs the HTTP sweep calls `query` answered on neither
       plugin callback. HTTP `/query` evaluates with a deck context that a bare
       plugin call may lack, so each is re-probed with `deck 1` / `deck 2` and
       with a `1` argument (many are effect/slider readers that want an index).
    2. Keyword discrimination. The plugin returns the HRESULT separately from
       the value, so a recognized argument may be distinguishable from an
       ignored one even when both render identically. Each binary-recovered
       keyword is paired with a nonsense control on the same verb.

    Only verbs whose contract says `executes: false` are given arguments here.
    Query position is side-effect-free in this repo's model, but an
    execute-capable verb plus a state-selecting keyword (`browser_window
    sampler`) is not worth betting a read-only guarantee on.
    """
    contracts = json.load(open(CONTRACTS))["verbs"]
    sweep = json.load(open(SWEEP))["verbs"]
    base = json.load(open(ARTIFACT))["probes"]

    out, seen = [], set()

    def add(probe, why):
        if probe not in seen:
            seen.add(probe)
            out.append((probe, why))

    silent = sorted(n for n, r in base.items()
                    if r["channel"] == "neither"
                    and sweep.get(n, {}).get("kind") == "query")
    for n in silent:
        add(f"deck 1 {n}", "context")
        add(f"deck 2 {n}", "context")
        add(f"{n} 1", "context")

    pure = sorted(n for n, r in contracts.items()
                  if r.get("keyword_candidates") and not r.get("executes"))
    for n in pure:
        add(n, "keyword")
        for kw in contracts[n]["keyword_candidates"]:
            add(f"{n} {kw}", "keyword")
        add(f"{n} {BOGUS}", "keyword")

    return out, len(silent), len(pure)


# Excluded from the execute-capable keyword sweep. Query position is
# side-effect-free in this repo's model and `GetInfo` maps to the query slot, but
# these are the families where being wrong about that is expensive rather than
# merely annoying. Exclusions are printed, never silent.
UNSAFE_CATEGORIES = {"system", "config", "record"}
UNSAFE_NAMES = {"broadcast_message", "browsed_file_analyze", "browsed_file_rename",
                "effect_bank_save", "system"}


def remaining_keyword_probes():
    """The execute-capable half of the keyword queue.

    The 62 pure-query verbs were swept first because they carry no risk at all.
    These 227 also declare an execute path, so each is probed only in query
    position, and the file/config/system families are dropped outright.
    """
    contracts = json.load(open(CONTRACTS))["verbs"]
    table = json.load(open(VERB_TABLE))["verbs"]

    probes, skipped = [], []
    for n in sorted(contracts):
        r = contracts[n]
        if not r.get("keyword_candidates") or not r.get("executes"):
            continue
        if table.get(n, {}).get("category") in UNSAFE_CATEGORIES or n in UNSAFE_NAMES:
            skipped.append(n)
            continue
        probes.append(n)
        probes.extend(f"{n} {kw}" for kw in r["keyword_candidates"])
        probes.append(f"{n} {BOGUS}")
    return probes, skipped


def prepared_state_probes():
    """Everything that an idle app could not answer.

    Two groups, both waiting on app state rather than on a better channel:

    1. Keyword pairs that came back indistinguishable. Most keywords select
       between things that are all inert with no track loaded, so the nonsense
       control matched them by default. Re-asked with real state, a recognized
       keyword has something to differ about.
    2. The song-level browser readers, which stayed silent even in the delayed
       sweep. They answer over HTTP with a song highlighted, so a *selection* is
       the variable, not initialization.
    """
    contracts = json.load(open(CONTRACTS))["verbs"]
    table = json.load(open(VERB_TABLE))["verbs"]

    inert = {}
    for path in ("tests/plugin-introspection-leads.json",
                 "tests/plugin-introspection-remaining.json"):
        if not os.path.exists(path):
            continue
        p = json.load(open(path))["probes"]
        for n, r in contracts.items():
            control = p.get(f"{n} {BOGUS}")
            if not r.get("keyword_candidates") or control is None:
                continue
            for kw in r["keyword_candidates"]:
                rec = p.get(f"{n} {kw}")
                if rec is None:
                    continue
                same = (rec["numeric_hresult"], rec["text_hresult"],
                        rec.get("numeric"), rec["text"]) == \
                       (control["numeric_hresult"], control["text_hresult"],
                        control.get("numeric"), control["text"])
                if same and n not in UNSAFE_NAMES and \
                        table.get(n, {}).get("category") not in UNSAFE_CATEGORIES:
                    inert.setdefault(n, []).append(kw)

    probes = []
    for n in sorted(inert):
        probes.append(n)
        probes.extend(f"{n} {kw}" for kw in inert[n])
        probes.append(f"{n} {BOGUS}")

    # Still-silent browser readers, and controls that prove the prepared state
    # actually took (a loaded deck, a highlighted song) so a null result cannot
    # be blamed on the setup.
    probes += ["get_browsed_comment", "get_browsed_composer", "get_browsed_song",
               "get_browsed_artist", "get_browsed_title", "get_browsed_key",
               "get_browsed_filepath", "get_sample_info", "sidereco_song"]
    probes += ["get_title", "get_artist", "get_bpm", "loaded", "get_filepath",
               "get_browsed_folder", "play"]
    return probes, len(inert)


# Position/length pairs chosen so the UNITS fall out of the data rather than an
# assumption. Nothing documents whether `pos` counts samples, frames, or
# milliseconds, so the list deliberately includes:
#   * the same span twice (determinism / caching)
#   * spans offset by 1 and by nb (overlap tells us the step size)
#   * 44100 and 1000 (one second, if the unit is samples or ms respectively)
#   * a position past any plausible song length (bounds behaviour)
#   * nb=1 (the smallest legal ask)
SONGBUFFER_REQUESTS = [
    (0, 1024), (0, 1024), (1, 1024), (512, 1024), (1024, 1024),
    (1000, 1024), (44100, 1024), (88200, 1024), (441000, 1024),
    (0, 1), (0, 2), (0, 4096),
    (-1, 1024), (999999999, 1024),
]


def cmd_songbuffer(args):
    os.makedirs(WORKDIR, exist_ok=True)
    with open(SONGBUFFER, "w") as f:
        f.write("# GetSongBuffer probe: '<pos> <nb>' per line. Read-only.\n")
        for pos, nb in SONGBUFFER_REQUESTS:
            f.write(f"{pos} {nb}\n")
    print(f"wrote {len(SONGBUFFER_REQUESTS)} requests to {SONGBUFFER}")
    print("Load a track, then: just plugin-go")


def cmd_songbuffer_report(args):
    d = json.load(open(SONGBUFFER_RESULTS))
    print(f"song: {d['song_title']!r}  totaltime={d['get_totaltime']} "
          f"position={d['get_position']} bpm={d['get_bpm']}")
    print(f"{'pos':>11} {'nb':>5} {'hresult':>13} {'rms':>10} {'even/odd':>15}  head")
    for r in d["requests"]:
        if r["hresult"] != 0 or r["buffer_null"]:
            print(f"{r['pos']:>11} {r['nb']:>5} {hresult_name(r['hresult']):>13} "
                  f"{'null' if r['buffer_null'] else '':>10}")
            continue
        even = "-" if r["rms_even"] is None else f"{r['rms_even']:.1f}"
        odd = "-" if r["rms_odd"] is None else f"{r['rms_odd']:.1f}"
        print(f"{r['pos']:>11} {r['nb']:>5} {'S_OK':>13} {r['rms']:>10.1f} "
              f"{even:>7}/{odd:<7} {r['head'][:6]}")

    ok = [r for r in d["requests"] if r["hresult"] == 0 and not r["buffer_null"]]
    by_hash = {}
    for r in ok:
        by_hash.setdefault(r["hash"], []).append((r["pos"], r["nb"]))
    print("\nidentical buffers (same hash) — this is what pins the units:")
    for h, rs in by_hash.items():
        if len(rs) > 1:
            print(f"  {h}: {rs}")


def cmd_go(args):
    os.makedirs(WORKDIR, exist_ok=True)
    open(GO, "w").close()
    print(f"triggered — the plugin sweeps {LATE_PROBES} within ~2s "
          f"(no restart). Then: just plugin-collect --late")


def cmd_prepare(args):
    target = LATE_PROBES if args.late else PROBES

    if args.prepared_state:
        probes, n_verbs = prepared_state_probes()
        os.makedirs(WORKDIR, exist_ok=True)
        with open(target, "w") as f:
            f.write("# VDJIntrospect — needs prepared state (track loaded, song highlighted).\n")
            f.write("\n".join(probes) + "\n")
        print(f"wrote {len(probes)} probes to {target} "
              f"({n_verbs} verbs whose keywords were indistinguishable when idle, "
              f"plus browser readers and state controls)")
        return

    if args.remaining:
        probes, skipped = remaining_keyword_probes()
        os.makedirs(WORKDIR, exist_ok=True)
        with open(target, "w") as f:
            f.write("# VDJIntrospect — execute-capable keyword verbs, query position only.\n")
            f.write("\n".join(probes) + "\n")
        print(f"wrote {len(probes)} probes to {target}")
        print(f"EXCLUDED {len(skipped)} verbs (file/config/system families): "
              f"{', '.join(skipped)}")
        return

    if args.leads:
        probes, n_silent, n_kw = leads_probes()
        os.makedirs(WORKDIR, exist_ok=True)
        with open(target, "w") as f:
            f.write("# VDJIntrospect lead probes — deck context + keyword discrimination.\n")
            for probe, why in probes:
                f.write(f"{probe}\n")
        print(f"wrote {len(probes)} lead probes to {target} "
              f"({n_silent} silent query verbs × 3 forms, "
              f"{n_kw} pure-query keyword verbs)")
        print("Restart VirtualDJ, then: just plugin-collect-leads")
        return

    if args.verbs:
        names = [v.strip() for v in args.verbs.split(",") if v.strip()]
    else:
        names = sorted(json.load(open(VERB_TABLE))["verbs"])
        if args.limit:
            names = names[:args.limit]

    os.makedirs(WORKDIR, exist_ok=True)
    with open(target, "w") as f:
        f.write("# VDJIntrospect probe list — one query-position script per line.\n")
        f.write("# Written by tools/plugin_introspect.py; '#' comments are skipped.\n")
        for n in names:
            f.write(n + "\n")
    print(f"wrote {len(names)} probes to {target}")
    print("Restart VirtualDJ — the sweep runs when the plugin loads.")


def cmd_status(args):
    for path, label in ((PROBES, "probes.txt"), (RESULTS, "results.json"),
                        (LOG, "plugin.log")):
        if os.path.exists(path):
            size = os.path.getsize(path)
            mtime = __import__("time").strftime(
                "%Y-%m-%d %H:%M:%S", __import__("time").localtime(
                    os.path.getmtime(path)))
            print(f"{label:14} {size:>9,} bytes  {mtime}")
        else:
            print(f"{label:14} (absent)")
    if os.path.exists(LOG):
        print("\nlast log lines:")
        for line in open(LOG).read().splitlines()[-8:]:
            print("  " + line)


def collect(late=False):
    raw = json.load(open(LATE_RESULTS if late else RESULTS))
    out, channels = {}, {}

    for rec in raw["probes"]:
        num_hr, txt_hr = rec["numeric_hresult"], rec["text_hresult"]
        answered_num = num_hr == 0 and rec.get("numeric_written", False)
        answered_txt = txt_hr == 0 and rec["text_len"] > 0

        if answered_num and answered_txt:
            channel = "both"
        elif answered_num:
            channel = "numeric"
        elif answered_txt:
            channel = "text"
        else:
            channel = "neither"
        channels[channel] = channels.get(channel, 0) + 1

        entry = {
            "channel": channel,
            "numeric_hresult": hresult_name(num_hr),
            "text_hresult": hresult_name(txt_hr),
            "text": rec["text"],
            "text_len": rec["text_len"],
        }
        if "numeric" in rec:
            entry["numeric"] = rec["numeric"]
            entry["numeric_bits"] = rec["numeric_bits"]
        out[rec["probe"]] = entry

    return {
        "summary": {
            "channel": "plugin",
            "tool_version": raw["tool_version"],
            "captured_utc": raw["captured_utc"],
            "trigger": raw["trigger"],
            "host_version": raw["host_version"],
            "probes": len(out),
            "channels": dict(sorted(channels.items())),
        },
        "probes": out,
    }


def cmd_collect(args):
    print(json.dumps(collect(args.late), indent=1, sort_keys=True))


def cmd_get(name):
    import glob
    for path in sorted(glob.glob("tests/plugin-introspection*.json")):
        rec = json.load(open(path))["probes"].get(name)
        if rec is not None:
            return print(json.dumps({"probe": name, "capture": path, **rec}, indent=1))
    sys.exit(f"no plugin-channel record for {name!r} "
             f"(is it in the probe list? re-run prepare/collect)")


def cmd_leads_report(args):
    """Answer the two lead questions from the follow-up capture."""
    p = json.load(open(LEADS_ARTIFACT))["probes"]
    contracts = json.load(open(CONTRACTS))["verbs"]
    base = json.load(open(ARTIFACT))["probes"]

    def sig(rec):
        return (rec["numeric_hresult"], rec["text_hresult"],
                rec.get("numeric"), rec["text"])

    print("=== Lead 1: does a deck context wake the silent query verbs? ===")
    silent = sorted(n for n in base
                    if base[n]["channel"] == "neither"
                    and any(f"deck 1 {n}" == q for q in p))
    woke = []
    for n in silent:
        forms = {f: p[f] for f in (f"deck 1 {n}", f"deck 2 {n}", f"{n} 1") if f in p}
        answered = {f: r for f, r in forms.items() if r["channel"] != "neither"}
        if answered:
            woke.append((n, answered))
    print(f"{len(silent)} silent verbs re-probed, {len(woke)} answered in some form")
    for n, answered in woke:
        for f, r in answered.items():
            val = r.get("numeric") if r["channel"] != "text" else r["text"]
            print(f"  {f:38} {r['channel']:8} {val!r}")

    print("\n=== Lead 2: does the HRESULT tell a keyword from nonsense? ===")
    verbs = sorted(n for n in contracts
                   if contracts[n].get("keyword_candidates") and n in p)
    hr_discriminates, value_discriminates, inert = [], [], []
    for n in verbs:
        bogus = p.get(f"{n} {BOGUS}")
        if bogus is None:
            continue
        for kw in contracts[n]["keyword_candidates"]:
            rec = p.get(f"{n} {kw}")
            if rec is None:
                continue
            hr_differs = (rec["numeric_hresult"], rec["text_hresult"]) != \
                         (bogus["numeric_hresult"], bogus["text_hresult"])
            val_differs = sig(rec) != sig(bogus)
            if hr_differs:
                hr_discriminates.append((n, kw, rec, bogus))
            elif val_differs:
                value_discriminates.append((n, kw, rec, bogus))
            else:
                inert.append((n, kw))
    total = len(hr_discriminates) + len(value_discriminates) + len(inert)
    print(f"{total} keyword/nonsense pairs on {len(verbs)} verbs:")
    print(f"  HRESULT differs : {len(hr_discriminates)}")
    print(f"  value differs   : {len(value_discriminates)}")
    print(f"  indistinguishable: {len(inert)}")
    for label, rows in (("HRESULT", hr_discriminates), ("VALUE", value_discriminates)):
        for n, kw, rec, bogus in rows[:40]:
            print(f"  [{label}] {n} {kw!r}: "
                  f"{rec['numeric_hresult']}/{rec['text_hresult']} {rec['text']!r} "
                  f"vs nonsense {bogus['numeric_hresult']}/{bogus['text_hresult']} "
                  f"{bogus['text']!r}")


def cmd_keyword_report(args):
    """Three-way split of every keyword against its nonsense control.

    The point of the nonsense control is that an unrecognized argument is
    *silently ignored* (established over HTTP, 2026-07-30), so a keyword cannot
    be confirmed by asking whether it errors. It is confirmed by differing from
    a word that is definitely not a keyword, on the same verb, in the same state.
    """
    p = json.load(open(args.capture))["probes"]
    contracts = json.load(open(CONTRACTS))["verbs"]

    hr, val, inert = [], [], []
    for n, r in sorted(contracts.items()):
        control = p.get(f"{n} {BOGUS}")
        if not r.get("keyword_candidates") or control is None:
            continue
        for kw in r["keyword_candidates"]:
            rec = p.get(f"{n} {kw}")
            if rec is None:
                continue
            if (rec["numeric_hresult"], rec["text_hresult"]) != \
               (control["numeric_hresult"], control["text_hresult"]):
                hr.append((n, kw, rec, control))
            elif (rec.get("numeric"), rec["text"]) != \
                 (control.get("numeric"), control["text"]):
                val.append((n, kw, rec, control))
            else:
                inert.append((n, kw))

    total = len(hr) + len(val) + len(inert)
    verbs = {n for n, _, _, _ in hr} | {n for n, _, _, _ in val} | {n for n, _ in inert}
    print(f"{args.capture}: {total} keyword/nonsense pairs over {len(verbs)} verbs")
    print(f"  confirmed by HRESULT : {len(hr):4}  ({len({n for n,_,_,_ in hr})} verbs)")
    print(f"  confirmed by value   : {len(val):4}  ({len({n for n,_,_,_ in val})} verbs)")
    print(f"  indistinguishable    : {len(inert):4}  (NOT disproof — an idle app "
          f"gives most keywords nothing to vary)")
    if args.verbose:
        for label, rows in (("HRESULT", hr), ("VALUE", val)):
            for n, kw, rec, control in rows:
                print(f"  [{label}] {n} {kw!r}: "
                      f"{rec['numeric_hresult']}/{rec['text_hresult']} {rec['text'][:20]!r}"
                      f"  vs nonsense {control['numeric_hresult']}/"
                      f"{control['text_hresult']} {control['text'][:20]!r}")


def cmd_check():
    if not os.path.exists(ARTIFACT):
        print("plugin introspection check skipped: no capture yet "
              f"({ARTIFACT} absent)")
        return
    s = json.load(open(ARTIFACT))["summary"]
    errs = []
    if s["probes"] < 1:
        errs.append("capture is empty")
    if s["channels"].get("neither", 0) == s["probes"]:
        errs.append("no probe answered on either channel — was VirtualDJ idle "
                    "or the plugin unloaded?")
    if errs:
        sys.exit("plugin introspection check FAILED:\n  - " + "\n  - ".join(errs))
    print(f"plugin introspection check passed: {s['probes']} probes on "
          f"{s['host_version']}, channels {s['channels']}")


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--get", metavar="PROBE")
    p.add_argument("--check", action="store_true")
    sub = p.add_subparsers(dest="cmd")

    prep = sub.add_parser("prepare", help="write the plugin's probe list")
    prep.add_argument("--verbs", help="comma-separated probes instead of every verb")
    prep.add_argument("--limit", type=int, help="first N verbs only")
    prep.add_argument("--prepared-state", action="store_true",
                      help="what an idle app could not answer: inert keywords + browser readers")
    prep.add_argument("--remaining", action="store_true",
                      help="execute-capable keyword verbs (query position only)")
    prep.add_argument("--late", action="store_true",
                      help="write probes-late.txt: swept 40s AFTER load instead of during it")
    prep.add_argument("--leads", action="store_true",
                      help="follow-up list: deck context + keyword discrimination")
    prep.set_defaults(func=cmd_prepare)

    sub.add_parser("status", help="show the plugin workdir").set_defaults(
        func=cmd_status)
    sub.add_parser("go", help="trigger a re-sweep of the delayed list, no restart").set_defaults(
        func=cmd_go)
    sub.add_parser("songbuffer",
                   help="write the GetSongBuffer request list").set_defaults(
        func=cmd_songbuffer)
    sub.add_parser("songbuffer-report",
                   help="read the GetSongBuffer capture").set_defaults(
        func=cmd_songbuffer_report)
    coll = sub.add_parser("collect", help="normalize results.json to stdout")
    coll.add_argument("--late", action="store_true", help="read results-late.json")
    coll.set_defaults(func=cmd_collect)
    kwr = sub.add_parser("keyword-report",
                         help="confirm keywords against their nonsense controls")
    kwr.add_argument("--capture", default=LEADS_ARTIFACT)
    kwr.add_argument("--verbose", action="store_true")
    kwr.set_defaults(func=cmd_keyword_report)

    sub.add_parser("leads-report",
                   help="analyze the follow-up capture").set_defaults(
        func=cmd_leads_report)

    args = p.parse_args()
    if args.get:
        return cmd_get(args.get)
    if args.check:
        return cmd_check()
    if not args.cmd:
        p.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
