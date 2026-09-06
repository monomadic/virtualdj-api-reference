#!/usr/bin/env python3
"""Cross-corpus topic search: one question, every source.

An agent arriving at a task asks "how do I do samplers", not "what does
sampler_pad return". This aggregates, for one topic term, the things that answer
that question together:

  - verbs from the record store (by section, name, or description)
  - native effects from the FX catalog
  - skin/pad XML elements from the inventory
  - REAL example files that use the matched verbs/elements (grep, so the hit is
    working code, not a claim)
  - topical docs
  - local-test quirks and undocumented candidates

Everything is derived from existing structure — verb `section`, inventory
`families`, and grep — so nothing needs hand-tagging to be reachable. Output is a
stdout report (or --format=json); no topic pages are written to disk.

Usage:
    python3 tools/topic.py <term> [--format=json] [--limit=N]
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERBS = ROOT / "docs" / "vdjscript-verbs.json"
FX = ROOT / "tests" / "fx-introspection-dump.json"
XML = ROOT / "docs" / "skin-xml-inventory.json"
TRACKER = ROOT / "docs" / "VDJScript Local Test Tracker.md"
CANDIDATES = ROOT / "docs" / "Undocumented VDJScript Candidates.md"
TAGS = ROOT / "docs" / "topic-tags.json"
MODULES = ROOT / "tests" / "action-modules-9246.json"
# Corpora to grep for real usage. Kept to authored/curated + built-in examples.
CORPORA = ["examples", "tests"]
# `tests/*.json` are the evidence artifacts — the verb table, the sweeps, the
# corpus. A verb name appears in them because it exists, not because anything
# uses it, so they crowd out the working examples this section is for.
ARTIFACT_RE = re.compile(r"^tests/[^/]+\.json$")


def load(path: Path, key: str | None = None):
    data = json.loads(path.read_text())
    if key and isinstance(data, dict) and key in data:
        data = data[key]
    return data


def tags() -> dict:
    if not TAGS.exists():
        return {"aliases": {}, "topics": {}}
    return json.loads(TAGS.read_text())


def normalize(term: str) -> tuple[str, str | None]:
    """(topic to search, the alias it came from). Multi-word terms are folded
    through the alias table, so `color fx` reaches `colorfx`."""
    t = term.strip().lower()
    aliases = tags().get("aliases", {})
    for candidate in (t, t.replace(" ", "")):
        if candidate in aliases:
            return aliases[candidate], term
    if t not in tags().get("topics", {}) and t.replace(" ", "") in tags().get("topics", {}):
        return t.replace(" ", ""), term
    return t, None


def tagged(term: str) -> dict:
    """The hand-maintained members of a topic, for items no derivation reaches."""
    return tags().get("topics", {}).get(term, {})


def module_verbs(term: str) -> set[str]:
    """Verbs whose source module names the topic.

    Derived, so it needs no tag. It matters most for the verbs the section
    backfill could not reach: a module only donated its section where it graded
    `clean`, leaving most module-known verbs still unsectioned — and those are
    invisible to a section match but not to this one.
    """
    if not MODULES.exists():
        return set()
    try:
        modules = json.loads(MODULES.read_text())["modules"]
    except (KeyError, json.JSONDecodeError):
        return set()
    t = term.lower()
    return {v for module, verbs in modules.items() if t in module.lower() for v in verbs}


def verb_records() -> dict:
    d = load(VERBS)
    recs = d["verbs"] if isinstance(d, dict) and "verbs" in d else d
    return {k: v for k, v in recs.items() if isinstance(v, dict) and "name" in v}


def match_verbs(term: str, recs: dict, tag_names: list[str] | None = None) -> list[dict]:
    t = term.lower()
    wanted = set(tag_names or [])
    hits = []
    for r in recs.values():
        if r["name"] in wanted:
            # A tag is the strongest signal there is: someone decided this verb
            # belongs to this topic when no derivation could find it.
            hits.append((-1, dict(r, matched_by="tag")))
            continue
        section = (r.get("section") or "").lower()
        hay = f"{r['name']} {r.get('description','')}".lower()
        # section match is the strongest signal; then name; then description
        if t in section:
            score = 0
        elif t in r["name"].lower():
            score = 1
        elif t in hay:
            score = 2
        else:
            continue
        hits.append((score, dict(r, matched_by="name")))
    hits.sort(key=lambda s: (s[0], s[1]["name"]))
    return [r for _, r in hits]


def match_effects(term: str) -> list[dict]:
    if not FX.exists():
        return []
    t = term.lower()
    out = []
    for e in load(FX, "effects"):
        blob = json.dumps(e).lower()
        if t in blob:
            out.append(e)
    return sorted(out, key=lambda e: e["effect"].lower())


def match_elements(term: str, tag_names: list[str] | None = None) -> list[tuple[str, str, dict]]:
    if not XML.exists():
        return []
    t = term.lower()
    wanted = set(tag_names or [])
    out = []
    for fam_name, fam in load(XML, "families").items():
        for el_name, el in (fam.get("elements") or {}).items():
            if el_name in wanted:
                out.append((fam_name, el_name, dict(el, matched_by="tag")))
            elif t in el_name.lower() or t in fam_name.lower():
                out.append((fam_name, el_name, dict(el, matched_by="name")))
    return out


def grep_files(needles: list[str]) -> dict[str, set[str]]:
    """file -> set of needles found in it, via ripgrep over the corpora."""
    if not needles:
        return {}
    found: dict[str, set[str]] = {}
    # one rg call with an alternation is far cheaper than one per needle.
    # Word boundaries so `effect_slider` does not match inside
    # `effect_slider_activate` — we want usage of THIS verb, not a longer one
    # that happens to share a prefix.
    pattern = "|".join(rf"\b{re.escape(n)}\b" for n in needles)
    try:
        res = subprocess.run(
            ["rg", "--no-heading", "--line-number", "-o", "-e", pattern,
             *CORPORA],
            cwd=ROOT, capture_output=True, text=True, timeout=30)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return {}
    for line in res.stdout.splitlines():
        # path:line:match
        parts = line.split(":", 2)
        if len(parts) < 3:
            continue
        path, _, match = parts
        found.setdefault(path, set()).add(match)
    return found


def match_docs(term: str, tag_docs: list[str] | None = None) -> list[str]:
    t = term.lower()
    out = list(tag_docs or [])
    for p in sorted((ROOT / "docs").glob("*.md")):
        rel = str(p.relative_to(ROOT))
        if t in p.stem.lower() and rel not in out:
            out.append(rel)
    return out


def grep_md(path: Path, term: str, limit: int = 4) -> list[str]:
    if not path.exists():
        return []
    t = term.lower()
    rows = []
    for line in path.read_text().splitlines():
        if line.startswith("|") and t in line.lower():
            # first backticked token is the verb/candidate name
            m = re.search(r"`([^`]+)`", line)
            if m:
                rows.append(m.group(1).split()[0])
    seen, out = set(), []
    for r in rows:
        if r not in seen:
            seen.add(r)
            out.append(r)
        if len(out) >= limit:
            break
    return out


def gather(term: str, limit: int) -> dict:
    topic, via_alias = normalize(term)
    tag = tagged(topic)
    recs = verb_records()
    verbs = match_verbs(topic, recs, (tag.get("verbs") or []) + sorted(module_verbs(topic)))
    effects = match_effects(topic)
    elements = match_elements(topic, tag.get("elements"))

    # grep the corpora for the matched verb names + element names, so the
    # example files we surface are ones that actually use this topic.
    needles = [v["name"] for v in verbs[:40]] + [e for _, e, _ in elements[:20]]
    files = grep_files(needles)
    # Quarantine/ holds personal/local-authorship examples (see
    # examples/Mappers/README.md, examples/Pads/README.md) — real usage, but
    # not official or curated, so they rank behind everything else instead of
    # crowding out reference examples.
    ranked_files = sorted(
        ((path, hits) for path, hits in files.items() if not ARTIFACT_RE.match(path)),
        key=lambda kv: ("/Quarantine/" in kv[0], -len(kv[1]), kv[0]),
    )

    return {
        "topic": topic,
        "searched_as": term if via_alias else None,
        "tag_note": tag.get("why"),
        "verbs": verbs,
        "effects": effects,
        "elements": elements,
        "example_files": ranked_files,
        "docs": match_docs(topic, tag.get("docs")),
        "tracker_quirks": grep_md(TRACKER, topic),
        "candidates": grep_md(CANDIDATES, topic),
        "limit": limit,
    }


def report(g: dict) -> None:
    term = g["topic"]
    lim = g["limit"]
    print(f"TOPIC: {term}")
    if g.get("searched_as"):
        print(f"  (searched as {g['searched_as']!r})")
    if g.get("tag_note"):
        print(f"  tagged: {g['tag_note']}")
    print()

    verbs = g["verbs"]
    if verbs:
        print(f"VERBS ({len(verbs)})  — just get-verb <name> for detail")
        for r in verbs[:lim]:
            sec = f"[{r.get('section')}]" if r.get("section") else ""
            st = r.get("test_status", "Untested")
            flag = f" ✓{st}" if st in {"Pass", "Partial", "Fail"} else ""
            desc = (r.get("description") or "").split(". ")[0][:70]
            mark = "+" if r.get("matched_by") == "tag" else " "
            print(f" {mark}{r['name']:<26} {sec:<20}{flag}  {desc}")
        if len(verbs) > lim:
            print(f"  … {len(verbs)-lim} more — just find-verbs {term}")
        print()

    if g["effects"]:
        names = [e["effect"] for e in g["effects"]]
        print(f"EFFECTS ({len(names)})  — just get-fx <name>")
        print("  " + ", ".join(names[:20]))
        print()

    if g["elements"]:
        print(f"SKIN/XML ELEMENTS ({len(g['elements'])})  — just get-xml-element <name>")
        for fam, el, info in g["elements"][:lim]:
            uses = info.get("uses", "?")
            doc = "documented" if info.get("documented") else "UNDOCUMENTED"
            mark = "+" if info.get("matched_by") == "tag" else " "
            print(f" {mark}<{el}>  ({fam}, {uses} uses, {doc})")
        print()

    if g["example_files"]:
        print(f"EXAMPLE FILES ({len(g['example_files'])})  — real usage, grep-verified")
        for path, needles in g["example_files"][:lim]:
            shown = ", ".join(sorted(needles)[:5])
            more = f" +{len(needles)-5}" if len(needles) > 5 else ""
            tag = "  [quarantined: personal/local]" if "/Quarantine/" in path else ""
            print(f"  {path}{tag}")
            print(f"      uses: {shown}{more}")
        if len(g["example_files"]) > lim:
            print(f"  … {len(g['example_files'])-lim} more files")
        print()

    if g["docs"]:
        print("DOCS")
        for d in g["docs"]:
            print(f"  {d}")
        print()

    if g["tracker_quirks"]:
        print("LOCAL-TEST QUIRKS  — just get-verb <name> for the evidence")
        print("  " + ", ".join(g["tracker_quirks"]))
        print()

    if g["candidates"]:
        print("UNDOCUMENTED CANDIDATES  — discovery-only, unproven")
        print("  " + ", ".join(g["candidates"]))
        print()

    if not any([verbs, g["effects"], g["elements"], g["example_files"], g["docs"]]):
        print("no matches. Try a broader term, or `just find-verbs "
              f"{term}` / `rg -i {term} docs/`.")


def selfcheck() -> None:
    """Cross-store smoke test: topic.py reads four other artifacts, so a schema
    change upstream can break it silently. Assert the pipeline runs and the
    known-rich `sampler` topic still resolves verbs and example files."""
    errors = []
    for path in (VERBS, XML):
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if not errors:
        try:
            g = gather("sampler", 8)
            if not g["verbs"]:
                errors.append("topic 'sampler' returned no verbs (store schema drift?)")
            if not g["example_files"]:
                errors.append("topic 'sampler' returned no example files (grep broken?)")
        except Exception as e:  # noqa: BLE001
            errors.append(f"gather('sampler') raised {type(e).__name__}: {e}")
    errors += check_tags()
    if errors:
        print("topic check FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    tag = tags()
    print(f"topic check passed: cross-corpus aggregation runs, 'sampler' resolves, "
          f"{len(tag['topics'])} tagged topics and {len(tag['aliases'])} aliases resolve")


def check_tags() -> list[str]:
    """Every tagged name must exist. A tag that names nothing is worse than no
    tag: it silently promises a topic reaches something it does not."""
    tag = tags()
    if not tag["topics"]:
        return [f"{TAGS.relative_to(ROOT)} is missing or empty"]
    errors = []
    known_verbs = set(verb_records())
    known_elements = {el for fam in load(XML, "families").values()
                      for el in (fam.get("elements") or {})} if XML.exists() else set()
    for name, rec in tag["topics"].items():
        for verb in rec.get("verbs", []):
            if verb not in known_verbs:
                errors.append(f"topic {name!r} tags verb {verb!r}, which is not in the store")
        for el in rec.get("elements", []):
            if el not in known_elements:
                errors.append(f"topic {name!r} tags element {el!r}, "
                              "which is not in the XML inventory")
        for doc in rec.get("docs", []):
            if not (ROOT / doc).exists():
                errors.append(f"topic {name!r} tags doc {doc!r}, which does not exist")
        if not rec.get("why"):
            errors.append(f"topic {name!r} has no `why` — a tag without a reason is unreviewable")
    for alias, target in tag["aliases"].items():
        if target not in tag["topics"]:
            errors.append(f"alias {alias!r} points at undefined topic {target!r}")
    return errors


def main(argv):
    if argv and argv[0] == "check":
        selfcheck()
        return
    args = [a for a in argv if not a.startswith("--")]
    opts = {a[2:].split("=")[0]: (a.split("=", 1)[1] if "=" in a else True)
            for a in argv if a.startswith("--")}
    if not args:
        sys.exit("usage: topic.py <term> [--format=json] [--limit=N]")
    term = " ".join(args)
    limit = int(opts.get("limit", 8))
    g = gather(term, limit)
    if opts.get("format") == "json":
        # sets are not JSON-serializable; render example files as name lists
        g = dict(g)
        g["example_files"] = [{"path": p, "uses": sorted(n)}
                              for p, n in g["example_files"]]
        print(json.dumps(g, indent=1, ensure_ascii=False))
    else:
        report(g)


if __name__ == "__main__":
    main(sys.argv[1:])
