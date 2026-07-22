# HTTP Control Interface

VirtualDJ exposes a local HTTP interface that executes VDJScript actions and evaluates
VDJScript queries over plain GET/POST requests. This is the preferred probe channel for
local-test work: it replaces pad-fixture readback with scriptable request/response, needs no
skin or pad context, and returns exact strings with no transcription step.

Verified locally on 2026-07-22 against VirtualDJ 2026 (`get_version` → `2026`) on macOS with
the interface enabled and listening on `http://localhost/` (port 80). Source labels: rows
marked `Local test` below were observed directly; the Authorization note is `Official`
(interface description) and not yet locally exercised.

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
POST is documented to use the `Authorization` header; locally, no authentication was required
for either method (`Official`, untested — revisit if a remote-access password is set).

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

Gotchas the table implies:

- **HTTP status does not signal script validity.** Unknown verbs return 200 with an
  `error:<code>` body. Malformed *requests* (missing `script`) return 4xx. Always check the
  body, not just the status.
- **This channel cannot prove a verb does not exist.** `error:-2147467259` (`E_FAIL`) means
  only "this script did not evaluate here". The documented, official verb `nothing` returns
  exactly the same body as `zzz_not_a_real_verb`, on both endpoints, with or without
  arguments — because an action-only verb has no query value either way. A different code,
  `error:-2147024809` (`E_INVALIDARG`), does mean the verb was recognized and the arguments
  were wrong: bare `browser_sort` returns it while `browser_sort 'title'` succeeds. So
  `E_INVALIDARG` is positive evidence a verb exists; `E_FAIL` is no evidence either way, and
  a name that only ever returns `E_FAIL` stays **unresolved**, not disproved.
- **`false` from `/execute` is not a transport failure.** It is the action's own return value
  (`nothing` legitimately returns `false`). Treat it as evidence about the verb, not the
  channel — and note that a bogus name also returns `false`, so `false` alone proves nothing.
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

## Security note

While enabled, this is an unauthenticated local control channel for the app. Leave it off when
not testing, and do not expose port 80 beyond localhost.
