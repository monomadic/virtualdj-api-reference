# Statement branch probe

Built and calibrated on 2026-09-24, VirtualDJ build 18.0.9644, arm64.

**This is a branch-outcome probe, not a statement validator.** The proposed
distinction was that a valid false predicate reaches the false branch, while an
invalid statement reaches neither branch. The captured HTTP tests do not support
that distinction: unknown verb names reached the false branch with both numeric
markers and `debug` messages.

## Run the automated calibration

```sh
just doctor
just statement-branches
just statement-branches --run --output /tmp/statement-branches-new.json
just statement-branches --check /tmp/statement-branches-new.json
```

The default command prints the fixed predicate list without writing to the app.
The run requires build 9644 and empty stopped decks. It tests only the reviewed
simple predicates in the tool; it does not accept arbitrary action scripts.
The execute wrapper is:

```text
<predicate> ? set '$statement_branch_probe_9644' 1 : set '$statement_branch_probe_9644' 2
```

Before every call, the marker is reset to zero and independently queried. After
execution, a separate HTTP query reads it: `TRUE_BRANCH`, `FALSE_BRANCH`,
`NO_BRANCH`, or `UNEXPECTED_MARKER`. Round two reverses test order and swaps the
numeric branch codes, preventing fixed-value or stale-marker assumptions. The
tool also records a query-only wrapper returning literal branch labels.

Intents and responses are journaled before/after each request, with no automatic
retry of uncertain writes. Final cleanup restores and verifies the marker and
deck state. An initially unset marker is left at zero, not deleted. The initial
run timed out during marker readback; it is retained under `-initial`, with
verified cleanup. The completed run uses paced requests and a longer timeout.

## Observed results

[The completed capture](../tests/statement-branches-9644.json) and
[journal](../tests/statement-branches-9644.jsonl) agree in both rounds:

| Predicate | Execute marker | Query wrapper |
| --- | --- | --- |
| `true`, `on` | true branch | true branch |
| `false`, `off` | false branch | false branch |
| `get_text 'hi'`, `get_text ''`, `get_version` | false branch | false branch |
| `gettext 'hi'`, `zzinvalidalpha`, `zzinvalidbeta` | false branch | false branch |
| `nothing`, bare `get_text` | false branch | false branch |
| `on zzinvalidalpha` | true branch | true branch |
| `get_text 'hi' zzinvalidalpha` | false branch | false branch |

These observations do not establish the cause of each false result. In particular,
the branch cannot distinguish recognized false/empty/no-value behavior from the
tested unknown names, and extra tails can survive without changing the branch.
No per-verb behavior status was promoted from this cross-verb experiment.

## The exact debug version

The reusable [pad fixture](../tests/Pads/Reference%20-%20Statement%20Branch%20Probe.xml)
contains direct popup calibration, true/false controls, valid text, a typo, two
nonsense names and an extra-tail test. Shift pads reproduce the user's exact
`<predicate> ? nothing : debug` form. It is not automatically installed, and
its button/pad results are not inferred from the HTTP run.

The compact labelled form is:

```text
<predicate> ? debug 'TRUE' : debug 'FALSE'
```

**Retraction of the conversational validity conclusion:** the user initially
reported a popup for valid `get_text 'hi'` but silence for `gettext 'hi'` on a
custom button, later also on a pad, on 9644. We treated that as a potential
recognition discriminator. However, when the HTTP probe sent uniquely labelled
debug branches, the user's [captured log](../tests/statement-debug-9644/user-captured-http-tagged.png)
showed `BP_VALID_FALSE`, `BP_TYPO_FALSE`, `BP_ALPHA_FALSE` and `BP_BETA_FALSE`,
alongside `BP_CALIBRATION`. The invalid names did reach the false debug branch.
The [capture metadata](../tests/statement-debug-9644/result.json) retains source
provenance and hashes; unrelated `Text: hi` rows are not attributed to this run.

A subsequent [exact-form retry journal](../tests/statement-debug-9644/http-retry-exact.jsonl)
and [agent-captured final log](../tests/statement-debug-9644/http-retry-exact.png)
showed `No param` between matching `R2_*_BEGIN` and `R2_*_END` labels for
each of `get_text 'hi' ? nothing : debug`,
`gettext 'hi' ? nothing : debug`, and
`zzinvalidalpha ? nothing : debug`. Thus the bare-debug form also failed to
separate the valid name from the tested unknown names over HTTP. The final log
also retained the earlier isolated `BP_ISOLATED_A_FALSE` output.

The agent initially saw only a partial log. A separate synthetic skin-button
calibration also lacked a visible popup at the instant inspected; it was stopped
and restored, not scored as invalid. The later log appearance demonstrates why
popup absence alone was an unreliable observation. The user's reported difficulty
reopening a dismissed window remains a lead, not a verified lifecycle rule.

For a manual run, keep the debug window available, use unique labels, verify
direct calibration output before and after each candidate, and retain the final
log. Do not call missing output a syntax failure until delivery/window lifecycle
and execution context are controlled. The original custom-button/pad distinction
remains unresolved; the HTTP result must not erase that surface distinction or
be advertised as a general validator.

## Next discriminating test

Repeat labelled and exact bare-debug forms through a custom button or pad, with
known-good direct debug controls interleaved and the entire final log retained.
If that still differs from HTTP, capture the custom-button/pad parsing and
execution path. Preserve raw branch outcomes; never map `NO_BRANCH` automatically
to invalid syntax, since state, channel and evaluator capability also need controls.
