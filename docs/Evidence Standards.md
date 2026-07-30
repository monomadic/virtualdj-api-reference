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

### 1. Deciding whether a verb exists — the verb table decides it

**Superseded 2026-07-27.** The earlier scheme needed four verdicts and a conservative
string-context leg because no complete name list had been located. One has now been found, so
existence is a **single membership test**:

> `just verb-table <name>` — in the table, the name is a verb; absent, it is not.

[tools/extract_verb_table.py](../tools/extract_verb_table.py) extracts a genuinely serialised
structure — a sorted array of 16-byte records in `__DATA,__data` —

```c
struct { const char *name; uint32_t id; uint32_t flags; };
```

1,028 records on VirtualDJ 2026 at `0x10402d020`, `action_deck` … `zoom_vertical`. It is
**complete**: it contains all 1,007 names the HTTP sweep proved real, including the strays
that defeated every earlier source (`load`, `loop`, `cue`, `hot_cue`, `nothing`, `browser`,
`config`, `jog`). `nothing` legitimately carries `id == 0`.

**Rule 1a — this is a structure, not an adjacency heuristic.** Earlier passes inferred tables
from `strings` output and from packed sorted blobs in `__cstring`. Both were suggestive only:
compilers pool literals near each other, so proximity proves nothing. A record array whose
members are pointers into `__cstring` paired with an id is the real dispatch data. Prefer it
over every earlier source; `tests/binary-verbs.json` and the sorted-blob findings are
superseded and kept only as corroboration.

**Rule 1b — absence from the table IS disproof**, on the inspected build, and no longer needs
a string-context adjudication. Settled cases: `browser_filter`, `browser_search`, and `none`
are absent, therefore not verbs; `remote_action`, `nothing`, and `crash` are present,
therefore real.

**Rule 1c — aliases are read off the table, not guessed.** Records **sharing an `id` are the
same verb**; `flags == 1` marks the alias spelling and the canonical carries `flags == 0`
(`auto_sync`=1 / `smart_play`=0, `config`=1 / `settings`=0, `hotcue`=1 / `hot_cue`=0). 61
alias groups, 73 alias forms. This retires the "in the table but with no `ACTION_` class"
derivation and it retires pairing-by-resemblance: never infer a pairing that the table states.

**Rule 1c2 — Button Editor categories come from the table too.** A `const char *[38]` name
array sits after the verb table and a non-decreasing `uint8[956]` in `__TEXT,__const` gives the
category per verb, indexed by `id + 1`. `just verb-table <name>` reports it. Do not infer a
category from `id` proximity — read it.

*Corrected 2026-07-29.* This was first written as "verified against the **independent** taxonomy
extraction's per-category counts". That was wrong, and the error is worth keeping visible because
it is the easiest one to make here: `extract_vdjscript_taxonomy.py` reads **the same three
structures**, differing only in that it pins virtual addresses where `extract_verb_table.py`
anchors on a string. Agreement between them is a *reproduction*, not corroboration, and cannot
confirm the mapping is right. What it does establish, on a genuinely different binary (bundle
`18.0.9336` → `18.0.9482`, different SHA-256): the table is stable across builds, and the
anchored locator lands on the same tables the pinned addresses did — including the same index
offset, since the pinned `category_ids_va` equals the anchored array start + 1.

The **provenance** is inherited from that older work, not established by anchoring:
`extract_vdjscript_taxonomy.py` found the tables via `DLGActionWizard` references, which is why
they are the *Button Editor's* categories, and why 38 compiled ids display as 37
(`DLGActionWizard::link` skips `defines`). An anchored walk proves the structure exists; it says
nothing about which UI consumes it. The only independent check on the mapping is Tier 1 — reading
the live Button Editor.

**Rule 1d — the table is not behavior.** It gives name, identity, and canonical-vs-alias, and
nothing else. Kind and behavior still come from the HTTP sweep and Tier-1 tests (rules 2-3).

**Rule 1e — locate it by anchoring, never by hard-coded address.** The extractor finds a known
verb string in `__cstring`, finds the record pointing at it, and walks outward while records
stay valid. That is why it works on a build where `extract_vdjscript_taxonomy.py`, which pins
virtual addresses, raises. Re-verify the record count after a VirtualDJ update.

**Rule 1f — a verdict is scoped to the inspected build**, and to the architecture slice read
(the arm64 slice of the universal binary; the x86_64 slice carries the same table).

**Rule 1g — corroborate, do not merely trust.** The table agreeing with 1,007/1,007
HTTP-proven names is what earns it authority here; a future structure claim needs the same
kind of independent check before it displaces this one.

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

## Tooling status (2026-07-29)

| Tool | State |
| --- | --- |
| `tools/extract_verb_table.py` | **Authoritative for existence, aliases, hidden flag, and category** (rule 1). Emits `tests/verb-table.json`; `just verb-table <name>`. |
| `tools/extract_action_contracts.py` | **Current for contract structure** (Tier 2): per-verb implementation class via the RTTI graph (a checked 955/955 bijection with verb-table ids), capability matrix from vtable overrides (slot meanings calibrated against HTTP-proven verbs at build time), family from the class hierarchy. Predicts; Tier-1 sweeps confirm. `just verb-contract <name>`. |
| `tools/sweep_return_types.py` | **Current for return type** (Tier 1): samples every HTTP query verb in three read-only contexts and classifies the answer (bool/int/float/percent/text). The authority for concrete rendered type — the structural matrix cannot supply it, because the generic query slot is a variant. `just verb-return-type <name>`. |
| `tools/sweep_verb_existence.py` | **Current for kind.** HTTP error-code sweep; `just verb-probe <name>`. Existence questions go to the verb table first; the sweep corroborates and classifies. |
| `tools/extract_binary_verbs.py` | **Corroboration only** — superseded by the verb table for every question it used to answer (rule 1a). Kept because its three sources (mangled `ACTION_` classes, language catalog, sorted name table) are genuinely different data from the verb table and so can still cross-check it. `just binary-verb <name>`. |
| `tools/extract_vdjscript_taxonomy.py` | **Stale on this build** (address-pinned) — and reads the *same structures* as `extract_verb_table.py`, so even when it ran it was never an independent check of it (rule 1c2). Its lasting contribution is provenance: it located the tables via `DLGActionWizard`, which is what ties them to the Button Editor. |
| `tools/extract_vdjscript_symbols.py` | **Stale on this build** — reports 0 `ACTION_*` classes, because the names now survive only as mangled strings and not as `nm`-visible symbols. Do not read its silence as absence. |

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
| `Verb table` | **1 for existence, aliases, hidden flag, category** | The single membership test (rule 1). Still Tier 2 for behavior. |
| `Binary symbol table`, and catalog entries | 2 | Corroboration for the verb table (rule 1a). Before the table was found these settled existence; now they only cross-check it. |
| `Binary compiled table`, `Binary string-table` | 2 | An unstructured string is not evidence of existence. The "conservative leg of a disproof" role is retired — absence from the verb table is disproof by itself (rule 1b). |
| `Community` | 3 | Record the test it suggests, not the claim. |
| `Inference` | 3 | Permitted only as explicitly-marked reasoning over Tier-1 facts, never as a finding. Do not let an inference acquire a source label by sitting next to one. |

## Writing a claim

1. State the claim as narrowly as the evidence supports — existence, kind, or behavior.
2. Name the tier or label, and for Tier 1 the build.
3. If it is a lead, name the test that would settle it.
4. If a claim is retracted, **say so in place** with what was wrong, rather than deleting it
   silently. A reader who acted on the old claim needs to find the correction.
