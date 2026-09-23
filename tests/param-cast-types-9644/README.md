# param_cast argument types: query versus execute

Local test, 2026-09-24, VirtualDJ 18.0.9644 arm64. Fixed synthetic query inputs:
`constant 1.75` and `get_text '1.75'`. No track, variable or playback mutations.
Loaded/play states of decks 1–4 were read before and after each batch and unchanged.
The test does not rely on those decks supplying the input value.

Each case used both paths:

```text
HTTP execute: <source> & param_cast <arguments> & debug
HTTP query:   <source> & param_cast <arguments>
```

The agent inspected each execute result in the already-open debug window. The
[transcribed observations and screenshot hashes](observations.json) join to the
adjacent batch JSON/JSONL requests. Forward and reverse passes agreed for every
query string and debug observation. HTTP execute return values are transport/action
readback, not the result of the conversion; they are not scored as acceptance.

## Observed execute results

| Cast arguments | Numeric source `constant 1.75` | Text source `get_text '1.75'` |
| --- | --- | --- |
| omitted | `Val: 1.75` | `Text: 1.75` |
| `float` | `Val: 1.75` | `Val: 1.75` |
| `integer` | `Int: 2` | `Int: 2` |
| `percentage` | `Percent: 175.00%` | `Percent: 1.75%` |
| `ms` | `Time: 1.75ms` | `Time: 1.75ms` |
| `beats` | `Beats: 1.75 bt` | `Beats: 1.75 bt` |
| `boolean` | `Bool: 1` | `Bool: 0` |
| `text` | `Text: 1.75` | `Text: 1.75` |
| `int_trunc` | `Int: 1` | `Int: 1` |
| `frac` | `Val: 0.75` | `Val: 0.00` |
| `relative` | `Val: 1.75 (relative)` | `Text: 1.75` |
| `absolute` | `Val: 1.75` | `Text: 1.75` |
| `'000'` | `Val: 1.75` | `Text: 1.75` |
| `'text' 3` | `Text: 1.75` | `Text: 1.7` |
| `zzcastalpha` | `Val: 1.75` | `Text: 1.75` |
| `zzcastbeta` | `Val: 1.75` | `Text: 1.75` |

This establishes observable effects for casts that change type, value or the
relative flag against both nonsense controls. `float` needs the text source to
separate; `text` needs the numeric source. `absolute` remains undistinguished here:
the numeric source was already absolute. No relative-input test is claimed.

## Query-path differences

- Bare cast and both nonsense cast names returned `error:-2147024809` (E_INVALIDARG)
  for both sources, despite preserving a value through the execute/debug path.
- `'000'` formatted the numeric query result as `002`; the execute result remained
  `Val: 1.75`. The text source stayed `1.75` on both paths.
- `'text' 3` gave query text `1.7` from both sources; in execute, only the already-text
  source was shortened. The numeric execute source became `Text: 1.75`.
- `ms` queried as `2ms`, while debug displayed `Time: 1.75ms`. This establishes a
  difference in visible precision; it does not prove that internal storage rounded.
- Other tested query values agree with the corresponding visible execute values,
  allowing for query rendering such as `yes`/`no` versus `Bool: 1`/`Bool: 0` and the
  relative flag not being displayed by the query string.

## Implications

A successfully displayed parameter after `param_cast` is not proof of a recognized
cast name. Unrecognized names can match the bare execute behavior. Conversely, a
query E_INVALIDARG does not establish that the execute chain produces no parameter.
Record source type, cast argument, query result, execute output type/value and state
separately. This qualifies earlier build-9598 query-only vocabulary evidence; it
does not rewrite those historical measurements as execute behavior.

Input type also changes semantics: the same digits cast to percentage become 175%
from a numeric source and 1.75% from text; boolean and fractional-part results differ
too. A per-verb argument record needs the source type as well as the argument token.

## Reproduce

```sh
just doctor
python3 tools/probe_query_cast_debug.py --suite casts
python3 tools/probe_query_cast_debug.py --suite casts --batch 1 --output /tmp/cast-batch1.json
python3 tools/probe_query_cast_debug.py --check tests/param-cast-types-9644
```

Run batches 1 through 8 with fresh output paths, retaining the complete debug window
after each batch before continuing. Batches 5–8 reverse the first pass. The tool
journals intent before requests, never retries uncertain execute requests, and
refuses existing capture paths. It checks build 9644 and unchanged deck loaded/play
state. Default invocation prints the plan only. The offline checker verifies case
coverage, script joins, round agreement, state and screenshot hashes, not pixels.
