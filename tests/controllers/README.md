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
