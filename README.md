# VirtualDJ API Reference

Community-maintained reference for VirtualDJ skinning, pad pages, and VDJScript.
VirtualDJ does not publish a comprehensive developer reference; this repo fills that gap.

## What is here

- **`docs/`** — Markdown documentation: VDJScript verb reference, skin SDK, waveform elements, pad-page schema, effects, options, filter syntax, mapper format, application internals
- **`examples/Pads/`** — focused pad page XML examples for ColorFX, samplers, cues, transport, reference patterns, and copied built-in pad pages; see [examples/Pads/README.md](examples/Pads/README.md)
- **`examples/Skins/`** — skin examples, copied built-in skins, and build-system demos; GraveRaver is intentionally minimal and only demonstrates the XInclude workflow
- **`examples/Mappers/`** — real working controller/keyboard mapper XML copied from a local install; ground truth for the mapper format
- **`examples/Samplerbanks/`** — sampler-bank XML copied from the app bundle (a third XML format alongside skins and pads)
- **`examples/VideoSkins/`** — built-in video skins (broadcast, karaoke, live) copied from the app bundle; same `<skin>` format as deck skins, rendered onto the video output
- **`tests/`** — reproducible documentation test harnesses, pad-page XML fixtures, and the **extracted data artifacts**: `verb-table.json` (the authoritative verb set), `action-contracts.json` (per-verb implementation contract), `verb-return-types.json` (observed types and boolean truth), `verb-existence-sweep.json`
- **`tools/`** — extractors, sweeps, linters and the `just` query API; every artifact is regenerable and gated by `just check`

## Where to start

| Goal | File |
| --- | --- |
| **Answer anything about one verb** | `just get-verb <name>` — joins every artifact: existence, category, aliases, implementation class, capability, argument demands, keyword arguments, observed return type, boolean truth |
| Pick the next active maintenance task | [TODO.md](TODO.md) |
| Route a topic to the right docs and fixtures | [INDEX.yml](INDEX.yml) |
| Understand the repo structure and source labeling | [docs/README.md](docs/README.md) |
| Pick the right VDJScript verb or pattern | [docs/VirtualDJ Reference.md](docs/VirtualDJ%20Reference.md) |
| Look up a specific verb | [docs/VDJScript Verbs.md](docs/VDJScript%20Verbs.md) |
| Check official verb coverage | [docs/Official VDJScript Coverage Audit.md](docs/Official%20VDJScript%20Coverage%20Audit.md) |
| Choose the next completeness pass | [docs/Completeness Roadmap.md](docs/Completeness%20Roadmap.md) |
| Choose or maintain a pad page | [examples/Pads/README.md](examples/Pads/README.md) |
| Look up the pad-page XML format | [docs/Pad Page XML.md](docs/Pad%20Page%20XML.md) |
| Build skin waveforms | [docs/Skin Waveforms.md](docs/Skin%20Waveforms.md) |
| Check skin/pad XML doc coverage | `just find-xml-elements --undocumented` (data: [docs/skin-xml-inventory.json](docs/skin-xml-inventory.json), refreshed by `just inventory`) |
| Look up verbs programmatically | [docs/vdjscript-verb-index.json](docs/vdjscript-verb-index.json) (generated; `just verb-index`) |
| Validate skin/mapper XML | `just lint-skins [paths]` · `just lint-mappers [paths]` · [tools/README.md](tools/README.md) |
| Run or update a test harness | [tests/README.md](tests/README.md) |
| Build or study a skin | [docs/Skin SDK.md](docs/Skin%20SDK.md) · [docs/Skin Runtime Findings.md](docs/Skin%20Runtime%20Findings.md) · [examples/Skins/README.md](examples/Skins/README.md) · [examples/Skins/ModularSkeleton/](examples/Skins/ModularSkeleton/) |
| Work with effects | [docs/Effects Usage.md](docs/Effects%20Usage.md) · [docs/Native Effects.md](docs/Native%20Effects.md) |
| Map a controller or keyboard | [docs/Mapper XML.md](docs/Mapper%20XML.md) |
| Write a native plugin, or understand where VDJScript results are still typed | [docs/Plugin SDK.md](docs/Plugin%20SDK.md) |
| Understand macOS paths and databases | [docs/Application Internals.md](docs/Application%20Internals.md) |
| Inspect or create `.vdjstems` sidecars | [docs/Stem File Format.md](docs/Stem%20File%20Format.md) |

## Agent Entry Point

`AGENTS.md` is intentionally retained for Claude, Codex, and other coding
agents that look for that filename. This `README.md` is the human-facing
overview; `AGENTS.md` keeps the operational shortcuts and repo-specific guardrails.

## Reliability

Every fact in the reference docs is labeled by source:

| Label | Meaning |
| --- | --- |
| `Official` | Current VirtualDJ manual or VDJPedia |
| `Official forum` | Post by VirtualDJ staff, CTO, or support |
| `Community` | Non-staff forum guidance |
| `Published skin` | Observed in a working public skin |
| `Built-in skin` | Observed in skin XML shipped inside the VirtualDJ app bundle |
| `Published pad page` | Observed in a working public pad page |
| `Built-in pad page` | Observed in pad-page XML shipped inside the VirtualDJ app bundle |
| `Built-in app resource` | Command name, description, or UI catalog entry observed in non-skin/non-pad app resources |
| `Verb table` | VirtualDJ's own serialised verb set, extracted from the binary — **decides existence outright** |
| `Binary compiled table` | Structured command metadata observed in compiled executable tables |
| `Binary symbol table` | Demangled implementation symbols observed in the VirtualDJ executable |
| `Binary string-table` | Command-looking string observed in the VirtualDJ executable; discovery only |
| `Action catalog` | The Button Editor's own description for a verb, shipped in `languages.zip` — the same prose the official appendix publishes, readable offline |
| `Vendor script` | A form Atomix wrote into a shipped Built-In pad page or skin — attested usage, no probe required |
| `Local test` | Reproduced in VirtualDJ locally |
| `Inference` | Conclusion drawn from the above sources |

Unlabeled files are raw material not yet normalized to this standard.
[docs/Evidence Standards.md](docs/Evidence%20Standards.md) governs every claim: three tiers,
what counts as a behavioral test, and why a channel's own return value is never a result.

## Status (2026-09-03)

### What a verb's arguments accept is now three-sourced

The reference used to document verb *names* well and their *arguments* barely. Three
independent sources now cover the tail of a statement, and `just action-catalog --cross-check`
prints them against each other:

- **`tests/action-catalog.json`** — 816 vendor descriptions extracted from the app bundle
  (`languages.zip` carries the official appendix's prose, so it is available offline). The only
  source that says what a parameter *means*.
- **`tests/attested-tails.json`** — 214 tails Atomix wrote into shipped skins, pad pages and
  the app's own compiled menu scripts, plus 410 argument *shapes* (`` fadeout DUR DUR `BOOL` ``,
  `param_bigger EXP:NUM EXP:NUM`, the `deck SEL EXP` wrapper) with
  the return type the vendor's attribute implies, for the verbs whose arguments are values
  rather than keywords. Attested without a probe, which reaches where no test state can.
- **`tests/binary-vocabularies.json`** — argument vocabularies as *groups*, recovered from the
  binary as structures (pointer tables, switch functions): the 38 colour names, the 5 stems,
  the 19 settings pages. The only source that sees an enumeration matched in a shared helper
  rather than in the verb's own code. Leads, not confirmations.
- **`tests/verb-arg-forms.json`** — every candidate probed against two nonsense controls inside
  10 named fixtures, because VirtualDJ silently ignores an argument it cannot parse, so a verb
  answering proves nothing on its own.

Agreement across all three is the strongest claim this project makes; 9 verbs have it today.

### Traps that will bite anyone writing VDJScript, added this cycle

- A **misspelled argument usually makes the action do nothing**, and on some verbs degrades to
  the bare action instead. Neither is reported as an error.
- **Relative and multiplying arguments are execute-only.** `loop 50%` halves a loop rather than
  setting one, and asking a query for it errors.
- **`deck all` broadcasts on execute but collapses to deck 1 on query** — the same line means
  two different things depending on position.
- **`timecode_cd_mode` latches**: script can set it and cannot unset it; only a restart clears.
- The sampler's **`all` means the selected slot**, not every slot.

## Status (2026-07-30)

### VDJScript is no longer a guessing game

The verb set, each verb's contract, and the grammar are now derived from VirtualDJ itself
rather than assembled from documentation.

| Question | Answer | How |
| --- | --- | --- |
| Is `x` a verb? | **Decided, both ways** | VirtualDJ's own verb table — 1,028 records, 955 distinct verbs, 61 alias groups, 37 editor-hidden. Membership proves; absence disproves. `just verb-table <name>` |
| What category is it in? | All 1,028 mapped | Compiled Button Editor category tables, confirmed against the live UI |
| Can it execute / query / return text? | All 955 | `ACTION_` class RTTI — a checked 955↔955 bijection of verbs to implementation classes. `just verb-contract <name>` |
| What type does it return? | 623 of 652 query verbs | Live HTTP sweep. `just verb-return-type <name>` |
| Does it take arguments? | 436 verbs flagged, incl. **301 with optional args** | `E_INVALIDARG` fingerprint in each class's own methods |
| Which keyword arguments? | 259 verbs | String-comparison fingerprint — recovered `get_bpm absolute`, `browser_window sidelist`, `loaded opposite` and 200+ more that no documentation lists |

### Traps now documented that will bite anyone writing VDJScript

- **A verb's value is not its truth.** `get_version` reports `2026` and is **false** as a
  condition. **171 of 652** query verbs are traps, and *no slider verb is ever true*.
- **`&&` is not an operator.** It never guards anything; it only changes which statement's
  value a query reports.
- **Chains stop after exactly 255 statements**, partially, returning `false`.
- **GET refuses scripts over ~2,650 characters** at the transport layer — which looks exactly
  like a language failure and caused a documented rule to be wrong for months. Use POST.
- Chained ternaries are a genuine else-if ladder; each branch takes its whole `&` chain.

### Other areas

- Skin SDK coverage is broad; the waveform element family is in `docs/Skin Waveforms.md`, and
  remaining element gaps are tracked mechanically (`just find-xml-elements --undocumented`).
- Controller mapper XML is rewritten around the real `<map value="">` + device-definition
  split, with working mappers in `examples/Mappers/Local/`. Custom device-definition XML is
  official-doc-derived and still not load-tested.
- The **VirtualDJ Remote** wire protocol is decoded and proven bidirectional
  ([docs/Remote Protocol.md](docs/Remote%20Protocol.md)).
- The **plugin SDK** is now documented ([docs/Plugin SDK.md](docs/Plugin%20SDK.md)): interface
  hierarchy, the `VDJPARAM_*` model and the `[autoparams]` manifest all 173 built-in plugins
  use, plugin UI models, and the interfaces present in the binary that the public headers never
  declare. It is the boundary where VDJScript results are still typed — `GetInfo` → `double`,
  `GetStringInfo` → text — which is both *why* the HTTP channel flattens them and the basis of
  the next session's primary plan below. Headers are third-party with no license grant, so they
  are fetched to a gitignored `vendor/` rather than committed.

### Recommended next steps

1. **Build the verb index from the artifacts, not from prose** ([TODO.md](TODO.md) task 11) —
   `extract_verb_index.py` still parses the 6,300-line `VDJScript Verbs.md` to produce
   `vdjscript-verb-index.json`, so where the prose and the extracted evidence disagree, the
   prose wins silently and nothing gates it. The reconciliation diff is the real prize: every
   discrepancy is either a documented claim the artifacts contradict, or a curated fact the
   store has no field for.
2. **Build the state-fixture harness and argument prober** ([TODO.md](TODO.md) task 10b) —
   the cheap unblock, Python over the existing HTTP channel. The blocker on argument forms is
   not the channel but *prepared state*: unknown arguments are silently ignored
   (`loaded bogusword` → `yes`), so a form is only confirmable by comparing it against both
   bare and a **nonsense control** in a state where they would disagree. That settles the
   217 undocumented keyword sets and the 301-verb optional-argument queue.
3. **Build the read-only introspection plugin** ([TODO.md](TODO.md) task 10a). Its value is
   *not* verb throughput — the 2026-07-30 sweeps ran ~3,000 HTTP probes in minutes. It is the
   only channel for things nothing else reaches: `GetSongBuffer` and `OnProcessSamples` give
   the actual PCM behind every waveform element; `OnKey(ch, vkey, modifiers, flag, scancode)`
   is the first channel that may expose press/release, which HTTP structurally cannot;
   `VDJINTERFACE_SKIN` turns skin testing from edit-and-restart into a loop. For verbs
   specifically, one real edge: `GetInfo` returns an **HRESULT separately from the value**,
   which HTTP flattens — the one way to tell a recognized keyword from an ignored one. Headers
   are fetched to a gitignored `vendor/`, never committed — Atomix grants no redistribution
   license.
4. **Behavior for ~940 verbs is still untested.** Existence, kind, category, capability and
   return type are settled; what a verb *does* mostly is not.
5. **Audit the remaining `Inference` and `Community` labels** against
   [docs/Evidence Standards.md](docs/Evidence%20Standards.md), which does not permit either as
   a standing claim.
6. **HTML export** of the reference is parked in [TODO.md](TODO.md) and now worth doing — the
   per-verb pages finally have real content to show.

Contributions and corrections welcome. Corrections especially: several long-standing claims
were overturned this session by re-testing them on a second channel, and the repo records
retractions in place rather than deleting them.
