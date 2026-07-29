#!/usr/bin/env python3
"""Classify every verb name by what a bare `/query` returns.

Read-only: sends each name with no arguments to the HTTP control interface and
reads the HRESULT (or the value). The error code is the signal —

    E_NOTIMPL     (0x80004001)  verb EXISTS, no query implementation -> action-only
    E_INVALIDARG  (0x80070057)  verb EXISTS, recognized but wants arguments
    E_ACCESSDENIED(0x80070005)  verb EXISTS, but its context is unavailable here
    S_FALSE       (0x00000001)  verb EXISTS, evaluated successfully to false
    E_FAIL        (0x80004005)  no evidence either way -> unresolved
    <a value>                   verb EXISTS and answers bare -> query verb

This proves existence and classifies kind. It does NOT prove behavior, so it is
not a substitute for a recorded local test.

    python3 tools/sweep_verb_existence.py > tests/verb-existence-sweep.json
    python3 tools/sweep_verb_existence.py --names a,b,c      # probe specific names

See docs/HTTP Control Interface.md for the error-code taxonomy.
"""
import http.client
import json
import re
import sys
import urllib.parse

HOST, PORT = "localhost", 80
STORE = "docs/vdjscript-verbs.json"

E_NOTIMPL = -2147467263
E_FAIL = -2147467259
E_INVALIDARG = -2147024809
E_ACCESSDENIED = -2147024891
S_FALSE = 1

VERDICT = {
    E_NOTIMPL: ("exists", "action-only"),
    E_INVALIDARG: ("exists", "needs-args"),
    E_ACCESSDENIED: ("exists", "context-gated"),
    S_FALSE: ("exists", "false-here"),
    E_FAIL: ("unresolved", None),
}


CANDIDATES_DOC = "docs/Undocumented VDJScript Candidates.md"


def load_names():
    """Store names, plus backticked identifiers from the candidates doc.

    Candidate extraction is deliberately loose, so ordinary prose words in
    backticks come along too; they simply come back `unresolved`. Each result
    records its `source` so a junk word is never mistaken for a known verb.
    """
    data = json.load(open(STORE))
    recs = data if isinstance(data, list) else data.get("verbs", data)
    recs = list(recs.values()) if isinstance(recs, dict) else recs
    names = {r["name"]: "store" for r in recs if isinstance(r, dict) and r.get("name")}
    try:
        txt = open(CANDIDATES_DOC).read()
    except OSError:
        return names
    for cand in re.findall(r"`([a-z][a-z0-9_]{2,})`", txt):
        names.setdefault(cand, "candidate-doc")
    return names


ARTIFACT = "tests/verb-existence-sweep.json"


def cmd_get(name):
    data = json.load(open(ARTIFACT))["verbs"]
    rec = data.get(name)
    if rec is None:
        sys.exit(f"no probe result for {name!r} (re-run the sweep?)")
    print(json.dumps(rec, indent=1))


def cmd_check():
    data = json.load(open(ARTIFACT))
    verbs, summary = data["verbs"], data["summary"]
    if len(verbs) < 900:
        sys.exit(f"existence sweep looks truncated: {len(verbs)} names")
    if sum(summary.values()) != len(verbs):
        sys.exit("existence sweep summary does not match verb count")
    proven = sum(n for k, n in summary.items() if k.startswith("exists"))
    print(f"verb existence sweep check passed: {len(verbs)} names, {proven} proven to exist")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--get":
        return cmd_get(sys.argv[2])
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        return cmd_check()
    if len(sys.argv) > 2 and sys.argv[1] == "--names":
        names = [n.strip() for n in sys.argv[2].split(",") if n.strip()]
    else:
        names = load_names()
    conn = http.client.HTTPConnection(HOST, PORT, timeout=10)
    out = {}
    for i, name in enumerate(names, 1):
        path = "/query?" + urllib.parse.urlencode({"script": name})
        for attempt in (1, 2):
            try:
                conn.request("GET", path)
                body = conn.getresponse().read().decode(errors="replace").strip()
                break
            except (http.client.HTTPException, OSError):
                conn.close()
                conn = http.client.HTTPConnection(HOST, PORT, timeout=10)
                if attempt == 2:
                    body = "error:transport"
        if body.startswith("error:"):
            try:
                code = int(body.split(":", 1)[1])
            except ValueError:
                code = None
            status, kind = VERDICT.get(code, ("unknown-code", None))
            out[name] = {"status": status, "kind": kind, "code": code, "source": names[name]}
        else:
            out[name] = {"status": "exists", "kind": "query", "value": body, "source": names[name]}
        if i % 100 == 0:
            print(f"  ...{i}/{len(names)}", file=sys.stderr, flush=True)
    conn.close()

    tally = {}
    for rec in out.values():
        key = f"{rec['status']}/{rec['kind']}" if rec["kind"] else rec["status"]
        tally[key] = tally.get(key, 0) + 1
    print(json.dumps({"summary": tally, "verbs": out}, indent=1, sort_keys=True))
    print(f"summary: {tally}", file=sys.stderr)


if __name__ == "__main__":
    main()
