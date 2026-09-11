# Controller archive and live MIDI fixture

The reader and format report are in
[Compiled Controller Definitions](../../docs/Compiled%20Controller%20Definitions.md).
The generated manifest and schema inventory live one directory above this one.

## Fixture

`SIMPLE_MIDI-definition.xml` declares a channel-zero note button and CC slider, bound to
`SIMPLE_MIDI_0_0`. It matches only the virtual port `Codex Definition Probe`.
`SIMPLE_MIDI-mapper.xml` maps those named controls to isolated numeric test globals.
`midi_probe.swift` creates temporary paired CoreMIDI endpoints. It opens no physical
hardware ports. Type three hexadecimal bytes per line; `quit` disposes the endpoints.

```sh
swiftc -module-cache-path /tmp/vdj-midi-module-cache tests/controllers/midi_probe.swift -o /tmp/vdj-midi-probe
/tmp/vdj-midi-probe
```

The installed test filenames are `Devices/Codex SIMPLE_MIDI Definition Probe.xml` and
`Mappers/SIMPLE_MIDI_0_0 - Codex Definition Probe.xml` under VirtualDJ's user home.
Use exclusive creation; never overwrite another file. Load the definition by restarting
an idle app, select the test mapping, then send `90 24 7f` and query
`get_var '$codex_device_button'`. The intended sentinel is `37`. Send `b0 10 20` and
`b0 10 60`, with independent reads of `get_var '$codex_device_slider'`. Neighboring note/CC
numbers and another MIDI channel provide negative controls. ONINIT alone proves only
mapper loading, not definition binding.

`live-http.json` records exact timestamped HTTP probes for the current test session.
It is a run log, not a reusable script that blindly restores old state. The final run
interpretation and cleanup state must be read alongside it.

## Observed result — 2026-09-12, bundle 18.0.9598

**Pass for this custom MIDI definition and paired mapper.** The Controllers tile and New
Device Detected dialog displayed the fixture description after restart. HTTP independently
read the mapper ONINIT sentinel `9598`. The HTTP listener subsequently became unavailable;
MIDI behavior was therefore read from the running app's `var_list` window instead.

Use `SIMPLE_MIDI-mapper-var-list.xml` for that readback variant. Its button action increments
the isolated counter and opens the variable window; filter `codex_device` and enable Auto
Update. Close the variable window before the next positive note, then reopen/refilter.
In the observed run, wrong note/channel inputs left the counter at `38`; the correct
`90 24 7f` followed by `80 24 00` advanced it to `39`. The prior sentinel fixture explains
the nonzero starting value; it is not an assumed initial state. CC `b0 10 20` produced
`0.252`; `b0 10 60` produced `0.756`. Neighboring CC and wrong-channel controls left the
value unchanged. These are rounded GUI values, consistent with division by 127.

[Structured live evidence](live-validation.json) gives the exact fixture hashes, byte
sequences, observations and limits. The variable list is independent application-state
readback, not the send function's status. No claims are made about real hardware outputs,
HID transport or the newly recovered settings/display vocabulary.

Cleanup: the test globals were read back as zero, the original `custom mapping` selection
was restored, both temporary MIDI endpoints were disposed, and only the two installed
test files were removed. The original `DeathDisco Grave Raver v1/:skin` was restored.
Network Control HTTP was still unavailable at the last check; its restoration was requested
from the user because the UI tool could operate dialogs but failed on the main window.
This does not affect the completed GUI readback evidence.

For future runs, prefer the variable-window variant when a restart is required: Network
Control's prior availability does not guarantee an HTTP listener after relaunch. The
initial Quit in this session left a background process; it required SIGTERM before relaunch.
