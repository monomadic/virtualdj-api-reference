# vdj-plugin — write VirtualDJ plugins in Rust

A Rust interface to the Atomix Plugin SDK 8, built on the evidence in this
repo's [Plugin SDK.md](../docs/Plugin%20SDK.md). The SDK is a C++ class
hierarchy, so the crate's core is a hand-laid Itanium-ABI vtable layer with a
safe trait API on top — the same architecture `vst3-sys`/`nih-plug` use for
VST3.

## Status

**Live-verified 2026-09-22 on VirtualDJ 2026 (bundle `18.0.9644`, macOS 26.6.2
arm64).** The RustTremolo bundle was loaded by the real host and driven end to
end (`~/…/VirtualDJ/rust-tremolo.log` is the capture):

- `DllGetClassObject` negotiation → listed as `RustTremolo` in the effects
  catalog (`get_effect_title 'RustTremolo'` → `RustTremolo - Deck 1`).
- `OnGetPluginInfo` + `OnLoad` on `effect_select` — and from inside `OnLoad`,
  both typed query channels answered through the Rust vtable with the correct
  split: `GetStringInfo("get_version")` → `S_OK, "2026"`;
  `GetInfo("get_version")` → `E_INVALIDARG` with `0.0` written anyway, exactly
  the HRESULT-is-the-answer behavior the reference repo documents.
- `OnStart`/`OnStop` (vtable slots 8/9) via `effect_active` toggles.
- `OnProcessSamples` (slot 10) is verified against a *real compiler-generated
  vtable call* by [fakehost/fakehost.cpp](fakehost/fakehost.cpp), which
  `dlopen`s the built bundle and drives it through the actual SDK headers,
  both teardown paths included; it has not yet been observed in-host with
  audio playing (no track was played during the live session).

Two host behaviors worth knowing, observed during the live run:

- **Effect bundles load lazily.** VirtualDJ lists a new bundle in the effects
  catalog without loading it (no `OnLoad`, no auto-generated `.ini`);
  `DllGetClassObject` runs on first `effect_select`, and the host instantiated
  the plugin twice. The plugin's catalog identity is the **bundle filename**,
  not the declared `PluginName`.
- **One unexplained startup wedge.** On the very first launch after installing
  the freshly built bundle, VirtualDJ came up with its plugin layer inert —
  no Network Control HTTP listener, no plugin loads — while the app itself ran
  normally. Removing the bundle and relaunching was clean, and *reinstalling
  it and relaunching was also clean*, so the wedge did not reproduce and its
  cause is unresolved (first-seen-binary assessment is a suspect). After
  installing a new bundle, verify the HTTP interface comes back up before
  concluding anything else.

## MVP scope

| Piece | Where |
| --- | --- |
| Raw ABI (`HRESULT`, LP64 `GUID`, callback vtable, info structs, flags) | [vdj-plugin/src/sys.rs](vdj-plugin/src/sys.rs) |
| Object layout + plugin vtables (basic and DSP), panic-safe shims | [vdj-plugin/src/wrapper.rs](vdj-plugin/src/wrapper.rs) |
| Safe traits `VdjPlugin` / `DspPlugin`, `Host`, `SharedHost` | [vdj-plugin/src/lib.rs](vdj-plugin/src/lib.rs), [host.rs](vdj-plugin/src/host.rs) |
| Entry-point macros `export_basic_plugin!` / `export_dsp_plugin!` | [vdj-plugin/src/export.rs](vdj-plugin/src/export.rs) |
| Layout harness (C++ reference diffed against the Rust `#[repr(C)]` types) | [vdj-plugin/tests/layout.rs](vdj-plugin/tests/layout.rs) |
| Example: beat-synced tremolo Sound Effect | [examples/tremolo/](examples/tremolo/) |
| Bundle packaging + install | [package.sh](package.sh) |

macOS only (arm64 exercised; the layouts are Itanium-ABI shapes that hold for
x86_64 macOS too, unverified). Windows would need the MSVC vtable variants.

## Build and test

```sh
cargo test          # unit offset tests + the C++ layout harness
./package.sh tremolo           # build rust/bundle/RustTremolo.bundle
./package.sh tremolo --install # …and install; restart VirtualDJ, select "RustTremolo" in a deck's effects
```

The fake host drives a built bundle exactly as VirtualDJ does (real C++ vtable
calls, host-poked members, both destructor paths), with a hang watchdog:

```sh
SDK="$(find ../vendor -name vdjDsp8.h -print -quit)"; SDK="${SDK%/*}"
clang++ -std=c++17 -arch arm64 -O0 -g -I "$SDK" fakehost/fakehost.cpp -o target/fakehost
HOME=/tmp/fakehome target/fakehost bundle/RustTremolo.bundle
```

The harness needs the Atomix SDK headers, which are **not** in this repo (no
license grant — see [Plugin SDK.md](../docs/Plugin%20SDK.md) §Provenance). Put
them under `../vendor/` (`just fetch-sdk` at the repo root) or set
`VDJ_SDK=<dir>`; without them the harness skips and says so.

## Why the layout layer looks the way it does

Facts this code is built on, each verified in the reference repo:

- The host calls the plugin through a real C++ vtable **and writes data members
  directly** (`cb`, `hInstance`, and the DSP fields at offsets 24/28/32) — no
  setter virtuals exist. Hence the `#[repr(C)]` instance prefix in
  `wrapper.rs`.
- `IVdjPlugin8`'s virtual destructor takes **two** vtable slots on Itanium, so
  `OnParameter` is slot 5. The harness proves this from the compiler itself by
  decoding pointers-to-member-functions.
- The SDK's `GUID` uses `unsigned long Data1` → **24 bytes on LP64**, not the
  16-byte Windows GUID.
- Type negotiation: the host probes one export with a sequence of IIDs and
  stops at the first acceptance, so `CLASS_E_CLASSNOTAVAILABLE` (-1, the
  header's macOS value) is the normal decline path.
- A basic plugin in `AutoStart/` is a **headless service** (`OnGetPluginInfo` +
  `OnLoad`, then nothing) — background work starts in `on_load`, on its own
  thread, via `SharedHost` (cross-thread host calls: one recorded session of
  evidence, see the type's docs).
- `OnLoad` fires early in startup; `E_INVALIDARG` then means "not available
  yet", not "no such query".

## Roadmap (post-MVP)

1. In-host `OnProcessSamples` confirmation with a playing deck (audible
   beat-synced tremolo) — the last MVP callback not yet observed live.
2. Parameter declaration (`DeclareParameter*` — needs pinned storage the host
   can write into) and the default parameter UI.
3. `IVdjPluginStartStop8` and buffer/position DSP variants (slot positions for
   StartStop already captured by the harness).
4. Skin-interface UI (`VDJINTERFACE_SKIN`) with buffers owned for the instance
   lifetime, per the verified contract.
5. A generated, typed verb layer from the repo's verb store
   (`docs/vdjscript-verbs.json` + plugin-channel HRESULT captures): per-verb
   methods choosing `GetInfo` vs `GetStringInfo` and surfacing `HRESULT`s as
   `Result` — the thing the C++ SDK never had.
6. Video / online-source interfaces (the latter blocked on the second-loading-
   path question in [Plugin SDK.md](../docs/Plugin%20SDK.md) §Loading).
