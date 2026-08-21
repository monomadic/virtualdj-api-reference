# Plugin SDK

VirtualDJ's C++ plugin interface: the native-code extension point, and — more importantly for
this repo — **the boundary where VDJScript's return values are still typed.**

Written 2026-07-30. Source labels follow [Evidence Standards](Evidence%20Standards.md): the
headers are `Official` (Tier 2 — official documentation, which this repo has caught being
incomplete before), the on-disk observations are `Local observation` on VirtualDJ 2026
(bundle `18.0.9482`, macOS arm64), and the binary findings are `Binary symbol table`.

## Why this matters beyond writing plugins

The HTTP control interface returns everything as text, so a query's real type has to be
recovered by observation. The plugin SDK shows why: the host exposes **two separately typed
query entry points**, and HTTP collapses both into a response body.

```cpp
struct IVdjCallbacks8
{
    virtual HRESULT SendCommand(const char *command)=0;                        // execute
    virtual HRESULT GetInfo(const char *command, double *result)=0;            // numeric query
    virtual HRESULT GetStringInfo(const char *command, void *result, int size)=0; // text query
    virtual HRESULT DeclareParameter(void *parameter, int type, int id,
                                     const char *name, const char *shortName,
                                     float defaultvalue)=0;
    virtual HRESULT GetSongBuffer(int pos, int nb, short **buffer)=0;
};
```

**VDJScript is not stringly typed.** Script goes *in* as `const char *`; results come *out* as
either a `double` or a UTF-8 buffer, chosen by which call you make. Everything numeric —
booleans, counts, 0..1 sliders, percentages — shares the single `double`. That is why
`tests/verb-return-types.json` records 334 "bool" verbs: those are doubles that the HTTP layer
renders as `yes`/`no`.

This maps exactly onto the vtable slots
[extract_action_contracts.py](../tools/extract_action_contracts.py) calibrated from compiled
`ACTION_` classes, *before* these headers were consulted — independent corroboration of the
same three-way split (Evidence Standards rule 1g):

| Verb-table vtable slot | SDK callback |
| --- | --- |
| slot 2 — execute | `SendCommand` |
| slot 3 — generic query (the variant) | `GetInfo` → `double *` |
| slot 4 — specialized text query | `GetStringInfo` → buffer |

**Corrected by measurement (`Local test`, plugin channel, 2026-08-15).** Calling both
callbacks on all 1,028 verbs partitions the result exactly, and the slot 3/slot 4 split above
is not what happens:

- **Slot 3 backs *both* callbacks** — 594 of the 599 text answers, and every numeric answer.
  `GetStringInfo` is mostly the variant rendered as text.
- **Slot 5 is a fallback label provider.** Of the 174 verbs that do not override slot 3,
  exactly 5 answer text and all 5 override slot 5 — `stop_button` → `"■"`,
  `scratchbank_load` → `"Bank A"`, `sampler_pad_page` → `"1 to 8"`. The other 169 answer
  nothing. Every text answer in the capture therefore comes from slot 3 or slot 5, with no
  remainder.
- **Slot 4's role is unproven.** All 85 of its text-answering verbs also override slot 3, so
  it explains nothing on its own.

Two operational facts from the same capture. `E_INVALIDARG` is the numeric channel's "wrong
channel, ask the other one" code and `S_FALSE` is the text channel's; **VirtualDJ writes
`0.0` to `*result` even when it returns an error**, so the HRESULT is the answer and a raw
`0` is meaningless without it. And because the HRESULT arrives separately from the value, this
channel can tell a **recognized argument from an ignored one** — `is_using cue` answers
`S_OK`/`off` where `is_using zzznotakeyword` answers `E_NOTIMPL` — which HTTP structurally
cannot. See the tracker's Plugin Channel section.

It also localised a known defect — and then **refuted the guess about it**. `master_beat_num`
returns float32 *bits* through an integer path over HTTP
([HTTP Control Interface](HTTP%20Control%20Interface.md)), and this page previously reasoned
that since the core hands back a `double`, the coercion was "almost certainly in the rendering
path, not the engine." Wrong. `GetInfo("master_beat_num", &d)` on VirtualDJ 2026 (bundle
`18.0.9583`, `Local test` via the plugin channel, 2026-08-15) returns `S_OK` with `d` holding
**exactly `1083943558.0`** — the int32 reading of float32 bits `0x409baa86` (= `4.8646`),
already punned before it reaches any channel. The defect is in the **core**; HTTP was rendering
a broken number faithfully. Consumers of this verb must reinterpret the int32 bits as float32
on either channel.

### What the SDK does *not* contain: any verb information at all

Worth stating plainly, because the headers look like they should be a reference and are not.
Checked mechanically 2026-07-30 against the 1,028-name verb table: across all 32 KB of unique
header text, **not one verb name appears as a verb**. Sixteen names match as ordinary English
in comments and C++ parameter names — `// the crossfader moves continuously…`,
`float *volume` in `OnTransformPosition`, `// load and unload a plugin`,
`OnSearch(const char* search, …)` — and that is the entire overlap.

This is structural rather than an omission. The command parameter is opaque:

```cpp
virtual HRESULT GetInfo(const char *command, double *result)=0;
```

The SDK defines **how to ask** — calling convention, type channels, HRESULT contract — and says
nothing about **what may be asked**. The vocabulary lives entirely inside VirtualDJ, which is
why the verb set had to be extracted from the binary
([Undocumented VDJScript Candidates](Undocumented%20VDJScript%20Candidates.md) §verb table)
rather than read out of a header.

Consequences worth keeping straight:

- The **plugin is not a discovery instrument for verbs.** It is for *types and behaviour* that
  only exist at runtime. Existence, aliases, categories and capability are already settled from
  the binary.
- Verb questions *can* be answered with no VirtualDJ present — from this repo's committed
  artifacts (`tests/verb-table.json`, `action-contracts.json`, `verb-return-types.json`,
  `verb-existence-sweep.json`, all read by `just get-verb <name>`). Producing them requires the
  app; consuming them does not.

## Provenance, and why the headers are not in this repo

| Fact | Detail |
| --- | --- |
| Copyright | `(c)Atomix Productions 2011-2018`, in every header |
| **License** | **None stated.** No LICENSE text in the headers, and no terms of use or redistribution conditions on the SDK download page. |
| Official download | [PluginSDK8.html](https://www.virtualdj.com/wiki/PluginSDK8.html) → `VirtualDJ8_SDK_20211003.zip` ("header files for all types of plug-ins") |
| Community examples | [github.com/szemek/virtualdj-plugins-examples](https://github.com/szemek/virtualdj-plugins-examples) — 8 buildable examples, Xcode 14.3 / macOS 13.3, "copied and adapted from official documentation". No LICENSE file; the headers are still Atomix's. |

Publishing the SDK for plugin authors implies permission to *use* it; it grants nothing about
redistribution. **This repo therefore does not vendor the headers** — `vendor/` is gitignored,
with fetch instructions in the ignore entry. Put a local copy in `vendor/vdj-sdk/` to build
anything described here.

## The interface hierarchy

Everything derives from `IVdjPlugin8`, which supplies lifecycle, parameters, UI, and the three
host callbacks above.

```cpp
class IVdjPlugin8
{
    virtual HRESULT VDJ_API OnLoad() {return S_OK;}
    virtual HRESULT VDJ_API OnGetPluginInfo(TVdjPluginInfo8 *info) {return E_NOTIMPL;}
    virtual ULONG   VDJ_API Release() {delete this; return S_OK;}
    virtual HRESULT VDJ_API OnParameter(int id) {return S_OK;}
    virtual HRESULT VDJ_API OnGetParameterString(int id, char *outParam, int outParamSize);
    virtual HRESULT VDJ_API OnGetUserInterface(TVdjPluginInterface8 *pluginInterface);
    IVdjCallbacks8 *cb;
};
```

| Subclass | Header | Key virtuals |
| --- | --- | --- |
| `IVdjPluginStartStop8` | `vdjPlugin8.h` | `OnStart`, `OnStop` |
| `IVdjPluginDsp8` | `vdjDsp8.h` | `OnProcessSamples(float *buffer, int nb)` |
| `IVdjPluginBufferDsp8` | `vdjDsp8.h` | buffered audio variant |
| `IVdjPluginPositionDsp8` | `vdjDsp8.h` | `OnTransformPosition(double *songPos, double *videoPos, float *volume, float *srcVolume)` |
| `IVdjPluginVideoFx8` | `vdjVideo8.h` | `OnDraw`, `OnDeviceInit`, `OnDeviceClose`, `GetDevice`, `GetTexture` |
| `IVdjPluginVideoTransition8` | `vdjVideo8.h` | `OnDraw(float crossfader)` |
| `IVdjPluginVideoTransitionMultiDeck8` | `vdjVideo8.h` | `OnDrawMultiDeck(int nbVideoDecks, int *videoDecks)` |
| `IVdjPluginOnlineSource` | `vdjOnlineSource.h` | `OnSearch`, `GetStreamUrl`, `GetFolder`, `GetFolderList`, `OnLogin`/`OnOAuth`, context menus |

`OnTransformPosition` and the online-source interface are worth noting for this repo: they
expose song position and browser/source integration at a level VDJScript does not reach.

### `GetSongBuffer` — characterized (`Local test`, 2026-08-15)

```cpp
virtual HRESULT GetSongBuffer(int pos, int nb, short **buffer)=0;
```

Undocumented in every header beyond that signature; measured on VirtualDJ 2026
(bundle `18.0.9583`), and the full evidence is in the
[Local Test Tracker](VDJScript%20Local%20Test%20Tracker.md).

- **`pos` and `nb` both count stereo frames.** A frame is 4 bytes: interleaved
  left/right `int16`.
- **It returns an interior pointer, not a copy**: `buffer = base + 4 × pos`, holding
  exactly over hundreds of thousands of frames. The whole track is decoded and
  resident (~54 MB for five minutes), so reading any part of it is free.
- **Sample rate is 44,100 Hz**, established by cross-check rather than assumption.
- **The buffer runs past the song**, silence-padded by roughly 2^16 frames.
- **Bounds are checked at the top only.** `pos + nb` beyond the buffer gives
  `E_FAIL`, but a **negative `pos` is accepted and returns a pointer before the
  buffer** — an out-of-bounds read. Clamp it yourself.

Track length is not available as `get_totaltime` or `get_length` (neither is a verb
on this build); use `get_time 'total'`, in milliseconds.

### Interfaces in the binary that the public SDK never declares

Typeinfo names present in `/Applications/VirtualDJ.app/Contents/MacOS/VirtualDJ` but absent
from every public header (`Binary symbol table`, 2026-07-30):

- **`IVdjPluginHelperBeats`** — unexplored. The name is suggestive given that beatgrids and
  waveforms are a standing gap in this repo.
- **`IVdjTransitionCallbacks8`**

The public surface is a **subset** of the live one. Treat the SDK as a partial export of an
internal framework, not a complete description of it.

## Parameters, and the manifest every native plugin uses

`DeclareParameter` is called during `OnLoad()`; typed wrappers exist for each kind.

| Constant | Value | Wrapper / notes |
| --- | ---: | --- |
| `VDJPARAM_BUTTON` | 0 | `DeclareParameterButton(int *)` |
| `VDJPARAM_SLIDER` | 1 | `DeclareParameterSlider(float *, …, float defaultvalue)` |
| `VDJPARAM_SWITCH` | 2 | `DeclareParameterSwitch(int *, …, bool)` |
| `VDJPARAM_STRING` | 3 | `DeclareParameterString(char *, …, int parameterSize)` |
| `VDJPARAM_CUSTOM` | 4 | `DeclareParameterCustom(void *, …, int parameterSize)` |
| `VDJPARAM_RADIO` | 5 | `DeclareParameterRadio(int *)` |
| `VDJPARAM_COMMAND` | 6 | `DeclareParameterCommand(char *)` |
| `VDJPARAM_COLORFX` | 7 | slider with default 0.5; **one per effect**, single-knob full control |
| `VDJPARAM_BEATS` | 8 | float, number of beats |
| `VDJPARAM_BEATS_RELATIVE` | 9 | int; set ±1 to step the beat count when `OnParameter` fires |
| `VDJPARAM_POSITION` | 10 | `float[4]`; user resize/position in a video plugin's GUI |
| `VDJPARAM_RELEASEFX` | 11 | pairs with the release-FX model in [Effects Engines](Effects%20Engines.md) |
| `VDJPARAM_TRANSITIONFX` | 12 | name fixed to `"Transition FX"` / `"Trans"` |

Declared parameters are persisted to a per-plugin `.ini` beside the plugin, in an
`[autoparams]` section of `<Type> <Name> <id>=<value>`:

```ini
[autoparams]
Slider Strength 0=1925                 ; native_Blur.ini
String Nudge 2=0.0 ms                  ; native_Ableton Link.ini
Custom HttpPort 1=50000000             ; native_Network Control.ini
SString Auth 2=
```

**Slider values are integers on a 0–4096 scale** (`Local test`, 2026-08-15). Decoded from
a plugin of our own: `DeclareParameterSlider(..., 0.5f)` wrote `Slider Probe Slider 1=2048`,
and 2048 = 4096 / 2. That decodes every shipped manifest — `native_Blur.ini`'s
`Strength 0=1925` is 47 %, not 1925 of anything. A written-down default in an `.ini` is
therefore readable as a fraction, which is what the FX catalog reports.

**`VDJFLAG_EPHEMERAL` (0x200) really does suppress the file.** Same session, two builds: the
AutoStart build set the flag and left no `.ini` beside it; the Sound Effect build did not set
it and VirtualDJ wrote one on removal. An accidental natural experiment, but a clean one.

**This is the same framework VirtualDJ is built with.** 173 `native_*.ini` manifests ship in
`~/Library/Application Support/VirtualDJ/PluginsMacArm/` — Blur, Backspin, Beat Grid, Slicer,
Ableton Link and Network Control all declare parameters this way. Type-name frequency across
all of them: `Slider` ×487, `Switch` ×220, `Custom` ×11, `SString` ×6, `Position` ×5,
`String` ×3.

Note `SString` — used for the Network Control plugin's `Auth` password field, and **not a
documented `VDJPARAM_` constant**. Another piece of internal surface that did not make it into
the public header. (Its meaning is unconfirmed; "secure string" is a guess from its one known
use, not a claim.)

### `VDJFLAG_*` (plugin info flags)

`NODOCK` 0x1 · `PROCESSAFTERSTOP` 0x2 · `PROCESSFIRST` 0x4 · `PROCESSLAST` 0x8 ·
`EXTENSION1` 0x10 (set *by VirtualDJ* when the passed struct is the extended type) ·
`SETPREVIEW` 0x20 · `POSITION_NOSLIP` 0x40 · `ALWAYSPREFADER` 0x80 · `ALWAYSPOSTFADER` 0x100 ·
`EPHEMERAL` 0x200 (do not save/load params from the ini).

## Can a plugin add VDJScript verbs? No — it extends the *argument* namespace

This matters for [Evidence Standards](Evidence%20Standards.md) rule 1b, which treats absence
from the verb table as disproof: if plugins could register verbs, the table would only be the
built-in set.

**The public SDK has no verb-registration call.** Every registration entry point it offers is a
parameter declaration — `DeclareParameter` plus its thirteen typed wrappers. There is no
`DeclareAction`, `RegisterVerb`, `AddCommand`, or equivalent, in any of the four headers.

Instead, plugin capability is surfaced through **existing verbs that take a name or index**:

| A plugin adds | Reached from VDJScript by |
| --- | --- |
| An effect (DSP / video FX / transition) | `effect_select "Blur"`, `effect_slider`, `effect_button` — by name or slot index |
| Effect-specific commands | `effect_command` — *"send a command to this effect"* |
| Declared parameters | the effect slider/button verbs, by id |
| An online source | browser entries, not verbs |

Consistent with that, every plugin-related name in the verb table is a **built-in verb for
plugins**, not a verb from one: `handshake`, `get_plugindeck`, `pluginsongpos`,
`show_pluginpage`, `effect_command`. And with two Beatport online-source plugins installed on
the test machine, the table contains no `beatport`/`tidal`/`soundcloud`/`deezer`/`spotify`
name at all.

**Scope limit, stated honestly.** This is evidence about the *public* SDK and the stock app.
Native plugins are compiled into the binary, so anything they contribute is already in the
table. But the public headers are a known subset of the live interface (see the internal
interfaces above), so an internal registration path cannot be ruled out from headers alone.
Rule 1b should be read as: **complete for a stock VirtualDJ plus any plugin using the public
API.** The test that would settle the rest is a built plugin probing for an undocumented
registration path — queued with the introspection plugin.

## `handshake` — the plugin-authenticity mechanism, and an oracle

`handshake` is a real verb (verb table id 84, category `system`) and it autocompletes in
VirtualDJ's editor. The bundled catalog documents it (`Official`, `languages.zip`):

> Perform an encrypted handshake to ensure that this plugin is currently being called by a real
> VirtualDJ environment. Call this passing any string, decrypt the result using VirtualDJ's
> handshake public key, and check that it matches what you passed.

Observed over HTTP (`Local test`, VirtualDJ 2026, 2026-07-30):

| Call | Result |
| --- | --- |
| `handshake` (bare) | `E_INVALIDARG` — argument required |
| `handshake 'nonce'` | **exactly 128 bytes of binary** (not UTF-8), i.e. a 1024-bit RSA block |
| same nonce, repeated | **byte-identical** — deterministic, so no random padding |
| different nonce | completely different 128 bytes |

So a plugin verifies it is talking to genuine VirtualDJ by having it sign a challenge with a
private key the plugin checks against a bundled public key.

**Worth knowing before building a shim.** Because `handshake` is reachable through the HTTP
control channel, any process that can reach that port can have VirtualDJ sign arbitrary
challenges — a signing oracle. A fake host could therefore relay a plugin's challenge to a real
VirtualDJ and return a valid response, which is precisely the attack the handshake exists to
prevent. This is directly relevant to the shim-server work in
[VDJScript Local Test Tracker](VDJScript%20Local%20Test%20Tracker.md): a shim that needs to
satisfy a plugin's handshake can proxy it, rather than needing the key. Recorded as an
architectural observation about local software on the tester's own machine; the practical
exposure is bounded by the same thing that bounds the whole channel — see the security note in
[HTTP Control Interface](HTTP%20Control%20Interface.md).

## Plugin user interfaces

`OnGetUserInterface` fills `TVdjPluginInterface8`, whose `Type` selects one of three models:

| Type | Value | Meaning |
| --- | ---: | --- |
| `VDJINTERFACE_DEFAULT` | 0 | VirtualDJ builds the UI from the declared parameters |
| `VDJINTERFACE_SKIN` | 1 | **the plugin supplies skin XML + a PNG** — the same skin dialect documented in [Skin SDK](Skin%20SDK.md) |
| `VDJINTERFACE_DIALOG` | 2 | native window: `HWND` on Windows, `NSWindow *` on macOS |

The skin path is the interesting one for this repo: a plugin hands VirtualDJ an XML buffer and
an image buffer, so plugin GUIs and skins share a rendering vocabulary.

## Loading, and one open question

The documented entry point is COM-style class-object negotiation:

```cpp
VDJ_EXPORT HRESULT VDJ_API DllGetClassObject(const GUID &rclsid, const GUID &riid, void **ppObject);
```

with `CLSID_VdjPlugin8` plus a per-type IID (`IID_IVdjPluginBasic8`, `IID_IVdjPluginStartStop8`,
`IID_IVdjPluginDsp8`, `IID_IVdjPluginBuffer8`, `IID_IVdjPluginOnlineSource`,
`IID_IVdjPluginVideoFx8`, `IID_IVdjPluginVideoTransition8`,
`IID_IVdjPluginVideoTransitionMultiDeck8`). The host string `DllGetClassObject` does appear in
the VirtualDJ binary.

**RESOLVED for the documented path (`Local test`, plugin channel, 2026-08-15).** A bundle
exporting `DllGetClassObject` and answering `CLSID_VdjPlugin8` + `IID_IVdjPluginBasic8` loads
and runs on VirtualDJ 2026 (bundle `18.0.9583`), from
`~/Library/Application Support/VirtualDJ/PluginsMacArm/AutoStart/`, **ad-hoc signed**. The host
type-probes by calling the same export repeatedly, once per interface, in this order:

1. `IID_IVdjPluginDsp8`
2. `IID_IVdjPluginBuffer8`
3. `IID_IVdjPluginVideoFx8`
4. `IID_IVdjPluginVideoTransition8`
5. `IID_IVdjPluginVideoTransitionMultiDeck8`
6. `IID_IVdjPluginBasic8` — accepted here, after which probing stopped

So a plugin declares its type by *which IID it accepts*, not by any manifest. Because probing
stops at the first acceptance, the positions of `IID_IVdjPluginStartStop8` and
`IID_IVdjPluginOnlineSource` in the order are unknown — a plugin that declines everything would
reveal the full list.

**Still open — the second path.** The bundled
`beatport16_vdj.bundle` (an online-source plugin) exports 11,303 symbols and **none** is
`DllGetClassObject`, nor does it contain any SDK GUID as raw bytes. Nor do those GUID byte
sequences appear in the host binary — consistent with the compiler materialising constant GUIDs
inline, so that part is unremarkable. But a shipped online-source plugin with no documented
entry point suggests a second, newer loading path. Unresolved; needs a built test plugin to
settle.

### On-disk layout (macOS, VirtualDJ 2026)

`~/Library/Application Support/VirtualDJ/` contains both `Plugins64/` and `PluginsMacArm/`
(same contents on this machine), with per-category subfolders: `AutoStart`, `OnlineSources`,
`SoundEffect`, `VideoEffect`, `VideoTransition`, `Visualisations`. Bundles sit at the top level
(`*.bundle`), and `native_*.ini` manifests for built-in plugins sit alongside them.

## Why this SDK is easy to miss

It is not linked from the wiki's main navigation and surfaces mainly in the context of the
(also obscure) Network Control plugin. The shape of the evidence — headers copyrighted
2011-2018, an interface versioned `8` (the VirtualDJ 8 era), a zip packaged in 2021, 173
first-party plugins built on it, and at least two interfaces plus one parameter type that were
never exported — reads as an internal framework that was published quietly and partially,
rather than a product-managed public API.

Practical consequence: **the interface is stable and heavily dogfooded** (Atomix's own effects
depend on it), which makes it a reasonable foundation to build tooling against.

## Use in this repo

A read-only introspection plugin is the next instrument for [TODO.md](../TODO.md) task 10 —
built and offline-verified 2026-08-15 ([tools/plugin/](../tools/plugin/), `just plugin-build`),
though not yet loaded into VirtualDJ, so nothing below is claimed as observed. Two build facts
worth recording: **Xcode is not needed** (Command Line Tools `clang++` produces a loadable
signed bundle), and VirtualDJ ships with `com.apple.security.cs.disable-library-validation`, so
an ad-hoc signature suffices. It can do what the HTTP channel structurally cannot:

- call `GetInfo` and `GetStringInfo` on each of the 955 verbs and read **native types plus raw
  HRESULTs**, giving a definitive per-verb type-path map instead of one inferred from rendered
  text;
- probe argument forms in-process, making the 301-verb optional-argument queue and the 217
  binary-discovered keyword sets tractable at loop speed rather than HTTP round-trip speed;
- run without the Network Control plugin or a Pro license — a fifth Tier-1 channel with
  different prerequisites from the existing four.

Caveat that survives the channel change: unrecognised arguments are **silently ignored** rather
than rejected, so keyword confirmation still needs prepared state where forms would differ, not
an error code.
