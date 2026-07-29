# Evidence Standards

Ratified 2026-07-27. **This document governs every claim in this repository.** When another
doc's wording conflicts with it, this one wins and the other doc is wrong.

The repo exists to be trusted offline by agents and humans who cannot re-verify its claims
cheaply. A confident-sounding guess costs more than a gap, because a gap prompts a test and
a guess prevents one. So claims are graded by *how they were established*, never by how
plausible they sound or how authoritative the source felt.

## The three tiers

### Tier 1 — Proof

Only these establish that something **functionally works**. All four are direct observation
of the running application:

| Channel | Doc |
| --- | --- |
| Network protocol tests (VirtualDJ Remote protocol) | [Remote Protocol.md](Remote%20Protocol.md) |
| HTTP control interface tests | [HTTP Control Interface.md](HTTP%20Control%20Interface.md) |
| Live pad tests (pad-page fixtures read back in the UI) | [VDJScript Local Test Tracker.md](VDJScript%20Local%20Test%20Tracker.md) |
| Agent driving the application window | see *Availability* below |

A Tier-1 record is only proof if it names the **build**, the **context** (decks, hardware,
account, loaded state), the **exact script or bytes sent**, and the **observed result** —
the template at the top of the tracker. An observation without those is an anecdote.

### Tier 2 — Leads

Real, worth recording, worth investigating. **Never** grounds for stating that something
works. Everything here must be labelled and must name what test would settle it:

- Atomix staff/CTO/Development-Manager posts on the official forums.
- Binary extraction and analysis (symbol tables, compiled taxonomy tables, string tables)
  that no Tier-1 test has yet confirmed — with one exception, below.
- Official Atomix example files: bundled pads, skins, samplerbanks, mappers.
- Official third-party example files from sanctioned vendors (AlphaTheta/Pioneer, Denon,
  Numark, Rane, AKAI…).

### Tier 3 — Hokum

Everything else: community blog posts, forum replies from non-staff, YouTube tutorials,
plausible-sounding inference, pattern-matching from other DJ software, and anything whose
provenance cannot be stated. Not recorded as a claim. If it suggests a test, record the
test, not the source.

## The rules

### 1. Deciding whether a verb exists — the four verdicts

The tiers above grade proof that something *works*. Whether a **name** is real is a separate,
now-decidable question, and it has four outcomes. Apply them in order:

| # | Verdict | Test |
| --- | --- | --- |
| 1 | **Exists** | Membership in the structured binary list (`just binary-verb <name>` — a mangled `ACTION_<name>` implementation class, or an entry in the app's own language catalog), **or** an existence code / value from `/query` (`just verb-probe <name>`). Either alone is sufficient. |
| 2 | **Does not exist** | Absent from the structured list **and** no bare `<name>` string anywhere in the executable. |
| 3 | **Does not exist (adjudicated)** | Absent from the structured list, a bare string exists, but every occurrence sits in a demonstrably unrelated context. State the contexts. |
| 4 | **Undecided** | Absent from the structured list, a bare string exists, and its context is plausibly verb-related. Stays open. |

**Rule 1a — the structured list proves existence but is not a completeness oracle.** It is a
union of three sources in the app itself (`just binary-verb <name>`, 1,076 names):

| Source | Size | What it is |
| --- | ---: | --- |
| `symbol` | 1,012 | mangled `ACTION_<name>` implementation classes — one per canonical verb |
| `catalog` | 812 | action names VirtualDJ documents in `languages.zip` → `English.xml` `<Actions>` |
| `table` | 967 | the parser's **alphabetically sorted name table**, recovered as long ascending identifier runs (`action_deck` … `zoom_vertical`). This is the source that carries **aliases** |

The union covers **998 of the 1,007** names the HTTP sweep proved real. The nine it misses are
`browser`, `config`, `jog`, `no`, `off`, `on`, `preview`, `volume`, `yes`. Five (`jog`, `no`,
`off`, `on`, `yes`) are under four characters and so invisible to `strings` at its default
minimum — a tooling limit, not a missing structure. The other four (`browser`, `config`,
`preview`, `volume`) are long enough to appear and do not, which means **at least one more
dispatch structure exists that has not been located.** Finding it is tracked as TODO task 9;
the goal is the exact verb set, at which point the disproof no longer needs its conservative
string leg. Individual sources are each *less* complete: the name table
omits core verbs (`load`, `loop`, `cue`, `hot_cue`, `nothing`), which is exactly why all three
are unioned rather than any one trusted. **Absence from the structured list is never a
disproof on its own** — that is what verdict 2's second leg is for.

**Rule 1h — aliases are derivable, structurally.** A name present in the `table` but with no
`symbol` of its own cannot be its own implementation, so it must dispatch to another class:
it is an alias or variant form. That rule recovers **52 of the aliases the store already
records independently** (from the official appendix) and predicts **11 more**:
`eq_high_slider`, `eq_low_slider`, `eq_mid_slider`, `eq_med`, `eq_kill_med`,
`get_hasheadphone`, `jog_wheel`, `pitch_slider`, `scratch_wheel`, `scratch_wheel_touch`,
`sampler_unload_from_deck`. The 52/63 agreement with an independent source is what makes this
a derivation rather than name-pattern guessing.

Its limit: it identifies a name **as** an alias, never **which** verb it aliases. Pairing by
resemblance (`eq_med` → `eq_mid`) is Tier 3 inference no matter how obvious it looks. Pairing
is settled behaviorally — drive the presumed canonical and check the alias tracks it — or from
the official appendix, which pairs them explicitly.

**Rule 1b — the string leg is conservative on purpose.** A bare string cannot prove a name is
a verb: `none` occurs three times in the executable, once amid compiled register-save junk,
once inside SQLite's internal string pool (beside `flexnum` and `sub-select returns %d
columns`), and once in a UI category list (beside `custom`, `pads`, `stems`). None is a verb
context, and `nothing` — which *is* in the catalog, documented as "Do nothing." — is almost
certainly what such a name was reaching for. So the string leg exists to prevent false
disproofs of aliases, not to grant existence.

**Rule 1c — positive HTTP codes are sound.** 26 deliberately invented names, including
family-prefix shapes (`get_zzzz`, `effect_zzzz`, `browser_zzzz`) chosen to trip a dispatcher,
all returned `E_FAIL` and nothing else. No fake name has produced `E_NOTIMPL`,
`E_INVALIDARG`, `E_ACCESSDENIED`, `S_FALSE`, or a value.

**Rule 1d — calibration must use an independently-sourced set.** The disproof was first
calibrated only against names the HTTP sweep itself proved real, which grades a test against
its own output. It is now also calibrated against the 812 action names in VirtualDJ's own
language catalog: **all 812 leave a trace in the executable, zero exceptions.** Recalibrate
this way whenever the method changes.

**Rule 1e — a verdict is scoped to the inspected build.** Record the build. A verb added
later leaves traces in that binary, not this one. Names of ≤3 characters need `strings -n 2`
(the default minimum is 4, which is why `jog`, `no`, `on`, `yes` appear traceless).

**Rule 1f — a verdict is about the name, never the behavior.** See rule 3.

**Rule 1g — the residual assumption, stated so it can be attacked.** All of this assumes a
real verb leaves a whole-name literal in the executable. A name assembled at runtime from
fragments would evade every test above. Nothing in either calibration set behaves that way,
but it is not ruled out.

Method detail and the calibration tables: [Undocumented VDJScript Candidates.md](Undocumented%20VDJScript%20Candidates.md)
§"Disproving A Name".

### 2. What counts as a behavioral test

A **behavioral test** is a Tier-1 observation with three parts: read the state, change it
through the thing under test, read it back independently. All three must be recorded. The
readback must not come from the same call that made the change (rule 4).

Worked shape, using alias pairing as the example — this **is** reachable at Tier 1, on either
channel:

- **HTTP:** set the presumed canonical to a distinctive value (`eq_mid 25%`), then query the
  candidate (`eq_med`). Repeat with two or three *different* values, and drive it from the
  other side too. Equal readings once could be coincidence — both idle at `0.5` proves
  nothing; tracking across several distinct values does not.
- **Network protocol:** subscribe to both names as separate ids in one session and watch the
  pushes. This is the stronger form: you see both resolve to the same underlying state feed
  and change in lockstep over time, rather than sampling twice.

Either establishes that two names address the same control. Neither tells you which name is
canonical — for that, use the implementation evidence (the one with its own `ACTION_` class)
or the official appendix's own pairing.

**"The appendix"** throughout these docs means the [official VDJScript verbs
appendix](https://www.virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html), which
this repo parses to 991 names including 59 explicitly-paired aliases. It is Tier 2 —
official *documentation*, incomplete and occasionally wrong — but it is the authority on
which name Atomix considers canonical.

### 3. Existence, kind, and behavior are three different claims

Do not let one become another. The HTTP error-code sweep proves a name is **real** and
classifies its **kind** (query / action-only / takes-arguments / context-gated). It says
nothing about what the verb *does*. `test_status=Pass` in the verb store means behavior was
observed, so an existence probe must never set it. State the claim you actually have:

> `clear_search` exists and is action-only (`E_NOTIMPL`, HTTP sweep 2026-07-27). Behavior
> untested.

### 4. A channel's own return value is not a result

Proof requires independent readback. Established cases:

- `/execute` returning `true` does not mean the action succeeded — `deck 2 load
  "<nonexistent path>"` returns `true` and leaves the deck in an error state.
- `/execute` returning `false` does not mean failure — it is the verb's own boolean.
- `E_FAIL` from `/query` is silence, not denial. A real, binary-confirmed verb
  (`remote_action`) returns it.
- A Remote-protocol `fail` value means "no value right now", not "bad query".

So: send, then **query the state independently**, and record that.

### 5. Provenance must be established independently of the artifact's own metadata

An artifact's self-description is not evidence about the artifact. A mapper file's
`author="Atomix Productions"` attribute sits on files whose bindings are entirely
user-written, so it cannot promote a local file to Tier 2 — see
[examples/Mappers/README.md](../examples/Mappers/README.md). Establish provenance from where
a file came from and what it contains, and if that cannot be done, the file is Tier 3 for
claims about content.

Corollary — **personal and experimental local files are not Tier 2 at all.** A mapping loads
and runs perfectly happily with bindings that do nothing, so a name appearing in one is
evidence of nothing except that the file parses. Personal files are legitimate examples of
*format and idiom*; they are never evidence that a verb exists or works.

## The one place shipped files are authoritative

Tier 2 says official example files cannot prove behavior. They remain the **authority for
format vocabulary** — which elements, attributes, and control names the parser accepts —
because a shipped file demonstrably loads. That is the basis of `lint_skins.py` (every
element/attribute must appear in the shipped-skin corpus) and of the XML inventory, and it
stays valid. The distinction:

- "`<panel>` accepts a `visibility` attribute" — shipped corpus is authority.
- "`visibility` re-evaluates dynamically while `condition` does not" — needs Tier 1.

## Tooling status (2026-07-27)

| Tool | State |
| --- | --- |
| `tools/extract_binary_verbs.py` | **Current.** Emits the structured list to `tests/binary-verbs.json`; `just binary-verb <name>`. |
| `tools/sweep_verb_existence.py` | **Current.** HTTP error-code sweep; `just verb-probe <name>`. |
| `tools/extract_vdjscript_symbols.py` | **Stale on this build** — reports 0 `ACTION_*` classes, because the names now survive only as mangled strings and not as `nm`-visible symbols. Do not read its silence as absence. |
| `tools/extract_vdjscript_taxonomy.py` | **Stale on this build** — address-pinned to VirtualDJ `8.5.9307` / bundle `18.0.9336` and raises on the current binary. The Button Editor autocomplete list it recovered is therefore unavailable; the structured list stands in for it. |

## Availability of the four Tier-1 channels

| Channel | Status |
| --- | --- |
| HTTP control interface | Available and cheap. Preferred first instrument. Requires the Network Control plugin enabled and a Pro license. |
| Network protocol | Available; needs a Bonjour advert and, for capture, one real device. Reconnects depend on the per-device "Connect automatically" checkbox. |
| Live pad tests | Available; needs a fixture installed and a human to read the UI. |
| Agent driving the window | **Method is valid but not wired up in this environment** — no screen-control tooling is present, so UI-only steps (clicking Connect in Config → Controllers, reading a dialog) currently have to be delegated to the user. Anything blocked on this is `Untested`, not `Blocked`. |

## Mapping the existing source labels

Labels already in the docs map onto the tiers as follows. Where a label spans tiers, the
claim's wording must make clear which applies.

| Existing label | Tier | Note |
| --- | --- | --- |
| `Local test` | 1 | Only if build + context + action + result are recorded. |
| `Local observation` | 1 or 2 | Tier 1 when it names build and context; otherwise a lead. |
| `Official` (manual/wiki/appendix) | 2 | Official *documentation*. Frequently incomplete and occasionally wrong — this repo has caught both. Prove behavior separately. |
| `Official forum` | 2 | Staff/CTO only. Non-staff replies are Tier 3. |
| `Built-in app resource`, `Built-in skin`, `Built-in pad page`, `Published skin`, `Published pad page` | 2 | Plus authoritative for format vocabulary (above). |
| `Binary symbol table`, and catalog entries | **1 for existence** | Structured-list membership proves the name is real (rule 1). Still Tier 2 for behavior. |
| `Binary compiled table`, `Binary string-table` | 2 | An unstructured string is not evidence of existence (rule 1b); it serves only as the conservative leg of a disproof. |
| `Community` | 3 | Record the test it suggests, not the claim. |
| `Inference` | 3 | Permitted only as explicitly-marked reasoning over Tier-1 facts, never as a finding. Do not let an inference acquire a source label by sitting next to one. |

## Writing a claim

1. State the claim as narrowly as the evidence supports — existence, kind, or behavior.
2. Name the tier or label, and for Tier 1 the build.
3. If it is a lead, name the test that would settle it.
4. If a claim is retracted, **say so in place** with what was wrong, rather than deleting it
   silently. A reader who acted on the old claim needs to find the correction.
