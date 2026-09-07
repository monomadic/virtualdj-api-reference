# TODO

This is the operational queue for open-ended VirtualDJ reference work.

Agents should start here for maintenance, cleanup, documentation, and evidence-pass tasks. Pick the first `Ready` task unless the user names a different task. Read the task-listed files before running broad repository searches.

## Queue Rules

### Status convention

Every `### <id>. <title>` task carries exactly one status line, and it is the first line under
the heading:

```
Status: <state>
```

The state is one word from a closed vocabulary and nothing else — no date, no bold, no
qualifier, no trailing prose. Everything else goes in a `Note:` paragraph directly below it.
This is machine-readable on purpose: `just next-task` parses it, and a status line it cannot
read stops the run instead of quietly skipping the task.

| State | Meaning |
| --- | --- |
| `Ready` | Startable now with the listed files and fixtures. Launching VirtualDJ locally counts as startable. |
| `Blocked` | Needs hardware or an external source not available here. |
| `Conditional` | Start only when the named trigger occurs; the `Note:` names it. |
| `Parking lot` | Useful later, but not the next best use of time. |
| `Done` | Complete; kept as the record of what was established. |

The state describes the task **now**. For a task whose first pass landed with work remaining,
it describes that remaining work — `Ready` if the remainder is startable, `Blocked` if it is
not — and the `Note:` carries what already landed. Task identifiers must be unique;
`just check` fails on a duplicate.

### Working rules

- Record manual VirtualDJ observations in [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md).
- Promote stable conclusions into the topical docs named by the task.
- Run `just check` after documentation, fixture, or status edits.
- `Read first` lists are section-scoped: read only the named rows/sections. Use `just grep-verb-docs <name>` for verb lookups instead of opening `docs/VDJScript Verbs.md`.
- [docs/VDJScript Reference Consolidation Plan.md](docs/VDJScript%20Reference%20Consolidation%20Plan.md) and [docs/Completeness Roadmap.md](docs/Completeness%20Roadmap.md) are frozen design references. Do not refresh, reorder, or re-scope them; this file is the only active queue.

## Accepted next sequence (2026-09-05 review)

This sequence takes precedence over the historical task ordering below. It reconciles the
review into this queue; the dated assessment is not another worklist. Existing task numbers
remain the owners of their broader work. Read their scoped evidence before probing.

### R1. Repair queue selection

Status: Done

Note: 2026-09-05. The convention, the parser, and the regression fixtures are in place; every
task in this file now carries a readable status.

What the selector used to do: `just next-task` was an `awk` pass matching `^Status: Ready$`
exactly. Of the 25 tasks here, 22 carried a decorated status — `Status: **Ready.**`,
`Status: Ready — reframed`, `Status: Ready, but low expected yield`, `Status: DONE (2026-07-26,
HTTP). A bank is…` — so the selector saw three tasks, would have gone silent the moment R1-R3
closed, and had no way to tell a finished task from an invisible one.

What replaced it:

- **A machine-readable status line**, specified in Queue Rules above: one state word from the
  closed vocabulary `Ready` / `Blocked` / `Conditional` / `Parking lot` / `Done`, first line
  under the heading, explanation moved to the `Note:` paragraph below it. All 22 decorated
  lines were rewritten this way, each one's prose preserved verbatim in its `Note:`.
- **[tools/todo_queue.py](tools/todo_queue.py)** as the single parser behind `just next-task`,
  `just task-queue`, `just status`, and `just check`. It refuses to select when *anything* in
  the file is malformed, so an unreadable status stops the run instead of removing a task from
  the queue. It rejects a missing status, two status lines in one block, a status buried below
  narrative, a state outside the vocabulary, and a duplicate task identifier.
- **Regression fixtures** in [tests/todo-status/](tests/todo-status/), run by
  `just check`: `legacy-decorated.md` holds the four real decorated forms this file carried
  (all four must now error, none may be skipped), `normalized.md` proves selection skips a
  `Done` entry and returns the first `Ready` one, and `structural.md` covers the four
  structural faults including the duplicate `13`.

States assigned by reading each task's completion narrative rather than its old wording — the
rule is that the state describes the *remaining* work. That reclassified several: task 0 and R4
are `Conditional` (both move only when task 10 names a record the store cannot hold), task 5 is
`Blocked` (needs unrecognized hardware or a virtual MIDI port), and tasks 1, 3, 10a and 10b are
`Ready` on their remainders even though their first pass landed. Identifiers were already
unique after the 13/13b split; `just check` now enforces it.

Not done here: the states are one agent's reading of each narrative, so a task whose remainder
is finer-grained than its heading still needs its own pass. The vocabulary is deliberately
small — add a state only when a task genuinely does not fit one of the five.

### R2. Panel and group parser pilot

Status: Done

Note: 2026-09-05, build 18.0.9598 (arm64) + live deck-skin fixture. The reader inspection,
the candidate diff, and one candidate carried to a confirmed local test. Full evidence:
the tracker's "Skin Reader Vocabulary And The `clickthrough` Attribute" section.

**The inspection.** Three readers located and recorded, each anchored by strings only it
compares, each window the tightest stretch of `__text` holding an xref to every anchor:
`skin_object_base` (`0x10037c54c`-`0x10037cebc`) — the attributes every skin object reads,
`<panel>` and `<group>` included; `element_dispatch` (`0x10037dfd4`-`0x10037ebf8`) — the
element-name switch; `panel_builder` (`0x1007959a4`-`0x100795f40`). Packaged as
[tools/extract_skin_readers.py](tools/extract_skin_readers.py) (`just skin-readers`,
`just skin-reader <name>`, `just skin-candidates`) over
`tests/skin-reader-vocabulary.json`, so the diff is regenerable rather than transcribed.
`--check` is build-anchored: it skips itself on a `CFBundleVersion` change rather than
failing on addresses that were never expected to survive a bump.

**Boundary, stated as R2 asked.** String references only, one call level, no call target
followed, no branch coverage measured, no disassembly of control flow, and no function
names — the build is stripped and none is guessed. A name a reader passes to a helper is
invisible to this method. `<group>` has no builder of its own in this extraction, which
locates the next question rather than proving none exists.

**The wall this pass hit, and it is not a helper-resolution wall.** Attributes shipped skins
use heavily — `sourcecolor` (460 uses), `textaction` (678), `panelname`, `swapdeck`,
`firstvisible`, `textwidth`, `dblaction` — are absent from the binary in any case. They are
not reader vocabulary at all: they are `class=""` template placeholders (the binary carries
`[TEXTACTION]`, `[ACTION1]`, `[bordercolor]` as placeholder tokens), which is why
`lint_skins.py` already skips attribute checks on elements with `class=""`. So absence from
the binary is evidence a name is *not* reader vocabulary, and says nothing about whether a
skin may use it. **No R4 trigger came out of this task** — nothing here was a finding the
current record could not hold, and no extractor failed to resolve a reference it needed.

**The candidate taken live: `clickthrough`.** Read by every skin object, compared against
the single value `pass`, present in no shipped skin and no SDK doc. Five generated deck
skins in [tests/Skins/clickthrough-probe/](tests/Skins/clickthrough-probe/), identical apart
from one attribute on one element: two buttons on the same rectangle, each writing its own
global, so the answer is read over HTTP instead of judged from a screenshot.

| Variant | Attribute on the top button | `$ct_top` | `$ct_bottom` |
| --- | --- | --- | --- |
| `baseline` | *(none)* | 1 | 0 |
| `visible-off` | `visibility="param_equal 'no' 'yes'"` | 0 | 1 |
| **`pass`** | `clickthrough="pass"` | **1** | **1** |
| `value-control` | `clickthrough="qzqzqz"` | 1 | 0 |
| `attr-control` | `zzclickthrough="pass"` | 1 | 0 |

Two independent runs, variant order reversed in the second, identical both times.
`clickthrough="pass"` makes an element fire its own action *and* let the click continue to
what is underneath — additive, not a redirect. Both controls separate, so the attribute name
and the value each carry the behavior. `visible-off` is the calibration with a known working
attribute: it proves in the same fixture that the click was over the bottom button and that
attributes on the top button are honored, so the negatives are about `clickthrough` and not
about aim. Documented in `docs/Skin SDK.md` under "Attributes Every Skin Object Reads".

**Two facts the setup established, both needed by anyone repeating this.** A skin folder with
no image beside the XML is refused — a modal "Impossible to open skin `<name>`" while
`load_skin` still returns `true`, so the channel's own result says nothing. And the skin list
is *not* cached: a folder created while VirtualDJ runs loads immediately, verified by copying
a known-good skin to a new name. `load_skin` also turned out to be its own restore oracle —
in query position it returns the current skin identity — and is recorded on the verb.

**Still open, deliberately.** Only `pass` was tested here, because it is the only value that
window compares. *(2026-09-07: the historical-installer excavation read the boolean parser
the loader falls back to, and the `yes`/`TRUE` fixture variants then confirmed a third state
live — drawn but transparent to clicks, own action not fired. Recorded in Skin SDK.)*
`clickthrough` on a container rather than a button, and whether the
pass-through reaches more than one layer, are untested. `just skin-candidates` still lists
`applyfx`, `setdeck`, `song_pos`, `foldersearch` and the `forceshow` values as untested
leads, and the element switch knows `multibutton`, `resizepanel`, `keyboardmap`, `rack`,
`onexit`, `os` and `darkmode` — existence only. Task 10a's waveform questions are untouched:
this pilot shared no fixture with them and closes none of them.

### R3. Known-position fixture and get_time discrimination

Status: Done

Note: 2026-09-06, HTTP, build 18.0.9598, deck stopped. The fixture exists and proves itself,
and each of the three targets has a reproducible position relationship across both runs.
Full evidence: the tracker's "Known-Position Fixture And `get_time` Discrimination" section
and `tests/get-time-positions.json`.

**The fixture, which was the prerequisite.** `known_positions` in
[tools/fixtures.py](tools/fixtures.py) — deck 1 stopped, cue 1, a loop start and a loop end at
three distinct positions — plus
[tools/probe_known_positions.py](tools/probe_known_positions.py) (`just known-positions`),
which establishes it, proves it, probes it and restores it. Every position is read by an
oracle that is not `get_time`: `cue_pos 1 mseconly`, `get_loop_in_time on`,
`get_loop_out_time on`, and `get_position` × `get_time 'total'` for the playhead. Nothing
assumes the numbers it asked for — quantize moved `set_cue 1 15000ms` to 14496 — so all four
are read back and the run **aborts rather than probe** if any two coincide. Restoration is
verified: cue deleted (`has_cue 1` → `no`), loop exited, deck returned to the contents found
at start, `display_time` never touched.

**The result.** Two runs, the fixture torn down and rebuilt between them with different
numbers and the form order reversed; two phases each; all four phases agreeing.

- `get_time 'cue1'` equals `cue_pos 1 mseconly` exactly, and **tracked the cue when it moved**
  (14496→70496, 24496→60496) while the loop endpoints were held fixed.
- `get_time 'loopout'` equals `get_loop_out_time` exactly, in all four phases.
- `get_time 'loopin'` equals `get_loop_in_time` **only while a loop is active**. With the loop
  exited it returns the loop-*out* value while the oracle still reports the in point.
  Reproduced in both runs, so it is recorded as a conditional rule, not as instability.

**The controls did the work R3 said they would.** An unrecognized tail falls back to
**`elapsed`**, not to the bare form — bare followed the operator's `display_time 'remain'`
throughout — so bare-versus-argument separation was never recognition, and the three targets
are confirmed by matching their *own* oracle and by tracking a moved position. `short` alone
behaves as an unrecognized tail. `absolute` keeps the `display_time` mode, so it is a modifier
rather than a mode. `cue` is not `cue1`: it reads the *active* cue, `0` until one is activated.

**Recorded elsewhere:** `get_time`, `cue_pos`, `get_loop_in_time`, `get_loop_out_time`, `loop`,
`set_cue` and `goto` all now carry local-test evidence in the store, and
`docs/VirtualDJ Reference.md` gained the tested rule with both traps. Two setup facts worth
their own line: `loop N` lays an N-beat loop **ending** at the playhead, and a bare signed
number to `goto` is beats.

**Unresolved, explicitly.** `to_lyrics` returned `0` in every phase — the fixture has no
lyrics, so this says nothing about the tail. Whether `cue2`, `cue3`, … exist as tails was not
probed. `loop_out` after `loop_in` on a stopped deck produced a 4-beat loop unrelated to
either point; `loop N` was used instead and that observation was not chased. Nothing was
tested on a *playing* deck, deliberately, so that no result could be drift. **No R4 trigger:**
the existing capture contract held this fixture without change, and no extractor failed to
resolve anything.

### R4. Only the infrastructure change demonstrated by R2 or R3

Status: Conditional

Note: Start only with a concrete blocker from R2 or R3. **Neither produced one (2026-09-06).** R2's wall was that many shipped skin attributes are `class=""` template placeholders rather than reader vocabulary — a fact about the format, not a reference the extractor failed to resolve. R3's fixture fitted the existing capture contract without change. So this stays Conditional and waits for a later finding the current record genuinely cannot hold; index inversion remains task 11 and is not a prerequisite for anything here.

Owners: task 0/10 for representation, 10/10b for shared runtime helpers. A specific extractor
repair is new work; index inversion remains task 11 and is not a pilot prerequisite.

Name the exact finding the current record cannot hold or the reader/reference the extractor
cannot resolve. Make the smallest data-command or extraction change that represents it or
recovers it, with a focused regression. Follow `CSkinEngine::createAction` or another shared
helper only when the investigation supplies a concrete question. No upfront coverage schema,
general extractor rebuild, or agent-cost bookkeeping is part of this task.

### R5. Repair `next-incomplete-verb`, which fails the way the queue selector did

Status: Done

Note: 2026-09-07. Both pools now report; the selftest fixtures hold the two silent failures.
`just verb-stats` prints `active_incomplete: 2` with `incomplete_pools: {audit: 2,
contract_gap: 224}`, and once the audit pool empties the selector hands back a task-10
worklist item labelled with the pool it came from.

- **Arithmetic by inclusion** (`audit_pool`): a record is active if it is `needs_test`, not
  `blocked`, and not already `Pass`. The old `needs_test - blocked - tested_and_needs`
  subtracted a set that only partly overlaps — records are `blocked` without ever having been
  flagged `needs_test` — so the figure crossed zero into -9.
- **Fall-through** (`contract_gap_pool`, `select_next`): with the audit pool empty, the pick
  comes from records with no row in `tests/verb-return-types.json` and none in
  `tests/verb-arg-forms.json`, resolving aliases to their canonical and skipping
  `HARDWARE_BLOCKED`. Both the picked record's pool and the pool sizes are reported; the split
  is computed at read time and never written into the store, since the artifacts regenerate.
- **Regression fixtures** in [tests/verbdb-selection/](tests/verbdb-selection/), run by
  `verbdb.py check`: `blocked-not-needs-test.json` is the store shape that went negative,
  `audit-pool-exhausted.json` must yield a contract-gap pick rather than silence, and
  `both-pools-empty.json` keeps real completion distinguishable from a stalled selector.

The diagnosis this task was written from, kept as the record of the defect:

Added 2026-09-07 from the review's metric finding ("the store's incomplete selector
follows an assigned `needs_test` flag, not every missing contract"). The finding has since
turned from a limitation into a defect: `just verb-stats` reports `active_incomplete` as a
**negative** number, and `just next-incomplete-verb` reports one active item while task 10
has open contracts on most of the store. Same failure shape R1 repaired for the task queue:
a selector that goes quiet is read as completion.

Cause, measured on the store as of 2026-09-07: `active_incomplete` is
`needs_test - blocked - tested_and_needs`, but eleven records are `blocked` without being
`needs_test` (the Rane, NS7 and motorwheel names), so the subtraction crosses zero. The
selector then draws only from the audit's `needs_test` set, which is nearly exhausted, and
never from records with no return-type or argument-form evidence — the very records task 10
exists to close.

Do, in [tools/verbdb.py](tools/verbdb.py) and nothing else:

1. Fix the arithmetic: count a record active only if it is `needs_test` and not `blocked`
   and not already `Pass`. The figure can never be negative.
2. Let the selector fall through: once the `needs_test` set is empty, select the next record
   with no Tier-1 contract evidence (no return-type row in `tests/verb-return-types.json`, no
   argument-form row in `tests/verb-arg-forms.json`), skipping `HARDWARE_BLOCKED`. Report which
   pool the pick came from so a reader can tell "audit gap" from "contract gap".
3. A selftest fixture in the style of [tests/todo-status/](tests/todo-status/), run by
   `verbdb.py check`: a store with a blocked-not-needs-test record must not go negative, and
   an exhausted `needs_test` pool must yield a contract-gap pick rather than nothing.

Acceptance: `just verb-stats` prints a non-negative `active_incomplete` with the pool split
shown, and `just next-incomplete-verb` returns a task-10 worklist item after the audit pool
is exhausted. No prose, no schema change; this is the worklist source for 10/10b and belongs
before the next 10b sweep.

### R6. Make `just xml-stats` name its own blind spot

Status: Done

Note: 2026-09-07. `just xml-stats` now prints `reader_vocabulary_unused` beside `undocumented`
in `totals`: the reader-vocabulary names no shipped file writes, joined from
`tests/skin-reader-vocabulary.json` at generation time.

- Build-anchored the way `extract_skin_readers.py --check` is. The join carries a `status`:
  `current` lists the names with the build they were read off; a `CFBundleVersion` mismatch
  between that artifact and the installed app reports `stale` and lists nothing, since a
  reader vocabulary read off one build says nothing about another; `unverified` (no app
  installed) and `unavailable` (vocabulary not extracted) are distinguished. `--check` prints
  a non-fatal notice when the committed join no longer matches a re-join — a build bump is
  not a broken inventory, but the blind spot must not read as current when it is not.
- The extractor docstring and the `docs/README.md` inventory entry now say what the count
  measures: mentions of the elements shipped files happen to use, with attributes and
  behavior contracts out of scope. Neither carries a number.
- Regenerating the inventory also picked up R2's `tests/Skins/clickthrough-probe/` fixtures
  (21 → 27 skin files scanned); element sets are unchanged, only use counts moved.

The task as written:

Added 2026-09-07. The review named the limitation ("XML inventory documented means an
element mention, not a full attribute/behavior contract"); R2 then proved it — `clickthrough`
is read by every skin object, was in no shipped skin and no doc, and `undocumented: 0` never
moved. It still reads `undocumented: 0` across all elements, and the next agent will read
that as completeness. The fix is a data-command change, not a warning paragraph.

Do:

1. In [tools/extract_xml_inventory.py](tools/extract_xml_inventory.py), have the stats output
   carry a second field alongside `undocumented`: the reader-vocabulary names no shipped file
   writes, joined from `tests/skin-reader-vocabulary.json` (the same list
   `just skin-candidates` prints). Build-anchored like that artifact's own `--check`: on a
   `CFBundleVersion` change the field says the vocabulary is stale rather than listing it.
2. One sentence in the extractor docstring and in the inventory entry of
   [docs/README.md](docs/README.md): the count measures mentions of elements shipped files
   happen to use; attributes and unused features are out of scope, see `extract_skin_readers.py`.

Acceptance: `just xml-stats` shows the candidates beside `undocumented`, and neither doc line
carries a number. Cheap-model delegable; can ride with R5.

### R7. Carry the skin-reader candidates R2 left untested to live tests

Status: Done

Note: 2026-09-07. Ran on build 18.0.9598 against a live VirtualDJ, deck-skin surface.
Fixture: [tests/Skins/reader-candidates-probe/](tests/Skins/reader-candidates-probe/) —
`generate.py` renders every variant from one template, `run.py` loads each one, resets the
globals, clicks a named point with a CGEvent helper it compiles itself, and reads the globals
back. Six series, each run forward and reversed with identical rows both times. Full tables in
the fixture README; the run narrative and its method notes are in the tracker's
"Skin Reader Candidates Taken Live 2026-09-07" section; the confirmed behavior is in
[docs/Skin SDK.md](docs/Skin%20SDK.md).

Per candidate, as the task asked:

| Candidate | Outcome |
| --- | --- |
| `r` | **Confirmed**: the `<mousecircle>` radius in skin units, with a nonsense-attribute control separating it; the default without it is the element's half-height, and `x`/`y` turned out to be absolute skin coordinates, not element-local |
| `onexit` | **Confirmed**: `<onexit action="…">` runs when the skin is *replaced*; nonsense-tag control never fired |
| `multibutton` | **Existence + behavior**: builds an object that absorbs a click while drawing nothing, and does not build child elements |
| `pannel` | **Confirmed as a container**: a button inside one is built and clickable, as inside `<group>` |
| `song_pos` | **Negative**: behaves like the nonsense control where `<songpos>` takes the click — very likely the verb name referenced as that element's default action, not an element spelling |
| `foldersearch` | **Negative**, calibrated against `<folderlist>` in the same placement, which does take the click |
| `resizepanel`, `rack`, `keyboardmap`, `os`, `darkmode` | **Negative** in a deck-skin panel and at the skin root: no hit area, no children built |
| `8pads` (and the whole `forceshow` vocabulary) | **Not reached**: a lone panel shows whatever it forces, and a two-panel `group=` kept showing the same member under both `skin3FxLayout`/`skin6FxLayout` states and through `effect_3slots_layout`. Boundary in the tracker |
| `applyfx`, `setdeck` | **Not reached**: no attribute or element to attach them to, and click routing cannot discriminate them. Needs the H4-style read of the panel builder |

Knock-on changes the run forced, all small: probe fixtures are excluded from the XML
inventory (they carry nonsense tags by design); `extract_skin_readers.py` now also counts a
backtick-quoted token as documented, since its `{2,}` pattern could never see a one-letter
name like `r`, which would have stayed a "candidate" forever after being confirmed. Writing
`r`, `song_pos` and `foldersearch` into the SDK doc shrank `summary.candidates` to the
`forceshow` values plus `applyfx`/`setdeck` — the intended reading of that field. `setting`
and `effect_3slots_layout` picked up local-test records along the way.

The task as written:

Added 2026-09-07. This is the review's "systematic Skin SDK discovery" gap, sized to what
R2 already extracted rather than to a new sweep. `just skin-candidates` lists the reader
vocabulary that no shipped skin and no doc names — `applyfx`, `setdeck`, `song_pos`,
`foldersearch`, `r`, and the `forceshow` value `8pads` on build 18.0.9598 — and R2's note adds
seven element names the dispatch switch knows only by existence (`multibutton`,
`resizepanel`, `keyboardmap`, `rack`, `onexit`, `os`, `darkmode`). Needs `just vdj-up`.

Method is the `clickthrough` series in [tests/Skins/clickthrough-probe/](tests/Skins/clickthrough-probe/)
and H1: one generated deck skin per candidate, identical apart from the attribute or element
under test, each variant writing its own global so the answer is read over HTTP rather than
judged from a screenshot; a nonsense-attribute and nonsense-value control per candidate; the
reader window (`just skin-reader <name>`) read first to size the value set, as H1 did with
`getBoolParam`. A candidate the window compares against a fixed set gets that set; one that
takes free text gets the argument shapes attested tails show for the nearest verb.

Deliver per candidate one of: confirmed behavior recorded in
[docs/Skin SDK.md](docs/Skin%20SDK.md) with the fixture path; existence-only (parsed, no
observable effect in the fixture) recorded as such; or not reached, with the reason. A
negative needs the R2 boundary — which reader, which values tried, which branch was not
exercised. Do not extend to the waveform questions in 10a; they share no fixture with this.

## Historical-installer follow-ups (2026-09-07 review)

Translated from the assessment in
[docs/Historical Installer Excavation.md](docs/Historical%20Installer%20Excavation.md). Same
rule as the R sequence: existing task numbers own their broader work, and these entries name
only the bounded piece the excavation made startable. The two live pieces ran the same day.

### H1. Clickthrough value matrix

Status: Done

Note: 2026-09-07, build 18.0.9598, deck-skin surface. The named `CXMLNode::getBoolParam`
disassembly (captured for 9.0.5308, 9.0.7607 and 18.0.9246 as `bool-param` in
`tests/build-history-2026-09-06/`) accepts only `yes`/`true`/`no`/`false`, case-insensitively,
and returns the caller's false default otherwise — so the proposed six-value test collapsed to
one unobserved state. `yes` and `TRUE` variants on the overlapping-button fixture, two
reversed-order runs: **boolean true is a third state** — the element stays drawn, its own action
does not fire, the click reaches the element underneath — beside additive `pass` and the
swallowing default. Recorded in Skin SDK `clickthrough`, the tracker's second-pass table, and
the fixture README.

### H2. Wrapper construction paths

Status: Done

Note: 2026-09-07, same build. Twelve more generated skins: the top button wrapped in a `<panel>`,
a plain `<group>`, and a `<group visibility="…true">`, each with no attribute, `pass`, and
`yes`; plus three-layer stacks. Panels and visibility-bearing groups honor `clickthrough`
exactly as a button does; **a plain group ignores it in both values**, the live counterpart of
the historical `CSkinPanel::loadChildren` split that tests the *presence* of
`visibility`/`novisibility`. `pass` carries a click exactly one layer down. Recorded in Skin SDK
`<group>` (two construction paths, constant-true `visibility` as the workaround) and
`clickthrough`. Not run: a constant-false `novisibility` wrapper. Not probed, deliberately: whether
the recorded `<group class="…">` crash is a plain-group artefact — a hypothesis only, and a crash
on a live instance is not a fixture.

### H3. Historical vendor corpus diff and store-visible compatibility history

Status: Done

Note: 2026-09-07. Both deliverables landed as artifacts and joins, not prose:
[tools/diff_vendor_history.py](tools/diff_vendor_history.py) (`just vendor-history-diff`) writes
`tests/build-history-2026-09-06/vendor-text-diff.json`; `summary.json` gained `verb_history`;
`joined_view` and `just verb` show both per verb. Three unofficial verbs (`setting_if_unchanged`,
`get_pad_page_name`, `pad_page_favorite`) received their 9.0.5308 appendix descriptions via
`put-verb`. Findings and the probe worklist they open (old parameter spellings such as
`get_saved_loop 'len'`, `video_source 'shader'`) are in the excavation doc's "What the older
vendor text and skins still say". The historical skin archives were not copied into
`examples/`. Original brief follows.

Offline, delegable to a cheap model, no runtime claims. Two deliverables from the three
older payloads (`~/Downloads/install_virtualdj_2020_b5308_mac.pkg`,
`~/Downloads/VirtualDJ_2023_b7607_mac.pkg`, `~/Downloads/install_virtualdj_2026_b9246_mac.pkg`,
expanded with `pkgutil --expand-full`; the memory notes hold the same paths):

- **Description and example diff.** Compare each historical `languages.zip` → `English.xml` →
  `<Actions>` and each shipped skin/pad archive against the current vendor corpus. Every verb
  *name* in the old appendices is already in the store (checked 2026-09-06), so the target is
  *text*: descriptions or parameter explanations that were shortened or dropped, and
  script-bearing XML that no longer ships. Output is a provenance-stamped list (archive path,
  member, build, exact source text), deduplicated against unchanged material. Historical vendor
  usage is a lead about current behavior, never a supported-form promotion.
- **`first_seen_build` and alias transitions in the store.** `summary.json` → `transitions`
  already holds the sampled name additions and primary-to-alias flag changes (`goto_bar` →
  `goto_beat_in_bar` between 18.0.9246 and 18.0.9583). Carry them into the verb store through
  the extractor/bootstrap path so `just verb <name>` prints them — never by hand, and never as a
  release date: the samples bracket table appearance, nothing finer.

### H4. Runtime argument parsing from the named `IAction::create`

Status: Conditional

Note: Trigger: task 10b's harness has landed, because every rule this walk recovers is a
10b test and nothing else. Folded into task 10 as its first sub-step; listed here so the
lead is not lost.
`IAction::create(char const*, char const**, int)` is named on 18.0.9246 (x86_64 entry
`0x100596f1c`; resolve it again with `nm` before use). Follow argument consumption, delimiter
handling and fallback branches, and contrast with the separately documented editor parser.
Every recovered rule becomes a discriminating test for the 10b harness, not a documented rule
on its own — editor acceptance and parser tolerance cannot substitute for an observed result.
This has the highest ceiling of the excavation's leads because VDJScript grammar is the
repo's stated cliff and the parser reports no errors.

## Ready Tasks

### 0. Build The Verb Record Store And `just` Data API

Status: Conditional

Note: Foundation landed (2026-07-22) — generation + migration remain

The store and its query/edit API exist and are wired into `just check`. This is the compounding-cost reducer: it replaces the record-in-tracker-then-promote-to-three-docs cycle with one `just put-verb`, and lets agents query verb state without loading the 6,300-line monolith.

Done in this pass:

- [tools/verbdb.py](tools/verbdb.py) over the authoritative store [docs/vdjscript-verbs.json](docs/vdjscript-verbs.json), fronted by `just get-verb / put-verb / find-verbs / next-incomplete-verb / verb-stats`. Storage is private behind the API so it can later become one-file-per-verb without retraining agents.
- Merge-safe `bootstrap` seeded all 991 records from the index + coverage audit (official names + Needs-Local-Test gap) + tracker status tables. It correctly finds the 19-name gap (17 hardware-blocked → skipped by `next-incomplete`), leaving `dualdeckmode_decks` and `system` as the 2 active items, and auto-detected 7 tracker `Pass` rows.
- `verbdb.py check` (schema, alias resolution, index coverage, count freshness) is in `just check`. Entrypoints (`AGENTS.md`, `INDEX.yml`, `docs/README.md`, `tools/README.md`) route verb lookups and result-recording to the flat `just get-verb` / `find-verbs` / `put-verb` commands.

Reports are queries, not files (2026-07-22):

- `just find-verbs` filters on `--surface`, `--section`, `--tier`, `--status`, `--kind`, `--needs-test`, with `--format=json` for structured output and `--limit`. A category listing is just an unfiltered query, so **no derived Markdown is written to disk** — nothing can drift, and there is no staleness gate to maintain. An earlier pass generated `docs/VDJScript/generated/*.md` and was reverted for exactly this reason.
- Rule for future work: do not add a generator that writes a Markdown copy of store data. If a view is wanted, add a query or a flag. Building reader-facing documentation is a later phase, driven by findings — not something to design for now.

Remaining:

- Add richer record fields as needed by contracts (`forms`, `platforms`, `deck_scope`); `put` currently covers the scalar/list fields, nested contract detail is hand-edited in the JSON.
- Grow the query layer where a real question is awkward to ask (e.g. verbs by evidence source, or by presence of a local-test note).
- The monolith still holds the authored prose. Retiring it follows the frozen plan's phased, one-family-at-a-time migration; do not delete hand-authored docs ahead of that.

Effect catalog is queryable (2026-07-22): [tools/fxdb.py](tools/fxdb.py) / `just get-fx / find-fx / fx-stats` answers slider/button questions straight from the sweep artifact, gated by `fxdb.py check` in `just check`. No Markdown copy — same rule as the verb store.

Tasks 1-4 are one FX cluster: they share the same VirtualDJ session and the same deck-FX context. Batch them into one local-test session where possible. Preferred readback channel: the [HTTP control interface](docs/HTTP%20Control%20Interface.md) (`just vdj-query`), which returns exact strings and makes the sweeps scriptable — the older `name=`-interpolation pad technique (proven on v2026-m b9482) is now needed only for pad/skin-surface-specific checks.

### 0b. Topic Search Across Every Corpus

Status: Done

Note: 2026-09-06. The metadata layer landed, and with it the two problems it was meant to fix
plus one it exposed.

**The gap was worse than described.** `just topic waveform` returned four *hardware* helpers
(`get_numark_waveform`, `gemini_waveform_zoomlevel`, …) and not one skin element — the entire
waveform surface (`wave`, `scratchwave`, `rhythm`, `rhythmzone`, `zoomed`, `songpos`, `grid`,
`gridlines`, `beattunnel`, `blockwave`) was unreachable, and only the doc pointer saved it.

**[docs/topic-tags.json](docs/topic-tags.json)** is the fix: 15 topics and 23 aliases, the only
hand-maintained input to `just topic`. Tagged hits are marked `+` in the report and the topic
prints *why* it needed a tag. `just topic "color fx"` now redirects to `colorfx`, `"beat grid"`
to `waveform`, and `waveform` returns the eleven elements plus the built-in skins that use them.

**Not a `topics: []` field on each verb record, deliberately.** Topics are cross-cutting, so a
per-record field scatters one topic's membership across a thousand records and makes it
unreviewable; it would also put a navigation aid inside the store that is authoritative for
per-verb *evidence*. One map, reviewed whole, is the maintainable shape. The reason is recorded
in the file's own `_meta` so the next agent does not re-litigate it.

**Tags cannot rot.** `just check` fails on a tag naming a verb, element or doc that does not
exist, on an alias pointing at an undefined topic, and on a topic with no stated reason. A tag
that names nothing is worse than no tag: it silently promises reach it does not have.

**The bug the work exposed.** "EXAMPLE FILES — real usage, grep-verified" was dominated by
`tests/*.json` — the verb table, the sweeps, the corpus. A verb name appears in those because
it *exists*, not because anything uses it, and they were crowding out the working examples the
section exists for. The evidence artifacts are now excluded from that grep, so `just topic
sampler` leads with real pad XML instead of `tests/verb-table.json`.

**Left open.** Tag coverage is the 15 topics where the gap was demonstrable, not a taxonomy —
add a topic when a search visibly misses something, and state why in the entry. Effects are
still matched by a whole-record substring search, which is generous and occasionally noisy.

### 1. Complete The Per-Effect FX Introspection Sweep

Status: Conditional

Note: Structural sweep complete 2026-07-22; the rendering half closed 2026-09-06. One settings-UI question is left, named at the end.

[tools/sweep_fx_introspection.py](tools/sweep_fx_introspection.py) captured counts, short+full labels, normalized **defaults**, live value text, and length/beats flags for all **119** installed effects into [tests/fx-introspection-dump.json](tests/fx-introspection-dump.json), plus the enabled cycle for all three targets. Query it with `just get-fx <effect>` / `just find-fx [--category=deck_fx|video_fx|transition] [--has-length]` / `just fx-stats` — do not read the dump and do not hand-transcribe it.

What the sweep settled:

- **Introspection is read-only.** Every `get_effect_*` helper accepts an effect *name* where the docs show a slot number (`get_effect_slider_count 'Echo'`, `get_effect_slider_default 'Echo' 3`), returning the same values as the slot form for all 119 title-resolvable effects with no `effect_select` and no state change. This is the cheap way to ask about an effect that is not loaded.
- **`get_effect_title '<name>'`** returns `'<Canonical> - Deck N'` or `''`, so it resolves a name to its canonical spelling and probes existence. Case-insensitive, *not* space-insensitive. Blind spot: `''` for `Stems` and `Vocals`, which select and introspect fine through a slot — so a title miss must be confirmed by selecting before the name is called unknown.
- **Audio-vs-video: cycle membership, not loadability.** All three selectors accept any installed effect name (`video_fx_select 'Echo'` really does set the video slot to Echo), so what a target accepts discriminates nothing. The three `+1` cycles *are* disjoint and are the app's own category assignment: 63 deck FX, 17 video FX, 35 transitions. Each is the enabled/favorites subset, so an installed effect in no cycle (`Lottery`, `Sweep`, `Title`, `Vocals`) is category-*unknown*, not uncategorised.
- **`Brake` and `Shader` resolved.** `Brake` is not a selector name on this build at all — a docs-catalog error; the real ones are `BrakeStart`, `VinylBrake`, `Beat Brake`. `Shader` is an alias for `Visuals`, which loads into a deck slot perfectly well; the original sweep only ever asked for it by the wrong name. `BeatGrid` is likewise a spacing error for `Beat Grid`. Nothing here was ever "video-only".
- **`*_skip_length` re-indexes, it does not blank.** Index *i* is the *i*-th slider with the length slider removed, so the last index is always empty. Verified on all 47 length-bearing effects; the length slider is not always index 2 and not always labelled `LEN`.

Narrowed 2026-09-06 (HTTP, build 18.0.9598). Three of the four remaining questions turned out
not to need rendering at all, and answering them found a broken verb. See the tracker's "Video
FX Over HTTP" section; state was recorded and restored.

- **`deck master` scoping: answered.** The video FX chain hangs off the master output, and an
  unscoped video verb addresses it — `video_fx_select` bare and `deck master video_fx_select`
  both read `0.18` while `deck 1 video_fx_select` reads `0`.
- **`video_fx_slider`: answered.** It indexes correctly in both positions; execute moves the
  named slider and nothing else. Recorded `Pass`.
- **`get_video_fx_slider_label`: answered, and it is broken.** The index argument is never
  read: with Colorize selected (labels COL/STR/SAT/SPD/BRI) every index 0–99 returned `COL`.
  Recorded `Fail`; use `get_effect_slider_label '<effect>' <n>`, which indexes correctly and
  needs no selection.
- **The 4 category-unknown effects: half answered.** Walking `video_fx_select +1` traversed
  exactly 17 effects and wrapped cleanly, matching the catalog's `video_fx` category and
  containing none of `Lottery`, `Sweep`, `Title`, `Vocals`. Whether *enabling* one in the FX
  list editor puts it in a cycle is still a GUI question.

Rendering half closed 2026-09-06 — **the gate was the video window, not video output.**
`video_fx` could not be activated with no track, with an audio track, or even with a real video
loaded; what was missing was the window itself. `video` ("Open/close video window") opens it, a
paused deck is enough to render a frame, and the identical `video_fx on` call then works. Four
rendering passes recorded, each watched on screen, all state restored (tracker: "Video FX
Rendering: The Gate Was The Video Window"):

| Verb | Watched | Result |
| --- | --- | --- |
| `video_fx` | `Negative` on a colour-bar pattern | every colour inverted |
| `video_fx_slider` | `Colorize` hue `0.1` → `0.7` | tint went amber → magenta |
| `video_fx_clear` | `Colorize` actively tinting | render returned to the source |
| `video_transition_slider` | `Blinds` NB `0.15` → `0.95` at crossfader `0.5` | ~5 thick blinds → ~15 thin |

`video_fx_clear` **deactivates only** — selection and slider values survive it, which the earlier
pass could not tell because it had only ever run with nothing active. Fixtures were generated
with ffmpeg (a `testsrc2` pattern and a white clip), never the user's library; the transition
needed two *different* videos or the crossfade would have been invisible.

**Conditional on one settings-UI action:** enable one of the four category-unknown effects
(`Lottery`, `Sweep`, `Title`, `Vocals`) in the FX list editor and re-walk the `+1` cycles to see
whether it joins one. There is no verb for that step. Everything else in this task is done.

Start here:

- Re-run after a VirtualDJ update: `python3 tools/sweep_fx_introspection.py > tests/fx-introspection-dump.json` (needs `just vdj-up` green)
- [tests/Pads/Reference - FX Introspection Test.xml](tests/Pads/Reference%20-%20FX%20Introspection%20Test.xml) (pad-surface checks only)

Read first:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md) (FX Helpers rows only, for the established method)
- `just get-fx <effect>` instead of [docs/Effects Engines.md](docs/Effects%20Engines.md) for control maps

Record results in:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md), and `just put-verb <name> test_status=… evidence="…"`

Done when:

- The remaining video-rendering verbs get at least one recorded pass each.
- Generic FX control guidance distinguishes observed behavior from inference.

### 2. Characterize FX Bank Save And Load

Status: Done

Note: 2026-07-26, HTTP. A bank is a rack of effect SELECTIONS for slots 1-6 — not active
state, not slider values, and global across decks. `effect_bank_load` returns true/false as
a bank-populated probe. Recorded in the tracker and on `effect_bank_save`/`effect_bank_load`
(`just get-verb effect_bank_save`).

Start here:

- [tests/Pads/Reference - FX Bank Test.xml](tests/Pads/Reference%20-%20FX%20Bank%20Test.xml)

Read first:

- [docs/Effects Engines.md](docs/Effects%20Engines.md) (bank save/load rows only — `rg -n effect_bank`)
- `just grep-verb-docs effect_bank_save`

Record results in:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md)

Promote to:

- [docs/Effects Engines.md](docs/Effects%20Engines.md)
- [docs/Effects Usage.md](docs/Effects%20Usage.md)

Done when:

- Restored effect names, active states, slider values, and deck scope are recorded.

### 3. Separate Release FX From Normal Slot FX

Status: Conditional

Note: 2026-09-06. The done-when is met — the release path is now described separately from
ordinary deck FX, in `docs/Effects Engines.md` §Release FX and `docs/Effects Usage.md`, with
local-test evidence on all three verbs. What is left waits on one operator action, named at the
bottom. Full narrative: the tracker's "Release FX: The Arming Path Does Not Exist In Script".

**This pass overturned the task's own diagnosis.** The 2026-07-26 note said the sliders were
inert because arming "needs a momentary control HTTP can't drive". That is not the obstacle.
`effect_releaseslider_active` is documented to activate *without* one — "and auto activate the
effect" — and it does nothing: `true` returned, `is_releasefx` still `no`, its own query still
`0`, every numbered slot inactive, with deck 1 empty, loaded and playing, scoped and unscoped.
And a pad would run the same script — `tests/Pads/Reference - Release FX Test.xml` fires plain
`effect_releaseslider 25%`, no `down`/`up` wrapper — so that surface adds nothing.

**What is actually missing has no verb.** The verb table, where absence disproves a name, holds
exactly three release names: `effect_releaseslider`, `effect_releaseslider_active`,
`is_releasefx`. There is **no selector**. `effect_select 'releasefx' 'Echo Out'` returns `false`
and changes nothing, scoped or unscoped, leaving the numbered slots untouched. The slot is armed
in the app's own FX lists — the binary carries `Deck %i release effects` and `Master release
effects` beside the other FX-list-editor categories, and `settings.xml` stores eight entries per
deck where script reaches only six. So VDJScript can *drive* the release slot and can never
*create* it.

`is_releasefx` was tried bare, deck-scoped, with slot arguments 0-10, and with the names of
effects this instance really has configured (`Echo Out`, `Phaser`, `Delay`, `Reverb`, `Cut`,
`Backspin`) — `no` throughout, so the earlier negative was never about naming the wrong effect.

**Conditional on one operator action:** assign a release effect in VirtualDJ's own FX lists, then
re-run against `tests/Pads/Reference - Release FX Test.xml` (or over HTTP — the surface does not
matter, as established above) to watch an armed slot for the first time. Until then no release-FX
*behavior* has been observed, and `is_releasefx` has never been seen returning `yes` on any
surface, so its catalog wording "query if **this effect** is in the release effect slot" — which
reads as effect-scoped, the question a plugin GUI asks about itself — stays plausible but
unestablished.

### 4. Keep BeatGrid `effect_command` Plugin-Specific

Status: Done

Note: 2026-07-26, HTTP. Confirmed plugin-instance-scoped (targets the BeatGrid slot), with a
bare form and an unquoted-slot-number form; get/set/cur are BeatGrid's own vocabulary.
Recorded as BeatGrid-specific, not generic. See `just get-verb effect_command`.

Start here:

- [tests/Pads/Reference - BeatGrid Command Test.xml](tests/Pads/Reference%20-%20BeatGrid%20Command%20Test.xml)

Read first:

- [docs/Effects Engines.md](docs/Effects%20Engines.md) (BeatGrid and `effect_command` rows only — `rg -n effect_command`)
- [docs/Native Effects.md](docs/Native%20Effects.md)

Record results in:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md)

Promote to:

- [docs/Effects Engines.md](docs/Effects%20Engines.md)
- [docs/VDJScript Verbs.md](docs/VDJScript%20Verbs.md)

Done when:

- Confirmed `effect_command` examples are documented as BeatGrid-specific rather than generic plugin control advice.

### 5. Author And Load-Test A Minimal Custom Device Definition

Status: Blocked

Note: MAPPER FIRING DONE (2026-07-27, DDJ-GRV6 hardware) — device-definition schema still
open. HTTP-verified on real hardware that the mapper `<map value action>` schema binds and
fires (ONINIT on load, PLAY_PAUSE on press), plus three gotchas: control names must match
the device definition exactly (wrong name fails silently), loading a mapping resets `$`
globals, and editing an active mapper file needs a full restart (re-select does not reload).
See the tracker's "Mapper Firing" section and `docs/Mapper XML.md`. Factory-mapping export
(Factory default -> Save) was tried as a shortcut to the device definition: it yields the
factory `<mapper>` (control names + canonical actions, 293 bindings, lints clean) but NOT
the `<device>` definition, so it does not unblock this. STILL OPEN: the custom `<device>`
definition schema is untested because the DDJ-GRV6 is factory-recognized — needs
unrecognized hardware or a virtual MIDI port + injection to exercise a custom device
definition.

The mapper reference's device-definition schema is official-doc-derived but never load-tested locally. A `SIMPLE_MIDI` device context already exists in the local install's Mappers folder. Mappers are one of the repo's named coverage cliffs, so this is the highest-value task outside the FX cluster.

Start here:

- [docs/Mapper XML.md](docs/Mapper%20XML.md)
- [examples/Mappers/README.md](examples/Mappers/README.md)

Done when:

- A minimal `<device type="MIDI">` XML placed in the VirtualDJ `Devices/` folder is detected by the app, and a paired mapper's `<map>` bindings fire.
- Results (including failures) are recorded in [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md) and promoted into `Mapper XML.md` source labels (`Local test`).
- RESOLVED 2026-07-27 for two of the three mapper-lint warnings (and note these were never factory-sourced: all three came from *personal* local mappings, mis-graded as factory by the now-corrected `author`-attribute rule (the tag does not track authorship) in [examples/Mappers/README.md](examples/Mappers/README.md)): `browser_filter` and `browser_search` are **not verbs on this build** — no `ACTION_` symbol and no bare string anywhere in the executable, no Button Editor autocomplete, `E_FAIL` over HTTP. The lint warnings are correct and the mapper lines using them do nothing; `clear_search` is the real verb. `none` remains unresolved (no `ACTION_` symbol and no autocomplete, but "none" is an English word so its presence in the string table proves nothing); its only observed use is as a do-nothing LED placeholder. See the disproof method in [docs/Undocumented VDJScript Candidates.md](docs/Undocumented%20VDJScript%20Candidates.md).

### 6. Continue Hidden Button Editor Candidate Probes

Status: Done

Note: 2026-09-06, HTTP, build 18.0.9598. Both done-when clauses are met: every one of the 38
`flags == 256` names is now recorded Pass, Partial or Fail, or explicitly blocked, and none is
left as active untested work. Full narrative: the tracker's "Editor-Hidden Verbs: Behavior, Not
Existence". State restored — pad page back to `1 CUE`, deck volume back to `1`, decks empty.

**The Flip family closed entirely, and it needed no gate.** The candidates doc had deferred all
six pending "Flip availability and how recording is gated"; a loaded track was enough. Driven end
to end on a disposable generated fixture with the deck volume at zero: `flip_record` is a toggle
whose first press reads `Rec Standby` and whose **recording begins on the first cue press**, the
status counts up, a second press stops it, and `flip_load` flips `no` → `yes` because a flip now
exists; `flip_play` jumps to the flip start and plays it; `flip_loop` and `flip_arm` toggle
cleanly. The reusable find is that **`flip_get_status` is a text query absent from the catalog** —
`''` / `Rec Standby` / `Rec MM:SS` / `Play MM:SS`, the display string a Flip control wants.

**`effect_beats_sliderindex` verified against an independent oracle.** It takes an effect *name*
and returns the 1-based index of that effect's beats/length slider: `BrakeStart` → 1,
`Backspin`/`Echo`/`VinylBrake` → 2, `Beat Brake`/`Reverb` → 0, matching the FX catalog (built by a
separate sweep) on three distinct answers. A nonsense name also returns 0, so 0 conflates "no
beats slider" with "unknown effect" and cannot probe existence.

**A trap in the pad-page trio.** `get_pad_page_name <n>` is index-only and follows
`padsPagesOrder`; `pad_page_favorite <n>` answers only for 1-4, so it addresses a four-slot
favourites bank rather than a per-page flag; and `pad_page_insplit '<name>'` takes a *name*, not
an index — but **it tracks the current page**. Switching to `2 SYNC` moved the `yes` with it.
With no split layout configured, "part of a split" and "is the current page" cannot be separated,
so its catalog meaning stays unconfirmed and no split indicator should be built on it yet.

**`all_decks` and `combine_query` are not query-position verbs** — `error:-2147467259` bare and
deck-scoped, while every other hidden verb in the sweep answered. Consistent with script-structural
prefixes that only parse in execute position, which was not tested.

**Two names deliberately not executed:** `crash`, now marked blocked — verb-table membership
already proves the name and that is all this repo wants from it — and `browser_colorfilter_edit`,
which opens a modal dialog (query position gives `error:-2147467263`, a different code from the
two above, matching its action-only kind).

**Ten hardware-gated names marked blocked**, under *two different gates* — the first labelling
flattened them and was corrected the same day. `controllerscreen_action` (needs a controller with a
screen) and `assign_related_controller` need only *an attached controller*, which the operator has,
so they become testable whenever one is plugged in; `get_controller_name` returned `''` during this
pass and is the presence oracle to check first. The five `rane_*` names, `ns7_get_drift` and
`motorwheel2`/`3` need specific vendor hardware that is not here and cannot be substituted.

Fifteen more are recorded Partial as return shapes only — `is_colorfx`, `masterbpm`,
`pad_pressure_switch`, `sampler_inputgain`, `send_nothing`, `shoutout`, `stem_volume`,
`timecode_no_jump`, `load_security_shown` and the two that require arguments — each with the state
that would move it named in its evidence, rather than dressed up as a behavior claim. `stem_volume`
in particular still wants a stem-analysed track, which is the candidates doc's own first-probe row.

### 7. Repeat `dualdeckmode_decks` In A Better Context

Status: Parking lot

Note: Low expected yield until a concrete context is identified. Deprioritised by the operator
2026-09-06 in favour of tasks 10b/11/12/13; move it back to Ready when a concrete context turns
up, not on a schedule.

The first pad-context run (v2026-m b9336) recorded `dualdeckmode` toggling on while current and deck-scoped `dualdeckmode_decks` readbacks stayed false on both decks. The promotion condition is a visible dual-deck pair or controller context (deck pairs 1/3 or 2/4), which realistically means a 4-deck skin setup or a controller. Do not repeat the same pad-context probe; identify the better context first, or treat this as semi-blocked.

Start here:

- [tests/Pads/Reference - Dual Deck Mode Test.xml](tests/Pads/Reference%20-%20Dual%20Deck%20Mode%20Test.xml)
- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md)

Read first:

- [docs/Official VDJScript Coverage Audit.md](docs/Official%20VDJScript%20Coverage%20Audit.md) (the `dualdeckmode` rows only)

Record results in:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md)

Promote to:

- [docs/VDJScript Verbs.md](docs/VDJScript%20Verbs.md)

Done when:

- A build, deck/controller context, observed result, and follow-up decision are recorded.
- The official local-test status is updated only if the repeat confirms behavior well enough for promotion.

### 8. Characterize The VirtualDJ Remote App Wire Protocol

Status: Done

Note: 2026-07-27 — transport, wire format, subscriptions, and actions are all verified in
both directions; only minor open questions remain (see end of this task)

Settled with a live session (socket watcher + `dns-sd` + per-connection `nettop` deltas;
recorded in the tracker, [docs/HTTP Control Interface.md](docs/HTTP%20Control%20Interface.md),
and [docs/Application Internals.md](docs/Application%20Internals.md) Remote Skins):

- Remote does **not** use the Network Control HTTP channel; port 80 saw no Remote traffic.
- Discovery is inverted from the obvious guess: the **phone advertises** Bonjour type
  `_vdjremote8._tcp` (SRV → phone, port 4243 observed) and listens; **VirtualDJ connects
  out** to the phone as the TCP client, one persistent connection.
- Semantics are **event-driven push**: idle seconds carry 0 bytes on that connection; a
  deck load pushed ~249 KiB desktop→phone in one second with no inbound request; unload
  ~1.4 KiB; otherwise only sub-KB keepalives.

**Wire format also DONE (2026-07-27)** — see [docs/Remote Protocol.md](docs/Remote%20Protocol.md).
Framing is `8JDV` + `u32` total length + `u16` type; the device opens with subscription
frames carrying ordinary VDJScript queries by id, and VirtualDJ pushes typed values
(`val` float32 / `txt` / `fail`) plus browser folder XML, settings, and selected-folder
state. Replaying a captured opener is enough to hold a session — no pairing token. Capture
tool: `python3 tools/vdjremote_dial.py <device-ip>`; reference capture at
[tests/vdjremote-opener.bin](tests/vdjremote-opener.bin).

**Subscriptions also DONE (2026-07-27)**: the vocabulary is *all of VDJScript*, not a fixed
schema. Verified by substituting synthetic SUBSCRIBE frames into a replayed opener —
`get_version`, `get_effect_name 1`, `deck 3 get_bpm`, and a full ternary all resolved, and
push-on-change was measured (a load pushed title/artist/BPM/path within the same second;
`get_position` streamed at 33-34 Hz while playing, silent when paused). KIND is a hint, not
a request; `fail` means "no value now", not "bad query". Tool:
`python3 tools/vdjremote_subscribe.py tests/vdjremote-opener.bin 'left:get_title' 'get_clock'`
paired with a `dns-sd -R` advert.

Remaining:

- **Mid-session subscribe/unsubscribe** is untested; only opening-burst registration has
  been exercised. A client that switches views needs it.
- **Map or bypass the `0x02` control id space.** Only four ids are known, all from one
  device skin (`0xc6` play, `0xc7` cue, `0x41` crossfader, `0x36` volume). Whether the space
  is global or skin-defined is open — but `0x31` may make it moot for third-party clients.
- **Mid-session subscribe/unsubscribe** is untested — only opening-burst registration has
  been exercised. A client that switches views needs it.
- **Undecoded types**: device→desktop `0x09`, `0x0c`, `0x27`, `0x29`, `0x34`; desktop→device
  `0x2b`, `0x3b`. Sessions work without understanding them (replay reproduces them), so this
  is lower priority.
- **Waveform data** has not been located in any frame; check inside the `0x25` ZIP payloads.

Record results in:

- [docs/VDJScript Local Test Tracker.md](docs/VDJScript%20Local%20Test%20Tracker.md)

Promote to:

- [docs/Remote Protocol.md](docs/Remote%20Protocol.md)

Done when:

- Action frames are catalogued with example payloads, and the subscription vocabulary is
  characterized as either "any VDJScript query" or a documented subset.

### 9. Map Verbs To Button Editor Categories

Status: Done

Note: 2026-07-27 — verb set, aliases, hidden flag, and categories all extracted

The exact verb set is settled: [tools/extract_verb_table.py](tools/extract_verb_table.py)
extracts VirtualDJ's own verb table (1,028 sorted 16-byte records
`{const char *name; uint32 id; uint32 flags}` at `0x10402d020`), covering 1,007/1,007
HTTP-proven names. Existence and non-existence are now a membership test
(`just verb-table <name>`), aliases are read off shared `id`s, and `flags == 256` marks the
37 Button-Editor-hidden names. 61 alias groups are written into the verb store.

Categories are solved too: a `const char *[38]` name array after the verb table, plus a
non-decreasing `uint8[956]` in `__TEXT,__const` giving the category per verb indexed by
`id + 1`. Both located structurally, no pinned addresses. Confirmed by the live Button Editor
list (read off screen, `flow`..`video` with `defines` skipped), and reproducing
[docs/Button Editor Taxonomy.md](docs/Button%20Editor%20Taxonomy.md)'s per-category counts
exactly — all 37 categories, total 1,028. See
[docs/Undocumented VDJScript Candidates.md](docs/Undocumented%20VDJScript%20Candidates.md)
§Categories.

Note (2026-07-29) that the count agreement is a **reproduction, not corroboration**:
`extract_vdjscript_taxonomy.py` reads the same three structures, only by pinned address instead
of by anchor. Rule 1c2 in [docs/Evidence Standards.md](docs/Evidence%20Standards.md) now says so.
The live Button Editor remains the only independent check.

Four-verb residue: RESOLVED as doc error. `mute`, `silent_cue`, `stems_split`, and `loaded` were
listed under different categories in the taxonomy doc's example column than the mapping gives.
That column is **hand-written**, not extraction output: the extractor emits
`visible_examples[:8]` over an alphabetically sorted table, yet every doc row has exactly 4
entries and four rows are not even alphabetical (`play, pause, stop, silent_cue`;
`mic, linein, aux_volume, mic_eq_high`; `leftdeck, rightdeck, masterdeck, pfl`;
`beatjump, clone_deck, dualdeckmode, mute`). The counts column *is* extraction output, so the
two columns have different pedigree and only the counts carry weight. Mapping stands; the doc's
example column is corrected in place.

### 9b. Remaining Verb-Name Structure Notes

Status: Done

Note: 2026-07-29 — both "done when" conditions are met: every HTTP-proven name is accounted
for by a named structure (the verb table covers 1,007/1,007), and every structure-found name
absent from the store has been added (the 35 hidden verbs, 2026-07-29). Kept because the
corroborating sources are still wired.

Three structures are extracted so far ([tools/extract_binary_verbs.py](tools/extract_binary_verbs.py),
1,019 names): 954 `ACTION_` implementation classes, 812 language-catalog entries, and the
parser's 967-entry alphabetically sorted name table. Their union covers **998 of the 1,007**
names the HTTP sweep proved real.

**Four names prove at least one more structure exists**: `browser`, `config`, `preview`, and
`volume` are real verbs, are ≥4 characters (so `strings` sees them), and appear in none of the
three sources. (`jog`, `no`, `off`, `on`, `yes` are also missing but are simply under the
`strings` length floor — use `strings -n 2` for those, and note a low minimum breaks the
sorted-run detection, so probe them separately.)

Why this is worth doing: the app must match input against a complete set of names, so the sets
exist in the binary. Recovering all of them yields **the exact verb set — including any
undiscovered verbs** — which is the strongest possible outcome for this topic, and it lets the
disproof drop its conservative string leg (see
[docs/Evidence Standards.md](docs/Evidence%20Standards.md) rule 1a).

Start here:

- Locate `browser` / `config` / `preview` / `volume` occurrences and inspect their
  neighbourhoods for table structure, as was done to find the sorted name table.
- The sorted table runs `action_deck` … `zoom_vertical` and omits `load`, `loop`, `cue`,
  `hot_cue`, `nothing` — so it is a *subset* dispatcher, and whatever holds those five is
  another candidate structure worth characterizing even though the union already covers them.
- Both older extractors are stale on this build (`extract_vdjscript_symbols.py` returns 0;
  `extract_vdjscript_taxonomy.py` is address-pinned) — re-anchoring the taxonomy tables would
  recover the Button Editor's own category structure, which is a likely home for the strays.

Done when:

- Every HTTP-proven name is accounted for by a named structure, or the residue is explained.
- Any name found in a structure but absent from the store is swept (`just verb-probe`) and
  recorded as a candidate.

### 10. Discover The Full Function Contract Per Verb

Status: Ready

Note: 2026-07-29 — the ratified priority now that existence, aliases, hidden flag, and
categories are settled. Goal: for every verb, the complete calling contract — **query return
type, accepted argument forms, and undocumented overloads** — established at Tier 1 where
possible and recorded as structured per-verb data, not prose.

Contract fields to establish per verb:

- **Return type in query position: HTTP leg DONE (2026-07-30)** —
  [tools/sweep_return_types.py](tools/sweep_return_types.py) sampled all 652 query verbs in
  three read-only contexts against live VirtualDJ: 623 typed (334 bool / 145 int / 68 float /
  4 percent / 72 text), 0 capability conflicts vs the structural matrix, gated in
  `just check`, queried with `just verb-return-type <name>`. It also refuted the first slot
  labeling: slot 3 is a generic variant query, not onQueryBool — structure claims capability,
  observation claims type. Remaining sub-legs: the 29 all-empty verbs need richer contexts,
  and the Remote-protocol typed sweep (`val` float32 vs `txt` VALUE frames) would confirm
  wire-level types independently of HTTP text rendering.
- **Argument forms — binary-first (reprioritized 2026-07-30, partially DONE)**. The
  E_INVALIDARG method fingerprint landed in the contracts artifact: **436 verbs demand an
  argument somewhere, 114/116 agreement with the sweep's needs-args kind, and 301
  bare-answering query verbs flagged as taking OPTIONAL arguments** — the
  undocumented-overload queue (`summary.optional_arg_queries`), invisible to the bare sweep.
  `method_strings` recovers per-method keywords (`loaded` → `opposite`, `get_time` →
  `short`). Remaining streams for the *forms and types*:

  0. **Runtime parser walk (H4, added 2026-09-07).** Before more sweeps, follow the named
     `IAction::create` on the unstripped 18.0.9246 build for delimiter, quoting and fallback
     rules; each rule becomes a discriminating 10b test. See H4 above for the boundary.
  1. **Argument keywords — DONE (2026-07-30)**; **types — closed as not-extractable.**
     `__stubs` are now named via DYSYMTAB's indirect symbol table (this build is classic
     `LC_DYLD_INFO_ONLY`, not chained fixups), so methods that compare an argument against
     literals are detectable: **259 verbs carry `keyword_candidates`**, recovering
     undocumented enums (`get_bpm absolute|ghost`, `browser_window sidelist|karaoke|…`,
     `loaded opposite`, `get_time short`, `sampler_group_volume touchrelative|locked`).
     Argument *types* were attempted through the same route and do not survive: param access
     is inlined, and a verb's library calls describe what it does with an argument, not how
     it fetches one (`_strcasecmp` appears in numeric-arg verbs). Types are a Tier-1 job.
  2. **HTTP probe in query position** (Tier 1): start with the 301 optional-arg queries and
     the recovered keywords. **Method note (2026-07-30, probed live)**: optional-arg verbs
     silently ignore unknown arguments (`loaded bogusword` → `yes`), so error codes cannot
     confirm a form — probes must compare VALUES across forms in a state where they would
     differ (e.g. `loaded opposite` with exactly one deck loaded). `get_time` demonstrated
     the pattern: bare returns one mode, any argument switches to another. Query-position
     probing is side-effect-free; execute-position confirmation only for whitelisted safe
     verbs, with independent readback (rule 4), never `system`/file/database verbs.
  3. **Shipped-XML corpus mining + appendix parsing** (Tier 2): demoted to corroboration of
     actually-used forms — the binary and the probes discover; the corpus confirms
     parser-accepted usage.
- **Capability matrix: DONE (2026-07-29)** — the vtable-override extraction worked on the
  first attempt. [tools/extract_action_contracts.py](tools/extract_action_contracts.py) walks
  the surviving RTTI (name → typeinfo → vtable) and emits
  [tests/action-contracts.json](tests/action-contracts.json): 955 classes ↔ 955 ids as a
  checked bijection, capability matrix (execute / bool / number / text query) with slot
  meanings calibrated from HTTP-proven verbs, family taxonomy from the class hierarchy
  (100 toggles, 56 sliders), and context mixins. Sweep agreement 652/652 (query) and
  181/186 (action-only); the 5 outliers surfaced a lead — slot 7 is probably the
  options-menu provider (`browser_export`, `*_options` override only it). Gated in
  `just check`; query with `just verb-contract <name>`. See the Candidates doc §Contract
  structure.

- **Slot names: DONE (2026-08-29)** — bundle `18.0.9246` is the last unstripped build, so
  [tools/extract_action_vtables.py](tools/extract_action_vtables.py) resolves every vtable
  entry to a named method ([tests/action-vtables-9246.json](tests/action-vtables-9246.json)).
  Slot 7 is `onUp`, not the options-menu provider guessed above; 8/9 are `onSaveState`/
  `onLoadState`. Recalibrating `query_text` off slot 5 (was reading slot 4, the bool query)
  moved 154 verbs; the old values are preserved as `query_bool`.
- **Verb table: refreshed to 18.0.9583 (2026-09-02).** 1,032 records, 958 distinct ids,
  62 alias groups. Four verbs are new since 9482 — `goto_beat_in_bar` (canonical spelling of
  `goto_bar`, same id 106), `karaoke_clear`, `repeat_start_fade`, `shoutout` — all four with
  bundled English descriptions, now in the Broad Verb Index and the store. The contracts
  bijection is whole again at 958 ↔ 958.
  9583 **dropped the `const char *[38]` category-name array** (no member survives anywhere in
  the executable, nor in `languages.zip`), but the `uint8[distinct_ids + 1]` id → category
  array is intact. `extract_verb_table.py` now falls back to a pinned name list and records
  `summary.categories_source`. The pinned order is not a guess: it is what the array reads on
  both `18.0.9246` (unstripped, read directly) and `18.0.9482`, and carrying it forward
  reproduces the previous category for **1,028/1,028** verbs shared with 9482 and
  **1,025/1,025** shared with 9246, placing the four new verbs in audio / karaoke / repeat /
  sampler. Re-anchor on the binary again if a later build restores the names.

### 10a. A read-only introspection plugin — the only instrument for four questions

Status: Ready

Note: **The channel is OPEN (2026-08-15).** The plugin builds, loads, and has returned its
first full capture: 1,028 verbs × both query callbacks, in `tests/plugin-introspection.json`
(`just plugin-probe <name>`). See the tracker's "Plugin Channel (VDJIntrospect)" section for
the evidence table. Headline results:

- **The documented `DllGetClassObject` path is live.** VirtualDJ type-probes with six IIDs in
  order (Dsp, Buffer, VideoFx, VideoTransition, VideoTransitionMultiDeck, then Basic) and stops
  at the first accepted one. Ad-hoc signing suffices; Xcode is not required.
- **`master_beat_num` is settled: the float-bits defect is in the CORE.** `GetInfo` hands back
  the double `1083943558.0` — the int32 reinterpretation of float32 `4.8646` — so HTTP was
  faithfully rendering an already-broken number. This was the first named experiment; it is
  done.
- **A definitive channel map**: 532 verbs answer on both callbacks, 67 text-only, 11
  numeric-only, 418 on neither, agreeing with the HTTP sweep's kinds (181/181 action-only).
  `E_INVALIDARG` is the numeric channel's "wrong channel" code; the text side says `S_FALSE`.
  Caveat: VirtualDJ writes `0.0` to `*result` even on `E_INVALIDARG`, so the HRESULT is the
  answer, not the value.

Follow-up captures, 2026-08-15 (`tests/plugin-introspection-{leads,controls}.json`) — all
three leads closed, details in the tracker:

- **The HRESULT keyword-discrimination hypothesis is CONFIRMED.** 26 of 165 keyword/nonsense
  pairs differ by HRESULT (`is_using zzznotakeyword` → `E_NOTIMPL`; `action_deck`,
  `device_side`, `get_ns7_platter` → `E_INVALIDARG`), 14 more by value. **This is the method
  for the keyword queue** — it needs no prepared state, unlike value comparison. Two argument
  traps found: `get_license` and `mixermode` return `on` for nonsense arguments.
- **Slot 5 is the label provider** (`stop_button` → `"■"`), and **slot 3 backs both
  callbacks**; slot 4's role is unproven. Exact partition, no remainder — the slot table in
  [docs/Plugin SDK.md](docs/Plugin%20SDK.md) is corrected.
- **Deck context was the wrong explanation** for the 50 silent query verbs, proven with a
  control (`deck 1 get_bpm` → `120`, so the prefix does work; `left get_bpm` fails — the
  `deck` scope word is required). They are 27 verbs HTTP also answered empty (the plugin
  channel distinguishes "no value" from "empty value"; HTTP cannot), 7 wanting an argument,
  and 21 needing **implicit defaults HTTP supplies and a plugin call does not**
  (`get_effect_slider_name 1 1` → `Strength`).

Fourth and fifth captures, 2026-08-15 (`-remaining`, `-late`), closing both remaining items:

- **The silent browser readers were startup timing, not a missing plugin context.** `OnLoad`
  fires while VirtualDJ is still starting. The plugin now sweeps an optional second list ~40s
  after load, and all six `get_browsed_folder*` verbs answer there with nothing else changed.
  **Method rule: an `E_INVALIDARG` from a load-time probe means "not available now", not "no
  such form"** — re-take negatives from the delayed sweep before recording them. Song-level
  readers (`get_browsed_comment|composer|song`) stay silent even late; a highlighted song is
  the next variable.
- **The execute-capable keyword verbs are swept**: 1,126 probes over 217 verbs, query position
  only, 10 excluded outright (file/config/system families, listed in the tracker). 51 pairs
  confirmed by HRESULT over 25 verbs, 36 more by value over 27 — full enum sets recovered for
  `crossfader_curve`, `maximize`, `loop_adjust`, `browser_scroll`, `cue_display`,
  `auto_bpm_transition_options`, `djc_button_select`. Reproduce with
  `just plugin-keyword-report remaining`.
- **Probing execute-capable verbs in query position changed no state**: all 217 bare verbs
  shared with the baseline returned byte-identical values afterwards, HTTP agreeing. One idle
  session's evidence, not a general proof.
- **Host callbacks work off the main thread** — the delayed sweep runs on a detached timer
  thread and completed cleanly. Undocumented in the SDK; one session's evidence.

Sixth capture, 2026-08-15 (`-prepared`) — taken through a **trigger loop** rather than a
restart, which is the ergonomic fix for this whole task: the plugin's thread now polls for a
trigger file, so `just plugin-go` re-sweeps in ~1s while VirtualDJ keeps running. Set the app
up by hand, then ask for a capture.

- **`loaded opposite` is confirmed** — with one deck loaded it returns `off` where nonsense
  returns `on`. This was the case named on 2026-07-30 as needing prepared state, and it is the
  proof that the *value* test works where error codes cannot.
- 25 more pairs confirmed over 12 verbs, including `get_key pioneer|rane|roland|harmonic`
  (controller key notations: 14, 13, 2, 02A vs a default `Ebm`), `get_loaded_song_color
  red|green|blue`, `get_position loopin|loopout`, and `get_song_event`.
- **Browser readers are state-gated, not unsupported**: `get_browsed_key`,
  `get_browsed_filepath` and `sidereco_song` answer once a song is *highlighted*.

Still open, and now clearly bounded:

1. **705 keyword pairs still indistinguishable.** Not disproof — each needs the specific state
   its own verb reacts to. This is per-verb work with a fixture, not another sweep, and the
   trigger loop makes each attempt cheap.
2. **`get_browsed_comment|composer|song`, `get_sample_info`** — likeliest reading is that this
   track carries no comment/composer tag, so `E_INVALIDARG` means "no value". Needs a track
   known to have one.
3. **The untouched half of the SDK.** `GetSongBuffer` is now **DONE** — fully characterized
   2026-08-15 (frames, interleaved stereo, interior pointers into one resident decoded buffer,
   44.1 kHz), which is the input side of the waveform cliff.

   `OnKey` is **attempted and unresolved**. Two plugin types were built and tested — a basic
   `AutoStart` plugin and an active Sound Effect with a visible panel — and neither receives
   anything through `IVdjVideoMouseCallbacks8`, though the slot is accepted every time. The
   interface name is the best remaining explanation: its `(x, y)` coordinates want a *video*
   surface. The last candidate is a video FX plugin, which needs video output.

   Worth knowing before spending more on it: the plugin *lifecycle* question is settled as a
   by-product. A recognised functional type is driven (`OnStart`, `OnProcessSamples`,
   `OnParameter` all fire); a basic plugin is loaded and left alone. So "get a surface, get
   input" has been tested twice and failed twice, and video FX is the only shape left.

   `VDJINTERFACE_SKIN` is **DONE, and it paid off** (2026-08-22). A Sound Effect built with
   `tools/plugin/build.sh --skin --install` returns `VDJINTERFACE_SKIN` from
   `OnGetUserInterface`; VirtualDJ calls it when the effect's GUI is shown, and calls it
   **again on every panel open**. The plugin serves `skin.xml` / `skin.png` from disk rather
   than from bundle resources, so a skin edit costs a panel re-open instead of a restart:
   `just plugin-skin-prepare <xml>` → `just plugin-skin-reload` → `just plugin-skin-log`.
   Everything rendered — backtick VDJScript, `action=""` queries, `visibility=""` conditions,
   `<define>` classes, sprite offsets against an in-memory PNG.

   First results off the new loop, all in the tracker: **starred placeholders are required**
   to substitute at all (in `format=""`, `text=""`, numeric attributes *and* conditions), and a
   starred placeholder inside a condition is genuinely evaluated — which closes the "still
   unclear, should be tested per pattern" note in [Skin SDK](docs/Skin%20SDK.md). The panel
   surface is a **flat element list**: `<group>` renders nothing. And `<group class="...">`
   **crashes VirtualDJ** — twice, reproducibly enough to be worth a warning, mechanism unknown.

   What the loop cannot reach: the waveform family. A plugin panel has no deck, so
   `<scratchwave>` and the stacked-`<size condition="">` question in
   [Skin Waveforms](docs/Skin%20Waveforms.md) need a real deck skin as the fixture. That is the
   next skin task, and it is now a well-specified one.

Ergonomic note for whoever continues: **each capture costs a VirtualDJ restart**, because the
sweep runs at plugin load. Three restarts got the above. If iteration gets heavy, a watcher
thread re-sweeping when `probes.txt` changes would remove that — at the cost of calling the
host callbacks off the main thread, which is untested.

Revised 2026-08-11 after re-reading the full `IVdjCallbacks8` surface; the earlier framing of
this task ("faster verb prober") undersold it in one direction and oversold it in another, and
both are corrected below.

Landed 2026-08-15 — plan steps 1 and 2, minus the host:

- [tools/plugin/VDJIntrospect.cpp](tools/plugin/VDJIntrospect.cpp) builds and ad-hoc signs with
  **Command Line Tools `clang++` — Xcode is not required** (`just plugin-build --install`), and
  VirtualDJ carries `com.apple.security.cs.disable-library-validation`, so a self-signed bundle
  is loadable. It reads a probe list at load and records, per probe, both HRESULTs, the raw
  `double` with its bit pattern, and the text buffer. Read-only by construction: the source
  contains no `SendCommand` call at all.
- An offline harness with a fake `IVdjCallbacks8` proved the sweep, the JSON escaping (binary
  answers survive), the once-guard, and GUID negotiation. The python side
  ([tools/plugin_introspect.py](tools/plugin_introspect.py): `prepare`/`status`/`collect`/
  `--get`/`--check`, gated in `just check` with an explicit skip until the first capture)
  round-trips that harness capture.
- Untested is everything needing the host: whether VirtualDJ loads it, from which folder
  (`AutoStart` is the first guess; override with `VDJ_PLUGIN_SUBDIR=`), and via which IID. The
  plugin answers for both published IIDs and logs every `DllGetClassObject` call, so a failed
  load is still diagnosable — and that log is the evidence for the second-loading-path question
  in [docs/Plugin SDK.md](docs/Plugin%20SDK.md).
- Next step is manual: install, restart VirtualDJ, `just plugin-prepare`, restart,
  `just plugin-status`.

**What it is genuinely the only channel for.** These have no HTTP, Remote, binary or XML
equivalent — not a speedup, an access path that does not otherwise exist:

```cpp
HRESULT GetSongBuffer(int pos, int nb, short **buffer);   // PCM of the loaded song, any position
HRESULT OnProcessSamples(float *buffer, int nb);          // the live audio stream
void    OnKey(const char *ch, int vkey, int modifiers, int flag, int scancode);
bool    OnMouseDown/Up/Move(int x, int y, int buttons, int keyModifiers);
HRESULT GetTexture(EVdjVideoEngine, int deck, void **texture, TVertex **vertices);
HRESULT DrawDeck(int deck, TVertex *vertices);
HRESULT OnTransformPosition(double *songPos, double *videoPos, float *volume, float *srcVolume);
// plus VDJINTERFACE_SKIN: the plugin supplies skin XML at runtime
```

Mapped onto this repo's three standing cliffs:

- **Waveforms.** [docs/Skin Waveforms.md](docs/Skin%20Waveforms.md) is reverse-engineered from
  skin XML and observed rendering. `GetSongBuffer` returns the sample data VirtualDJ itself
  draws from, at arbitrary positions; `OnProcessSamples` gives the live stream. That is the
  input side of every `<scratchwave>` / `<blockwave>` / `<beattunnel>` question.
- **Mappers.** `OnKey` exposes VirtualDJ's own input model — virtual key, modifier mask,
  scancode, plus a `flag` that is a **candidate for press/release** (unverified; confirm from
  inside). `while_pressed` and the whole down/up half of the mapper contract are currently
  "not established" precisely because **HTTP has no press**. This is the first channel that
  might carry one.
- **Skins.** `VDJINTERFACE_SKIN` takes a skin XML buffer at runtime. Today, testing a skin
  hypothesis costs an edit-file-and-restart cycle; this makes it a loop, against a 2,600-line
  SDK doc with open `visibility` / `condition` questions.

Additionally, there is **no push channel anywhere else in the repo** — HTTP and Remote are both
pull-only from our side. `OnParameter(int id)`, `OnKey` and the sample callbacks are events,
which is the only way to observe *when* something changes rather than sampling for it.

**What it does for verb signatures specifically — a real but narrower win.**

```cpp
virtual HRESULT SendCommand(const char *command)=0;                            // execute
virtual HRESULT GetInfo(const char *command, double *result)=0;                // numeric query
virtual HRESULT GetStringInfo(const char *command, void *result, int size)=0;  // text query
```

- **The HRESULT is returned separately from the value.** HTTP collapses both into one response
  body, so any case where the status code carries information the value does not is invisible
  to us today. That is exactly the silent-fallback problem: `loaded opposite` and
  `loaded bogusword` return the same value over HTTP, but may differ in HRESULT. **This is the
  one place the plugin can discriminate a recognized keyword from an ignored one**, and it is
  worth an early experiment — but it is a hypothesis, not a known result.
- **Native types, no flattening.** Settles the `master_beat_num` float-bits defect in one call
  (core defect vs HTTP rendering), and calling both `GetInfo` and `GetStringInfo` per verb
  yields a definitive type-path map rather than one inferred from rendered strings.
- **Different prerequisites.** No Network Control plugin, no Pro license — a fifth Tier-1
  channel, which [docs/Evidence Standards.md](docs/Evidence%20Standards.md) already lists as
  planned and explicitly forbids claiming anything from until it exists.

**What it does NOT solve, stated plainly.** Throughput is not the bottleneck — the 2026-07-30
sweeps ran ~3,000 HTTP probes in minutes. And apart from the HRESULT channel above, argument
forms still need **prepared state** where forms would produce different values; a plugin
supplies no state a fixture harness cannot. See 10b, which is cheaper and should not wait on
this.

Plan:

1. Build the minimal plugin read-only: `GetInfo`/`GetStringInfo` sweeps only, **no
   `SendCommand`**, so loading it cannot change state. Execute-position testing comes later
   behind an explicit switch.
2. Emit the same artifact shape as the existing sweeps (`tests/…json` + a `just` query) so it
   joins `just get-verb` for free.
3. First experiments, in order: **the HRESULT discrimination test** (a known-good keyword vs a
   nonsense one on the same verb — if the codes differ, the entire 217-verb undocumented
   keyword queue becomes mechanically decidable, and that single result is what determines how
   much the plugin is worth); `master_beat_num` via `GetInfo`; the both-channels type map.
4. Then the cliff work, which is the larger prize: `GetSongBuffer` against a known file to
   ground [docs/Skin Waveforms.md](docs/Skin%20Waveforms.md); `OnKey` logging to establish the
   press/release model for [docs/Mapper XML.md](docs/Mapper%20XML.md).

Prerequisites and constraints:

- SDK headers are **not** vendored — no license grant exists. Fetch to `vendor/` (gitignored);
  see the `.gitignore` entry and [docs/Plugin SDK.md](docs/Plugin%20SDK.md).
- Xcode build, macOS arm64. The community examples build under Xcode 14.3 / macOS 13.3.
- Open question to resolve while building: the shipped `beatport16_vdj` bundle exports no
  `DllGetClassObject`, so a second loading path may exist. A built test plugin settles it.
- Also worth probing from inside: whether an *internal* verb-registration path exists, which
  is the one scope limit on Evidence Standards rule 1b.

Storage: **DONE (2026-07-30)** — `just get-verb <name>` joins the store record with the verb
table, the structural contract, the HTTP existence probe, and the observed return type at
read time (`--raw` for the bare record). Artifacts stay authoritative; nothing is copied into
the store, so a re-extraction is picked up without a migration.

Done when:

- Every query verb has an observed return type with the observing channel recorded.
- Every verb has an arg-forms record: observed forms, rejected forms, or `no-args`.
- Overloads (same verb, distinct arg shapes with distinct behavior) are recorded as such.
- The store's per-verb record surfaces all of it through `just get-verb`.

### 10b. State-fixture harness + argument prober (do this first — it is the cheap unblock)

Status: Ready

Note: **Steps 1-2 built 2026-09-02; the sweep itself is unrun.** Python over the existing
HTTP channel; no build toolchain, no SDK, no new evidence tier. Added 2026-08-11.

Step 1 shipped as [tools/fixtures.py](tools/fixtures.py) (`just fixtures`,
`just fixture-verify <name>`, `just fixture-establish <name>`): six named states —
`one_deck_loaded`, `both_decks_loaded`, `deck2_playing`, `loop_active`, `fx_slot_1_on`,
`sampler_slot_loaded` — each polling its own readbacks and raising `FixtureError` rather
than reporting a state it could not confirm. Fixture audio is generated locally with ffmpeg
(90 s, 120 BPM pulse train, cached under `~/Library/Caches/virtualdj-api-reference/`) so
results never depend on the user's collection, and teardown restores each deck to the
contents and transport state observed at establish time. `--check` validates definitions
offline, so `just check` stays hermetic.

Not yet done: `stems_active` needs a stem-capable fixture track and an analysis wait, so it
is deliberately absent rather than half-verified.

Step 2 shipped as [tools/probe_arg_forms.py](tools/probe_arg_forms.py)
(`just probe-arg-forms`, `just verb-arg-forms <name>`): 483 target verbs — the 300 that answer
bare while demanding an argument somewhere, plus every verb carrying recovered
`keyword_candidates` — probed as **token lists** (bare, each token alone, then all ordered
pairs: 835 single-token and 3,112 pair forms), inside each fixture, `/query` only. Two
unrelated nonsense controls run alongside every verb; they must agree with each other or the
reading is reported `unstable` rather than scored. A form is `recognized` only where it
separates from garbage in at least one state. Full sweep: 32,376 requests over 6 fixtures
(13,704 with `--no-pairs`).

**Run 2026-09-02** (`tests/verb-arg-forms.json`): 176 single-token tails confirmed across 89
verbs. The pair result needed the classifier fixed first — separating from nonsense is not
enough for a two-token form, since `is_using loop zzqqx` separates purely because `loop` does.
Comparing each pair against its own singles splits 763 apparent hits into 416 first-token-wins,
288 singles-agree, 51 beyond-singles and 5 last-token-wins, leaving **8 verbs with real
two-token grammar**, not the 62 first claimed.

`get_song_event` and `browsed_song` were then confirmed by direct query: the first takes
`[current|next] <field>` with the selector defaulting to `current`, the second is an exact-match
predicate `browsed_song <field> <value>` requiring both tokens. Both are documented in
[VDJScript Verbs](docs/VDJScript%20Verbs.md).

`get_cpu` and `is_using` are **disputed** — their two-token verdict flipped between independent
`--repeat 3` runs, `get_cpu` because its value drifts faster than repeat-agreement can catch and
`is_using` because `effect inaudible` depends on FX state the fixture does not pin. Two agreeing
runs is the guard that caught both; `--repeat` alone was not enough.

**Catalog + corpus extraction, 2026-09-03.** `Resources/languages.zip` is the source of the
official verbs-appendix prose — verified verbatim against the published page — so the appendix
is available offline and the repo had been reading that file for verb *names* only, discarding
816 descriptions. [tools/extract_action_catalog.py](tools/extract_action_catalog.py) now emits
them (`tests/action-catalog.json`), with the quoted parameters pulled out: 97 verbs document
parameters, 18 promise more than one argument.

The cross-check against the probe artifacts is the useful part, and it cuts three ways:
**16 verbs confirmed by both**, **90 documented but never probe-confirmed** (`auto_cue`
always/on/off, `display_time` elapsed/remain/total, `broadcast` direct/podcast/server/video …
— each one a state the fixtures never built, or an observable the probe could not see), and
**64 probe-confirmed but undocumented** (`browser_scroll` top/bottom/parent, `cue_display`
num/number, `action_deck` left/right …). The 90 are the immediate worklist: the meaning is
already written down, only the local confirmation is missing.

[tools/extract_script_corpus.py](tools/extract_script_corpus.py) collects the sanctioned
examples into `tests/vdjscript-corpus.json`: 1,390 snippets over 372 verbs, 269 quoted in
catalog descriptions and 1,131 from shipped Built-In XML, deduped with provenance on each.
Two provenance traps were fixed while building it — prose sentences beginning with a verb-like
word (`"Load saved loop named …"`) are excluded by requiring a lowercase first character, and
only `Built-In` trees are read, since `examples/Pads/Quarantine` and the repo's own skins would
otherwise let our test fixtures masquerade as vendor evidence.

**Catalog-driven probe run 2026-09-03** (`--from-catalog`: take each verb's candidates from the
catalog's own prose rather than the binary). 97 verbs, 196 single-token forms, read 2x in all
six fixtures. **27 verbs confirmed a documented parameter locally, 16 of them tokens no
previous sweep had found** — `display_time` elapsed/remain/total, `get_time` absolute/remain/
total, `loop_adjust` in/move/out, `sampler_mode` hold/stutter/unmute, `wheel_mode` jog/loop_in/
loop_move/loop_out, `param_cast` frac/ms/relative, `scratch_dna_option` drymix/quantized,
`auto_cue always`, `cross_assign thru`, `timecode_mode relative`, `get_vu_meter sampler`,
`effect_select audioonlyvisualisation`, `effect_select_multi video`. The catalog is a better
candidate source than the binary: it is written for these verbs, so its hit rate is far above a
generic lexicon's.

Cross-check moved from 16/90/64 to 26/81/64. The 81 that remain documented-but-unconfirmed are
mostly *contextual* — `broadcast` direct/podcast/server/video, `effect_arm_deck` aux/mic/sampler,
`automix_editor_movetrack` current/next/previous — states no fixture builds. Those need
fixtures, not more probing.

Fixed while doing this: `--merge` **replaced** a verb's forms with the incoming run's, so
merging a narrow re-probe over a broad sweep deleted measurements (950 recognized forms
collapsed to 535) and manufactured disputes for verbs whose pairs the new run never sent. It
now UNIONs form lists and disputes only a form both runs actually measured.

Still next: (1) fixtures for the contextual parameters — the count is
`just action-catalog --cross-check` → `documented_but_not_probe_confirmed`, not a figure to
quote; (2) mine corpus tails as a third independent source of argument forms; (3) use the corpus
as a parse-regression set for every grammar claim in
[VDJScript Grammar](docs/VDJScript%20Grammar.md). (2) and (3) have since landed.

**The worklist itself was wrong, and was repaired 2026-09-06 before more probing.** Three defects
in the catalog's parameter tokenizer, each distorting it in a different direction:

- **Nested quotes desynchronised the scanner.** In `'get time_min "absolute"'` the inner `"`
  closed the outer `'` span, so the scanner resumed mid-example and silently dropped the real
  parameters that followed. Single- and double-quoted spans are now scanned separately, which
  raised the verbs with documented parameters from 96 to **146** — fifty verbs whose documented
  vocabulary had never been visible to the cross-check at all.
- **The verb's own name came out as one of its parameters** (`browser_gotofolder`,
  `get_beat_num`, `loop`, `pad_page` …), because the catalog quotes whole examples.
- **Doc example names were treated as vocabulary to confirm** — `loop_load "myloop"`,
  `rack "unit1"`, `set "varname"`, `os2l_scene "myscene"`. These can never be confirmed. They now
  land in `documented_example_placeholders`, classified by absence from the binary's string pool,
  with two guards learned the hard way: a token any other source vouches for is never a
  placeholder (whole-string matching had called the real `sampler_mode` keywords `stutter` and
  `unmute` placeholders, since they only occur inside longer strings), and a signed token is
  stripped before the lookup (`browser_sort "+bpm"` is a real key wearing a direction prefix).

**Two new inputs so focused work stops being invisible.** A probe that writes its own artifact —
the known-position fixture proving `get_time cue1/loopin/loopout` — now feeds the cross-check, so
it stops listing settled tokens as unconfirmed. And a `documented_but_locally_refuted` bucket
holds tokens a local test measured behaving exactly like its nonsense controls, so nobody is sent
after them again.

**First worklist entries actually closed, same day.** The `get_time_*` family, probed on a fixture
paused at a known position with deck pitch at **+8.33%** so the pitched and unpitched timelines
differ: `elapsed`, `remain`, `total` and `absolute` all separate from two agreeing nonsense
controls on `get_time_sec` (32 / 50 / 23 / 55), corroborated on `_min` and `_ms`. `display_time`
returned exactly what both nonsense tokens returned on every variant — it was never a parameter,
only the setting named in prose, and it is refuted on all seven verbs that listed it.

That pitch also sharpened an earlier result: `get_time 'absolute'` returned **55000** where
`remain` returned 50769, and 55000 is exactly 90000 − 35000 — the remaining time on the
*unpitched* timeline. The known-position run could not separate the two because pitch was 0 there,
which is why `absolute` had looked merely equal to `remain`.

**Execute-position pass run 2026-09-03** ([tools/probe_execute_forms.py](tools/probe_execute_forms.py),
`just probe-execute-forms`, artifact `tests/verb-execute-forms.json`). Motivated by `deck all`:
32,376 queries could not see it because the query path collapses it to deck 1, and one execute
made it obvious. Method is two baselines per form — from `off` and from `on` — which is what
separates *set* from *flip* from *no-op*; from one baseline they are indistinguishable.

**Query-side entries closed 2026-09-07** (tracker: "Documented Parameters Taken Live
2026-09-07"): `get_loaded_song` album/title/artist/playcount, `get_key` harmonic,
`get_saved_loop` next (and the undocumented `len`, seconds), `get_pitch_zero` absolute, and
`get_date` as a strftime format string with the catalog's `format` reclassified as a
placeholder. Undiscriminated, not refuted, and needing a state no fixture builds:
`get_limiter` outputs (nothing playing), `get_time_sign` (never negative here),
`get_time_hour` (short track), `get_key musical` (keyDisplay already musical). Recorded in
`LOCAL_CONFIRMED` so the cross-check stops listing them. A second batch the same day added
`get_browsed_song` title/playcount/artist, `browsed_song` rating (a predicate in query
position), `sampler_loop` current, `get_time` to_lyrics; reclassified `get_version` 2026,
`get_text` title/on/off and `get_artist_before_feat` featuring as the doc's own words
(`LOCAL_PLACEHOLDERS`); and left `get_song_event`, `get_automix_song`, `get_slip_time`,
`filter_label`, `effects_used` undiscriminated — each returned E_FAIL or one constant on every
form in the state built, so they want a playing deck, an automix list, slip, or an active effect.
A third pass the same day used the `fx_slot_1_on` and `deck2_playing` fixtures: `get_song_event`
current/next and volume/hasbeats/remaining confirmed on a playing deck; the effect-name argument
confirmed on `effect_active`, `effect_select`, `effect_select_multi` with the loaded Phaser, and
the catalog's `flanger`/`echo` recorded as example names; level/VU/limiter tails still
undiscriminated because the meters read 0 on a playing deck in this setup (routing, not the
verb). Tracker: "Documented Parameters Taken Live 2026-09-07 (fixtures)".

**Corrected same day:** the pass reported `auto_bpm_transition`'s own candidates
(`source_original`, `target_original`, `target_current`) as behaving like junk, and this file
first recorded that as corroborating the query negative. The official verbs appendix documents
all three as parameters forcing which BPM the transition lands on — the probe's observable was
a boolean saying whether a transition is *running*, which cannot see which BPM it targets. The
appendix also documents `auto_bpm_transition_options 'stems' 'vocal'`, a two-token tail, which
independently confirms what `verb-arg-forms.json` found structurally. **Read
`tail-ignored-in-execute` as "not visible in this observable".** ~~Open task: re-test those three
with two decks at different BPMs, reading the resulting BPM over time.~~

**That open task is closed (2026-09-07)**, and it settled the reading above.
[tools/probe_bpm_transition.py](tools/probe_bpm_transition.py) (`just bpm-transition`, artifact
`tests/bpm-transition-forms.json`, gated in `just check`) builds the state no fixture has — a
100 BPM track on deck 1 against a 120 BPM track pitched to 132 on deck 2, both stopped, so
`source_original`/`target_original`/`target_current` are three distinct numbers — and reads
**where the pair of decks settles** instead of whether a transition is running. Two runs, order
reversed. `source_original` lands on 100 and `target_current` on 132, neither reachable by
anything else, so both are confirmed; `all` lands like `target_current` but disengages, where
`target_current` alone leaves the transition running. Bare and both nonsense controls land on
120, which is also where `target_original` lands: it **names the default**, so this observable
cannot separate it from an ignored tail — retested with `smart_play` off, same default — and it
stays on the worklist with the reason recorded rather than being called refuted. Two method
findings came out of it, both of which had corrupted a run first: the verb is a **toggle**, so a
form that leaves a transition engaged makes the next form stop it instead of starting one (the
prober now waits for disengagement and aborts if one will not stop), and a form that lands where
the deck already sits is stable from the first read, so the settle loop needs a minimum window.
Tracker: "`auto_bpm_transition`: The Observable Was Wrong, Not The Parameters".

Yield: the tail-handling rule is **verb-specific**, not universal. On 9 of 10 toggles a junk
tail suppresses the action entirely; on `auto_bpm_transition` it is ignored and the toggle
flips anyway. Only one token turned up that the query sweeps had missed —
`auto_bpm_transition all` — and it reads as the target keyword again, not verb vocabulary. The
verbs' own binary-recovered candidates behaved like junk in execute position too, so the query
sweep's negatives are corroborated rather than overturned.

**Two safety lessons, both worth keeping.** The first run aborted on `timecode_cd_mode`, which
went `on` and would not come back — `off`, `0`, bare toggle and deck-scoped forms all left it
`yes`. It is not in `settings.xml`, so it should be runtime-only and clear on restart; **verified
2026-09-07 — after a restart the query reads `no`**, recorded on the verb record. Still one-way
within a session: no form found here turns it off. It reached the probe because of a plain bug: `table.get(name)`
against an artifact shaped `{"summary":…, "verbs":{…}}` returns `None` for every verb, so the
**entire category deny-list was inert** — `timecode`, `browser`, `cues`, `database` were never
excluded and only the name and audible filters were doing any work. Fixed, and the tool now
exits if the table carries no categories rather than trusting it. Added since: a **pre-flight
round-trip** (flip once, put it back, skip the verb if it does not return — it caught four
verbs that ignore `on`/`off` entirely) and **partial results on abort**, because the first run
threw away 25 verbs of completed work when the exception escaped.

Next in this direction: the allowlist is deliberately tiny (18 verbs, settings-only, silent).
Widening it to the audible tier (`--include-audible`: faders, mics, playback) needs an instance
nobody is listening to, and widening past toggles/sliders needs a restore story for verbs whose
state is not a single readable value.

**Shared-lexicon pass run 2026-09-02** (`--lexicon`, 25 tokens proven real for more than one
verb, 215 candidate-less verbs, 5,375 forms read 2x per fixture). Yield: **`all` is a reserved
tail token on 22 verbs** — the whole sampler family plus `loop_load`, `loop_select`,
`load_skin`, `load_pulse`, `effect_stems`, `effect_dock_gui`, `apply_audio_config` — and
`wheel_mode` takes `browser`/`search`. What `all` *does* was answered on 2026-09-07, in the
`sampler_slots_differ` fixture that follow-up asked for: **`all` returns exactly the bare value in
query position and does nothing in execute position** on the two verbs whose state is readable and
restorable — `sampler_volume all 0.7` and `sampler_volume_nogroup all 0.3` moved nothing, where
`current` and a slot number both did. The `recognized` verdict was an artifact of how these verbs
fail: an unrecognized tail *errors*, so separation from a nonsense control is satisfied by any
token the parser accepts. **Where junk errors, separation from junk is evidence of parsing, not of
meaning** — the comparison that carries meaning there is against the *bare* form, which the
artifact already records as `same_as_bare_everywhere`. Not a claim about the other 24 verbs:
`sampler_stop all` is the shape that would mean "every slot", and confirming it needs samples
actually playing, which is audible and was not run. By-product, and worth more than the answer:
**`sampler_volume` is group-scoped** — `sampler_volume 1 0.5` moved all three `Drums` slots
together and left the ungrouped slot alone, where `sampler_volume_nogroup` moved exactly one.
Tracker: "`all`: Recognized By The Sweep, Inert Where It Was Tested".

The pass also needed a second guard. `record_vu` matched 24 of the 25 arbitrary tokens and
`pioneer_cue` 15 — a verb separating from nonsense on half a vocabulary that was not written for
it is drifting under the probe, not speaking. `_flag_undiscerning` now strips those (recorded in
`summary.undiscerning_verbs`), which is the same failure as `get_cpu` one level up: `--repeat`
catches a value that moves between two reads, this catches one that moves between a token read
and its control.

Candidate filtering is done, and the first version of it was wrong in an instructive way: "is
this token a suffix of some `ACTION_<verb>` symbol" is true of nearly every real keyword, since
verbs named `left`, `loop` and `top` all exist — it dropped 300 candidates including
probe-confirmed ones. The token has to reach back *into* the `ACTION_` prefix
(`len(token) > len(verb)`), which drops exactly the one real fragment, `TION_get_text`.

**Superseded — this said the sweep was unrun:** the write-side fixtures unload decks, and the machine's decks
were live. `tests/verb-arg-forms.json` does not exist yet; `--check` skips cleanly until it
does. Run it on an idle instance — the first real question it answers is whether any verb
accepts a two-token tail at all, which nothing to date has established.

The blocker for argument forms is not the channel, it is **prepared state**. Unknown arguments
are silently ignored (`loaded bogusword` → `yes`), so a form can only be confirmed by comparing
values across forms **in a state where the forms would disagree**. `loaded opposite` is
meaningless with both decks empty — which is how the decks sat for most of 2026-07-30's
session, and why 301 optional-arg verbs are still unprobed.

Plan:

1. **Fixture layer.** Named states, each set up and torn down over HTTP execute, each asserting
   its own preconditions before probes run: `one_deck_loaded`, `both_decks_loaded`,
   `deck2_playing`, `loop_active`, `fx_slot_1_on`, `sampler_slot_loaded`, `stems_active`. Fail
   loudly if setup does not verify — a probe against an unestablished state is worse than none.
2. **Prober.** For each verb in `summary.optional_arg_queries` (301) crossed with its
   `keyword_candidates` (259 verbs, 217 undocumented), sample bare vs each keyword vs a
   nonsense control, in every fixture. Record: value-differs-from-bare, value-differs-from-
   nonsense-control. **The nonsense control is the whole design** — a keyword that behaves
   differently from garbage is recognized; one that matches garbage is not.
3. **Multiple tail tokens.** Nothing established so far says whether a verb accepts *more than
   one* token in its tail (`get_time short absolute`, `get_bpm absolute ghost`) — the
   `E_INVALIDARG` fingerprint only reports "demands an argument somewhere", and every probe run
   to date has been single-token. Add a cross-product pass over each verb's recovered
   `keyword_candidates`: bare, each token alone, each ordered pair, and a pair with one nonsense
   member. Four outcomes to distinguish per pair — both recognized, first wins, last wins, pair
   rejected entirely. Cheap to fold in here; expensive to retrofit once the artifact shape is
   fixed, so **design `verb-arg-forms.json` for a token list from the start, not a single
   `argument` string**.

   This matters more than it looks: `GetInfo(const char *command, …)` takes the whole command as
   **one string**, so there is no ABI-level parameter list anywhere — each `ACTION_` class parses
   its own tail. "Signature" for a VDJScript verb therefore means *the grammar of its tail*, and
   token count is the first unknown of that grammar.
4. Emit `tests/verb-arg-forms.json` in the existing artifact shape, gated in `just check`,
   joined by `just get-verb`.

Constraint: query position only. Execute-position confirmation is whitelist-only with
independent readback (rule 4), and never `system` / file / database verbs.

Done when the 217 undocumented keyword sets are each classified recognized / ignored /
state-dependent, with the fixture that decided it recorded alongside.

### 11. Build The Verb Index From The Artifacts, Not From Prose

Status: Done

Note: 2026-09-06, offline. The generator is inverted, the schema is unchanged, both consumers
still pass, and the reconciliation — the actual deliverable — is recorded in the tracker's
"Verb Index Inversion: What The Prose And The Artifacts Disagreed About".

**The defect was live and reproducible.** `lint_mappers.py` reads the index, and before the
inversion it called `flip_record`, `flip_play` and `get_pad_page_name` unknown verbs — all three
real, all three characterised the day before. Every one of the 37 editor-hidden names was missing
because the prose never listed them. The same file now lints with 0 verb warnings.

**The whole diff was 36 entries** (959 of 995 shared entries differed only by an empty
`"aliases": []` the old generator emitted), splitting exactly into the two buckets this task
predicted:

- **Artifacts correcting the prose — 30 alias facts.** 17 pairs the prose missed (`browser` is an
  alias of `browser_zoom`, `preview` of `prelisten`, `goto_bar` of `goto_beat_in_bar`, the four
  `eq_*_slider` spellings, …) and **three claims the table contradicts outright**: the prose made
  `pitch2` canonical for `pitch2_slider` when all four `pitch*` names share id 722 under `pitch`,
  and made `scratch_wheel_touch` canonical when all four share id 153 under `touchwheel_touch`.
  No name was contradicted on *existence* — the prose never invented a verb, it mis-ranked
  aliases and omitted the hidden set.
- **Curated facts with no artifact home — 2, repaired rather than dropped.**
  `auto_bpm_transition` and `auto_bpm_transition_options` carried richer prose than the store, so
  the store was updated to hold it before switching. Every other alias row that lost a description
  had only `Official alias of X` boilerplate, which the `canonical` field now states structurally.

**The schema gap it exposed.** Six store names are absent from the verb table, which is *silent*
on them rather than negative: `ONINIT`, `while_pressed` and `deck` are structural keywords rather
than verbs, and `browser_filter`, `browser_search`, `none` are names this repo disproved. Index
rows carry `not_in_verb_table: true` rather than promoting or dropping them. The store field this
names — a `kind` meaning "structural keyword, not a verb" — is **not added**; it wants a second
case before being designed, and step 3 of the plan is deliberately left open rather than guessed.

Also fixed in passing: `lint_mappers.py` raised `ValueError` on any path outside the repo, so
linting a scratch file produced a traceback instead of a lint.

#### Not reasons to do this, recorded so they are not resurrected

The trigger for this task was "should the monolith become `verbs/<category>/<verb>.md`?" —
assessed 2026-08-11 and **mostly not worth it**:

- **Per-verb files: no benefit.** The only problem a file tree solves is finding one verb
  without loading 6,300 lines, and `just get-verb` already solves it *better* — it joins five
  artifacts at read time, where a checked-in page can only be a stale copy of that join. 955
  files, nothing gained. Per-verb *pages* belong in the HTML export (Parking Lot): generated at
  build time, never committed.
- **Family files: a small benefit, and not a retrieval one.** The one thing `just` genuinely
  cannot do is narrative — it returns records, not "how the transport verbs relate to each
  other". That kind of writing wants related verbs on one page. Real, but a nice-to-have; the
  frozen [consolidation plan](docs/VDJScript%20Reference%20Consolidation%20Plan.md) already
  chose families over per-verb, so nothing needs redeciding. Do it if the prose becomes hard to
  write, not on a schedule.
- **Dropping the 1,175 catalog rows** is *conditional*, not a driver. They duplicate the store
  and can drift, but they are harmless while nothing reads them and they only become removable
  after step 1. The ~1,000 lines of curated prose stay hand-authored regardless — that is the
  part no artifact can produce.

Ordering note: 10b adds a fifth artifact. Doing this first means it joins one generator; doing
it after means reconciling a Markdown parser against it too. That is a convenience, not the
justification.

Done when `just verb-index` reads no Markdown, `just check` is green, and the step-2
reconciliation is recorded.

### 12. Mine Argument Tails From The Vendor Corpus

Status: Ready

Note: The cheapest source left — static extraction, no live VirtualDJ, no fixtures. Added
2026-09-03.

Measured before queueing: splitting every snippet in
[tests/vdjscript-corpus.json](tests/vdjscript-corpus.json) on `& ? : ( )` and reading the token
after each leading verb yields bare-word tails on **73 verbs**, of which **119 tokens across 50
verbs appear in neither [tests/verb-arg-forms.json](tests/verb-arg-forms.json) nor
[tests/action-catalog.json](tests/action-catalog.json)** — `browser_window folders|songs`,
`eq_mode frequency|stems`, `effect_arm_deck master|single`, `effect_stems vocal`,
`dump quantized|notquantized`, `effect_show_gui transition|audioonlyvisualisation`,
`cue_name active`.

These are attested by construction: Atomix shipped them in Built-In skins and pad pages, so the
parser accepts them. That makes the corpus a **third independent source** alongside the binary's
`keyword_candidates` and the catalog's prose, and it is the best remaining candidate list to feed
`probe_arg_forms.py` — the catalog scored 27 verbs from 97 where the generic lexicon scored 24
from 215, and a source written *for these verbs* is why.

Plan:

1. `--from-corpus` in [tools/probe_arg_forms.py](tools/probe_arg_forms.py), mirroring
   `--from-catalog`: candidates per verb taken from attested tails.
2. Record attestation in its own right. A tail in shipped XML is evidence *without* a probe: the
   probe can only separate a token from nonsense, and it is blind wherever no fixture
   discriminates. Emit `tests/attested-tails.json` with the snippet and file each token came
   from, so a token can be documented as attested even when unprobeable.
3. Then probe them, in fixtures, `--repeat 2`, and merge (the union-merge, so nothing is lost).

**Filter the known non-arguments first**, or the extraction will invent parameters. Already
visible in the sample: `dump while_pressed` is the statement suffix from
[VDJScript Grammar](docs/VDJScript%20Grammar.md), not an argument to `dump`. Same failure class
as the `TION_get_text` symbol fragment and the `"Load saved loop named …"` prose sentence — both
of which shipped before being caught. Exclude `while_pressed`, the unit suffixes, and anything
that is itself a verb name.

**DONE 2026-09-03.** [tools/extract_attested_tails.py](tools/extract_attested_tails.py)
(`just attested-tails`) emits `tests/attested-tails.json`: **154 tokens on 71 verbs, 116 of them
unknown to both other sources**, each carrying the snippet and shipped file it came from.
`probe_arg_forms.py --from-corpus` probes them; 33 verbs confirmed an attested tail locally and
**11 were newly confirmed** — `browser_window songs`, `effect_stems vocal`, `stem_pad vocal`,
`skin_panel audiomixer|defaultwave`, `get_next_karaoke_song artist|singer|title`,
`setting eqmode`, `pad_page btn1`, `cue_display name`, `effect_slider active`,
`get_sample_name active`, `color green`.

**Extended 2026-09-03 — a fourth corpus source and the tails' binary locations.** The app
binary compiles its own menu and toolbar scripts as `__cstring` literals; 83 statements pass
the statement filter in `extract_script_corpus.py`, 80 in no other source, and they add 22
attested tails on 15 verbs (`show_splitpanel effects|info`, `sideview clone`, `font_size big`,
`scratch_dna_option continue`, `browser_options le`) plus a real two-token form,
`sideview 'automix' 'blink'`. Locating every attested tail in the binary split them 52 in the
verb's own method / 67 shared / 66 absent — the shared ones are enumerations matched in
helpers, which is what §13 recovers.

**Shapes, 2026-09-03 — the first verb tried exposed the gap.** `fadeout` has two catalog
examples and two shipped ones, and every command answered "nothing": the catalog extractor's
quote regex rejected examples containing `&` or backticks, the tails extractor drops literals
by design, and the prober then declared the verb "needs no args". Measured: 114 verbs with
vendor examples had tails made only of values and were invisible to every source. Fixed three
ways — the catalog regex admits chains, ternaries and backticks (and bare example lines such
as `color 0.8 0.5 0.25` now enter the corpus); `attested-tails.json` carries `shapes` (410 on
262 verbs, 167 with no keyword tail; classes DUR/PCT/NUM/REL/STR/VAR/BOOL/KW/NAME, expressions reduced to their inner return type (`` `BOOL` ``, `EXP:NUM`), and
the `deck SEL EXP` wrapper unwrapped so inner verbs are shaped) with per-shape return evidence from the vendor's
attribute, the catalog prose and the bare-form sweep; and `verb-arg-forms` points at the
shapes. Confirming a shape live still needs a fixture.

**Shape probing landed 2026-09-06** as [tools/probe_arg_positions.py](tools/probe_arg_positions.py)
(`just probe-arg-positions`, `just verb-arg-positions <name>`), asking a better question than the
planned "`DUR DUR` against `DUR` and nonsense": hold the attested shape and vary ONE position
*within its own class*, so a changed answer means that position is read. Nonsense is still sent,
but only to separate "reads it" from "ignores everything here". Query-only; the baseline is
re-read last so a drifting verb is reported unstable rather than scored as reading everything.

37 verbs probed, 0 unstable, 8 read at least one position and **4 read one beyond the first** — a
class of fact no artifact here carried. The keeper is a pair with identical `NUM NUM` shapes:
`effect_slider_active` reads both slot and index, while **`effect_arm_slider` ignores its slot
position entirely** (slot 1 and slot 2 both return `0.73`, as does nonsense) and reads only the
index. Nothing short of varying the slot on its own would have shown that.
`get_effect_slider_label`, independently confirmed the same day, doubles as the method's
calibration. Full table: the tracker's "Argument Positions: A Question The Other Probers Cannot
Ask".

Still next here: a keyword position can only be varied where the verb has two attested keywords,
so the multi-token shapes that were skipped want either attested tails or the catalog's own
parameter list as a second value source.

### 13. Probe The Shared Enumerations The Binary Serialises

Status: Ready

Note: 2026-09-03 — candidates extracted, fixtures exist, needs `just vdj-up`. **Two groups done
2026-09-06**, with opposite outcomes; the rest of the list below is still open. Full evidence:
the tracker's "Shared Enumerations: The Colour Table Confirmed, The Pad-Page Table Unreachable".

- **`colors`: confirmed, and cheaply.** `color '<name>'` resolves in *query* position — it echoes
  the canonical spelling for a recognized colour and returns `transparent` for anything else — so
  the whole group is classifiable read-only with a free floor. **24 of 26 members echo
  themselves**, 16 of them names no per-verb source knew. Three nonsense controls and a two-word
  control all returned `transparent`; `RED` returned `red`, so matching is case-insensitive.
  `none` and `reset` are **undiscriminated, not disproved**: they return `transparent`, which is
  itself a real member, so this observable cannot separate them from the floor. Group-level
  conclusion recorded: for `color`, the serialised table *is* the accepted vocabulary.
- **`pad_pages`: unreachable through `pad_page`, and this is the more instructive half.**
  `pad_page 'sampler'` and `pad_page 'cueloop'` both returned `true` and the query then reported
  that page as current — which looks like confirmation until the control runs.
  **`pad_page 'qzqzqz'` behaved identically.** The verb takes an arbitrary string and reports it
  back, so the 17 table names are undiscriminated *through this verb*, not unconfirmed by it.
  Confirming them needs an observable reflecting what a page contains, not what it is called.
- Also settled while the colour vocabulary was in hand: the sibling verbs do **not** share the
  resolver. `browsed_file_color` echoes any argument verbatim, nonsense included — it looks like a
  resolver and confirms nothing. `sampler_color` bare returns hex, not a name. `get_browsed_color`
  is stable over three runs but context-dependent and not interpretable in this state.

[tests/binary-vocabularies.json](tests/binary-vocabularies.json) (`just binary-vocab`) holds
21 argument groups recovered as *structures* — pointer tables and switch functions — with
190 members no per-verb source names. The highest-yield leads, each already tied to a verb:

- `settings <page>`: 18 unprobed pages from a 19-entry table (`settings 'audio'` is attested).
- `color` / `get_loaded_song_color` / `cue_color`: 16 unprobed colour names from the 38-entry
  table — `beige`, `marine`, `violet`, `transparent`, `none`, `reset`.
- `effect_arm_deck` / `effect_fxsendreturndeck`: `booth auxin auxout mic2 preview samplerin
  timecode deckfxsend deckfxreturn` from the audio-channel switch.
- `browser_window`: the 17 root-folder names (`itunes`, `rekordbox`, `history`, `crates` …).
- `pad_page`: the 17 table names, several with spaces (`'loop roll'`, `'saved loops'`).
- `stem_pad instrumental`, `get_time cue`, `effect_show_gui` × 14.

Read first (added 2026-09-07): the named `CSettingEnum::unserialize`, `getActionParam` and
`setActionParam` on 18.0.9246 (`unserialize` at `0x10078a142` x86_64; re-resolve with `nm`)
walk the typed candidate values and conversion rules for the `settings` pages and other
enum-typed keys. Associate a default with a key only where the initializer does; a type name
alone is not a schema. Any persistent write in the live confirmation needs round-trip
restoration.

Probe with `probe_arg_forms.py` against nonsense controls in a discriminating fixture (colours
need a coloured track; settings pages need the dialog observable), `--repeat 2`, union-merge.
Record confirmations with `just put-verb`; record a group-level conclusion (the table IS the
vocabulary) in the tracker, since it does not reduce to one verb. Rule reminder: a member that
fails to separate is undiscriminated, not disproved.

The filters earned their place immediately: `dump while_pressed` is correctly gone while
`dump quantized|notquantized` survives.

`just action-catalog --cross-check` now reports a fourth column, `confirmed_by_all_three` — 8
verbs whose tokens are documented by the vendor, written by the vendor, *and* locally
reproduced (`crossfader_curve` cut/full/smooth, `loop_adjust` in/move/out, `is_using`
effect/equalizer/pads/sample, `get_time` remain/total). That is as settled as this project can
make a claim.

### 13b. Fixtures For The Documented-But-Unconfirmed Parameters

Status: Ready

Note: Needs a live instance — the expensive one of this group. Added 2026-09-03. **Three more
verbs closed 2026-09-06, and the premise needs qualifying**: two of the three were not waiting on
a fixture at all. Tracker: "Contextual Parameters: Three Verbs Off The Worklist, One Wall".

- **`get_sample_info`: all three documented fields confirmed** (`group` → `Drums`, `length` →
  `4bt`, `pos` → `00:00.0`), two nonsense controls returning `''`. **The obstacle was the argument
  SHAPE, not the state** — the form is slot-first, `get_sample_info <slot> <field>`, and a
  single-argument probe errors on every token including the real ones, so the sweep read the
  documented fields as indistinguishable from nonsense. The state had been there since
  `sampler_slots_differ` landed. This is exactly the failure task 12 predicted when it measured
  114 verbs whose vendor examples are value-shaped.
- **`get_saved_loop`: `length` and `name` confirmed** against two agreeing controls, on a fixture
  built and torn down (a 32-beat loop saved, then deleted with the deletion verified). `pos` is
  **undiscriminated** — it returns the right value but so do bare and both nonsense tokens, so it
  is the default. `next` is **out of context** rather than refuted: nothing upcoming to report.
- **`get_slip_time`: a wall.** E_FAIL in every form, bare included, with a track loaded,
  `slip_mode` on, playing, and the playhead jumped. Because the *bare* form errors, no token can
  separate, so the three documented units are untested rather than refuted.

**So before building a fixture for an entry, re-read its documented example for the shape.** The
count to work from is `just action-catalog --cross-check` →
`documented_but_not_probe_confirmed`, and it now excludes doc example placeholders, verb-name
self-references and locally refuted tokens.

`just action-catalog --cross-check` lists, under `documented_but_not_probe_confirmed`, the
verbs whose parameters the vendor documents and no local probe has confirmed. They are
overwhelmingly **contextual**, not wrong: `broadcast` direct/podcast/server/video,
`effect_arm_deck` aux/mic/sampler, `automix_editor_movetrack` current/next/previous,
`browser_move` top/bottom. The fixtures in [tools/fixtures.py](tools/fixtures.py) (`just
fixtures`) never build the state in which these would differ, so the probe reads them as
indistinguishable from nonsense and that verdict means nothing.

The meaning is already written down for every one of them, so this is confirmation work, not
discovery: each needs a state, then a re-probe with `--from-catalog --verbs <name>`.

Fixture candidates, cheapest first: `sideview_populated` (automix list, sidelist),
`browser_folder_deep` (a folder tree with a scrollable parent), `sampler_slots_differ` (several
slots loaded with *different* tracks — also settles what the sampler `all` means, still open from
2026-09-02), `effect_armed`, `broadcast_configured` (likely blocked: needs a server).

Each fixture must assert its own preconditions and fail loudly, per the rule the harness already
follows: a probe against an unestablished state is worse than none.

**PARTLY DONE 2026-09-03.** Two fixtures added, both **assert-only** — the shipped state already
satisfies them, so they write nothing and refuse to run if it is absent:

- `sampler_slots_differ` (slots 1-5 hold different samples, 6-8 empty) — settled what the
  sampler `all` means: **the selected slot**, not an aggregate. See
  [VDJScript Verbs](docs/VDJScript%20Verbs.md).
- `sideview_populated` (`file_count sideview` nonzero).

Re-probing all 97 catalog verbs across 8 fixtures added `get_time` cue1/loopin/loopout/
to_lyrics and more `param_cast` types, but the cross-check middle column did not move (81). The
new states simply are not the ones those 81 parameters need.

**It also exposed a drift verb.** In the 8-fixture run `get_time` tripped the undiscerning guard
— with a deck playing its value moves, so it separates from a control by noise, the `get_cpu`
pattern again. Its absolute/remain/total tokens stay recognized because the *catalog documents
them*, not because the probe is trustworthy here.

**Two more fixtures, 2026-09-03 (after the restart).** `effect_armed` (deck 1 loaded, slot 1
active, deck arm engaged — round-trip verified on `effect_arm_deck` before being written into a
fixture) and `browser_populated` (assert-only: it reads whatever the user is already browsing
rather than navigating somewhere it cannot return from). Re-probing all 97 catalog verbs across
**10 fixtures** confirmed `effect_arm_deck` aux/mic/sampler — one of the 81, and exactly the
kind of state-gated parameter the fixture was built for — plus `timecode_mode smart`.

Cross-check: **27 / 80 / 71**, with 9 verbs now confirmed by all three sources. The middle
column has moved only 90 → 80 across three fixture rounds, which is the honest measure of how
state-specific the remainder is.

Still to build: `broadcast_configured` (blocked — needs a server), a karaoke fixture, and an
automix-list fixture. `browser_folder_deep` was deliberately *not* built: navigating the browser
tree has no verified way back, and an assert-only fixture that reads the user's current position
is worth more than a probe that leaves them somewhere else.

The rest of the 80 likely need an observable other than the verb's own value — the
`auto_bpm_transition` lesson. That is a different instrument, not another fixture.

Two merge rules were fixed while doing this, both found by watching totals rather than by a
test: a re-probe must use a **superset** of the artifact's fixtures (a swapped fixture set
produces verdicts that are not comparable), and **separation is positive evidence while failure
to separate is not evidence of absence** — so a token recognized in any run stays recognized,
annotated `not_reproduced_in` when a later run's states could not show it. Taking the newer
verdict had silently deleted four confirmations.

### 14. Run The Corpus As A Parse-Regression Set

Status: Done

Note: Expanded corpus regression shipped in `675addf`.

The 2026-09-05 review verified 1,610 snippets through `just check`. The counts and
results below describe the earlier 2026-09-03 run, not the current corpus. Query the current
artifact/check for current results; this task is not startable work.

Historical setup (2026-09-03): the first check that could falsify a grammar claim rather than
extend one.

Every one of the 1,427 snippets in the corpus is a form the vendor considers valid — 1,131 from
shipped Built-In XML, 269 quoted in the catalog's own descriptions, 41 from the wiki. Send each
through the read-only query channel and any that fail to parse contradicts something this repo
believes about the grammar.

Design constraints, learned the hard way this session:

- **Query only.** Corpus snippets contain `load`, `unload`, `browsed_song color`, sampler and
  broadcast verbs; executing them would rewrite the library. The channel's own return value
  proves nothing either (rule 4) — the observable is whether the parse errors, not what it says.
- **`E_FAIL` is silence, not denial.** A snippet returning `E_FAIL` is not evidence of a parse
  failure; only `E_INVALIDARG`-style structural errors are, and even those need the nonsense
  control treatment before being called a contradiction.
- Snippets naming effects, skins or files this install lacks will fail for environmental
  reasons. Classify those separately or the signal drowns.

**DONE 2026-09-03.** [tools/check_corpus_parses.py](tools/check_corpus_parses.py)
(`just corpus-parses`, gated in `just check`) sends all 1,427 snippets through `/query`:
**1,099 parse and none contradicts a grammar claim.** Outcomes are classified rather than
counted — 152 not-implemented, 97 other-error, 28 `E_FAIL` no-value, 28 surface-gated
(action-position verbs sent to a query surface), 15 pipeline (`& param_*` needs an inbound
value HTTP cannot supply), 1 placeholder, 7 structural.

The seven residual cases turned out to be execute-position semantics — `loop 50%` multiplies
rather than sets, `pitch_range +1` and `sampler_loop ±1` are relative — and each has an
absolute equivalent that answers normally. Written up in
[VDJScript Grammar](docs/VDJScript%20Grammar.md); a relative or multiplying argument is
execute-only, and asking a query for one errors rather than going silent.

**It also falsified something on its first run — my own extractor.** Eight snippets read
`color &apos;red&apos;`: `extract_script_corpus.py` never XML-unescaped attribute values, so
the corpus had been storing escaped entities since it was built an hour earlier. Fixed, and it
is exactly what a regression set is for.

### 15. Two Loose Ends

Status: Done

Note: Both loose ends closed; details below. Added 2026-09-03.

- **`timecode_cd_mode` — CLOSED 2026-09-03.** VirtualDJ restarted at 09:42 and the verb reads
  `no` on all four decks, back to its pre-probe value. So it is **runtime-only state**: settable
  from script, not clearable from script, and not persisted to `settings.xml`. The 2026-09-03
  execute-probe incident is closed with no lasting change to the user's configuration.

  Worth keeping as a documented verb property rather than only an incident: a verb can latch for
  the life of a session. The execute prober's pre-flight round-trip now catches that class
  before probing (it flips once and requires the value to return), and `timecode` is back inside
  the category deny-list that was inert at the time.
- **What the sampler `all` means — DONE 2026-09-03.** It is **the selected slot**, not an
  aggregate: with slot 1 selected `get_sample_name all` reads slot 1's name, after
  `sampler_select 5` it reads slot 5's, and `sampler_loaded all` stays `yes` while
  `sampler_loaded 8` is `no`. Recorded in [VDJScript Verbs](docs/VDJScript%20Verbs.md), along
  with the `sampler_select` quirk found while restoring state — 1-based slot on execute, 0-1
  slider value on query.

## Blocked Or Hardware-Gated

- Controller display helpers: `controllerscreen_deck`, `controller_battery`.
- Gemini display helper: `gemini_waveform_zoomlevel`.
- Phase helpers: `phase_movement`, `phase_position`, `phase_active`.
- Numark V7 helper: `v7_status`.
- Pioneer RZX helpers: `rzx_touch`, `rzx_touch_x`, `rzx_touch_y`.
- DJC-family helpers: `djc_shift`, `djc_button`, `djc_button_popup`, `djc_button_slider`, `djc_button_select`, `djc_panel`.
- Denon platter/display helper: `denon_platter`.

## Parking Lot

- **Crossfader-curve serialization format** (from the 2026-09-06 excavation): named
  `CSettingCrossfaderCustom::serialize`/`unserialize` survive on 18.0.9246. Recover a narrow
  format description only if configuration tooling ever needs it; validate with app-produced
  samples and isolated round trips. Serializer symbols alone establish nothing about delimiters
  or field meaning.
- **Category-index mapping for the historical x86_64 verb tables**: the older extractions carry
  category names but no index mapping, and none was guessed. Resolve only if a compatibility
  question needs per-category history; the current build's mapping is not evidence for them.
- **Plain-group `class` crash hypothesis** (H2): the recorded `<group class="…">` crash may be the
  plain-group construction path applying a template to no object. Test only with a disposable
  instance and a saved configuration, never on the operator's running app.
- **HTML reference export for humans** (requested 2026-07-29, deliberately deferred until the
  contract data exists): generate a static, browsable HTML reference from the verb store +
  verb table + contracts artifact — one page per verb plus category/alias indexes. Generation
  only, from the JSON stores (never hand-written HTML copies, same rule as Markdown); becomes
  worthwhile once task 10 gives the pages real content beyond names.
- `system`: revisit only if an official example, bundled-resource context, or clearly harmless parameter appears.
- Skin `visual type` canaries: **partly overtaken** (2026-08-22). The placeholder half is answered
  for a plugin-panel surface by the runtime-skin loop (task 10a) — starred is required, and works
  in conditions. What is left is the same canary run against a *real deck skin*, to say whether
  the plugin panel and a deck skin share the rule; the fixtures are ready in
  `tests/Skins/runtime-probe/`. Do that with the waveform questions, since both now want the same
  fixture.
