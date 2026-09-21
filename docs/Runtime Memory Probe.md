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
