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

## Four rules that today's work earned

### 1. The binary can DISPROVE, though it cannot prove

The tiers above are about proving something *works*. Absence is different, and the binary is
the only instrument we have for it. The calibrated two-part test — no mangled
`ACTION_<name>` symbol **and** no bare `<name>` string in the executable — is **proof-grade
for non-existence on the inspected build**, because the parser needs the literal in order to
dispatch on it. Calibration and caveats: [Undocumented VDJScript Candidates.md](Undocumented%20VDJScript%20Candidates.md)
§"Disproving A Name" (no false negatives across 1,007 names for names of ≥4 characters).

This is the one asymmetry in the scheme: binary evidence is a Tier-2 *lead* about what
exists and does something, and Tier-1-grade about what does **not** exist.

### 2. Existence, kind, and behavior are three different claims

Do not let one become another. The HTTP error-code sweep proves a name is **real** and
classifies its **kind** (query / action-only / takes-arguments / context-gated). It says
nothing about what the verb *does*. `test_status=Pass` in the verb store means behavior was
observed, so an existence probe must never set it. State the claim you actually have:

> `clear_search` exists and is action-only (`E_NOTIMPL`, HTTP sweep 2026-07-27). Behavior
> untested.

### 3. A channel's own return value is not a result

Proof requires independent readback. Established cases:

- `/execute` returning `true` does not mean the action succeeded — `deck 2 load
  "<nonexistent path>"` returns `true` and leaves the deck in an error state.
- `/execute` returning `false` does not mean failure — it is the verb's own boolean.
- `E_FAIL` from `/query` is silence, not denial. A real, binary-confirmed verb
  (`remote_action`) returns it.
- A Remote-protocol `fail` value means "no value right now", not "bad query".

So: send, then **query the state independently**, and record that.

### 4. Provenance must be established independently of the artifact's own metadata

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
| `Binary compiled table`, `Binary symbol table`, `Binary string-table` | 2 | Tier-1-grade for **absence** only, via the two-part test. |
| `Community` | 3 | Record the test it suggests, not the claim. |
| `Inference` | 3 | Permitted only as explicitly-marked reasoning over Tier-1 facts, never as a finding. Do not let an inference acquire a source label by sitting next to one. |

## Writing a claim

1. State the claim as narrowly as the evidence supports — existence, kind, or behavior.
2. Name the tier or label, and for Tier 1 the build.
3. If it is a lead, name the test that would settle it.
4. If a claim is retracted, **say so in place** with what was wrong, rather than deleting it
   silently. A reader who acted on the old claim needs to find the correction.
