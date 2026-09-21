# Runtime memory probe

A bounded first experiment in native plugin access to VirtualDJ's process memory.
The instrument is a separate passthrough effect built by the existing plugin build
script; it does not run VDJIntrospect's general probe lists.

## Scope and commands

- `just plugin-memory-test` exercises bounded reads, invalid addresses, malformed
  table candidates, and rejection of a non-VirtualDJ host.
- `python3 -m unittest discover -s tools -p test_plugin_memory.py` checks that the
  collector rejects mismatched image UUIDs, builds, records and table locations.
- `just plugin-memory-build --install` builds and installs `VDJMemoryProbe.bundle`
  in the macOS arm64 SoundEffect directory. It may require restarting VirtualDJ
  to discover a newly installed effect. Do not restart a working session without
  checking whether its loaded state can be interrupted.
- Load **VDJMemoryProbe** into an inactive effect slot. Its `OnLoad` takes the
  capture; activating audio processing is unnecessary. Restore the original slot
  selection afterward.
- Captures are new files named `memory-<pid>-<unix-time>.json` under
  `~/Library/Application Support/VirtualDJ/VDJIntrospect/`. Existing captures are
  never overwritten. A same-second duplicate load can fail to create a file.
- `just plugin-memory-check '/absolute/path/to/memory-….json' --output
  tests/plugin-memory-<build>.json` verifies a capture and saves a new artifact.
  The output path must not already exist. A verification mismatch must be
  investigated, not bypassed. A superseded capture keeps an `-initial` name.

## What is read

The plugin reads its own task with `mach_vm_read_overwrite`, which reports a failed
read rather than requiring a direct dereference of an untrusted address. Individual
reads are capped at 32 MiB. It copies the main executable's Mach-O load commands,
`__TEXT,__cstring` and `__DATA,__data`, then locates the existing sorted
`{name pointer, id, flags}` table using `hot_cue` as its anchor. All candidate name
pointers are resolved inside the copied string section. Missing, duplicate or
unsorted candidates abort the capture.

It also reads the SDK callback object's vtable pointer and its five public method
addresses. Only addresses inside an executable host segment are recorded, as
unslid addresses; other slots receive `null`. The slots follow the public
`IVdjCallbacks8` header: SendCommand, GetInfo, GetStringInfo, DeclareParameter,
GetSongBuffer. **None is invoked by this probe.** Reading a method address does
not establish its internal implementation or parser layout.

No heap sweep, arbitrary query list, audio samples, browser records, track metadata,
private function call, code patch, or debugger attachment is performed. Section
copies are temporary and never written to disk. The capture retains only the
structured verb rows and bounded technical metadata.

## Evidence and limits

The collector checks the loaded image's Mach-O UUID against the executable on disk,
checks the build and table location, compares every name/id/flags record with a
fresh extraction, and records the disk binary's SHA-256. This is a reproduction of
the same structure through a live channel, **not independent proof of verb
behaviour**, and not a claim that the entire memory image equals the disk file.

Unit tests and a successful build establish instrument readiness only. Until a
verified host capture is linked here, direct access in VirtualDJ remains unmeasured
by this instrument.

The next discriminating experiment is to follow the current-build GetInfo callback
to its parser boundary and inspect one known-valid tail against nonsense controls.
Old x86_64 parser addresses must not be reused in the current arm64 host. Private
object layouts and ownership have to be recovered before any inspection or call;
this first probe deliberately does not guess them. If that boundary cannot be
observed safely, keep the parser-object experiment unresolved and use the existing
native HRESULT and prepared-state probes.

For agents: use the small verified JSON artifact and the commands above. Do not
read raw process dumps or create a second Markdown list of verb records.
