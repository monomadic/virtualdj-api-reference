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
| `fxdb.py` | Query API over the swept native effects catalog `tests/fx-introspection-dump.json`: `get <effect>` (spelling-tolerant, resolves aliases; bare `fxdb.py <effect>` works too), `search` (filters: `--min/max-sliders`, `--min/max-buttons`, `--has-slider=LABEL`, `--has-button=LABEL`, `--category=deck_fx\|video_fx\|transition`, `--has-length`, `--in-cycle`, `--name-only`, `--format=json`), `stats`, `check`. `get` warns before answering when the asked name is one the sweep could not resolve, so a near-miss match (`Brake` → `Beat Brake`) cannot pass for a real selector name. No `put` — effect structure is machine-derived; re-run the sweep to refresh. | `just get-fx`, `just find-fx`, `just fx-stats`; `check` in `just check` |
| `verbdb.py` | Verb record store API over `docs/vdjscript-verbs.json` (authoritative, hand-editable; a bare `verbdb.py <name>` is shorthand for `get`): `get`/`put`/`next-incomplete`/`stats`/`search`/`check`, plus `bootstrap` (merge-safe seed from the index + coverage audit + tracker). Replaces the record-then-promote-to-three-docs cycle with one `put`. `put` refuses an unknown name with did-you-mean suggestions so a typo cannot mint a junk record; a genuinely unofficial name (scope wrapper, hidden candidate) needs an explicit `--new`, which records it as `tier=unofficial, official=false` rather than silently claiming official status. `evidence=` appends one entry verbatim (it is prose, so it is not comma-split); `aliases=`/`surfaces=` still take comma lists. `search` filters on surface/section/tier/status/kind with `--format=json`, so reports are queries on stdout — no derived Markdown is written to disk, and nothing can go stale. `check` validates schema, alias resolution, index coverage, and count freshness. | `just get-verb`, `just find-verbs`, `just put-verb`, `just next-incomplete-verb`, `just verb-stats`; `check` in `just check` |

| `topic.py` | Cross-corpus topic search: one term → matching verbs (store), effects (FX catalog), skin/pad XML elements (inventory), the **real example files that use them** (ripgrep with word boundaries, ranked by coverage), topical docs, and local-test quirks/candidates. Pure aggregation over the already-gated stores — no artifact of its own, nothing to hand-tag; everything is derived from `section`, inventory families, and grep. `check` is a cross-store smoke test (schema drift upstream would break it). Known gap: elements whose family topic is not in their name (waveform's `rhythmzone` etc.) are reachable only via the DOCS pointer until items carry topic tags. | `just topic <term> [--format=json --limit=N]`; `check` in `just check` |

Regenerate order after editing verb docs or XML corpora: `just verb-index && just inventory && just check`.

## Live probe: running VirtualDJ required

These drive a running VirtualDJ over the [HTTP control interface](../docs/HTTP%20Control%20Interface.md) (`just vdj-up` to check reachability). They change live app state and their output is committed *evidence*, promoted with a `Local test` label — not directly authoritative docs.

| Tool | Does | Output |
| --- | --- | --- |
| `sweep_verb_existence.py` | Queries every store name plus the candidates-doc names bare and buckets the HRESULT: a value (query verb), `E_NOTIMPL` (action-only), `E_INVALIDARG` (takes arguments), `E_ACCESSDENIED` (context-gated), `S_FALSE`, or `E_FAIL` (unresolved). Read-only. Proves existence and kind, NOT behavior — never a substitute for a recorded local test. Query it with `just verb-probe <name>`. | `tests/verb-existence-sweep.json` |
| `sweep_fx_introspection.py` | Enumerates the enabled cycle for all three targets (deck FX / video FX / transition), resolves every known name to its canonical spelling via `get_effect_title`, then reads counts, short/full labels, normalized defaults, live value text, and length/beats flags per effect. Introspection is read-only — the `get_effect_*` helpers accept an effect *name* in place of the slot, so no selection is needed except for the two names `get_effect_title` is blind to. Restores the video-FX and transition selections it changed. | `tests/fx-introspection-dump.json` |

## Remote protocol: running VirtualDJ, one device for capture

These speak the [VirtualDJ Remote protocol](../docs/Remote%20Protocol.md) — a separate
channel from the HTTP interface, on Bonjour `_vdjremote8._tcp` / port 4243. Roles are
inverted: the *device* is the TCP server, so both tools act as a device and VirtualDJ dials
in. Pair them with an advert (`dns-sd -R "iPad" _vdjremote8._tcp . 4243`, using a name
VirtualDJ already lists); if it does not dial, drop and re-add the registration.

| Tool | Does | Output |
| --- | --- | --- |
| `vdjremote_dial.py` | Dials a real Remote device (which speaks first) and captures its opening handshake, or `--decode`s a saved capture into a frame listing. The only step needing a phone/tablet. | `tests/vdjremote-opener.bin` |
| `vdjremote_subscribe.py` | Impersonates a device: reuses a capture's setup/info/panel prefix, substitutes your own VDJScript subscriptions, and prints every pushed value. Needs no device. | stdout |

Read-only in practice — subscriptions only observe — but they do hold a live Remote session,
and VirtualDJ lists the fake device in Config → Controllers → Phone/tablet until removed.

## Plugin channel: a read-only plugin loaded into VirtualDJ

The fifth Tier-1 channel (TODO task 10a). HTTP renders every answer to text; the C++ plugin
interface does not, so `GetInfo` (a `double`) and `GetStringInfo` (a UTF-8 buffer) are asked
separately and **which channel a verb answers on is observed, with raw HRESULTs**. Needs the
Atomix SDK headers under `vendor/` — deliberately not vendored, see
[Plugin SDK](../docs/Plugin%20SDK.md) and `.gitignore`.

| Tool | Does | Output |
| --- | --- | --- |
| `plugin/VDJIntrospect.cpp` | The plugin itself. Reads a probe list at load, calls both query callbacks per probe, writes the raw capture. **Read-only by construction: the source contains no `SendCommand` call at all**, so no probe list can reach execute position. Logs every `DllGetClassObject` negotiation, which is itself evidence for the open second-loading-path question. | `~/Library/Application Support/VirtualDJ/VDJIntrospect/{results.json,plugin.log}` |
| `plugin/build.sh` | Builds and ad-hoc signs `build/VDJIntrospect.bundle`; `--install` copies it into the plugin folder. Command Line Tools `clang++` is enough — **no Xcode required**. | `build/VDJIntrospect.bundle` |
| `plugin_introspect.py` | `prepare` writes the probe list from the verb table; `status` shows the workdir and log tail; `collect` normalizes the raw capture (naming HRESULTs, classifying the answering channel); `--get`/`--check` query and gate it. `--check` passes with an explicit skip until the first capture exists. | `tests/plugin-introspection.json` |

Order: `just plugin-build --install` → restart VirtualDJ → `just plugin-prepare` → restart
again (the sweep runs at plugin load) → `just plugin-status` → `just plugin-collect`.

Two things that bite. **Each capture costs a VirtualDJ restart**, because the sweep runs when
the plugin loads. And **a load-time probe can be too early**: `OnLoad` fires while VirtualDJ is
still starting, so an uninitialized subsystem (the browser) answers `E_INVALIDARG` exactly as a
nonexistent form would. Use `prepare --late` to write `probes-late.txt`, which the plugin
sweeps again ~40s after load from a timer thread, and re-take any negative there before
believing it. `prepare --remaining` emits the execute-capable keyword verbs (query position
only, unsafe families excluded and printed); `just plugin-keyword-report <capture>` splits
every keyword against its nonsense control.

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
