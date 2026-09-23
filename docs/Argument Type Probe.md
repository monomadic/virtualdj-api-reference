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

Next: apply the same labelled-type/independent-result pairing to another selected
consumer and argument position. Native HRESULTs can add evidence on query-capable
consumers, but a query HRESULT is not proof that an execute argument was consumed.
