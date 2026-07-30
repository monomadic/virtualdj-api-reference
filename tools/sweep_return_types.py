#!/usr/bin/env python3
"""Observe the HTTP return type of every query verb, and reconcile it with the
structural contract matrix.

Task 10 leg: the existence sweep proved which verbs answer `/query`; this sweep
records *what type* they answer with. Each query verb is sampled in three
read-only contexts (bare, `deck 1 …`, `deck 2 …`) so state-dependent verbs get a
chance to show more than one value, and the samples are classified on a small
lattice:

    bool (yes/no/on/off/true/false)  int  float  percent  empty  text

merged per verb (int ⊔ float = float; anything ⊔ text = text; empty defers to a
typed sibling; bool ⊔ numeric = mixed, flagged). The observation is Tier 1 but
single-machine, idle-state: it proves the verb CAN return this type, not that it
always does.

Each verb is then reconciled with `tests/action-contracts.json` (the vtable
override matrix). The generic query slot returns a variant — bool, number, and
text all flow through it — so the reconciliation is capability-level: a typed
observation agrees when the class overrides any query path (generic,
specialized text, or an extended/slider interface). Disagreements are recorded,
not hidden — they are leads. **This sweep, not the structure, is the authority
for a verb's concrete rendered type** (Tier 1, single-machine, idle-state: it
proves the verb CAN return this type, not that it always does).

    python3 tools/sweep_return_types.py > tests/verb-return-types.json
    python3 tools/sweep_return_types.py --get crossfader
    python3 tools/sweep_return_types.py --check
"""
import http.client
import json
import re
import sys
import urllib.parse

HOST, PORT = "localhost", 80
SWEEP = "tests/verb-existence-sweep.json"
CONTRACTS = "tests/action-contracts.json"
ARTIFACT = "tests/verb-return-types.json"
CONTEXTS = ["{v}", "deck 1 {v}", "deck 2 {v}"]
# A verb's VALUE and its BOOLEAN TRUTH are independent channels: `get_version`
# answers 2026 yet is false in a conditional. Probe the boolean separately.
TRUTH_PROBE = "{v} ? get_text 'T' : get_text 'F'"
BOOL_WORDS = {"yes", "no", "on", "off", "true", "false"}


def classify(v: str) -> str:
    if v.startswith("error:"):
        return "error"
    if v == "":
        return "empty"
    if v.lower() in BOOL_WORDS:
        return "bool"
    if re.fullmatch(r"-?\d+", v):
        return "int"
    if re.fullmatch(r"-?\d*\.\d+", v):
        return "float"
    if re.fullmatch(r"-?\d+(\.\d+)?\s*%", v):
        return "percent"
    return "text"


def merge(kinds) -> str:
    ks = {k for k in kinds if k not in ("error", "empty")}
    if not ks:
        return "untyped"
    if ks <= {"int", "float"}:
        return "float" if "float" in ks else "int"
    if ks == {"bool"}:
        return "bool"
    if ks == {"percent"}:
        return "percent"
    if "text" in ks and ks <= {"text", "int", "float", "percent"}:
        return "text"
    if len(ks) == 1:
        return ks.pop()
    return "mixed"


def reconcile(observed: str, c: dict) -> str:
    if not c:
        return "no-contract"
    if observed in ("untyped", "mixed"):
        return "unclassified"
    can_query = c.get("queries") or c.get("query_text") \
        or c.get("extended_interface") or c.get("family") == "slider"
    return "agree" if can_query else "conflict"


def sweep() -> dict:
    names = sorted(n for n, r in json.load(open(SWEEP))["verbs"].items()
                   if r.get("kind") == "query")
    contracts = json.load(open(CONTRACTS))["verbs"]
    conn = http.client.HTTPConnection(HOST, PORT, timeout=10)
    out = {}
    for name in names:
        samples = {}
        for ctx in CONTEXTS:
            script = ctx.format(v=name)
            path = "/query?" + urllib.parse.urlencode({"script": script})
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
            samples[script] = body
        kinds = [classify(v) for v in samples.values()]
        observed = merge(kinds)
        c = contracts.get(name, {})
        rec = {
            "observed_type": observed,
            "samples": samples,
            "agreement": reconcile(observed, c),
        }
        # boolean truth in ternary-condition position — NOT derivable from the value
        path = "/query?" + urllib.parse.urlencode(
            {"script": TRUTH_PROBE.format(v=name)})
        for attempt in (1, 2):
            try:
                conn.request("GET", path)
                tb = conn.getresponse().read().decode(errors="replace").strip()
                break
            except (http.client.HTTPException, OSError):
                conn.close()
                conn = http.client.HTTPConnection(HOST, PORT, timeout=10)
                if attempt == 2:
                    tb = "error:transport"
        if tb in ("T", "F"):
            rec["boolean_truth"] = tb == "T"
            first = next(iter(samples.values()), "")
            if tb == "F" and first not in ("", "0", "0.0", "no", "off", "false"):
                # the trap: a value that reads as true, in a verb that is not
                rec["truthiness_trap"] = True
        if c:
            rec["structural"] = {k: c[k] for k in ("queries", "query_text")}
            if "family" in c:
                rec["structural"]["family"] = c["family"]
        out[name] = rec

    from collections import Counter
    types = Counter(r["observed_type"] for r in out.values())
    agrees = Counter(r["agreement"] for r in out.values())
    truth = [r for r in out.values() if "boolean_truth" in r]
    traps = sorted(n for n, r in out.items() if r.get("truthiness_trap"))
    typed = sum(n for t, n in types.items() if t not in ("untyped", "mixed"))
    denom = agrees["agree"] + agrees["conflict"]
    return {
        "summary": {
            "query_verbs": len(out),
            "typed": typed,
            "observed_types": dict(types),
            "agreement": dict(agrees),
            "agreement_rate": round(agrees["agree"] / denom, 4) if denom else None,
            "conflicts": sorted(n for n, r in out.items()
                                if r["agreement"] == "conflict"),
            "boolean_probed": len(truth),
            "boolean_true": sum(1 for r in truth if r["boolean_truth"]),
            "truthiness_traps": len(traps),
            "truthiness_trap_verbs": traps,
        },
        "verbs": out,
    }


def cmd_get(name):
    rec = json.load(open(ARTIFACT))["verbs"].get(name)
    if rec is None:
        sys.exit(f"no return-type record for {name!r} (query verbs only; re-sweep?)")
    print(json.dumps({"name": name, **rec}, indent=1))


def cmd_check():
    s = json.load(open(ARTIFACT))["summary"]
    errs = []
    if s["query_verbs"] < 600:
        errs.append(f"sweep looks truncated: {s['query_verbs']} query verbs")
    if s["typed"] < s["query_verbs"] * 0.8:
        errs.append(f"too few typed: {s['typed']}/{s['query_verbs']}")
    if s["agreement_rate"] is not None and s["agreement_rate"] < 0.85:
        errs.append(f"structural agreement too low: {s['agreement_rate']}")
    if errs:
        sys.exit("return-type sweep check FAILED:\n  - " + "\n  - ".join(errs))
    print(f"return-type sweep check passed: {s['query_verbs']} query verbs, "
          f"{s['typed']} typed {s['observed_types']}, "
          f"agreement {s['agreement_rate']} ({len(s['conflicts'])} conflicts), "
          f"boolean-true {s.get('boolean_true')}/{s.get('boolean_probed')}, "
          f"{s.get('truthiness_traps')} truthiness traps")


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--get":
        return cmd_get(sys.argv[2])
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        return cmd_check()
    print(json.dumps(sweep(), indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
