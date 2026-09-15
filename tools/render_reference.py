#!/usr/bin/env python3
"""Fill the human-facing reference template from the verb store.

    just reference                      # → build/reference/index.html
    python3 tools/render_reference.py --out /tmp/x.html

The template is `design/human-api-reference.template.html`; the page it
produces is a rendered *copy* of store data, so it is written to the
git-ignored `build/` tree and never committed. Nothing here is new evidence:
every field is the existing store record and artifacts, joined the same way
`just verb` joins them, with the tier of each piece carried into the page.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verbdb import joined_view  # noqa: E402
from coverage_report import assess, build_stamp, load_context  # noqa: E402
from verb_summary import pick_examples  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "design" / "human-api-reference.template.html"
LOGO = ROOT / "design" / "logo.png"
DEFAULT_OUT = ROOT / "build" / "reference" / "index.html"

# Status signal: store test_status → (css class, label). The css classes are
# the ones the template styles; "verified" has no override and renders teal.
SIGNAL = {
    "Pass": ("verified", "Locally verified"),
    "Partial": ("partial", "Partially verified"),
    "Fail": ("caveat", "Known caveat"),
    "Untested": ("unverified", "Behavior untested"),
}

# Source label → css class for contract rows. The classes mirror the evidence
# tiers: observed/local are Tier 1, curated is Tier 2 vendor material,
# structural is Tier 2 binary leads, unresolved is a channel that answered
# with an error.
OBSERVED, LOCAL, CURATED, STRUCTURAL, UNRESOLVED = (
    "observed", "local", "curated", "structural", "unresolved")


def load(name: str, key: str | None = None):
    path = ROOT / "tests" / name
    if not path.exists():
        return {}
    data = json.load(open(path))
    return data.get(key, {}) if key else data


def kind_of(rec: dict, contract: dict) -> str | None:
    kind = rec.get("kind") or (rec.get("http_probe") or {}).get("kind")
    if kind in ("query", "action", "action-only"):
        kind = "Action" if kind.startswith("action") else "Query"
    if not kind and contract:
        if contract.get("queries") and contract.get("executes"):
            kind = "Dual"
        elif contract.get("queries"):
            kind = "Query"
        elif contract.get("executes"):
            kind = "Action"
    return kind


def shape_result(shape: dict, contract: dict, observed: str | None) -> str:
    r = shape.get("returns", {})
    if r.get("attested"):
        return r["attested"][0]
    if r.get("executed_in"):
        return "nothing"
    if contract.get("executes") and not contract.get("queries"):
        return "nothing"
    return r.get("observed_bare") or observed or "unknown"


def contracts_for(name: str, rec: dict, ctx, shapes: dict, catalog: dict,
                  probed: dict | None, executed) -> list[dict]:
    contract = rec.get("contract") or {}
    ret = ctx.rtypes.get(name) or {}
    observed = ret.get("observed_type")
    rows: list[dict] = []
    seen: set[str] = set()

    def add(call, result, mode, source, cls):
        key = (call, mode)
        if key in seen:
            return
        seen.add(key)
        rows.append({"call": call, "result": result, "mode": mode,
                     "source": source, "sourceClass": cls})

    http = rec.get("http_probe") or {}
    if observed:
        add(name, observed, "HTTP query", "HTTP observed", OBSERVED)
    elif http.get("status") == "exists" and http.get("kind") == "action":
        add(name, "nothing", "Action", "HTTP existence sweep", OBSERVED)
    elif http.get("status") and http.get("status") != "exists":
        add(name, "unknown", "HTTP", f"HTTP {http['status']}", UNRESOLVED)

    for shape_name, shape in shapes.items():
        example = (shape.get("snippets") or [{}])[0].get("snippet") or f"{name} {shape_name}"
        r = shape.get("returns", {})
        if r.get("executed_in"):
            src, cls = "Executed locally", LOCAL
        else:
            src, cls = "Vendor script", CURATED
        mode = "Action" if contract.get("executes") and not r.get("attested") else "Query"
        add(example, shape_result(shape, contract, observed), mode, src, cls)

    for param in catalog.get("documented_parameters", []):
        add(f"{name} '{param}'", "nothing" if contract.get("executes") else (observed or "unknown"),
            "Action" if contract.get("executes") else "Query", "Vendor catalog", CURATED)

    if probed:
        for form in probed.get("recognized_tokens", []):
            for tok in form:
                add(f"{name} {tok}", observed or "recognized", "Query",
                    "HTTP tail prober", LOCAL)

    if executed:
        forms = executed.get("forms") if isinstance(executed, dict) else None
        for form in (forms or []):
            call = form.get("form") if isinstance(form, dict) else str(form)
            if call:
                add(call, "nothing", "Action", "Executed locally", LOCAL)

    if not rows and contract:
        if contract.get("queries"):
            add(name, "unknown", "Query", "Structural candidate", STRUCTURAL)
        if contract.get("executes"):
            add(f"{name} <value>", "nothing", "Action", "Structural candidate", STRUCTURAL)
    return rows


def note_for(rec: dict, assessment: dict) -> str:
    if rec.get("note"):
        return rec["note"]
    if rec.get("evidence"):
        return rec["evidence"][0]
    dims = assessment.get("dimensions") or {}
    settled = [k.replace("_", " ") for k, v in dims.items() if v == "settled"]
    open_ = [k.replace("_", " ") for k, v in dims.items() if v == "open"]
    parts = []
    if settled:
        parts.append("settled: " + ", ".join(settled))
    if open_:
        parts.append("open: " + ", ".join(open_))
    if rec.get("blocked"):
        parts.append("blocked (hardware or context)")
    return "; ".join(parts).capitalize() if parts else "No behavior evidence recorded."


def returns_for(name: str, rec: dict, ctx) -> str:
    ret = ctx.rtypes.get(name) or {}
    if ret.get("observed_type"):
        sample = next(iter((ret.get("samples") or {}).values()), None)
        return f"{ret['observed_type']} · {sample}" if sample is not None else ret["observed_type"]
    http = rec.get("http_probe") or {}
    if http.get("kind") == "action":
        return "action-only"
    if http.get("status") and http["status"] != "exists":
        return f"HTTP {http['status']}"
    return "not swept"


def examples_for(name: str, rec: dict, corpus: list[dict], limit: int) -> list[dict]:
    out = []
    if rec.get("example"):
        out.append({"label": "Store", "code": rec["example"]})
    for s in pick_examples(corpus, name, limit):
        origin = (s.get("origins") or [""])[0]
        label = origin.rsplit("/", 1)[-1].split("@")[0].removesuffix(" mapping.xml")[:28]
        label = label or ", ".join(s["sources"])
        if any(e["code"] == s["script"] or e["label"] == label for e in out):
            continue
        out.append({"label": label, "code": s["script"]})
        if len(out) >= limit:
            break
    return out


def record_for(name: str, rec: dict, ctx, corpus, shapes_art, argforms, execforms, vt) -> dict:
    rec = joined_view(name, rec)
    contract = rec.get("contract") or {}
    catalog = ctx.catalog_actions.get(name) or {}
    assessment = assess(name, rec, ctx)
    status = rec.get("test_status") or "Untested"
    cls, label = SIGNAL.get(status, SIGNAL["Untested"])
    if rec.get("blocked") and status == "Untested":
        cls, label = "caveat", "Blocked"
    table = rec.get("verb_table") or {}
    history = rec.get("history") or {}
    module = rec.get("module") or {}
    description = rec.get("description") or catalog.get("text") or ""
    return {
        "name": name,
        "kind": kind_of(rec, contract) or "Action",
        "section": rec.get("section") or "Unassigned",
        "description": description,
        "contracts": contracts_for(name, rec, ctx, shapes_art.get(name, {}), catalog,
                                   argforms.get(name), execforms.get(name)),
        "examples": examples_for(name, rec, corpus, 4),
        "surfaces": rec.get("surfaces") or [],
        "status": cls,
        "statusLabel": label,
        "note": note_for(rec, assessment),
        "returns": returns_for(name, rec, ctx),
        "aliases": ", ".join(rec.get("aliases") or []) or "None",
        "id": str(table.get("id", "—")),
        "category": table.get("category") or "uncategorized",
        "categoryBuild": (vt.get("summary") or {}).get("build", "unknown"),
        "contract": contract.get("class") or "—",
        "evidence": (rec.get("evidence") or ["No behavior evidence"])[0],
        "tier": rec.get("tier") or "unknown",
        "official": bool(rec.get("official")),
        "dimensions": assessment.get("dimensions") or {},
        "complete": bool(assessment.get("complete")),
        "firstSampled": history.get("first_sampled_in") or "—",
        "sampledBuilds": history.get("present_in_samples") or [],
        "module": module.get("name") or "—",
        "moduleBuild": module.get("build") or "",
        "hidden": bool(table.get("editor_hidden")),
        "documented": bool(rec.get("description")),
    }


def render(out: Path) -> tuple[int, str]:
    ctx = load_context()
    corpus = load("vdjscript-corpus.json", "snippets")
    shapes_art = load("attested-tails.json", "shapes")
    argforms = load("verb-arg-forms.json", "verbs")
    execforms = load("verb-execute-forms.json", "verbs")
    vt = load("verb-table.json")
    records = [record_for(n, r, ctx, corpus, shapes_art, argforms, execforms, vt)
               for n, r in sorted(ctx.canon.items(), key=lambda kv: kv[0].lower())]
    payload = json.dumps(records, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    stamp = build_stamp()
    build = (vt.get("summary") or {}).get("build", "unknown")
    html = TEMPLATE.read_text()
    for token in ("__RECORDS__", "__VERB_COUNT__", "__BUILD__", "__STAMP__", "__RENDERED__"):
        if token not in html:
            sys.exit(f"template is missing placeholder {token}")
    html = (html.replace("__RECORDS__", payload)
                .replace("__VERB_COUNT__", f"{len(records):,}")
                .replace("__BUILD__", build)
                .replace("__STAMP__", stamp)
                .replace("__RENDERED__", dt.date.today().isoformat()))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    shutil.copyfile(LOGO, out.parent / LOGO.name)
    return len(records), stamp


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args(argv)
    n, stamp = render(args.out)
    print(f"{args.out.relative_to(ROOT) if args.out.is_relative_to(ROOT) else args.out}: "
          f"{n} records rendered from {stamp}")


if __name__ == "__main__":
    main()
