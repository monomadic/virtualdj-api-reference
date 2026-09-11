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
just runtime-grammar
just runtime-grammar --group delimiters
just runtime-grammar --get backtick-numeric-consumer
just runtime-grammar --artifact tests/runtime-grammar-followup-9598.json
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
adds exact-script comparisons to the same prober. It uses only `/query`. The named
`parser_constants` fixture asserts distinct constant values and deck identities, performs no
setup mutations, and records loaded/playing/default-deck context. Context-dependent follow-up
cases additionally require their contrasting sampler/effect outputs to match; a changed bank
or effect setting makes those cases inconclusive rather than evidence against the parser.
Hardware and account state were not inspected. The live process architecture was not measured.

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

- Identify and safely reproduce the interrupted deck-context case before replaying it.
- Exercise scope keywords in prepared, asymmetric master/active/video/mixer states; constant
  reachability alone cannot identify the selected deck or prove fan-out.
- Test relative flags, default/all/value flags and button-lifetime modifiers through a
  reversible action fixture with independent readback. Query serialization does not expose
  all native parameter tags or dispatch flags.
- Observe local/global/persistent variable isolation, remote-mode creation, and surface
  consumers through appropriate fixtures. The present read-only suite tests lexical forms,
  not those state changes or the `isRemote` branch.
- Close argument-consuming targets at the recorded static frontier and run the matching
  candidate corpus through the live Button Editor. Do not treat C++ library calls or
  factory allocation as evidence of additional argument grammar.

For future agents, inspect `just runtime-grammar --group …` first. Reuse the exact-script
suite and raw captures instead of re-reading assembly or adding token variants to a prober
that normalizes their separators. Keep formatting, parsing, consumer semantics and editor
appearance as separate predictions.
