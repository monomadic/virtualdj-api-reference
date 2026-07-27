# VirtualDJ Remote Protocol

Wire protocol between VirtualDJ (desktop) and the VirtualDJ Remote companion app. This is
**not** the [HTTP Control Interface](HTTP%20Control%20Interface.md) — different transport,
different port, different semantics. Where that channel is request/response and poll-only,
this one is a **push subscription channel**: the device registers VDJScript queries by id
and VirtualDJ streams values back as they change.

All rows `Local test` unless marked otherwise, captured 2026-07-27 against VirtualDJ 2026
on macOS with a real iOS Remote app (app build `8515`) on the LAN. Nothing here is official
documentation; the protocol is undocumented and this is black-box observation.

## Transport and discovery

| Fact | Detail |
| --- | --- |
| Roles | **Inverted from the obvious guess.** The *device* is the TCP server; VirtualDJ is the client and dials out. |
| Discovery | The device advertises Bonjour/mDNS service type `_vdjremote8._tcp` (SRV → device host, port 4243 observed). VirtualDJ browses for it. |
| Port | `4243`, from the `iRemoteDefaultPort` setting in `settings.xml` (configurable). |
| Device list | `settings.xml` `<vdjRemoteDevices>` is the discovered/paired list by *instance name*; entries appear in Config → Controllers → Phone/tablet with a liveness suffix (`(Waiting)`, `(Not here)`). |
| Auto-connect | With "Connect automatically" checked, VirtualDJ redials ~5 s after a session ends. After several failed sessions it parks the device at `(Waiting)` and stops until the user clicks Connect. |
| Who speaks first | **The device.** Across 8+ sessions VirtualDJ opened the connection and sent *zero* bytes, holding the socket open for minutes. A fake device that stays silent learns nothing; a fake device must speak first. Eight candidate openers (newline, text, HTTP, XML, four binary framings) all drew silence — the real opener is required. |

Consequence for tooling: any third-party client impersonates a *device* — advertise
`_vdjremote8._tcp`, listen on the port, and send the opener. You do not connect to
VirtualDJ; it connects to you. No root and no packet capture is needed anywhere in this
flow, because the device end is a plain TCP server you can dial directly.

## Framing

Every message is one frame:

```text
+--------+--------+------------------+
| "8JDV" | u32 LE | payload          |
| 4 bytes| total  | total - 8 bytes  |
+--------+--------+------------------+
```

- Magic is the ASCII bytes `38 4a 44 56` = `8JDV` on the wire — a fourcc `'VDJ8'` stored
  little-endian.
- The length field is the **total frame size including the 8-byte header**, not the payload
  size. A minimal frame is `0c 00 00 00` (12) with a 4-byte payload.
- Payload begins with a `u16 LE` **message type**. Frames are packed back-to-back in the
  stream, several per TCP segment, so a reader must buffer and split on the length field.

Deck scope is a fourcc stored little-endian, so it reads reversed in a hexdump: `74 66 65 6c`
is `'left'`, `72 69 67 68` is `'righ'` (i.e. `right`), all-zero means unscoped/global.

## Message types: device → desktop

From a real device's 1184-byte opening burst (49 frames), sent immediately on connect:

| Type | Name (working) | Payload after the u16 type | Meaning |
| --- | --- | --- | --- |
| `0x0001` | SUBSCRIBE | `u16 id`, `fourcc scope`, ASCII VDJScript | Register a query under `id`; VirtualDJ pushes its value when it changes. |
| `0x0003` | KIND | `u16 kind`, `u32 id` | Declares the value type for `id`. Observed `0` (numeric: `pitch`, `volume`, `get_vu_meter`, `crossfader`), `1` (string: `get_artist`, `get_title`, `get_bpm`, `get_status`), `2` (`search_options`, `sampler_used`, `automix`). |
| `0x0024` | PANEL | ASCII name | Declares an available view: `playlist`, `sampler`, `sidelist`, `karaoke`, and one empty. |
| `0x0040` | INFO | `u32`, then XML | Device announcement (see below). |
| `0x0009`, `0x000c`, `0x0027`, `0x0029`, `0x0034` | unresolved | fixed-size numeric blobs, mostly `u16 deck`, `u16 deck`, `u32`, then values; sent once per deck (1 and 2) | Per-deck setup/capability negotiation. Not decoded. |

The INFO frame is plain XML and identifies the device and its skin:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<info build="8515" skin="DeathDisco Grave Raver Remote" width="1179" height="2556" dpi="3.0" />
```

So the **device** tells VirtualDJ which Remote skin it is running plus its pixel geometry
and DPI — the desktop does not push a skin down. This matches the Remote-skin deployment
model in [Application Internals.md](Application%20Internals.md).

## The subscription model

The heart of the protocol, and the reason it matters: the device sends pairs of
SUBSCRIBE + KIND frames, one per value it wants to display. Verbatim from the capture:

```text
id=0   scope='left'  get_artist            kind=1
id=1   scope='left'  get_title             kind=1
id=2   scope='left'  get_bpm               kind=1
id=3   scope='left'  pitch                 kind=0
id=4   scope='righ'  get_artist            kind=1
id=7   scope='righ'  pitch                 kind=0
id=8   scope='left'  deck left volume      kind=0
id=10  scope='left'  deck left get_vu_meter kind=0
id=12  scope=global  crossfader            kind=0
id=13  scope=global  search_options        kind=2
id=14  scope=global  get_status            kind=1
id=15  scope=global  sampler_used          kind=2
id=16  scope=global  automix               kind=2
```

These are **ordinary VDJScript query strings** — the same grammar the HTTP `/query`
endpoint and skin `query=""` attributes evaluate, including deck-scoped forms
(`deck left volume`). The device picks what it wants; there is no fixed schema of pushed
fields. That is what makes this a general event channel rather than a fixed remote-control
API: subscribe to `get_vu_meter` and you get a meter feed, subscribe to `get_title` and you
get track changes.

Push semantics were confirmed independently by traffic sampling during a real session: idle
seconds carry 0 bytes, while a deck load pushed ~249 KiB desktop→device in one second with
no inbound request.

## Message types: desktop → device

**Replaying a captured opener is sufficient to hold a session.** Verified 2026-07-27: a fake
device advertising `_vdjremote8._tcp` that sends the 1184-byte capture verbatim is accepted
by VirtualDJ, which then streams state — 6.7 KB in 106 frames within seconds, with no
pairing token, nonce, or challenge. The handshake is stateless replay.

| Type | Name (working) | Payload after the u16 type | Meaning |
| --- | --- | --- | --- |
| `0x0005` | VALUE | `u16 id`, `fourcc kind`, value | The answer to subscription `id`. Kind fourccs observed: `val` → `float32 LE`; `txt` → `u32 length` + UTF-8; `fail` → the query produced no value. |
| `0x0025` | FOLDER | `u16`, `u32`, XML *or* a ZIP blob | Browser folder content. Small listings are `<foldercontent path= name= hasorder= haschildren= canmove= candelete= total= start= nb= />` XML; larger ones arrive as a PKZip archive containing `data.xml`. |
| `0x0036` | SETTING | `u16`, `u32 index`, `u32 len`, key+value text | Config push, one per setting: `vinylMode`/`yes`, `pitchRange`/`33.0`, `skinWaveformType`/`colors`, `automixMode`/`smart`, `keepPlayingPastEnd`/`no`, … 50 frames in one session. |
| `0x003f` | SELECTFOLDER | `u16`, `u32`, XML | Current browser location: `<selectfolder selectedfolderpath="root:/All Files.vdjfolder" selectedfolderidx="0" selectedsideviewname="remixes" />`. |
| `0x002b`, `0x003b` | unresolved | mostly-zero fixed blocks, one per deck/index | Not decoded; likely per-deck state or waveform scaffolding. |

Worked examples from a live session, matching the subscription ids above:

```text
id=1  left get_title  txt  len=35  "Drag a song on this deck to load it"   (empty deck)
id=2  left get_bpm    val  00 00 f0 42  -> 120.0
id=8  left volume     val  00 00 80 3f  -> 1.0
id=0  left get_artist fail                                                  (no track)
```

So a third-party client gets exactly what it asks for: subscribe to any VDJScript query and
VirtualDJ pushes a typed value whenever it changes. Combined with the browser folder frames,
this is enough to build an external browser or full alternate interface — the direction the
[HTTP Control Interface](HTTP%20Control%20Interface.md) cannot serve because it has no push.

## Reproducing a capture

The device is a plain TCP server that speaks first, so no interception is required — open
the Remote app, leave it on its connect screen, and dial it:

```sh
python3 tools/vdjremote_dial.py <device-ip> 4243 25    # capture + decode the opener
```

Run `tools/vdjremote_dial.py --decode <file>` on a saved capture to re-print the frame
listing. A raw reference capture is stored at
[tests/vdjremote-opener.bin](../tests/vdjremote-opener.bin).

## Open questions

- **Actions are unobserved.** The captured opener is subscription-only, so the frames a
  device sends to *act* (play, cue, load, crossfade) have not been seen. Capturing them
  needs a real device session with the user touching controls — either a relay between
  desktop and device, or dialing a device while it is being used.
- The device→desktop numeric types (`0x09`, `0x0c`, `0x27`, `0x29`, `0x34`) are undecoded,
  as are desktop→device `0x2b` and `0x3b`. They are sent once per deck and look like
  capability/state scaffolding; a session is accepted whether or not they are understood,
  since replay reproduces them verbatim.
- The subscription vocabulary has only been exercised with the ~17 queries the captured
  skin happened to use. Whether *arbitrary* VDJScript queries can be subscribed (e.g.
  `get_position`, custom `deck N` scopes) is untested and is the obvious next probe: edit
  the subscription frames in the replay and watch what comes back.
- Waveform data has not been identified in any frame. If it rides this channel it is
  probably inside the `0x25` ZIP payloads or the undecoded blocks.

See TODO task 8 for the current plan.
