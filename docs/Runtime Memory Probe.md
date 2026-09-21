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
- Prefer `just vdj-query "get_effect_title 'VDJMemoryProbe'"` after the app has
  discovered the installed plugin. On build 18.0.9644 this loaded the plugin and
  captured from `OnLoad` without selecting an effect slot or activating it.
  Alternatively load **VDJMemoryProbe** into an inactive effect slot and restore
  that selection afterward. Cached title queries may not invoke `OnLoad` again.
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

## Live result — 2026-09-21, build 18.0.9644, arm64

[Verified capture](../tests/plugin-memory-9644.json) and
[HTTP run record](../tests/plugin-memory-run-9644.json): a read-only title query
loaded the plugin. The mapped image UUID, build, unslid table address and every
name/id/flags record matched the fresh same-build disk extraction. This directly
establishes that the plugin could read these host memory regions. It recovered
no additional verb names relative to that disk extraction. Query `verification.records`
in the capture for the measured total.

All public callback addresses landed inside the host executable. The
[bounded callback trace](../tests/plugin-memory-callbacks-9644.json) records their
numeric/text entry points and one direct-call level, with exact LC_FUNCTION_STARTS
bounds and code hashes. This trace is **Tier 2 disk analysis rooted in live-located
addresses**, not observation of a private parser call executing.

On this build, both query callbacks pass the script pointer to `0x10057d5f8`
with two zero arguments, test the returned pointer, call `0x10058029c`, and then
use separate numeric/text routines. Both later decrement a field at returned-object
`+8`, conditionally invoking a virtual method at vtable `+8`. **Inference:** this
is a shared parser/factory followed by context setup, evaluation and release;
the decrement means an object may be destroyed before the public callback returns.
The exact private ABI and lifetime are not established. Do not call these addresses
or read a guessed object layout based on this trace.

Reproduce the structural trace with an optional isolated capstone environment:

```sh
uv run --with capstone --python .venv/bin/python3 python tools/plugin_memory_trace.py \
  tests/plugin-memory-9644.json --output /tmp/plugin-memory-callbacks.json
```

For this run, Apple's `llvm-objdump` Mach-O disassembly ignored the requested
address bounds and began at the start of `__text`. Use the bounded helper above
instead; it decodes only exact selected function intervals and caps routine size.
The base environment did not have capstone, so this optional command supplies it
without changing the project's dependency set.

The next discriminating experiment is to follow the current-build GetInfo callback
to its parser boundary and inspect one known-valid tail against nonsense controls.
Old x86_64 parser addresses must not be reused in the current arm64 host. Private
object layouts and ownership have to be recovered before any inspection or call;
this first probe deliberately does not guess them. If that boundary cannot be
observed safely, keep the parser-object experiment unresolved and use the existing
native HRESULT and prepared-state probes.

For agents: use the small verified JSON artifact and the commands above. Do not
read raw process dumps or create a second Markdown list of verb records.
