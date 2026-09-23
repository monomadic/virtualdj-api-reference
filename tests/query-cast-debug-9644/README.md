# Query-to-parameter debug probe

Local test, 2026-09-24, VirtualDJ 18.0.9644 arm64. Deck 1 was loaded and deck 2
empty. Each batch records loaded/play state for decks 1–4 before and after; those
states did not change. No tracks were loaded, unloaded, selected or played by the
probe. The debug window was already open. Track identity was not captured.

The agent sent HTTP execute requests and independently observed the desktop debug
window. [Observations](observations.json) join exact scripts to retained screenshots
and hashes. Adjacent batch JSON/JSONL files retain context and request journals.
Two passes used opposite case order. This compares different deck contexts; it is
not a same-deck unload/reload experiment.

| Script | Observed in both passes |
| --- | --- |
| `deck 1 get_genre & debug` | `No param` |
| `deck 1 get_genre & param_cast & debug` | `Text: Bass House` |
| `deck 1 getgenre & param_cast & debug` | `No param` |
| `deck 1 zzcastalpha & param_cast & debug` | `No param` |
| `deck 2 get_genre & param_cast & debug` | `No param` |
| `deck 2 getgenre & param_cast & debug` | `No param` |
| `deck 2 zzcastalpha & param_cast & debug` | `No param` |
| `deck spoon get_genre & param_cast & debug` | `No param` |

**Conclusion:** the cast-mediated chain discriminated the valid genre query from
the typo and nonsense control on the loaded deck, but not on the empty deck.
Bare debug did not receive the loaded query's value directly. `No param` is not a
universal syntax-invalid result. This does not prove that extra arguments to a
recognized verb were consumed. It does not establish internal parser mechanics.

## Reproduce

```sh
just doctor
python3 tools/probe_query_cast_debug.py
python3 tools/probe_query_cast_debug.py --batch 1 --output /tmp/query-cast-batch1.json
```

Repeat with batches 2, 3 and 4, saving the completed debug window after each batch
before sending the next. The runner requires build 9644, loaded deck 1 and empty
deck 2. It accepts only the fixed scripts, journals before each request, refuses
existing capture paths, and does not retry uncertain requests. Default invocation
prints the plan without executing. New captures need independent UI observations;
HTTP `true` is not the probe outcome.
