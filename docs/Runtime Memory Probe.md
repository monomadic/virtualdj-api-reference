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

The memory plugin accepts a VirtualDJ app bundle at any installation path. It
requires the main bundle identifier `com.atomixproductions.virtualdj`, verifies
that the loaded main image is that bundle's executable (resolving symlinks), and
retains the arm64 and bounded Mach-O checks. This identity check is not signature
verification. For an alternate or historical app, pass its executable explicitly
to `just plugin-memory-check CAPTURE --binary '/path/VirtualDJ.app/Contents/MacOS/VirtualDJ'`.
The collector still rejects UUID, build, table-address or record mismatches.
This path flexibility applies only to the read-only memory probe; it does not
relax the separate private-parser probes' build guards. A successful compilation
does not establish live compatibility with an untested historical build.

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

The follow-up parser-object experiment below tests this candidate with fixed
inputs and additional code/ownership guards. It does not make these addresses a
supported or general-purpose API.

For agents: use the small verified JSON artifact and the commands above. Do not
read raw process dumps or create a second Markdown list of verb records.

## Parser objects — 2026-09-21, build 18.0.9644, arm64

A **separate experimental plugin**, `VDJParserProbe`, now calls the parser candidate
on a fixed list of `is_using` inputs. This expands beyond the memory-only probe's
no-private-calls scope. The calling convention is supported by the current public
callback call sites and the historical named `IAction::create(char const*, char
const**, int)` signature. Current consumer code supplies the parameter-vector
layout; the public callback and current deleting destructor supply the release
sequence. The [guard manifest](../tests/parser-object-layout-9644.json) records the
exact image, vtable, function bounds and code hashes. The historical address is
not called or transplanted.

Before calling private code, the plugin checks the loaded build, architecture,
UUID and SHA-256 of every guarded code interval. It accepts only the expected
`ACTION_is_using` vtable, a reference count of one, and a bounded parameter span.
It copies only tag/payload fields and input-matching text, then atomically releases
its reference and calls the verified deleting destructor. It never evaluates or
executes that private object. Separately, public `GetInfo` evaluates the same
fixed script to obtain its HRESULT. Thus this is live object inspection, **not a
hook observing the object created inside a particular SDK call**.

The [live capture](../tests/parser-objects-9644.jsonl) completed two identical
rounds within one load; the [run journal](../tests/parser-object-run-9644.json)
records context, bundle/capture hashes and before/after checks. All four decks
were stopped and unloaded, and remained so. Every expected release call returned.
The earlier [discovery attempt](../tests/parser-object-run-9644-initial.json)
returned an empty title and produced no parser capture before restart.

Observed representation and recognition, scoped to this fixture:

- `cue`, quoted `cue`, and both nonsense controls became text parameters in the
  same action class. Nonsense was **retained**, not discarded by this parse.
  Public evaluation distinguished `cue` (`S_OK`) from nonsense (`E_NOTIMPL`).
- Bare `is_using` yielded an empty parameter vector and public `E_INVALIDARG`.
- The second arguments `7`, `7.5`, `1000ms` and `50%` produced distinct integer,
  decimal, millisecond and percentage tags. The percentage payload was float32
  `0.5`; the millisecond payload was float32 `1000`. `just parser-objects` prints
  all decoded fields from the capture, avoiding another hand-maintained table.
- No conclusion about recency, timing, or whether the extra arguments affect
  behaviour follows from these results. `is_using` remains behaviour-Untested.
- The rounds are repeats within one run, not independent sessions. Object layout
  is measured for these cases on this build, not a public or portable ABI.

Reproduction:

```sh
just plugin-parser-test
just plugin-parser-build --install
just vdj-query "get_effect_title 'VDJParserProbe'"
just parser-objects
```

`parser-<pid>-<time>.jsonl` is written in the same working directory as the memory
probe. The last command validates the committed capture by default; pass a new
capture path to validate another run. A cached plugin may not rerun `OnLoad`.
Do not overwrite an in-use bundle expecting it to reload. A newly installed name
required a restart in this session. Normal quit left an idle process without
UI/HTTP; SIGTERM and relaunch restored the app before the first parser call. The
cause of that shutdown issue is unresolved; it is not evidence of parser failure.

Failure handling is bounded: an unexpected class or shared reference count aborts
rather than guessing a destructor or freeing someone else's reference. Such an
abort can retain one parser allocation until app exit. The happy path was observed;
private API changes can still invalidate assumptions outside the guarded intervals.
This tool is deliberately not a general arbitrary-script parser service.

**Next useful discovery target:** the consumer's keyword comparisons, joined to
these typed parameters. This run shows why dumping parsed objects alone will not
enumerate valid tails: real and nonsense text both survive parsing. Keep any
consumer-derived list as candidates until a discriminating runtime test validates
it. Use the parser instrument for argument types, units and binding questions.

## Consumer keyword pass — 2026-09-21, build 18.0.9644, arm64

`just is-using-keywords` joins the
[current consumer extraction](../tests/is-using-consumer-9644.json) to the native
captures named and hashed in the [run journal](../tests/is-using-keyword-run-9644.json).
The extractor locates `ACTION_is_using` through current RTTI and its query vtable
slot, then records exact direct literal-setup/comparison sites and helper bodies.
It accepts only a contiguous ADRP/ADD/MOV/BL pattern, checks the helper's text-tag
and literal-length checks, and keeps source register/callsite provenance. This is
bounded Tier 2 extraction, not transitive analysis or a complete keyword schema.

The separate **VDJKeywordProbe** uses public `GetInfo` and `GetStringInfo` only.
It has no private parser calls and never executes the scripts it queries. Its
compiled [case list](../tests/is-using-keyword-cases.json) includes every recovered
literal in first position, nonsense controls, quoted/uppercase `cue`, and later
`inaudible` positions paired with nonsense at the same positions.

The captures agree across rounds and repeat triggers in one stopped/unloaded
session. First-argument `cue`, `effect`, `equalizer`, `filter`, `load`, `loop`,
`loopsize`, `pads`, `sample` and `stems` returned native `S_OK` and `off` text.
`inaudible` in first position matched the nonsense controls: numeric `E_NOTIMPL`
and empty text with `S_FALSE`. Bare `is_using` returned numeric `E_INVALIDARG`.
Quoted and uppercase `cue` matched lowercase `cue` in this fixture.

The consumer compares `inaudible` against later parameter values, whereas its
feature comparisons use the first parameter (see recorded parameter setup and
callsite registers). This is a **structural modifier lead**. Both later-position
forms in the live suite matched their nonsense-tail controls; their behaviour is
unresolved in this fixture. Do not turn a string recovered from this routine into
a first-argument keyword without checking its role. No new keyword was found
relative to the existing vocabulary, and behaviour remains Untested.

Commands:

```sh
just plugin-keywords-build --install
just vdj-query "get_effect_title 'VDJKeywordProbe'"
just is-using-keywords
```

The first title query loaded the plugin and captured without selecting an effect
slot. To repeat the fixed sweep in the loaded plugin, read its button state first,
then use `effect_button 'VDJKeywordProbe' 1` and explicitly restore `off` if the
starting state was off. In this run the bare button action captured but stayed on;
repeating the bare action did not turn it off. The explicit `off` restore was
independently read back as `no`. The journal preserves that initial restore failure
and final successful restore. Multiple callbacks can produce multiple captures;
never infer capture count from the number of actions. Files are
`keywords-<pid>-<time>-<serial>.jsonl` in the shared probe working directory.

Re-extract the structural evidence without touching the canonical vocabulary:

```sh
uv run --with capstone --python .venv/bin/python3 python tools/is_using_consumer.py \
  --check tests/is-using-consumer-9644.json
python3 -m unittest discover -s tools -p test_is_using_keywords.py
```

For future agents, query the compact join before opening disassembly. This pass
supports the method **consumer comparisons → position-aware candidates → native
recognition controls**. For `inaudible` behaviour, the next fixture must actually
separate audible from inaudible use while controlling timing; another idle sweep
will not answer it. For broader discovery, apply the method to a verb whose
consumer vocabulary is unresolved rather than repeating this settled list.

## Shared time reader follow-up — build 18.0.9644 arm64

[time-sign-consumer-9644.json](../tests/time-sign-consumer-9644.json) follows
the current `ACTION_get_time_sign` query slot to its single direct callee.
The wrapper at `0x1004f2a9c` calls the shared reader at `0x1004f268c`;
the artifact preserves bounded instructions, literal callsites and helper hashes.
This is **Tier 2 structural evidence**, not an argument or behaviour promotion.

The shared reader contains literal comparison sites for `elapsed`, `remain`,
`total`, `loopin`, `loopout`, `absolute`, `cue` and `to_lyrics`. Parameter zero
is fetched into `x23`; `x24` points to its string storage. A later `absolute`
comparison uses parameter one (`x22`). The `cue` helper requires at least three
characters and compares the first three; the caller then passes the suffix to
another routine. Thus `cue` is a **prefix-family lead**, not evidence that only
the standalone token is accepted. Suffix grammar remains unresolved.

Two structural details change the probe plan:

- Deck-data checks branch to failure before parameters are read. An unloaded
  deck therefore cannot discriminate this consumer's keywords, even with native
  HRESULTs.
- Unmatched first-position text reaches the same continuation as `elapsed`.
  A positive elapsed-time sign is consequently a poor nonsense control. The
  wrapper also has a zero-output branch, which remains a live-test lead.

The read-only [empty-deck capture](../tests/time-sign-empty-9644.json), on live
build 9644, returned HTTP `error:1` for every form listed in the capture, including
both nonsense controls, in both rounds. Decks 1–4 were stopped and unloaded before
and after. This establishes only the measured unavailable result in that fixture;
it does not prove any tail invalid, nor recover the native HRESULT from HTTP.

Reproduce the bounded extraction and empty control:

```sh
uv run --with capstone --python .venv/bin/python3 python tools/time_sign_consumer.py \
  --check tests/time-sign-consumer-9644.json
python tools/probe_time_sign_empty.py --output /tmp/time-sign-empty-new.json
```

The next discriminating fixture should use generated audio, remain stopped, and
read zero and negative elapsed positions against positive remaining/total time,
with two nonsense controls. Establish that the requested position actually took
effect before interpreting sign results. Loop, cue-prefix and lyric-relative
leads need separately prepared markers/content. Do not repeat the earlier
positive-time sweep or promote static branches to supported syntax.

For future agents, the tail queue's full JSON includes extensive helper evidence.
Project only verb names, open tails and candidate fields when choosing work;
open a selected record afterwards. A full queue dump consumes context without
improving target selection.

### Stopped position fixture — 2026-09-22, build 18.0.9644 arm64

[time-sign-positions-9644.json](../tests/time-sign-positions-9644.json) records
two independently loaded runs using generated, silent 60-second WAV audio.
Each tests stopped positions 0 ms and 1000 ms under elapsed, remain and total
display modes, with forward/reversed query order and reversed phase order in
the second run. `get_position & param_multiply 60000` independently verifies
each position. The companion journal records write intent before each action;
neither actions nor uncertain writes are retried.

At position zero, both runs produced:

| Form | Elapsed display | Remaining display | Total display |
| --- | --- | --- | --- |
| bare | 0 | 1 | 1 |
| `elapsed` | 0 | 0 | 0 |
| `remain` | 1 | 1 | 1 |
| `total` | 1 | 1 | 1 |
| `absolute` | 0 | 1 | 1 |
| either nonsense control | 0 | 0 | 0 |

At 1000 ms all tested forms returned 1. **Zero is an observed return value**,
despite the vendor description naming only -1 and +1. `remain` and `total`
separate from nonsense at zero; their measured sign is positive. Bare form
follows the selected display mode. `absolute` follows that mode in this fixture,
but this does not establish its pitch-scaling semantics. Explicit `elapsed`
returns zero even when the display mode is remaining/total, but matches both
nonsense controls; its fallback-equivalent recognition remains unresolved.

The [initial aborted attempt](../tests/time-sign-positions-9644-initial.aborted.json)
requested `goto -1000ms` after establishing zero. The independent position
readback stayed zero, so the runner aborted and restored the starting state.
This does not establish whether the seek was clamped or the position reader
hides negative positions. **Negative-sign behavior remains untested.** The
completed runs omit that unavailable phase. All attempts verified restoration
of empty/stopped state, pitch and display mode; no playback was started.

```sh
python tools/probe_time_sign_positions.py --check tests/time-sign-positions-9644.json
python -m unittest discover -s tools -p test_time_sign_positions.py
# New capture, requiring an empty stopped deck 1:
python tools/probe_time_sign_positions.py --output /tmp/time-sign-new.json
```

`--include-negative` reproduces the attempted negative setup and aborts if its
position cannot be established. Future work should first resolve negative-position
readback/seek behavior, rather than repeat this now-discriminating zero fixture.

### Loaded long_time boundaries — 2026-09-22, build 18.0.9644 arm64

Local test over HTTP: [time-sign-loaded-9644.json](../tests/time-sign-loaded-9644.json)
reuses `probe_long_time.audio()` and the named `long_time` fixture. Independent
unload/reload runs in the same application session reverse phase/form order;
`--repeat 3` samples each form in each stopped state under each display mode.
The capture embeds exact queries, readbacks, write intent and restoration.

**Negative elapsed is reachable.** Both `goto -1000ms` from zero and
`goto -0.013333333333%` establish elapsed **-1000 ms**, remaining **7501000 ms**.
`get_position` and its scaled readback still return zero before start. Thus the
older position-only rejection above did not establish that seeking had failed.
The retained runner verifies signed `get_time 'elapsed' 'absolute'` and
`get_time 'remain' 'absolute'` together, retaining the position readback too.
Start (0 ms) and end (7500000 ms, remaining zero) were also verified in both runs.
No requested state was skipped in the confirmed capture; playback stayed stopped.

| Explicit form | Start | Before start (-1000 ms) | End | Argument conclusion |
| --- | --- | --- | --- | --- |
| `elapsed` | 0 | -1 | 1 | UNDISCRIMINATED; matches both controls |
| `remain` | 1 | 1 | 0 | Recognized; separates at every boundary in both runs |
| `total` | 1 | 1 | 1 | Recognized; separates at start and before start in both runs |
| `elapsed absolute` | 0 | -1 | 1 | UNDISCRIMINATED; matches first- and second-slot controls |
| Either first-slot nonsense token | 0 | -1 | 1 | Elapsed fallback observed |

Bare form follows `display_time`; explicit forms above have the same results
under elapsed, remain and total display modes. `absolute` here is the **second
argument**, not a one-token string containing a space, and not a standalone
first-argument claim. Its recognition and pitch-scaling semantics remain open;
zero pitch and sign alone do not discriminate them. No tail is marked Fail.

The [initial aborted attempt](../tests/time-sign-loaded-9644-initial.aborted.json)
and its [journal](../tests/time-sign-loaded-9644-initial.journal.jsonl) retain an
HTTP read timeout and verified restoration. The subsequent
[position-only initial capture](../tests/time-sign-loaded-9644-initial.json)
skipped negative states despite recording signed elapsed -1000 ms; it is
superseded by the confirmed signed-readback capture. Read-only queries may retry
once after a timeout; writes never retry. Every attempt restored and verified the
original empty/stopped deck, pitch and remaining-time display mode.

```sh
python tools/probe_time_sign_loaded.py --check tests/time-sign-loaded-9644.json
# Requires an empty, stopped deck 1; writes a new capture only:
python tools/probe_time_sign_loaded.py --output /tmp/time-sign-loaded-new.json --repeat 3
```

For future agents: inspect `just verb get_time_sign` and this compact matrix,
not the embedded request journal. The focused coverage query now reads this
capture. Do not repeat positive-midpoint sweeps or use `get_position` alone to
reject negative elapsed. Next: prepare loopin/loopout markers, cue-prefix suffix
fixtures, and lyric content for `to_lyrics` separately; these were out of scope.

## Relocated historical host — 2026-09-22, build 18.0.9246, arm64

The updated memory probe produced a [verified capture](../tests/plugin-memory-9246.json)
from the unpacked historical app. Its image UUID, build, table address and all
name/id/flags records matched that executable. The [HTTP observation record](../tests/plugin-memory-run-9246.json)
retains the responding plugin title and the limits of the session-state checks.
This confirms memory-capture compatibility with this relocated build; it does not
validate private parser calls or skin XML behaviour. Future historical captures
should use `--binary` with the exact app executable instead of the collector's
current-installation default.

## Named tail-consumer pilot — 2026-09-22, build 18.0.9246, arm64

**Result:** memory anchoring plus named consumer dataflow is a useful way to assess
tail candidates. It is not a universal valid-argument oracle. The fresh
[memory capture](../tests/tail-probe-9246-memory.json) matched the historical
executable's UUID, build, verb-table address and every record. The
[run journal](../tests/tail-probe-9246.json) brackets each plugin title query with
a directory inventory, establishing that each produced a new capture in this run.
The installed application was build 9644 while HTTP and the captured image were
9246: use the actual executable passed to the verifier, not the default app path.

The [consumer artifact](../tests/tail-consumers-9246.json) records exact routine
bounds/hashes, named comparison call sites, possible parameter indices, unresolved
receivers, and a direct-call inventory of parameter helpers. It follows both
control-flow branches and traces `IAction::getParam(int)` results into parameter
text or `SActionParam::isTxt` comparisons. Parameter indices are zero-based.
This is **Tier 2 disk analysis anchored to live memory identity**, not a hook
observing those instructions executing. The parameter accessor and string-member
models remain structural ABI assumptions; no private routine is called.

The useful calibration cases are:

| Consumer | Structural result on build 9246 | Live result in this run |
| --- | --- | --- |
| `filter_label` | `name` and `clean` compare with parameter 0. `Skin`, `BASS`, and `FILTER` go to `CMessageEngine::getMessage`. The lowercase `filter` comparisons have unresolved receivers. | `clean` returned `OFF`; bare, `name`, both nonsense controls and the other tested strings returned `DELAY`, agreeing in both rounds. Only `clean` separated in this fixture. |
| `is_using` | Feature comparisons trace to parameter 0; `inaudible` comparisons trace to parameters 1 and 2. Another `filter` comparison has an unresolved receiver. | The fixed native suite distinguishes first-position feature tokens from nonsense. First-position `inaudible` matches nonsense; the later-position modifier pairs remain indistinguishable in this fixture. |
| `get_song_event` | `current`/`next` comparisons trace to parameter 0; `hasbeats`, `volume`, `volume_end`, and `remaining` to parameter 1. `getEvent()` also examines parameter 0. | Not re-probed: this pass recovers input provenance, not the full branching/fallback grammar or song-event behavior. |
| `get_time_sign` | Its query delegates to named `ACTION_get_time::getTime(long long&, SActionParam*&)`. | Not re-probed: the shared consumer is explicitly retained as an unexpanded edge. An empty local literal list does not imply no tails. |

The [native capture](../tests/tail-probe-9246-native.jsonl) uses the existing
`VDJKeywordProbe` compiled suite. On this build, feature-token queries returned
numeric `S_OK` and text `off`; nonsense returned numeric `E_NOTIMPL` and empty
text with `S_FALSE`; the bare query returned numeric `E_INVALIDARG`. This supports
recognition in the measured fixture, not activity/timing behavior. Both rounds
agree within one capture; they are not independent application sessions.
The preceding [initial attempt](../tests/tail-probe-9246-initial.json) completed
both plugin captures but stopped before retaining HTTP label results because
the runner's output allowlist omitted the built-in `DELAY`/`OFF` readings. Its
captures remain under initial names. The corrected run completed.

All four decks were stopped and unloaded before and after. No execute calls,
effect selections, restart, private parser calls or heap scan were used.
Hardware/account context was not inventoried. The observation does not establish
that every other part of application state was unchanged. No verb-store status
was promoted from these structural or recognition findings.

### Other useful targets

- **Exact public callback names.** The live callback addresses resolve to
  `CPlugin::SendCommand`, `GetInfo`, `GetStringInfo`, `DeclareParameter` and
  `GetSongBuffer`; `callback_symbols` retains the same-build mapping. This makes
  future wrapper/context investigations easier without cross-build addresses.
- **Typed and evaluated arguments.** The helper inventory exposes direct ACTION
  callers of `getBoolParam`, `getFloatParam`, `getParamEval`, `getFloatParamEval`,
  `SActionParam::toFloat`, `toString`, `toColor`, and the text-comparison templates.
  These are useful routes for deciding which consumers need unit, expression or
  coercion tests. Caller-site totals are queried with `--helpers`, not copied
  into prose. Shared-base calls, indirect calls and inlining remain outside it.
- **A tempting but unproven list API.** `getListParam(int, int&, char const*, int)`
  is present, but the named ACTION direct-BL inventory finds no callers. Do not
  assume it exposes a per-verb enumeration service. Inspect shared callers and
  its list representation before considering a bounded private-call experiment.
- **Parameter serialization.** Named `SActionParam::serialize` and `unserialize`
  offer leads for typed round-trip fixtures. Names alone establish neither the
  serialized format nor that it is safe to apply to arbitrary live objects.
- **Editor assistance and scope.** `DLGActionWizard::updateList`, `updateHint`,
  `getCurrentWord`, its `deckArguments` data symbol, and `IAction::setSource`
  offer targeted routes for editor suggestions and source/deck binding. These
  remain symbol leads; the current pilot does not claim to read their data or
  establish their behavior.

### Reuse and next experiment

```sh
just tail-consumers filter_label
just tail-consumers is_using
just tail-consumers get_song_event
just tail-consumers get_time_sign
just tail-consumers --helpers
just tail-consumers --leads
just tail-consumers-test
```

Queries use only the standard library. Re-extract with `tools/tail_consumers.py
--binary /path/to/9246/VirtualDJ.app/Contents/MacOS/VirtualDJ --check` under the
optional capstone environment used above. The default memory anchor is the fresh
`tail-probe-9246-memory.json`. To repeat the read-only live calibration, use
`tools/probe_tail_consumers.py --binary /path/to/9246/VirtualDJ.app/Contents/MacOS/VirtualDJ
--output tests/tail-probe-9246-new.json`; it refuses existing outputs and requires
stopped/unloaded decks. A cached or absent plugin that produces no new capture
aborts rather than silently reusing old evidence.

The default report is a short human-readable view; `--format=json` retains
callsite, receiver, routine and uncertainty details for focused follow-up.

The recommended next step is to extend this position-aware analysis through
shared consumers, starting with `ACTION_get_time::getTime`, and carry every
unexpanded call forward. Use the resulting input comparisons to select runtime
fixtures. Keep localized output strings and unresolved internal comparisons out
of any *confirmed* argument list, but do not globally disprove a token from this
bounded pass. A runtime branch trace could resolve default-versus-recognized
paths that return the same result, but would require a separate guarded instrument;
the present memory plugin does not provide it.
