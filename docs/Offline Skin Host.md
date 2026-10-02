# Hosting the native skin engine offline

## Result

A custom host rendered a synthetic skin through the native VirtualDJ 18.0.9246
arm64 window loader, panel/button drawing code, and Metal backend on 2026-09-30
UTC. GPU readback produced the expected image, and every pixel was checked against
an independent geometry/color expectation. The installed app was not modified or
attached to.

![Native offscreen render](../tests/offline-skin-host-9246.png)

The source texture has an orange rectangle at the top left on a blue background.
The skin draws another copy of that rectangle as a button, offset by the XML
position. Their overlap produces the stepped outline above. This is the native
rendered result, not a host-side drawing of the expected picture.

The **headless hosting path works for this fixture**. Full application-style
`CSkinEngine::load` reaches `loadEnd()` but requests a dialog saying
`Graphics failed to initialize.` The debugger stops before displaying that dialog.
A complete interactive replacement for VirtualDJ's application is not established.

Under [Evidence Standards](Evidence%20Standards.md), these are offline native
observations / Tier 2 leads. Confirming live-app parity requires loading the same
fixture in the same build and comparing layout, rendering, and interaction there.

## What runs in the custom host

```text
Copied VirtualDJ image, original native code and symbols
  CXMLFile::loadFromBuffer
  CImage::loadFromFile → native PNG decoder
  CSkinWindow constructor + load
    CSkinPanel::loadChildren → native object factory
  Native Metal renderer + native offscreen texture
  Host supplies a Metal command buffer
  Native offscreen encoder setup
  CSkinPanel::draw → CSkinButton::draw
  Native readback into CImage
  Host saves pixels as PNG
```

The host loads the whole converted copied binary, not a separately extracted skin
library. It supplies a small app bundle containing the vendor's `default.metallib`.
Without that resource the native Metal initializer asserts because its vertex
function is missing.

Even `beginDraw(CImage*)` tries to acquire an onscreen drawable. With no OS window
it returns false. The adapter uses the native backend's command queue to create a
real Metal command buffer, supplies it through `setCmdBuffer:`, then invokes the
native `setRenderTargetBeginDraw:setCurrentRT:` method. It does not patch the binary,
force a successful return, or draw a replacement skin itself.

The panel and button execute their native draw methods. Native GPU readback writes
into a natively initialized `CImage`; the host reads its bounded pixel buffer and
only changes BGRA channel order to encode a normal PNG. The saved checker decodes
that PNG, reconstructs the raw native bytes, checks their hash, then tests every
pixel against the expected background and translated button rectangles.

Fixture:

```xml
<skin name="Offline probe" version="8" width="320" height="200">
  <button>
    <pos x="20" y="20"/>
    <size width="100" height="40"/>
    <up x="0" y="0"/>
  </button>
</skin>
```

This fixture has no actions, queries, text, fonts, animations, or deck dependencies.

## Composition without rendering

The follow-up [Native Skin Child Relationships](Native%20Skin%20Child%20Relationships.md)
recovers contextual construction routes, named slots, and wrapper behavior with
source-path traces. Query its partial manifest with `just native-skin-children`.

The follow-up custom host calls the symbol-rich **18.0.9246 arm64** window loader
and reads its native object tree without creating a renderer or operating-system
window. This is native composition, not a host reimplementation of XML rules.
The 2026-09-30 UTC capture preserves object classes, ordered children, current and
definition rectangles, and the raw deck field. Independent worker runs reproduced
the same trees. These remain **Tier 2 offline native observations**, pending
same-build live-app comparisons.

Observed paired cases:

| Input | Native result in the fixed 9246 host |
| --- | --- |
| Panel at `(40,30)`, child position `(7,9)` | Child retains `(7,9)` and belongs to the panel |
| Same panel, child position `(+7,+9)` | Child position becomes `(47,39)` |
| Position `100-20,80/2`, size `10*3,5+15` | Rectangle becomes `(80,40,30,20)` |
| Earlier `<define class="tile">` with size `80,24` | Button inherits size `80,24` |
| Button overrides width only to `45` | Size becomes `45,24`; missing height is merged |
| Button overrides both dimensions | Explicit size wins |
| Definition appears after the button | Button retains zero dimensions in this fixture |
| `<deck deck="1">` around a button | Wrapper creates no object; button's deck field becomes `1` |
| Unknown wrapper around a button | Neither wrapper nor button appears in the tree |
| Missing class name, explicit position and size | Button still appears with its explicit rectangle |

The window loader also inserts native `CSkinGrabZone` objects before and after the
authored children. Consequently the object tree is not a one-to-one copy of the
XML tree. Likewise, definitions supply data and deck wrappers pass context without
becoming runtime objects. That distinction is useful for a compiler's intermediate
representation and for diagnostics about XML that produced no object.

For example, the relative-position fixture produces this excerpt, omitting the
generated grab zones:

```text
CSkinWindow  [0, 0, 320, 200]
  CSkinPanel  [40, 30, 200, 100]
    CSkinButton  [47, 39, 30, 20]
```

Read the saved input and complete tree without executing vendor code:

```sh
just offline-skin-composition show --case nested_relative
just offline-skin-composition show --case class_partial_override
just offline-skin-composition show --case class_forward
just offline-skin-composition show --case nested_relative --stage resized
just offline-skin-composition-check
```

The host also directly invokes `CSkinPanel::move(SRect const&)` on the root with
`[0,0,640,400]`, snapshots the tree, then restores `[0,0,320,200]`. Every restored
tree matches its loaded tree. This is **not the complete window-resize path**:
the host does not update window scale/stretch state. Fixed buttons remain fixed;
the panel and generated grab zones change according to native state. The unusual
intermediate panel rectangles are retained, not normalized into an assumed
uniform scale. Do not infer general resize behavior from this direct call.

Reproduce the native run with fresh paths:

```sh
just doctor
uv run --with capstone --with numpy --python .venv/bin/python3 python \
  tools/probe_skin_composition.py prepare \
  --app /Volumes/nom/src/virtualdj-api-reference-resources/unpacked/9246/vdj.pkg/Payload/VirtualDJ.app \
  --work /private/tmp/vdj-composition-example
just offline-skin-composition run --work /private/tmp/vdj-composition-example \
  --output /private/tmp/vdj-composition-example/capture.json
```

Preparation currently reuses the rendering host's setup, including unused Metal
bundle resources; the composition workers execute `bin/host` and never initialize
Metal. Each fixed input runs in a fresh sandboxed process, with code fingerprints,
bounded memory reads, class checks, vector bounds, cycle/depth limits, and arena
canaries. Unreviewed runtime classes stop the reader instead of guessing a layout.

Evidence: [confirmed composition capture](../tests/offline-skin-composition-9246.json),
[ABI and bounded disassembly](../tests/skin-composition-layout-9246.json), and
[host source](../tools/plugin/offline_composition_host.cpp). The initial capture
stopped because the reader did not yet recognize the generated grab-zone class;
the `-layout-initial` and `-expanded-initial` captures preserve the subsequent
experiments. The final repeat reproduced all expanded-case events.

This recovers a **runtime instance hierarchy for the tested classes**, not a
complete allowed-tag manifest. The reader currently understands windows, panels,
buttons, and grab zones. It does not supply script evaluation, visibility updates,
all element ABIs, or arbitrary-skin compilation. Useful next work is to map native
objects back to source XML and expand class coverage; missing classes and dropped
subtrees can then become contextual lint diagnostics rather than mere load success.

## Full-engine loader boundary

`CSkinEngine::load` expects a skin basename beneath the configured data directory's
`Skins` folder; supplying an absolute filename did not bypass that prefix. The
host sets only the copied process's `_Config` data-directory string to its temporary
work folder and supplies a natively constructed `_mainWindow` object. With those
dependencies, native full loading finds the fixture, loads the image and XML,
constructs children, and reaches `loadEnd()`.

The remaining error is at application graphics initialization. A constructed
`CSkinWindow` is not a fully initialized operating-system window. Completing this
path will require recovering the actual OS-window startup sequence and its
relationship to the engine's render target. The successful headless path does not
require solving that first.

## Reproduction and checks

Use a fresh temporary folder and output filename. The source is the user-provided
symbol-rich app; no installation or replacement is performed.

```sh
just doctor
uv run --with capstone --with numpy --python .venv/bin/python3 python \
  tools/probe_skin_host.py prepare \
  --app /Volumes/nom/src/virtualdj-api-reference-resources/unpacked/9246/vdj.pkg/Payload/VirtualDJ.app \
  --work /private/tmp/vdj-skin-host-example
just offline-skin-host run --work /private/tmp/vdj-skin-host-example \
  --output /private/tmp/vdj-skin-host-example/capture.json
just offline-skin-host-check
```

The run launches independent debugger-supervised processes for window loading,
offscreen drawing, and full-engine loading. It saves a PNG beside the capture when
offscreen drawing and readback complete; it verifies the fixture pixels before
marking the suite finished. A finished suite includes the recorded full-loader
limitation, not a claim that every mode succeeded. The saved check requires no
vendor code execution or debugger.

Evidence:

- [Confirmed capture](../tests/offline-skin-host-9246.json): sandbox controls,
  fingerprints, native call traces, worker output, readback, and pixel oracle.
- [Rendered PNG](../tests/offline-skin-host-9246.png).
- [Layout and bounded disassembly](../tests/skin-host-layout-9246.json).
- Earlier `offline-skin-host-9246-*-initial.json` captures retain failed and
  superseded experiments. The first capture is `offline-skin-host-9246-initial.json`.

Initial failures distinguish different causes: the direct window draw dereferenced
a missing render target; missing shader resources caused a Metal assertion; native
`beginDraw` had no drawable; an incorrect host readback destination caused a memory
error and was corrected to the native `CImage` ABI; full loading needed a data path
and main window before reaching the remaining graphics-startup error. No failure
is classified as invalid skin XML.

## Boundaries and ownership

This extends [Offline XML Parser](Offline%20XML%20Parser.md) and
[Offline Parser Host](Offline%20Parser%20Host.md). The source build/hash is pinned;
the prepared library, executable, fixtures, shader resource, bundle files, framework
files/symlinks, and routine fingerprints are checked. Each process denies real-home
reads, network access, and writes outside its temporary tree. Positive/negative
sandbox controls must pass. Metal's denied cache writes are retained in the logs;
restrictions were not relaxed to make the render pass.

Class ABIs, the copied configuration string, and the main-window pointer are
build-specific. Native constructors initialize oversized zeroed host arenas; the
window/image arenas have end canaries. This is not a recovered public C++ header
or an exact-size ownership model. Objects are intentionally retained until worker
exit, and vendor application-global finalizers are skipped. The native renderer
uses a real Metal device; this is not a portable or software-only rendering host.

The experiment does not establish arbitrary-skin support, current-build parity,
interactive events, timers, scripting evaluation, fonts, plugin support, or clean
in-process teardown. It does establish a useful next foundation for headless skin
inspection and preview while recovering the engine's hierarchy and dependencies.
