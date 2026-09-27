# Pad FX argument contract

`padfx` has effect-dependent named assignments as well as positional arguments.
The useful model is a verb grammar joined to the selected effect's control catalog,
not a finite list of literal tails. Use `just get-fx 'Echo Out'` to retrieve names,
short labels, indices and defaults; do not infer these from other effects.

## Live assignment evidence

Local test, 2026-09-27, build 9644, HTTP: deck 2 retained its loaded track and was
stopped, as were the other decks. Target effects began inactive. Each test used
an explicit final `on`, read the effect's independent sliders/buttons and display
texts, then deactivated it and restored every captured control. No audible-output,
stem-routing, query-return-contract or automatic padfx restoration claim is made.

[Capture](../tests/padfx-assignments-9644.json) records both forward and reversed
rounds with identical after-states per case. Every case restored its baseline.
The final boundary read timed out after the cases completed, so `complete` remains
false. A separate [read-only boundary capture](../tests/padfx-assignments-9644-boundary.json)
confirmed stopped/loaded states, other-deck target activation, selected slots,
BPM/pitch and all target control baselines. Both captures have adjacent request
journals. The earlier `-initial` capture records the aborted calibration: direct
HTTP slider values rounded, so the final runner scales values before readback.
That initial restoration was verified only at rounded/display precision.

All examples below are tails after `deck 2 padfx 'Echo Out'` and before final `on`,
unless another effect is named. See the capture for exact complete scripts.

| Form | Observed control result on build 9644 |
| --- | --- |
| `'Feedback:37%' 'Color:62%' 'Reverb:23%'` | Sliders 1, 3, 4 became .37, .62, .23 |
| Same values as decimal strings | Same control values |
| `'fbck:37%' 'col:62%' 'rvb:23%'` | Lowercase short labels produced the same values |
| Reordered independent assignments | Same control values |
| `'Length:2bt'` | Length display became `2 bt` |
| `'Feedback:2bt'` | Length became `2 bt`; Feedback stayed .8 |
| `'zzunknowna:37%'`, separately `'zzunknownb:37%'` | Activated effect, left controls unchanged |
| `'Feedback:zzunknowna'`, separately `zzunknownb` | Feedback became zero, rather than leaving it unchanged |
| `'Feedback:23%' 'Feedback:61%'`, then reversed | Last assignment won (.61, then .23) |
| `'Color:61%' 0.23` | Slider 3 became .61 and slider 2 became .23; named text occupied the first position |
| `0.23 'Color:61%'` | Sliders 1 and 3 became .23 and .61 |
| `'Feedback:80%' 'Length:1bt' 'Color:50%' 'Reverb:78%'` | Values .8, one beat, .5, .78 |
| Reverb: `0.4 0.1 0.3 0.4` | Values .4, .1, .3, .4 |
| Flanger: `'Tone:on'` | Tone enabled |
| Flanger: `'Tone:off'` or either nonsense value, starting enabled | Tone disabled |

Flanger's `0.5 8bt 0.5 0.5` activated with those displayed settings, but they
already matched the baseline, so this run does not independently establish each
assignment. Flanger button cases also showed small slider changes during activation
(about .000122); the capture preserves them and restoration succeeded.

`'Length:500ms'` did not discriminate from the one-beat baseline at the captured
BPM. It remains unresolved by this run; do not promote the static millisecond
branch to a confirmed conversion rule.

## Structural explanation, build 9246 — Tier 2

[Saved decompiles](../tests/ghidra-padfx-consumers-9246.json) include
`setPluginParameters`, `isActive`, `onExecute`, `getPlugin`, `stem2PluginClass`
and saved-state helpers. The setter at `0x100023390` splits colon strings and
compares the key case-insensitively with both full and short plugin control names.
This supplies a discovery route for names absent from shipped script examples.

- Ordinary named slider values use numeric conversion; `%` divides by 100.
- `bt` and `ms` take special branches through the effect's length parameter.
  A matching slider key can consequently route to length rather than that slider.
- Button values compare against `on`; other values map to false.
- Positional control indices derive from the whole argument list position.
- `getPlugin` scans for `stemfx:` before applying parameters. `solostem` and
  `mutestem` have distinct setter branches. These are not ordinary slider keys.
- Explicit final `on` takes a different lifecycle branch from implicit toggling.
  This live suite deliberately did not test the saved-state/toggle contract.

These are observations about the 9246 code, not proof that all such branches work
on 9644 or with arbitrary third-party effects. The two builds are kept separate.

## Reproduce and extend

Run `just doctor` first. Validate the saved export against independently decoded
function boundaries, original symbols and code hashes:

```sh
.venv/bin/python3 tools/verify_padfx_consumers.py \
  --app /Users/nom/src/virtualdj-api-reference-resources/VirtualDJ-9246.app
```

The persistent Ghidra project's reuse instructions are in
`/Users/nom/src/virtualdj-api-reference-resources/ghidra/README.md`.
Use `VDJTailExport.java` with `-readOnly -noanalysis`. Export address/length pairs:
`100023390 1584 1000239c0 2100 100022bd0 1020 10002323c 340 100024420 216 100024254 292 100024640 1168`.

The fixed live runner refuses existing output paths and requires stopped decks,
inactive targets, positive deck BPM and build 9644. It writes to deck 2:

```sh
.venv/bin/python3 tools/probe_padfx_assignments.py --output /tmp/padfx-new-run.json
```

Next: discriminate millisecond conversion across beat/BPM settings; independently
identify and read back the stem-scoped instance before testing the user's combined
named-assignment plus `stemfx` forms; then test implicit toggle/restoration and
`isActive` query semantics. Generalize by joining each recovered argument consumer
to its runtime vocabulary source, preserving separate structural and live evidence.
