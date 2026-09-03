#!/usr/bin/env python3
"""One verb, everything this repo knows, on one screen.

    just verb fadeout
    just verb fadeout --format=json

The per-artifact commands (`get-verb`, `action-catalog`, `attested-tails`,
`verb-arg-forms`, `binary-vocab`, `verb-contract`, `verb-return-type`) each
answer one question. This joins them: the store record (kind, status, evidence),
the vendor's own description, a few real usages from the corpus, the argument
shapes with their return evidence, every tail candidate by source, the shared
vocabulary the verb draws from, and what has actually been probed. Aliases are
followed. Nothing here is new evidence — it is the existing artifacts, read
together, with the tier of each piece stated.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verbdb import joined_view, load_store  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "tests"


def load(name: str, key: str | None = None):
    path = T / name
    if not path.exists():
        return {}
    data = json.load(open(path))
    return data.get(key, {}) if key else data


def resolve(name: str, store: dict) -> tuple[str, dict | None, str | None]:
    rec = store.get(name)
    if rec and rec.get("tier") == "alias" and rec.get("canonical"):
        return rec["canonical"], store.get(rec["canonical"]), name
    if rec:
        return name, rec, None
    for n, r in store.items():
        if name in r.get("aliases", []):
            return n, r, name
    return name, None, None


def pick_examples(snippets: list[dict], verb: str, limit: int) -> list[dict]:
    """Short, diverse, vendor-shipped first: one per source, then by length."""
    mine = [s for s in snippets if verb in s["verbs"]]
    mine.sort(key=lambda s: (0 if "builtin" in s["sources"] else 1 if "catalog" in s["sources"]
                             else 2, len(s["script"])))
    out, seen = [], set()
    for s in mine:
        head = s["script"].split("&")[0].strip()[:24]
        if head in seen:
            continue
        seen.add(head)
        out.append(s)
        if len(out) >= limit:
            break
    return out


def summary(name: str, limit: int = 6) -> dict:
    store = load_store()
    canon, rec, alias_of = resolve(name, store)
    if rec is None:
        sys.exit(f"no record for '{name}' — try: just find-verbs {name}")
    rec = joined_view(canon, rec)
    catalog = load("action-catalog.json", "actions").get(canon, {})
    corpus = load("vdjscript-corpus.json", "snippets")
    tails_art = load("attested-tails.json")
    contract = load("action-contracts.json", "verbs").get(canon, {})
    probed = load("verb-arg-forms.json", "verbs").get(canon)
    executed = load("verb-execute-forms.json", "verbs").get(canon)
    ret = load("verb-return-types.json", "verbs").get(canon, {})
    vocab = load("binary-vocabularies.json", "groups")
    groups = {g: r["verbs"][canon] for g, r in vocab.items() if canon in r.get("verbs", {})}
    novel_in_groups = {g: vocab[g]["novel"] for g in groups}

    shapes = tails_art.get("shapes", {}).get(canon, {})
    # The store leaves `kind` empty for verbs the index never classified; the
    # HTTP sweep and the contract still know whether it answers queries.
    kind = rec.get("kind") or (rec.get("http_probe") or {}).get("kind")
    if not kind and contract:
        kind = "Query" if contract.get("queries") and not contract.get("executes") else \
               "Action" if contract.get("executes") else None
    return {
        "name": canon,
        "alias_of": alias_of,
        "aliases": rec.get("aliases", []),
        "kind": kind,
        "section": rec.get("section"),
        "surfaces": rec.get("surfaces", []),
        "status": {"test_status": rec.get("test_status"), "evidence": rec.get("evidence", []),
                   "blocked": rec.get("blocked", False)},
        "description": {"store": rec.get("description"), "store_example": rec.get("example"),
                        "catalog": catalog.get("text")},
        "examples": [{"script": s["script"], "sources": s["sources"], "origin": s["origins"][0]}
                     for s in pick_examples(corpus, canon, limit)],
        "shapes": {sh: {"n": len(r["snippets"]), "contexts": r["contexts"],
                        "returns": r["returns"], "example": r["snippets"][0]["snippet"]}
                   for sh, r in shapes.items()},
        "wrapper": tails_art.get("wrappers", {}).get(canon),
        "tails": {
            "catalog_documented": catalog.get("documented_parameters", []),
            "attested": sorted(tails_art.get("tails", {}).get(canon, {})),
            "binary_keyword_candidates": contract.get("keyword_candidates") or [],
            "probed_recognized": sorted({t for f in (probed or {}).get("recognized_tokens", [])
                                         for t in f}) if probed else None,
            "execute_position": executed,
        },
        "vocabulary_groups": {g: {"known_via": v, "unprobed_members": novel_in_groups[g]}
                              for g, v in groups.items()},
        "returns": {"observed_bare": ret.get("observed_type"), "samples": ret.get("samples"),
                    "structural": {k: contract.get(k) for k in ("queries", "query_bool", "query_text")
                                   if k in contract},
                    "arg_demand_slots": contract.get("arg_demand_slots")},
        "tiers": {"examples/shapes/attested": "Tier 2 vendor script — attested, not behaviour",
                  "catalog": "Tier 2 vendor prose — meaning, not behaviour",
                  "binary_keyword_candidates/vocabulary_groups": "Tier 2 structural — leads",
                  "probed_recognized/returns.observed_bare/status": "Tier 1 local test"},
    }


def render(s: dict) -> str:
    L = []
    head = s["name"] + (f"  (alias: {s['alias_of']})" if s["alias_of"] else "")
    L += [head, "=" * len(head)]
    L.append(f"{s['kind'] or '?'} · {s['section'] or '?'} · surfaces {', '.join(s['surfaces']) or '?'}"
             + (f" · aliases {', '.join(s['aliases'])}" if s["aliases"] else ""))
    st = s["status"]
    L.append(f"status {st['test_status']}" + (" (blocked)" if st["blocked"] else "")
             + (f" — {st['evidence'][0]}" if st["evidence"] else ""))
    L.append("")
    d = s["description"]
    if d["catalog"]:
        L += ["Vendor description (catalog):"] + ["  " + ln for ln in d["catalog"].splitlines()]
    elif d["store"]:
        L.append(f"Description (store): {d['store']}")
    if d["store_example"]:
        L.append(f"Store example: {d['store_example']}")
    L.append("")
    if s["examples"]:
        L.append("Usage (vendor corpus):")
        for e in s["examples"]:
            L.append(f"  {e['script']}")
            L.append(f"      — {'/'.join(e['sources'])}: {e['origin']}")
    else:
        L.append("Usage: no vendor snippet uses this verb")
    L.append("")
    if s["wrapper"]:
        L.append(f"Grammar wrapper: {s['name']} {s['wrapper']['shape']} — selectors "
                 + ", ".join(sorted(s["wrapper"]["selectors"])))
    if s["shapes"]:
        L.append("Argument shapes (attested; expression args reduced to their return type):")
        for sh, r in s["shapes"].items():
            ret = r["returns"]
            bits = []
            if ret["attested"]:
                bits.append("attribute ⇒ " + "/".join(ret["attested"]))
            if ret["executed_in"]:
                bits.append("executed in " + "/".join(ret["executed_in"]))
            L.append(f"  {s['name']} {sh:24} ×{r['n']}   {'; '.join(bits)}")
            L.append(f"      e.g. {r['example']}")
        prose = next((r["returns"]["catalog_prose"] for r in s["shapes"].values()
                      if r["returns"]["catalog_prose"]), [])
        if prose:
            L.append(f"  catalog says: {prose[0]}")
    else:
        L.append("Argument shapes: none attested (bare use only, or no vendor snippet)")
    L.append("")
    t = s["tails"]
    L.append("Tail candidates by source:")
    L.append(f"  catalog documented : {', '.join(t['catalog_documented']) or '—'}")
    L.append(f"  attested (corpus)  : {', '.join(t['attested']) or '—'}")
    L.append(f"  binary keywords    : {', '.join(t['binary_keyword_candidates']) or '—'}")
    if t["probed_recognized"] is None:
        L.append("  probed             : not probed")
    else:
        L.append(f"  probed recognized  : {', '.join(t['probed_recognized']) or '— (none separated from nonsense)'}")
    for g, v in s["vocabulary_groups"].items():
        L.append(f"  vocabulary group   : {g} — known via {v['known_via']}; "
                 f"unprobed members: {', '.join(v['unprobed_members']) or '—'}")
    L.append("")
    r = s["returns"]
    L.append(f"Returns: bare-form observed {r['observed_bare'] or 'unmeasured'}"
             + (f" {r['samples']}" if r["samples"] else "")
             + (f"; structural {r['structural']}" if r["structural"] else "")
             + (f"; demands an argument in slots {r['arg_demand_slots']}" if r["arg_demand_slots"] else ""))
    L.append("")
    L.append("Tiers: examples/shapes/attested and catalog are vendor material (Tier 2); binary "
             "keywords and vocabulary groups are structural leads (Tier 2); probed, observed "
             "return and status are local tests (Tier 1).")
    return "\n".join(L)


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    opts = [a for a in argv if a.startswith("--")]
    if not args:
        sys.exit("usage: verb_summary.py <verb> [--format=json] [--examples=N]")
    limit = next((int(o.split("=", 1)[1]) for o in opts if o.startswith("--examples=")), 6)
    s = summary(args[0], limit)
    if "--format=json" in opts:
        print(json.dumps(s, indent=1, ensure_ascii=False))
    else:
        print(render(s))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
