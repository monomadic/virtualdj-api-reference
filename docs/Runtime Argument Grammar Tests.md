# Runtime argument grammar: H4 tests

This is a candidate specification expressed as executable predictions, **not a grammar
reference**. Binary observations remain Tier 2. A live verdict establishes only the exact
HTTP result in its named fixture, on the recorded build. It does not establish universal
argument acceptance, action behavior, editor acceptance, or equivalence between builds.

The common parser has been captured and its main lexical branches exercised. This is **not
an exhaustive recovery of every reachable argument consumer**. The unresolved call graph
and the remaining discriminating fixtures are explicit below; H4 remains open.

## Reproduce and inspect

```sh
pkgutil --expand-full ~/Downloads/install_virtualdj_2026_b9246_mac.pkg /tmp/vdj-h4-9246
python3 tools/extract_runtime_parser.py \
  --app /tmp/vdj-h4-9246/vdj.pkg/Payload/VirtualDJ.app \
  --package ~/Downloads/install_virtualdj_2026_b9246_mac.pkg \
  --output tests/runtime-parser-9246
python3 tools/runtime_parser_frontier.py \
  --binary /tmp/vdj-h4-9246/vdj.pkg/Payload/VirtualDJ.app/Contents/MacOS/VirtualDJ
just runtime-grammar
just runtime-grammar --group delimiters
just runtime-grammar --get backtick-numeric-consumer
just runtime-grammar --artifact tests/runtime-grammar-followup-9598.json
just runtime-grammar --artifact tests/runtime-grammar-actions-9598.json
just runtime-grammar --artifact tests/runtime-grammar-scopes-9598.json
just runtime-grammar --artifact tests/runtime-grammar-action-default-9598.json
just runtime-grammar --artifact tests/runtime-grammar-whitespace-9598.json
just runtime-parser-frontier
just check-runtime-grammar
```

Expansion requires a destination that does not already exist; it does not install or launch
the historical app. The capture reads the x86_64 slice of bundle **18.0.9246** (app
**8.5.8769**). Its [manifest](../tests/runtime-parser-9246/manifest.json) records installer,
executable and assembly hashes, fresh `nm` symbol resolution, exact `LC_FUNCTION_STARTS`
intervals, direct calls, unresolved indirect calls, and unexpanded direct targets.
`IAction::create(char const*, char const**, int)` resolves to
`[0x100596f1c, 0x1005984e0)` in that stamped capture.

The [initial suite](../tests/runtime-grammar-cases.json),
[confirmation suite](../tests/runtime-grammar-confirmation-cases.json), and
[focused follow-up suite](../tests/runtime-grammar-followup-cases.json) retain their own
predictions. Each case contains an exact script, candidate expectation, independent
contrasting script and expectation, unrelated nonsense controls, named fixture and binary
sites. `prior_case` distinguishes a revised prediction from its original; failed predictions
are not overwritten in the initial suite.

```sh
just vdj-up
just probe-arg-forms --grammar-cases tests/runtime-grammar-confirmation-cases.json \
  --repeat 2 --rounds 2 --out /tmp/runtime-grammar-new-run.json
just runtime-grammar --artifact /tmp/runtime-grammar-new-run.json --group numbers
```

The existing token-list sweep cannot represent delimiter bytes or prefixes; `--grammar-cases`
adds exact-script comparisons to the same prober. It uses only `/query`.
The original and confirmation captures used the shared channel's whitespace-trimmed
response strings. They cannot establish preservation of leading/trailing output whitespace.
New exact-script runs retain the raw decoded HTTP body; the separate
[whitespace suite](../tests/runtime-grammar-whitespace-cases.json) tests that boundary,
and `summary.response_normalization` records the method. The named
`parser_constants` fixture asserts distinct constant values and deck identities, performs no
setup mutations, and records loaded/playing/default-deck context. Context-dependent follow-up
cases additionally require their contrasting sampler/effect outputs to match; a changed bank
or effect setting makes those cases inconclusive rather than evidence against the parser.
Hardware and account state were not inspected. The live process architecture was not measured.

## Stateful fixtures

The action and selected-scope suites also run through `tools/probe_arg_forms.py`:

```sh
just probe-arg-forms --grammar-actions tests/runtime-grammar-action-cases.json \
  --repeat 2 --rounds 2 --out /tmp/runtime-grammar-actions.json
just probe-arg-forms --grammar-actions tests/runtime-grammar-action-fallback-cases.json \
  --repeat 2 --rounds 2 --out /tmp/runtime-grammar-fallback.json
just probe-arg-forms --grammar-scopes tests/runtime-grammar-scope-cases.json \
  --repeat 2 --rounds 2 --out /tmp/runtime-grammar-scopes.json
```

These modes have their own named fixture definitions, shown by adding `--check` to the
commands above. They require a live instance with four unloaded, stopped decks and save
readbacks before any mutation:

- `parser_zoom_levels` compares zoom baselines `0.25` and `0.65`.
- `parser_beatlock_levels` compares deck 1 beatlock off and on.
- `parser_all_decks_asymmetric` starts decks 1–4 off/on/off/on, then on/off/on/off.
- `parser_selected_scope` selects deck 1, then deck 2, for query-only selector comparisons.

The allowlist permits zoom/beatlock forms, or literal `deck N select` setup/restoration in
the scope mode. The runners verify absolute-setter round trips before candidates, read
state independently of execute responses, and restore the original state after every
action sample. Read-only scope queries share a selected-deck baseline; that baseline is
checked before each query and the original state is restored after each batch. Guard
readbacks include selection, PFL, master assignment, automatic master mode,
and each deck's loaded/playing state. Scope restoration relies on selecting the original
deck and checks PFL afterward; it never guesses a PFL correction.

Mutation requests are sent once, including after a lost response. A pending-write journal
is saved before each mutation; successful responses and restoration outcomes are saved
immediately. A restoration failure aborts the run. Shared controls are measured once per
fixture per pass, with two independent passes and repeated readbacks; cases retain the
actual repeated observations. The checker recomputes verdicts, checks suite and assembly
hashes, verifies binary-site bounds and validates restoration records.

The initial action attempt timed out waiting for a restore response. A fresh read found
zoom at `0.25`, followed by absolute restoration to the recorded `0.31`; all resource and
guard readbacks then matched the initial snapshot. That interrupted capture remains
[incomplete](../tests/runtime-grammar-actions-initial-9598.json), with separate recovery
evidence. The replacement transport reuses one connection without replaying mutations;
connection handling is an engineering change, not an established explanation of the timeout.

The first selected-scope attempt and a
[second attempt](../tests/runtime-grammar-scopes-second-attempt-9598.json) timed out at
baseline-selection writes before the
pending candidate query. Both `finally` restorations completed; after the first, an
additional fresh full snapshot matched the initial state without another mutation. Both attempts, including the [first capture](../tests/runtime-grammar-scopes-initial-9598.json),
remain `incomplete-run`; a pending query label must not be mistaken for the operation that
timed out. The journal and traceback identify the write phase.
The final scope runner batches its read-only candidates under each selected baseline,
reducing redundant selection writes while retaining independent passes and readback guards.

## Questions covered by the candidate specification

- `delimiters`: Does each whitespace byte work before the script, after the head, and after
  a numeric argument? Does punctuation terminate numeric parsing differently from a quoted
  argument? Do quotes preserve an actual newline?
- `numbers`: What do signs, leading zeros, decimal point/comma, missing integer part,
  exponent/hex/fraction syntax, `%`, `ms`, `bt`, suffix case, spacing, and suffix adjacency
  produce? Does a fractional duration survive a cast independently of display rounding?
  The follow-up also asks about integer-width boundaries.
- `quotes` and `names`: Which quote terminates the argument; do backslashes escape it;
  what happens to unmatched/empty/doubled quotes? Which punctuation truncates an unquoted
  text token? How are `$`, `%`, and quoted/unquoted `@` names represented? These last
  questions do **not** test variable persistence or shared state.
- `backticks`: Compare literal transport through `constant`, interpolation through
  `get_text`, evaluation through `param_add`, quoted backtick expressions, unmatched
  delimiters, and a computed deck prefix. A single consumer cannot stand in for all others.
- `prefixes`: Compare numeric deck identity, `zone`, case, quoting, numeric junk suffixes,
  nested prefixes and the keyword vocabulary found in `deckMatch`. Constant-valued tests
  of deck keywords establish query reachability only. Follow-ups contrast legacy sampler,
  effect and `get` forms with distinguishable results.
- `fallback` and `operators`: Does a plain unknown argument become text, does punctuation
  stop before a later query, what does an unknown head return, and do malformed arguments
  prevent a later query? Parentheses, chaining, ternaries, comparison syntax and modifier
  spellings are boundary tests, not a complete action-semantics specification.

The expanded capture adds the zoom executor, `IActionSwitch` executor, beatlock setter,
all-deck wrapper and initialization, selected-deck setter, `getDeck`/`getDeckSafe`, query
conversion entrypoints, and the exact `char const*` comparison overloads reached by
`create`. Ambiguous symbol requests now fail extraction instead of choosing an overload.
The [frontier artifact](../tests/runtime-parser-frontier.json) retains every unexpanded
direct target and indirect call site from the selected bodies. Its name-based review labels
are triage only: an empty parser-adjacent-name queue would not prove transitive completeness.

The binary path inventory includes `create` → `deckMatch` → `numberMatch`/`stringMatch`,
`create` → `stringGetParam`, and recursive creation of structural children. The capture
also follows parameter retrieval/conversion helpers, `getParamEval`,
`IParamValuesAction::getValues`, `actionGetText`, and the query/execute dispatch entrypoints.
These are instruction-level relationships. Factory and virtual dispatch remain explicitly
listed boundaries; selected consumer bodies do not establish coverage of every action class.
`SActionParam::toInt` was not found by the requested symbol lookup.

## Live observations, 2026-09-12 local time

The live app reported **build 9598** through `get_build`. UTC timestamps are in each capture.
Use `just runtime-grammar` → `verdicts` for current artifact-derived totals, and `--get` for
all repeated values and controls. Verdicts are recomputed from stored observations by
`--check`; drift, failed controls, and a failed contrast cannot produce `held-in-fixture`.

The [confirmation capture](../tests/runtime-grammar-confirmation-9598.json) completed
forward and reverse passes. Representative observations in `parser_constants`:

- `constant\t37` returned `error:-2147467259`; a leading tab followed by `constant 37`
  returned `37`. `constant 37\t& param_add 5` returned blank, while the space-separated
  counterpart returned `42`.
- `constant 37,5` returned `37.5`. `constant 37.5ms` returned `38ms`, while
  `constant 37.5ms & param_cast float` returned `37.5`. This separates observed rendering
  from an assertion that the parser discarded the fraction.
- `constant` with a backtick-wrapped `constant 37` returned the backtick text. `get_text`
  interpolation returned `37`; `param_add` with backtick-wrapped `constant 37` and
  `constant 5` returned `42`.
- `constant 37 #zzqqx & param_add 5` returned `37`; replacing `#zzqqx` with `zzqqx`
  returned `42`. `constant zzqqx` itself returned `zzqqx`. A generic “unknown tokens are
  ignored” assertion would conflate different observations.
- `deck 99 get_deck` returned `1` in this context; deck 2 returned `2`. This does not prove
  that arbitrary out-of-range deck numbers always select deck 1.

The confirmation's remaining failed predictions concern `get_text` handling of backslash-n,
an unknown legacy effect verb, and an assumed empty sampler slot. The
[focused follow-up](../tests/runtime-grammar-followup-9598.json) independently repeats
corrected comparisons: it records CR/LF expansion by `get_text` versus literal preservation
by `constant`, and observed sampler/effect prefix results. Its `int-width-*` cases retain
the exact numeric boundary inputs and outputs. None of these observations promotes a
verb-store status or edits the normative grammar reference.

The [stateful action capture](../tests/runtime-grammar-actions-9598.json) completed both
passes on HTTP build 9598 with every frozen prediction `held-in-fixture`. Exact cases and
readbacks remain in the artifact; representative observations were:

- `zoom 0.25` ended at `0.25` from both baselines. `zoom +0.25` ended at `0.5` and `0.9`;
  `zoom -0.25` ended at `0` and `0.4`. Integer `zoom 1` left each baseline unchanged.
- Deck 1 `beatlock 1` set both baselines on, while `beatlock 1.0` left them unchanged.
  `beatlock +0` inverted them. Quoted `on` and the tested backtick operands left them
  unchanged; the literal `on` set them on.
- From off/on/off/on, bare `deck all beatlock` ended on/on/on/on; from the inverse baseline,
  it ended off/off/off/off. Explicit `deck all beatlock toggle` inverted each individual
  deck instead. These are observations in `parser_all_decks_asymmetric`, not a universal
  claim about every action broadcast by `deck all`.
- `deck 1 beatlock #zzqqx` inverted its baselines, whereas the ordinary nonsense controls
  left them unchanged. The measured difference is specific to that consumer and input.

The [selected-scope capture](../tests/runtime-grammar-scopes-9598.json) completed both
passes. `deck 99 get_deck`, `deck 0 get_deck`, and `deck default get_deck` returned the
selected baseline, first `1`, then `2`. Explicit deck 1/2 and left/right retained their
respective identities in this skin. The prediction that `active` would follow selection
failed: it returned `1` in both baselines. The prediction that a backtick-computed deck
prefix would return `2` also failed: it returned `error:-2147467259` in both. The artifact
keeps those failed predictions, with the independent deck-3 contrast and nonsense controls.

The [scope follow-up](../tests/runtime-grammar-scope-followup-9598.json) independently
repeated revised active/backtick predictions and added `deck master get_deck`, with deck 1
verified as master after each selection baseline. All of those predictions held on build
9598. The isolated master query completed here; that does not explain the earlier app exit
in the initial lexical sweep.

The [raw-response capture](../tests/runtime-grammar-whitespace-9598.json) completed with
all predictions held: the tested quoted leading/trailing spaces, tab-only, LF-only and
CR-only strings survived in the HTTP body. `get_text '\n'` produced CR/LF bytes; `constant`
with the same literal backslash-n retained those literal characters. Read its `--get` records
for escaped input/output bytes rather than relying on Markdown whitespace rendering.

The [original fallback predictions](../tests/runtime-grammar-action-fallback-9598.json)
also completed both passes. Predictions of `0.5` failed: bare zoom, quoted default and the
malformed numeric/punctuation inputs repeatedly produced `0.2` from both baselines. `.25`
also produced `0.2`, contrary to the predicted unchanged state. Separated `25 %` left the
baselines unchanged, as predicted. The separately frozen
[revised suite](../tests/runtime-grammar-action-default-cases.json) retains `prior_case`
links and adds bare zoom as an explicit comparison; the failed suite is not rewritten.
An [initial revised attempt](../tests/runtime-grammar-action-default-initial-9598.json)
timed out on `zoom 25BT`; its restoration verified successfully and its verdicts remain
incomplete. The subsequent runner spaces writes without replaying them. A timeout is not
used as a grammar verdict, and pacing is not claimed to explain the transport failure.
The [revised confirmation capture](../tests/runtime-grammar-action-default-9598.json)
completed both passes with all predictions held and final restoration verified. In those
comparisons the malformed inputs matched bare zoom at `0.2`, while the ordinary junk
controls left their baselines unchanged.

The action run's final zoom, beatlock, selection, PFL, master, loaded and playing readbacks
matched the initial snapshot. No action result was inferred from its execute response.

The [initial capture](../tests/runtime-grammar-live-9598.json) was interrupted by a connection
reset during the reverse pass, with `deck-token-master` pending after `deck-token-sandbox`.
A process check then found no VirtualDJ process. No crash report was located. The app was
relaunched and the remaining confirmation suite completed. **The cause of the exit is not
established.** Initial cases retain `incomplete-run`; the pending case is excluded from
automatic confirmation and listed in `excluded_cases`.

## Contrast with the Button Editor

The same-build capture includes `DLGActionWizard::updateList`, `getCurrentWord`, `onChanged`,
`updateHint`, and `STree` methods. The editor tree builder's bounded body contains its own
character tests, span allocations and tree operations; the runtime body contains typed
parameter construction and action-factory dispatch. The selected editor builder does not
call `IAction::create`. This is a structural contrast, **not proof that the two accept the
same language**.

The editor's structural masks and quote branches suggest comparing the whitespace,
quote/newline, backtick, unknown-head and modifier cases above against editor spans. Existing
[Syntax Evidence](VDJScript%20Syntax%20Evidence.md#targeted-disassembly-findings) supplies
historical editor observations. A [fresh UI observation](../tests/runtime-grammar-editor-9598.json)
on build 9598 displayed `constant 37zzqqx & param_add 5` without a visible syntax-error
message, while the HTTP case returned blank. The editor showed ordinary `param_add` help.
This is not acceptance or token-tree proof: AX exposed no script field or spans, and an
exact-tab paste attempt timed out. The original button action was visibly restored and
the editor closed without executing a test script. HTTP cannot read highlighting or guard
hints, so the prober cannot adjudicate the editor half of the suite.

## What remains

H4 cannot honestly be called a complete grammar recovery yet. `manifest.coverage` and
`manifest.unresolved` retain the static frontier. Remaining discriminating work includes:

- The isolated master query has now completed in a guarded fixture, but the earlier app
  exit remains unexplained. Do not assign causation from the pending-query label.
- Exercise scope keywords in prepared, asymmetric master/active/video/mixer states; constant
  reachability alone cannot identify the selected deck or prove fan-out.
- Extend the tested action consumers to button-lifetime modifiers with a channel that can
  supply both press and release. The HTTP execute channel does not expose that lifecycle;
  numeric, boolean and flag observations in zoom/beatlock cannot stand in for it.
- Observe local/global/persistent variable isolation, remote-mode creation, and surface
  consumers through appropriate fixtures. The present read-only suite tests lexical forms,
  not those state changes or the `isRemote` branch.
- Close argument-consuming targets at the recorded static frontier and run the matching
  candidate corpus through the live Button Editor. Do not treat C++ library calls or
  factory allocation as evidence of additional argument grammar.

For future agents, inspect `just runtime-grammar --group …` and `just runtime-parser-frontier` first. Reuse the exact-script
suite and raw captures instead of re-reading assembly or adding token variants to a prober
that normalizes their separators. Keep formatting, parsing, consumer semantics and editor
appearance as separate predictions.
