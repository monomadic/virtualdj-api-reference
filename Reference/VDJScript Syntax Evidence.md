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

The helper summarizes `ACTION_*` implementation classes by visible methods. This is not a perfect verb list because aliases, dispatcher-only names, and public spellings may not map one-to-one with implementation class names, but it can identify useful capability buckets:

- action classes with `onExecute`
- query-capable classes with `onQuery`, `onQueryBool`, or `onQueryText`
- text-query classes with `onQueryText`
- tooltip-aware classes with `onTooltip`
- editor/parser anchor symbols around `DLGActionWizard`

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
3. Documentation consequence for `Reference/VDJScript Verbs.md` or surface-specific docs.

## Current Working Model

The visible ternary form is:

```vdjscript
query ? true_branch : false_branch
```

The true and false branches can themselves be action expressions. Nested conditionals are already common in working pad XML, but the exact precedence between `? :`, `&`, and `&&` should be documented from controlled tests rather than inferred from examples alone.

`&&` should continue to be treated as a query-composition operator until tests prove broader action-branch semantics. For side-effecting action branches, nested ternaries remain the clearer documented pattern.
