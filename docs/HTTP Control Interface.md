# HTTP Control Interface

VirtualDJ exposes a local HTTP interface that executes VDJScript actions and evaluates
VDJScript queries over plain GET/POST requests. This is the preferred probe channel for
local-test work: it replaces pad-fixture readback with scriptable request/response, needs no
skin or pad context, and returns exact strings with no transcription step.

Verified locally on 2026-07-22 against VirtualDJ 2026 (`get_version` → `2026`) on macOS with
the interface enabled and listening on `http://localhost/` (port 80). Source labels: rows
marked `Local test` below were observed directly; rows marked `Official` come from the
official wiki page.

## Provenance (Official)

The interface is the **Network Control plugin** — `GET /` on the running server returns a
page linking its official documentation:
[NetworkControlPlugin](https://virtualdj.com/wiki/NetworkControlPlugin.html) (discovered
2026-07-27 via `GET /`; settings.xml registers it as `internal://Network Control`). Official
facts from that page, none locally exercised except where noted:

- Requires VirtualDJ 2023+ and a **Pro license**. Aimed at developers.
- Install: Config → Extensions → Effects → Other → "Network Control". After install it
  appears in the Master panel's Master Effect drop-down under **Auto-Start**; its cog wheel
  opens settings.
- The **port is configurable** in those settings (80 observed locally), as is an optional
  authentication string.
- Auth, when a password is set: `Authorization: Bearer <password>` header or a
  `&bearer=<password>` URL/form parameter. Wrong auth returns an HTTP error code. Locally
  no password was set and no auth was required.
- The page documents **exactly two endpoints** — `/query` and `/execute` — for both GET and
  POST. No event, subscription, or push channel is documented.

Prefer the wrapped recipes over raw `curl` — they URL-encode the script for you:

```sh
just vdj-query 'get_effect_name 1'     # -> Phaser
just vdj-execute 'effect_active 1'     # -> true/false
just vdj-up                            # reachability check
```

## Endpoints

| Endpoint | Purpose | Response body | Source |
| --- | --- | --- | --- |
| `GET /query?script=<vdjscript>` | Evaluate a query expression | The query result as plain text | Local test |
| `GET /execute?script=<vdjscript>` | Run an action | `true` or `false` | Local test |
| `POST /query`, `POST /execute` | Same, script in the body | Same | Local test |

POST accepts the script either raw in the body with `Content-Type: text/plain`, or as a
`script=` form field with `Content-Type: application/x-www-form-urlencoded`. Both verified.
Auth (if a password is configured) is `Authorization: Bearer` or `&bearer=` — see Provenance
above; locally no password was set and no authentication was required for either method.

## No push channel (poll-only)

Probed 2026-07-27, all `Local test`:

- `GET /` returns a static HTML page pointing at the official wiki — no web UI, no asset
  tree.
- A WebSocket upgrade request (`Connection: Upgrade`, `Upgrade: websocket`) is **ignored**:
  the server answers `HTTP/1.0 200` with the same static page, no `101 Switching Protocols`.
  The server speaks HTTP/1.0, which also rules out SSE-style long-lived chunked responses in
  practice.
- `GET /events` → 404. The official page documents only `/query` and `/execute`.
- `lsof`: the VirtualDJ process has exactly one TCP listener (`*:80`, this plugin) plus its
  own mDNS socket (UDP 5353), so there is no second hidden control port *on this setup*.

Conclusion: **this channel has no event hooks — state readback is polling `/query`.** This
is a statement about the Network Control plugin only. The VirtualDJ Remote companion app
uses a completely different transport (`Local test` 2026-07-27, live iOS Remote session):
the phone advertises Bonjour type `_vdjremote8._tcp` (SRV → phone port 4243), VirtualDJ
connects **out** to the phone as the TCP client, and state flows as **event-driven push**
over that persistent connection — idle seconds carry 0 bytes, a deck load pushed ~249 KiB
desktop→phone unprompted. Port 80 is uninvolved. So push exists in the product, just not on
this channel; the Remote wire format itself is still uncharted (TODO task 8, shimming the
phone side). Details in [Application Internals.md](Application%20Internals.md) (Remote
Skins).

## Verified behavior

All rows `Local test`, VirtualDJ 2026, 2026-07-22:

| Request | Result |
| --- | --- |
| `query?script=get_clock` | `09:18 AM` |
| `query?script=get_effect_name 1` (URL-encoded space) | `Phaser` |
| `query` with no `script` parameter | HTTP 400, empty body |
| `query?script=not_a_real_verb_xyz` | **HTTP 200** with body `error:-2147467259` |
| `execute?script=nothing` | `false` — the body is the verb's own boolean result |
| `execute?script=nothing & nothing` (encoded `&`) | Chained actions accepted |
| `query?script=get_bpm 0 ? get_bpm : get_version` | `2026` — full grammar, ternaries work |
| `execute?script=deck 2 load "<absolute path>"` | `true` — loads that file onto deck 2 directly, no browser selection involved (2026-07-27) |
| `execute?script=deck 2 load "<nonexistent path>"` | **`true`** — but the deck enters an error state: title reads `Error`, `deck 2 deck_has_error` → `yes` (2026-07-27) |
| `query?script=deck 2 get_loaded_song "fullpath"` | Absolute path of the loaded file; `"filepath"` returns the folder only, `"filename"` the basename; `"path"`/`"file"` are `E_INVALIDARG` (2026-07-27) |

Gotchas the table implies:

- **HTTP status does not signal script validity.** Unknown verbs return 200 with an
  `error:<code>` body. Malformed *requests* (missing `script`) return 4xx. Always check the
  body, not just the status.
- **This channel cannot prove a verb does not exist.** `error:-2147467259` (`E_FAIL`) means
  only "this script did not evaluate here". The documented, official verb `nothing` returns
  exactly the same body as `zzz_not_a_real_verb`, on both endpoints, with or without
  arguments — because an action-only verb has no query value either way. Two *other* codes
  are positive evidence a verb exists:
  - `error:-2147024809` (`E_INVALIDARG`) — recognized, wrong arguments. Bare `browser_sort`
    returns it while `browser_sort 'title'` succeeds.
  - `error:-2147467263` (`E_NOTIMPL`) — recognized, but with no query implementation, i.e.
    an action-only verb. Verified 2026-07-27: `load`, `unload`, `browser_enter`,
    `open_stem_creator`, and `rescan_controllers` all return it from `/query`, while
    `zzz_bogus` returns `E_FAIL`. This is the cheapest existence probe the channel offers.
  - `error:-2147024891` (`E_ACCESSDENIED`) — recognized, but the context it needs is not
    available here. Returned by 27 track-metadata queries (`get_album`, `get_artist`,
    `get_bar`, `get_beat_counter`, …) with no track loaded.
  - `error:1` (`S_FALSE`) — note the **cleared** severity bit: this is a *success* code
    meaning "evaluated, and the answer is false". Returned by 26 names including
    `browser_shortcut`, `cue_pos`, and `get_firstbeat`.

  These are COM **HRESULT**s printed as signed 32-bit integers, not opaque numbers or
  leaked addresses — VirtualDJ is a Windows-first C++ codebase and carries the convention
  on macOS. Decode any new one by masking to 32 bits: bit 31 is the severity flag (which is
  why failures print as large negatives), bits 16-30 are the facility, and the low 16 bits
  are the code. `0x80004001` = facility 0, code `0x4001` (`E_NOTIMPL`); `0x80004005` =
  `E_FAIL`; `0x80070057` = facility 7 (`FACILITY_WIN32`) with code 87
  (`ERROR_INVALID_PARAMETER`), i.e. `HRESULT_FROM_WIN32(87)` = `E_INVALIDARG`.

  So `E_INVALIDARG` and `E_NOTIMPL` both prove existence; `E_FAIL` is no evidence either
  way, and a name that only ever returns `E_FAIL` stays **unresolved**, not disproved *by
  this channel*. To actually disprove a name, use the binary two-part test (`ACTION_<name>`
  symbol, else a bare string) documented in
  [Undocumented VDJScript Candidates.md](Undocumented%20VDJScript%20Candidates.md) — it has
  no false negatives across all 1,007 names this sweep proved real.
  `remote_action` is the worked counterexample: it returns `E_FAIL` on every form tried, yet
  `ACTION_remote_action` is in the binary symbol table and the name autocompletes in the
  Button Editor. `E_FAIL` never disproves a verb.
- **The whole corpus can be classified in one read-only sweep.**
  [tools/sweep_verb_existence.py](../tools/sweep_verb_existence.py) sends every name in the
  verb store (plus backticked candidates from
  [Undocumented VDJScript Candidates.md](Undocumented%20VDJScript%20Candidates.md)) as a
  bare query and buckets the result by code. 1,043 names in ~22 s on 2026-07-27, of which
  **1,007 are proven to exist**: 652 answer bare (query verbs, with the value captured),
  186 `E_NOTIMPL` (action-only), 116 `E_INVALIDARG` (takes arguments), 27 context-gated,
  26 `S_FALSE`, leaving only 36 unresolved. Ask about one name with
  `just verb-probe <name>`; re-run with `just sweep-verb-existence`.

  What this does and does not establish: it proves the name is **real** and classifies its
  **kind**, and for query verbs it captures a live sample value. It does not prove behavior,
  argument contracts, or deck scoping, so it never justifies a `test_status` of `Pass` —
  that still needs a recorded observation. Treat it as the cheap first pass that tells you
  which names are worth a real test and what shape that test should take.
- **`setting` reads configuration over this channel**, and validates names: `setting
  'iRemoteDefaultPort'` → `4243`, while an unknown key returns `E_INVALIDARG`. That makes it
  a cheap way to test whether a setting name is real. Note not every UI toggle is exposed as
  a setting — the per-device "Connect automatically" checkbox is reachable through none of
  the five `*Remote*` keys that exist (`iRemote`, `iRemoteList`, `iRemoteDefaultPort`,
  `vdjRemoteDevices`, `vdjRemoteIPs`), whose values are identical with the box on and off.
- **`false` from `/execute` is not a transport failure.** It is the action's own return value
  (`nothing` legitimately returns `false`). Treat it as evidence about the verb, not the
  channel — and note that a bogus name also returns `false`, so `false` alone proves nothing.
- **`true` from `/execute` is not proof of success either.** `deck 2 load "<nonexistent
  path>"` returns `true` while the deck lands in an error state. Verify outcomes with a
  follow-up query (`deck_has_error`, `get_loaded_song "fullpath"`), not the execute result.
- **Out-of-process loading works by path.** `deck N load "<absolute path>"` loads an
  arbitrary file onto a deck with no browser interaction, which makes external
  browser/controller frontends viable: read the library from `database.xml`, drive loads
  and transport over this channel.
- **URL-encode the whole script.** Spaces, `&` (action chaining), `?`/`:` (ternaries), and
  quotes must be percent-encoded in GET; `curl -G --data-urlencode 'script=...'` (what the
  `just` recipes use) handles all of it. The `&amp;` escaping rule is XML-only and does not
  apply here.
- Full VDJScript grammar is available — this channel evaluates the same expressions as pad
  `query=""` attributes, so grammar findings transfer both ways.

## Probe workflow

1. `just vdj-up` — confirm the interface is reachable before burning a session on fixtures.
2. Queries are read-only: use them freely for sweeps (`for` loops over `just vdj-query` calls).
3. `/execute` changes live app state. Only execute verbs the current task names, prefer
   reversible actions, and never execute `system`, file-writing, or database-touching verbs
   through this channel.
4. Record results in [VDJScript Local Test Tracker.md](VDJScript%20Local%20Test%20Tracker.md)
   with the build and the note that the run used the HTTP interface.

## GET has a URL-length limit; POST does not

`Local test` 2026-07-30. Scripts longer than roughly **2,650 characters** sent as
`GET /execute?script=…` are refused at the transport layer — the connection is reset and
VirtualDJ never sees the script. The same script over `POST` runs normally.

This matters beyond convenience: it produces a symptom identical to a VDJScript failure
(nothing runs, no error), and it caused a documented language rule to be wrong for months —
see [Chains stop after exactly 255 statements](VDJScript%20Grammar.md#chains-stop-after-exactly-255-statements).
**Use POST for any generated or long script**, and treat "nothing happened" over GET as a
transport question first.

POST bodies have their own, much higher ceiling: above roughly 9,500 characters the connection
is reset as well.

## Return values are typed underneath, rendered as text here

VDJScript queries are typed at the implementation level — the `ACTION_` vtable carries a
generic `onQuery` (a variant: bool, number and text all flow through it) plus a specialized
text query, and the Remote protocol pushes the distinction on the wire as `val` float32 vs
`txt`. This channel flattens all of that to a text body, so the type must be recovered by
observation: `just verb-return-type <name>` (334 bool / 145 int / 68 float / 4 percent /
72 text across the 652 query verbs).

### Three verbs whose bare form returns raw internals (2026-07-30)

Found by sweeping all 768 query/needs-args verbs across four argument forms
(bare, `1`, `999999`, `"zz"`) and flagging returns above 1,000,000.

| Verb | Bare form returns | What it actually is |
| --- | --- | --- |
| `master_beat_num` | `1065869312` | **float32 bits rendered through an int path.** Those bits decode to `1.06`, and successive samples give 1.06 → 2.27 → 3.49 → 4.70 — **+1.21 beats per 0.6 s, matching the deck's live 118.66 BPM (1.98 beats/s) exactly.** `master_beat_num 5` uses the correct path and returns `0.8`. |
| `get_deck_analysis` | `147167840` (`0x8c59a60`) | **Pointer-shaped**, not an analysis value: stable within a session, different in an earlier one (`0x9155a60`). Magnitude, intra-run stability and inter-run variance all fit the low 32 bits of a heap pointer — consistent with, but not proof of, a pointer. With a numeric argument it is a proper comparison predicate (`1` → `1`, `2` → `0`), the documented `get_decks` pattern. |
| `countdown` | `13314212` | Legitimate (milliseconds, decreasing ~1000/s). Only an *unparseable text* argument misbehaves, returning a stable `-1785418588` that decodes as neither a sane int nor float — a garbage path, not a leak. |

**No return value is a pointer derived from an argument.** The sweep found zero cases where
an argument *value* produced a pointer-magnitude result; all three anomalies live in the
bare/unrecognized-argument fallback path. Note that unparseable text arguments fall back to
the bare path rather than erroring — the same silent-fallback behavior that makes keyword
arguments unconfirmable by error code.

Practical impact is low — this channel already executes arbitrary VDJScript, so a leaked
heap address adds little — but treat both bare forms as **unusable for their apparent
purpose** and prefer the argument forms.

## Security note

While enabled with no password set, this is an unauthenticated control channel bound to
**all interfaces** (`*:80` per `lsof`), not just loopback — anyone on the LAN who can reach
the port can drive the decks. Leave it off when not testing, or set the bearer password in
the plugin settings if it must stay on.
