#!/usr/bin/env python3
"""Contract coverage across every verb, computed from the artifacts at read time.

    just coverage
    just coverage --format=json
    just coverage --settled          # the verbs with nothing left open
    just coverage --frontier         # what each dimension is blocked on, by name

`verb-stats` counts the store's own `test_status` field, which answers one
question: has behaviour been confirmed live. That is a quarter of a verb's
calling contract. Task 10 wants four things per verb — what it returns in query
position, what arguments it accepts, what it does in execute position, and
whether any of that has been observed rather than inferred — and each lives in a
different artifact with a different denominator. This joins them.

Three rules the numbers here obey:

- **Denominators are per dimension.** A verb that cannot be queried has no
  return type to establish, so it is `n/a` there, not `open`. Reporting 578
  typed verbs against all 979 canonical names would understate the return-type
  sweep by counting execute-only verbs as gaps.
- **Nothing is read from a stored summary.** Every figure is recounted from the
  artifact's own records, because a stored summary goes stale the moment a probe
  appends to the data without regenerating the header — `verb-arg-forms.json`
  currently ships one that does. Where a summary disagrees with its own records,
  this says so instead of trusting either.
- **"Settled" is a claim about evidence, not about effort.** A probed verb where
  nothing separated from the nonsense controls is `open`, not settled: it means
  the state did not discriminate, which is not the same as the verb having no
  arguments. See docs/Evidence Standards.md.

`assess()` is the single per-verb assessment; `just verb` imports it, so the
one-screen view and the aggregate can never disagree about what "settled"
means. Each open item carries one of five reasons (REASONS) because the reason
decides the next test.

Read-only. Touches no live instance and writes nothing.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verbdb import audit_pool, contract_names, load_store  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "tests"

DIMENSIONS = ("return_type", "arguments", "execute", "behaviour")

# The one state that closes a dimension. `no_known_candidates` (a verb probed
# against nonsense with no candidate token in the binary, the catalog or a
# shipped script) is reported on its own and does NOT close: absence of a
# candidate is not evidence of absence of arguments, so exhaustive absence is
# never claimed. `partial` (execute tokens found, others undiscriminated) and
# `unknown` (no capability row) stay open for the same reason.
CLOSED = {"settled"}

# The execute channel writes to a live instance, so it is deliberately the
# slowest to fill and would otherwise mark every verb incomplete. The read-side
# contract — what it returns, what it accepts, whether behaviour was observed —
# is reported separately for that reason, and is the figure worth quoting.
READ_SIDE = ("return_type", "arguments", "behaviour")


def artifact(name: str, key: str | None = None):
    """A missing artifact is a smaller report, never a crash — several are
    regenerated from a live app or an app bundle that may not be present."""
    path = T / name
    if not path.exists():
        return {} if key else None
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return {} if key else None
    return data.get(key, {}) if key else data


def build_stamp() -> str:
    """The verb table's own stamp, copied rather than recalled — the phrase is
    evidence about one build and must not drift (see CLAUDE.md)."""
    table = artifact("verb-table.json")
    if not table:
        return "build unknown — tests/verb-table.json not extracted"
    s = table["summary"]
    return (f"{s['records']} records / {s['distinct_ids']} distinct verbs on build "
            f"{s['build']} ({s['arch']}, extracted {s['extracted']})")


def cross_check() -> tuple[dict, dict, str]:
    """Documented-vs-probed-vs-attested buckets, plus the confirmations that
    reached a verb through some channel other than the argument prober.

    Preferred live from the app bundle, because the tool carries the
    LOCAL_CONFIRMED / LOCAL_PLACEHOLDERS tables in its own source and those
    change with every probe session — the committed artifact lags them. Falls
    back to the artifact with the source named, so a stale number is never
    presented as a fresh one.
    """
    extra: dict[str, set[str]] = {}
    try:
        from extract_action_catalog import DEFAULT_APP, LANGUAGE, catalog
        from extract_action_catalog import cross_check as live_cross_check
        from extract_action_catalog import extra_confirmations
        extra = extra_confirmations()
        entries = catalog(DEFAULT_APP, LANGUAGE)
        checked = live_cross_check(entries)
        if checked:
            return checked, extra, "live from the app bundle"
    except (ImportError, OSError, KeyError):
        pass
    art = artifact("action-catalog.json")
    if art and art.get("cross_check"):
        return (art["cross_check"], extra,
                "tests/action-catalog.json (app bundle unavailable — may lag)")
    return {}, extra, "unavailable"


# Why an open item is open. Five reasons, and each names a different next
# action, which is the point: "measured but the observable did not
# discriminate" must never be re-run with the same observable.
REASONS = {
    "not_measured":    "not measured",
    "undiscriminated": "measured, but the observable did not discriminate",
    "unavailable":     "required state, surface or hardware unavailable here",
    "conflicting":     "conflicting observations between runs",
    "prose_only":      "evidence exists only in store prose, not in an artifact row",
}

# Worked-out fixtures for frontier verbs, copied from TODO.md so `just verb`
# can name the next test instead of "needs a discriminating state". A hint is
# a pointer to a recipe, not evidence; drop it when the verb closes.
NEXT_TEST_HINTS = {
    "get_time_hour": "long-track fixture (TODO 10b/10d): 2h05m generated track, playhead "
                     "1h10m separates elapsed/remain/total; ~3,700 s at +12% separates absolute",
    "get_time_hour_absolute": "same long-track fixture as get_time_hour",
}


class Context:
    """Every artifact the assessment reads, loaded once. `just coverage` walks
    the whole store with it; `just verb` asks about one name."""

    def __init__(self):
        self.store = load_store()
        self.canon = {n: r for n, r in self.store.items() if r.get("tier") != "alias"}
        self.contracts = artifact("action-contracts.json", "verbs")
        self.rtypes = artifact("verb-return-types.json", "verbs")
        self.argforms = artifact("verb-arg-forms.json", "verbs")
        af_summary = (artifact("verb-arg-forms.json") or {}).get("summary", {})
        self.arg_fixtures = af_summary.get("fixtures", [])
        self.disputed = set(af_summary.get("disputed_verbs", []))
        self.execforms = artifact("verb-execute-forms.json", "verbs")
        self.positions = artifact("verb-arg-positions.json", "verbs")
        self.bpm_transition = artifact("bpm-transition-forms.json") or {}
        self.fx_dump = artifact("fx-introspection-dump.json") or {}
        tails_art = artifact("attested-tails.json") or {}
        self.attested = tails_art.get("tails", {})
        self.shapes = tails_art.get("shapes", {})
        self.catalog_actions = artifact("action-catalog.json", "actions")
        self.checked, self.extra_confirmed, self.cc_source = cross_check()
        self.open_tokens = self.checked.get("documented_but_not_probe_confirmed", {})
        self.placeholders = self.checked.get("documented_example_placeholders", {})
        self.refuted = self.checked.get("documented_but_locally_refuted", {})
        # A documented token that selects what the verb does anyway. No state
        # can separate it from the bare form, and the vendor prose says why; it
        # is settled by construction and must not be re-probed.
        self.names_default = self.checked.get("documented_but_names_the_default", {})
        # token -> what the state lacked, for documented tails a live test tried
        # and could not separate. Keeps "undiscriminated" apart from "never
        # probed" even when the run's artifact holds no row for the form.
        self.tried = self.checked.get("documented_but_undiscriminated_here", {})


def load_context() -> Context:
    return Context()


def focused_execute_claims(name: str, capture: dict) -> list[dict]:
    """Join the landing-BPM experiment, never the channel-ambiguous token table."""
    if name != "auto_bpm_transition" or not capture.get("summary", {}).get("controls_agree"):
        return []
    claims = []
    for form, result in capture["summary"].get("forms", {}).items():
        if not result.get("verdict", "").startswith("recognized-"):
            continue
        claim = _claim("execute", form, "settled", observation=
                       f"landing BPM {result['bpms']}; {capture.get('method', {}).get('observable', '')}",
                       channel="HTTP execute + independent BPM readback")
        claim["source"] = "tests/bpm-transition-forms.json"
        claim["build"] = capture["summary"].get("build")
        claims.append(claim)
    return claims


def _claim(dimension: str, form: str, status: str, reason: str | None = None,
           observation: str = "", channel: str = "") -> dict:
    c = {"dimension": dimension, "form": form, "status": status}
    if reason:
        c["reason"] = reason
    if observation:
        c["observation"] = observation
    if channel:
        c["channel"] = channel
    return c


def focused_fx_claims(name: str, dump: dict) -> list[dict]:
    """The FX introspection sweep read every installed effect through the
    NAME form of the get_effect_* helpers, with no effect_select for those
    reads. Only the result field for the requested verb supplies a measurement;
    empty control collections do not. Joined here so the 2026-07-22 conclusion stops
    living only in store prose. The dump predates build stamping: it carries
    the product version, not a build, and the claim says so."""
    if not dump:
        return []
    try:
        from sweep_fx_introspection import NAME_FORM_VERBS
    except ImportError:
        return []
    spec = NAME_FORM_VERBS.get(name)
    if not spec:
        return []
    shape, result_path, kind = spec
    measurements = []
    excluded = {"missing": 0, "error": 0, "invalid": 0}
    for effect in dump.get("effects", []):
        if effect.get("introspected_via") != "title" or not effect.get("effect"):
            continue
        collection, dot, field = result_path.partition(".")
        rows = effect.get(collection, []) if dot else [effect]
        for row in rows:
            key = field if dot else collection
            if key not in row:
                excluded["missing"] += 1
                continue
            value = row[key]
            if isinstance(value, str) and value.startswith("error:"):
                excluded["error"] += 1
                continue
            if dot and (type(row.get("index")) is not int or row["index"] < 1):
                excluded["invalid"] += 1
                continue
            if kind == "count":
                # Legacy to_int() maps failures to zero: only positive stored
                # counts independently establish a successful count response.
                valid = type(value) is int and value > 0
            elif kind == "bool":
                valid = value in ("yes", "no", "true", "false", "on", "off")
            elif kind == "number":
                try:
                    valid = value != "" and math.isfinite(float(value))
                except (ValueError, TypeError):
                    valid = False
            else:
                valid = isinstance(value, str) and (bool(value) or kind == "optional_text")
            if not valid:
                excluded["invalid"] += 1
                continue
            measurements.append({"effect": effect["effect"], "value": value,
                                 **({"index": row["index"]} if dot else {})})
    if not measurements:
        return []
    example = measurements[0]
    effects = {m["effect"] for m in measurements}
    claim = _claim("arguments", f"{name} {shape}", "settled", None,
                   f"{len(measurements)} usable measurements across {len(effects)} effects "
                   f"addressed by name; e.g. {example}; no effect_select for these reads",
                   "HTTP FX introspection sweep")
    claim["source"] = "tests/fx-introspection-dump.json"
    claim["result_path"] = result_path
    claim["example"] = example
    claim["excluded_results"] = excluded
    claim["build"] = None
    claim["provenance"] = {"vdj_version": dump.get("vdj_version"), "build": None,
                           "note": "capture predates build stamping"}
    return [claim]


def prose_about_arguments(name: str, evidence: list[str], known: set[str] = frozenset()) -> bool:
    """Heuristic for explicit argument references, not proof of their absence.
    A form qualifies — the verb followed by a quoted or numeric
    token, a sign, a placeholder, or another verb (`all_decks get_version`) —
    and so does the word itself. `deck_has_error stayed off` and
    `video_fx_clear returned true` do not: prose verbs are not arguments."""
    form = re.compile(rf"\b{re.escape(name)}\s+(['\"<$+\-]|\d|(\w+))")
    words = re.compile(r"\bargument|\btails?\b|\bforms?\b", re.IGNORECASE)
    for e in evidence:
        e = e or ""
        if words.search(e):
            return True
        for m in form.finditer(e):
            if m.group(2) is None or m.group(2) in known:
                return True
    return False


def assess(name: str, rec: dict, ctx: Context) -> dict:
    """The per-verb contract assessment: one dimension state each for return
    type, arguments, execute position and behaviour, plus a claim per FORM
    saying what was observed or why it is still open. Shared by `just
    coverage` (aggregate) and `just verb` (one screen), so the two cannot
    disagree about what "settled" means."""
    c = ctx.contracts.get(name)
    # No contract row is unknown applicability, not inapplicability: a verb the
    # binary extraction missed must not shrink a denominator.
    queries = bool(c.get("queries")) if c is not None else None
    executes = bool(c.get("executes")) if c is not None else None
    rt = ctx.rtypes.get(name, {})
    observed = rt.get("observed_type")
    af = ctx.argforms.get(name)
    ex = ctx.execforms.get(name)
    pos = ctx.positions.get(name)
    focused_execute = focused_execute_claims(name, ctx.bpm_transition)
    focused_args = focused_fx_claims(name, getattr(ctx, "fx_dump", {}))
    extra = set(ctx.extra_confirmed.get(name, ()))
    claims: list[dict] = list(focused_args)

    # --- recognized tails, by channel ---------------------------------------
    probed_recognized = {tuple(t) for t in (af or {}).get("recognized_tokens", [])}
    single_probed = {t[0] for t in probed_recognized if len(t) == 1}
    recognized = sorted(single_probed | extra)
    tail_probed = af is not None
    probed_any = (tail_probed or pos is not None or ex is not None or bool(extra)
                  or bool(focused_args))

    candidates = set((c or {}).get("keyword_candidates") or [])
    candidates |= set(ctx.catalog_actions.get(name, {}).get("documented_parameters", []))
    candidates |= set(ctx.attested.get(name, {}))
    candidates -= {name}
    candidates -= set(ctx.placeholders.get(name, []))
    candidates -= set(ctx.refuted.get(name, []))
    defaults = set(ctx.names_default.get(name, []))
    candidates -= defaults
    unresolved = sorted((candidates - set(recognized)) | set(ctx.open_tokens.get(name, [])))
    for tok in sorted(defaults):
        claims.append(_claim("arguments", tok, "settled", None,
                             "names the default: lands where the bare form lands, by construction",
                             "catalog + local test"))
    probed_forms = {tuple(f["tokens"]): f for f in (af or {}).get("forms", [])}

    dims: dict[str, str] = {}

    # 1. Return type — applies only where the verb answers a query.
    if queries is None:
        dims["return_type"] = "unknown"
        claims.append(_claim("return_type", "bare", "open", "not_measured",
                             "no capability row from the binary; applicability unknown"))
    elif not queries:
        dims["return_type"] = "n/a"
    elif observed and observed != "untyped":
        dims["return_type"] = "settled"
        ctxs = sorted((rt.get("samples") or {}).keys())
        claims.append(_claim("return_type", "bare", "settled", None,
                             f"{observed}" + (f" in {len(ctxs)} contexts" if ctxs else ""),
                             "HTTP return-type sweep"))
    elif name in ctx.rtypes:
        dims["return_type"] = "untyped"
        claims.append(_claim("return_type", "bare", "open", "undiscriminated",
                             "empty in every sampled context; needs a richer state",
                             "HTTP return-type sweep"))
    else:
        dims["return_type"] = "unswept"
        claims.append(_claim("return_type", "bare", "open", "not_measured",
                             "never in the sweep population"))

    # 2. Arguments — applies to every verb.
    for tok in recognized:
        f = probed_forms.get((tok,))
        focused = next((claim for claim in focused_execute if claim["form"] == tok), None)
        if focused:
            claims.append({**focused, "dimension": "arguments"})
        elif f and f.get("verdict") == "recognized":
            obs = "separates from nonsense in " + ", ".join(f.get("separates_in", [])[:4])
            if len(f.get("separates_in", [])) > 4:
                obs += f" (+{len(f['separates_in']) - 4} more)"
            claims.append(_claim("arguments", tok, "settled", None, obs, "HTTP tail prober"))
        elif tok in extra:
            claims.append(_claim("arguments", tok, "settled", None,
                                 "confirmed by a focused probe with its own oracle",
                                 "focused probe (LOCAL_CONFIRMED)"))
        else:
            claims.append(_claim("arguments", tok, "settled", None, "recognized", "HTTP tail prober"))
    for tok in unresolved:
        f = probed_forms.get((tok,))
        if name in ctx.disputed:
            reason, obs = "conflicting", "verdict flipped between independent runs"
        elif tok in ctx.tried.get(name, {}):
            reason, obs = "undiscriminated", ctx.tried[name][tok]
        elif f is not None:
            reason = "undiscriminated"
            obs = (f"{f.get('verdict', 'probed')} in {len(ctx.arg_fixtures)} fixtures; "
                   "needs a state where this form and the bare form disagree")
        else:
            reason, obs = "not_measured", "candidate named by a source, never probed"
        claims.append(_claim("arguments", tok, "open", reason, obs,
                             "HTTP tail prober" if f is not None else ""))
    for tt in sorted(probed_recognized):
        if len(tt) == 2:
            f = probed_forms.get(tt, {})
            shape = f.get("pair_shape")
            if shape in ("beyond-singles", "last-token-wins"):
                claims.append(_claim("arguments", " ".join(tt), "settled", None,
                                     f"two-token form ({shape})", "HTTP tail prober"))
    attested_shapes = sorted(ctx.shapes.get(name, {}))
    if pos:
        for p_ in pos.get("positions", []):
            form = f"{pos.get('shape', '')} position {p_['index']} ({p_['class']})"
            if not pos.get("stable", False):
                claims.append(_claim("arguments", form, "open", "conflicting",
                                     "baseline changed during the position probe",
                                     "HTTP position prober"))
            elif p_["verdict"] == "no-answer":
                claims.append(_claim("arguments", form, "open", "unavailable",
                                     "baseline, variant and nonsense all returned errors",
                                     "HTTP position prober"))
            elif p_["verdict"] != "reads":
                claims.append(_claim("arguments", form, "open", "undiscriminated",
                                     "varying the value left the answer unchanged; unchanged "
                                     "output does not establish that the position is ignored",
                                     "HTTP position prober"))
            else:
                claims.append(_claim("arguments", form, "settled", None,
                                     f"{p_['verdict']} ({p_['baseline']} vs {p_['variant']})",
                                     "HTTP position prober"))
    for sh in attested_shapes:
        # Keyword recognition covers vocabulary, not a value-bearing or
        # multi-position signature. A position capture covers only its shape.
        if (not pos or pos.get("shape") != sh) and (not recognized or sh not in {"KW", "STR", "NAME"}):
            claims.append(_claim("arguments", f"{name} {sh}", "open", "not_measured",
                                 "shape attested in a shipped script (Tier 2); values, not "
                                 "keywords, so the tail prober cannot see it", "vendor script"))

    # Finite catalog obligations: preserve the actual source text rather than
    # inventing an unbounded requirement to discover every possible overload.
    catalog = ctx.catalog_actions.get(name, {})
    measured_forms = probed_recognized | {
        tuple(row["tokens"]) for row in (ex or {}).get("recognized", [])}
    for label, pattern, value_pattern in (
            ("numeric value", r"enter a value[^.]*\.", r"[+-]?\d+(?:\.\d+)?%?"),
            ("drawn curve", r"draw your own curve.*?(?:\.(?:\s|$)|$)", r".*=\[.*\].*")):
        match = re.search(pattern, catalog.get("text", ""), re.IGNORECASE)
        if match:
            measured = [form for form in measured_forms if len(form) == 1
                        and re.fullmatch(value_pattern, form[0].strip("\"'"))]
            claim = _claim("arguments", f"catalog: {label}", "settled" if measured else "open",
                           None if measured else "not_measured",
                           (f"observed forms: {measured}; " if measured else "") + match.group(0),
                           "HTTP form probe + vendor catalog" if measured else "vendor catalog")
            claim["source"] = f"tests/action-catalog.json:actions.{name}.text"
            claims.append(claim)
    two_position_focused = any(len(cl["form"].split()) >= 3 for cl in focused_args)
    if catalog.get("multi_argument") and not (pos and pos.get("stable") and
            all(p["verdict"] == "reads" for p in pos.get("positions", []))) and not (
            af or {}).get("two_token_grammar") and not two_position_focused:
        claims.append(_claim("arguments", "catalog: multiple arguments", "open", "not_measured",
                             "catalog names a multi-argument form not covered by the token results",
                             "vendor catalog"))
    if (c or {}).get("arg_demand_slots") and not (recognized or defaults or pos or focused_execute
                                                  or focused_args):
        claims.append(_claim("arguments", "binary argument-demand slots", "open", "not_measured",
                             str(c["arg_demand_slots"]), "binary contract (Tier 2 lead)"))

    if unresolved or any(c["dimension"] == "arguments" and c["status"] == "open"
                         for c in claims):
        dims["arguments"] = "open"
    elif recognized or defaults or focused_args or (
            pos and pos.get("stable") and pos.get("positions")
            and all(p["verdict"] == "reads" for p in pos["positions"])):
        dims["arguments"] = "settled"
    elif tail_probed and not candidates and not attested_shapes:
        # Probed against nonsense with no candidate anywhere. Absence of a
        # candidate is not proof of absence of arguments, so this is reported
        # apart from `settled` and does not close the dimension.
        dims["arguments"] = "no_known_candidates"
        claims.append(_claim("arguments", "(any)", "open", "not_measured",
                             "no source names a candidate; exhaustive absence is not claimed",
                             "HTTP tail prober"))
    elif attested_shapes:
        dims["arguments"] = "shape_attested"
    elif (not probed_any and rec.get("confidence") == "local_test" and rec.get("evidence")
          and prose_about_arguments(name, rec["evidence"], set(getattr(ctx, "canon", {})))):
        # The prose names a form or speaks of the argument: a live result that
        # never reached an artifact row. Locate it before re-running anything.
        dims["arguments"] = "evidence_in_prose"
        claims.append(_claim("arguments", "(see store evidence)", "open", "prose_only",
                             (rec["evidence"][0] or "")[:160]))
    elif not probed_any:
        dims["arguments"] = "unprobed"
        obs = ("no structured argument evidence joined; the prose filter found no explicit "
               "argument reference" if rec.get("evidence") else "no argument evidence joined")
        claims.append(_claim("arguments", "(any)", "open", "not_measured", obs))
    else:
        dims["arguments"] = "open"

    # 3. Execute position — read the row, not just its presence.
    if executes is None:
        dims["execute"] = "unknown"
        claims.append(_claim("execute", "bare", "open", "not_measured",
                             "no capability row from the binary; applicability unknown"))
    elif not executes:
        dims["execute"] = "n/a"
    elif ex is None:
        dims["execute"] = "open"
        claims.append(_claim("execute", "bare", "open", "not_measured",
                             "no execute capture joined; check store or focused evidence before re-probing"))
    elif "skipped" in ex:
        dims["execute"] = "no_observable"
        claims.append(_claim("execute", "bare", "open", "unavailable", ex["skipped"],
                             "HTTP execute prober"))
    else:
        exec_hits = {" ".join(r["tokens"]) for r in ex.get("recognized", [])}
        for h in sorted(exec_hits):
            claims.append(_claim("execute", h, "settled", None,
                                 f"changes the {ex.get('family', '?')} readback differently "
                                 "from bare and from nonsense", "HTTP execute prober"))
        # Focused confirmations can be query-only; never promote them into
        # execute evidence without an execute-specific observation.
        exec_open = sorted((candidates - exec_hits))
        for tok in exec_open:
            if tok in ex.get("signatures", {}):
                claims.append(_claim("execute", tok, "open", "undiscriminated",
                                     f"indistinguishable from nonsense in the {ex.get('family', '?')} "
                                     "readback; that observable cannot see what this tail selects",
                                     "HTTP execute prober"))
            else:
                claims.append(_claim("execute", tok, "open", "not_measured",
                                     "candidate has no execute signature in this capture"))
        if ex.get("verdict") == "unstable-controls":
            claims.append(_claim("execute", "(controls)", "open", "conflicting",
                                 "nonsense controls disagree; no execute form is established",
                                 "HTTP execute prober"))
        if ex.get("verdict") == "has-execute-tokens":
            dims["execute"] = "settled" if not exec_open else "partial"
        elif ex.get("verdict") == "tail-ignored-in-execute":
            dims["execute"] = "undiscriminated"
            if not exec_open:
                claims.append(_claim("execute", "bare", "open", "undiscriminated",
                                     f"toggles the {ex.get('family', '?')} readback; no tail "
                                     "changed it", "HTTP execute prober"))
        else:
            dims["execute"] = "open"

    if focused_execute:
        # The generic toggle observable's failure is not a contradiction of a
        # focused experiment that measures the parameter's actual effect.
        measured = {claim["form"] for claim in focused_execute}
        claims = [claim for claim in claims if not (
            claim["dimension"] == "execute" and claim["form"] in measured)]
        claims.extend(focused_execute)
        remaining = candidates - measured - {" ".join(r["tokens"])
                                            for r in (ex or {}).get("recognized", [])}
        if not remaining:
            claims = [claim for claim in claims if not (
                claim["dimension"] == "execute" and claim["status"] == "open"
                and claim["form"] == "bare")]
        dims["execute"] = "partial" if remaining else "settled"

    # 4. Behaviour — the store's own claim; evidence required to count.
    status = rec.get("test_status", "Untested")
    if status == "Pass" and rec.get("evidence"):
        dims["behaviour"] = "settled"
        claims.append(_claim("behaviour", "(store)", "settled", None,
                             (rec["evidence"][0] or "")[:160], "store evidence"))
    elif rec.get("blocked"):
        dims["behaviour"] = "blocked"
        claims.append(_claim("behaviour", "(store)", "open", "unavailable",
                             "hardware or external source not available here"))
    else:
        dims["behaviour"] = "open"
        claims.append(_claim("behaviour", "(store)", "open", "not_measured",
                             f"store status {status}"))

    # An open dimension must always explain itself, including captures with
    # missing or unfamiliar verdicts. Row presence alone is not a conclusion.
    for dimension, state in dims.items():
        if state not in CLOSED | {"n/a"} and not any(
                claim["dimension"] == dimension and claim["status"] == "open" for claim in claims):
            claims.append(_claim(dimension, "(remaining contract)", "open", "not_measured",
                                 "existing observations do not resolve this dimension"))

    applicable = [d for d in DIMENSIONS if dims[d] != "n/a"]
    settled = [d for d in applicable if dims[d] in CLOSED]
    read_applicable = [d for d in READ_SIDE if dims[d] != "n/a"]
    read_settled = [d for d in read_applicable if dims[d] in CLOSED]
    contract = ("settled" if applicable and len(settled) == len(applicable)
                else "open" if not settled else "partial")
    for claim in claims:
        channel = claim.get("channel")
        source, provenance = None, {}
        if channel == "HTTP tail prober":
            source = "tests/verb-arg-forms.json"
            form = probed_forms.get(tuple(claim["form"].split()), {})
            provenance = form.get("provenance", {})
        elif channel == "HTTP execute prober":
            source = "tests/verb-execute-forms.json"
            provenance = (ex or {}).get("provenance", {})
        elif channel == "HTTP return-type sweep":
            source = "tests/verb-return-types.json"
        if claim.get("source") and "provenance" in claim:
            continue  # focused joins carry their own provenance
        if source:
            claim["source"] = source
            claim["build"] = provenance.get("build")
            if provenance:
                claim["provenance"] = provenance
    return {
        "queries": queries, "executes": executes,
        "observed_type": observed, "test_status": status,
        "recognized_tails": recognized, "unresolved_tails": unresolved,
        "positions_probed": pos is not None,
        "attested_shapes": attested_shapes,
        "dimensions": dims,
        "contract": contract,
        "claims": claims,
        "next": next_tests(name, dims, claims, ctx),
        "applicable": len(applicable), "settled": len(settled),
        "complete": len(settled) == len(applicable) and len(applicable) > 0,
        "read_side_complete": (len(read_settled) == len(read_applicable)
                               and len(read_applicable) > 0),
    }


def next_tests(name: str, dims: dict, claims: list[dict], ctx: Context) -> list[str]:
    """The smallest test that would close each open reason. Derived from the
    reason, never from effort spent: an `undiscriminated` item is not re-run
    with the observable that already failed to separate it."""
    out: list[str] = []
    reasons = {(c["dimension"], c.get("reason")) for c in claims if c["status"] == "open"}
    if ("return_type", "not_measured") in reasons and dims["return_type"] == "unswept":
        out.append("add to the return-type sweep population (tools/sweep_return_types.py)")
    if ("return_type", "undiscriminated") in reasons:
        out.append("query in a state where the bare form has a value (see `just fixtures`)")
    if ("arguments", "not_measured") in reasons:
        if any(c["dimension"] == "arguments" and c.get("channel") == "vendor script"
               and c["status"] == "open" for c in claims):
            out.append(f"position probe holding the attested shape: tools/probe_arg_positions.py "
                       f"(`just verb-arg-positions {name}` afterwards)")
        else:
            out.append(f"inspect sources and shape first; capture a focused tail probe to a separate "
                       f"--out FILE, then merge (see `just verb-arg-forms {name}`)")
    if ("arguments", "undiscriminated") in reasons:
        hint = NEXT_TEST_HINTS.get(name)
        out.append(hint or "a fixture and observable where the candidate separates from nonsense; "
                           "the recorded measurement did not resolve it")
    if ("arguments", "conflicting") in reasons:
        out.append("two independent runs with `--repeat 2`; a slow-drifting value needs both")
    if ("arguments", "prose_only") in reasons:
        out.append("locate and link the recorded test; re-probe only if its evidence is insufficient")
    if ("execute", "not_measured") in reasons:
        out.append("allowlisted execute with independent readback and verified restore: "
                   "tools/probe_execute_forms.py")
    if ("execute", "undiscriminated") in reasons:
        out.append("an execute observable that sees what the tail selects, not only on/off "
                   "(the bpm-transition prober is the model)")
    if ("execute", "unavailable") in reasons:
        out.append("an execute readback other than on/off; none exists for this verb yet")
    if ("behaviour", "unavailable") in reasons:
        out.append("blocked: hardware or external source (see the store's blocked flag)")
    return out


def collect() -> dict:
    ctx = load_context()
    verbs = {name: assess(name, rec, ctx) for name, rec in ctx.canon.items()}
    return {
        "stamp": build_stamp(),
        "read_on": date.today().isoformat(),
        "cross_check_source": ctx.cc_source,
        "cross_check": {k: {"verbs": len(v), "tokens": sum(len(t) for t in v.values())}
                        for k, v in ctx.checked.items()},
        "population": population(ctx.canon, ctx.store, verbs),
        "dimensions": {d: tally(verbs, d) for d in DIMENSIONS},
        "ladder": ladder(verbs),
        "staleness": staleness(ctx.argforms, ctx.execforms, ctx.rtypes),
        "frontier": frontier(ctx.canon, verbs, ctx.store),
        "verbs": verbs,
    }


def population(canon: dict, store: dict, verbs: dict) -> dict:
    return {
        "store_records": len(store),
        "canonical": len(canon),
        "aliases": len(store) - len(canon),
        "query_capable": sum(1 for v in verbs.values() if v["queries"]),
        "execute_capable": sum(1 for v in verbs.values() if v["executes"]),
        "both": sum(1 for v in verbs.values() if v["queries"] and v["executes"]),
        "no_contract_row": sum(1 for v in verbs.values() if v["queries"] is None),
    }


def tally(verbs: dict, dim: str) -> dict:
    out: dict[str, int] = {}
    for v in verbs.values():
        out[v["dimensions"][dim]] = out.get(v["dimensions"][dim], 0) + 1
    applicable = sum(n for k, n in out.items() if k != "n/a")
    closed = sum(n for k, n in out.items() if k in CLOSED)
    out["_applicable"] = applicable
    out["_closed"] = closed
    out["_closed_pct"] = round(100 * closed / applicable, 1) if applicable else 0.0
    return out


def ladder(verbs: dict) -> dict:
    """Verbs by how much of their own contract is closed. Sorted by the fraction
    itself, so a 2/2 verb ranks above a 2/4 one rather than tying with it."""
    rungs: dict[str, int] = {}
    for v in verbs.values():
        rungs[f"{v['settled']}/{v['applicable']}"] = rungs.get(f"{v['settled']}/{v['applicable']}", 0) + 1

    def rank(key: str) -> tuple:
        got, tot = (int(x) for x in key.split("/"))
        return (-(got / tot if tot else 0), -got, -tot)

    return dict(sorted(rungs.items(), key=lambda kv: rank(kv[0])))


def staleness(argforms: dict, execforms: dict, rtypes: dict) -> list[str]:
    """A stored summary that no longer matches its own records. Worth printing:
    it is how a regenerated artifact silently keeps quoting the old figure."""
    notes = []
    for fname, records in (("verb-arg-forms.json", argforms),
                           ("verb-execute-forms.json", execforms),
                           ("verb-return-types.json", rtypes)):
        data = artifact(fname)
        if not data or not records:
            continue
        claimed = data.get("summary", {}).get("verbs")
        if isinstance(claimed, int) and claimed != len(records):
            notes.append(f"{fname}: summary says {claimed} verbs, the records hold "
                         f"{len(records)} — the header predates the last append")
    return notes


def frontier(canon: dict, verbs: dict, store: dict) -> dict:
    """What each dimension is actually blocked on, as names rather than a count."""
    known = contract_names()
    return {
        "return_type_untyped": sorted(n for n, v in verbs.items()
                                      if v["dimensions"]["return_type"] == "untyped"),
        "return_type_unswept": sorted(n for n, v in verbs.items()
                                      if v["dimensions"]["return_type"] == "unswept"),
        "arguments_open": sorted(n for n, v in verbs.items()
                                 if v["dimensions"]["arguments"] == "open"),
        "arguments_unprobed_with_candidates": sorted(
            n for n, v in verbs.items()
            if v["dimensions"]["arguments"] == "unprobed" and v["unresolved_tails"]),
        "execute_open": sorted(n for n, v in verbs.items()
                               if v["dimensions"]["execute"] == "open"),
        "execute_partial_or_undiscriminated": sorted(
            n for n, v in verbs.items()
            if v["dimensions"]["execute"] in ("partial", "undiscriminated", "no_observable")),
        "capability_unknown": sorted(n for n, v in verbs.items() if v["queries"] is None),
        "no_tier1_row_at_all": sorted(n for n, r in canon.items()
                                      if n not in known and not r.get("blocked")),
        "audit_pool": sorted(r["name"] for r in audit_pool(store)),
        "blocked": sorted(n for n, r in canon.items() if r.get("blocked")),
    }


LABELS = {
    "return_type": ("Return type in query position", "sweep_return_types.py, live over HTTP"),
    "arguments":   ("Accepted argument tails",        "probe_arg_forms.py vs nonsense controls"),
    "execute":     ("Execute-position behaviour",     "probe_execute_forms.py, writes to a live app"),
    "behaviour":   ("Behaviour confirmed live",       "the store's test_status, evidence required"),
}
ORDER = ("settled", "partial", "no_known_candidates", "shape_attested", "evidence_in_prose",
         "open", "undiscriminated", "no_observable", "untyped", "unswept", "unprobed",
         "unknown", "blocked", "n/a")
GLOSS = {
    "partial": "some tails change the readback; others indistinguishable from nonsense",
    "no_known_candidates": "probed, no candidate in any source — absence not claimed",
    "undiscriminated": "executed; no tail changed the on/off readback",
    "no_observable": "no readback other than on/off exists for it",
    "unknown": "no capability row from the binary — applicability unknown, counted open",
    "shape_attested": "takes values, not keywords — shape from a shipped script (Tier 2)",
    "evidence_in_prose": "live-tested, but the conclusion is only in store prose",
    "untyped": "swept, empty in every context",
    "unswept": "never in the sweep population",
    "unprobed": "never probed",
}


def bar(pct: float, width: int = 28) -> str:
    filled = round(pct / 100 * width)
    return "█" * filled + "·" * (width - filled)


def render(d: dict, show: str | None) -> str:
    L = ["VDJScript contract coverage", "=" * 27,
         d["stamp"], f"read {d['read_on']} from the artifacts; nothing here is stored", ""]

    p = d["population"]
    L.append(f"Population: {p['canonical']} canonical verbs ({p['aliases']} aliases folded away) — "
             f"{p['query_capable']} answer queries, {p['execute_capable']} execute, "
             f"{p['both']} do both")
    if p["no_contract_row"]:
        L.append(f"            {p['no_contract_row']} carry no capability row from the binary")
    L.append("")

    L.append("PER DIMENSION   (denominator is the verbs the dimension applies to)")
    for dim in DIMENSIONS:
        t = d["dimensions"][dim]
        title, how = LABELS[dim]
        L.append("")
        L.append(f"  {title}")
        L.append(f"    {bar(t['_closed_pct'])}  {t['_closed']}/{t['_applicable']}"
                 f"  ({t['_closed_pct']}%)")
        for k in ORDER:
            if k not in t or k in ("settled", "n/a"):
                continue
            gloss = f"   — {GLOSS[k]}" if k in GLOSS else ""
            L.append(f"      {t[k]:>4} {k}{gloss}")
        L.append(f"    via {how}")
    L.append("")

    L.append(f"CROSS-CHECK     documented vs probed vs written by Atomix — {d['cross_check_source']}")
    for k, v in d["cross_check"].items():
        L.append(f"  {k:<36} {v['tokens']:>4} tokens across {v['verbs']:>3} verbs")
    L.append("")

    L.append("COMPLETENESS LADDER   closed/applicable dimensions per verb")
    for rung, n in d["ladder"].items():
        got, tot = rung.split("/")
        L.append(f"  {rung:<6} {n:>4} verb" + ("" if n == 1 else "s") + ("   <- nothing left open" if got == tot else ""))
    read = sum(1 for v in d["verbs"].values() if v["read_side_complete"])
    full = sum(1 for v in d["verbs"].values() if v["complete"])
    L.append(f"  {full} {'verb is' if full == 1 else 'verbs are'} closed on every dimension "
             "including execute position;")
    L.append(f"  {read} {'is' if read == 1 else 'are'} closed on the read-side contract "
             "(return type, arguments, behaviour),")
    L.append("  which is the figure worth quoting while the execute channel is deliberately thin.")
    L.append("")

    f = d["frontier"]
    L.append("FRONTIER        what is actually left, by dimension")
    for label, key in (("query verbs never swept for a type", "return_type_unswept"),
                       ("swept but empty in every context", "return_type_untyped"),
                       ("verbs with an unresolved tail", "arguments_open"),
                       ("never probed, but candidates exist", "arguments_unprobed_with_candidates"),
                       ("execute-capable, never executed", "execute_open"),
                       ("executed, tails not (fully) discriminated", "execute_partial_or_undiscriminated"),
                       ("no capability row (applicability unknown)", "capability_unknown"),
                       ("no Tier-1 row of any kind", "no_tier1_row_at_all"),
                       ("hardware-blocked", "blocked")):
        L.append(f"  {label:<38} {len(f[key]):>4}")
    L.append("")

    if d["staleness"]:
        L.append("STALE HEADERS   (the records were recounted; these summaries were not regenerated)")
        for note in d["staleness"]:
            L.append(f"  {note}")
        L.append("")

    if show == "settled":
        done = sorted(n for n, v in d["verbs"].items() if v["read_side_complete"])
        L.append(f"SETTLED VERBS   read-side contract closed ({len(done)}); "
                 "* also measured in execute position")
        for n in done:
            v = d["verbs"][n]
            tails = ", ".join(v["recognized_tails"]) or "takes no arguments"
            mark = "*" if v["dimensions"]["execute"] == "settled" else " "
            L.append(f" {mark}{n:<34} {v['observed_type'] or 'execute-only':<8} {tails}")
    elif show == "frontier":
        L.append("FRONTIER, BY NAME")
        for key, names in f.items():
            if not names:
                continue
            L.append("")
            L.append(f"  {key} ({len(names)})")
            for i in range(0, len(names), 4):
                L.append("    " + "  ".join(f"{x:<28}" for x in names[i:i + 4]).rstrip())
    else:
        L.append("`--settled` lists the finished verbs, `--frontier` lists what each dimension "
                 "is waiting on, `--format=json` gives the per-verb rows.")
    return "\n".join(L)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--format", choices=("text", "json"), default="text")
    ap.add_argument("--settled", action="store_true", help="list the verbs with nothing open")
    ap.add_argument("--frontier", action="store_true", help="list what each dimension awaits")
    args = ap.parse_args(argv)

    data = collect()
    if args.format == "json":
        print(json.dumps(data, indent=1))
        return 0
    show = "settled" if args.settled else "frontier" if args.frontier else None
    print(render(data, show))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
