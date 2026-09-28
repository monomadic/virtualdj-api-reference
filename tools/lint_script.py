#!/usr/bin/env python3
"""Lint VDJScript statically, against the rules this repo has settled.

VirtualDJ never reports a syntax error: wrong script silently does something
else. This catches the forms the reference has shown go wrong, and every rule
names the evidence it rests on (docs/Evidence Standards.md). Nothing here runs
script; `vdj_query` / `just vdj-query` is how a construct is actually verified.

Levels:
  error    the form is broken on the evidence (unterminated quote, empty
           branch, a name the verb table disproves). Always fails the run.
  warning  the form is legal but its tested behaviour is almost never what was
           meant (`&&` in front of an action, a string stored in a variable).
           Fails the run with --strict.
  note     legal and sometimes intended, but a known trap (a chain trailing a
           ternary belongs to the false branch). Never fails the run.

Scripts come from a string (--script), or from XML files, whose action/query
attributes and pad bodies are extracted with their line numbers.

Usage:
  python3 tools/lint_script.py --script "cond && play"
  python3 tools/lint_script.py --script "volume ? a : b" --context query
  python3 tools/lint_script.py --xml page.xml skin.xml
  python3 tools/lint_script.py --repo        # this repo's pads, skins, mappers
  python3 tools/lint_script.py --corpus      # vendor corpus, summarised by rule
"""

from __future__ import annotations

import argparse
import difflib
import html
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERB_TABLE = ROOT / "tests" / "verb-table.json"
STORE = ROOT / "docs" / "vdjscript-verbs.json"
RETURN_TYPES = ROOT / "tests" / "verb-return-types.json"
CONTRACTS = ROOT / "tests" / "action-contracts.json"
CORPUS = ROOT / "tests" / "vdjscript-corpus.json"

GRAMMAR = "docs/VDJScript Grammar.md"
TESTED_RULES = "docs/VirtualDJ Reference.md §Tested Grammar Rules (Local test, pad, b9482)"

# Statement prefixes that are parser keywords, not verbs. `deck` takes one target
# token and `not` none; the verb after them is checked. `effect`, `sampler` and
# `get` take their own sub-keywords (`effect slider 3`, `sampler 2 play`,
# `get position`), which are not verbs, so the rest of the statement is skipped.
# Source: every non-verb statement head in the vendor corpus (tests/vdjscript-corpus.json).
WRAPPERS = {"deck": 1, "not": 0}
OPAQUE_HEADS = {"effect", "sampler", "get"}
# `GRAMMAR` §Deck and scope wrappers: the nine wiki targets plus `master`; any
# integer is accepted (`deck 99` silently), an unknown word errors.
DECK_TARGETS = {"left", "right", "leftvideo", "rightvideo", "all", "default", "active", "master"}
# Statement suffixes, not verbs (`GRAMMAR` §Deck and scope wrappers).
SUFFIXES = {"while_pressed"}
# Transport verbs that ignore a backtick-computed argument (`TESTED_RULES`).
IGNORE_COMPUTED = {"loop", "beatjump", "phrase_sync"}
# Skin define placeholders (`[ACTION]`, `[LEFTDECK]`) are substituted before any
# script runs, so they are not verbs or deck targets.
PLACEHOLDER = re.compile(r"\[[A-Za-z0-9_]+\]$")
COMMENT_MARKERS = ("//", "/*", "--", "#", ";")
NUMBER = re.compile(r"[+-]?(\d+\.?\d*|\.\d+)(ms|bt|%)?$", re.IGNORECASE)
OPS = ("&&", "&", "?", ":", "(", ")")


@dataclass
class Tok:
    kind: str  # W word, Q quoted, BT backtick, OP operator
    text: str

    @property
    def value(self) -> str:
        return self.text[1:-1] if self.kind in ("Q", "BT") else self.text


@dataclass
class Finding:
    level: str
    rule: str
    message: str
    evidence: str

    def render(self, where: str = "") -> str:
        prefix = f"{where}: " if where else ""
        return f"{self.level.upper():7} {prefix}{self.message} [{self.rule}; {self.evidence}]"


class Vocabulary:
    def __init__(self) -> None:
        table = json.loads(VERB_TABLE.read_text())
        self.verbs = set(table["verbs"])
        self.stamp = (f"verb table of build {table['summary']['build']} "
                      f"({table['summary']['arch']}, extracted {table['summary']['extracted']})")
        store = json.loads(STORE.read_text())["verbs"]
        self.disproved = {n for n, r in store.items() if r.get("test_status") == "Disproved"}
        self.known = (self.verbs | {n.lower() for n in store}) - self.disproved
        self.kind = {n: r.get("kind") for n, r in store.items()}
        types = json.loads(RETURN_TYPES.read_text())["verbs"]
        contracts = json.loads(CONTRACTS.read_text())["verbs"]
        # The sweep read each verb at rest. For a query-only verb, or a slider (no
        # slider is ever boolean-true), that reading is its truth; a dual verb such
        # as effect_select may turn true in a state the sweep did not reach.
        self.traps, self.rest_traps = set(), set()
        for n, r in types.items():
            if r.get("truthiness_trap"):
                firm = self.kind.get(n) == "Query" or "Slider" in contracts.get(n, {}).get("base", "")
                (self.traps if firm else self.rest_traps).add(n)


def closing(script: str, i: int) -> int:
    """Index of the delimiter closing the quote or backtick opened at i, or -1.

    Vendor scripts nest them: `param_equal '`pitch_slider`' 0.5` puts a backtick
    segment inside a quote, and that segment may hold quotes of its own.
    """
    opener = script[i]
    j = i + 1
    while j < len(script):
        ch = script[j]
        if ch == opener:
            return j
        if ch == "`" or (opener == "`" and ch in "'\""):
            end = closing(script, j)
            if end == -1:
                return -1
            j = end
        j += 1
    return -1


def tokenize(script: str) -> tuple[list[Tok], list[Finding]]:
    toks: list[Tok] = []
    i, n = 0, len(script)
    while i < n:
        ch = script[i]
        if ch.isspace():
            i += 1
            continue
        if ch in "'\"`":
            j = closing(script, i)
            if j == -1:
                what = "backtick" if ch == "`" else "quote"
                return toks, [Finding("error", "unterminated", f"unterminated {what}: {script[i:i + 30]!r}",
                                      "a statement cannot end inside a quoted value")]
            toks.append(Tok("BT" if ch == "`" else "Q", script[i:j + 1]))
            i = j + 1
            continue
        op = next((o for o in OPS if script.startswith(o, i)), None)
        if op:
            toks.append(Tok("OP", op))
            i += len(op)
            continue
        j = i
        while j < n and not script[j].isspace() and script[j] not in "&?:()'\"`":
            j += 1
        toks.append(Tok("W", script[i:j]))
        i = j
    return toks, []


def statements(toks: list[Tok]):
    """Yield (statement tokens, separator before it, separator after it)."""
    cur: list[Tok] = []
    before = None
    for t in toks:
        if t.kind == "OP":
            yield cur, before, t.text
            cur, before = [], t.text
        else:
            cur.append(t)
    yield cur, before, None


def strip_wrappers(stmt: list[Tok], vocab: Vocabulary, out: list[Finding]) -> list[Tok]:
    """Drop `deck <target>` / `not` prefixes, checking deck targets on the way."""
    while stmt and stmt[0].kind == "W" and stmt[0].text.lower() in WRAPPERS:
        head = stmt[0].text.lower()
        skip = 1 + WRAPPERS[head]
        if head == "deck" and len(stmt) > 1:
            target = stmt[1].value.lower()
            if stmt[1].kind == "W" and not target.isdigit() and target not in DECK_TARGETS \
                    and not PLACEHOLDER.match(target) \
                    and not re.fullmatch(r"mixer\d+", target):
                out.append(Finding("warning", "deck-target", f"unknown deck target {stmt[1].text!r}",
                                   f"{GRAMMAR} §Deck and scope wrappers: an unknown target errors (HTTP)"))
        stmt = stmt[skip:]
    return stmt


def lint_script(script: str, context: str, vocab: Vocabulary) -> list[Finding]:
    toks, out = tokenize(script)
    if out:
        return out

    # Parentheses (separate threads) must balance.
    depth = 0
    for t in toks:
        if t.kind == "OP" and t.text in "()":
            depth += 1 if t.text == "(" else -1
            if depth < 0:
                return [Finding("error", "parens", "`)` closes no `(`", f"{GRAMMAR} §Deck and scope wrappers")]
    if depth:
        return [Finding("error", "parens", "unclosed `(`", f"{GRAMMAR} §Deck and scope wrappers")]

    for t in toks:
        if t.kind == "W" and (t.text.startswith(COMMENT_MARKERS) or ";" in t.text):
            out.append(Finding("warning", "comment", f"{t.text!r} is not a comment: it discards the rest of the statement",
                               f"{GRAMMAR} §There is no comment syntax (HTTP)"))
            break

    for i, t in enumerate(toks):
        if t.kind == "OP" and t.text in "?:":
            nxt = toks[i + 1] if i + 1 < len(toks) else None
            if nxt is None or (nxt.kind == "OP" and nxt.text != "("):
                side = "true" if t.text == "?" else "false"
                out.append(Finding("error", "empty-branch", f"empty {side} branch",
                                   f"{GRAMMAR} §Conditionals: an empty branch errors when taken (HTTP)"))

    for stmt, before, after in statements(toks):
        if not stmt:
            continue
        core = strip_wrappers(stmt, vocab, out)
        if not core:
            continue
        head = core[0]
        if before in ("?", ":") and (head.kind == "Q" or (head.kind == "W" and NUMBER.match(head.text))):
            out.append(Finding("warning", "literal-branch", f"branch {head.text} is a literal, not a verb",
                               f"{GRAMMAR} §Conditionals: `on ? 'A' : 'B'` and `on ? 1 : 2` error (HTTP)"))
            continue
        if head.kind != "W":
            continue
        name = head.text.lower()
        args = [t for t in core[1:] if not (t.kind == "W" and t.text.lower() in SUFFIXES)]
        if name in OPAQUE_HEADS or name in SUFFIXES or PLACEHOLDER.match(name):
            continue
        if name in vocab.disproved:
            out.append(Finding("error", "disproved", f"{head.text!r} is not a verb",
                               f"verb store: test_status=Disproved (`just verb {name}`)"))
        elif name not in vocab.known:
            close = difflib.get_close_matches(name, vocab.verbs, n=1)
            hint = f" (closest: {close[0]!r})" if close else ""
            out.append(Finding("warning", "unknown-verb", f"{head.text!r} is not in the verb table{hint}",
                               f"{vocab.stamp}; a newer build may add it"))

        # Tested per-verb argument rules.
        if name == "beatjump" and args and args[0].kind == "W" and NUMBER.match(args[0].text) \
                and args[0].text[0] not in "+-":
            out.append(Finding("warning", "beatjump-unsigned", f"`beatjump {args[0].text}` is a no-op; sign it: "
                               f"`beatjump +{args[0].text}`", TESTED_RULES))
        if name in IGNORE_COMPUTED and any(a.kind == "BT" for a in args):
            out.append(Finding("warning", "computed-arg", f"`{name}` ignores a backtick-computed argument; "
                               "branch to literals or use param chaining", TESTED_RULES))
        if name == "sampler_loaded" and len(args) > 1 and args[1].value.lower() == "auto":
            out.append(Finding("warning", "sampler-loaded-auto", "`sampler_loaded <n> 'auto'` is not page-aware; "
                               "use an absolute slot guard", "verb store: sampler_loaded, Partial, local_test"))
        if name == "set" and len(args) > 1:
            value = args[1]
            if value.kind == "Q" and not NUMBER.match(value.value):
                out.append(Finding("warning", "string-variable", f"storing the string {value.text} makes the "
                                   "variable unreadable, and var_equal matches anything; store a number",
                                   f"{GRAMMAR} §Variables hold numbers, not strings (HTTP)"))
            elif value.kind == "W" and value.text.lower() in ("true", "false"):
                out.append(Finding("warning", "string-variable", f"`{value.text}` stores nothing; use on/off or 1/0",
                                   f"{GRAMMAR} §Variables hold numbers, not strings (HTTP)"))
        if context == "query" and name == "filter_selectcolorfx":
            out.append(Finding("note", "query-selector", "this repo reads the selected ColorFX with "
                               "`param_equal `filter_label 'name'` …` rather than a selector verb in a query",
                               "docs/VirtualDJ Reference.md convention; the vendor corpus does use this form"))

        # A bare condition whose value reads true while the verb is false.
        if after == "?" and not args and name in vocab.traps | vocab.rest_traps:
            firm = name in vocab.traps
            out.append(Finding("warning" if firm else "note", "truthiness-trap",
                               f"`{name}` reports a value but read false as a condition"
                               + ("" if firm else " at rest (it may turn true in another state)")
                               + "; compare explicitly (param_bigger, var_equal)",
                               f"{GRAMMAR} §A verb's value and its truth; tests/verb-return-types.json (HTTP)"))

    # `&&` never guards. In a query it is AND over the reported value, which is
    # fine on its own, but it never reaches into a following conditional.
    for i, t in enumerate(toks):
        if t.kind != "OP" or t.text != "&&":
            continue
        rest = toks[i + 1:]
        nxt = next((r for r in rest if r.kind == "OP" and r.text in ("&", "&&", "?", ":", ")")), None)
        if nxt is not None and nxt.text == "?":
            out.append(Finding("warning", "and-condition", "`a && b ? …` tests only `b`; `a` does not take part",
                               f"{GRAMMAR} §Boolean composition with `&&` (Button Editor parse, HTTP)"))
        elif context == "action":
            out.append(Finding("warning", "and-guard", "`&&` does not guard an action: both sides always run; "
                               "use `cond ? action : nothing`", f"{GRAMMAR} §Boolean composition with `&&` (HTTP)"))

    # A chain after a ternary's `:` runs only on the false side.
    depth, colon_at = 0, set()
    for t in toks:
        if t.kind != "OP":
            continue
        if t.text == "(":
            depth += 1
        elif t.text == ")":
            colon_at.discard(depth)
            depth -= 1
        elif t.text == ":":
            colon_at.add(depth)
        elif t.text in ("&", "&&") and depth in colon_at:
            out.append(Finding("note", "trailing-chain", "a chain after a ternary's `:` belongs to the false "
                               "branch; put always-run actions first", f"{GRAMMAR} §Conditionals (Pad)"))
            break

    for t in toks:
        if t.kind == "BT":
            out += lint_script(t.value, "query", vocab)
    return out


# --------------------------------------------------------------------------
# XML extraction
# --------------------------------------------------------------------------

ACTION_ATTRS = {"action", "rightclick", "dblclick"}
QUERY_ATTRS = {"query", "visibility"}
ATTR = re.compile(r"""\b([A-Za-z_][\w.:-]*)\s*=\s*("([^"]*)"|'([^']*)')""")
# Pad bodies are actions: <pad1 …>hot_cue 1</pad1>, <shift_pad1>, <param1>.
PAD_BODY = re.compile(r"<((?:shift_)?pad\d+|param\d+|knob\d*)\b[^>]*>([^<]+)</\1>", re.IGNORECASE)


def xml_scripts(text: str):
    """Yield (line, attribute, context, script) from XML text."""
    def line(at: int) -> int:
        return text.count("\n", 0, at) + 1

    for m in ATTR.finditer(text):
        attr = m.group(1).lower()
        value = html.unescape(m.group(3) if m.group(3) is not None else m.group(4))
        if attr in ACTION_ATTRS:
            yield line(m.start()), attr, "action", value
        elif attr in QUERY_ATTRS:
            yield line(m.start()), attr, "query", value
        else:
            for bt in re.findall(r"`[^`]*`", value):
                yield line(m.start()), attr, "query", bt
    for m in PAD_BODY.finditer(text):
        body = html.unescape(m.group(2)).strip()
        if body:
            yield line(m.start(2)), f"<{m.group(1)}>", "action", body


def display(path: Path) -> Path:
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


# --------------------------------------------------------------------------
# entry points
# --------------------------------------------------------------------------

VENDOR_SOURCES = {"factory", "builtin", "addon", "wiki"}
REPO_GLOBS = [
    "tests/Pads/**/*.xml",
    "examples/Skins/ModularSkeleton/build/*.xml",
    "examples/Skins/GraveRaver/build/*.xml",
    "tests/Skins/**/*.xml",
    "examples/Mappers/Local/*.xml",
    "examples/Mappers/Official-Addons/**/*.xml",
]


def corpus_report(vocab: Vocabulary) -> int:
    """Lint every vendor snippet. Errors here are linter bugs or vendor findings."""
    snippets = json.loads(CORPUS.read_text())["snippets"]
    by_rule: Counter = Counter()
    examples: dict[str, str] = {}
    errors = 0
    for sn in snippets:
        if not VENDOR_SOURCES & set(sn["sources"]):
            continue
        for f in lint_script(sn["script"], "action", vocab):
            by_rule[(f.level, f.rule)] += 1
            examples.setdefault(f.rule, sn["script"][:110])
            errors += f.level == "error"
    for (level, rule), n in sorted(by_rule.items(), key=lambda kv: -kv[1]):
        print(f"{n:6} {level:7} {rule:20} e.g. {examples[rule]}")
    print(f"\nvendor corpus: {errors} error findings")
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--script", help="one VDJScript string")
    src.add_argument("--xml", nargs="+", metavar="FILE", help="lint the scripts inside XML files")
    src.add_argument("--repo", action="store_true", help="lint the scripts in this repo's own pads, skins, mappers")
    src.add_argument("--corpus", action="store_true", help="lint the vendor corpus and summarise by rule")
    parser.add_argument("--context", choices=("action", "query"), default="action",
                        help="for --script: where it runs (default: action)")
    parser.add_argument("--strict", action="store_true", help="warnings fail the run")
    args = parser.parse_args()

    vocab = Vocabulary()
    if args.corpus:
        return corpus_report(vocab)

    if args.repo:
        args.xml = [str(p) for g in REPO_GLOBS for p in sorted(ROOT.glob(g))]

    rendered: list[tuple[str, str]] = []
    if args.script is not None:
        rendered = [(f.level, f.render()) for f in lint_script(args.script, args.context, vocab)]
        scanned = "1 script"
    else:
        count = 0
        for p in args.xml:
            path = Path(p).resolve()
            try:
                text = path.read_text(encoding="utf-8-sig", errors="replace")
            except OSError as exc:
                rendered.append(("error", f"ERROR   {display(path)}: cannot read: {exc.strerror}"))
                continue
            for line, attr, context, script in xml_scripts(text):
                count += 1
                for f in lint_script(script, context, vocab):
                    rendered.append((f.level, f.render(f"{display(path)}:{line} {attr}")))
        scanned = f"{count} scripts in {len(args.xml)} files"

    for _, text in rendered:
        print(text)
    levels = Counter(level for level, _ in rendered)
    failed = levels["error"] or (args.strict and levels["warning"])
    print(f"Script lint {'FAILED' if failed else 'passed'}: {scanned}, {levels['error']} errors, "
          f"{levels['warning']} warnings, {levels['note']} notes")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
