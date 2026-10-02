# Offline parser host

## Symbol-rich host — 2026-09-30, build 18.0.9246, arm64

The symbol-rich build now has its own offline host. Both the
[initial run](../tests/offline-parser-9246-initial.json) and the
[confirmed run](../tests/offline-parser-9246.json) loaded the converted image,
passed the build-specific code guards, parsed the fixed `is_using` suite, and
released its objects. The confirmed preparation also checks that the named
routines and `ACTION_is_using` vtable remain in the converted library.

The source was the unpacked historical app under
`/Volumes/nom/src/virtualdj-api-reference-resources/unpacked/9246/vdj.pkg/Payload/VirtualDJ.app`.
Its full hash and UUID match the prior 9246 memory-anchored extraction. The
installed 9644 application and the source archive were not changed. The built
worker and symbol-bearing library from the confirmation run are in
`/private/tmp/vdj-offline-parser-9246-confirmed`; these are temporary products,
reproducible with the commands below, not checked-in vendor binaries.

**Comparison scope:** the observed action class, raw parameter tags/payloads/text
and release result match the existing **9644** live parser-object baseline. This
is a cross-build comparison. There is no same-build 9246 live parser-object
capture, and matching these fixed inputs does not establish equivalence of the
full language. No action evaluation or skin parsing was performed.

The [9246 guard manifest](../tests/parser-object-layout-9246.json) was recovered
from named methods and same-build RTTI, independently of the 9644 addresses:

- `IAction::create(char const*, char const**, int)` and its call from
  `CPlugin::GetInfo` establish the callable boundary and argument setup.
- `IAction::getParam(int)` supplies the parameter-vector start/end and stride;
  the named vector append helper supplies its end/capacity relationship.
- `IAction::IAction()` and `CPlugin::GetInfo` supply reference initialization and
  release; the RTTI-linked deleting destructor supplies the cleanup target.
- `SActionParam::toFloat`, `toString` and its destructor support the inspected
  payload and string representation. The fixed suite uses short text only.

The manifest retains routine names, exact bounds, code hashes, bounded
disassembly and the reviewed instruction patterns behind the layout. These are
Tier 2 structural findings, complemented by the separately recorded offline
execution. They are not promoted to verb behavior conclusions. The extractor is
specific to this binary; it rejects a different hash or changed reviewed pattern.

Reproduce the named manifest using the optional extraction dependencies:

```sh
uv run --with capstone --with numpy --python .venv/bin/python3 \
  python tools/prepare_symbol_parser.py --check \
  --app '/Volumes/nom/src/virtualdj-api-reference-resources/unpacked/9246/vdj.pkg/Payload/VirtualDJ.app'
```

Build and run a fresh copy (use new work/capture paths):

```sh
just doctor
just offline-parser prepare \
  --app '/Volumes/nom/src/virtualdj-api-reference-resources/unpacked/9246/vdj.pkg/Payload/VirtualDJ.app' \
  --work /private/tmp/vdj-parser-9246-new
just offline-parser run --work /private/tmp/vdj-parser-9246-new --output /private/tmp/vdj-parser-9246-new.json
just offline-parser check --output /private/tmp/vdj-parser-9246-new.json
```

Preparation selects the manifest from the app's exact build, verifies the full
binary hash and generates a private header for that worker. Layout offsets and
addresses come from the selected manifest. Saved 9644 captures remain immutable
and continue to validate. `just offline-parser-check` checks both builds offline.
The [9644 regression capture](../tests/offline-parser-9644-generated-guards.json)
also reruns the fixed suite with the shared host's newly generated guard header;
it matches the same-build live baseline after this refactor.

This is the preferred discovery host for the next bounded investigation of
compound action objects; use the current build to test selected compatibility
questions. Arbitrary scripts and XML construction remain outside this host's
fixed allowlist.

## Bounded result — 2026-09-30, build 18.0.9644, arm64

A copy of the installed executable loaded as a library in a standalone native
worker and parsed the fixed `is_using` suite from the earlier in-app plugin.
The confirmed [capture](../tests/offline-parser-9644.json) matches the saved live
baseline's action class, raw parameter tags/payloads/text, and successful object
release. Each case ran in a fresh process. No parsed action was evaluated, no
`GetInfo` callback was called, and the installed application was not launched,
restarted, or instrumented by this experiment.

This is **offline execution of vendor code compared with a prior live capture**,
not a new live behavior result or a per-verb status promotion. The live baseline
is [parser-objects-9644.jsonl](../tests/parser-objects-9644.jsonl), described in
[Runtime Memory Probe](Runtime%20Memory%20Probe.md#parser-objects--2026-09-21-build-1809644-arm64).
The comparison deliberately excludes its evaluation HRESULT and numeric result.
Real and nonsense text both survive parsing; keyword validity remains a separate
consumer question. No skin parser was called.

Inspect and validate without running vendor code:

```sh
just offline-parser-check
```

The observed boundary is `IAction::create(char const*, char const**, int)` with
the existing fixed inputs, a null end-pointer argument and zero flags. The host
accepts only the previously verified `ACTION_is_using` vtable, parameter span,
tags and reference count. It uses the guarded deleting destructor after dropping
its sole reference. Unexpected objects are left to worker exit, never evaluated
or freed through a guessed layout. Success does not establish grammar coverage,
arbitrary-script safety, or a reusable private ABI.

## What made the standalone call possible

[The converter and runner](../tools/offline_parser.py) reject any source whose
full hash differs from the existing parser-layout manifest. They save that
source in a new temporary directory, extract its arm64 slice, change `MH_EXECUTE`
to `MH_DYLIB`, clear `MH_PIE`, remove `LC_MAIN`, empty but preserve `__PAGEZERO`,
and add a library ID. File-backed section bytes are checked unchanged before
ad-hoc signing. Segment order and other load commands remain in place.

This binary uses classic `LC_DYLD_INFO_ONLY`; the converter rejects chained-fixup
layouts. It bounds command and section records, rejects insufficient header
space, and is not a general executable-to-library converter. The initializer
table's location, size and hash are retained in the confirmed preparation record;
its entries were allowed to run under the tested sandbox, not individually
classified as harmless.

The worker has a copied Breakpad framework at the executable-relative path the
image expects. Dependency contents and symlink targets are recorded and checked
before execution. No application resource tree or defaults were supplied. That
was sufficient for these fixed cases; other parser routes may require more state.

[The native host](../tools/plugin/offline_parser_host.cpp) locates the converted
image separately from its own executable and checks the vendor UUID and existing
routine fingerprints at that image's slide. The in-app probe's image-zero and
installed-path assumptions are not reused. On success it releases the parsed
object, flushes its capture, and uses `_Exit` to skip unreviewed global exit
handlers. It does not test unloading or repeated use of one loaded image.

## Execution boundary and retained attempts

Before any library load, a separate worker verifies that writing inside its work
directory succeeds, while opening the real home directory, writing outside the
work directory, and making a loopback network connection are denied with `EPERM`.
The profile denies network operations, home-directory reads, writes outside the
temporary tree, and execution of programs other than the host. The host and
supervisor have deadlines; core dumps are disabled. These are tested controls,
not a claim that every OS interaction or initializer was audited.

- [Initial attempt](../tests/offline-parser-9644-initial.json): the enclosing tool
  sandbox prevented applying the worker sandbox. No vendor code loaded.
- [First sandboxed run](../tests/offline-parser-9644-sandbox-initial.json): the
  control worker, library load and fixed parse suite completed. Its stored fields
  are retrospectively compared with the live baseline by the unit tests.
- [Confirmed run](../tests/offline-parser-9644.json): separately prepared copy and
  fresh workers, with comparison required after every case before continuing.
  Records exact worker arguments, environment, profile and provenance hashes.

The first attempts retain the original full initializer-address listing; the
confirmed preparation uses the bounded section fingerprint instead. Historical
captures are not rewritten when tooling changes.

## Reproduction and next boundary

Requires the exact installed build, Apple arm64 compiler tools and macOS
`sandbox-exec`; no plugin SDK headers are required. Use a new work directory and
a new capture filename each time:

```sh
just doctor
just offline-parser prepare --work /private/tmp/vdj-parser-new
just offline-parser run --work /private/tmp/vdj-parser-new --output /private/tmp/vdj-parser-new.json
just offline-parser check --output /private/tmp/vdj-parser-new.json
```

If an enclosing sandbox prevents installing the worker policy, use the normal
approved execution mechanism to run the **same sandboxed runner**. Do not remove
the worker policy or run the host unsandboxed. Preparation never edits the
installed executable; copied binaries remain outside the repository.

The next script milestone is to identify and guard the object layouts and release
paths for compound expressions before expanding the fixed suite to chains,
conditionals and scope wrappers. The worker can then supply native structural
comparisons for an independent linter/compiler front end. It currently provides
no source spans or stable serialized intermediate representation.

Skin work needs a separate entry-point and ownership investigation: XML node
construction first, then a bounded skin-object factory route. This pilot does
not justify assuming those paths can run without window, image, template or
rendering context. Keep the partial candidates in
[Skin Schema Recovery](Skin%20Schema%20Recovery.md) separate from accepted syntax
and observed rendering behavior.
