# Argument type probe

Local test, 2026-09-24, VirtualDJ 18.0.9644 arm64; HTTP execute/query, empty
stopped decks, with debug output observed in the running desktop application.

**Debug exposes argument types, units and a relative flag. These help construct
consumer-specific tests; they do not independently validate another verb's arguments.**
The first target was `set`, with independent `get_var` readback. Its bundled
catalog description explicitly supports a numeric value or a quoted source-variable
name. This run used the supported HTTP channel, not native plugin HRESULTs.

## Results

The target started at `0.12` before every case. The source variable held `0.37`.
The [values capture](../tests/argument-types-9644/values.json) and
[request journal](../tests/argument-types-9644/values.jsonl) retain two rounds in
opposite orders, with identical results. Debug labels are independently transcribed
from the [first screenshot](../tests/argument-types-9644/debug1.png),
[second screenshot](../tests/argument-types-9644/debug2.png), and
[completed second batch](../tests/argument-types-9644/debug2-confirmation.png).
The second screenshot supplies the trailing source-variable result absent from the
first screenshot; the confirmation supplies the trailing time result. Immediate
absence from a partial debug log is not scored as failure.

| Argument | Observed direct `debug` output | `get_var` after `set` |
| --- | --- | --- |
| `1` | `Int: 1` | `1` |
| `0.5` | `Val: 0.50` | `0.5` |
| `50%` | `Percent: 50.00%` | `50%` |
| `'0.5'` | `Text: 0.5` | blank |
| `'$argtype_source_9644'` | `Text: $argtype_source_9644` | `0.37` |
| `'zzargalpha'` | `Text: zzargalpha` | blank |
| `'zzargbeta'` | `Text: zzargbeta` | blank |
| omitted | `No param` | `1` |
| `+0.5` | `Val: 0.50 (relative)` | `0.62` |
| `500ms` | `Time: 500.00ms` | `500ms` |

This discriminates absolute from relative numbers, and ordinary numeric rendering
from percentage/time rendering. It also confirms a text argument can have useful
meaning for `set`: the prepared variable name copies its value. Quoted numeric text
and the nonsense controls read blank; this alone does not identify rejection,
missing-variable lookup, or stored text. Every execute response was `true`, so that
response alone did not discriminate the cases.

The debug calls inspect their own explicit argument. They do not peek at `set`'s
internal parameter or prove all verbs share its conversions. The numeric source was
restored before the separate debug batches; those batches observe the literal name
as text, not the source value. No general accepted-type schema is claimed.

## Second consumer: param_multiply

Local test, 2026-09-24, same build and empty/stopped-deck context. The bundled
catalog documents two explicit operands, each a value or action. The
[base capture](../tests/argument-types-multiply-9644/values.json) and
[expanded capture](../tests/argument-types-multiply-9644/values-expanded.json)
retain two opposite-order rounds each. The expanded capture adds zero and valid
action-valued controls. Each execute case resets the target to `0.12` and runs:

```text
param_multiply 0.8 <argument> & set '$argtype_target_9644'
```

A separate query tests `param_multiply 0.8 <argument>`. A separate execute batch
replaces the final `set` with bare `debug`, which **does display the incoming
calculated parameter** on this path. The [UI observations and screenshot hashes](../tests/argument-types-multiply-9644/debug-observations.json)
join each case to its retained screenshot and exact request journal.

| Second operand | Query result | Stored result | Output from chained debug |
| --- | --- | --- | --- |
| `1` | `0.8` | `0.8` | `Val: 0.80` |
| `0.5` | `0.4` | `0.4` | `Val: 0.40` |
| `50%` | `40%` | `40%` | `Percent: 40.00%` |
| `+0.5` | `0.4` | `0.4` | `Val: 0.40` (no relative suffix) |
| `500ms` | `400ms` | `400ms` | `Time: 400.00ms` |
| `'0.5'` | `0` | `0` | `Val: 0.00` |
| `'$argtype_source_9644'` | `0` | `0` | `Val: 0.00` |
| `'zzargalpha'`, `'zzargbeta'` | `0` | `0` | `Val: 0.00` |
| omitted | `error:1` | `1` | `No param` |
| `0` | `0` | `0` | `Val: 0.00` |
| `'constant 0.5'` | `0.4` | `0.4` | `Val: 0.40` |
| `` `constant 0.5` `` | `0.4` | `0.4` | `Val: 0.40` |

The prepared source variable held `0.37` during both numeric sweeps. Its quoted
name alone did not reproduce `set`'s copy behavior. In contrast, quoted and
backtick-wrapped `constant 0.5` both produced the expected product. Therefore text
arguments cannot all be rejected based on a direct-debug Text label: what the
consumer does with the text matters.

Zero is not an invalid-argument verdict: the valid literal zero and both nonsense
controls produce the same numeric result and output type. The missing operand is
also a trap: the stored `1` matches bare `set`'s default from the first experiment;
the `No param` debug output supports interpreting it as absence of an incoming
calculated value, not a product of one. These comparisons establish bounded
behavior, not an internal parser rejection reason or a universal type schema.

The relative flag on the second operand was not present in this operation's
observed output. This does not establish the behavior of relative first operands
or other arithmetic verbs. Both numeric runs restored the temporary variables to
zero and verified unchanged deck state. Native plugin HRESULTs were not measured.

## Query-to-parameter bridge: loaded versus empty deck

A subsequent [genre-query probe](../tests/query-cast-debug-9644/README.md) on build
18.0.9644 reproduced the user's distinction with explicit deck scopes. On loaded
deck 1, `get_genre & debug` produced `No param`, while adding bare `param_cast`
produced text. The typo `getgenre` and nonsense `zzcastalpha` produced `No param`
even with the cast. On empty deck 2, the valid query and both controls all produced
`No param`. Opposite-order passes agreed; exact scripts, state, and debug screenshots
are retained. No load/unload operation was performed.

This demonstrates a state-dependent query-value probe, not a universal statement
validator. Absence of an incoming parameter can mean missing query data, and direct
`query & debug` can miss a value that the cast-mediated chain exposes.

## Cast argument variants

The [param_cast matrix](../tests/param-cast-types-9644/README.md) tests numeric and
text synthetic sources on build 18.0.9644, through both HTTP query and execute/debug,
in opposite-order passes. Named conversions can be distinguished by their output
types, values and relative flag. But bare and nonsense cast names preserve a value
through execute while failing with E_INVALIDARG through query. Formatting and text
length also differ by source type and channel. Therefore neither query acceptance
nor parameter presence alone defines execute argument validity. The linked matrix
retains exact scripts, results, UI screenshots, and unresolved comparisons.

## Reproduce

```sh
just doctor
just argument-types
just argument-types --phase values --output /tmp/argument-values-new.json
just argument-types --check /tmp/argument-values-new.json
just argument-types --phase debug1 --output /tmp/argument-debug1-new.json
# Retain the completed debug window before sending the next batch.
just argument-types --phase debug2 --output /tmp/argument-debug2-new.json
```

The default prints the fixed cases without executing. The runner refuses existing
capture paths, requires build 9644 and empty stopped decks, journals before each
request, and never automatically retries uncertain writes. Temporary variables are
required to start unset or zero to avoid lossy restoration through formatted readback,
then restored and read back; an initially unset variable becomes zero rather than being
deleted. Deck states are checked again afterward. Leave the debug window open.

The [initial capture](../tests/argument-types-9644/values-initial.json) stopped during
calibration because `get_var` rendered `0.375` as `0.38`. Cleanup passed. The completed
run instead uses exact two-decimal fixture values and retains the aborted journal.
This is a display-precision observation, not evidence that storage was rounded.

For the second consumer, add `--consumer multiply`. Its plan includes the extra
controls, and `--phase debug3` captures their calculated output types. The saved
expanded capture is checked by `just check`.

Next: compare argument positions or another consumer with the same controls. Native HRESULTs can add evidence on query-capable
consumers, but a query HRESULT is not proof that an execute argument was consumed.
