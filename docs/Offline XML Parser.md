# Offline XML parser and skin-construction spike

## Result

**The proposed experiment is viable on the symbol-rich build.** On VirtualDJ
18.0.9246 (arm64, captured 2026-09-29 UTC), a copied image accepted XML buffers,
returned native failure information, constructed skin objects, and exposed the
field-reader calls and their return values under a debugger. A button's `action`
attribute reached the native VDJScript parser and produced an `ACTION_is_using`
object. The installed application was not launched, attached to, or modified.

These are **offline native observations / Tier 2 leads** under
[Evidence Standards](Evidence%20Standards.md), not proof of rendered skin behavior.
Confirming application parity requires loading the same fixtures in build 9246
and comparing diagnostics, constructed layout, and the script binding in the live
skin context. No verb-store status has been promoted from this experiment.

## A concrete example

Input `factory_button_action`:

```xml
<button action="is_using cue">
  <pos x="1" y="2"/>
  <size width="10" height="20"/>
</button>
```

The capture uses this XML on one line. Selected observed calls, condensed from
[the trace](../tests/offline-xml-trace-9246.json):

```text
CXMLFile::loadFromBuffer
  CXMLFile::loadFromString
    CXMLNode::load                         -> success
ISkinObject::createSkinObject("button")
  CSkinButton::CSkinButton
    ISkinObject::load
      getIntParam(size, "width", default=0)  -> 10
      getIntParam(size, "height", default=0) -> 20
    getParam(button, "action")              -> "is_using cue"
    [skin action cache callback]
      IAction::create("is_using cue")        -> ACTION_is_using
  -> CSkinButton
```

This is a selected call sequence, not a complete instruction trace. The recorded
`caller` and `caller_pc` identify the actual consumer of a reader result. Every
entry/return pair has a `call_id`; addresses are normalized to the original image.
The input reaches the action parser more than once in this constructor path; the
raw trace retains each invocation. The host never calls click, drawing, action
execution, or query-evaluation methods.

## What the comparisons showed

Every row below refers only to the build and capture above. Exact inputs, partial
parse trees, return values, and process output are in the
[native suite](../tests/offline-xml-9246.json).

| Input or change | Observed result |
| --- | --- |
| `<skin/>` | Reader returns true and a `skin` node. |
| `<skin><button></skin>` | Reader returns false, error flag true, position 16, message `XMLError`; a partial tree remains. |
| Unclosed element or unquoted attribute | Reader returns false with an error flag and position. |
| `<?xml broken><skin/>` | Reader returns false, but error flag stays false and message stays empty. |
| Unknown element/attribute | XML reader preserves it and returns true. This is not schema validation. |
| `<skin/>garbage` or `<skin/><button/>` | Reader returns true and stops at position 7, after the first root. |
| `<Skin></skin>` | Reader accepts the differently cased closing name. |
| Bare ampersand in an attribute | Accepted in this fixture. Named and numeric entities in the separate entity fixture are decoded. |
| Unknown element passed to skin factory | Null object; no separate factory error object was observed. |
| Minimal `button`, `panel`, `text` | Factory returns objects whose vtables identify `CSkinButton`, `CSkinPanel`, and `CSkinText`. |
| Button size `width="10"` | Integer reader returns 10. |
| Button size `width="nonsense"` | Integer reader returns 0, and construction still returns `CSkinButton`. |
| Button size `width="10" width="99"` | Both attributes survive XML parsing; the constructor's integer reader returns 10. |
| Uppercase `BUTTON`, `SIZE`, `WIDTH` | Factory still returns `CSkinButton`; width reader returns 10. |
| Button with `zzunknown` attribute and `zzchild` child | Construction succeeds. No getter request for the attribute was observed in the selected trace. This does not exclude direct or inlined reads. |

There is no returned exception/error object at the XML entry point: it returns a
boolean and stores diagnostic state on `CXMLFile`. In this standalone environment
the message is the untranslated key `XMLError`; disassembly shows the failure path
uses the application's message engine. The message and error flag therefore cannot
replace checking the boolean return. Position is the reader's native cursor, not
yet a guaranteed user-facing offending-character span.

## Are unknown names actually ignored?

The follow-up on 18.0.9246 arm64 (captured 2026-09-29 UTC) distinguishes **an
unconsumed value in a particular construction path** from **a globally unknown
XML name**. The reader provides no schema-recognition result in these tests.
It retains arbitrary names in the parsed tree. The object factory returning null
is insufficient to classify a name as unknown: the recognized child `<size>` also
returns null when passed to the factory as a standalone object.

The follow-up installs hardware **read watchpoints** when the factory begins and
removes them when it returns. For the short string values in these fixed inputs,
they cover the text including its terminator and the string's length/tag byte.
This observes accesses even when a getter is inlined. The same run watches a known
width as a positive control. The XML snapshots taken before and after construction
are equal: construction neither removes unknown fields nor marks them consumed.

| Fixture change | Observation during construction |
| --- | --- |
| `<button><size width="10" height="20"/></button>` | Width value and length are read; integer getter returns 10. |
| Add `zzunknown="yes"` to that button | Neither the unknown value nor its length is read; the known width is still read and returns 10. |
| Add `<zzchild width="99"/>` beside the valid `<size>` | Unknown child's width value and length are unread; the valid sibling's width returns 10. |
| Put `<size width="99" height="20"/>` inside `<zzchild>` | Nested width is unread; button's width getter returns its default 0. The wrapper is not transparently flattened in this path. |
| Misspell `width` as `widht` on `<size>` | Misspelled value is unread; the constructor requests `width`, gets 0, and still constructs the button. |
| `<zzunknown/>` as the factory input | No skin object returned. |
| `<size width="10" height="20"/>` as the factory input | Also no skin object returned, although `size` is recognized within a button. |

Thus the tested unknown attribute's **value is ignored during button construction**;
the tested unknown child does not supply button geometry. This is stronger than
merely observing no named getter call. It does not mean the unknown child node is
never visited: condition checks can inspect its metadata. Nor does it rule out
later use, different parents, custom classes, other flags, or behavior in another
build. No full renderer was exercised, so these remain offline/Tier-2 observations.

For a linter, report `not consumed in this element/context` with the tested build
and path. Reserve `unknown name` for a context whose complete dispatch/reader rules
have been established. Do not derive a global schema by subtracting a single run's
getter names from the XML: optional branches and direct reads make that unsound.
Live confirmation would load these paired fixtures in build 9246, compare geometry
and diagnostics, and exercise relevant later state changes.

Evidence: [native comparisons](../tests/offline-xml-unknowns-9246.json),
[read watches and call/return traces](../tests/offline-xml-unknowns-trace-9246.json).
The saved checks verify positive reads, candidate non-reads, getter results,
unchanged trees, sandbox controls, and completion. Watchpoint hit totals are
instrumentation details, not semantic operation counts.

```sh
just offline-xml-unknowns prepare --app /Volumes/nom/src/virtualdj-api-reference-resources/unpacked/9246/vdj.pkg/Payload/VirtualDJ.app --work /private/tmp/vdj-xml-unknowns-example
just offline-xml-unknowns run --work /private/tmp/vdj-xml-unknowns-example --output /private/tmp/vdj-xml-unknowns-example/native.json
just offline-xml-unknowns trace --work /private/tmp/vdj-xml-unknowns-example --output /private/tmp/vdj-xml-unknowns-example/trace.json
just offline-xml-unknowns-check
```

Preparation needs the optional dependencies described below; use the `uv run`
wrapper there with `tools/probe_xml_unknowns.py` if they are not installed in the
project environment. The trace uses the shared callbacks in
`tools/offline_xml_trace.py` and the additional hardware watches in
`tools/offline_xml_unknown_trace.py`. Initial debugger module-registration attempts
remain under the `offline-xml-unknowns-trace-9246-*-initial.json` names (including
`offline-xml-unknowns-trace-9246-initial.json`).

## What this enables

A practical next implementation can keep separate results for:

1. XML parsing: accepted/rejected, native position, partial tree, diagnostic state.
2. Skin construction: selected class, fields requested, conversions/defaults, and
   whether a field was observed being consumed along the exercised path.
3. Embedded script compilation: attribute text, parser calls, and returned action
   class; evaluation remains a separate live-state question.

A linter should add explicit diagnostics around native behavior: trailing content,
duplicate attributes, unknown names, and invalid numeric text can otherwise pass
silently. Strict XML errors and VirtualDJ compatibility warnings should be
reported separately because their accepted inputs differ. A compiler can use the
captured tree and call traces as differential test cases for its own implementation.
These traces do not yet define a complete schema or portable compiled skin format.

## Reproduce

The source binary is the user-provided 9246 app at the path below; no download or
installed-app replacement is needed. Choose a new temporary work directory and
new output filenames on subsequent runs. Captures are never overwritten.

```sh
just doctor
uv run --with capstone --with numpy --python .venv/bin/python3 python \
  tools/offline_xml.py prepare \
  --app /Volumes/nom/src/virtualdj-api-reference-resources/unpacked/9246/vdj.pkg/Payload/VirtualDJ.app \
  --work /private/tmp/vdj-xml-example
just offline-xml run --work /private/tmp/vdj-xml-example \
  --output /private/tmp/vdj-xml-example/native.json
just offline-xml-trace --work /private/tmp/vdj-xml-example \
  --output /private/tmp/vdj-xml-example/trace.json
just offline-xml-check
```

`offline-xml-check` checks the committed captures without loading VirtualDJ or
requiring LLDB. Prepare requires `capstone` and `numpy`; tracing requires the
Xcode command-line debugger and permission to debug the user-owned worker.
Executing a child sandbox from a sandboxed agent may require execution approval.

## Isolation and remaining limits

Preparation reuses the copied-image conversion from
[Offline Parser Host](Offline%20Parser%20Host.md). It pins the source SHA-256 and
image UUID, preserves native symbols, checks routine fingerprints, and writes
only into the new temporary directory. The runner verifies the prepared binary,
host, sandbox, dependency files/symlinks, and the compiled fixed-input suite.
The [layout manifest](../tests/xml-reader-layout-9246.json) saves bounded
instruction listings and hashes for the reviewed XML/factory routines.

Each input runs in a fresh process with a timeout and disabled core dumps. The
sandbox denies real-home reads, network access, and writes outside its work tree;
positive and negative controls are captured. The debugger launches our own host,
which applies the same sandbox **before** loading vendor code. Breakpoints are
installed only after code fingerprints pass; installing them earlier changes the
bytes and correctly fails the guard. The in-process sandbox API is deprecated by
macOS, so each run checks its actual denials instead of assuming it worked.

`CXMLFile` is initialized with a reviewed, build-specific ABI layout and zero
flags. Native close releases the parsed XML tree. Factory objects are deliberately
retained until worker exit: their ownership/destructors have not been audited.
The host exits without invoking vendor application-global finalizers.

The factory receives null image and window dependencies. There is no full skin
engine startup, image loading, class/template expansion test, rendering, or live
state equivalence test. Complex controls may require more context. Selected named
function breakpoints do not cover inlined reads or every downstream call, and the
symbol-rich build may differ from current builds. These limits bound the findings;
they do not prevent using the demonstrated reader and construction paths as an
experimental test oracle.

The [first XML suite](../tests/offline-xml-9246-initial.json) and
[debugger development attempts](../tests/offline-xml-trace-9246-initial.json) remain
under initial names. The latter documents the protected system-launcher attach
failure, wrong working-directory control failure, early-breakpoint guard failure,
and the first successful entry-only trace.
