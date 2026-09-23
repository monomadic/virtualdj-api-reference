# Determining whether a skin XML element is recognized

Investigation: 2026-09-24. Live rendering below is scoped to desktop build
18.0.9644, arm64. Binary observations are Tier 2, separately pinned to builds
18.0.9644 and 18.0.9246. A skin loading successfully is not an element verdict.

**Use a contextual recognition test followed by a reader-specific behavioral
test.** The lookup key is `(build, surface, parent/reader, tag, prerequisites)`,
not just the tag. Keep recognized object, handled directive, consumed property,
gated/skipped and unresolved outcomes separate. Only report rejection when the
relevant dispatch is known to have reached its unmatched path; absence from our
partial inventory is unknown.

## Nested-child experiment: useful, but only for containers

[The fixture and capture](../tests/Skins/element-validity-probe/README.md) compare
a cyan textzone directly under the skin with the same object inside each wrapper.
Two independently loaded revisions in the same running process reverse row order
and change the visible revision labels. Both gave these results on build 18.0.9644:

| Wrapper | Nested textzone visible | Wrapper's own content |
| --- | --- | --- |
| none | yes | positive control |
| `panel` | yes | no separate drawing requested |
| `group` | yes | no separate drawing requested |
| `pannel` | yes | no separate drawing requested |
| `zzinvalidalpha` | no | none |
| `zzinvalidbeta` | no | none |
| `button` | no | red rectangle rendered |
| `textzone` | no | yellow `OWN TEXT` rendered |

Thus nested-child survival discriminates these desktop containers from these
nonsense wrappers. The valid leaves are a direct counterexample to using child
absence as an invalid-element verdict. Unknown wrappers did not transparently
pass through the child in this fixture. This does not establish all unknown-tag
handling or prove why a child was absent.

Always retain a sibling positive control before/after the tested region, use two
nonsense names, and repeat with a fresh visible revision. A surviving child alone
could otherwise mean a transparent-wrapper fallback. To test a container's own
semantics next, vary its offset or visibility while holding the child fixed;
child visibility must follow the parent in a way the nonsense controls do not.
That follow-up was not performed here.

The older [plugin-panel experiment](VDJScript%20Local%20Test%20Tracker.md#a-plugin-can-supply-skin-xml-at-runtime--and-that-makes-skin-testing-a-loop-2026-08-22)
reported dropped `group` contents. Today's desktop result must not be generalized
to that surface or used to claim the earlier behavior changed on the same surface.

## Attributes and script-valued attributes

Follow-up local tests on 2026-09-24, desktop build 18.0.9644, arm64:
[attributes/visibility](../tests/Skins/attribute-validity-probe/README.md),
[condition](../tests/Skins/condition-validity-probe/README.md) and
[button/text action](../tests/Skins/script-validity-probe/README.md).
Each fixture was reloaded with reversed rows and a new visible revision;
the observations agreed. No buttons were clicked. These are rendering
observations, not measurements of native HRESULTs or construction timing.

| Placement | Input | Observed rendering |
| --- | --- | --- |
| Button attribute | `zzinvalidalpha="off"` or `zzinvalidbeta="0"` | normal cyan rectangle |
| Button attribute | `zzvisibility="off"` or `zzcondition="off"` | normal cyan rectangle |
| Button `visibility` | `on` | rectangle visible |
| Button `visibility` | `off`, `zzinvalidalpha`, `zzinvalidbeta` | rectangle absent |
| Button `condition` | `on` | rectangle visible |
| Button `condition` | `off`, `zzinvalidalpha`, `zzinvalidbeta` | rectangle absent |
| Button `action` | omitted, `nothing`, `zzinvalidalpha`, `zzinvalidbeta` | rectangle visible |
| Text child's `action` | `get_text 'VALID TEXT'` | `VALID TEXT` visible |
| Text child's `action` | `get_text ''`, `zzinvalidalpha`, `zzinvalidbeta` | no text visible |

An unknown attribute name did not suppress the known-good button in these cases.
A recognized attribute with a nonsense script can affect rendering: the
visibility and condition cases demonstrate that distinction. Do not generalize
these results to malformed XML or every attribute's invalid-value handling.

Neither `condition` nor `visibility` is a validity oracle: a valid false expression
and an unknown verb have the same visible outcome here. Text output has the same
problem with valid empty results. A button can render despite an invalid action
binding. Even positive output does not by itself establish that every argument
was consumed; the language has silently ignored-tail cases elsewhere in the
[grammar evidence](VDJScript%20Grammar.md).

For **attribute recognition**, locate the reader/getter for the exact node, then
change a value that should cause a distinguishable result. Compare with omitted
and nonsense-name controls. Shared-base attributes, nested property attributes
and template parameters must remain distinct. A getter trace should identify
the actual key and receiver, whether lookup found the key, and the consumer
that uses its value; a retained XML attribute is not consumption evidence.

For **VDJScript recognition**, use the structured verb table for name membership
and native `GetInfo`/`GetStringInfo` HRESULTs for channel-specific evaluation,
with known true, false, empty and nonsense controls in prepared state. Native
failure alone is not a syntax verdict: valid verbs can lack a result or be gated
by state/channel. For arguments and compound syntax, observe the parser and
consumer branch or a discriminating behavioral effect. Keep name existence,
parse representation, argument consumption and behavior as separate outcomes.

The proposed native recorder should correlate both stages: XML node/key consumed
by the skin reader, then the script passed to its evaluator and that evaluator's
outcome. This can distinguish an ignored XML attribute from a recognized
attribute whose script evaluated false or failed, which pixels alone cannot do.

## The native mechanism to instrument

[The bounded capture](../tests/skin-validity-mechanism-9644-9246.json) retains image
hashes, routine hashes, literal operands, selected instructions and historical
callee symbols. It was regenerated from disk during this investigation, with the
current image verified against the existing memory anchor. This is not a new live
memory capture.

The symbol-rich arm64 build 18.0.9246 names the two useful entry points:

- `ISkinObject::createSkinObject(CXMLNode*, CImage*, CSkinWindow*)`, unslid
  `0x10036abcc`: tag dispatch and object/directive handling.
- `CSkinPanel::loadChildren(CXMLNode*, CImage*, CSkinWindow*)`, unslid
  `0x1007bb7f4`: parent traversal, special cases and insertion of returned objects.

The current factory is at unslid `0x100396890` on build 18.0.9644. Its button
comparison at `0x10039693c` leads to the constructor already recorded in the
[button ownership capture](../tests/skin-schema-button-9644.json). Addresses are
build-specific analysis coordinates, not callable SDK functions.

Important distinctions visible in the inspected code:

- The current factory gates on `os` and another pre-dispatch check before its
  button comparison. The historical factory names its corresponding check
  `ISkinObject::checkCondition`. A skipped node is not an unknown tag.
- On 9644, the `tooltip` branch calls its handler then reaches the null-return
  block at `0x100396c0c`. The `window` branch allocates/initializes a window and
  also reaches that block. The final unmatched path and handled `define` path
  reach it too. **Null is not a validity boolean**, even for the factory.
- On 9246, `loadChildren` has special handling for `group`, including checks for
  `visibility` and `novisibility`, and a recursive route. Its ordinary factory
  call at `0x1007bba1c` branches past insertion when the result is null. A
  factory-only trace can therefore miss parent-handled nodes.
- Property children such as a button's `pos`, `up` and `text` belong to their
  enclosing reader. They need not create a standalone skin object. The existing
  [schema recovery](Skin%20Schema%20Recovery.md) tracks these receiver paths.

**Proposed runtime probe:** observe normal skin loading on its actual loader
thread; correlate fixture XML node/path, parent route, matched tag branch,
constructor/handler, returned object and insertion into its owner's collection.
Record early gates separately. For property children, record the parent's child
lookup and the node passed to its reader. Copy bounded values while objects are
alive; do not retain node pointers across reloads. Templates need both the
original call site and expanded node identity.

Start on 9246 with named breakpoints to validate this event model. Then locate
equivalent current-build routines from verified anchors and repeat the controlled
fixture. Symbol names do not transfer private ABI, offsets or behavior to 9644.
Use observation of normal calls rather than constructing private objects or
calling the factory with guessed arguments. Debugger/hook installation and this
event recorder have **not** been implemented or validated by this investigation.

## What each available channel can establish

| Channel | Useful role | Limit |
| --- | --- | --- |
| Plugin `VDJINTERFACE_SKIN` | Reload XML/PNG and observe a plugin panel | The SDK callback supplies XML; it receives no per-element parse report. The plugin's own `S_OK` is not host acceptance. |
| Plugin `GetInfo` / `GetStringInfo` | Native script HRESULT/value and independent state readback | These accept VDJScript, not arbitrary XML. Script keyword recognition does not validate an element. |
| Existing memory probe | Identify the loaded image and read guarded structures | It reads the verb table/callbacks, not skin node consumption or the live skin object graph. Finding a tag in XML memory proves only retention. |
| New bounded native trace | Observe dispatch, child-reader consumption and object insertion | Requires build/surface guards and calibration; construction still does not prove rendering or interaction. |
| HTTP | Load a fixture once, read the skin identity, read independent interaction flags | `load_skin` success alone is insufficient. No XML-validation operation was found in the documented interface. |
| Remote protocol | Subscribe to scripts and independently observe their state changes | The recorded `INFO` XML identifies the device skin; it is not a skin-parser request. No validation operation is established in the captured protocol. |

The Remote conclusion is about our [captured protocol](Remote%20Protocol.md), not
a proof that no undiscovered message exists. Testing the Remote client's skin
parser requires a fixture on that client and client-side rendering/reader evidence.
A desktop subscription acknowledging a script does not establish that a Remote
XML object was instantiated.

## Practical behavioral alternatives

- **Leaf controls:** draw a distinct solid color or literal label through the
  candidate's own reader. For an interactive control, click it and read a unique
  numeric hit flag over HTTP; pair with a nonsense-tag copy and an independent
  baseline. These are positive, context-scoped behavior tests.
- **Property nodes:** vary only the child name or placement inside a known-good
  parent; observe changed geometry/color/hit area. Reuse the established
  [conditional-child fixture](../tests/Skins/schema-condition-probe/README.md).
- **Nonvisual directives:** observe the resource or registration they create,
  using a known consumer. A visible nested object is not the appropriate oracle.
- **Diagnostic tricks:** load time, allocation totals, crashes, retained strings
  and lack of error dialogs are not reliable membership tests. They do not
  identify which node a reader consumed.

The next useful implementation is the bounded 9246 branch/child-reader recorder,
calibrated with this fixture and a recognized non-object directive. Keep a
contextual result with evidence rather than returning one global `valid: true`.

Reproduce the structural capture without attaching to a process:

```sh
just doctor
uv run --with capstone --with numpy --python .venv/bin/python3 \
  python tools/skin_validity_mechanism.py \
  --historical /Users/nom/src/virtualdj-api-reference-resources/VirtualDJ-9246.app \
  --output /tmp/skin-validity-new.json
```
