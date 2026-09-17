# History

Completed tasks, moved here from [TASKS.md](TASKS.md) when they landed, plus the dated
progress log of open tasks whose narrative outgrew a `Note:`. Each completed block keeps its
`### <id>. <title>` heading and `Status: Done` line so identifiers stay unique across both files;
`just check` enforces that and that nothing here is anything but `Done`, and that nothing
`Done` remains in `TASKS.md`. Blocks are the record of what was established and where it was
recorded; they are not startable and `just next-task` never reads this file.

## Accepted next sequence (2026-09-05 review)

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
- **[tools/task_queue.py](tools/task_queue.py)** as the single parser behind `just next-task`,
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

## Ready Tasks

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

Status: Done

Note: Custom device-definition loading and mapper firing completed 2026-09-12 on build
18.0.9598 using paired virtual CoreMIDI ports in the existing `SIMPLE_MIDI_0_0` context.
The app displayed the authored device description; named note/CC controls fired, with
wrong-address/channel controls and independent live variable-window readback.
[Fixture, exact bytes, results and cleanup](tests/controllers/README.md).

The archive reader also recovers every original XML member from bundled `controllers.dat`,
including definitions, factory mappings and audio presets. The earlier assumption that
the compiled definition layer was opaque is corrected in
[Mapper XML](docs/Mapper%20XML.md) and
[Compiled Controller Definitions](docs/Compiled%20Controller%20Definitions.md).
`just controllers` queries the generated inventory; `just controllers-extract` emits XML.
Extraction is Tier 2; the live fixture validates only its tested MIDI behavior.

The earlier physical DDJ-GRV6 mapper-firing result remains in the tracker. The historical
`browser_filter`/`browser_search`/`none` naming questions are covered by the verb table and
existing disproof records; they are not prerequisites for this now-completed definition test.

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

### 10c. Make The Contract View Say What It Can Vouch For

Status: Done

Note: Added 2026-09-11 from a two-round review of task 10. The instruments exist; what is
missing is a per-verb view that answers *what can I rely on, within what scope, and what is
still open* — and closure rules in `just coverage` that do not claim more than their test
established. Do this before collecting more evidence: it is offline, and it is the
stopping-point and next-test that every later batch will be recorded against. Do **not**
add a reporting command or a Markdown document; extend `just verb` and `just coverage`.

Landed with the review (2026-09-11), so not on the list below:

- `probe-arg-forms` / `probe-execute-forms` no longer shell-redirect into the artifact. The
  tools take `--out FILE` and write atomically only on a real run; `--dry-run` used to
  truncate `tests/verb-arg-forms.json` to zero bytes and `--merge` read it after the shell
  had already emptied it.
- `just verb` prints the execute-position row it was already loading (verdict, recognized
  tails, how many tails the readback could not separate from nonsense, or why it was
  skipped).
- H4 flipped to `Ready`; 10b's opening line no longer says the sweep is unrun.

**Landed 2026-09-12 (items 1-4 below):** `assess()` in `tools/coverage_report.py` is the one
per-verb assessment and `just verb` renders it as a `Contract:` block; `CLOSED` is `settled`
only, `no_known_candidates` replaces the old closing label, execute reads the row's verdict
(`partial` / `undiscriminated` / `no_observable`), and a verb with no capability row is
`unknown` and counted open. A state-limited live result that had lived only in the tracker
(`get_time_hour elapsed/remain`, `0` on a 2:26 track) now reaches the assessment through the
catalog tool's `LOCAL_UNDISCRIMINATED` table and the `documented_but_undiscriminated_here`
cross-check bucket, so `just verb get_time_hour` says *undiscriminated* and names the
long-track fixture rather than *never probed*. Coverage after the change reads lower on
arguments and execute; that is the labels telling the truth, not lost evidence.

Review follow-up (2026-09-12): regression tests now gate the shared assessment.
Failed or unstable position captures stay open; an unmeasured shape is not closed by
recognized keywords, and query confirmations cannot close execute evidence. Known-token
coverage is labelled `vocabulary_covered`, not a full argument contract. Aborted execute
runs preserve the previous output and save partial results separately with a failing exit.
The view still cannot supply missing build stamps or infer complete value/overload coverage
from legacy captures; those need explicit observations in later batches. Next is 10d,
which doubles as the validation run.

Follow-up correction (2026-09-12): the blanket `vocabulary_covered` residual above was
too strong and is superseded. Arguments close when all known obligations are resolved;
remaining obligations must name a catalog value/multiple-argument form, attested shape,
unresolved token or unaccounted binary argument-demand lead. The BPM-transition artifact
is joined directly as execute-with-independent-BPM-readback evidence, so a toggle-only
capture's nondiscrimination cannot reopen its confirmed landing-BPM forms. Capture-time
build provenance is part of 10d below, not a separate task.

**Follow-up 2026-09-12, the `evidence_in_prose` bucket.** It held 37 verbs and two kinds of
thing. Eighteen were behaviour-only prose (`deck_has_error stayed off`) that said nothing about
arguments; the assessment now asks whether the evidence names a form or the argument before
using the label, and those read `unprobed` with the note that behaviour evidence exists. Nine
were the effect-introspection verbs whose NAME-form result had a real artifact all along —
`tests/fx-introspection-dump.json` reads every installed effect by name — so the dump is joined
directly through the sweep's own `NAME_FORM_VERBS` declaration, the same way the BPM-transition
capture is, and those verbs close with the dump's provenance (product version only; it predates
build stamping, and the claim says so). What is left in the bucket is genuinely prose-only:
`get_date`'s strftime value form, `get_effect_slider_name`'s plugin-channel result, the two
`get_video*_name` verbs whose argument is *ignored* (a negative finding), `is_releasefx`'s
undiscriminated slot/name forms, the grammar wrappers `deck` / `all_decks` / `nothing`, and
`browser_colorfilter_edit`'s E_NOTIMPL. Locate and structure each existing observation first,
including the plugin capture for `get_effect_slider_name`. Run a new probe (for example,
a `get_date` position probe) only if the recorded evidence is insufficient. Check the current
count with `just coverage`; do not copy it here.

Review correction: the FX join now checks each verb's own result field, including the
conditional slider/button rows, before claiming a measured form. It excludes error and
missing results, retains the legitimate blank skip-length label, and reports a concrete
effect/index/value. Legacy count zero is ambiguous because the sweep converted errors to
zero; positive count measurements support that form. The prose filter is only a routing
heuristic: a miss means no explicit argument reference was detected, not "never probed".

Checklist as landed, each line with the command that proved it:

1. **One per-verb assessment, shared.** `tools/coverage_report.py` already builds a per-verb
   dictionary (dimensions, recognized/unresolved tails, positions probed). Lift it into a
   function `just verb` imports, so the two commands cannot drift. Proof: no second copy of
   the closure logic in `tools/verb_summary.py`.
2. **Loosen three closure rules** in `coverage_report.py`, in the same change:
   - `argument_less` fires on `probed and not candidates`, but `probed` is also true for a
     verb that only appears in the positions or execute artifact. Rename to
     `no_known_candidates`, require an actual tail-prober row, and drop it from `CLOSED`.
     Exhaustive absence is not claimed.
   - `execute` is `settled` on row presence. Read the row: `has-execute-tokens` with the
     tails it recognized is settled *for those tails*; `tail-ignored-in-execute` and
     `skipped` are open with the reason carried. `auto_bpm_transition` is the type case —
     its toggle readback cannot see a destination-BPM argument, and the row says so.
   - A verb with no contract row gets `queries`/`executes` false and both dimensions `n/a`.
     Make that `unknown` so missing capability data cannot shrink the denominator.
   Proof: `just coverage` shows the new labels, `just check` passes, and no sentence in this
   file or the coverage audit quotes the old label (`rg argument_less`).
3. **A contract block at the top of `just verb`**, rendered from the shared assessment:
   `Contract: settled | partial | open`, then per dimension one line each — what was
   observed, on which channel and build, and the smallest test that would close what is
   open. Every unresolved item carries one of five reasons: *not measured* (`unswept`,
   `unprobed`), *measured but the observable did not discriminate* (`untyped`,
   `tail-ignored-in-execute`), *state or surface unavailable* (`blocked`), *conflicting
   observations* (the disputed list), *evidence only in prose* (`evidence_in_prose`). These
   are the existing labels; the change is the unit, from per-dimension to per-form claim.
   Proof: `just verb crossfader_curve` reads as partial — bare float over HTTP, six names
   settled by HRESULT on the plugin, no execute evidence — and `just verb get_time_hour`
   names the long-track fixture as its next test.
4. **Write task 10's completion criterion as one sentence**, in task 10's note: *every
   verb either has an evidence-backed contract for the stated build and surfaces or a named
   open item with one of the five reasons above; `just coverage --frontier` is the test.*
   "Every undocumented overload found" is not finite and is not the criterion.

Done when the four proofs hold and `just check` passes — they did on 2026-09-12. Then 10d.

### 10d. Long-Track Time Fixture: `get_time_hour` And Its Neighbours

Status: Done

Note: Completed 2026-09-12 on live build 9598 over HTTP. `tests/long-time-forms.json`
records independently established runs, reversed form order, phase readbacks and verified
restoration. `just long-time-forms get_time_hour` reports the result; `just verb get_time_hour`
now closes return type, arguments and behavior using this stamped capture. `elapsed` is
accounted for as the documented elapsed fallback, not a token separated from nonsense.
`get_time_sign` remains undiscriminated in positive-time states. The final fixture uses the
exact midpoint 3750s and fractional position 4207.125s; scaling get_position before HTTP
serialization provides the needed precision. A focused runner preserves phase controls and
restoration rather than merging into the generic prober's incompatible fixture set.

Original plan, added 2026-09-11. The first live batch after 10c, chosen because the expected
differences are already worked out and the state is cheap to manufacture. The recipe is in
10b's note ("`get_time_hour` wants a track longer than an hour"): generated 2h05m track,
playhead at 1h10m so `elapsed`/`remain`/`total` read 1/0/2, read once with `display_time`
on `elapsed` and once on `remain`, then place the playhead where pitched and unpitched
remaining time straddle an hour boundary (about 3,700 s in at +12%) to separate `absolute`.
Do not restate the recipe here; extend `tools/fixtures.py` with the state and run
`tools/probe_arg_forms.py --verbs … --fixtures <new state>` against every time reader that
the state can discriminate in one session — the `get_time*` family and `display_time`
readback, batched, not one question per round. Record per-verb conclusions with
`just put-verb … confidence=local_test evidence="… build …, HTTP"`, the fixture and any
non-discriminating readings in the tracker, and check the artifact in with its stamp. This
run doubles as the validation of 10c's view: after it, `just verb get_time_hour` must show
the dimension closed with the observation, not `Untested`.

Prerequisite: `just vdj-up` (reachable on 2026-09-11) and ffmpeg for the generated track.

Capture checklist: both argument and execute probers read `get_build` from the running
instance before fixture writes, and include that value, query, HTTP channel and UTC time
in the new capture's summary and observations. Do not copy the installed binary's stamp or
apply a new stamp to legacy rows during a merge. Check `just verb`'s per-claim provenance
after recording 10d; older unstamped observations must remain explicitly unknown.

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

## Progress log for open tasks

#### H4 progress log

Progress 2026-09-17 (generic evaluator caller): retained the direct-caller scan and
bounded bodies in `runtime-parser-branch-routes.json`. A verified b9246
`ACTION_setting::onQuery` call supplied the read-only `parser_setting_eval` fixture
on build 9598. Computed boolean comparisons and the outer-quoted missing-final-
backtick forms discriminated. Computed numeric one and text on failed their true
predictions; literal/type controls retained and explained the exact consumer
comparison without generalizing to other settings. No settings were changed.
`getFloatParamEval` caller bodies are captured, but its live fixture is still open.

Progress 2026-09-17 (backtick evidence routing): split the broad backtick family into
exact consumer/case links. The existing constant, get_text and param_add results
follow distinct captured readers; they no longer stand in for generic getParamEval
or getFloatParamEval coverage. The audit validates recorded call edges against the
manifest and hashed assembly and rejects unknown selected case IDs. No live result
or grammar prediction was changed by this correction.

Progress 2026-09-17 (unmatched-quote chains): froze and ran the
`parser_constants` suite in `tests/runtime-grammar-unmatched-quote-cases.json` on
build 9598. Unmatched opening quotes and opposite closers preserved the numeric
prefix instead of applying the following addition; a later matching closer allowed
the outer addition. Both quote styles and numeric baselines matched their frozen
predictions and separated from their controls. The audit links the capture without
claiming internal cursor behavior or universal consumer fallback.

Progress 2026-09-17 (empty-quote consumer): the frozen `parser_constants` suite
`tests/runtime-grammar-quote-consumer-cases.json` ran through the existing argument
prober on build 9598. Single/double empty operands and both marker/value baselines
matched the predictions. Explicit omission contrasts distinguish the positional
cases; those cases still match unequal-string nonsense controls and retain that
label. The quoted-argument audit links the new capture without claiming a universal
empty-argument rule or closing unmatched-quote behavior.
The same-length follow-up also held and separated from both nonsense-value controls:
equal nonempty triples and an empty last operand selected the equal result, unlike
an empty first or second operand. This tests the argument-count alternative directly.

Progress 2026-09-17 (editor span calibration): aborted before candidate tests after
a cropped-dialog coordinate click reached a cue pad behind the editor and started
deck 1. The safety pause was independently verified; exact position restoration
was impossible without a pre-click baseline. The failed calibration is retained in
`tests/runtime-grammar-editor-spans-calibration-aborted-9598.json`; no span or guard
finding was recorded. Further coordinate-based editor tests require a verified
targeting method that preserves the active dialog.

Moved from the H4 task block on 2026-09-16; the task itself stays in [TASKS.md](TASKS.md).

Progress 2026-09-17: repeated the frozen `parser_editor_help` predictions on build
9598 with forward/reverse UI screenshots saved under `tests/`, plus original and
reopened-restoration images and a fresh paired HTTP capture. Candidate predictions
held again; both nonsense controls again displayed `zoom` help, preserving the
failed no-help prediction. The new capture is separate from the historical run
whose images remain unrecoverable. `runtime_grammar_editor.py --http … --ui …`
selects a capture pair and validates saved screenshot paths and hashes. Token spans,
guard hints, and the independently established remote-mode fixture remain open.

Progress 2026-09-12: bounded parser/editor capture and exact-script HTTP candidate suites landed; see [Runtime Argument Grammar Tests](docs/Runtime%20Argument%20Grammar%20Tests.md). `just runtime-grammar` reports the completed build-9598 confirmation capture. H4 remains open: factory/consumer coverage is not exhaustive, live editor comparison has only a visual spot check, and the interrupted deck-context case has unproven exit causation. The continuation adds guarded zoom/beatlock/all-deck execution fixtures, selected-deck query comparisons, untrimmed output tests, restoration journals and a regenerable static frontier. Inspect each capture through `just runtime-grammar --artifact <path>`; the report distinguishes complete and interrupted runs, and derives a `separation` field so a prediction that held against a blank result is not mistaken for a discriminating one. The rules that survived two suites and two baselines were promoted into [VDJScript Grammar](docs/VDJScript%20Grammar.md) on 2026-09-12 (keyword quoting, unit-suffix case/adjacency, comma decimals, signed-vs-unsigned numbers, the malformed-number reset, backtick inertness on execute), with `local_test` store records for `zoom` and `beatlock`. Single-capture and editor-side candidates stay unpromoted.

Progress 2026-09-12 (later): the asymmetric-scope item is half closed. `parser_master_scope`
(`just runtime-grammar-master`) pins selection and master to different decks, which the earlier
suites never did, and the capture settles that **`deck master` and `deck active` both track the
master deck while an unwrapped verb and `deck default` track the selection** — promoted into
[VDJScript Grammar](docs/VDJScript%20Grammar.md#which-deck-a-target-resolves-to-2026-09-12) with
`local_test` store records for `get_deck`, `masterdeck` and `masterdeck_auto`. It also found
`playing` and `mixer1`-`mixer4` to be recognized targets the wiki does not list, with `mixerN`
resolving to a deck that is not N (cause untested, recorded as an observation only). That
stopped fixture left asymmetric playback untested; the 2026-09-16 playing-scope result below
now supplies that comparison. Button press/release lifetime is now **done** via the mapper surface: a virtual CoreMIDI
button read over HTTP between note-on and note-off settles that a button action runs on press
only, that `while_pressed` saves and RESTORES the prior value rather than clearing, and that it
binds its own statement rather than the chain. See
[VDJScript Grammar](docs/VDJScript%20Grammar.md#button-lifetime-what-press-and-release-actually-run-2026-09-14).

Progress 2026-09-13: the static frontier is closed (`just frontier-closure`, gated in
`just check`). All 30 queued indirect sites resolve to virtual dispatch (26, of which 18 are
refcount releases), `_actionFactory` calls (3) or a disassembly artifact (1) — **no argument
consumers**. `_actionFactory` is indexed by verb id, proven by two fixed-entry calls that
store the same number at object+0xc. The structural finding: `IAction::create` finishes the
argument loop into `vector<SActionParam>` *before* calling the factory, so arguments are lexed
centrally and only then dispatched per verb. The static route to argument grammar therefore
ends here; what remains is per-verb behavior inside the constructed action. Variable scope is
also settled, including `@` persistence across a real restart. The paired editor-help
pass on 2026-09-16 is captured by `just runtime-grammar-editor`: candidate HTTP/help
predictions held, but the frozen no-help prediction for two unknown-head controls
failed (both showed `zoom` help). This is appearance evidence only; matching
editor token spans or guard hints remain outstanding. The 2026-09-16
boundary-placement suites now isolate whitespace position from operator adjacency, retain
the failed skip-whitespace predictions, and confirm the narrower original-value result
with changed values and quoted forms; inspect the boundary captures through `just runtime-grammar`. The asymmetric
playback gap is also covered: `--grammar-playing` uses verified digital silence on initially
empty decks 3/4, preserves loaded decks 1/2, swaps the sole playing deck against a pinned
master, and verifies restoration. The completed build-9598 capture separated `active`/`master`
from `playing` and `default`; the initial selection-changing calibration is retained as
incomplete. Multiple-playing, automatic-master transitions and the mixer permutation remain
outside that fixture.

Hazard 2026-09-12 (superseded, kept for the reasoning): the reported VirtualDJ "crashes" were
a minimized window — live process, live HTTP, no window, cmd-tab unable to restore it. `/query`
is inert; `/execute minimize` is what does it, and every skin has a minimize button. See
[Runtime Argument Grammar Tests](docs/Runtime%20Argument%20Grammar%20Tests.md). The original
note read: These exits
leave **no crash report**, so a clean artifact directory is not evidence a run was safe; the one
recorded instance had `deck master constant 37` pending right after `deck sandbox constant 37`.
The shared factor with the asymmetric-master run is unusual deck-wrapper tokens (`sandbox`,
`playing`, `mixer1`-`mixer4`). Do not probe deck targets on an instance in use, and do not treat
one clean completion as clearance — see the hazard section in
[Runtime Argument Grammar Tests](docs/Runtime%20Argument%20Grammar%20Tests.md).

### H4 floating evaluator progress (2026-09-17)

Recovered and hashed the b9246 Pioneer display query entry route to the captured
floating-evaluator consumer. Added lossless binary HTTP comparisons to the existing
argument prober, a read-only empty-deck fixture, pre-candidate literal calibration,
and frozen questions. Two independent build 18.0.9598 captures each recorded 10 held
predictions and one failed computed-text prediction; a held leading-space result
matched controls and remains null evidence. Preserved both captures and joined
their exact cases to the branch audit. This does not close H4: editor token spans,
remote-mode establishment/restoration, reachability and final branch reconciliation
remain open. Details: `docs/Runtime Argument Grammar Tests.md`.

### H4 floating conversion follow-up (2026-09-17)

Two independent build 18.0.9598 read-only captures each recorded 13 held and two
failed predictions against frozen display-frame oracles. Direct numeric/unit forms,
computed beats, and longer expressions separated from controls. Zero-frame cases
matched controls. Chained constant-prefix predictions failed with ASCII constants,
so they do not establish the inherited-parameter path. Original expectations and
both captures are retained; see the Runtime Argument Grammar Tests follow-up.

### H4 evaluator branch classification (2026-09-17)

The structured audit now partitions the conditional jumps of the two captured b9246
evaluator bodies into grammar questions, caller context, cache lifecycle, string
storage, ownership and caller-interface groups. It checks exact assembly-derived
membership and retains a question/limit per group. This narrows future fixture work
without claiming live branch coverage or whole-parser completeness; cache lifecycle,
incoming parameters and nonzero relative input remain explicit evidence limits.

### H4 arithmetic reader comparisons (2026-09-17)

Both operand positions and two asymmetric constant pairs were tested in the existing
read-only prober. Two build 18.0.9598 runs each recorded 36 held predictions and eight
failures, with 12 held cases matching controls. Raw quoted actions and computed beats
produced sums; direct beats returned error:1; computed numeric text yielded second-
then-first concatenation. Trailing-backtick-only predictions failed. Frozen suites,
both captures and exact consumer/conversion call edges are preserved and audit-linked.

### H4 text interpolation comparisons (2026-09-17)

Added sentinel-controlled get_text boundary, escape and formatting questions to the
existing read-only prober. Two build 18.0.9598 captures each recorded 20 held and two
failed predictions; three held cases matched controls. Fractional and beat formatting
predictions failed with exact outputs retained. The audit links these observations
to the distinct interpolation route and excludes outer-token escape, internal type,
skin-cache and universal-formatting claims. No live state writes were needed.

### H4 unmapped-symbol triage (2026-09-17)

Reviewed the captured b9246 symbols lacking primary branch-family mappings and recorded
dispositions, representative assembly anchors and next actions in the existing obligation
checklist. `just runtime-grammar --triage` exposes this focused view; totals come from
`disposition_counts`, with unreviewed additions visible in `symbols_without_triage`.
Priorities are optional-cache boolean evaluation, incoming-parameter selection and the
distinct typed/float pair evaluators. Existing family gaps remain visible and no live
coverage was promoted. Anchor/duplicate/category regressions and the runtime grammar
checks passed. The full `just check` stopped at the unchanged binary-vocabulary artifact's
re-extraction mismatch against installed build 18.0.9628; historical data was not rewritten.

### H4 boolean cache consumer follow-up (2026-09-17)

Extended the existing historical caller scan to `getBoolParam`, identifying the
selected-slot and named-effect `effect_active` routes as cache-supplying leads on
b9246. Reproduced the bounded assembly capture and added checked argument-setup
classification without claiming indirect-call completeness or live cache reuse.

Extended the reversible-action runner with the prepared `parser_effect_boolean`
Phaser fixture on HTTP build 18.0.9628. Initial and independent confirmation captures
preserve predictions, off/on baseline readbacks, controls, journals and restorations.
The confirmation adds shape-matched quoted-text/unclosed-expression controls and
opposite-valued forms: their null results prevent interpreting selected-slot activation
or malformed-input toggling as expression evaluation. Paired-backtick boolean/integer
cases separate from controls. Exact results are joined by `boolean-cache-consumer` in
`just runtime-grammar --audit`, with per-verb evidence available through
`just verb effect_active`. Cache reuse and native type/branch coverage remain open;
the unmapped-symbol triage now starts with incoming-parameter selection.

Runtime-grammar, capture, restoration-guard and reference-status checks passed.
Full `just check` again stopped at the unchanged historical binary-vocabulary
artifact's mismatch against installed build 18.0.9628; no historical binary data
was re-anchored as part of this consumer test.
