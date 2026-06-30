# VDJScript Reference Consolidation Plan

A plan for turning the VDJScript reference from one large, partly-redundant catalog into a
small, navigable, best-of-class set of documents — without losing the official-name coverage
guarantee and without inventing syntax along the way.

This document practices what it preaches: it is short, it states rules instead of restating
them per section, and it leaves the verbose, structured detail for the few places that earn it.

## Why change anything

The reference already works. It has 991/991 official-name coverage, source labels, a coverage
audit, a local-test tracker, a routing index, and `just` helpers. The problem is not coverage.
The problem is **noise and duplication**:

- `VDJScript Verbs.md` is ~244 KB. Answering one verb question means loading or grepping a
  monolith that mixes a curated layer with a still-normalizing broad catalog.
- The same fact lives in several files. Aliases appear in the Verbs.md alias index, the coverage
  audit, and would have appeared again in a per-verb index. Surfaces, "needs local test," and
  examples are similarly scattered. Every duplicate is a place to drift.
- There is no single rule for *where a fact is authored* versus *where it is derived*.

So the goal is not "more documentation." It is **one authored home per fact, everything else
generated, and depth only where depth pays for itself.**

## Principles

These govern every decision below. If a step violates one of these, change the step.

1. **Single source of truth.** Each fact is authored in exactly one file. Alias maps, surface
   indexes, and gap reports are *generated* from that source, never hand-maintained alongside it.
2. **Lean by default, deep on evidence.** A verb's default form is one compact, machine-readable
   row. It earns a structured contract only when it has real, non-obvious detail to record.
3. **Generate, don't duplicate.** If two views of the same data must both exist, one is authored
   and the other is produced by a `just` recipe. Never two hand-edited copies.
4. **Author for the reader, extract for the tool.** The primary consumer is a human or agent
   reading prose, so author readable Markdown — but give each entry a small, fixed,
   machine-parseable shape so tooling can extract aliases/surfaces/confidence without guessing.
5. **Honesty beats polish.** An explicit `needs_test` is more valuable than a confident guess.
   The structure must make "we don't know" cheap to write and obvious to read.
6. **Smaller context loads.** An agent should be able to read exactly the family it needs, not a
   quarter-megabyte monolith.

## Division of ownership

This is the heart of the plan. Each fact has exactly one authoring home.

| Fact | Authored in | Derived from it |
| --- | --- | --- |
| Official name exists / parity count | `Official VDJScript Coverage Audit.md` | — (canonical, unchanged role) |
| Build/hardware/context test result | `VDJScript Local Test Tracker.md` | — (canonical, unchanged role) |
| Canonical name, aliases, surfaces, syntax, behavior, examples | `VDJScript/families/<family>.md` | alias index, surface index, gap report |
| Precise multi-form signature detail for hard verbs | `VDJScript/contracts/<verb>.md` | (feeds the same indexes) |

Nothing else authors aliases or surfaces. The Verbs.md alias index and any per-verb index become
**generated artifacts** (or disappear). That single change removes most of the current drift risk.

## Target structure

```text
Reference/
  Official VDJScript Coverage Audit.md      # unchanged role: names-only parity, the gap count
  VDJScript Local Test Tracker.md           # unchanged role: build-specific results
  VDJScript/
    README.md                               # how the reference is organized; the two tiers; labels
    families/                               # ~12-20 files; the authored home for most verbs
      transport.md
      cue-loop.md
      sync-tempo.md
      deck-metadata.md
      effects-slot.md
      effects-color.md
      sampler.md
      pads.md
      browser-sideview.md
      skin-panels.md
      variables-flow.md
      environment.md
    contracts/                              # full contracts ONLY for high-value, non-obvious verbs
      effect_select.md
      sampler_pad.md
    generated/                              # never hand-edited; produced by `just`
      aliases.md
      surfaces.md
      signature-gaps.md
```

`VDJScript Verbs.md` is not in this tree on purpose. During migration it stays as the fallback
catalog; at the end it is either deleted or replaced by a short, generated landing page that links
into the families. The official-name coverage guarantee is preserved by the checker, not by the
monolith.

## The two tiers

Most verbs are a **row**. A few are a **contract**. The line between them is the whole point — it
is what keeps the reference small.

### Tier 1 — compact row (the default)

Every verb appears as one row in its family file. The columns are fixed so a generator can parse
them. This is also close to today's table shape, so it is a small change, not a rewrite.

```md
| Verb | Aliases | Surfaces | Confidence | Notes |
| --- | --- | --- | --- | --- |
| `get_hwnd` | — | Text, SkinQuery | official_sparse | Windows native window handle; macOS return unverified. Diagnostics only. |
```

- **Surfaces** use the existing legend: `Map`, `Button`, `Pad`, `SkinAction`, `SkinQuery`, `Text`.
- **Confidence** uses the existing source-label vocabulary distilled to one token:
  `official`, `official_sparse`, `built_in`, `published`, `local_test`, `inference`,
  `discovery_only`.
- A sparse official name with no observed behavior is **one row**, never a contract. Its honest
  Notes cell is "exists per official appendix; behavior untested."

### Tier 2 — full contract (earned, not default)

A verb graduates to `contracts/<verb>.md` only if **at least one** of these is true:

- it has two or more distinct argument forms with different behavior,
- its return/query shape (truthiness, empty state, units) is non-obvious and matters for codegen,
- a surface has a real caveat (e.g. works in pad query but not skin text),
- it has a known unreliable form that must be documented to steer agents away from it.

Otherwise it stays a row. Expect the contract set to be ~40-80 verbs, not 991.

The contract is a lean YAML block inside a readable Markdown file. Only the load-bearing fields
are required; optional blocks appear **only when they carry information** (no skeletons of
`needs_test` placeholders).

````md
# `effect_select`

```yaml
verb: effect_select
aliases: [fx_select]
kind: action                 # action | query | text | dual
surfaces: [map, button, pad, skinaction]
forms:
  - sig: "effect_select <slot> 'Name'"
    returns: none
    note: select an FX by name into a numbered slot
    confidence: local_test
  - sig: "effect_select <slot> <index>"
    returns: none
    confidence: built_in
needs_test: []
# optional blocks below — include ONLY when they say something
# platforms: { windows: supported, macos: needs_test }
# deck_scope: { accepts_deck_prefix: true, default: current_deck }
```

## Notes
Short prose for decisions an implementing agent needs. Keep it to what the YAML cannot say.
````

The family row for a contracted verb stays, with its Notes cell pointing at the contract. The row
is generated from the contract's front-matter so the two never disagree.

## Tooling first

Build the generators and checkers **before** moving any prose. They deliver value against the
current files, and they prove the parse-shape works before it is depended on.

Add to the `justfile`:

- `just verbs-index` — regenerate `generated/aliases.md` and `generated/surfaces.md` from the
  family rows and contract front-matter. Deterministic; no network.
- `just signature-gaps` — non-failing report: official names from the coverage audit that have a
  family row, that lack one, aliases that resolve to a real canonical, and contracts still marked
  `needs_test`.
- Extend `just check` (currently `lint_pads.py` + `check_reference_status.py` + `git diff --check`)
  with `check_vdjscript_refs.py` that verifies:
  - every official name in the audit appears in a family row or contract,
  - every alias resolves to a canonical that exists,
  - every `needs_test` entry has a matching Local Test Tracker row or an explicit reason,
  - every contract parses and has the required keys.
- The checker **reports** during migration and only **fails** on a malformed migrated file, so a
  half-migrated repo stays green.

If the parse-shape can't be extracted reliably from the current tables, fix the row shape now,
while there is one file to fix — not after it is split into twenty.

## Migration sequence

Phased, highest-traffic family first, with a real stop-and-evaluate gate after the first one.

- **Phase 0 — Tooling.** Add the generators and checker against the *existing* `VDJScript Verbs.md`.
  No restructure yet. Land `generated/` as derived output. Confirm `just check` stays green.
- **Phase 1 — One family, end to end.** Pick the highest-traffic family (transport or FX slot).
  Create `VDJScript/families/<family>.md` with compact rows, write ≤5 contracts for its hard verbs,
  regenerate indexes, and **delete those rows from `VDJScript Verbs.md`**. The monolith shrinks by
  exactly what the family file gains — net files up, net bytes flat, net duplication down.
  **Then stop.** Did context load drop? Is the family file genuinely easier to use than the
  monolith slice it replaced? Only continue if the answer is clearly yes.
- **Phases 2..N — Remaining families.** Repeat in descending traffic order. Each pass is
  self-contained and leaves the repo green.
- **Final phase — Retire the monolith.** When the last family is extracted, replace
  `VDJScript Verbs.md` with either a short generated landing page or nothing, repoint
  `INDEX.yml`, `AGENTS.md`, and `Reference/README.md`, and make the coverage guarantee the
  checker's job.

Suggested family order (traffic-first): transport → effects-slot → sampler → deck-metadata →
cue-loop → browser-sideview → skin-panels → effects-color → variables-flow → sync-tempo → pads →
environment.

## Definition of done (per family pass)

- Every verb in the family is a compact row in its family file.
- Verbs that meet the graduation bar — and only those — have a contract; the rest stay rows.
- Aliases and surfaces are present in the authored rows/contracts and **nowhere else**;
  `generated/` is regenerated and reflects them.
- The equivalent rows are removed from `VDJScript Verbs.md` (no parallel copy survives).
- Unverified behavior is marked `needs_test` with a tracker row or an explicit reason.
- `just check` passes; `just signature-gaps` shows no regressions.

## Anti-goals

The ways this plan fails if we are not careful:

- **Recreating the duplication.** If aliases or surfaces end up authored in both a family row and a
  generated index, we have rebuilt the problem. Generated files are read-only output.
- **Contract sprawl.** If most verbs get contracts, the reference is bigger and noisier than the
  monolith it replaced. Hold the graduation bar. When in doubt, it's a row.
- **Skeleton padding.** A 60-line contract that is mostly `needs_test` is noise wearing a contract's
  clothes. Optional blocks stay absent until they carry information.
- **Overconfident sparse names.** The oldest failure mode: turning a searchable but sparse official
  name into invented API detail. A truthful row beats a polished guess. Promote depth only on
  evidence from official examples, built-in XML, or a local test.
- **A permanently half-migrated repo.** Avoid by making each family pass complete and green, and by
  deleting the monolith rows in the same pass that adds the family file — never "later."
