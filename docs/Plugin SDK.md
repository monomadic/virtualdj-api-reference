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

It also localises a known defect. `master_beat_num` returns float32 *bits* through an integer
path over HTTP ([HTTP Control Interface](HTTP%20Control%20Interface.md)); since the core hands
back a `double` here, that coercion is almost certainly in the **rendering** path, not the
engine. A plugin calling `GetInfo("master_beat_num", &d)` settles it in one call — see
[TODO.md](../TODO.md) task 10.

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

**Open question — do not assume the documented path is the only one.** The bundled
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

A read-only introspection plugin is queued as the next instrument for
[TODO.md](../TODO.md) task 10, because it can do what the HTTP channel structurally cannot:

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
