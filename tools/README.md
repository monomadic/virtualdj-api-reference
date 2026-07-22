# Tools

Scripts supporting the reference. Two groups: **offline** tools that run against repo content only (safe anywhere, wired into `just check`), and **extraction** tools that read a local VirtualDJ install (macOS, Apple Silicon) and are version-pinned.

## Offline: validators and generators

| Tool | Purpose | Recipe |
| --- | --- | --- |
| `check_reference_status.py` | Doc consistency: coverage-count cross-checks, broken local markdown links, test-fixture inventory completeness, no tracked Python cache files. | in `just check` |
| `lint_pads.py` | Pad XML: well-formed, `<page>` root, unique non-empty `name`, `pad_page` targets resolve, no `filter_selectcolorfx` inside `query=""`. | in `just check` |
| `lint_skins.py` | Skin XML vocabulary check: every element and per-element attribute must appear in the shipped-skin corpus (Built-In + SDK example); unknowns get closest-match suggestions. Catches the class of typo Atomix itself shipped (`ction=`, `hightlight=`), which the VirtualDJ parser silently ignores. Elements with `class=""` skip attribute checks (define-placeholder passing is arbitrary). Pass file paths to lint generated skins; `--strict` fails on findings. | `just lint-skins [paths]`, in `just check` |
| `lint_mappers.py` | Mapper XML: `<mapper device>` root schema, `<map value action>` structure, unknown attributes; leading verbs of each action statement resolved against the generated verb index (warnings with suggestions; `--strict` to fail). | `just lint-mappers [paths]`, in `just check` |
| `extract_xml_inventory.py` | Writes the data artifact `docs/skin-xml-inventory.json`: element×attribute usage across all XML corpora (`examples/`, `tests/`), cross-checked against the docs. Tolerant tokenizer (built-in skin XML is not well-formed). `--check` fails on newly undocumented elements. No Markdown view — query with `xmldb.py`. | `just inventory`, `--check` in `just check` |
| `extract_verb_index.py` | Generates `docs/vdjscript-verb-index.json`: machine-readable verb index parsed from `docs/VDJScript Verbs.md` (curated entries, catalog rows, alias table) unioned with the audit's official 991-name list. Consumed by `lint_mappers.py` and by `verbdb.py bootstrap`. `--check` fails when stale. | `just verb-index`, `--check` in `just check` |
| `fxdb.py` | Query API over the swept native effects catalog `tests/fx-introspection-dump.json`: `get <effect>` (spelling-tolerant; bare `fxdb.py <effect>` works too), `search` (filters: `--min/max-sliders`, `--min/max-buttons`, `--has-slider=LABEL`, `--has-button=LABEL`, `--in-cycle`, `--name-only`, `--format=json`), `stats`, `check`. No `put` — effect structure is machine-derived; re-run the sweep to refresh. | `just get-fx`, `just find-fx`, `just fx-stats`; `check` in `just check` |
| `verbdb.py` | Verb record store API over `docs/vdjscript-verbs.json` (authoritative, hand-editable; a bare `verbdb.py <name>` is shorthand for `get`): `get`/`put`/`next-incomplete`/`stats`/`search`/`check`, plus `bootstrap` (merge-safe seed from the index + coverage audit + tracker). Replaces the record-then-promote-to-three-docs cycle with one `put`. `search` filters on surface/section/tier/status/kind with `--format=json`, so reports are queries on stdout — no derived Markdown is written to disk, and nothing can go stale. `check` validates schema, alias resolution, index coverage, and count freshness. | `just get-verb`, `just find-verbs`, `just put-verb`, `just next-incomplete-verb`, `just verb-stats`; `check` in `just check` |

Regenerate order after editing verb docs or XML corpora: `just verb-index && just inventory && just check`.

## Live probe: running VirtualDJ required

These drive a running VirtualDJ over the [HTTP control interface](../docs/HTTP%20Control%20Interface.md) (`just vdj-up` to check reachability). They change live app state and their output is committed *evidence*, promoted with a `Local test` label — not directly authoritative docs.

| Tool | Does | Output |
| --- | --- | --- |
| `sweep_fx_introspection.py` | Cycles + by-name-selects the native deck-FX catalog into slot 1 and reads the introspection helpers (counts, short/full labels, live value text) per slider/button. Non-destructive (no resets). | `tests/fx-introspection-dump.json` |

## Extraction: local VirtualDJ required

These read `/Applications/VirtualDJ.app` (override with `--app`). They need macOS with Apple Silicon tooling (`nm`, `c++filt`, `otool`, `strings`) and produce *evidence*, which is hand-promoted into the docs with source labels — their output is not directly committed.

| Tool | Reads | Build sensitivity |
| --- | --- | --- |
| `extract_vdjscript_symbols.py` | Demangled `ACTION_*::onExecute/onQuery*` symbols from the executable | Works per-build; symbol names may drift |
| `extract_vdjscript_catalogs.py` | `Resources/languages.zip` action tags + executable string table, diffed against the coverage audit | String-block sentinels (`action_deck`…`zoom_vertical`) are content-anchored; verify hits on a new build |
| `extract_vdjscript_taxonomy.py` | Compiled Button Editor taxonomy tables via a hand-rolled Mach-O parser | **Hard-pinned**: default virtual addresses are for VirtualDJ `8.5.9307` / bundle `18.0.9336`; on any other build you must re-derive addresses and pass `--*-va` flags |
| `disassemble_vdjscript_parser_targets.py` | `otool -tV` disassembly of eight `DLGActionWizard` parser/highlighter symbols | Breaks if symbols are stripped or renamed |
| `extract_vdjscript_metadata.py` | Joins the four extractors into one summary/CSV | Inherits all of the above |

Usage examples live in the docs that consume them: `docs/Button Editor Taxonomy.md`, `docs/Button Editor Catalog Audit.md`, `docs/Undocumented VDJScript Candidates.md`, `docs/VDJScript Syntax Evidence.md`.

## New-VirtualDJ-build refresh procedure

When the installed VirtualDJ updates (check with `defaults read /Applications/VirtualDJ.app/Contents/Info.plist CFBundleVersion`):

1. **Refresh the shipped copies** using the commands in each provenance README, then review diffs and update the version/date lines there:
   - `examples/Pads/Built-In/README.md`
   - `examples/Skins/Built-In/README.md`
   - `examples/Samplerbanks/Built-In/README.md`
   (Copies may intentionally lag the installed build; each README records which bundle its files came from. As of 2026-07, pads/skins are from bundle `18.0.9336` while samplerbanks are from `18.0.9482`.)
2. **Re-run the offline suite** — `just verb-index && just inventory && just check` — and resolve anything the inventory or link checker flags from the refreshed XML.
3. **Re-anchor the binary tools** if you need fresh compiled-table evidence: `extract_vdjscript_symbols.py` and `extract_vdjscript_catalogs.py` usually work as-is; for `extract_vdjscript_taxonomy.py`, re-derive the three table addresses for the new binary and pass them via `--*-va` (the process notes are in `docs/Button Editor Taxonomy.md`). Update the Evidence Baseline block (version, bundle, SHA-256) in `docs/Undocumented VDJScript Candidates.md`.
4. **Refresh the coverage audit** only when intentionally re-fetching the live official appendix; `docs/Official VDJScript Coverage Audit.md` records its own refresh date, and `check_reference_status.py` keeps the counts consistent afterwards.
