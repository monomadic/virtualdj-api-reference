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


def cmd_prepare(args):
    target = LATE_PROBES if args.late else PROBES

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
    prep.add_argument("--remaining", action="store_true",
                      help="execute-capable keyword verbs (query position only)")
    prep.add_argument("--late", action="store_true",
                      help="write probes-late.txt: swept 40s AFTER load instead of during it")
    prep.add_argument("--leads", action="store_true",
                      help="follow-up list: deck context + keyword discrimination")
    prep.set_defaults(func=cmd_prepare)

    sub.add_parser("status", help="show the plugin workdir").set_defaults(
        func=cmd_status)
    coll = sub.add_parser("collect", help="normalize results.json to stdout")
    coll.add_argument("--late", action="store_true", help="read results-late.json")
    coll.set_defaults(func=cmd_collect)
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
