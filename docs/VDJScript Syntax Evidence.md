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

The Button Editor highlighter and hover spans should be used to probe these cases:

| Question | Test shape |
| --- | --- |
| Conditional branch extent | `play ? action_a & action_b : action_c & action_d` |
| Conditional associativity | `a ? b ? c : d : e` |
| Empty false branch behavior | `a ? b :` and `a ? b : nothing` |
| Query chain vs action chain | `a && b ? c : d` compared with `a & b ? c : d` |
| Parameter tokenization | `effect_stems vocal on`, `effect_stems 'vocal' on`, `effect_stems "vocal" on` |
| Backtick expression boundaries | ``param_equal "`get_text 'x'`" "x" ? on : off`` |
| Word/operator ambiguity | verbs or parameters named near constants such as `on`, `off`, `true`, `false`, `nothing` |
| Deck/scope wrappers | `deck 1 play ? action_a : action_b`, `all_decks play` |

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
