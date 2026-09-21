# Conditional child selection — build 18.0.9644, arm64

Local test on 2026-09-22, desktop-skin button surface. All decks were empty and
stopped before and after. This fixture tests the guarded helper interpretation in
[skin-node-helpers-9644.json](../../skin-node-helpers-9644.json).

`generate.py` creates a synthetic skin with independent rows. Each button writes
only its own `$schema_condition_N` hit flag. No transport/media action is used.
The first `pos`, `size` or `up` child has the tested attribute; the second child
has the same name and no condition. Position candidates are left/right, sizes
are narrow/wide, and drawing candidates are red/green.

## Observations

Both independently loaded rounds agreed, with phase and row click order reversed
in round two. These are reloads in the same app session, not separate app launches.
The [journal](run-9644.jsonl) retains exact HTTP requests, write intents, readbacks
and cleanup. [result-9644.json](result-9644.json) contains fixture/screenshot hashes,
click results, sampled colors and bounded conclusions.

| Case | First child | Left hit | Right hit | Drawing |
| --- | --- | --- | --- | --- |
| pos-baseline | only one position | yes | no | blue |
| pos-false-first | `condition="off"` | no | yes | blue |
| pos-true-first | `condition="on"` | yes | no | blue |
| pos-attr-control | `zzcondition="off"` | yes | no | blue |
| size-false-first | `condition="off"` | yes | yes | blue, wide |
| size-attr-control | `zzcondition="off"` | yes | no | blue, narrow |
| up-false-first | `condition="off"` | yes | no | **green** |
| up-true-first | `condition="on"` | yes | no | **red** |
| up-attr-control | `zzcondition="off"` | yes | no | **red** |

This confirms selection of the alternate `pos`, `size` and `up` child under the
false condition in this fixture. True and nonsense-attribute controls select the
first node where tested. It does not establish every condition expression,
outer-attribute precedence, dynamic reevaluation without reload or other surfaces.

## Screenshots and coordinate provenance

[Round 1](round-1.png) and [round 2](round-2.png) were captured from the live app
through `cua_repl` after loading the fixture and before that round's clicks.
They contain only the synthetic fixture. Both are 1229×768 pixels. CUA click
coordinates were x=440 (left) and x=748 (right), with row centers y=89, 159, 228,
298, 368, 437, 507, 577, 646. Round one clicked rows top-to-bottom, left then
right. Round two clicked bottom-to-top, right then left. AX state was refreshed
after each deterministic batch. The baseline and the alternate-position row
calibrate both x coordinates independently through their hit flags.

Color samples at x=440 and the drawing-row centers are `[32,192,96]` (green),
`[224,48,48]` (red), `[224,48,48]` (red) in both images. The retained screenshots
and independent hit readbacks are the evidence, not the `load_skin` return value.

## Cleanup and execution notes

The original skin and empty/stopped deck state were restored and verified. The
installed fixture was removed only after every installed byte matched the generator.
Previously unset probe variables were reset to zero, **not deleted**; their initial
blank readings were not restored. This is the existing variable-probe limitation
described in the grammar guide. No `@` persistent variable was used.

The first skin load's immediate readback still named the previous skin. A later
read and screenshot confirmed the load; the write was not retried. The runner now
polls skin readback after a single write. Between rounds the original skin was
restored, but the first variable cleanup attempted to parse a blank value as a
number and stopped. Round two then loaded the fixture; the corrected final cleanup
verified the skin/decks and zeroed the test variables. The journal retains these
steps and an explicit note; no result row was discarded.

## Reproduction

```sh
python tests/Skins/schema-condition-probe/generate.py --check
python tools/skin_condition_evidence.py --check
uv run --with pillow --python .venv/bin/python3 \
  python tools/skin_condition_evidence.py --check --pixels
```

For a new live run, install with `generate.py --install`, then invoke `run.py`
with new `--journal` and `--state` paths on **every step**. The committed journal
cannot be restarted by `begin`. Sequence: `begin`, `load --round 1`,
`arm --round 1 --side left`, CUA clicks, `read`, then the other side. Restore and
reload for round two and reverse the order. Always finish with `restore`, verify
its readback, then `generate.py --uninstall`. Do not reuse these screen coordinates
until a fresh screenshot establishes the current geometry. Use CUA for all UI
interaction; the runner performs only HTTP requests and local journaling.

For agents: `just skin-schema button --format=json` joins the compact live claim.
Do not load the full request journal unless investigating a specific observation.
