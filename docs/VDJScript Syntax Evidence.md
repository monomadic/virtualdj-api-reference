# VDJScript Syntax Evidence

Local notes on evidence for VDJScript tokenization, parsing, highlighting, and conditional grammar.

Source app: `/Applications/VirtualDJ.app`

Observed on 2026-05-29:

- VirtualDJ app version: `8.5.9307`
- VirtualDJ bundle build: `18.0.9336`
- Main executable SHA-256: `233f36a8d454d0fe90e7bb1c57b9550a4ea8aa3ee0a9f219624c24aa8aaa59f1`

## Purpose

The Button Editor is not only an action catalog. Its script field also performs syntax highlighting and hover-based token separation. That behavior is a separate evidence stream from the bundled language descriptions: it can help document VDJScript grammar, branch boundaries, operator precedence, and query/action token classification.

This file records the current binary anchors and the specific grammar questions to test. Treat this as parser evidence, not as a public API claim until paired with visible UI observation or local behavior tests.

## Button Editor UI Clue

In the Button Editor, a script such as:

```vdjscript
play ? effect_stems vocal on : off
```

is rendered as separate colored spans. The observed split separates at least:

- `play` as the first query/action token.
- `?` and `:` as conditional separators.
- `effect_stems` as the true-branch action token.
- `vocal` as a parameter-like word.
- `on` and `off` as state constants or branch values.

This strongly suggests the editor owns a token/span model, not just a plain text box. It does not yet prove whether the highlighter is driven by the full runtime parser or by a parallel lightweight parser.

### Confirmed: the highlighter is ternary-**aware**, not just token-coloured (2026-07-30)

`Local test` (VirtualDJ 2026 `v2026-m b9482`, Button Editor, screenshot). Typing:

```vdjscript
hot_cue ? get_text "hi" : get_text "no"
```

renders with **branch-role colouring, not per-token-type colouring**:

| Span | Rendering |
| --- | --- |
| `hot_cue` | condition — blue/violet |
| `get_text "hi"` | **true branch — green** |
| `get_text "no"` | **false branch — red** |

The same verb (`get_text`) is coloured differently on either side of the `:`, so the colour
encodes **position in the ternary**, not lexical class. The editor is therefore parsing
structure, not lexing tokens — which upgrades the earlier "owns a token/span model" reading.

Two layers are in play, visible together: **background** carries the branch role (neutral
condition / green true / red false) while **foreground** carries token type — quoted string
literals keep their own colour inside either branch. So the highlighter runs a lexer *and* a
structural parser.

**It does not know the verb set.** Three scripts differing only in head verb — `get_version`,
`zzz_bogus`, `browser_filter` — render identically (`Local test`, 2026-07-30, screenshots). A
ternary built entirely from nonexistent verbs colours perfectly. Autocomplete has the verb list;
the highlighter does not. That makes this a **grammar-mapping instrument, not a linter**, and it
is why `tools/lint_mappers.py` still has a job.

### The editor reports the guard of the statement under the cursor (2026-07-30)

*Scoped 2026-07-30.* This section was first written as "a parse-tree reader". It is narrower
than that: the hint appears **only for statements that carry a guard**. A plain unconditional
chain — `get_text "x" & get_text "x"` — produces no hint line at all, with the cursor in either
statement. So it reports conditional guards, not parse roles in general, and it is silent about
any construct outside a conditional.

`Local test` (Button Editor, screenshot). Below the Action box, a **hint line names the
structural role of the span under the cursor**, in VirtualDJ's own vocabulary. With the cursor
inside `param_equal` in:

```vdjscript
param_equal "`get_text 'A'`" "A" ? get_text "B" : get_text "C"
```

the editor displays:

```
condition: param_equal "`get_text 'A'`" "A"
```

This is qualitatively better than the colouring. Colour shows *that* a structure model exists;
this line shows **what the parser thinks the structure is**, labelled with the parser's own term
(`condition:`), and it delimits the span — here confirming that the whole backticked argument
list belongs to the condition.

**Method**: place the cursor in a construct and read the label; no execution, no side effects,
and the answer is the parser's own account rather than an inference from an observed value. This
is the instrument of choice for every open ternary-binding question below — branch extent,
chained-vs-nested `else if`, and backtick boundaries — because those are exactly the cases the
runtime cannot answer (a query returns only the first statement's value).

**What the hint actually reports: the effective guard condition, not the branch name.**
Moving the cursor through all four statements of

```vdjscript
get_version ? get_text "A" & get_text "B" : get_text "C" & get_text "D"
```

gives (`Local test`, 2026-07-30, four screenshots):

| Cursor in | Hint line |
| --- | --- |
| `get_text "A"` | `condition: get_version` |
| `get_text "B"` | `condition: get_version` |
| `get_text "C"` | `condition: not get_version` |
| `get_text "D"` | `condition: not get_version` |

The editor **negates the condition for the false side** rather than labelling the branch. So the
mental model VirtualDJ itself uses is: *every statement carries a guard, and the hint tells you
that guard.* Any statement's execution condition can be read directly, which is a far more
useful primitive than a branch label — and for nested or chained ternaries it should compose
into a compound guard, making binding directly legible.

**This case also validates the instrument itself.** Both-sides branch binding was already
settled behaviorally over HTTP by variable readback
([VDJScript Grammar](VDJScript%20Grammar.md#conditionals): `a=1 b=1 c=0 d=0` when true,
`a=0 b=0 c=1 d=1` when false). The parse hint reports exactly the same structure. That is the
first direct comparison between the **editor's** parser and the **runtime's** behavior, and they
agree — which partially answers the standing caveat that the two had never been shown to be the
same code. One agreement is not proof they always agree, but it is the first evidence that hint
output can be trusted about the runtime, and it raises the value of the hint for the questions
HTTP *cannot* reach.

**Guards accumulate — which settles chained ternaries.** For

```vdjscript
get_version ? get_text "A" : get_version ? get_text "B" : get_text "C"
```

the hint gives `not get_version & get_version` inside B, and
`not get_version & not get_version` inside C. Each nesting level contributes a term: "past the
previous branch" plus "this ternary's own condition". So `a ? b : c ? d : e` is right-associative
and behaves as a true **else-if ladder** — the form the community most often gets wrong, now
readable rather than inferred. Promoted into
[VDJScript Grammar](VDJScript%20Grammar.md#conditionals).

> **The `&` in a hint is not the `&` of VDJScript.** In the hint it denotes logical
> conjunction; in the language `&` is a *statement separator* and `&&` is boolean AND. Hint text
> is a description of a guard, not a pasteable script — copying `not get_version & get_version`
> into an Action box would mean two statements, not a conjunction.

Worth one more probe when convenient: the test above uses the *same* expression for both
conditions, so the composition is legible but not maximally explicit. Repeating it with two
distinct conditions (say `get_version ? … : get_bpm ? … : …`, expecting
`not get_version & get_bpm`) would remove any residual doubt about which term comes from where.

### Further results from the guard hint (all `Local test`, 2026-07-30)

**Deck/scope wrappers are part of the guard.** `deck 1 get_version ? …` reports
`condition: deck 1 get_version`, negating to `condition: not deck 1 get_version`. Chained with
a second scope, the guards compose with the scope intact:

```vdjscript
deck 1 get_version ? get_text "A" : deck 2 get_version ? get_text "B" : get_text "C"
```

→ A: `deck 1 get_version` · B: `not deck 1 get_version & deck 2 get_version` ·
C: `not deck 1 get_version & not deck 2 get_version`. So a deck wrapper binds into the
condition it precedes, and deck-scoped else-if ladders read exactly as written — useful for
mapper authors, where mis-scoped conditionals are a common bug.

**Backticks are not expanded, and do not terminate a quoted argument.** The guard shows the
backticked text **verbatim**, unresolved:

| Script | Guard (true branch) |
| --- | --- |
| ``get_text "`get_bpm`" ? …`` | ``get_text "`get_bpm`"`` |
| ``param_equal "`get_bpm` X" "Y" ? …`` | ``param_equal "`get_bpm` X" "Y"`` |

In the second, the trailing ` X` stays **inside** the same quoted argument and `"Y"` remains a
separate second argument. So a closing backtick does not end the argument — the quotes do. This
corroborates [Backticks are a surface feature, not a parser
feature](VDJScript%20Grammar.md#backticks-are-a-surface-feature-not-a-parser-feature) and
answers the *backtick boundaries in nested quoting* gap: the parser sees one quoted string and
never interprets its contents.

**Operator-lookalike words in argument position stay arguments.** `set '$a' on ? …` reports
`condition: set '$a' on` — the whole verb-plus-arguments expression is the condition, with `on`
absorbed as `set`'s argument rather than read as a constant. `get_text "on" ? …` likewise reports
`condition: get_text "on"`. Two side notes: a ternary condition may be an *action* verb (`set`),
and the negated forms are `not set '$a' on` / `not get_text "on"`.

**Reproduction note.** The hint is easy to miss: it is low-contrast grey beneath the Action box,
appears only for the construct under the cursor, and is transient. Click precisely inside the
statement and read immediately.

**Not every construct produces a hint — answered 2026-07-30.** `get_text "x" & get_text "x"`
(no conditional) shows no hint line for either statement. Unguarded statements have nothing to
report, which is consistent with the per-statement-guard model and confirms the feature is a
*guard* display rather than a general structural annotation.

Still open: whether any label other than `condition:` exists. Every observation so far —
ternaries, chained ladders, deck scopes, backticked arguments — has used `condition:`.

**Consequence for the chain-ceiling probe.** A bare `&` chain cannot be measured with this
instrument, because unguarded statements are silent. To use the hint on
[the chain ceiling](VDJScript%20Grammar.md#chains-have-a-silent-length-ceiling), put the chain
*inside* a conditional so every statement carries a guard:

```vdjscript
get_version ? get_text "1" & get_text "2" & … & get_text "40" : nothing
```

Then walk the cursor toward the tail and find the first statement that stops reporting
`condition: get_version`. If the hint gives out at the same length the runtime does, the ceiling
is a **parse** limit; if the hint keeps reporting past the runtime's cutoff, it is an
**execution** limit. That distinction is currently unknown.

**Blocked by the UI, though** (`Local test`, 2026-07-30). The hint survives a chain of roughly
55 statements, but once the pasted script fills the Action box the box expands and **the hint
line is no longer displayed at all** — it is pushed out of view rather than reporting anything
different. Since the documented runtime ceiling is ~142-152 `set` statements, the interesting
region is exactly where the instrument goes blind. Also note the condition must be genuinely
boolean-true or the whole chain sits in the untaken branch — use `on ?`, not `get_version ?`
(see [A verb's value and its truth are different
channels](VDJScript%20Grammar.md#a-verbs-value-and-its-truth-are-different-channels)).

**This makes the editor a syntax-validation channel.** A construct can be checked for
*structural acceptance* by typing it and reading the colouring, with no execution and no side
effects — useful for exactly the open questions in *Grammar Questions To Test* below
(branch extent, backtick boundaries, word/operator ambiguity), several of which are hard to
settle over HTTP because a query returns only the first statement's value. Caveat: this shows
what the **highlighter** accepts. Whether the highlighter and the runtime parser are the same
code is still unproven, so a colouring result is a lead that still needs a Tier-1 behavioral
run to become a claim (rule 3).

## Autocomplete is bound to the canonical verb set — 955, not 1,028

`Local test` (VirtualDJ 2026 `v2026-m b9482`, Button Editor and Controllers→Keyboard mapper,
screenshots, 2026-07-30). The Action box completes a typed prefix and filters the Action list.
Two probes settle which list it is bound to:

| Typed | Result | What it proves |
| --- | --- | --- |
| `remote` | completes to **`remote_action`** in both the Button Editor and the mapper | Editor-**hidden** verbs (`flags == 256`) *are* in the autocomplete set, even though they are absent from the browsable Category→Action list |
| `hotc` | **matches nothing.** (`hot` alone matches `hot_cue`; adding the `c` deselects it) | The alias spelling `hotcue` (`flags == 1`) is **not in the set**. `hotc` is a prefix of `hotcue` but not of `hot_cue`, so if the alias were present it would have matched |

That is exactly the shape of the verb table's identity model, arrived at from a completely
different direction:

```
918 canonical (flags 0) + 37 editor-hidden (flags 256) = 955 = distinct verb ids
                                    73 alias spellings (flags 1) = excluded
```

**One autocomplete entry per distinct `id`.** The live UI and the compiled table agree on the
955/73 split, which is independent corroboration of the alias model in
[Undocumented VDJScript Candidates](Undocumented%20VDJScript%20Candidates.md) (Evidence
Standards rule 1g) — the binary says two records share an id; the editor shows one of them.

Matching is ordinary **prefix** matching — which is what makes the `hotc` probe a clean disproof
rather than an inference. `hot` selects `hot_cue`; typing the `c` deselects it, because no verb
in the set begins with `hotc`. The alias `hotcue` would have been the one entry that did.

### Using it as a discovery instrument

Walking the alphabet in this box would enumerate the runtime verb set without touching the
binary, and it is Tier 1 (agent driving the window). Its limits, now measured rather than
assumed: it yields **names only** — no `id`, no alias grouping, no category, no capability — and
it omits the 73 alias spellings. It is best used as what it just did: an independent spot-check
on the table, and the one channel that would catch a runtime-registered verb if such a thing
existed (see [Plugin SDK](Plugin%20SDK.md) — the public SDK has no way to register one).

## Binary Anchors

The arm64 symbol table exposes a cluster around the Button Editor and action parser:

| Symbol area | Why it matters |
| --- | --- |
| `CActionEdit::onCreate`, `CActionEdit::onActionEdit` | Dialog wrapper for editing actions. |
| `DLGActionWizard::setAction`, `DLGActionWizard::onChanged`, `DLGActionWizard::onKey` | Entry points that likely reparse text as the editor changes. |
| `DLGActionWizard::customDraw` | Likely draws the highlighted action text. |
| `DLGActionWizard::STree::clear`, `DLGActionWizard::STree::setColor`, `DLGActionWizard::STree::toString` | Strong parser/highlighter-tree clue; `setColor` is especially relevant to syntax coloring. |
| `DLGActionWizard::getCurrentWord` | Likely maps cursor/hover position to the current token. |
| `DLGActionWizard::xyToPos`, `DLGActionWizard::posToXY`, `DLGActionWizard::posToRealPos`, `DLGActionWizard::realPosToPos` | Position translation between rendered text and source offsets. |
| `DLGActionWizard::onTouchOver`, `DLGActionWizard::onTouchOverLeave`, `DLGActionWizard::updateHint`, `DLGActionWizard::setHelp` | Hover hint and token-help path. |
| `DLGActionWizard::onCategory`, `DLGActionWizard::updateList`, `DLGActionWizard::onList` | Button Editor category/action list path. |
| `CSkinEngine::createAction`, `CMacroEngine::addAction`, `IController::execute` | Runtime action creation/execution pipeline. |
| `SActionParam::serialize`, `SActionParam::unserialize`, `SActionParam::toString`, `SActionParam::toFloat`, `SActionParam::toColor` | Runtime value representation and conversions. |
| `ACTION_*::onExecute`, `ACTION_*::onQuery`, `ACTION_*::onQueryBool`, `ACTION_*::onQueryText`, `ACTION_*::onTooltip` | Per-action implementation capability hints. |

Reproduction command:

```sh
nm -arch arm64 -m /Applications/VirtualDJ.app/Contents/MacOS/VirtualDJ | c++filt | rg "DLGActionWizard|CActionEdit|CSkinEngine::createAction|CMacroEngine::addAction|IController::execute|SActionParam"
```

## Symbol Capability Extractor

Run:

```sh
python3 tools/extract_vdjscript_symbols.py --show-anchors
```

For machine-readable parser/editor anchors:

```sh
python3 tools/extract_vdjscript_symbols.py --anchors-format csv
```

Initial arm64 counts from the installed app:

| Symbol bucket | Count |
| --- | ---: |
| `ACTION_*` implementation classes | 800 |
| Classes with `onExecute` | 461 |
| Classes with `onQuery` | 603 |
| Classes with `onQueryBool` | 46 |
| Classes with `onQueryText` | 89 |
| Classes with `onTooltip` | 79 |
| Parser/editor anchor symbols | 68 |

Structured parser/editor anchor groups from the same run:

| Anchor group | Count | Main evidence |
| --- | ---: | --- |
| `action_param` | 20 | `SActionParam` conversion, serialization, equality, and `isTxt<N>` helpers. |
| `catalog_list` | 4 | Category/action list handlers plus `DLGActionWizard::onChanged()::deckArguments`. |
| `editor_dialog` | 8 | `CActionEdit` wrapper lifecycle and action-edit callback. |
| `hover_help` | 7 | Current-word extraction, touch-over handling, hint update, and help text setters. |
| `render_position` | 6 | Highlight drawing and source/rendered position conversion. |
| `runtime_create_execute` | 6 | Skin action creation, macro action insertion, controller execution. |
| `syntax_tree` | 7 | `DLGActionWizard::STree` plus `vector<DLGActionWizard::SItem*>` storage. |
| `wizard_lifecycle` | 10 | Wizard construction, linking, text setting, key handling, and change handling. |

The helper summarizes `ACTION_*` implementation classes by visible methods. This is not a perfect verb list because aliases, dispatcher-only names, and public spellings may not map one-to-one with implementation class names, but it can identify useful capability buckets:

- action classes with `onExecute`
- query-capable classes with `onQuery`, `onQueryBool`, or `onQueryText`
- text-query classes with `onQueryText`
- tooltip-aware classes with `onTooltip`
- editor/parser anchor symbols around `DLGActionWizard`

## Parser Structure From Symbols

The symbol cluster now looks like a layered parser/editor pipeline, not a single flat autocomplete table:

| Layer | Symbol evidence | Current interpretation |
| --- | --- | --- |
| Dialog shell | `CActionEdit::onCreate`, `CActionEdit::onActionEdit`, `CActionEdit::onClose` | The Button Editor action field is wrapped by a dedicated action-edit dialog. |
| Wizard lifecycle | `DLGActionWizard::setAction`, `DLGActionWizard::onKey`, `DLGActionWizard::onChanged`, `DLGActionWizard::onCallback` | Text entry flows through a dedicated wizard/editor object that can react to each edit. |
| Syntax tree/span model | `DLGActionWizard::STree::clear`, `STree::setColor`, `STree::toString`, `vector<DLGActionWizard::SItem*>::push_back` | The editor appears to build an internal item/tree representation for colored spans. `setColor` is the strongest direct syntax-highlighting clue. |
| Position mapping | `customDraw`, `setPosition`, `posToRealPos`, `realPosToPos`, `posToXY`, `xyToPos` | Highlighted text is drawn with explicit mapping between source offsets and rendered coordinates. This matches the hover/cursor behavior seen in the UI. |
| Hover/help | `getCurrentWord`, `onTouchOver`, `updateHint`, `setHelp`, `onHelp` | The editor has a token-at-position path that can turn the current word/span into help text. |
| Catalog list | `onCategory`, `updateList`, `onList`, `onChanged()::deckArguments` | The visible category/action browser is tied to the same wizard. `deckArguments` suggests special handling for the `deck` wrapper or its autocomplete/help path. |
| Runtime creation | `CSkinEngine::createAction`, `CMacroEngine::addAction`, `IController::execute` | Runtime parsing/execution is separate but adjacent: skins create actions, macros add actions, controllers execute action strings with `SActionParam` values. |
| Value representation | `SActionParam::toString`, `toFloat`, `toColor`, `serialize`, `unserialize`, `operator==`, `isTxt<4ul>` through `isTxt<19ul>` | Runtime parameters are typed/convertible values, with optimized text-comparison helpers for fixed string lengths. This is relevant to constants such as `on`, `off`, named stems, and quoted/unquoted text. |

Important caveat: these symbols prove the existence of parser/highlighter infrastructure, but they do not by themselves prove the complete grammar or precedence table. The next confirmation layer is UI observation for token spans plus harmless runtime tests.

High-value binary handles for the next deeper pass:

| Handle | Address | Mangled name |
| --- | --- | --- |
| `DLGActionWizard::onChanged()` | `0x1006908bc` | `__ZN15DLGActionWizard9onChangedEv` |
| `DLGActionWizard::getCurrentWord(...)` | `0x10068feb8` | `__ZN15DLGActionWizard14getCurrentWordERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEmRmS9_` |
| `DLGActionWizard::customDraw(...)` | `0x1006913a4` | `__ZN15DLGActionWizard10customDrawEiiiiii` |
| `DLGActionWizard::updateList()` | `0x100691a24` | `__ZN15DLGActionWizard10updateListEv` |
| `DLGActionWizard::updateHint()` | `0x1006921e8` | `__ZN15DLGActionWizard10updateHintEv` |
| `DLGActionWizard::STree::toString()` | `0x100692800` | `__ZN15DLGActionWizard5STree8toStringEv` |
| `DLGActionWizard::STree::setColor(unsigned int)` | `0x100692998` | `__ZN15DLGActionWizard5STree8setColorEj` |
| `CSkinEngine::createAction(bool, string const&, int)` | `0x100512c9c` | `__ZN11CSkinEngine12createActionEbRKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEi` |
| `CSkinEngine::createAction(vector<SActionCacheItem*>*, char const*, int)` | `0x100512cf4` | `__ZN11CSkinEngine12createActionEPNSt3__16vectorIP16SActionCacheItemNS0_9allocatorIS3_EEEEPKci` |
| `CMacroEngine::addAction(...)` | `0x1005f19e4` | `__ZN12CMacroEngine9addActionEP7IActionP12SActionParamjj` |
| `IController::execute(...)` | `0x10073c380` | `__ZN11IController7executeERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEiP12SActionParamjP16IControllerInput` |

Use `otool` for targeted Mach-O disassembly:

```sh
otool -arch arm64 -tV -p __ZN15DLGActionWizard10updateListEv /Applications/VirtualDJ.app/Contents/MacOS/VirtualDJ
```

The helper below runs that command for known parser/editor targets and summarizes calls, literals, ASCII immediates, and decoded bitmasks:

```sh
python3 tools/disassemble_vdjscript_parser_targets.py --target getCurrentWord --target updateList --target updateHint --target setColor
```

## Targeted Disassembly Findings

These are instruction-level findings from `otool`; still treat them as parser/editor evidence until paired with UI observations and harmless runtime tests.

| Target | Finding |
| --- | --- |
| `DLGActionWizard::customDraw` | Calls `updateList`, then `updateHint`, then `CDLGText::draw`. This ties parser refresh and hover/help refresh directly to drawing the editor text. |
| `DLGActionWizard::getCurrentWord` | Contains literal `"deck "`, calls `_strncasecmp`, uses delimiter bitmask `& ( : ?`, skips spaces, and scans the resulting word as `[A-Za-z0-9_]`. This is the strongest current evidence for the editor's hover/current-token rule. |
| `DLGActionWizard::updateList` | Clears `STree`, allocates parser/list nodes, measures text, and includes literals `"while_pressed"`, `"deck"`, `"not"`, and `"string_view::substr"`. Its structural delimiter mask is `& ( ) : ?`; it also recognizes string delimiters/end markers `\0`, newline, `"`, `'`, plus a shifted mask for `"`, `'`, and backtick. |
| `DLGActionWizard::updateHint` | Contains literals `"?"`, `" ?"`, `"not "`, `"config"`, and `"condition: "`, and calls `STree::setColor` plus `STree::toString`. This links the tree representation to hover help and conditional-context display. |
| `DLGActionWizard::STree::toString` | Recursively calls itself three times and appends child text, supporting the interpretation that `STree` is a nested expression/tree representation rather than a flat token array. |
| `DLGActionWizard::STree::setColor` | Iterates the tree's item vector, writes the color at item offset `0x10`, and recursively calls `setColor` on three child pointers before following another link. This confirms recursive color propagation through syntax-tree branches. |

Working grammar clues from this pass:

- Hover/current-word extraction treats `&`, `(`, `:`, and `?` as token boundaries, then consumes letters, digits, and `_`.
- The syntax-tree builder treats `&`, `(`, `)`, `:`, and `?` as structural delimiters.
- Quotes and backticks have explicit tokenizer handling in `updateList`; they are not just ordinary word characters.
- `deck` and `not` are special in the editor path, so they deserve focused UI/runtime tests rather than being documented as ordinary verbs/parameters.
- `while_pressed` is checked during tree construction, which suggests it has special parser/highlighter treatment even if runtime behavior is action-specific.

## Grammar Questions To Test

The Button Editor highlighter and hover spans should be used to probe these cases. Five of
the eight were answered on 2026-07-22 over the [HTTP control interface](HTTP%20Control%20Interface.md);
the settled rules are written up in [VDJScript Grammar](VDJScript%20Grammar.md) and the
still-open ones are listed in its *Not yet established* section.

| Question | Test shape | Status |
| --- | --- | --- |
| Conditional branch extent | `get_version ? get_text "A" & get_text "B" : get_text "C" & get_text "D"` | **Answered — and this row was stale.** [VDJScript Grammar](VDJScript%20Grammar.md#conditionals) settled it over HTTP with variable readback (`a=1 b=1 c=0 d=0` / `a=0 b=0 c=1 d=1`). The parse hint **independently corroborates**: A/B report `condition: get_version`, C/D report `condition: not get_version` |
| **Chained ternaries** (community confusion point) | `a ? b : c ? d : e` | **Answered 2026-07-30 (parse hint): a true else-if ladder.** Right-associative, guards accumulate — B reports `not get_version & get_version`, C reports `not get_version & not get_version`. Written up in [VDJScript Grammar](VDJScript%20Grammar.md#conditionals). Still open: whether a 4+-deep chain keeps composing, and whether the runtime agrees (the ladder has not had a behavioral run) |
| Does the editor flag an unknown verb? | `zzz_bogus ? get_text "A" : get_text "B"` vs a real head verb | **Answered 2026-07-30: no.** `get_version`, `zzz_bogus` and `browser_filter` render identically. The highlighter parses shape, not vocabulary — it colours a well-formed ternary built entirely from nonexistent verbs. The editor is a **grammar instrument, not a linter** |
| Conditional associativity | `a ? b ? c : d : e` | **Answered**: standard, `a ? (b ? c : d) : e` |
| Empty false branch behavior | `a ? b :` and `a ? b : nothing` | **Answered**: errors when reached; `nothing` has no query value |
| Query chain vs action chain | `a && b ? c : d` compared with `a & b ? c : d` | **Answered**: `&` separates statements (query returns the first); `&&` is boolean AND that short-circuits destructively on a false left operand |
| Parameter tokenization | `effect_stems vocal on`, `effect_stems 'vocal' on`, `effect_stems "vocal" on` | **Answered**: all three equivalent for single tokens; quotes mandatory once a value contains a space |
| Backtick expression boundaries | ``param_equal "`get_bpm` X" "Y" ? …`` | **Answered 2026-07-30 (parse hint)**: the guard shows the backticked text verbatim and unresolved, the trailing ` X` stays inside the same quoted argument, and `"Y"` remains a separate argument. Quotes delimit arguments; backticks do not |
| Word/operator ambiguity | `set '$a' on ? …`, `get_text "on" ? …` | **Answered 2026-07-30 (parse hint)**: `on` in argument position is absorbed as an argument — the guard is the whole `set '$a' on` expression, not a constant comparison. Still open for a verb whose *parameter name* collides with a constant |
| `&&` — a real operator? | `get_version && get_bpm ? get_text "A" : get_text "B"` vs the same with `&` | **Answered 2026-07-30**: no. Byte-identical guards (`get_bpm`), and identical action-position behaviour under HTTP readback. `&&` only changes which statement's value a *query* reports. Rewritten in [VDJScript Grammar](VDJScript%20Grammar.md#boolean-composition-with-) |
| Deck/scope wrappers | `deck 1 play ? action_a : action_b`, `all_decks play` | **Answered**: a deck wrapper covers a following conditional; out-of-range decks are accepted silently; `all_decks` is action-only and cannot wrap a query |

For each case, record three layers:

1. Button Editor visual token split and hover hint.
2. Runtime behavior in a harmless pad or skin test.
3. Documentation consequence for `docs/VDJScript Verbs.md` or surface-specific docs.

## Current Working Model

The visible ternary form is:

```vdjscript
query ? true_branch : false_branch
```

The true and false branches can themselves be action expressions. The following precedence and interpolation rules were established by a controlled pad-page run of [Reference - Grammar Battery Test.xml](../tests/Pads/Reference%20-%20Grammar%20Battery%20Test.xml) on VirtualDJ `v2026-m b9482` (2026-07-14 entry in [VDJScript Local Test Tracker](VDJScript%20Local%20Test%20Tracker.md)):

- **Trailing `&` chains bind to the false branch.** In `cond ? a : b & c`, the `& c` runs only when the false branch runs. With a true condition the observed state was `a=1 b=0 c=0`; with a false condition it was `a=0 b=1 c=1`. Never place always-run actions after a ternary.
- **Leading `&` chains split off before the ternary parses.** `set 'a' 1 & cond ? b : c` ran the `set` unconditionally and then evaluated the ternary independently (observed `a=1 b=1 c=0` with a true condition). Put unconditional actions first, or put the ternary last in the statement.
- **Nested ternaries associate standard.** `a ? b ? c : d : e` parses as `a ? (b ? c : d) : e`: outer-true/inner-false selected the inner false branch, and outer-false selected the outermost false branch.
- **Backtick-computed arguments are accepted per-verb, not globally.** ``set '$dst' `get_var '$src'` `` works (dst read back 42), but `loop`, `beatjump`, and `phrase_sync` ignored backtick-computed arguments even when the identical literal worked on the same playing deck. The `beatjump` case was tested with a stored `'+4'` string, ruling out the unsigned-argument no-op as the cause. For verbs that reject computed arguments, select literals with a conditional, or use implicit param chaining, which works: `get_var '$src' & param_multiply 2 & set '$dst'` read back 84.

Build-specific side observations from the same run: `beatjump` requires a signed argument (`beatjump +4` jumps, `beatjump 4` does nothing), and string values written by `set` read back blank via `get_var` in pad labels while numeric values display.

`&&` should continue to be treated as a query-composition operator until tests prove broader action-branch semantics. For side-effecting action branches, nested ternaries remain the clearer documented pattern.
