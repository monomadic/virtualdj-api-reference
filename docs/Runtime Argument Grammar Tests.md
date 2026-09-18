# Runtime argument grammar: H4 tests

This is a candidate specification expressed as executable predictions, **not a grammar
reference**. Binary observations remain Tier 2. A live verdict establishes only the exact
HTTP result in its named fixture, on the recorded build. It does not establish universal
argument acceptance, action behavior, editor acceptance, or equivalence between builds.

The common parser has been captured and its main lexical branches exercised. This is **not
an exhaustive recovery of every reachable argument consumer**. The historical call-graph frontier, its later closure, and the remaining discriminating
fixtures are explicit below; H4 remains open.

## Branch-family audit

`just runtime-grammar --audit` joins the reviewed branch-family obligations in
[the structured checklist](../tests/runtime-grammar-obligations.json) to exact case ids,
fixtures, builds, verdicts and control separation. It validates the linked captures and
historical assembly hashes. The output also fixes a representative editor corpus by exact
runtime case reference, so a new UI pass can record the same source text with screenshots.

This is a coverage audit in progress, **not an exhaustive control-flow-edge proof**. A mapped
family is not a closed branch: null readings, failed predictions and the next required review
are retained. Symbols without a family mapping are listed rather than silently counted as
covered. The remote entry route and list conversion helper currently have no reviewed live
case linkage; deciding their exact scope and adding discriminating fixtures remains work.
Editor corpus entries are pending observations, not predictions of editor acceptance.

### Unmapped-symbol triage (2026-09-17)

`just runtime-grammar --triage` returns only the reviewed dispositions, next actions,
related obligation ids and checked instruction anchors for captured b9246 symbols
without a primary family mapping. The same result is included under
`unmapped_symbol_triage` in `--audit`; derive totals from its `disposition_counts`.
The checklist owns the review, and the command checks each anchor against the hashed
assembly. Related obligations are navigation links, **not live case associations**.

The former `investigate-next` leads now have separate consumer obligations:
`boolean-cache-consumer`, `incoming-parameter-selection`, `pair-typed-consumer`
and `pair-float-consumer`. The pair-reader association retains a build-specific
route uncertainty described below; mapping is not branch closure. Each remaining lead needs a verified caller and a discriminating
observable before a new behavioral obligation. Existing switch or arithmetic results cannot silently cover
another helper or overload. The remaining dispositions separate support for existing
lexical/conversion families, stateful dispatch/deck questions, selected action behavior,
editor observations, and construction/ownership support.

This review does not remove entries from `symbols_without_family_mapping`, partition
all branches, or claim live coverage. `symbols_without_triage` exposes newly captured
gaps. Follow the recorded `next_action` instead of reopening every helper: cleanup and
factories need a concrete lifetime/construction question, while editor evidence needs
saved screenshots. The historical capture remains b9246; no current-build behavior
was tested in this triage.

**Fold-in (2026-09-19).** The triage is now split three ways:

- **Joined to a family as navigation.** Every `review-with-existing-family` symbol is
  listed under `related_symbols` on each obligation its group names. These are the lexical
  helpers, `getDeckFromString`, the text-expansion pair and the typed-result conversions.
  Such a listing adds no evidence link. The symbol stays in
  `symbols_without_family_mapping`, and the family's result counts are unchanged. The next
  step for each is still its group's `next_action`: join exact caller sites to existing
  cases.
- **Out of scope.** Each `support-only` symbol has a one-line `out_of_scope` reason: the
  all-decks and combined-query factories, `ACTION_all_decks::init`, and the editor-tree
  `clear`/destructor.
- **Named open items.** The `context-fixture-needed` groups are dispatch/source context and
  deck-state selection. `editor-fixture-needed` is editor word and presentation.
  `consumer-specific` is the selected `zoom`/`beatlock` implementations. These stay open,
  and none is closed by this fold-in.

`just check-runtime-grammar` fails if any `related_symbols` entry names a symbol, group or
obligation that the triage does not, or carries anything beyond navigation. It also fails if
an `out_of_scope` reason appears on a symbol that is not `support-only`, or is missing from
one that is.

### Incoming parameter selection (2026-09-17)

**Tier 2 route, b9246:** `ACTION_zoom::onExecute` calls `IAction::getParam(0)`
at `0x1005c931c`. The getter first selects explicit stored arguments; its fallback
at `0x100596c6d` reads the incoming area at object offset `0x68`, subject to
index/flag checks. `IAction::execute` stores its incoming pointer there and checks
the following action before virtual query dispatch (`0x100596126`–`0x100596175`).
These checked historical bodies motivate the fixture; they do not identify which
instructions executed on the current build.

The [initial query capture](../tests/runtime-grammar-incoming-query-initial-9628.json)
did not discriminate: `constant 37 & constant 11` still returned `37`, and the
opposite-valued source repeated that pattern. Its oracle failures cannot establish
incoming-argument fallback. The
[direct action capture](../tests/runtime-grammar-incoming-actions-initial-9628.json)
then showed that `constant 0.37 & zoom` and the `0.83` source reset zoom to `0.2`;
explicit decimal/zero/relative tails worked, while `default` matched nonsense
controls. Those frozen failed propagation predictions remain in the audit.

The [first pipeline attempt](../tests/runtime-grammar-incoming-pipeline-aborted-9628.json)
and [bounded attempt](../tests/runtime-grammar-incoming-pipeline-bounded-aborted-9628.json)
aborted on uncertain HTTP writes. Both verified restoration; neither supplies
behavior evidence. Their uncertain scripts were not replayed. The write channel
now opens a fresh connection for each mutation, still without retrying a lost
response. Connection reuse was a suspected transport issue, not a demonstrated
cause of those timeouts.

**Local test, HTTP build 18.0.9628:** the
[completed pipeline run](../tests/runtime-grammar-incoming-pipeline-9628.json) and
[independent confirmation](../tests/runtime-grammar-incoming-pipeline-confirmation-9628.json)
use four unloaded, stopped decks and the existing `parser_zoom_levels` fixture.
Each script starts from zoom `0.25` and `0.65`, repeats independent `zoom` readback,
then restores the original resource values and verifies deck/context guards.
The confirmation adds same-source direct-chain contrasts.

- `constant 0.41 & param_cast float & zoom` sets zoom to `0.41`; source `0.79`
  sets it to `0.79`. Both separate from pipeline nonsense tails.
- Adding explicit `zoom 0.25` or `zoom 0.0` overrides either incoming source.
- Explicit `zoom +0.25` yields `0.5` and `0.9` from the prepared baselines,
  rather than adding to the incoming source.
- Removing the `param_cast float` bridge resets bare zoom to `0.2`, including
  the same `0.41`/`0.79` source controls in the confirmation.

These exact observations map the getter to a discriminating live consumer. They
are not a universal chain rule, native-type proof, flag-bit coverage, or evidence
for the second incoming slot. `default` with the bridge remains unmeasured after
the uncertain write. Per-verb conclusions are available through `just verb zoom`.

Inspect without loading the journals into agent context:

```sh
just runtime-grammar --artifact tests/runtime-grammar-incoming-pipeline-confirmation-9628.json --group incoming-zoom --check
just probe-arg-forms --grammar-actions tests/runtime-grammar-incoming-pipeline-confirmation-cases.json --check
```

Use a new output path for a fresh guarded live run. Do not re-run aborted suites
as a way to complete them; keep their uncertain writes excluded.

### Pair-reader consumers (2026-09-18)

**Tier 2, b9246 x86_64:** the bounded direct-call scan now includes both exact
`IParamValuesAction::getValues` overloads. `ACTION_param_add::onQuery` calls the
`SActionParam*` overload at `0x100992a73`; `ACTION_param_multiply::onQuery`
calls the `float*` overload at `0x100993524`. Other verified float callers are
`param_bigger`, `param_equal`, `param_smaller`, `param_pow` and `param_mod`.
The scan retains an unrelated byte candidate at `0x10217e5b3` with
`verified_instruction: false`; it is not a caller edge. Indirect calls and inlined
copies remain outside this inventory.

Use the compact checked lookup rather than loading every captured body:

```sh
just runtime-grammar --callers 'IParamValuesAction::getValues(float*, float*)'
just runtime-grammar --callers 'IParamValuesAction::getValues(SActionParam*, SActionParam*)'
```

Only explicitly scanned targets are accepted. The lookup includes source build/hash,
verified instruction sites and rejected candidates; it never claims live coverage.
The `pair-typed-consumer` obligation joins the existing `param_add` captures without
silently extending those observations to the float helper.

**Local test, HTTP build 18.0.9628:** the read-only `parser_constants` fixture uses
asymmetric operands in both positions, repeated reads, reversed order on the second
pass, and shape-matched nonsense controls. The
[initial run](../tests/runtime-grammar-pair-float-9628.json) and
[independent confirmation](../tests/runtime-grammar-pair-float-confirmation-9628.json)
retain the same frozen predictions, including failures. Exact outcomes are exposed by:

```sh
just runtime-grammar --artifact tests/runtime-grammar-pair-float-confirmation-9628.json --group pair-float --check
```

With the other operand fixed at `3`, in either position:

- Integer `7`, quoted action text `'constant 7'`, paired-backtick `constant 7`, and
  the longer quoted action chain return `21`, separating from their controls.
- Decimal `2.5` and paired-backtick `constant 2.5` return `7.5`.
- Direct `25%` returns `75%`, direct `7ms` returns `21ms`, and paired-backtick
  `constant 7bt` returns `21bt`. These **fail** the frozen plain-number predictions.
- Direct `7bt` returns `error:1`, failing the predicted multiplication result.
- Quoted numeric text, computed numeric text, an outer-quoted expression missing
  its final backtick, and trailing-backtick-only action text return `0`, matching
  their respective controls. The trailing-only prediction remains failed; none
  of these zero outputs proves successful evaluation or a universal coercion rule.

The historical float-success branch multiplies scalar temporaries and writes a
`val` result at `0x10099362d`–`0x100993644`. The unit-bearing outputs above do not
establish that route on build 9628. The consumer has other paths, and the binaries
are different builds; determining whether the current route changed requires
current-build structural evidence or a discriminating path observation. No native
parameter-type or current instruction execution is inferred from HTTP formatting.

The separate overload obligations preserve this uncertainty. Next: partition each
helper's operand-source/type branches and establish the current multiplication
route before explaining the unit behavior. Implicit input, persistent action-cache
reuse, execute behavior and the other callers remain outside this query fixture.
Per-verb observations belong to `just verb param_multiply`.

### Bounded evaluator branch review (2026-09-17)

The audit's `evaluator_branch_review` partitions every conditional jump in the
captured b9246 `IAction::getParamEval` and `IAction::getFloatParamEval` bodies.
Each group records exact instruction sites, a **Tier-2 structural interpretation**,
and the unresolved question or evidence limit. The checker derives the conditional
jump set from the hashed assembly and rejects missing, duplicate or unknown sites.
The output includes the branch instructions/targets and derived classification counts.

The classifications distinguish token/evaluation questions from caller context,
cache lifecycle, string storage, ownership, and optional caller outputs. This is
an inspection boundary, not a declaration that a branch executed or worked. In
particular, the constant-prefix display failures do not settle incoming parameters;
the zero-initialized display input does not settle nonzero relative addition; and
separate HTTP requests do not establish compiled-action reuse or invalidation.
Long-expression results do not prove which string-storage alternative ran.

The partition excludes unconditional transfers, callees, other parser functions,
and instruction-level live coverage. It does not supply a denominator for all of
H4. Future work should consult the group's `remaining_question` before adding a
fixture: cleanup and optional output-pointer branches are not separate syntax rules.

### Boolean cache callers (2026-09-17)

The [route capture](../tests/runtime-parser-branch-routes.json) now includes direct
`getBoolParam` call candidates verified inside bounded b9246 x86_64 disassembly.
`boolean_cache_arguments` reviews the nearby setup of the fifth SysV argument,
`r8` (counting `this`). Both `ACTION_effect_active::onExecute` calls, at
`0x1008a16ea` and `0x1008a179c`, supply an object-relative address. The other
verified calls in this scan explicitly zero `r8d`. Derive the inventory from
`boolean_cache_arguments.calls`; indirect and inlined callers are outside the scan.

The selected-slot route and explicit-effect-name route therefore provide concrete
**Tier-2 caller leads** for the helper's optional-cache path. This does not prove
current instruction execution or cache reuse. The reviewer checks nearby straight-line
setup only and leaves unresolved patterns visible; disassembler labels substituted
for numeric displacements are not field identities. Reproduce using the branch-route
extraction command below, whose source hash must match the historical manifest.

The `parser_effect_boolean` fixture extends the existing reversible-action runner.
It requires four unloaded, stopped decks and Phaser already selected in deck 1
slot 1. It performs no effect selection or parameter writes. Each candidate starts
from both off/on baselines, is read back through `deck 1 effect_active 1`, and is
followed by verified restoration. Guards retain deck context, neighboring effect
selections/activation, and Phaser slider/button values. The runner rejects other
slots, effect names, chained actions and arbitrary nested expressions. A changed
selected effect name blocks restoration writes to the replacement effect.

Reproduce with the prepared fixture (the command changes activation temporarily):

```sh
just probe-arg-forms --grammar-actions tests/runtime-grammar-effect-boolean-confirmation-cases.json --check
just probe-arg-forms --grammar-actions tests/runtime-grammar-effect-boolean-confirmation-cases.json --rounds 2 --repeat 2 --out /tmp/effect-boolean-new.json
just runtime-grammar --artifact /tmp/effect-boolean-new.json --check
```

#### Phaser activation observations, HTTP build 18.0.9628

The [initial capture](../tests/runtime-grammar-effect-boolean-initial-9628.json)
preserves the original predictions and failures. The
[confirmation capture](../tests/runtime-grammar-effect-boolean-9628.json) uses
shape-matched quoted-text and unclosed-expression controls, and adds opposite-valued
forms without rewriting the initial expectations. Each run repeats both off/on
baselines and reverses case order on its second pass. Inspect verdicts and control
separation through `just runtime-grammar --artifact <capture> --check`; the
`boolean-cache-consumer` audit obligation joins both runs to their actual state readbacks.

In both the selected-slot and explicit `'Phaser'` forms, bare/`toggle`/`-1` toggled,
`1` set activation on, and `0` set it off. Paired-backtick `on`/`off` and
`constant 1`/`constant 0` produced on/off signatures; `constant -1` toggled.
The outer-quoted paired-backtick expression also set activation on. These outcomes
separated from the paired-backtick nonsense controls. The tested direct decimal/percent
forms and computed decimal forms left both baselines unchanged, matching their controls;
this does not identify a native type or prove a general conversion rule.

The control correction matters: selected-slot quoted `on`/`off`, raw quoted
`constant 1`/`constant 0`, and quoted nonsense all set activation on. With explicit
`'Phaser'` naming, those same quoted arguments and controls left activation unchanged.
Unclosed expressions and unclosed nonsense toggled in both routes. None of those
results proves successful raw-text or unclosed-expression evaluation. Failed predictions
remain failed even where their outputs match the improved controls.

The captures establish activation readback only, with restoration and collateral
guards; they do not establish audible processing, other plugins, stems, native parameter
types, live instruction coverage or persistent compiled-action cache reuse. The next
cache-specific obligation is to execute the **same independently identified compiled
action** with changing nested input and observe activation separately. Repeated HTTP
requests alone do not supply that identity.

### Remote-entry and list-helper reachability review (2026-09-17)

The [route capture](../tests/runtime-parser-branch-routes.json) records the b9246 binary hash,
remote-branch anchors, bounded mode-writer assembly, and the exact limits of a list-helper
reference scan. These are Tier-2 leads, not grammar rules. Reproduce with:

```sh
.venv/bin/python tools/runtime_parser_branch_routes.py --binary /tmp/vdj-h4-9246/vdj.pkg/Payload/VirtualDJ.app/Contents/MacOS/VirtualDJ > /tmp/branch-routes.json
.venv/bin/python tools/runtime_parser_branch_routes.py --check
just runtime-grammar --audit
```

The remote question is now specifically: **with `IAction::isRemote` independently
established, which checked action heads rejoin ordinary parsing at `0x1005974cf`, and which
reach the source-text wrapper route at `0x100598365`?** The capture includes the literal
checks and the factory/text-assignment sites. Immediate-byte writes to the mode flag were
verified in bounded skin-load, Remote-client callback and scratch-constructor bodies.
This supplies possible fixture entry points; it does not establish that subscribing over
the Remote protocol enables the flag. `parser_remote_mode` remains a fixture obligation,
not an available prober fixture. No new remote behavior is claimed or marked tested.

For `getListParam`, the scan found no E8/E9 direct-branch candidates in `__TEXT`, and no
exact target-address bytes in the scanned file-backed non-LINKEDIT segments. The method
and target are recorded so the negative is reproducible. This does **not** rule out indirect,
computed or inlined equivalents. The earlier audit associated a captured utility with a
possible common conversion path, but had not demonstrated reachability from `create`.
Its obligation is therefore reachability review first, not a speculative live consumer sweep.

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

## Position-controlled delimiter tests (2026-09-16)

The earlier `number-end-*` and `suffix-boundary-*` cases confounded the inserted byte
with operator adjacency. The frozen [boundary suite](../tests/runtime-grammar-boundary-cases.json)
separates terminal bytes, a byte before an ordinary separating space, and a byte after it.
It tests TAB, LF, CR, VT, FF and NBSP after integer, percent, millisecond and beat arguments,
inside `parser_constants`. The [follow-up](../tests/runtime-grammar-boundary-confirmation-cases.json)
changes the value and calculation and adds quoted arguments. Every row remains a question
with a frozen expected output, two junk controls and independent contrast oracles.

```sh
just runtime-grammar --artifact tests/runtime-grammar-boundary-9598.json
just runtime-grammar --artifact tests/runtime-grammar-boundary-confirmation-9598.json
just probe-arg-forms --grammar-cases tests/runtime-grammar-boundary-confirmation-cases.json --repeat 2 --rounds 2 --out /tmp/boundary-confirmation.json
```

Observed on build 9598 in forward/reverse passes with repeated reads:

- Did `constant 37<TAB>`, and the version with a calculation following the tab and
  a separating space, return blank? Yes. These match their malformed-number controls,
  so the held predictions are **null readings**, not token-recognition evidence.
- Did `constant 37 <TAB> & param_cast float & param_add 5` reach `42`? **No: `37`.**
  LF and CR gave the same failed prediction. The byte-free contrast returned `42`.
  The corresponding `%`, `ms` and `bt` cases also retained the original rendered value.
- Did the narrower prediction survive new values: `constant 53 <TAB> & param_cast float & param_add 9`
  returning `53`, versus `62` with the tab removed? Yes. Each tested byte, including
  VT, FF and NBSP, gave its frozen original-value prediction; the unit-bearing and quoted
  variants also matched. These outputs separated from the blank junk controls.

The initial failed predictions remain unchanged. For artifact-derived verdict and separation
totals use the commands above. The observation constrains those exact output comparisons;
it is not a claim that all whitespace everywhere follows one rule. The historical binary
lead at `IAction::stringGetParam@0x10059961c` tests ordinary spaces after a parameter,
whereas the head/prefix paths contain different delimiter masks.

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
- `parser_master_scope` pins the selection and the master deck to *different* decks —
  `(selection, master)` of `(1, 2)` then `(2, 3)` — so a selector's two-baseline signature
  identifies which state it reads.

The allowlist permits zoom/beatlock forms, or literal `deck N select` setup/restoration in
the scope mode; `parser_master_scope` adds literal `deck N masterdeck on` and
`masterdeck_auto on|off`, each journaled and put back before the shared guard comparison
runs. It refuses to start unless exactly one deck holds master, and aborts rather than
proceed if a pin does not hold, since a master that silently stayed put would make every
selector look like a constant. The runners verify absolute-setter round trips before candidates, read
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

**A held verdict is not by itself a discriminating result.** A frozen prediction of blank
holds when the script returns blank — and so do the nonsense controls, which makes that
reading a null rather than evidence about the token. The report therefore derives a
`separation` field beside every verdict (`separates`, `matches-controls`), counts them in
the summary, and names the `held_but_matches_controls` cases outright; it is computed from
the stored observations and never written into a capture, so recorded evidence is unchanged.
Read the verdict for whether the prediction was right and `separation` for whether the case
could have distinguished anything. The two stateful suites answer this differently from the
read-only one: their asymmetric baselines mean a script that moves *neither* baseline while
the contrast oracle demonstrably moves both is a genuine no-op finding, not a null.

The [confirmation capture](../tests/runtime-grammar-confirmation-9598.json) completed
forward and reverse passes. Representative observations in `parser_constants`:

- Whitespace bytes are not interchangeable at the head: `constant\t37` returned
  `error:-2147467259` while `constant\n37` returned `37`, and a leading tab before
  `constant 37` returned `37`. That pair is the unconfounded whitespace comparison.
- The post-number whitespace cases are **not** such a comparison, and an earlier revision of
  this section read them as one. `constant 37\t& param_add 5` returned blank against `42`
  for the space-separated form — but `constant 37& param_add 5`, carrying no tab at all,
  also returned blank. The discriminator there is the space *preceding* `&`, not the byte
  following the number, so every `number-end-*` case restates one result. The twelve
  `suffix-boundary-*` cases add a unit-suffix confound on top and cannot isolate the
  delimiter either.
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
the exact numeric boundary inputs and outputs.

**Promoted 2026-09-12.** The lexical candidates stayed unpromoted while they were single
readings. The rules that survived two independent suites, two prepared baselines and two
passes are now written into the normative reference: keyword quoting, unit-suffix case and
adjacency, comma decimals, signed-versus-unsigned numbers, the malformed-number reset, and
backtick inertness in execute position — see
[Arguments and quoting](VDJScript%20Grammar.md#arguments-and-quoting),
[Backticks](VDJScript%20Grammar.md#backticks-are-a-surface-feature-not-a-parser-feature)
and [What an unrecognized tail does in execute position](VDJScript%20Grammar.md#what-an-unrecognized-tail-does-in-execute-position-2026-09-03).
`zoom` and `beatlock` carry `local_test` records in the verb store. Everything still
resting on a single capture, and every editor-side question, stays here as a candidate.

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

## Closing the static frontier (2026-09-12)

`runtime_parser_frontier.py` queues an indirect call site whenever the target depends on
runtime state. That is correct triage, but a queue is not a conclusion, and 30 open sites left
it possible that argument grammar lived somewhere the lexical suites never reached. Reading
the captured assembly around each site closes all 30, and the answer is that **none of them
consumes script arguments**:

| Closure | Sites | What the setup instructions show |
| --- | ---: | --- |
| `virtual-dispatch` | 26 | `movq (%obj), %rax` then `callq *0xNN(%rax)` — a vtable loaded from object offset 0. In 18 of them the preceding instruction is `lock decl 0x8(%obj)`, an atomic refcount decrement, so the call is a release or destructor. |
| `action-factory` | 3 | `leaq _actionFactory(%rip)` then a call through that table. |
| `disassembly-artifact` | 1 | Surrounding bytes decode as `bad opcode` / `lcalll` / `sti`: the decoder walked into data, so the site is not code. |

**`_actionFactory` is a function-pointer table indexed by verb id**, and the capture proves
the indexing rather than assuming it. Two of the three sites call a fixed entry and then store
that same number as the object's id at `+0xc`: entry 5 is followed by `movq $0x5, 0xc(%rax)`,
entry 61 (`*0x1e8`) by `movl $0x3d, 0xc(%rax)`. Offset ÷ 8 == verb id.

The structural conclusion is the useful part. In `IAction::create`, the argument loop —
`IAction::stringGetParam` feeding `vector<SActionParam>::push_back` — runs to completion
*before* the factory call, and the constructed object is then handed the finished vector. So
**arguments are lexed centrally and only then dispatched per verb.** The lexical rules the H4
suites recovered are the whole of the central grammar; anything further is per-verb behavior
inside the constructed action, which no amount of reading `IAction::create` will reveal. That
is the boundary this task was told to find, and it is where the static route ends.

One warning for anyone reading the raw capture: it symbolizes **offset 0** as
`CONFIG_EMULATE_HARDWARE`. So `*CONFIG_EMULATE_HARDWARE(%rax)` is vtable slot 0 and
`movq CONFIG_EMULATE_HARDWARE(%r14), %rax` is an ordinary vtable load — a symbolization
artifact, not a configuration branch. Two frontier rows look alarming until you know that.

## Hazard: this suite family has made VirtualDJ exit (2026-09-12)

**Treat deck-target probing as capable of taking the app down, and do not run it against an
instance the user is playing on.** The repo has two independent signals:

- A recorded exit during the live lexical sweep: connection reset mid-pass, no VirtualDJ
  process afterwards, and **no crash report anywhere** — so an absent `.ips` in
  `~/Library/Logs/DiagnosticReports` does not clear a run. The scripts at that point were
  `deck sandbox constant 37` (ran) and `deck master constant 37` (pending).
- The repo owner reports the app crashing in this line of tests generally, which is a
  stronger signal than the artifacts, precisely because the exits leave nothing behind.

The common factor in both is an **unusual token in the deck-wrapper slot** — `sandbox`, and
the `playing` / `mixer1`-`mixer4` targets the asymmetric-master run added. That slot is one of
the few the parser does not silently accept (`deck zzqqx` returns `error:-2147467259`), which
means it resolves the token to an object; a token that names a real but absent object is the
obvious candidate. **This is a hypothesis with two data points, not an established cause.**
The asymmetric-master run used exactly those targets and completed cleanly with the process
still healthy hours later, so whatever it is, it is intermittent.

### What the bisection ruled out (2026-09-12)

Two hypotheses were tested against the live instance and **both failed**, so the cause is
still open. Neither result clears the app; they narrow where to look next.

- **Not a single token.** `just probe-deck-targets` sent every attested and observed
  deck-wrapper token with two read-only payloads — 46 probes, one per fresh connection,
  journal flushed before each send, process identity checked after each. All 46 answered and
  the process survived, **including `deck sandbox constant 37`, the exact script in flight at
  the recorded exit**. Word tokens all resolve; the bracket forms Atomix uses in shipped
  scripts (`deck [LEFTDECK]`, `[RIGHTDECK]`, `[SWAPDECK]`, `[MINIDECK_LEFT]`,
  `[MINIDECK_RIGHT]`) return `error:-2147467259` over HTTP, consistent with their being
  skin-context names rather than parser targets.
- **Not sustained request volume.** `just probe-http-stability` ran 300 benign `get_build`
  queries over one reused connection and 300 more over a fresh connection each, then 120 more
  in follow-ups — roughly 800 requests without an exit.

That second run did surface something worth knowing, though it is not the crash: the fresh
arm **timed out at request 21**, the process stayed alive, and the reuse arm immediately
after completed all 300. Two later fresh arms of 60 at the same pacing did not reproduce it.
So the interface stalls intermittently for a few seconds and recovers. That is the most
likely reading of this suite family's recorded *timeouts* — and it is the reason a timeout
must never be recorded as a grammar result — but a stall is not an exit.

### The symptom is a hung window, not a crash (2026-09-12)

The owner's account changes what to look for: **VirtualDJ never crashed.** Cmd-tab stopped
being able to reach it — no window, nothing to focus, every other app fine — and it had to be
force quit. So the process survives; it is the window that goes.

That reading fits the artifacts better than a crash ever did. It explains why these events
leave no crash report, and it explains the earlier "no VirtualDJ process afterwards" note as
the *aftermath of a force quit*, not a spontaneous exit.

**`minimize` reproduces the symptom exactly, and the query surface is not how it gets sent.**
Both halves were tested on build 9598 with the decks idle, watching the window through
`AXMinimized` rather than inferring from the HTTP answer:

| Sent | Response | Window |
| --- | --- | --- |
| `/query?script=minimize` | `no` | unchanged, `AXMinimized` false |
| `/query?script=maximize` | `yes` | unchanged, 1 window |
| `/execute?script=minimize` | `false` | **`AXMinimized` true**, process and HTTP both alive |

So `/query` is **inert even for a bare no-argument action verb** — it answers that verb's
state, the same way `deck 3 beatlock on` returns `no` and `beatlock off` returns `yes` while
the state stays `no`. `parsed` in the corpus results meant "answered `no`", not "performed".
The corpus sweep is query-only and is therefore **not** the trigger; a denylist was added
here on that suspicion and then removed, because it would only have cost coverage.

What the execute row does establish is the mechanism. A minimized VirtualDJ is a live process
with a live HTTP interface and no window, and **macOS cmd-tab deliberately will not restore an
app whose only window is minimized** — which is the reported symptom precisely, down to
needing a force quit. `open -a VirtualDJ` restores it without one.

What can send it: **every skin ships an `action="minimize"` button in its title bar** — the
built-in Desktop skins, Lite, and the installed third-party skins all carry one. Nothing in
the user's mappers or `settings.xml` binds the verb, so a keystroke is not the route. A blind
coordinate click during skin-probe or GUI-driving work is, and this repo already records that
route costing misclicks. Treat an unexplained "VirtualDJ is gone" as **minimized until
checked**: read `AXMinimized`, not the process list, and never conclude "crash" from the
absence of a crash report.

The untested difference between these probes and the sessions where the app died: **deck
state**. Every probe above ran against four unloaded, stopped decks, because that is what the
fixtures require. The targets most under suspicion (`mixerN`, `playing`, `sandbox`, the video
targets) name objects that may only exist once something is loaded. Probing them against a
loaded instance has since been done — all 46 probes answered with decks 1 and 2 loaded and
playing ([capture](../tests/deck-target-exit-probe-loaded-9598.json)), so deck state does not
rescue the token hypothesis either.

What this does *not* license: assigning causation from a pending-query label, or treating a
completed run as evidence the tokens are safe. What it does require of any future run here:

- Ask before probing deck targets on an instance in use; a crash costs the user a live set.
- Expect no crash report. Check for the process itself, and remember that after an exit the
  port-80 socket can stay `LISTEN` while refusing connections — only a full quit and relaunch
  clears it.
- The journal is the recovery record. Mutations are written to the capture before they are
  sent, so a vanished process leaves a readable account of what had been changed and not yet
  restored; read it before assuming state was put back.

## Asymmetric master, 2026-09-12

The selected-scope suites pinned only the selection. Master was deck 1 in that fixture, so
`deck master` and `deck active` both answering `1` was consistent with three different
hypotheses at once. `parser_master_scope` pins selection and master apart —
`(selection, master)` of `(1, 2)` then `(2, 3)` — which gives each hypothesis its own
signature: follows-master `['2','3']`, follows-selection `['1','2']`, constant-1 `['1','1']`,
constant-2 `['2','2']`.

```sh
just runtime-grammar-master --run --out tests/runtime-grammar-master-9598.json \
  --repeat 2 --rounds 2
just runtime-grammar-master --check
```

Thirteen predictions were frozen before the run. Ten held, three did not, and the capture's
`signatures` field names what each target actually tracks:

| Case | Predicted | Observed | Signature |
| --- | --- | --- | --- |
| `deck master get_deck` | `2`, `3` | `2`, `3` | tracks-master-deck |
| `deck active get_deck` | `2`, `3` | `2`, `3` | tracks-master-deck |
| `deck playing get_deck` | `1`, `2` | `1`, `2` | tracks-selected-deck |
| `deck default get_deck` | `1`, `2` | `1`, `2` | tracks-selected-deck |
| `get_deck` | `1`, `2` | `1`, `2` | tracks-selected-deck |
| `deck left` / `deck leftvideo` | `1`, `1` | `1`, `1` | fixed-deck-1 |
| `deck right` / `deck rightvideo` | `2`, `2` | `2`, `2` | fixed-deck-2 |
| `deck mixer1 get_deck` | `1`, `1` | `3`, `3` | fixed-deck-3 |
| `deck mixer2 get_deck` | `2`, `2` | `1`, `1` | fixed-deck-1 |
| `deck mixer3 get_deck` | `3`, `3` | `2`, `2` | fixed-deck-2 |
| `deck mixer4 get_deck` | `4`, `4` | `4`, `4` | fixed-deck-4 |

The three failures are all one finding: `mixerN` does not mean deck N. The mapping was
constant across both selections and both master decks, and an independent read after the
run reproduced it, but its cause is untested — do not record it as a language rule.

Read `separation` here narrowly. The junk controls return `error:-2147467259`, so *any*
real answer differs from a control; `separates` means the target was recognized, not that it
discriminated state. The `signatures` field is the reading the asymmetric baselines were
built to produce, and it is what the cross-baseline comparison supports.

This also explains the earlier `scope-active` and `scope-followup-master` rows rather than
contradicting them: under `tracks-master-deck`, a fixture whose master is deck 1 must report
`1` in both baselines, which is exactly what those runs recorded.

The run extends the mutation allowlist by `deck N masterdeck on` and `masterdeck_auto on|off`.
Both were round-tripped by hand against the live instance before the suite was allowed to use
them. The first attempt aborted at the precondition, with an empty journal and no mutation,
because two decks were loaded and playing; that refusal is the fixture working, not a result.

## Asymmetric playback test (2026-09-16)

The frozen [playing-scope suite](../tests/runtime-grammar-playing-cases.json) is run by the
existing prober inside `parser_playing_scope`. It requires four stopped decks, deck 1 selected,
and decks 3/4 empty and unlooped. Decks 1/2 may retain loaded tracks: their loaded/play state,
position, volume, pitch and loop readbacks are protected. The runner generates and verifies
digital silence, loads it only on the currently designated fixture deck, and checks that its
position advances independently of the `play` return value.

```sh
just probe-arg-forms --grammar-playing tests/runtime-grammar-playing-cases.json --check
just probe-arg-forms --grammar-playing tests/runtime-grammar-playing-cases.json --repeat 2 --rounds 2 --out /tmp/playing-scope.json
just runtime-grammar --check --artifact tests/runtime-grammar-playing-9598.json
just runtime-grammar --artifact tests/runtime-grammar-playing-9598.json --group playing-scope
```

The [completed capture](../tests/runtime-grammar-playing-9598.json) records build 9598,
forward/reverse query order and reversed baseline order, repeated reads, nonsense controls,
literal-deck contrasts, setup/calibration, write journals and restoration after each baseline.
The selected deck stays at 1; automatic master mode is disabled while measuring.

| Frozen question | Master 3, only deck 4 playing | Master 4, only deck 3 playing | Live verdict |
| --- | --- | --- | --- |
| Does `deck active get_deck` follow the pinned master despite a different playing deck? | `3` | `4` | Held in this fixture |
| Does `deck master get_deck` return the pinned master? | `3` | `4` | Held in this fixture |
| Does `deck playing get_deck` follow the sole playing deck? | `4` | `3` | Held in this fixture |
| Does `deck default get_deck` remain at the selected deck? | `1` | `1` | Held in this fixture |

Every candidate separated from both unknown-selector controls. Literal deck 3/4 contrasts
returned their respective fixed deck ids. These observations do not settle multiple-playing
deck selection, automatic-master transitions, or the cause of a mixer-number permutation.

The [initial calibration](../tests/runtime-grammar-playing-initial-9598.json) aborted before
candidate queries because the intended selection did not hold after starting playback.
Restoration verified successfully. The corrected setup explicitly reselects deck 1 after
starting the fixture, then verifies selection, master and every play flag before each query.
The failed attempt remains `incomplete-run`; no expectation was changed to turn it into a pass.

Cleanup pauses and unloads only media whose path matches the generated fixture, restores
master/automatic-master mode, selection, PFL and fixture-deck pitch, and verifies the full
recorded guards and protected readbacks. An unexpected replacement track is never unloaded.
The complete capture passed all restoration checks; generated temporary audio is not committed.

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

### Paired help-display test (2026-09-16)

Run `just runtime-grammar-editor` for the joined results. The frozen
[case suite](../tests/runtime-grammar-editor-help-cases.json) runs through the existing
argument prober in the named `parser_editor_help` fixture:

```sh
just probe-arg-forms --grammar-cases tests/runtime-grammar-editor-help-cases.json --repeat 2 --rounds 2 --out /tmp/editor-help-http.json
```

The [HTTP capture](../tests/runtime-grammar-editor-help-http-9598.json) and separate
[UI observations](../tests/runtime-grammar-editor-help-ui-9598.json) are build 9598
observations. UI passes used forward and reverse order, with the original button action
restored and the editor reopened between passes. The final restoration was also checked
by reopening. No test action was executed from the editor. The screenshots behind the UI
rows were not saved, so the UI file is the agent's reading of screenshots that no longer
exist (its `screenshot_provenance` field says so); later UI passes save each screenshot
under `tests/` beside the capture.

| Discriminating prediction in `parser_editor_help` | HTTP observation on build 9598 | Help observation in both UI passes | Result |
| --- | --- | --- | --- |
| Does `constant 37 & param_add 5` return `42` and show `param_add` help? | `42` | `param_add` | Candidate predictions held |
| Does `constant 37zzqqx & param_add 5` return blank but show the same help? | blank | `param_add` | Candidate predictions held; appearance did not distinguish the malformed form |
| Does `constant 37ms` return `37ms` and show `constant` help? | `37ms` | `constant` | Candidate predictions held |
| Does `constant 37MS` return blank but show the same help? | blank | `constant` | Candidate predictions held; appearance did not distinguish the suffix case |
| Do controls `zzh4_editor_a` and `zzh4_editor_b` show no help? | Both `error:-2147467259` | Both showed `zoom` help | **Prediction did not hold** |
| Does contrast `constant 37` return `37` and show `constant` help? | `37` | `constant` | Contrast prediction held |

The frozen suite retains the failed control prediction. The joined report therefore marks
each combined prediction as not held, while reporting the runtime and candidate-help
predictions separately. This observation does not establish acceptance, token boundaries,
or a general unknown-token fallback algorithm. It constrains only the displayed help for
these exact scripts. The matching corpus still needs a token-span or guard-hint observable.

### Screenshot-backed help repeat (2026-09-17, build 9598)

The same frozen predictions were rerun in `parser_editor_help` through
`tools/probe_arg_forms.py`, with a new
[HTTP capture](../tests/runtime-grammar-editor-help-http-2026-09-17-9598.json) and
[UI capture](../tests/runtime-grammar-editor-help-ui-2026-09-17-9598.json).
Every UI row links to an unmodified screenshot under
`tests/runtime-grammar-editor-ui-2026-09-17/` and its SHA-256. The original action,
restored action, and reopened restoration each have a screenshot too. These are
new observations; the historical screenshots remain unrecoverable.

```sh
just runtime-grammar-editor --http tests/runtime-grammar-editor-help-http-2026-09-17-9598.json --ui tests/runtime-grammar-editor-help-ui-2026-09-17-9598.json
```

The candidate HTTP and help predictions above held again in this fixture, in
forward and reverse UI order. The nonsense-control prediction failed again:
both controls displayed `zoom` help. Both UI passes used one editor opening;
afterward the original action and button name were restored, verified by reopening,
and the editor closed. No candidate was executed through the editor. This repairs
inspectability for this repeat, not the remaining token-span or guard-hint gap.
The comparison tool checks screenshot existence and hashes when a capture says
its images were persisted, so a missing image cannot silently retain that status.

### Empty quoted operands with an omission contrast (2026-09-17)

The [frozen suite](../tests/runtime-grammar-quote-consumer-cases.json) asks whether
empty quoted operands alter `param_equal` results relative to explicit omission.
The [live capture](../tests/runtime-grammar-quote-consumer-9598.json), build 9598,
uses `parser_constants`, both quote styles, two marker/value baselines, repeated
reads, and forward/reverse query passes. Only the query endpoint was used.

```sh
just probe-arg-forms --grammar-cases tests/runtime-grammar-quote-consumer-cases.json --repeat 2 --rounds 2 --out /tmp/quote-consumer.json
just runtime-grammar --artifact tests/runtime-grammar-quote-consumer-9598.json --get quote-consumer-first-single-empty-first
```

| Frozen question, single-quote first baseline | Observed candidate / contrast on build 9598 | Result |
| --- | --- | --- |
| Does `param_equal '' '' ? constant 37 : constant 83` select `37`, unlike an empty/nonempty pair? | `37` / `83` | Prediction held and separated from both unequal-string controls |
| Does `param_equal '' 'H4Q' 'H4Q' ? constant 37 : constant 83` differ from omitting the first empty operand? | `83` / `37` | Prediction held; omission contrast discriminated |
| Does `param_equal 'H4Q' '' 'H4Q' ? constant 37 : constant 83` differ from omitting the second empty operand? | `83` / `37` | Prediction held; omission contrast discriminated |

The double-quote counterparts and the second `H4R` / `53` / `91` baseline also
matched their frozen predictions. The positional cases returned the same value as
the unequal-string controls, and the standard report retains `matches-controls`.
Those controls are quoted nonsense **values**, not presumed unrecognized syntax;
they cannot by themselves establish argument recognition. The explicit omission
contrast supplies the positional distinction. This is an exact `param_equal`
consumer observation, not a universal claim that every action preserves empty
arguments. Unmatched quotes remain a separate obligation.

The [same-length follow-up suite](../tests/runtime-grammar-quote-consumer-arity-cases.json)
tests the alternative explanation that three arguments always select the unequal
branch. In its [build-9598 capture](../tests/runtime-grammar-quote-consumer-arity-9598.json),
`param_equal 'H4Q' 'H4Q' 'H4Q' ? constant 37 : constant 83` returned `37`,
while replacing the middle operand with `''` returned `83`. Moving the empty
operand from first to third likewise changed `83` to `37` without changing the
argument count. These frozen predictions held with both quote styles and both
marker/value baselines, and each candidate separated from its nonsense-value
controls. This discriminates the argument-count explanation in these exact tests.
An [initial arity capture](../tests/runtime-grammar-quote-consumer-arity-initial-9598.json)
is retained separately because its scope text incorrectly called the same-length
contrast an omission contrast; the corrected suite was rerun with unchanged scripts
and expectations. No earlier capture was overwritten.

### Unmatched quotes with a chain observable (2026-09-17)

The [frozen suite](../tests/runtime-grammar-unmatched-quote-cases.json) asks what
happens to a following addition when a quote after a numeric prefix is unmatched.
It ran through the existing argument prober in `parser_constants`; the
[build-9598 capture](../tests/runtime-grammar-unmatched-quote-9598.json) retains both
quote styles, both numeric baselines, repeated reads and forward/reverse passes.

| Frozen question, first single-quote baseline | Observed output | Matching-quote contrast / nonsense-value controls | Verdict |
| --- | --- | --- | --- |
| Does `constant 37 ' & param_add 5` retain `37`? | `37` | `42` | Held and separated |
| Does `constant 37 'H4Q & param_add 5` retain `37`? | `37` | `42` | Held and separated |
| Does `constant 37 'H4Q" & param_add 5` also retain `37`? | `37` | `42` | Held and separated |
| Does `constant 37 'H4Q & param_add 5' & param_add 10` return `47`, rather than applying the inner addition too? | `47` | `42` | Held and separated |

All corresponding double-quote and second-baseline predictions held. The exact
matching-quote contrast was `constant 37 'H4Q' & param_add 5` in the first baseline;
controls replaced the quoted contents with each nonsense value. This measures
preservation of the numeric prefix and the observable effect of the following
chain. It does not expose an internal cursor, prove an argument representation,
or establish the same fallback for every consumer. Earlier unmatched-first-argument
`get_text` observations remain separate evidence.

```sh
just runtime-grammar --artifact tests/runtime-grammar-unmatched-quote-9598.json --group unmatched-quote-chain
```

### Backtick evidence routed by consumer (2026-09-17)

The audit previously attached the whole backtick case group to
`IAction::getParamEval`. That association was too broad. The b9246 bounded bodies
contain distinct call paths: `constant` calls `getParam`; `get_text` calls
`actionGetText`, which creates an action and calls `queryText`; `param_add` calls
`IParamValuesAction::getValues(SActionParam*, SActionParam*)`, which has its own
creation/query path. These are Tier-2 call-site observations, not a live instruction
trace or a claim that every branch was exercised.

`just runtime-grammar --audit` now selects exact case IDs for these consumers and
checks each recorded direct edge against both the captured manifest and hashed
assembly. Literal, interpolation, numeric and lexical-negative results stay separate.
At that review, the generic `getParamEval` and `getFloatParamEval` rows had no
attached live result. The setting fixture below subsequently adds an identified
caller and discriminating results for `getParamEval`; the float helper remains open. Their empty
evidence lists must not be filled merely because some other verb evaluated a
backtick expression. Cache-hit behavior and conversion branches also require their
own observable before any completeness claim.

### Generic evaluated-parameter caller and setting fixture (2026-09-17)

The [route capture](../tests/runtime-parser-branch-routes.json) now includes an
`evaluation_callers` section. The extractor scans x86_64 direct relative calls/jumps
to the generic evaluation helpers and checks each candidate in a function body
bounded by `LC_FUNCTION_STARTS`. Caller assembly and hashes are retained. This is
Tier-2 evidence: it excludes indirect callers and inlined copies and does not claim
that an observed live query executed an instruction from this older binary.

`ACTION_setting::onQuery` contains the call to `getParamEval` at `0x10050c448` in
b9246. The named `parser_setting_eval` fixture uses the existing
`videoRandomTransition` setting while it reads `yes`, compares equal to literal
`on`, and unequal to literal `off`. It aborts if these preconditions differ and
never changes a setting, loads media, or calls the execute endpoint. The audit
checks the caller anchor and links the new exact query results, rather than
borrowing observations from the separate `param_add` or `get_text` readers.

The frozen [initial suite](../tests/runtime-grammar-setting-eval-cases.json),
[true-value discrimination suite](../tests/runtime-grammar-setting-eval-discrimination-cases.json),
and [literal/type follow-up](../tests/runtime-grammar-setting-eval-types-cases.json)
ran through `tools/probe_arg_forms.py` with repeated reads and forward/reverse passes.
Their build-9598 captures are [initial](../tests/runtime-grammar-setting-eval-9598.json),
[discrimination](../tests/runtime-grammar-setting-eval-discrimination-9598.json), and
[types](../tests/runtime-grammar-setting-eval-types-9598.json).

| Frozen question in `parser_setting_eval` | Observed build-9598 result | Verdict and limit |
| --- | --- | --- |
| Do bare and outer-quoted computed `off` arguments compare unequal? | `no`; failed-expression controls read `yes` | Held and separated |
| Does outer-quoted `` '`off' `` compare unequal without its final backtick? | `no` | Held and separated |
| Does outer-quoted `` ' `on`' `` with a leading space compare unequal? | `no` | Held; exact consumer output, not a universal whitespace rule |
| Does computed `param_equal 37 37` compare equal, unlike plain nonsense text and computed `param_equal 37 83`? | `yes` versus `no` | Held and separated |
| Does outer-quoted `` '`param_equal 53 53' `` also compare equal without its final backtick? | `yes` versus `no` | Held and separated |
| Do computed numeric `1` and computed text `"on"` compare equal? | Both `no` | **Predictions did not hold**; both matched plain nonsense-text controls |
| Do literal `1` and literal quoted `'on'` likewise compare unequal? | Both `no` | Follow-up predictions held and separated from failed-expression controls |
| Do computed `constant on` / `constant off` compare equal / unequal? | `yes` / `no` | Follow-up predictions held and separated |

The initial computed-true row also read `yes` against `yes` failed-expression
controls; it remains `matches-controls`. The later true-comparison and type controls
supply the distinction. No expectation was rewritten to turn a failure into a pass.
The setting still read `yes` after the runs, and fixture assertions were checked
at the start of each pass and at completion. These results concern this setting
comparison only; they do not prove all settings coerce values alike or prove
persistent compiled-action cache reuse.

For `getFloatParamEval`, verified direct callers include Pioneer display browser/
cuepoint readers and `wait` / `repeat_start`. Those are fixture leads only. No live
float-evaluator result is attached yet; selecting a bounded query observable remains
preferable to introducing asynchronous timing mutations.

```sh
just runtime-grammar --artifact tests/runtime-grammar-setting-eval-discrimination-9598.json --group setting-eval-discrimination
just runtime-grammar --audit
```

## What remains

Completion review, 2026-09-17: the historical package and bounded parser bodies are
captured, the queued indirect-call frontier is resolved, and the ordinary parser has
broad live coverage. Delimiters, numeric/unit forms, quoting, keyword/fallback forms,
representative typed consumers, deck scopes and variable isolation have named-fixture
captures. Empty quoted operands now have omission and same-length controls. These
results do not yet establish exhaustive branch coverage or a complete editor comparison.

The remaining completion obligations are:

- **Audit runtime branches and conversion paths.** Use `just runtime-grammar --audit`
  to join each reviewed path to its actual query, execute or lifecycle observable.
  The unmatched-quote chain discriminator is now captured; review backtick
  evaluation/conversion branches; preserve failed predictions and readings that match controls. A mapped
  function or branch family is not proof that every edge was measured.
- **Complete the Button Editor comparison.** The frozen `editor_corpus` in
  `tests/runtime-grammar-obligations.json` still needs screenshot-backed token-span
  or guard-hint observations. Help-display repeats now have durable screenshots,
  but do not substitute for those observables. Coordinate-based observation is
  blocked pending a verified targeting method that preserves the active dialog.
- **Measure the alternate remote entry.** Establish `parser_remote_mode` independently,
  record a restoration procedure, and test the checked-head bypass versus source-text
  wrapper predictions. A Remote-protocol subscription or ordinary HTTP response
  alone does not establish `IAction::isRemote`.
- **Resolve scope and reconcile the final specification.** Determine whether
  `IAction::getListParam` is actually reached from the recovered paths; absence of
  direct references does not prove it is unused. Then ensure every in-scope proposed
  rule links to a discriminating live result or an explicit unresolved status, and
  distinguish b9246 structural leads from b9598 behavior. Do not expand H4 into every
  action implementation, every mixer configuration or every deck-selection policy.

There is no defensible completion percentage until the runtime branch audit has a
closed denominator. Editor targeting and remote-mode establishment are the principal
fixture blockers; the remaining read-only tests and evidence joins can proceed.

The [failed editor calibration](../tests/runtime-grammar-editor-spans-calibration-aborted-9598.json)
records a cropped-dialog click reaching a cue pad behind the editor. Deck 1 was
paused and independently read back as stopped; its exact prior position was not
recorded and was not restored. Do not repeat that coordinate method. Capture
playback/position baselines before any future UI calibration. Keyboard-only help
observations remain a separate demonstrated method.

For future agents, start with `just runtime-grammar --audit`, then retrieve the exact
case through `just runtime-grammar --artifact <capture> --get <case>`. This avoids
re-reading the full assembly or treating completed fixture work as an open task.
Keep runtime output, consumer semantics, lifecycle behavior and editor appearance
as separate predictions.

### Floating evaluator: binary HTTP comparisons (2026-09-17)

The b9246 structural lead now includes a bounded, hashed `get_pioneer_display`
query entry body and its jump to `getCuepoints`, whose call at `0x1006695b6`
targets `IAction::getFloatParamEval`. This is a recovered route, not an observed
instruction trace. The audit joins this route to the following frozen questions.

[Literal calibration](../tests/runtime-grammar-display-float-calibration-9598.json)
recorded distinct, repeatable binary bodies for literal 0, 1 and 2 before candidate
predictions were frozen. `parser_display_float` asserts deck 3 exists, is empty
and is stopped; it performs no setup writes. Current implicit controller/mapping
context was retained, with no independently identified Pioneer hardware.

Run the [frozen suite](../tests/runtime-grammar-display-float-cases.json) through
`tools/probe_arg_forms.py --grammar-cases tests/runtime-grammar-display-float-cases.json
--repeat 3 --rounds 2 --out <new-capture-path>`. Its per-case `response_encoding: hex`
preserves every HTTP body byte, including NUL and invalid UTF-8. Candidate and
literal frames must agree exactly; changed literal oracles invalidate the result.

The [first run](../tests/runtime-grammar-display-float-9598.json) and
[independent repeat](../tests/runtime-grammar-display-float-confirmation-9598.json)
on build 18.0.9598 each recorded 10 held predictions and one failed prediction:

| Frozen question, in `parser_display_float` | Both captures |
| --- | --- |
| Do computed integer 2, float 2.0, 200%, and 2ms match the literal-2 frame? | Held; separated from both controls. |
| Do single/double outer quotes, or an outer-quoted missing final backtick, retain the literal-2 frame? | Held; separated from both controls. |
| Does computed `on` match the literal-1 frame? | Held; separated from both controls. |
| Does computed text `"2"` match the literal-2 frame? | Prediction failed; matched the zero frame and controls. |
| Does leading space inside the outer quote match the zero frame? | Held, but matched controls; not positive recognition evidence. |
| Does computed signed `+2` match literal 2 with the consumer's zero input? | Held; separated, but cannot distinguish relative addition from absolute conversion. |

These questions concern exact returned frames in this consumer and fixture.
Physical rendering, compiled-action cache reuse, nonzero relative input, and
universal coercion rules remain unmeasured. For future binary-valued probes,
reuse the prober's hex mode rather than comparing replacement-decoded text.

### Floating conversion follow-up (2026-09-17)

The separately frozen [conversion questions](../tests/runtime-grammar-display-conversions-cases.json)
reuse `parser_display_float` and the pre-candidate binary literal calibration.
Generate/check with `tools/build_runtime_display_float_cases.py --conversions --check`;
run through the same argument prober with this suite path and a new output path.
The [first capture](../tests/runtime-grammar-display-conversions-9598.json) and
[independent repeat](../tests/runtime-grammar-display-conversions-confirmation-9598.json)
on build 18.0.9598 each recorded 13 held predictions and two failed predictions:

| Frozen question | Both captures in `parser_display_float` |
| --- | --- |
| Do direct `2.0`, `200%`, `2ms`, `2bt`, and computed `constant 2bt` match literal 2? | Held and separated from both controls. |
| Does direct `on` match literal 1? | Held and separated. |
| Do quoted direct text `2`, computed text `2`, omission, computed empty constant, and computed `off` match literal 0? | Held but matched both controls; no recognition evidence. The earlier computed-text-to-2 prediction remains a preserved failure. |
| Does the longer expression `constant 2 & param_add 0 & param_add 0` match literal 2, with a normal backtick pair or with an outer quote and no final backtick? | Both predictions held and separated. This does not prove a particular string-storage branch executed. |
| Does preceding the omitted-operand display query with `constant 1 &` or `constant 2 &` supply the missing operand and return its literal frame? | Both predictions failed: exact HTTP bodies were ASCII `1` and `2` respectively. These scripts do not establish traversal of the helper's inherited-parameter path. |

No setup or restoration writes were required. Zero-frame equality remains unable
to distinguish a recognized zero from a failed evaluation in this consumer.

### Arithmetic reader: operand-position comparisons (2026-09-17)

The [frozen arithmetic suite](../tests/runtime-grammar-math-reader-cases.json) asks
separate questions of both operand positions, using `(37, 5)` and `(53, 9)` inside
`parser_constants`. Same-arity nonsense controls replace only the operand under test.
The b9246 route is `param_add` → the `SActionParam*` overload of
`IParamValuesAction::getValues`; text concatenation and numeric conversion have
separately captured caller edges. This is not the generic `getParamEval` route.

The [first run](../tests/runtime-grammar-math-reader-9598.json) and
[independent repeat](../tests/runtime-grammar-math-reader-confirmation-9598.json)
on build 18.0.9598 each recorded 36 held predictions and eight failed predictions.
Twelve held predictions matched controls and do not establish recognition.

| Frozen question, tested at both operand positions and both value pairs | Both captures |
| --- | --- |
| Does quoted action text without backticks contribute its numeric value? | Held; sums were `42` and `62`, separated from controls. |
| Do paired backticks and longer expressions, with or without backticks, contribute their computed value? | Held and separated. No storage or cache branch execution is inferred. |
| Does computed numeric text concatenate second operand then first, rather than add? | Held and separated: `537` and `953`. This is an exact `param_add` result, not a universal text-conversion rule. |
| Do direct beat operands contribute their magnitudes? | Prediction failed; every direct-beat case returned `error:1`. |
| Do computed beat operands contribute their magnitudes? | Held and separated; sums were `42` and `62`. |
| Does action text with only a trailing backtick retain its numeric contribution? | Prediction failed; the other operand alone was returned, matching controls. |
| Do missing final backticks, leading space before paired backticks, and quoted numeric text contribute zero? | Held but matched controls; internal failure, null and fallback paths remain indistinguishable. |

Reproduce through `tools/probe_arg_forms.py --grammar-cases
 tests/runtime-grammar-math-reader-cases.json --repeat 3 --rounds 2 --out <new-path>`;
check the frozen questions with `tools/build_runtime_math_reader_cases.py --check`.
These are query results with no state mutations. Incoming-parameter behavior,
compiled-action reuse, and other arithmetic verbs remain outside this capture.

### Text interpolation: boundary and formatting questions (2026-09-17)

The [frozen text-reader suite](../tests/runtime-grammar-text-reader-cases.json) uses
`get_text` with literal `A`/`B` sentinels in `parser_constants`. Both nonsense controls
are otherwise matching interpolations and return the sentinels alone. The structural
route remains `get_text` → `actionGetText` → nested create/queryText; it is not an
observation of the generic parameter evaluator or a skin render.

The [first capture](../tests/runtime-grammar-text-reader-9598.json) and
[independent repeat](../tests/runtime-grammar-text-reader-confirmation-9598.json)
on build 18.0.9598 each recorded 20 held predictions and two failed predictions.
Three held predictions matched controls and remain non-discriminating.

| Frozen question in `parser_constants` | Both captures |
| --- | --- |
| Does an unmatched backtick remain literal with the rest of the string? | Held and separated: `A` followed by the unmatched backtick and `constant 37 B`. |
| Do adjacent and separated interpolations preserve the predicted order and intervening text? | Held and separated: `A375B` and `A37C5B`. |
| Do leading/trailing spaces within an expression retain the integer result? | Held and separated: `A37B`. |
| Do empty pairs around action-looking text leave that text literal? | Held and separated: `Aconstant 37B`. |
| Do a single empty pair, an unknown expression, and an empty result leave only `AB`? | Held but matched controls; no recognition evidence. |
| Do true/false expressions insert `on`/`off`? | Held and separated: `AonB` and `AoffB`. |
| Does fractional `0.37` insert `37%`? | Prediction failed: `A0.37B`. |
| Does `37%` insert percentage text? | Held and separated: `A37%B`. |
| Does a beat value insert nothing? | Prediction failed: `A37 btB`. |
| Do backslash-n, backslash-t, decimal `\65`, doubled backslash and doubled percent produce the predicted characters? | Held and separated: CRLF, tab, `A`, one backslash and one percent respectively, between the sentinels. |
| Does backslash before a backtick remain literal while the expression evaluates? | Held and separated: `A\37B`. |
| Does unknown `\q` remain literal? | Held and separated: `A\qB`. |

These are exact HTTP observations of this text consumer. Do not turn them into
outer-argument escape rules or infer an internal result tag from the rendered text.
The failed formatting predictions do not distinguish a changed build from a
conversion inside `queryText`; the b9246 assembly is only the structural lead.
Legacy metadata placeholders and skin-specific cache contexts are not covered.
Reproduce through the existing argument prober using this suite path, `--repeat 3
--rounds 2`, and a new output path; check the suite with
`tools/build_runtime_text_reader_cases.py --check`.
