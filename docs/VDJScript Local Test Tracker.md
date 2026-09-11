# VDJScript Local Test Tracker

Focused manual-test log for verbs marked **Needs local test** in [Official VDJScript Coverage Audit](Official%20VDJScript%20Coverage%20Audit.md). Keep rows practical: one reproducible check, the VirtualDJ build, hardware/context, result, and any follow-up notes.

Result values: `Untested`, `Pass`, `Partial`, `Fail`, `N/A`.

## Evidence Snapshot

Last sparse-prose spot-check: 2026-05-21 against the [official VDJScript verbs appendix](https://www.virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html) and local official/published skin examples.

- Current coverage cross-check: the 2026-06-30 official appendix refresh parses to 991 official verb/alias names; `VDJScript Verbs.md` contains all 991, missing names are 0, and the compact official remainder is empty. The formal `Needs local test` gap is 19 official names: `system`, `dualdeckmode_decks`, and the 17 hardware-specific controller helpers below. `dualdeckmode_decks` now has a build-recorded pad-page observation, but still needs a dual-deck pair/controller-context repeat before promotion to `Pass`.
- `Untested` means behavior has not been observed in VirtualDJ locally, even if the verb is official.
- `Pass` means a specific VirtualDJ build, hardware/context, action, and observed result were recorded.
- `connect` has local skin evidence: [official Lite](../examples/Skins/Built-In/Lite/Lite.xml) uses `<button action="connect">`. Local testing on VirtualDJ `v2026-m b9336` confirmed action/query behavior for logged-in and logged-out states.
- `karaoke_venue_name` was locally tested on VirtualDJ `v2026-m b9336`; it returns blank when the karaoke venue name is empty and updates to the configured venue name from the Karaoke > Venue Name dialog.
- `system` was locally tested on VirtualDJ `v2026-m b9336`; in the sparse helper pad context it returned blank text and pressing it produced no visible UI or log result. This is still too sparse to promote beyond a conservative note. Do not infer `system` behavior from unrelated parameter values such as `get_vu_meter 'system'` or from `system_volume`.
- `open_stem_creator` was locally tested on VirtualDJ `v2026-m b9336`; pressing it opened the Stem Creator dialog. Treat it as a workflow opener, not a selected-track automation helper.
- `get_mixfx_active` was locally tested on VirtualDJ `v2026-m b9336`; in a pad-page text/query context, it mirrored `effect_mixfx_activate` off/on for Filter and Echo after a track was loaded.
- `deck_has_error` was locally tested on VirtualDJ `v2026-m b9336`; it stayed off for normal load/unload states, turned on after loading a deliberately missing file, scoped to deck 1 in the tested context, and cleared after a later successful selected-track load.
- `dualdeckmode_decks` has a local pad-page result on VirtualDJ `v2026-m b9336`: in the pad-page context it remained false/red for current and deck-scoped readbacks even after `dualdeckmode` toggled on; repeated on deck 2 with the same reported behavior.
- The VDJScript grammar battery ran on VirtualDJ `v2026-m b9482` (2026-07-14 log entry): trailing `&` chains bind to the ternary false branch, leading chains split off normally, nested ternaries associate standard, and backtick-computed arguments work for `set` but are ignored by `loop`, `beatjump`, and `phrase_sync`. Side findings: `beatjump` needs a signed argument (`+4` jumps, `4` is a no-op), and string values read back blank via `get_var` in pad labels.
- Controller-display, Phase, RZX, DJC, V7, Gemini, and Denon rows are hardware-dependent; keep them `Untested` unless the named target device or an equivalent controller mapping environment was used.

Suggested test order:

1. No-hardware sparse helpers: revisit `system` only if official examples or harmless parameters are found.
2. Optional controller/deck setup: repeat/expand `dualdeckmode_decks` with [Reference - Dual Deck Mode Test.xml](../tests/Pads/Reference%20-%20Dual%20Deck%20Mode%20Test.xml), especially in any context where dual-deck pair routing is visible.
3. Hardware-only batches: controller displays, Phase, RZX, DJC, V7, Gemini, Denon
4. Non-official Button Editor hidden probes: use [Reference - Hidden Button Editor Tests.xml](../tests/Pads/Reference%20-%20Hidden%20Button%20Editor%20Tests.xml), then record results in the dedicated hidden-candidate section below without promoting them to official guidance.

## Test Run Template

Before changing a row result from `Untested`, capture enough context to reproduce it:

```text
Date:
VirtualDJ build:
Test asset:
Account/deck/hardware state:
Steps:
Observed result:
Tracker rows updated:
Follow-up:
```

## Test Run Log

```text
Date: 2026-07-27
VirtualDJ build: 2026 (get_version)
Test asset: tools/sweep_verb_existence.py -> tests/verb-existence-sweep.json
Account/deck/hardware state: no hardware; decks empty; read-only (query endpoint only, no /execute)
Steps: send every name in the verb store plus every backticked identifier from Undocumented VDJScript Candidates.md as a BARE query over the HTTP interface, and bucket each result by HRESULT. 1043 names in ~22 s over one keep-alive connection.
Observed result: 1007 of 1043 names PROVEN TO EXIST — 652 answered bare (query verbs, sample value captured), 186 E_NOTIMPL (action-only), 116 E_INVALIDARG (takes arguments), 27 E_ACCESSDENIED (context-gated; track-metadata queries with no track loaded), 26 S_FALSE (evaluated false); only 36 unresolved (E_FAIL). Two codes were new this run: E_ACCESSDENIED (0x80070005) and S_FALSE (0x00000001, severity bit CLEAR = success). Of the 47 candidate names not in the store, 34 are proven real, including the whole flip_* family (flip_arm/load/loop/play/record all query-capable returning `no`; flip_get_status returns empty, so it is a string status not a boolean), `masterbpm` (120), `crash` (a REAL action-only verb — do not execute), and five argument-taking names. `master_beat_num` returns RAW IEEE-754 float32 BITS as a decimal integer: successive reads 1078136832/1078243328/1078341632 reinterpret to 3.048/3.073/3.097, a smoothly advancing beat position. `browser_filter`, `browser_search`, and `none` stayed E_FAIL, so TODO task 5's note still stands.
Tracker rows updated: none directly — the sweep proves existence and kind, NOT behavior, so no test_status was promoted on this evidence. Recorded in HTTP Control Interface.md, Undocumented VDJScript Candidates.md, tools/README.md, INDEX.yml.
Follow-up: use the sweep to target real tests — `needs-args` names tell you a test must supply arguments, `action-only` names cannot be probed by query at all, and `context-gated` names need the right state loaded first. Next natural step is an argument-shape probe over the 116 E_INVALIDARG names.
```

```text
Date: 2026-07-27
VirtualDJ build: 2026 (get_version)
Test asset: HTTP control interface — error-code taxonomy and `setting` readability
Account/deck/hardware state: no hardware; no decks touched (queries only)
Steps: query known-official ACTION verbs (`load`, `unload`, `browser_enter`, `open_stem_creator`, `rescan_controllers`) and compare their error bodies against `nothing` and a bogus name; query `remote_action` in three forms; read the five `*Remote*` setting keys via `setting '<key>'` with the per-device "Connect automatically" checkbox first off and then on; read four invented setting names; extract `*Remote*` setting names from the binary string table to bound the key list.
Observed result: NEW existence signal — `error:-2147467263` (`E_NOTIMPL`) is returned by every action-only official verb queried (`load`, `unload`, `browser_enter`, `open_stem_creator`, `rescan_controllers`), while `nothing` and a bogus name return `E_FAIL`. So `E_NOTIMPL` joins `E_INVALIDARG` as positive proof a verb exists, and is the cheapest such probe. `remote_action` returns `E_FAIL` in all three forms despite `ACTION_remote_action` being in the binary symbol table and autocompleting in the Button Editor — the clearest worked example that `E_FAIL` never disproves a verb; it is presumably context-gated to a Remote skin. `setting` works over HTTP and validates names (`setting 'iRemoteDefaultPort'` -> 4243; unknown keys -> `E_INVALIDARG`). The binary yields exactly five valid `*Remote*` keys (iRemote, iRemoteList, iRemoteDefaultPort, vdjRemoteDevices, vdjRemoteIPs) and ALL FIVE read identically with the "Connect automatically" box off and on, so that checkbox is not exposed as a setting and cannot be flipped from VDJScript.
Tracker rows updated: none (channel finding) — recorded in HTTP Control Interface.md and Undocumented VDJScript Candidates.md.
Follow-up: `connect` is the VirtualDJ ACCOUNT login button (already recorded), not a device connect; `remote_action` is a Remote-skin helper for reaching desktop actions/variables, not a connect helper. No VDJScript route to connect a Remote device has been found — with the checkbox ticked VirtualDJ dials automatically, which is the practical workaround.
```

```text
Date: 2026-07-27
VirtualDJ build: 2026 (get_version); Remote app build 8515 (iOS)
Test asset: Remote action frames — capture in tests/vdjremote-actions.log; reverse test via a device impersonator over tests/vdjremote-opener.bin
Account/deck/hardware state: no DJ hardware; iOS Remote app on the LAN (default skin) for the capture half; deck 1 loaded and paused for the reverse test, restored empty afterwards
Steps: (1) impersonate VIRTUALDJ to the real device — dial it, answer its subscriptions with synthesized values so its UI activates — then log every frame while a scripted press sequence was performed (play, play again, cue, crossfader sweep, volume sweep); (2) impersonate a DEVICE to VirtualDJ and send `frame(0x31, u16 deck=1 + "deck 1 play")`, verifying with `deck 1 play` / `get_position` over HTTP.
Observed result: Three device->desktop action types. 0x31 SCRIPT carries an action as VDJScript TEXT (`touchwheel_touch on`, `touchwheel +0.00000ms`). 0x02 CONTROL carries a u16 numeric control id + u32 PHASE + optional `val` float32, where phase is begin(1)/update(0)/end(2) and NOT a deck number: buttons send 1 then 2, faders send 1, a stream of 0s each carrying a float, then 2. The timed sequence mapped 0xc6 play, 0xc7 cue, 0x41 crossfader, 0x36 volume on that device's skin. 0x26 LOAD carries a u16 deck plus an absolute file path. REVERSE DIRECTION CONFIRMED: sending 0x31 with "deck 1 play" flipped `deck 1 play` from no to yes within ~2 s with get_position advancing. A second run sent three different action kinds down one session, each verified by HTTP readback: `deck 1 pause` (play yes->no), `deck 2 load_next` (loaded no->yes), `crossfader 100%` (0.5->1). So a third-party client can both subscribe and act over this one socket with no HTTP involvement. `play` starts rather than toggles — sending it twice left the deck playing.
Tracker rows updated: none (protocol finding, not a verb) — recorded in docs/Remote Protocol.md and TODO task 8 (now DONE).
Follow-up: a passive man-in-the-middle relay does NOT work — the device accepts one session at a time and VirtualDJ auto-connects to it directly; impersonating the desktop side avoids the race. Reconnect behavior is governed by the per-device "Connect automatically" checkbox: ticked, VirtualDJ redials ~5 s after a drop and on a fresh mDNS appearance; unticked, the device sits at "(Waiting)" and only a manual Connect starts a session. Still open: the 0x02 id space beyond four ids, mid-session subscribe/unsubscribe, and where waveform data lives.
```

```text
Date: 2026-07-27
VirtualDJ build: 2026 (get_version)
Test asset: Remote subscription probe — tools/vdjremote_subscribe.py over tests/vdjremote-opener.bin; state driven via the HTTP interface
Account/deck/hardware state: no hardware; no phone involved (the captured opener supplies the setup/info/panel prefix); deck 1 empty at start, restored empty at end
Steps: substitute synthetic SUBSCRIBE/KIND frames into the captured opener; advertise a fake device (`dns-sd -R iPad _vdjremote8._tcp . 4243`) so VirtualDJ dials in; log pushed values. Probe set covered a known-good control, the same query declared under two different KINDs, global queries, `deck 1/2/3` scoping inside the script, quoted arguments, FX introspection, a ternary, and a bogus verb. Then a 75 s session while `deck 1 load "<path>"`, `deck 1 play`, and `deck 1 pause & unload` ran over HTTP.
Observed result: Subscriptions accept ARBITRARY VDJScript — `get_clock` -> '05:29 PM', `get_version` -> '2026', `get_effect_name 1` -> 'Phaser', `deck 1/2/3 get_bpm` -> 120 each (deck scoping works inside the script, not just via the left/righ fourcc), and `get_bpm 0 ? get_bpm : get_version` -> '2026' (same as the HTTP channel). KIND is a HINT, not a request: `get_bpm` declared kind=0 and kind=1 both returned `val`. `fail` means "no value now", not "bad query" — `deck 1 get_loaded_song 'fullpath'` returned `fail` on an empty deck and the real path once loaded; a bogus verb is indistinguishable, exactly like E_FAIL over HTTP. Push-on-change confirmed with timestamps: the load pushed get_title 'Body Lang', get_artist 'Balanka', get_bpm 127.999, fullpath and filename within the same second as the HTTP call; unload pushed all back to empty-deck values. `get_position` streamed at 33-34 pushes/second while playing and was silent while paused; `get_clock` pushed once a minute. 225 pushes logged in one session.
Tracker rows updated: none (protocol finding, not a verb) — recorded in docs/Remote Protocol.md and TODO task 8.
Follow-up: action frames (device->desktop play/cue/load) still unobserved — the last significant gap; needs a real device session with controls being touched. Mid-session subscribe/unsubscribe untested. Note VirtualDJ parks unresponsive devices at "(Waiting)" and stops dialing; dropping and re-adding the dns-sd advert triggers a fresh redial without touching the UI.
```

```text
Date: 2026-07-27
VirtualDJ build: 2026 (get_version); Remote app build 8515 (iOS)
Test asset: VirtualDJ Remote wire-protocol capture — tools/vdjremote_dial.py, tests/vdjremote-opener.bin
Account/deck/hardware state: no DJ hardware; iOS Remote app on the LAN running a custom Remote skin; decks empty
Steps: (1) advertise a fake device via `dns-sd -R <name> _vdjremote8._tcp . 4243` and listen — VirtualDJ connected and sent 0 bytes across repeated sessions; (2) send 8 candidate openers (newline, text, HTTP, XML, 4 binary framings), one per reconnect — all drew silence; (3) open the Remote app on the device and dial it directly with a plain client socket (the device is the TCP server and speaks first), capturing its 1184-byte opener; (4) decode the frames; (5) replay the captured opener verbatim from the fake device and log what VirtualDJ pushes back.
Observed result: Framing is `8JDV` (fourcc 'VDJ8' LE) + u32 total length (header included) + u16 message type. The device opens with 49 frames: an XML `<info build= skin= width= height= dpi=>` announcement, panel declarations (playlist/sampler/sidelist/karaoke), and SUBSCRIBE (0x01) + KIND (0x03) pairs registering ordinary VDJScript queries by id with a little-endian fourcc deck scope ('left'/'righ'/zero) — get_artist, get_title, get_bpm, pitch, `deck left volume`, `deck left get_vu_meter`, crossfader, get_status, sampler_used, automix. Replaying that opener verbatim is ACCEPTED by VirtualDJ with no pairing token or challenge: it streamed 6752 bytes in 106 frames. Desktop->device types: 0x05 VALUE (u16 id + kind fourcc — `val` float32, `txt` u32-len+UTF-8, `fail`), 0x25 browser folder XML (large listings as a PKZip containing data.xml), 0x36 settings key/value (50 frames: vinylMode, pitchRange 33.0, skinWaveformType, automixMode...), 0x3f selectfolder XML. Values matched the subscriptions exactly: id=2 get_bpm -> 120.0, id=8 volume -> 1.0, id=1 get_title -> "Drag a song on this deck to load it", id=0 get_artist -> fail.
Tracker rows updated: none (protocol finding, not a verb) — recorded in docs/Remote Protocol.md, TODO task 8, INDEX.yml, docs/README.md.
Follow-up: action frames (play/cue/load) unobserved — needs a device session with controls being touched. Whether ARBITRARY VDJScript queries can be subscribed is untested and is the load-bearing question for external interfaces; probe by editing subscription frames in a replay. Undecoded: device 0x09/0x0c/0x27/0x29/0x34, desktop 0x2b/0x3b. Waveform data not located.
```

```text
Date: 2026-07-27
VirtualDJ build: 2026 (get_version)
Test asset: VirtualDJ Remote app transport probe (iOS Remote app on the LAN; no VDJScript verbs exercised beyond the already-passed deck 2 load/unload)
Account/deck/hardware state: no hardware; Network Control on port 80; iOS Remote app connected over Wi-Fi; deck 1 loaded/paused, deck 2 empty
Steps: run a 1 Hz lsof socket watcher on the VirtualDJ process while the Remote app connects; browse mDNS service types and resolve the new instance (dns-sd -B/-L); sample per-second per-connection byte deltas (nettop -d) across idle, deck 2 load "<path>", and deck 2 unload; restore deck 2 empty.
Observed result: The Remote app does NOT use the Network Control HTTP channel. The phone advertises Bonjour type _vdjremote8._tcp (SRV -> phone:4243); VirtualDJ browses and connects OUT to the phone (desktop is the TCP client, phone is the server) over one persistent TCP connection. Semantics are event-driven push, not polling: idle seconds show 0 B in / 0 B out on that connection; deck 2 load pushed ~249 KiB desktop->phone in one second with 0 B inbound (track metadata/waveform/art payload, unprompted); unload exchanged ~1.4 KiB; only occasional sub-KB keepalives otherwise. Port 80 saw no Remote traffic.
Tracker rows updated: none (transport finding, not a verb) — recorded in HTTP Control Interface.md, Application Internals.md (Remote Skins), TODO task 8.
Follow-up: wire format (framing/handshake/message schema) still unknown. TODO task 8 reshaped: shim the PHONE side — advertise _vdjremote8._tcp from the desktop and log what VirtualDJ sends on connect; needs no root and no packet capture.
```

```text
Date: 2026-07-27
VirtualDJ build: 2026 (get_version)
Test asset: HTTP control interface channel probe (no VDJScript verbs exercised)
Account/deck/hardware state: no hardware; interface enabled on port 80
Steps: GET / on the running interface; send a WebSocket upgrade request (Connection: Upgrade, Upgrade: websocket) to /; GET /events; lsof the VirtualDJ process for all TCP/UDP sockets; fetch the official page GET / linked to.
Observed result: GET / returns a static HTML page linking https://virtualdj.com/wiki/NetworkControlPlugin.html — official provenance for the interface (Network Control plugin, VDJ 2023+, Pro license, configurable port, Bearer auth). The WS upgrade is ignored (HTTP/1.0 200 with the same static page, no 101); /events is 404; the official page documents only /query and /execute. lsof shows exactly one TCP listener (*:80) plus UDP 5353 (mDNS). Conclusion: the Network Control plugin is poll-only, no event hooks. The VirtualDJ Remote app's protocol remains uncharacterized (TODO task 8).
Tracker rows updated: none (channel finding, not a verb) — recorded in HTTP Control Interface.md (Provenance + No push channel sections), Resources.md, TODO task 8.
Follow-up: TODO task 8 — packet-capture a live Remote app session, then shim the desktop side to enumerate the Remote request surface.
```

```text
Date: 2026-07-27
VirtualDJ build: 2026 (get_version)
Test asset: HTTP control interface (http://localhost/), local FLAC file
Account/deck/hardware state: no hardware; interface enabled; deck 1 loaded and paused, deck 2 empty
Steps: query deck 1 play / deck 2 loaded for a safe baseline; read deck 1's path via get_loaded_song "fullpath"; execute deck 2 load "<that absolute path>"; read back deck 2 title/fullpath; execute deck 2 load "<nonexistent path>"; read back title and deck 2 deck_has_error; execute deck 2 unload; confirm deck 2 loaded -> no.
Observed result: load accepts an absolute file path and loads it onto the scoped deck with no browser selection involved — deck 2 title/fullpath matched the requested file. The nonexistent path ALSO returned true from /execute, with the deck landing in an error state (title "Error", deck_has_error yes), so the execute boolean does not signal load success; verify with deck_has_error or get_loaded_song readback. Field names for get_loaded_song: "fullpath" = absolute path, "filepath" = folder only, "filename" = basename, "path"/"file" = E_INVALIDARG. deck 2 unload restored the empty state.
Tracker rows updated: load verb record (test_status Pass, evidence, note); HTTP Control Interface.md verified table + gotchas.
Follow-up: untested whether relative paths, netsearch URLs, or non-audio files behave differently; bare load (browser-selection form) not exercised over HTTP.
```

```text
Date: 2026-07-22
VirtualDJ build: 2026 (get_version)
Test asset: HTTP control interface (http://localhost/), tools/sweep_fx_introspection.py -> tests/fx-introspection-dump.json
Account/deck/hardware state: no hardware; interface enabled; sweep drives deck-FX slot 1
Steps: Pass A cycled effect_select 1 +1 until the name wrapped (enabled/favorites list). Pass B selected each documented catalog name plus every cycled name by name, using a 'Dump' sentinel park to detect non-loads, and read the introspection helpers (get_effect_name, get_effect_slider_count/button_count, effect_has_slider/button, get_effect_slider_label/label_full/name/text, get_effect_button_shortname) per position.
Observed result: 95 effects reachable into deck-FX slot 1 and fully mapped (slider/button counts, short+full labels, live value text); 63 of them are in the +1 cycle (enabled list), the rest are name-only. The +1 cycle is a SUBSET of installed effects: Reverb/Flanger/Phaser and others are absent from the cycle but selectable by name. Slot 1 also accepts VIDEO effects by name — `Blinds`, `Cube`, and `Camera` all load and report controls — so the 95 mix audio and video, and "reachable into slot 1" must not be read as "is an audio effect". Names that did not load at all: `BeatGrid` (wrong spelling; the installed selector name is `Beat Grid`), `Brake` (no spelling loaded), `Shader`. Their reason is unresolved — NOT "video-only", which the loading video effects above rule out; most likely not installed, or not the selector name. Spot-check reproduced the prior hand-built map exactly for Backspin, Flanger (incl. the LEN/Speed pair), Echo, Reverb, Beat Grid, and Cut, confirming the HTTP channel matches pad-fixture readback.
Tracker rows updated: FX introspection sweep (this entry)
Follow-up: Structural map (labels/counts) captured for all 95 in the dump and queryable via `just get-fx / list-fx / fx-stats`. NOT yet captured: normalized slider defaults (get_effect_slider_default) and reset-value text, which need a per-slider reset pass; and an audio-vs-video classification for the 95 (the sweep cannot currently tell them apart). No hand-transcription into Effects Engines.md — query the dump instead.
```

```text
Date: 2026-05-23
VirtualDJ build: v2026-m b9336
Test asset: Reference - Sparse Helper Tests.xml; shown in VirtualDJ as "Reference - Sparse Helper Tests"
Account/deck/hardware state: tested logged in and logged out; no dedicated hardware
Steps: load the sparse helper pad page, observe Pad 1, press Pad 1 while logged in, log out, observe Pad 1 again, press Pad 1 while logged out
Observed result: logged in shows green "CONNECT: on"; pressing opens a small menu with "Log out". Logged out shows red "CONNECT: off"; pressing opens the VirtualDJ CONNECT login dialog.
Tracker rows updated: connect
Follow-up: none for basic action/query behavior
```

```text
Date: 2026-05-23
VirtualDJ build: v2026-m b9336
Test asset: Reference - Sparse Helper Tests.xml; shown in VirtualDJ as "Reference - Sparse Helper Tests"
Account/deck/hardware state: no dedicated hardware
Steps: observe the purple KARAOKE pad with no venue set, press it to open the Karaoke menu, choose Venue Name, set a venue value, observe the pad label, clear the venue value, observe the pad label again
Observed result: empty venue shows "KARAOKE:" with no value. Pressing the pad opens the Karaoke menu with Venue Name. Setting the venue updates the pad label to include the configured venue name. Clearing the venue returns the label to "KARAOKE:".
Tracker rows updated: karaoke_venue_name
Follow-up: none for venue-name query and empty-state behavior
```

```text
Date: 2026-05-24
VirtualDJ build: v2026-m b9336
Test asset: Reference - Sparse Helper Tests.xml; shown in VirtualDJ as "Reference - Sparse Helper Tests"
Account/deck/hardware state: logged in; no dedicated hardware; tested with a browser track selected and with an empty browser result set
Steps: load the sparse helper pad page, observe Pad 3, press Pad 3, press Pad 4 with a browser track selected, close the opened dialog, filter the browser to 0 files, press Pad 4 again, close the dialog, then clear the browser filter
Observed result: Pad 3 showed "SYSTEM:" with no returned value from `system`; pressing it produced no visible UI change and no new Log Report entry. Pad 4 `open_stem_creator` opened the Stem Creator dialog with Bass, Kick (Drums), HiHat (Optional), Vocals (Optional), Instruments, Instru2 (Optional), Output, Headroom set to 6dB, and Create controls. The selected browser track was not auto-filled into the dialog. With 0 browser results, the same blank dialog opened. No export/create action was attempted.
Tracker rows updated: system, open_stem_creator
Follow-up: `system` remains too sparse to promote beyond the blank/no-visible-effect observation; `open_stem_creator` still needs separate testing for full stem-file creation, file-picker behavior, and license/build gating.
```

```text
Date: 2026-05-26
VirtualDJ build: v2026-m b9336
Test asset: Reference - Mix FX Query Test.xml; shown in VirtualDJ as "MIX FX QUERY TEST"
Account/deck/hardware state: no dedicated hardware; deck 1 loaded with a local browser track; selected Mix FX tested with Filter and Echo
Steps: load a track to deck 1, open the Mix FX query pad page, observe Filter selected with Mix FX inactive, press Pad 7 to toggle `effect_mixfx_activate` on/off, press Pad 6 to select Echo, then repeat the Pad 7 toggle and compare Pad 8 `` `get_mixfx_active` `` text/query/color against Pad 7.
Observed result: With Filter selected, Pad 8 showed "GET: off" when Pad 7 `effect_mixfx_activate` was off; pressing Pad 7 changed it to green "GET: on"; pressing Pad 7 again returned it to red "GET: off". After selecting Echo, direct and indirect Echo selected-state pads turned blue while Filter pads turned red, and Pad 8 again followed `effect_mixfx_activate` off/on. The page needed a loaded deck before the pad labels/state rendered clearly in the active skin.
Tracker rows updated: get_mixfx_active
Follow-up: repeat in a skin text/custom-button context if documenting non-pad surfaces, but pad text/query behavior is confirmed.
```

```text
Date: 2026-05-26
VirtualDJ build: user-provided local result, build not recorded
Test asset: User-provided pad XML fragment with two `FX-VOCALS` pads
Account/deck/hardware state: vocal stem FX slot available; exact deck/hardware state not recorded
Steps: create two pads that both call `effect_select_multi 'vocals'`, one for `echo out` and one for `reverb`; use `effect_active 'vocals' '<effect>'` as each pad query and action target
Observed result: Echo Out and Reverb light independently according to their selected/active effect state, while both play through the same `vocals` stem FX slot.
Tracker rows updated: effect_select_multi, effect_active
Follow-up: repeat on a recorded VirtualDJ build and add a minimal test pad page if this pattern becomes a canonical fixture.
```

```text
Date: 2026-05-26
VirtualDJ build: user-provided local result, build not recorded
Test asset: User-provided pad XML fragments for a vocal `padfx` chain
Account/deck/hardware state: vocal stem pad FX available; exact deck/hardware state not recorded
Steps: compare a pad that starts with `effect_disable_all 'padfx'` followed by `padfx 'echo out' ... 'stemfx:vocal'` and `padfx 'reverb' ... 'stemfx:vocal'` against the same pad without the inline `effect_disable_all`; then compare with other pads that use the same effect/stem targets with different parameter values.
Observed result: The inline `effect_disable_all 'padfx'` version did nothing visible and did not light; removing the inline clear made the chained pad FX work. Separate pads using the same effect/stem target can alter or "steal" one or more effects from another pad-FX chain by changing the active parameters.
Tracker rows updated: padfx, effect_disable_all
Follow-up: repeat on a recorded VirtualDJ build with a minimal fixture that logs visible pad state, `effects_used 'padfx'`, and audible behavior for same-event cleanup versus separate cleanup.
```

```text
Date: 2026-06-01
VirtualDJ build: user-provided local result, build not recorded
Test asset: Local FX slot/stem slot setup; `examples/Pads/Quarantine/FX-SLOTS.xml` is the nearest repo fixture
Account/deck/hardware state: normal deck FX slots and named stem FX slots available; exact deck/hardware state not recorded
Steps: load/select effects into FX1-FX8 and named stem FX slots such as `vocals` and `rhythm`; verify persistence across track loads/current session; close and reopen VirtualDJ; compare loaded effect names after restart
Observed result: FX1-FX6 kept their loaded effect across a VirtualDJ restart. FX7, FX8 and higher, plus named stem FX slots such as `vocals` and `rhythm`, kept their loaded effect during the current session and across track loads, but reset/cleared after restart. Working interpretation: FX1-FX6 behave like persistent rack state, while FX7+ and named stem FX slots behave like volatile performance state.
Tracker rows updated: effect_select, get_effect_name
Follow-up: repeat on a recorded VirtualDJ build and capture whether active state, slider values, and `effect_select_multi` contents follow the same persistence boundary.
```

```text
Date: 2026-06-08
VirtualDJ build: v2026-m b9336
Test asset: Reference - Deck Error Test.xml; shown in VirtualDJ as "REF: DECK ERROR TEST"
Account/deck/hardware state: no dedicated hardware; deck 1/current deck had a valid selected browser track available
Steps: load the deck error test page, load a valid track, observe state, press LOAD SEL, press UNLOAD, press LOAD MISS, then press LOAD SEL again.
Observed result: After the initial valid load, ERR was off, LOAD was on, D1ERR was off, and D2ERR was off. Pressing LOAD SEL caused no visible state change. After UNLOAD, ERR stayed off, LOAD turned off, and D1ERR/D2ERR stayed off. Pressing LOAD MISS turned ERR on/red, left LOAD off/gray, turned D1ERR on/red, and left D2ERR off/green. Pressing LOAD SEL with a valid selected track cleared ERR and D1ERR back off/green and set LOAD on/blue.
Tracker rows updated: deck_has_error
Follow-up: optional repeat from deck 2/current-deck context to further confirm scoped error behavior.
```

```text
Date: 2026-06-08
VirtualDJ build: v2026-m b9336
Test asset: Reference - Dual Deck Mode Test.xml; shown in VirtualDJ as "REF: DUAL DECKMODE TEST"
Account/deck/hardware state: no dedicated hardware; tested from deck 1/current context and repeated on deck 2
Steps: load the dual deck mode test page, observe MODE/CUR/D1-D4 states with dual-deck mode off, press MODE to toggle `dualdeckmode` on, then repeat from deck 2.
Observed result: With mode off, MODE was off/gray and CUR, D1, D2, D3, and D4 were false/red. Pressing MODE toggled MODE on/blue, but CUR and all deck-scoped `dualdeckmode_decks` pads stayed false/red. Repeating on deck 2 produced the same reported behavior.
Tracker rows updated: dualdeckmode_decks
Follow-up: test any deck layout/controller context where dual-deck pair routing is visibly active; current pad-page evidence suggests `dualdeckmode_decks` may not be a simple boolean query for "dual-deck mode is enabled."
```

```text
Date: 2026-06-08
VirtualDJ build: v2026-m b9336
Test asset: Reference - Hidden Button Editor Tests.xml; selector label "Reference - Hidden Button Editor Tests"; XML page name `REF: HIDDEN TAXONOMY TEST`
Account/deck/hardware state: no dedicated hardware
Steps: look for "Reference - Hidden Button Editor Tests" in the VirtualDJ pad-page selector.
Observed result: Page was not found in the pad-page selector during the user run. A later local filesystem check showed the XML installed at `~/Library/Application Support/VirtualDJ/Pads/Reference - Hidden Button Editor Tests.xml` with XML page name `REF: HIDDEN TAXONOMY TEST`, and repo pad lint passed. Follow-up testing confirmed VirtualDJ's selector uses the filename stem for local pad XML files rather than the XML `<page name="">` value.
Tracker rows updated: hidden Button Editor candidate probes
Follow-up: reload/restart VirtualDJ or recopy the XML, then look for selector label `Reference - Hidden Button Editor Tests`; if it still does not appear, inspect VirtualDJ logs/loading behavior for that pad file.
```

```text
Date: 2026-06-08
VirtualDJ build: v2026-m b9336
Test asset: Reference - Hidden Button Editor Tests.xml; shown in VirtualDJ as "Reference - Hidden Button Editor Tests"
Account/deck/hardware state: no dedicated hardware; deck/stems readiness not recorded
Steps: load the hidden Button Editor test page, observe Pads 1-3, press Pad 1 `stem_volume 'Vocal' 50%`, press Shift+Pad 1 debug readback, press Pad 2 `stem_volume 'Vocal' 100%`, then press Pad 3 `stem_volume 'Instru' 50%`.
Observed result: Initial labels/readbacks showed "VOC 50: 1", "VOC 100: 1", and "INSTRU 50: 1". Pressing Pad 1 produced no audible change and no pad-label change. Pressing Shift+Pad 1 opened a popup with text `` `stem_volume 'Vocal'` `` rather than an obvious evaluated value; no audible change and no label change followed. Pressing Pads 2 and 3 also produced no audible change and no pad-label change.
Tracker rows updated: stem_volume
Follow-up: repeat with a confirmed stems-ready loaded deck and visible stem controls; compare ordinary `stem 'vocal'` or `stem_pad 'vocal'` behavior in the same deck context before deciding whether `stem_volume` is nonfunctional, context-gated, or only a query/readback helper.
```

```text
Date: 2026-06-08
VirtualDJ build: v2026-m b9336
Test asset: Reference - FX Introspection Test.xml; shown in VirtualDJ as "REF: FX INTROSPECT"
Account/deck/hardware state: no dedicated hardware; Flanger loaded in deck FX slot 1
Steps: load the FX introspection page, load Flanger, and open the effect GUI.
Observed result: The Flanger GUI opened and displayed Strength 50%, Speed 8bt, Tone n/a, Feedback 50%, and LFO AMP 40%.
Tracker rows updated: effect_has_slider/effect_has_button/get_effect_slider_* probes, native effect parameter examples
Follow-up: press the count/label/text/default/name/shortname/button shift-log pads for Flanger, then repeat for Echo, Reverb, and BeatGrid to compare returned helper values against visible GUI controls.
```

```text
Date: 2026-07-05
VirtualDJ build: user-provided local result, build not recorded
Test asset: User-provided skin `<button>` with action `sync & phrase_sync <arg>`, driven by a global `$phrase_len` variable
Account/deck/hardware state: not recorded
Steps: compare a working clamped form against two interpolated forms that pass the variable value as the `phrase_sync` argument:
  1. sync & var_equal '$phrase_len' 16 ? phrase_sync 16 : phrase_sync 32   (clamped literal)
  2. sync & phrase_sync '`$phrase_len`'                                     (bare $var in backticks, quoted)
  3. sync & phrase_sync `get_var '$phrase_len'`                             (documented get_var query in backticks)
Observed result: Form 1 works and was kept. Form 3 (`phrase_sync `get_var '$phrase_len'`) did NOT work either, despite `get_var` being the documented way to read a variable value inside backticks. Form 2 also does not work as written. Working interpretation: `phrase_sync` does not accept a backtick-interpolated/computed argument in this context and requires a literal beat count; select the literal with a conditional instead.
Tracker rows updated: phrase_sync (see FX/Deck note below)
Follow-up: repeat on a recorded VirtualDJ build; test whether other numeric-argument action verbs (e.g. beatjump, loop) accept `` `get_var '...'` `` interpolation, to determine whether this is a `phrase_sync`-specific limit or a general rule that action arguments must be literals rather than backtick-substituted values. RESOLVED 2026-07-14: see the grammar battery entry below; the failure generalizes to `loop` and `beatjump`.
```

```text
Date: 2026-07-14
VirtualDJ build: v2026-m b9482
Test asset: Reference - Grammar Battery Test.xml; shown in VirtualDJ as "Reference - Grammar Battery Test"
Account/deck/hardware state: no dedicated hardware; A/B/C1/C3 ran with no track needed; deck 1 loaded and playing for C2/C4 and the literal control pads
Steps: pressed SETUP (pad 1) before every test pad, then read the blue result pads (a-b-c, r, dst, src/n); for C2/C4 compared against the yellow literal control pads on a playing deck. Mid-run fixture fixes: B1/B2 switched from string result codes ('X'/'Y'/'Z') to numeric codes (1/2/3) after string values displayed blank; the beatjump control pad switched to the signed form after unsigned `beatjump 4` proved to be a no-op; C4 switched to interpolating a stored '+4' string so the sign could not confound the backtick test.
Observed result:
  A1 (true cond, trailing & after false branch): a-b-c = 1-0-0. The trailing "& set c" did not run when the condition was true, so a trailing & chain binds inside the ternary false branch, not at statement level.
  A2 (false cond, same statement): a-b-c = 0-1-1. The false branch ran together with its trailing & chain. (A first press without SETUP read 1-1-1 from leftover A1 state; rerun cleanly after SETUP.)
  A3 (leading "set a &" then ternary, true cond): a-b-c = 1-1-0. The leading chain executed as its own statement and the ternary then evaluated independently.
  B1 (nested ternary, outer true / inner false): r = 2 ('Y'). Standard inner-binds-tightest nesting.
  B2 (nested ternary, outer false): r = 3 ('Z'). Standard nesting confirmed.
  C1 (set '$gb_dst' `get_var '$gb_src'`): dst = 42. `set` accepts a backtick-computed argument.
  C2 (loop `get_var '$gb_n'` with n=4 confirmed on the readout): no loop engaged; the literal `loop 4` control engaged a 4-beat loop on the same playing deck.
  C3 (get_var '$gb_src' & param_multiply 2 & set '$gb_dst'): dst = 84. Implicit param chaining works as the alternative pattern.
  C4 (beatjump `get_var '$gb_n'` with $gb_n set to the string '+4'): no jump; the literal `beatjump +4` control jumped on the same playing deck.
  Side findings: unsigned `beatjump 4` is a no-op on this build while `beatjump +4` jumps; string values written by `set` read back blank via `get_var` in pad labels, while numeric values display normally.
Tracker rows updated: phrase_sync follow-up (2026-07-05) resolved as a general rule, not verb-specific: `loop`, `beatjump`, and `phrase_sync` all ignore backtick-computed arguments even when the identical literal works, while `set` accepts them and param chaining works.
Follow-up: derived rules promoted to VDJScript Syntax Evidence.md and VirtualDJ Reference.md; optional later pass: map which other value-consumer verbs besides `set` accept backtick-computed arguments, and whether the signed-argument requirement applies to other relative-jump verbs.
```

```text
Date: 2026-07-14
VirtualDJ build: v2026-m b9482
Test asset: Reference - Grammar Battery Test.xml; shown in VirtualDJ as "Reference - Grammar Battery Test"
Account/deck/hardware state: no dedicated hardware; no track needed for A/B/C1/C3
Steps: pressed SETUP before each test pad, read blue result pads after each press
Observed result:
  SETUP: 000 (a-b-c) / r= / dst=0 / src=42 n=0
  A1 (true-cond trailing &): a-b-c = 1-0-0 -> a=1, b=0, c=0 - The trailing
  "& set '$gb_c' 1" did NOT run when the condition was true, so the trailing & chain
  binds inside the ternary false branch, not at statement level.
  Side note: SETUP sets $gb_r to 'none' but the r= pad displayed blank.
  A2 (false-cond trailing &): 0-1-1
Tracker rows updated: none yet (grammar evidence, not a verb row)
Follow-up: complete A2, A3, B1, B2, C1-C4; then promote derived precedence rules to
  VDJScript Syntax Evidence.md and VirtualDJ Reference.md
```

## Button Editor Hidden Candidate Probes

These rows are not official `Needs local test` rows. They track flag1-hidden Button Editor taxonomy candidates that are absent from the official appendix but have one or more local evidence streams: bundled language descriptions, compiled taxonomy placement, runtime strings, or exact `ACTION_*` method-symbol hints.

Do not promote these into ordinary user-facing verb guidance until a row has a concrete VirtualDJ build, setup, observed result, and notes. Use [Undocumented VDJScript Candidates](Undocumented%20VDJScript%20Candidates.md) as the evidence inventory, and use [Reference - Hidden Button Editor Tests.xml](../tests/Pads/Reference%20-%20Hidden%20Button%20Editor%20Tests.xml) for the low-risk pad probes.

| Candidate | Evidence | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `stem_volume` | `Built-in app resource`; `Binary compiled table`; no exact class. | Stem controls, pad text/actions, stems-ready deck. | Load a stems-ready track and the hidden taxonomy test page; compare Pads 1-3 and shift-pad readbacks for `stem_volume 'Vocal'` / `'Instru'` at 50% and 100%; compare against ordinary `stem 'vocal'` behavior and audible output. | v2026-m b9336 | None required | Partial | First run: Pads 1-3 read back `1`, but pressing `stem_volume 'Vocal' 50%`, `stem_volume 'Vocal' 100%`, and `stem_volume 'Instru' 50%` produced no audible or label change; Shift+Pad 1 opened a popup with literal-looking `` `stem_volume 'Vocal'` `` text. Repeat with confirmed stems-ready deck/visible stem controls before promoting or failing. The hidden language string lists `HiHat`, `Vocal`, `Instru`, `Bass`, `Kick`, `Melody`, `Rhythm`, and `MeloVocal`; keep `MeloRhythm` separate until observed for this hidden helper. |
| `sampler_inputgain` | `Built-in app resource`; `Binary compiled table`; exact `onExecute` / `onQuery`. | Hardware sampler input gain, sampler input path. | On the hidden taxonomy test page, observe Pad 4 and shift-pad 3 before/after `sampler_inputgain 50%`; if an input sampler path is available, compare audible/input gain. | TBD | Optional input path | Untested | May return a value even when no matching input path is active; record both readback and audible effect separately. |
| `get_pad_page_name` / `pad_page_insplit` / `pad_page_favorite` / `pad_page_split` | `Binary compiled table`; exact symbols for all; `pad_page_insplit` also has a language description; `get_pad_page_name` has public forum examples; `pad_page_favorite` has changelog/forum/published-skin evidence. | Pad-page state, split/favorite page UI. | Load the hidden taxonomy test page in normal pad mode and any split/favorite pad-page context; log shift pads 4-7 and observe Pad 6 query/color. For `pad_page_favorite`, also test action/query/text behavior across the current favorite slots and compare with `pad_page_favorite_select`. | TBD | None required | Untested | Good first pass for understanding split/favorite pad-page internals. Record selector label and XML `<page name="">` because local pad-page selectors use filename stems. |
| `pad_pressure_switch` | `Built-in app resource`; `Binary compiled table`; no exact class. | Pressure-capable pad controller mappings. | On pressure-capable hardware, bind a spare control to `pad_pressure_switch`, toggle it, and compare velocity/pressure-sensitive pad behavior. | TBD | Pressure-capable controller | Untested | Not included in the starter harness because no-hardware behavior may be meaningless. |
| `is_colorfx` / `effect_beats_sliderindex` | `Binary compiled table`; exact `onQuery` symbols. | Effect and ColorFX selected-state/readback. | On the hidden taxonomy test page, select a ColorFX and a normal deck FX with beat controls; observe Pad 7, Pad 8, and shift-pad 8 while changing effect selection and beat length. | TBD | None required | Untested | Low-risk query probes; useful if they expose ColorFX/beat-slider UI state more directly than documented helpers. |
| `flip_arm` / `flip_load` / `flip_loop` / `flip_play` / `flip_record` / `flip_get_status` | Language descriptions for most `flip_*`; exact symbols for `flip_get_status`, `flip_load`, `flip_play`, and `flip_record`. | Saved Flip / macro playback state. | Confirm Flip functionality is available; create or load a simple Flip, then use the hidden taxonomy test page param controls plus a custom button/log for `flip_get_status`; record state transitions for record, arm, load, loop, and play. | TBD | None required if Flip available | Untested | Keep separate from normal cue/macro docs until the feature state and licensing/build assumptions are clear. |
| `setting_if_unchanged` | `Community`; `Binary compiled table`; exact `onQuery`. | Settings/config change guards, skin `oninit` defaults. | Build a harmless throwaway-skin or custom-button probe around one known reversible setting; compare `setting_if_unchanged` before changing the setting, after changing it, and after restoring it. | TBD | None required | Untested | Public forum examples use it in action slots, while the exact symbol hint looks query-only. Verify action-slot behavior before documenting it as a defaulting helper. |
| `masterbpm` / `master_beat_num` | `Binary compiled table`; exact `onExecute` / `onQuery`. | Master deck BPM and beatgrid readback. | With two loaded decks and a known master deck, log both helpers while switching `masterdeck`, changing tempo, and moving across beatgrid positions; compare with `get_bpm`, `get_beat_num`, and visible master state. | TBD | None required | Untested | Promising for sync/master diagnostics, but not language-described. |
| `all_decks` / `combine_query` | `Binary compiled table`; exact `onExecute`, `onQuery`, `onQueryBool`, and `onQueryText`; `all_decks` is also a syntax-evidence test shape. | Query grammar, multi-deck combinators. | Start in custom buttons only: log bare readbacks, then test with tiny harmless boolean expressions if bare readback is accepted. | TBD | None required | Untested | Potential grammar-level helpers; do not use in pad fixtures until syntax and side effects are understood. A public LED thread shows `all_decks ? ...` as a user attempt, not as a validated pattern. |
| `remote_action` | `Official forum`; `Binary compiled table`; exact `onExecute`, `onQuery`, `onQueryBool`, and `onQueryText`. | VirtualDJ Remote skins; desktop-vs-remote action/variable state. | In a current Remote skin, create a Remote-local variable and a desktop variable/custom button with clear labels; compare direct Remote action/query against `remote_action "..."` for readback and action side effects. | TBD | Remote skin/device or simulator context | Untested | Staff/CTO posts say Remote custom buttons and variables are independent from desktop state and use `remote_action` for desktop-side actions. Keep this Remote-specific until a local Remote test records syntax and version behavior. |
| Hardware-only hidden candidates | `Built-in app resource` and/or exact symbols for `assign_related_controller`, `controllerscreen_action`, `motorwheel2`, `motorwheel3`, `ns7_get_drift`, `rane_motor_enable`, `rane_timecode`, `rane_timecode_enable`, `rane_screen_input`, `rane_screen_output`, `send_nothing`. | Matching controller, Rane screen/timecode, motorized platter, or controller-screen mapping context. | Test only with matching hardware or a known stock mapper context; record exact device, mapper, deck assignment, and observed display/motor/timecode behavior. | TBD | Required | Untested | Keep out of general docs unless hardware-specific behavior is reproduced. |

## Sampler

| Verb / Pattern | Why local test | Likely surface/context | Repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `sampler_loaded 8 'auto'` | Forum examples and older local examples use `"auto"`, but official docs only document fixed-slot `sampler_loaded 1`. | Pad XML sampler page with `sampler_pad_page`. | Load [Reference - Sampler Loaded Test.xml](../tests/Pads/Reference%20-%20Sampler%20Loaded%20Test.xml); use a bank with slot 8 loaded and slot 16 empty; switch to sampler page `9-16`. | 8.5.9307 / 18.0.9336 | None required | Fail | On page `9-16`, `sampler_loaded 8 'auto'` returned true while explicit `sampler_loaded 16` returned false. Treat `sampler_loaded` as absolute for empty-slot checks. |
| `sampler_loaded 8 auto` | Installed/public `Loop Recorder.xml` uses unquoted `auto`; check whether omitting quotes changes page-aware behavior. | Pad XML sampler page with `sampler_pad_page`. | Same diagnostic page; compare `AUTO8`, `AUTO8RAW`, `SLOT16`, and `AUTO16RAW` pads on page `9-16`. | 8.5.9307 / 18.0.9336 | None required | Fail | On page `9-16`, `sampler_loaded 8 auto` returned true while `sampler_loaded 16 auto` returned false. Unquoted `auto` matched quoted behavior and did not make `sampler_loaded 8` page-aware. |
| Read-only multi-page sampler guards | Need a page-aware sampler page that plays loaded samples but does not record or show slot-number fallbacks for empty slots. | Pad XML sampler page with `sampler_pad_page`, 8-pad and 16-pad controller layouts. | Load [SAMPLER READ ONLY.xml](../examples/Pads/Quarantine/SAMPLER%20READ%20ONLY.xml); use a bank with more than 8 presets; switch to page `9 to 16`; verify loaded slots show/play and empty slots stay blank/off/nothing. | 8.5.9307 / 18.0.9336 | XP2-style 16-pad layout observed | Pass | Working pattern: branch on text ranges like `"9 to 16"`, guard with absolute `sampler_loaded` slots, use `sampler_pad <visible-pad>` for loaded actions, `nothing` for empty actions, and `get_text ' '` for blank labels. Pads 9-16 map to the next eight visible sampler positions, so page `"9 to 16"` plus pad16 maps to slot 24. |

## Controller Display

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `controllerscreen_deck` | Sparse official prose; likely depends on controller screen routing and deck assignment. | Controller mapping with display-capable device; possibly screen page/action context. | Map a spare button/display action to `deck 1 controllerscreen_deck`, then repeat on deck 2 and observe whether the controller screen follows or reports the selected deck. | TBD | TBD | Untested | Official name only; needs display-capable controller context. |
| `controller_battery` | Hardware/environment dependent; useful only on devices that expose battery state. | Controller mapping, wireless/battery-capable controller display or LED feedback. | With a battery-capable controller connected, bind/display `` `controller_battery` `` and compare against the device/OS battery indicator while plugged and unplugged. | TBD | TBD | Untested | Official name only; requires battery-capable controller. |
| `gemini_waveform_zoomlevel` | Gemini-specific helper; behavior likely only visible on supported Gemini displays. | Gemini controller display/waveform mapping. | On supported Gemini hardware, bind `gemini_waveform_zoomlevel +1` and `-1`; verify waveform zoom changes and persists/display updates as expected. | TBD | TBD | Untested | Official name only; Gemini display helper. |

## Phase, RZX, DJC, And Hardware Helpers

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `phase_movement` | Phase-specific motion helper; no meaningful result without Phase hardware. | Phase controller/timecode-style deck mapping. | Connect Phase, load a track, display/log `` `phase_movement` `` while rotating and stopping the remote; record value range and idle behavior. | TBD | TBD | Untested | Official name only; requires Phase hardware. |
| `phase_position` | Phase-specific position helper; expected units/range need confirmation. | Phase controller display/query feedback. | Display/log `` `phase_position` `` while rotating slowly through one full turn; note wrap point, scale, and deck scoping. | TBD | TBD | Untested | Official name only; requires Phase hardware. |
| `phase_active` | Phase active-state helper; needs hardware and deck assignment confirmation. | Phase controller mapping or skin query. | Toggle Phase control/connection while displaying `` `phase_active` ``; confirm true/false states for connected, assigned, and disconnected cases. | TBD | TBD | Untested | Official name only; requires Phase hardware. |
| `v7_status` | Numark V7-specific helper; behavior depends on motor/display state. | Numark V7 mapping or status display. | On a V7, display/log `` `v7_status` `` while switching play, cue, platter touch, and motor states; capture observed status values. | TBD | TBD | Untested | Official name only; requires Numark V7. |
| `rzx_touch` | Pioneer RZX touchscreen helper; requires RZX touch surface. | Pioneer RZX mapping, touch/display context. | On RZX hardware, display/log `` `rzx_touch` `` while touching and releasing the screen; confirm boolean/timing behavior. | TBD | TBD | Untested | Official name only; requires Pioneer RZX. |
| `rzx_touch_x` | RZX-specific X coordinate helper; coordinate range is unknown locally. | Pioneer RZX touch/display mapping. | Touch left, center, and right of the RZX screen while logging `` `rzx_touch_x` ``; record min/max and origin. | TBD | TBD | Untested | Official name only; requires Pioneer RZX. |
| `rzx_touch_y` | RZX-specific Y coordinate helper; coordinate range is unknown locally. | Pioneer RZX touch/display mapping. | Touch top, center, and bottom of the RZX screen while logging `` `rzx_touch_y` ``; record min/max and origin. | TBD | TBD | Untested | Official name only; requires Pioneer RZX. |
| `djc_shift` | DJC-family helper; shift behavior may be controller/mapping specific. | DJC controller mapping. | On supported DJC hardware, bind/display `` `djc_shift` `` and press/release the hardware shift; confirm scope and latch/hold behavior. | TBD | TBD | Untested | Official name only; requires matching DJC-family context. |
| `djc_button` | DJC-family button helper; argument/value behavior is sparse. | DJC controller mapping/button feedback. | Bind `djc_button` to a test control and observe UI/LED/display response; repeat with likely button indexes if the mapping exposes them. | TBD | TBD | Untested | Official name only; requires matching DJC-family context. |
| `djc_button_popup` | DJC popup helper; expected popup/menu target needs confirmation. | DJC controller mapping with screen/menu controls. | Trigger `djc_button_popup` from a spare mapping button; note whether it opens a menu, affects a selected DJC button, or requires parameters. | TBD | TBD | Untested | Official name only; requires matching DJC-family context. |
| `djc_button_slider` | DJC slider-button helper; hardware control semantics need confirmation. | DJC controller mapping with slider/button controls. | Bind `djc_button_slider` to an encoder/slider test control and observe any display or selection changes. | TBD | TBD | Untested | Official name only; requires matching DJC-family context. |
| `djc_button_select` | DJC selection helper; likely navigates or commits a hardware-menu choice. | DJC controller mapping/menu context. | Open any DJC-related menu/popup, trigger `djc_button_select`, and record whether it selects, cycles, or toggles an item. | TBD | TBD | Untested | Official name only; requires matching DJC-family context. |
| `djc_panel` | DJC panel helper; target panel names/states are not locally verified. | DJC controller display/panel mapping. | Trigger `djc_panel` from a spare button and, if needed, try known panel identifiers from the stock mapping; record visible panel changes. | TBD | TBD | Untested | Official name only; requires matching DJC-family context. |
| `denon_platter` | Denon-specific platter action/helper; platter LED/display behavior depends on device family. | Denon controller/player mapping; platter display feedback. | On supported Denon hardware, bind `denon_platter` and compare with `` `get_denon_platter` `` while playing, cueing, scratching, and changing deck assignment. | TBD | TBD | Untested | Official name only; requires Denon platter/display hardware. |

## System And Config Helpers

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `connect` | Official skins use it, but action/query behavior varies by account connection state. | Skin button, custom button, config/account UI. | Test logged out and logged in: run `connect`, then display/query `` `connect` `` if accepted; record opened UI and returned state. | v2026-m b9336 | None required | Pass | Logged in: green `CONNECT: on`; pressing opens menu with `Log out`. Logged out: red `CONNECT: off`; pressing opens CONNECT login dialog. |
| `system` | Sparse official system helper; parameters and return behavior are unclear. | Custom button, skin query/text, possible system integration context. | Run `system` with no parameter in a custom button; then try a harmless known/obvious parameter only if official examples are found; record UI/log output. | v2026-m b9336 | None required | Partial | In the sparse helper pad context, `` `system` `` returned blank text and pressing `system` produced no visible UI change or new Log Report entry. Still too sparse to promote beyond a conservative note; do not infer from `system_volume` or system VU labels. |
| `open_stem_creator` | Opens a workflow that may depend on license/build/stem features. | Skin/custom button, config/workflow action. | Run `open_stem_creator` with a track selected and with no track selected; note opened window, gating, and any error/status message. | v2026-m b9336 | None required | Pass | Pressing it opened the Stem Creator dialog with per-stem input pickers, Output, Headroom, and Create controls. A selected browser track did not auto-fill; 0 browser results opened the same blank dialog. Full export/create and license gating not tested. |

## FX Helpers

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `effect_has_slider` / `effect_has_button` and `get_effect_slider_*` / `get_effect_button_*` | Built-in skins use these heavily, but the exact return shapes and context scoping need a focused local fixture. | Skin controls, pad text/query, custom button display; deck FX, video FX, transition FX. | Load [Reference - FX Introspection Test.xml](../tests/Pads/Reference%20-%20FX%20Introspection%20Test.xml), press each LOAD pad, observe slider/button counts, labels, defaults, text, and `effect_has_*` states; read Shift-layer pads 5-14 (exact strings via `name=`); repeat separately for `video` and `transition` targets. | v2026-m b9482 | None required | Pass | Deck FX slot 1, Backspin (2 sliders / 0 buttons). Reliable and GUI-matching: `get_effect_name`=`Backspin`; `get_effect_slider_count`=2, `get_effect_button_count`=0; `effect_has_slider`/`effect_has_button` lit correctly per position; `get_effect_slider_text`=`0%`/`4 bt` (matches GUI values). Label family splits: `get_effect_slider_label`=`get_effect_slider_shortname`=`STR` (short), while `get_effect_slider_label_full`=`get_effect_slider_name`=`Strength` (full, matches GUI). `get_effect_slider_default` has two working forms (resolved by a follow-up probe plus shipped-skin evidence): the effect-name form `get_effect_slider_default 'Backspin' 1` returned `0.5` — a genuine normalized 0-1 default, distinct from the current `0%`, and not the trailing `1` (which is a fallback, not a slider index). The slot form `get_effect_slider_default 1 1 0.5` returned `off` in the same pad `name=` text context. Built-in skins ship both: deck skins use `<slot> <index> <fallback>` 300+ times inside `<slider frommiddle=…>` (numeric-value) contexts, and the Broadcast video skin uses the effect-name form `frommiddle="get_effect_slider_default 'active' 0.5"` — where `0.5` is the fallback — confirming the target-name signature (`examples/VideoSkins/Built-In/broadcast/broadcast.xml:241`). So the slot form is context-sensitive, not broken; my initial "broken" conclusion was a wrong-argument call (slot `1` passed where the form wanted a target name). Separate finding: `debug` logs the literal backtick expression instead of evaluating it (same computed-argument behavior as loop/beatjump/phrase_sync), so exact strings must be read via `name=` interpolation. **Follow-up sweep (VirtualDJ 2026, HTTP interface, 2026-07-22):** every one of these helpers accepts an effect *name* where the docs show a slot number — `get_effect_slider_count 'Echo'`, `get_effect_slider_default 'Echo' 3` — returning the same values as the slot form for all 119 title-resolvable effects, with no `effect_select` and no state change. That makes introspecting an effect you have not loaded a read-only operation. `get_effect_title '<name>'` returns `'<Canonical> - Deck N'` or `''`, so it resolves names and probes existence (case-insensitive, not space-insensitive; blind to `Stems`/`Vocals`, which still introspect through a slot). The `*_skip_length` variants **re-index** rather than blank: index *i* is the *i*-th slider of the list with the length slider removed, so the last index is always empty — verified on all 47 length-bearing effects, where the length slider is not always index 2 (`Loop Out`, `Slideshow` put it first) and not always labelled `LEN` (`Phaser`, `Wahwah` label it `SPD`). |
| Native effect parameter examples | Existing pad pages provide working presets, but the repo does not yet have a systematic effect-by-effect slider/button map. | Pad XML and skin/custom button controls for selected native effects. | Use [Reference - FX Introspection Test.xml](../tests/Pads/Reference%20-%20FX%20Introspection%20Test.xml) as a starter fixture; for each native effect, load it in slot 1, record counts, labels, defaults, button count, and tested `effect_slider`/`padfx` presets with VirtualDJ build/effect version. | v2026-m b9482; full pass TBD | None required | Partial | Per-effect map (deck FX slot 1, v2026-m b9482) started in `docs/Effects Engines.md`: **Backspin** — 2 sliders, 0 buttons: S1 `Strength`/`STR` (%, e.g. `0%`), S2 `Length`/`LEN` (beats, e.g. `4 bt`). **Flanger** — 4 sliders, 2 buttons: S1 `Strength`/`STR` (`50%` reset), S2 `Speed`/`LEN` (`8 bt` reset), S3 `Feedback`/`FBCK` (`50%` reset), S4 `LFO Amp`/`LFO` (`50%` reset); B1 `Tone`/`TONE`, B2 `Phase`/`PHASE`. **Echo** — 6 sliders, 4 buttons: S1 `Strength`/`STR` (`52%` reset), S2 `Length`/`LEN` (`1/2 bt` reset), S3 `Feedback`/`FB` (`52%` reset), S4 `Filter`/`FILT` (`OFF` reset), S5 `Lowpass`/`LP` (`20 Hz` reset), S6 `Highpass`/`HP` (`20000 Hz` reset); B1 `Reverse`/`REV`, B2 `Freeze`/`FRZ`, B3 `Mute Source`/`MUTE`, B4 `Lock On Max`/`LCK`. **Reverb** — 4 sliders, 2 buttons: S1 `Strength`/`STR` (`50%` reset), S2 `Decay`/`DEC` (`50%` reset), S3 `Room Size`/`SIZE` (`50%` reset), S4 `Brightness`/`BRI` (`50.0%` reset); B1 `Low Cut`/`LOW`, B2 `Hi Cut`/`HI`. **Beat Grid** — 1 slider, 2 buttons: S1 `Slot`/`SLOT` (`Slot 1` reset); B1 `Mode`/`>>`, B2 `Video`/`VIDEO`. Reset changed the slot readback from `Slot 3` to `Slot 1`; the GUI showed the mode choices as `SNGL` and `CONT`. The canonical selector is `'Beat Grid'`: the earlier `'BeatGrid'` loader left the previous effect selected, so affected fixtures/examples were corrected. **Beat Brake** — 4 sliders, 1 button: S1 `Strength`/`STR` (`50%` reset), S2 `Pattern`/`PAT` (`Pat 1` reset), S3 `Bars`/`BARS` (`2 bars` reset), S4 `HPF`/`HPF` (`Off` reset); B1 `Quantize`/`QUANT`. **BrakeStart** — 1 slider, 1 button: S1 `Length`/`LEN` (`2.76 s` reset); B1 `Restart Play`/`RESTART`. The live name corrected the stale catalog spelling `Break Start`. **Choppa** — 3 sliders, 1 button: S1 `Strength`/`STR` (`100%` reset), S2 `Length`/`LEN` (`Pat 1` reset), S3 `Invert`/`INV` (`Off` reset); B1 `Quantize`/`QUANT`. **Cut** — 4 sliders, 4 buttons: S1 `Strength`/`STR` (`52%` reset), S2 `Length`/`LEN` (`1/2 bt` reset), S3 `Duty`/`DUTY` (`50%` reset), S4 `Swing`/`SWING` (`0%` reset); B1 `Low Cut`/`LOW`, B2 `High Cut`/`HIGH`, B3 `Mute Beats`/`INV`, B4 `Video`/`VIDEO`. **Cyclone** — 3 sliders, 0 buttons: S1 `Strength`/`STR` (`50%` reset), S2 `Length`/`LEN` (`1/2 bt` reset), S3 `Delay`/`DELAY` (`203 ms` reset). **Delay** — 4 sliders, 2 buttons: S1 `Strength`/`STR` (`52%` reset), S2 `Length`/`LEN` (`1/2 bt` reset), S3 `Swing`/`SWING` (`0%` reset), S4 `LR Ratio`/`LR` (`0%` reset); B1 `Low Cut`/`LC`, B2 `High Cut`/`HC`. Counts and `effect_has_*` positions matched the visible controls. The by-name default pad remained hardcoded to Backspin, so its `0.5` was excluded for the other effects. **Superseded by the full sweep (VirtualDJ 2026, HTTP interface, 2026-07-22):** [tools/sweep_fx_introspection.py](../tools/sweep_fx_introspection.py) captured counts, short+full labels, normalized defaults, live value text, and length/beats flags for all **119** installed effects into [tests/fx-introspection-dump.json](../tests/fx-introspection-dump.json). Query it with `just get-fx <effect>` / `just list-fx` rather than reading either the dump or the prose above; the hand-written entries here are kept only as the provenance of the original method. Spot-checked identical to the hand map. |
| `get_mixfx_active` | Official sparse Mix FX helper; return value and relationship to `effect_mixfx_activate` needed confirmation. | Skin text/query, pad query/color, custom button display. | Load [Reference - Mix FX Query Test.xml](../tests/Pads/Reference%20-%20Mix%20FX%20Query%20Test.xml), select Filter/Echo, toggle Pad 7 `effect_mixfx_activate` off/on, then compare Pad 8 and shift-pad debug output for `` `get_mixfx_active` ``. | v2026-m b9336 | None required | Pass | In pad text/query/color, `` `get_mixfx_active` `` returned `off`/`on` and matched `effect_mixfx_activate` for Filter and Echo once a track was loaded on deck 1. |
| `effect_select_multi` with `effect_active <slot> '<effect>'` | Multi-effect-per-slot behavior is official by name/summary but easy to miss in pad design. | Pad XML, numeric deck FX slot, named stem FX slot. | Build a two-pad page for slot 1 and `vocals`: Echo Out pad uses `effect_select_multi ... 'echo out'`; Reverb pad uses `effect_select_multi ... 'reverb'`; query each with `effect_active ... '<effect>'`; verify independent LED state and simultaneous audio. | User-provided local result, build not recorded | None recorded | Partial | User-provided vocal-slot pads confirmed Echo Out and Reverb light independently while both play on the `vocals` stem FX slot. Conservative guidance is promoted to the `effect_select_multi` and `effect_active` entries; repeat on a recorded build for fixture-grade `Pass`. |
| `padfx` shared identity and `effect_disable_all 'padfx'` ordering | `padfx` is useful for quick triggers, but deterministic chained presets can be affected by shared effect/stem targets and cleanup timing. | Pad XML with stem-targeted pad FX. | Create Pad A with `effect_disable_all 'padfx' & padfx 'echo out' ... 'stemfx:vocal' & padfx 'reverb' ... 'stemfx:vocal'`; create Pad B with the same chain but no inline clear; create Pad C using one of the same effect/stem targets at different values; observe pad light/audible behavior and parameter changes. | User-provided local result, build not recorded | None recorded | Partial | Inline `effect_disable_all 'padfx'` before new padfx calls did not activate/light; removing it worked. Another pad using the same effect/stem target can alter the active pad-FX parameters. Conservative guidance is promoted to the `padfx` notes and `effect_disable_all 'padfx'` example: treat cleanup as a separate broad reset, not as private per-pad state or an inline initializer. Repeat with `effects_used 'padfx'` before promoting to fixture-grade `Pass`. |
| Numeric and named FX slot selected-effect restart persistence | Official docs emphasize deck FX slots 1-6; user observation suggests restart persistence follows that same boundary. | Pad XML or custom buttons using `effect_select`, `effect_select <slot>`, and `get_effect_name`; normal deck FX slots 1-8 and named stem FX slots. | Use [FX-SLOTS.xml](../examples/Pads/Quarantine/FX-SLOTS.xml) or equivalent controls; select visible effects for FX1-FX8 and named stem FX slots such as `vocals`/`rhythm`; load tracks; close/reopen VirtualDJ; compare returned loaded effect names. | User-provided local result, build not recorded | None recorded | Partial | FX1-FX6 kept their loaded effect across restart. FX7+ and named stem FX slots kept loaded effects across track loads/current session but reset after restart. This is selected-effect persistence only; active state, slider values, and multi-effect contents need separate testing. |
| `effect_bank_save` / `effect_bank_load` | Official rack snapshot helpers; persistence, scope, and active-state recall need a reproducible note. | Deck FX slots 1-6, HTTP or pad. | Read-only recon first (`effect_bank_load N` + restore) to find an empty bank; save/load a round-trip into it; test active-state and slider recall and deck scope. | VirtualDJ 2026 (HTTP interface, 2026-07-26) | None required | Pass | A bank is a rack of effect **selections** (slots 1-6), nothing more. `effect_bank_save N` writes the selection; `effect_bank_load N` restores it. **Round-trip:** scrambled slots via one bank, loaded another, exact selection returned. **Return value is an existence probe:** load returns `true` for a populated bank, `false` for an empty one (banks 1-3 held user racks → true; 4-8 empty → false); save always returns `true`. **Active state NOT recalled:** saved with slot 1 active, deactivated, loaded → stayed inactive. **Slider values NOT recalled:** slider left at its changed value after load (effect was already selected). **Global, not per-deck:** a rack saved on deck 1 loaded intact onto deck 2. Safe-testing method confirmed: pick an empty bank via the load-return probe rather than writing over an occupied one. |
| `effect_releaseslider` / `effect_releaseslider_active` / `is_releasefx` | Release-FX path is separate from normal slot sliders; selection and query behavior need a recorded result. | Pad/custom button/momentary control with a selected release FX. | Compare `is_releasefx` with various effects in deck slots; test the release sliders against normal `effect_slider`. | VirtualDJ 2026 (HTTP interface, 2026-07-26) | None required | Partial | Confirmed **separate from deck-FX slots 1-6**: `is_releasefx` stayed `no` with every effect loaded into slot 1, release-type effects included (Backspin, BrakeStart, VinylBrake, Beat Brake) — loading into a numbered slot never arms it. Forms `is_releasefx`, `is_releasefx <slot>`, `is_releasefx '<effect>'` all `no`. `effect_releaseslider` / `effect_releaseslider_active` are accepted (execute `true`) but **inert** without an armed release FX: `effect_releaseslider 50%` left the readback at `0` and did not flip `is_releasefx`. Arming a release FX needs a momentary press/release this channel cannot drive, so activation and slider behavior still need a pad or mapper surface. |
| `effect_fxsendreturn*` helpers | Routing depends on mixer/send-return context and may be hardware-sensitive. | Skin/custom button, controller with software/hardware FX send-return path. | Toggle `effect_fxsendreturnenable`, select master/mic/deck sources with `effect_fxsendreturndeck_multi`, and record available/visible routing changes. | TBD | Optional hardware | Untested | Official names are present; practical behavior is context-dependent. |
| `effect_command` plugin commands | Command strings are plugin-specific; built-in BeatGrid UI provides evidence but not a universal command map. | BeatGrid plugin in a deck FX slot, track loaded. | Load `Beat Grid` into slot 1 with a track on the deck; probe `get RC` / `set RC` / `cur N` per the built-in `Plugin-UI/AFX_beatgrid.xml`. | VirtualDJ 2026 (HTTP interface, 2026-07-26) | None required | Pass | **Plugin-instance-scoped, not generic.** `effect_command 'get 00'` returned `no` with Phaser in slot 1 and `yes` after loading `Beat Grid` there. Two forms: bare `effect_command '<cmd>'` targets the loaded plugin; `effect_command <slot> '<cmd>'` takes an **unquoted** slot number (`effect_command 1 'get 00'` → yes; quoted `effect_command '1' …` → no). BeatGrid vocabulary, confirmed live against the built-in UI: `get RC` queries the grid cell at row R, col C (hex); `set RC` toggles it (verified reversible on an editable cell: off→set→on→set→off, grid left pristine); `cur N` is the current-playback-column indicator. Needs a loaded track for grid content. Do **not** document as generic plugin control. |
| Video FX slot controls | Built-in skins expose video FX panels, but a focused behavior pass would improve examples. | Built-in skin or test skin with video output enabled. | Select a video FX, toggle `video_fx`, move `video_fx_slider 1`, test `video_fx_clear`, then repeat with `deck master video_fx...`; record text/query behavior. | VirtualDJ 2026 (HTTP interface, 2026-07-22) | None required | Partial | Selection and enumeration are characterized; rendering behavior is not. `video_fx_select +1` cycles the enabled video-FX list (**17** entries here) with readback via `get_videofx_name`; `video_transition_select +1` cycles transitions (**35** entries, including `None`) with readback via `get_videotrans_name`. The three `+1` cycles — deck FX, video FX, transition — are **disjoint**, which is the app's own category assignment and the only working audio-vs-video discriminator found: **loadability is not one**, because all three selectors accept any installed effect name by name (`video_fx_select 'Echo'` really does set the video slot to Echo). Each cycle is the *enabled/favorites* subset, so an installed effect in no cycle (here `Lottery`, `Sweep`, `Title`, `Vocals`) is category-unknown rather than uncategorised. Both readback verbs ignore their argument. Still untested: `video_fx_slider`, `video_fx_clear`, `deck master` scoping, and what any of these actually render. |

## Deck And Mode Helpers

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `deck_has_error` | Official sparse loading/deck helper; error state and reset behavior are now locally characterized in a pad-page load workflow. | Deck skin query/text, load workflow, custom button display. | Load [Reference - Deck Error Test.xml](../tests/Pads/Reference%20-%20Deck%20Error%20Test.xml), compare current/deck-scoped `` `deck_has_error` `` before load, after a valid selected-track load, after unload, after loading the deliberately missing file, and after a subsequent valid load. | v2026-m b9336 | None required | Pass | In the pad-page run, `deck_has_error` stayed off for normal load/unload states, turned on/red after a deliberately missing file load, scoped to deck 1 while deck 2 stayed off, and cleared after a later successful selected-track load. |
| `dualdeckmode_decks` | Official prose ties it to dual-deck pairs 1/3 or 2/4, but mapping behavior remains sparse. | Controller mapping, deck assignment logic, dual-deck mode. | Load [Reference - Dual Deck Mode Test.xml](../tests/Pads/Reference%20-%20Dual%20Deck%20Mode%20Test.xml), toggle `dualdeckmode`, compare current and `deck 1`-`deck 4` `` `dualdeckmode_decks` `` labels/queries/logs, then repeat from deck-pair contexts 1/3 and 2/4 if available. | v2026-m b9336 | Optional controller | Partial | In the pad-page run, `dualdeckmode` toggled on/blue but current and deck-scoped `dualdeckmode_decks` readbacks stayed false/red; repeating on deck 2 gave the same result. Test a visible dual-deck pair/controller context before promotion. |

## Karaoke

| Verb | Why local test | Likely surface/context | Suggested minimal repro | VirtualDJ build | Hardware | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `karaoke_venue_name` | Sparse karaoke helper; source of value and empty-state behavior need confirmation. | Karaoke skin text/query, karaoke options/config. | Set/clear the venue name in karaoke options, display `` `karaoke_venue_name` ``, and record value, fallback text, and whether changes update live. | v2026-m b9336 | None required | Pass | Empty venue returns blank after `KARAOKE:`. Pressing the pad opens the Karaoke menu; Venue Name dialog sets the value; clearing the venue returns to blank. |

## Grammar Battery Over HTTP

VirtualDJ 2026, HTTP control interface, 2026-07-22. Global variables (`$zz_*`) as
observable side effects: reset to 0, execute the script, read back with `get_var`. This
reproduces the pad [Grammar Battery](../tests/Pads/Reference%20-%20Grammar%20Battery%20Test.xml)
without a fixture or manual reading. Settled rules are written up in
[VDJScript Grammar](VDJScript%20Grammar.md); this table is the run record.

| Question | Script | Observed | Result |
| --- | --- | --- | --- |
| Branch extent, chains both sides | `on ? set a & set b : set c & set d` | `a=1 b=1 c=0 d=0`; with `off`, `0011` | Pass — each branch takes its whole chain |
| Trailing `&` binding (cross-surface check) | `on ? set a : set b & set c` | `1000`; with `off`, `0110` | Pass — reproduces the pad result exactly, so the rule is parser-level not surface-level |
| Leading `&` split (cross-surface check) | `set a & on ? set b : set c` | `1100`; with `off`, `1010` | Pass — reproduces the pad result |
| `&&` in action position | `off && set a` | `a=1` | **Fail as a guard** — action runs regardless; same for a false `var_equal`. `&&` behaves as `&` here |
| Correct action guard | `var_equal '$x' 999 ? set a : nothing` | `a=0` when false, `1` when true | Pass — ternary is the only guard; `nothing` is a valid action-position null branch |
| Constants in value position | `set '$v' on` / `off` / `true` / `false` | `yes` / `no` / `''` / `''` | Pass — `on`/`off` are constants, `true`/`false` are not |
| String variable readback | `set '$v' 'apple'` then `get_var`/`var_equal` | `get_var`=`''`; `var_equal` = `yes` vs `'apple'`, `'banana'`, bare `banana` | **Fail** — string variables are write-only: unreadable and uncomparable; `var_equal` matches anything |
| Numeric variable readback | `set '$v' 5` | `var_equal '$v' 5`=yes, `'5'`=no, `7`=no | Pass — quoting is type-significant |
| Comment syntax | `set a 1 // set b 1`, and `#`, `;`, `--`, `/*x*/` | `a=1 b=0` in all five | Pass (negative) — no comment syntax; every marker silently discards the rest of the statement |
| Chain length ceiling | 142 vs 152 `set` statements; 302 vs 402 cheap statements | 142 and 302 all ran; 152 and 402 ran **nothing at all**, `execute` still `true` | Partial — a ceiling exists and failure is total, not truncating; boundary moves with statement content. Identical on GET and POST, so not a URL artefact |
| `while_pressed` placement | `set a 1 while_pressed & set b 1` | `a=1 b=1` | Partial — accepted trailing and mid-chain, does not block the chain; release behavior untestable over HTTP |

Side effect: this run leaves `$zz_*` session globals set. They are session-scoped and clear
on VirtualDJ restart.

## Mapper Firing (Real Hardware)

VirtualDJ 2026, HTTP interface + AlphaTheta DDJ-GRV6, 2026-07-27. A minimal test
mapper for `device="DDJGRV6"` bound `ONINIT` and `PLAY_PAUSE` to `set '$var' 1`;
probes read back over HTTP. Confirms the mapper `<map value action>` schema fires
on real hardware, and surfaces three operational facts.

> Correction (same session): an earlier draft claimed "loading a mapping resets `$` globals." That was confounded — the test mapping required **two** VirtualDJ restarts (one to make the new file appear, one to load the `PLAY`→`PLAY_PAUSE` edit), and session globals clear on restart regardless. There is no clean evidence a mapping *switch* clears globals; the claim is retracted.

| What | Script / step | Observed | Result |
| --- | --- | --- | --- |
| `<map>` binding fires on button press | `<map value="PLAY_PAUSE" action="set '$vdj_maptest_fired' 1"/>`, press play | `$vdj_maptest_fired` 0 → 1 over HTTP | Pass — first local proof a mapper binding executes on hardware |
| `ONINIT` fires on load | `<map value="ONINIT" action="set '$vdj_maptest_init' 1"/>` | `$vdj_maptest_init` = 1 after load and after restart | Pass |
| Control name must match exactly | `value="PLAY"` (real name is `PLAY_PAUSE`) | loaded without error, never fired | Pass (negative) — wrong name binds nothing, silently (no-error parsing) |
| New/edited mapper file needs a restart | add a file, then edit it | new file did not appear in the selector until restart; re-selecting after an edit served the cached copy | Pass — VirtualDJ scans `Mappers/` at startup; both new files and in-place edits need a restart (two restarts this session). Switching between mappings it already knows is live. |

Not covered: the custom **device-definition** (`<device>`) schema. The DDJ-GRV6 is
factory-recognized (compiled `controllers.dat`), so a custom `<device>` XML is not
exercised. Testing that needs unrecognized hardware or a virtual MIDI port + injection.

## Plugin Channel (VDJIntrospect)

VirtualDJ 2026 (bundle `18.0.9583`), macOS arm64, 2026-08-15. First capture from the
fifth Tier-1 channel: a read-only plugin ([tools/plugin/VDJIntrospect.cpp](../tools/plugin/VDJIntrospect.cpp))
calling `GetInfo` and `GetStringInfo` on all 1,028 verb-table names, bare, in query
position only — the plugin contains no `SendCommand` call. Idle app, no track loaded,
crossfader centred. Artifact `tests/plugin-introspection.json`; query with
`just plugin-probe <name>`.

| What | Script / step | Observed | Result |
| --- | --- | --- | --- |
| The documented loading path is live | drop an ad-hoc-signed bundle exporting `DllGetClassObject` into `PluginsMacArm/AutoStart/`, restart | VirtualDJ called it 6 times with `CLSID_VdjPlugin8`, type-probing in order: `IVdjPluginDsp8`, `IVdjPluginBuffer8`, `IVdjPluginVideoFx8`, `IVdjPluginVideoTransition8`, `IVdjPluginVideoTransitionMultiDeck8`, then `IVdjPluginBasic8` — accepted, `OnLoad` fired | Pass — SDK's COM path works on this build; probing stops at the first accepted IID (`IVdjPluginStartStop8` and `IVdjPluginOnlineSource` were never reached, so their position in the order is unknown) |
| Ad-hoc signature is sufficient | `codesign --sign -`, no Developer ID | loaded | Pass — VirtualDJ carries `com.apple.security.cs.disable-library-validation` |
| Xcode is not required | Command Line Tools `clang++ -bundle` | loaded | Pass |
| `master_beat_num` float-bits defect is in the CORE, not HTTP rendering | `GetInfo("master_beat_num", &d)` | `S_OK`, `d = 1083943558.0` exactly (bits `0x41d026eaa1800000`) — the double holds the *integer*. Reinterpreting `0x409baa86` as float32 gives `4.8646` | Pass — settles the open question: the coercion happens before the value reaches either channel, so HTTP was faithfully rendering an already-broken number. Consumers must reinterpret the int32 bits as float32. |
| The two channels answer with distinct, informative codes | both calls per verb | `GetInfo`: `S_OK` ×543 / `E_INVALIDARG` ×485. `GetStringInfo`: `S_OK` ×599 / `S_FALSE` ×429. No other code appeared | Pass — "wrong channel" is `E_INVALIDARG` on the numeric side and `S_FALSE` (not an error) on the text side |
| Channel map over all 1,028 names | classify by which call returned `S_OK` | both 532, text-only 67, numeric-only 11, neither 418 | Pass — booleans answer on both (`play` → `0.0` / `"off"`), so the numeric channel gives native 0/1 for the 334 HTTP-"bool" verbs |
| Agreement with the HTTP existence sweep | join on the sweep's `kind` | 181/181 `action-only` and 113/116 `needs-args` answered on neither channel; all 602 answering names are HTTP `query` verbs | Pass — the channels agree on kind |

Caveat on the numeric channel: VirtualDJ writes `0.0` to `*result` even when it returns
`E_INVALIDARG`, so **the HRESULT, not the value, is the answer** — a raw `0` is
indistinguishable from a real zero without it.

Leads, not conclusions:

- **50 HTTP `query` verbs answered on neither plugin channel** (e.g. browser/deck-scoped
  names). Most likely a context difference — HTTP `/query` evaluates with a deck context
  a plugin's bare call lacks — but that is untested. Re-probe with `deck 1 …` prefixes.
- **5 `action-only` and 3 `needs-args` verbs returned text**, which the HTTP sweep could
  not see.
- The **HRESULT keyword-discrimination hypothesis** (does `loaded opposite` differ from
  `loaded bogusword` in HRESULT where the value is identical?) is NOT tested here — this
  capture is bare verbs only. It needs an argument-bearing probe list.

### Follow-Up Captures (2026-08-15, same build and session)

Three leads from the bare-verb capture, chased with two further probe lists
(`tests/plugin-introspection-leads.json`, `-controls.json`; `just plugin-probe <probe>`
finds a record in any capture).

**Lead A — argument keywords are distinguishable by HRESULT. Hypothesis CONFIRMED.**
165 keyword/nonsense pairs over the 62 keyword-bearing verbs whose contract says
`executes: false` (execute-capable verbs were deliberately excluded: query position is
side-effect-free in this repo's model, but `browser_window sampler` is not worth
betting that on). Each binary-recovered keyword was paired with `zzznotakeyword` on the
same verb.

| Outcome | Count | Example |
| --- | ---: | --- |
| HRESULT differs | 26 | `is_using cue` → `S_OK`/`off`; `is_using zzznotakeyword` → **`E_NOTIMPL`**/`S_FALSE` |
| Value differs only | 14 | `get_cpu audio` → `0`; nonsense → `0.01` |
| Indistinguishable | 125 | — |

Two discriminator shapes: **`E_NOTIMPL`** on the numeric channel (all ten `is_using`
keywords) and **`E_INVALIDARG`** (`action_deck left|right`, `device_side`,
`get_ns7_platter on_instant|off_instant|rpm`). `get_browsed_color` corroborates itself:
`red`/`green`/`blue` return `243`/`198`/`211` where nonsense falls back to the hex string
`#F3C6D3` — the same three bytes, so the keywords are component selectors.

**Do not read the 125 as disproof.** The app was idle with no track loaded; most of those
keywords had nothing to vary. Absence of discrimination in an unprepared state is not
evidence the keyword is unrecognized.

Two **argument traps** — a nonsense argument answering confidently and wrongly:

| Probe | Real keyword | Nonsense argument |
| --- | --- | --- |
| `get_license` | `home` → `off`, `pro` → `on` | `get_license zzznotakeyword` → **`on`** |
| `mixermode` | `external` → `off` | `mixermode zzznotakeyword` → **`on`** |

Neither is a safe existence probe for a license or a mode name.

**Lead B — the eight action verbs that returned text are LABEL PROVIDERS, and they
identify vtable slot 5.** `stop_button` → `"■"`, `scratchbank_load` → `"Bank A"`,
`sampler_pad_page` → `"1 to 8"`, `sideview_sort` → `"Original Sort Order"`. Cross-tabbing
the whole capture against `tests/action-contracts.json` partitions it exactly: of the 174
verbs that do **not** override slot 3, precisely 5 answer text and **all 5 override slot
5**; the other 169 answer nothing. All 599 text answers in the capture come from a verb
overriding slot 3 (594) or slot 5 (5), with no remainder. So slot 3 backs *both* callbacks
and slot 5 is a fallback label provider. Slot 4's role is **not** established — all 85 of
its text-answering verbs also override slot 3, so it explains nothing on its own.

**Lead C — deck context was the wrong explanation. REFUTED, with a control.** All 100
`deck 1 …` / `deck 2 …` re-probes of the 50 silent query verbs returned
`E_INVALIDARG`/`S_FALSE`. A control batch proves the prefix itself works on this channel
(`deck 1 get_bpm` → `120`, `deck left get_bpm` → `120`), so the negative is real. Note
`left get_bpm` **fails** — the `deck` scope word is required here.

What the 50 actually are:

| Group | Count | Evidence |
| --- | ---: | --- |
| HTTP answered empty too — no divergence | 27 | The plugin channel reports "no value" as `E_INVALIDARG`; HTTP renders it as `""`, indistinguishable from a real empty answer. **The plugin channel separates the two; HTTP cannot.** |
| Wanted an argument | 7 | `get_constant 1` → `1`, `sampler_group_name 1` → `Drums`, `effect_beats 1` → `64 bt` |
| Real divergence: HTTP has a value, plugin silent | 21 | Mostly effect-slider readers, and it is about **implicit defaults, not context**: `get_effect_slider_name` is silent bare but `get_effect_slider_name 1 1` and `get_effect_slider_name 'Blur' 1` both return `Strength`. HTTP's evaluation path supplies a default slot/index that a plugin call does not. |

Still unexplained inside that last group: the browser readers (`get_browsed_folder` →
`All Files` over HTTP) stay silent on the plugin channel even with an argument. A browser
context that HTTP evaluation has and a plugin call lacks is the obvious guess — untested.

### Delayed Sweep And The Execute-Capable Keyword Verbs (2026-08-15)

Two more captures in one restart, from a plugin build that also sweeps a second
list ~40s *after* load (`tests/plugin-introspection-{remaining,late}.json`).

**The silent browser verbs were a STARTUP-TIMING artifact, not a missing plugin
context.** `OnLoad` fires while VirtualDJ is still starting, so a subsystem that
has not initialized is indistinguishable from a verb that never answers. Swept
again 40 seconds later, with no other change, six browser readers came alive:

| Verb | At load | 40s later |
| --- | --- | --- |
| `get_browsed_folder` | silent | `All Tracks` |
| `get_browsed_folder_path` | silent | `filters:/All Tracks.vdjfolder` |
| `get_browsed_folder_icon` | silent | `8` |
| `get_browsed_folder_scrollpos` | silent | `0` |
| `get_browsed_folder_scrollsize` | silent | `29` |
| `get_browsed_folder_tab` | silent | `1` |

**Method consequence:** an `E_INVALIDARG` from this channel means "not available
*now*", not "no such form". Any negative result taken at load time is suspect,
and should be re-taken from the delayed sweep before being recorded.

Still silent at 40s: the song-level readers (`get_browsed_comment`,
`get_browsed_composer`, `get_browsed_song`) and the effect/controller readers.
The song-level three answer over HTTP with a song highlighted, so a *selection*,
not just an initialized browser, is the next thing to vary.

**Execute-capable keyword verbs, query position only.** 1,126 probes over 217
verbs (10 excluded outright — the file/config/system families:
`auto_cue`, `broadcast_message`, `browsed_file_analyze`, `browsed_file_rename`,
`debug`, `effect_bank_save`, `play_mode`, `setting_if_unchanged`,
`setting_ismodified`, `system`). Run the split with
`just plugin-keyword-report remaining [--verbose]`.

| Outcome | Pairs | Verbs |
| --- | ---: | ---: |
| Confirmed by HRESULT | 51 | 25 |
| Confirmed by value | 36 | 27 |
| Indistinguishable in idle state | 605 | — |

Confirmed enum sets include `crossfader_curve` (`scratch` active, plus `custom`,
`cut`, `disabled`, `full`, `smooth`), `maximize`
(`fullscreen`/`maximized`/`original`/`windowed`), `loop_adjust` (`move`, `out`),
`browser_scroll` (`top`, `bottom`), `cue_display` (`num`, `number`),
`auto_bpm_transition_options` (`autostart`, `length`, `loop`, `master_tempo`),
`font_size` (`big`), and `djc_button_select` (`deck1`-`deck4`, `deckA`, `deckB`).

**Safety check on probing execute-capable verbs in query position: no state
changed.** All 217 bare verbs common to this capture and the load-time baseline
returned byte-identical values afterwards (0 differences), and HTTP readback
agreed. Combined with the plugin containing no `SendCommand` call, that is two
independent reasons the sweep was read-only — but it is evidence from one idle
session, not a proof for every verb.

**Also proven incidentally: the host callbacks are safe to call from a
non-main thread.** The delayed sweep runs on a detached timer thread and
completed 55 probes with no crash, hang, or visible misbehaviour. Undocumented
in the SDK; one session's evidence.

### Prepared-State Capture (2026-08-15)

Taken through the plugin's trigger loop rather than a restart: with VirtualDJ
already running, a track was loaded and playing on deck 1 (`Salt on my lips`,
129 BPM) and a *different* song highlighted in the browser (`No Bite`), then
`just plugin-go` re-swept 1,240 probes in about a second
(`tests/plugin-introspection-prepared.json`). The controls confirm the state took
— `loaded` on, `play` on, `get_title` and `get_browsed_title` differing — so a
null result here cannot be blamed on the setup.

**`loaded opposite` is confirmed, by the value test HTTP could not run.** With
exactly one deck loaded, `loaded opposite` returns `off` where
`loaded zzznotakeyword` returns `on`. This is the case
[TODO.md](../TODO.md) task 10 named in 2026-07-30 as needing prepared state, and
it behaves exactly as predicted: the keyword is silently ignored, so only a state
where the two forms *must* disagree can prove it.

New enums confirmed only with state (25 pairs over 12 verbs):

| Verb | Keywords | Observed |
| --- | --- | --- |
| `get_key` | `pioneer`, `rane`, `roland`, `harmonic` | controller-specific key notations — `14`, `13`, `2`, `02A`, against a default text of `Ebm` |
| `get_loaded_song_color` | `red`, `green`, `blue` | `243`/`198`/`211` vs the `#F3C6D3` hex fallback — the same component-selector shape as `get_browsed_color` |
| `get_position` | `loopin`, `loopout` | `0` vs `0.1` bare |
| `get_song_event` | `hasbeats`, `remaining`, `volume`, `volume_end`, `next` | `S_OK` where nonsense gives `E_INVALIDARG`; `next` also differs in value (`B4-93` vs `bB4-53`) |
| `get_time_msf` | `absolute` | `0` vs `3` |
| `get_crossfader_result` | `full` | `0.5` vs `0` |
| `get_ns7_platter`, `get_denon_platter` | `on_normal`, `off_normal`, `reverse`, `speed`, `speedup` | answer `S_OK` with no hardware attached |

**The song-level browser readers are partly explained.** With a song highlighted,
`get_browsed_key` (`G#`), `get_browsed_filepath`, and `sidereco_song` answer,
having been silent both at load and in the idle delayed sweep. Still silent:
`get_browsed_comment`, `get_browsed_composer`, `get_browsed_song`,
`get_sample_info` — and for comment/composer the likeliest reading is simply that
this track has no such tag, i.e. `E_INVALIDARG` here means "no value", not "no
such form". Untested: a track known to carry a comment.

705 of 730 pairs remain indistinguishable. That is **not** disproof and the
number should not be read as one: it means this particular state gave those
keywords nothing to vary. Each needs the specific state its own verb reacts to,
which is per-verb work, not another sweep.

### `GetSongBuffer` — First PCM Capture (2026-08-15)

VirtualDJ 2026 (bundle `18.0.9583`), track `Salt on my lips` loaded on deck 1.
14 requests through the plugin's trigger loop. **This is the first time anything
in this repo has read decoded audio** — HTTP, Remote, the binary and the XML
corpora all stop at metadata.

| What | Observed | Reading |
| --- | --- | --- |
| Buffer layout | At `pos 0` the leading samples are `[2, 3, 4, 4, 1, 6]`; at `pos 1` they are `[4, 4, 1, 6, 0, 5]` — the same data shifted by **two** shorts, not one | `pos` counts **stereo frames**, and the buffer is **interleaved L/R `short`** |
| Channel split | At `pos 44100` the even/odd RMS are `2726` vs `1122`, with leading samples `[1710, -159, 1763, -173, …]` alternating loud/quiet | Confirms interleaving independently: the two parities are two channels, not noise |
| Negative position | `pos -1` returns **`S_OK`** with `[0, 0, 2, 3, 4, 4]` — two zero shorts, then the `pos 0` data | **Corrected below (pointer capture): this is an unchecked out-of-bounds read, not padding.** The returned pointer is 4 bytes *before* the buffer; those zeros are whatever precedes it in the heap |
| Past the end | `pos 999999999` → `E_FAIL` | Bounded |
| Determinism | The same `(pos, nb)` twice gives an identical hash | No streaming/decode drift between calls |
| Content | RMS `2.6` at the start, `5512` two seconds in | Real audio, and the track begins with near-silence |

`nb`'s unit is **not** established: the probe reads `nb` shorts and never faulted
up to 4096, which is consistent with `nb` counting either frames (twice as many
shorts available as read) or shorts exactly. Do not assume it matches `pos`.

Note `get_totaltime` returned `0` for a loaded, playing track on this channel —
unexplained, and worth a separate look before anything relies on it.

### The Extended Plugin-Info Struct Is Offered (2026-08-15)

`OnGetPluginInfo` is called with `Flags=0x10` (`VDJFLAG_EXTENSION1`) on entry,
for an ordinary non-video plugin. Per the SDK header that means the struct passed
is really a `TVdjPluginInfo8_Extension1`, carrying a `mouseCallbacks` slot for
`IVdjVideoMouseCallbacks8` — whose members are `OnMouseDown`/`OnMouseUp`/
`OnMouseMove` and **`OnKey(const char *ch, int vkey, int modifiers, int flag,
int scancode)`**.

Why this matters beyond plugins: `while_pressed` and the whole down/up half of
the mapper contract are recorded as "not established" precisely because **HTTP
has no press**. `OnKey` is the first channel that might carry one, and its `flag`
parameter is a candidate for press/release. This capture proves only that the
struct is *offered* to a plugin like ours — wiring up the callbacks and pressing
keys is the next build, not a finding yet.

### `GetSongBuffer` Fully Characterized (2026-08-15)

Same track and session, using the trigger loop to run eight further captures in a
couple of minutes — no restarts. The refinement that settled everything was
recording the **returned pointer address** per request: if the addresses are a
linear function of `pos`, the byte step *is* the unit, with nothing left to infer.

**It is a direct pointer into one contiguous, fully decoded buffer.** Across
`pos` 0 → 441,000 the address advances by **exactly 4.00 bytes per unit of
`pos`**, with no deviation:

```
pos      0:        +4 bytes from pos -1     pos   4096:    +16388 bytes
pos      1:        +8 bytes                 pos  44100:   +176404 bytes
pos      2:       +12 bytes                 pos  88200:   +352804 bytes
pos      3:       +16 bytes                 pos 441000:  +1764004 bytes
```

So `buffer = base + 4 × pos`. **No copy, no decode-on-demand, no streaming**: the
entire track is resident as PCM and this hands out interior pointers.

| Property | Value | How it was established |
| --- | --- | --- |
| `pos` unit | **stereo frame** (4 bytes: interleaved L/R `int16`) | 4.00 bytes per unit, exactly, over 441,000 units |
| `nb` unit | **stereo frames too** — same unit as `pos` | At the last valid frame `L`, `nb=1` succeeds and `nb=2` fails; at `L-100`, `nb=101` succeeds and `nb=200` fails. The check is `pos + nb ≤ total_frames` |
| Sample rate | **44,100 Hz** | Cross-check, not assumption: `get_time 'total'` = 306,046 ms predicts frame 13,496,629, and that is exactly where the audio stops (RMS 4.4 → 0.5 → 0.0) |
| Buffer length | 13,562,187 frames ≈ **54 MB** for this 5-minute track | Bisected the `E_FAIL` boundary: frame 13,562,186 valid, 13,562,187 fails |
| Tail | Digital silence (`rms` exactly 0, `max` 0) past the song end | ~65,558 frames of padding — within ms-rounding of exactly 2^16 frames, so a 64Ki allocation slack is the likely explanation |

**Bounds are checked at the top only — `pos` is NOT checked for negatives.**
`pos = -1` returns `S_OK` and a pointer 4 bytes *before* the buffer. The zeros
seen there are adjacent heap memory, not padding; the earlier "zero-padded"
reading in the section above is corrected. **A negative `pos` is an
out-of-bounds read and a caller must not use one.**

Why this matters for [Skin Waveforms](Skin%20Waveforms.md): peak/RMS data for the
whole track, at any zoom, is computable directly and immediately — the audio is
already in memory, and reading it is pointer arithmetic. That is the input side
this repo has never had.

Also noted: `get_totaltime` and `get_length` are **not verbs** on this build
(`E_FAIL` over HTTP). Track length comes from `get_time 'total'` in ms. That also
explains the `get_totaltime` = 0 recorded in the previous capture — it was never
a verb, so the reading was meaningless, not a defect.

### `OnKey` — First Attempt Was INVALID (2026-08-15)

> **Retracted the same day.** This section first recorded a clean negative
> result: callbacks installed, no events delivered. It was confounded. The keys
> were typed while **the browser's search input had focus**, so VirtualDJ
> consumed them as text entry — they would never reach plugin routing whether or
> not such routing exists. The test measured the search box, not the interface.
> A re-test with focus outside any text field is required before anything is
> concluded. The original observations are kept below for the record.

The extended info struct is offered and the callbacks are accepted — the log
records `mouseCallbacks installed` on every load — but no key or mouse event was
delivered **in that invalid run**. `keylog.jsonl` was never created.

The likely reason is in the interface's own name: `IVdjVideoMouseCallbacks8`. Its
mouse coordinates are `(x, y)` pairs, which only mean something relative to a
surface the plugin renders. A plugin with no video output and no window has no
such surface, so there is probably nothing to route events to.

**What the invalid run establishes: nothing about `OnKey`.** Keys going to a
focused text field is ordinary application behaviour and says nothing about
whether VirtualDJ routes input to plugins. Note the mouse clicks logged nothing
either, which is *not* explained by the search-field confound and remains a
genuine (if single) observation.

Re-test method — the confound is the method note worth keeping:

1. Take focus out of every text input first (press `Esc`, or click a deck or
   waveform area). A focused search box eats keystrokes before anything else
   sees them.
2. Prefer keys bound to VirtualDJ shortcuts, which prove the app is receiving
   them as commands rather than as text.
3. Click on non-interactive chrome for the mouse half.

Two routes remain untried, in increasing intrusiveness:

1. **A plugin with a user interface** (`VDJINTERFACE_SKIN` or
   `VDJINTERFACE_DIALOG` from `OnGetUserInterface`). Gives the plugin a real
   surface without touching audio or video.
2. **A video FX plugin** (`IID_IVdjPluginVideoFx8`), which owns a rendered
   surface by definition. More intrusive: it appears in the effect list and needs
   video output to test.

Instrumentation added for the next load: `OnGetUserInterface` and `OnParameter`
now log when called. Whether VirtualDJ ever *asks* a basic AutoStart plugin for a
UI distinguishes "we were never offered a surface" from "we were offered one and
declined it", which decides between the two routes above.

### The Basic AutoStart Plugin Lifecycle Is Headless (2026-08-15)

Re-test after the invalid run, with `OnGetUserInterface` and `OnParameter`
instrumented. Across every load of a plain `IVdjPluginBasic8` in
`PluginsMacArm/AutoStart/`, VirtualDJ calls **exactly two** of the plugin's
methods:

| Callback | Called? |
| --- | --- |
| `OnGetPluginInfo` | yes — once, with `VDJFLAG_EXTENSION1` set |
| `OnLoad` | yes — once |
| `OnGetUserInterface` | **never** (0 calls) |
| `OnParameter` | **never** (0 calls) |
| `OnStart` / `OnStop` | never (we hold `IID_IVdjPluginBasic8`, not StartStop) |
| mouse / key callbacks | never, despite `mouseCallbacks` being accepted |

So this plugin type is a **headless service**: it is handed the host callbacks
and left alone. Everything this channel has produced came from calls the plugin
makes *outward* (`GetInfo`, `GetStringInfo`, `GetSongBuffer`), never from
VirtualDJ calling *in*.

That explains the input silence without needing the earlier
video-surface argument: VirtualDJ never offers this plugin a user interface at
all, so there is no surface, no focus, and nothing to route `(x, y)` events to.
Accepting the `mouseCallbacks` slot is necessary but nowhere near sufficient.

**Consequence for the press/release question.** `OnKey` remains the only
candidate channel in reach, and it is still untested — but reaching it needs a
plugin VirtualDJ actually drives, not merely loads. Ordered by intrusiveness:

1. **Declare a parameter.** The 173 shipped `native_*.ini` manifests show every
   first-party plugin declaring parameters, and parameters are what give a plugin
   a settings panel. If declaring one makes `OnParameter`/`OnGetUserInterface`
   fire, the UI path opens with no audio or video involvement. Cheapest test of
   whether "headless" is inherent to the type or a consequence of declaring
   nothing.
2. **A video FX plugin** (`IID_IVdjPluginVideoFx8`), which owns a rendered
   surface by definition — the interface is called `IVdjVideoMouseCallbacks8`
   for a reason. Intrusive: it appears in the effect list and needs video output.

Until one of those lands, the mapper contract's down/up half stays exactly where
it was: **not established**, and `while_pressed` remains undocumented behaviour.

### A Recognised Plugin Type IS Driven — And `OnKey` Still Does Not Fire (2026-08-15)

The same source built as a Sound Effect (`VDJIntrospectFX`, installed to
`PluginsMacArm/SoundEffect/`), selected on deck 1 and switched on, with its
parameter panel open.

**VirtualDJ called INTO the plugin for the first time.** The headless lifecycle
recorded earlier is a property of the *plugin type*, not of the SDK:

| Callback | Basic, in `AutoStart/` | Sound Effect, active on a deck |
| --- | --- | --- |
| `OnGetPluginInfo`, `OnLoad` | yes | yes |
| `OnStart` | never | **yes** |
| `OnProcessSamples` | n/a | **yes** |
| `OnParameter` | never | **yes** — `id=0 (switch=1)` when the panel switch was toggled |
| `OnGetUserInterface` | never | never observed — **but see the retraction below** |

So a plugin VirtualDJ recognises as a functional type gets driven; one that
answers only to `IVdjPluginBasic8` is loaded and left alone.

> **Retraction (2026-08-22).** The `OnGetUserInterface` / Sound Effect cell above
> read "never (the default UI is built from declared parameters)". That was not a
> measurement. `CVDJIntrospectFX` did not override `OnGetUserInterface` at all in
> that build, so it inherited the header's default and logged nothing — the
> instrument could not have recorded the call even if it happened. The parenthetical
> explanation was an inference dressed as an observation. It **is** called on a
> Sound Effect; see "A Plugin Can Supply Skin XML At Runtime" below.

**`SampleRate = 44100`, straight from the host** — an independent confirmation of
the rate that `GetSongBuffer`'s frame arithmetic implied, arriving through a
different interface. The DSP header's own note that *"samples are stereo, so you
need to process up to `buffer[2*nb]`"* corroborates the frame convention a third
time. First audio buffer: `nb=512` frames.

`SongBpm = 22050` with `SongPosBeats = 0.000` while the deck was not playing.
The header defines `SongBpm` as *samples between two consecutive beats*, and
22050 samples at 44,100 Hz is exactly 0.5 s — i.e. 120 BPM, not the loaded
track's 129. Read as an idle default rather than the song's tempo; untested.

**Key and mouse events still never arrive.** `keylog.jsonl` was never created,
with the effect active, its panel open, focus outside any text field, keys
pressed and the panel's switch clicked. `mouseCallbacks` was installed on every
instantiation.

That is now a **two-type negative**: neither a basic `AutoStart` plugin nor an
active audio effect with a visible panel receives anything through
`IVdjVideoMouseCallbacks8`. The interface's name remains the best explanation —
its `(x, y)` coordinates suggest a *video* surface, which neither of these builds
has.

**Remaining route, and the honest cost.** A video FX plugin
(`IID_IVdjPluginVideoFx8`) owns a rendered surface by definition, and is the last
untried candidate. It needs video output to exercise and appears in the video
effect list. Until then:

- `OnKey` is **untested**, not refuted, on the only surface it plausibly serves.
- `while_pressed` and the down/up half of the mapper contract remain
  **not established**, exactly as before this line of work started.

---

### A Plugin Can Supply Skin XML At Runtime — And That Makes Skin Testing A Loop (2026-08-22)

Build: VirtualDJ 2026 (`get_version` → `2026`), macOS arm64. Instrument:
`VDJIntrospectSkin.bundle`, the same source built with
`tools/plugin/build.sh --skin --install` (Sound Effect + `-DVDJINTROSPECT_SKIN`),
installed to `PluginsMacArm/SoundEffect/`. Context: no track loaded on any deck;
the effect selected on deck 1 and switched on; its panel opened with
`deck 1 effect_show_gui 'VDJIntrospectSkin'` over the
[HTTP interface](HTTP%20Control%20Interface.md). The plugin itself sends no
commands — every state change below came from HTTP or from the GUI by hand.

**`OnGetUserInterface` is called, and `VDJINTERFACE_SKIN` renders.** The first
call arrived the moment the effect's GUI was shown — never at load, never while
the effect was merely active. The plugin returned `S_OK` with
`Type = VDJINTERFACE_SKIN`, an XML buffer and a PNG buffer, and VirtualDJ drew
the panel. This is the first `Local test` evidence that the documented runtime
skin path in [Plugin SDK](Plugin%20SDK.md) §Plugin user interfaces is live.

Everything in the probe skin rendered on the first attempt:

| Element | Served | Rendered |
| --- | --- | --- |
| `<textzone><text format="PROBE REV 1"/>` | literal | `PROBE REV 1` |
| `format="deck=`get_deck`"` | backtick-interpolated VDJScript | `deck=1` |
| `<text action="get_effect_slider_text 1"/>` | query action | `50.0%` |
| `<button action="effect active">` with `<selected y="+200"/>` | sprite offset | drew from the `+200` band of the served PNG |
| `<Skin width="220" height="200">` | panel size | honoured |

So a plugin panel evaluates VDJScript exactly as a skin does — backticks in
`format=""`, `action=""` on a `<text>`, and sprite-sheet state offsets all work
against a PNG that exists only in memory.

**It is called again on every panel open, which is the whole point.** Call #2
arrived after `skin.xml` was edited on disk and the panel closed and re-opened;
the log recorded the new byte count and the panel showed the new content, with no
rebuild and no restart. Because the plugin re-reads both files inside
`OnGetUserInterface` rather than baking them into the bundle the way the SDK
example does, the edit→observe cycle is now:

```sh
just plugin-skin-prepare <some.xml>   # write skin.xml + skin.png
just plugin-skin-reload               # close + re-open the panel
just plugin-skin-log                  # confirm VirtualDJ asked again
```

That replaces a VirtualDJ restart per skin edit, which is what made the skin
questions expensive in the first place.

#### The surface is a FLAT element list — `<group>` renders nothing

Measured with a control row that must always appear, so "nothing rendered" is
distinguishable from "the panel never opened":

| Construct | Result |
| --- | --- |
| Top-level `<textzone>`, `<button>` | renders |
| `<group>` containing a `<textzone>` | **contents dropped**, no crash |
| `<group condition="...">` containing a `<textzone>` | contents dropped |
| `<define>` whose body is `<size>/<pos>/<text>` (property children) | renders |
| `<define>` whose body is a whole nested `<textzone>` | **contents dropped**, no crash |

A `<define>` body is spliced in as *property* children of the call-site element.
Give it a complete nested element and that element is silently discarded. The
same is true of `<group>`. Whether this is specific to the plugin-panel surface
or is also true of a full deck skin is **untested** — do not generalise it to
deck skins from this evidence.

#### Starred placeholders: the star is required, and it does work in conditions

This settles the open question at [Skin SDK](Skin%20SDK.md) §`<define>`, which
recorded the condition behaviour as "still unclear, should be tested per pattern".
Each canary rendered one define twice, once with a value that should pass its test
and once with a value that should fail, so a condition that is *ignored* (both
rows appear) is distinguishable from one that is *evaluated* (exactly one appears).

| Canary | Placeholder | Context | Result |
| --- | --- | --- | --- |
| `placeholder-text.xml` | `val=X` (unstarred) | `format="1 u-text [VAL]"` | **not substituted** — rendered the literal `[VAL]` |
| `placeholder-text.xml` | `*val=X` (starred) | `format="2 s-text [VAL]"` | substituted |
| `placeholder-text-attr.xml` | `val=X` (unstarred) | `text="1 u [VAL]"` | **not substituted** — literal `[VAL]` |
| `placeholder-text-attr.xml` | `*val=X` (starred) | `text="2 s [VAL]"` | substituted |
| `visibility-condition.xml` | none (literal control) | `visibility="param_equal 'yes' 'yes'"` / `'no' 'yes'` | true row shown, false row hidden — the condition really is evaluated |
| `visibility-condition.xml` | `*val` (starred) | `visibility="param_equal '[VAL]' 'yes'"` on the `<define>` tag | **substituted and evaluated** — `val="yes"` row shown, `val="no"` row hidden |

Two further things fell out of the same run: a starred placeholder substitutes
into a *numeric* attribute (`<pos y="[Y]">` placed each row at its own height),
and **element attributes written on the `<define>` tag are forwarded to the
instantiated element** — that is how `visibility` reached the `<textzone>`.

The narrow claim: **in a plugin-supplied runtime skin, a named placeholder must be
starred to substitute at all** — in `format=""`, in `text=""`, in a numeric
attribute, and in a `visibility=""` condition alike; and once substituted into a
condition, the resulting expression is genuinely evaluated rather than pasted.

This sharpens, and partly contradicts, the existing note that built-in skins "use
many unstarred placeholders in ordinary pass-through contexts, including
`text="[TEXT]"`". Unstarred `text="[TEXT]"` did **not** substitute here. The two
observations can both be true — this is a plugin panel, not a deck skin, and the
built-in usage is a `Built-in skin` reading rather than a rendering test — so the
existing note is kept and qualified rather than replaced. Settling it for deck
skins needs the same canary run as a real skin.

#### Hazard: `<group class="...">` crashes VirtualDJ

Two separate skins that instantiated a visual class onto a `<group>` element —
`<group class="s_cond" val="yes"/>`, the define body being
`<group condition="param_equal '[VAL]' 'yes'">` around a `<textzone>` — took
VirtualDJ down within about a second of the panel opening. Both times it
relaunched itself as `VirtualDJ recover`; both times the plugin had already
logged the `OnGetUserInterface` call, so the XML was served and the crash is on
VirtualDJ's side of the handoff.

The star is not the trigger: one crashing skin used `*val`, the other `val`. The
two components were then separated, and each is safe on its own — a plain
`<group>` renders nothing without crashing, and a `<define>` body containing a
nested element renders nothing without crashing. What is left is the combination:
**a visual class instantiated on a `<group>`**. Two occurrences, one build; the
mechanism is unknown.

Operational note: after a crash-recovery relaunch, VirtualDJ held the Network
Control listener open on port 80 without accepting connections — `netstat` showed
`LISTEN`, `connect()` timed out, and toggling the plugin off and on did not clear
it. A full quit and relaunch did. Budget for that when a skin under test kills the
app.

#### What this channel cannot answer

The panel is a plugin surface, not a deck. `<scratchwave>`, `<songpos>`,
`<rhythmzone>` and the rest of the waveform family have no deck to bind to here,
so the stacked-`<size condition="">` question at
[Skin Waveforms](Skin%20Waveforms.md) §Open Questions is **not reachable through
this instrument** and stays open. That is a bounded negative, not a failure: it
names the fixture the question actually needs, which is a real skin.

## Corpus Parse Regression, Full Corpus

VirtualDJ 2026 (bundle `18.0.9598`), macOS arm64, 2026-09-04, HTTP `/query`.
First run covering the whole corpus after the mapper source and the refreshed
vendor copies landed: **1,610 snippets, 1,206 parsed**
(`just corpus-parses`, `tests/corpus-parse-results.json`).

**No grammar claim was falsified.** That is the headline, and it needed the
controls to establish — the run reports 15 `structural` rows, and the artifact's
own rule is that each is only a candidate until a nonsense control separates it.
None does:

| Verb | Vendor form | Nonsense control | Reading |
| --- | --- | --- | --- |
| `sampler_bank` | `+1` → `E_INVALIDARG` | `zzqqx` → `no` | **Separates.** The step argument is recognized and refused on query while garbage is silently ignored — positive evidence for the documented execute-only rule, not against it |
| `pad_page` | `+1` → `E_INVALIDARG` | `zzqqx` → `no` | Separates, same reading |
| `pitch_range` | `'8,16,50' +1` → `E_INVALIDARG` | `zzqqx` → `E_INVALIDARG` | **Does not separate.** Bare answers `0.33`; every tail errors, real or invented, so the verdict says nothing about the form |
| `loop` | `50%` / `200%` | `zzqqx` → same error | Does not separate |
| `display_time` | `'elapsed,remain'` | `zzqqx` → same error | Does not separate |
| `sampler_loop`, `sampler_mode` | `+1` / `-1` | `zzqqx` → same error | Does not separate |

So the `structural` bucket currently mixes two unrelated things: verbs whose
relative argument really is distinguished from garbage, and verbs that reject
**every** argument on the query surface regardless of what it is. Neither is a
contradiction. `pitch_range '8,16,50' +1` is the one new row this run added, and
it lands in the second group — it is attested in Atomix's own DDJ-XP2 factory
mapping, so the form is vendor-shipped; the query surface simply cannot evaluate
`pitch_range` with any tail at all.

**Method note.** The classifier reaches `structural` only for verbs the existence
sweep calls `query` — a verb that answers bare, like `pitch_range` (`0.33`), skips
the `surface-gated` branch even when it refuses every argument. Argument-surface
gating and structural rejection are therefore not yet distinguished automatically,
and the controls above have to be run by hand.

## Skin Reader Vocabulary And The `clickthrough` Attribute

Build 18.0.9598 (arm64), deck-skin surface, 2026-09-05. Two channels: a static
read of the binary's skin readers, then a live deck-skin fixture over HTTP.

### Where the readers are

Extraction is `tools/extract_skin_readers.py` (`just skin-readers`), the
stripped-build ADRP+ADD xref method with the enumeration heuristics removed —
a skin reader is exactly the "dispatcher referencing far more strings than it
hits" that `extract_binary_vocabularies.py` deliberately discards. Each reader
is anchored by strings only it compares, and the window is the tightest stretch
of `__text` holding an xref to every anchor. Addresses are for **this build**;
they are not expected to survive a bump, which is why `--check` skips itself
when `CFBundleVersion` changes rather than failing.

| Reader | `__text` range | Anchors | What it reads |
| --- | --- | --- | --- |
| `skin_object_base` | `0x10037c54c`–`0x10037cebc` | `condition`, `canstretch`, `clickthrough`, `mousemask`, `mousecircle` | the attributes every skin object gets, `<panel>` and `<group>` included |
| `element_dispatch` | `0x10037dfd4`–`0x10037ebf8` | `multibutton`, `resizepanel`, `keyboardmap`, `pannel` | the element-name switch |
| `panel_builder` | `0x1007959a4`–`0x100795f40` | `forceshow`, `childtooltip`, `breakline1`, `grabzone` | panel/menu-item construction |

Query the vocabulary with `just skin-reader <name>` and the diff with
`just skin-candidates`; the summary field that answers "how many are in neither
the shipped corpus nor the SDK doc" is `summary.candidates`.

**Boundary of this pass.** Three readers, one window each, one call level: the
windows are string-reference extents, not disassembled control flow, so no call
target was followed, no branch coverage was measured, and a name a reader passes
to a helper is invisible here. `<panel>` and `<group>` share `skin_object_base` —
`group` has no builder of its own in this extraction, which is a finding about
where to look next rather than proof that none exists. Names are labelled by
address and reader, never by a guessed function name; the readers have no
symbols on a stripped build and none is claimed.

**A wall this pass did not hit but named.** Many attributes shipped skins use
heavily — `sourcecolor` (460 uses), `textaction` (678), `panelname`, `swapdeck`,
`firstvisible`, `textwidth`, `dblaction` — are **absent from the binary
entirely**, in any case. They are not reader vocabulary at all: they are
`class=""` template placeholders, substituted by the skin's own `<define>`
mechanism (the binary carries `[TEXTACTION]`, `[ACTION1]`, `[bordercolor]` and
friends as placeholder tokens). `lint_skins.py` already skips attribute checks
on elements with `class=""` for this reason. The consequence for this method:
absence from the binary is evidence a name is **not** reader vocabulary, and
says nothing about whether a skin may legitimately use it.

### The candidate taken live: `clickthrough`

`clickthrough` is compared once, in `skin_object_base`, against the value
`pass`. It appears in no shipped skin and no SDK doc. Fixture and full method:
[tests/Skins/clickthrough-probe/](../tests/Skins/clickthrough-probe/) — originally five
generated deck skins, identical apart from one attribute, two overlapping
buttons each writing its own global so the answer is read over HTTP rather than
judged from a screenshot.

| Variant | Attribute on the top button | `$ct_top` | `$ct_bottom` |
| --- | --- | --- | --- |
| `baseline` | *(none)* | 1 | 0 |
| `visible-off` | `visibility="param_equal 'no' 'yes'"` | 0 | 1 |
| **`pass`** | `clickthrough="pass"` | **1** | **1** |
| `value-control` | `clickthrough="qzqzqz"` | 1 | 0 |
| `attr-control` | `zzclickthrough="pass"` | 1 | 0 |

Two independent runs, variant order reversed in the second, identical results.

**Second pass (2026-09-07, same build, same surface, all seven variants):**

| Variant | `$ct_top` | `$ct_bottom` |
| --- | --- | --- |
| `baseline` | 1 | 0 |
| `visible-off` | 0 | 1 |
| **`pass`** | **1** | **1** |
| `value-control` | 1 | 0 |
| `attr-control` | 1 | 0 |
| **`yes`** | **0** | **1** |
| **`true`** (written `TRUE`) | **0** | **1** |

Forward then reversed, identical both times; the `yes` skin screenshotted with
the TOP button still drawn. Boolean true is a third state: the element renders
but is transparent to clicks and its own action does not fire, where `pass` is
additive and the stored `0` swallows. `TRUE` agreeing with `yes` confirms the
case-insensitive compare that the named `getBoolParam` disassembly predicted
(`tests/build-history-2026-09-06/*-bool-param.asm`).

**Third pass (2026-09-07, same build, same surface): containers and layers.**
The TOP button carries nothing and a wrapper carries the candidate; the layer
rows add a MIDDLE button with its own global. Forward then reversed, identical.

| Variant | Wrapper around TOP | Attribute on the wrapper | `$ct_top` | `$ct_bottom` |
| --- | --- | --- | --- | --- |
| `panel-none` | `<panel>` | *(none)* | 1 | 0 |
| `panel-pass` | `<panel>` | `clickthrough="pass"` | 1 | **1** |
| `panel-yes` | `<panel>` | `clickthrough="yes"` | **0** | **1** |
| `group-none` | `<group>` | *(none)* | 1 | 0 |
| **`group-pass`** | `<group>` | `clickthrough="pass"` | 1 | **0** |
| **`group-yes`** | `<group>` | `clickthrough="yes"` | **1** | **0** |
| `group-vis-none` | `<group visibility="…true">` | *(none)* | 1 | 0 |
| `group-vis-pass` | `<group visibility="…true">` | `clickthrough="pass"` | 1 | **1** |
| `group-vis-yes` | `<group visibility="…true">` | `clickthrough="yes"` | **0** | **1** |

| Variant | TOP | MIDDLE | `$ct_top` | `$ct_mid` | `$ct_bottom` |
| --- | --- | --- | --- | --- | --- |
| `3-top-pass` | `pass` | *(none)* | 1 | 1 | **0** |
| `3-both-pass` | `pass` | `pass` | 1 | 1 | **1** |
| `3-top-yes` | `yes` | *(none)* | 0 | 1 | 0 |

A `<panel>` and a `<group visibility="…">` honor `clickthrough` as a button
does; a plain `<group>` ignores it in both values — the live counterpart of the
historical `CSkinPanel::loadChildren` split, which tests the *presence* of
`visibility`/`novisibility` and takes a non-object path otherwise. `pass`
carries a click exactly one layer down; each layer decides for itself.
Recorded in Skin SDK under `clickthrough` and `<group>`.

**Reading.** `clickthrough="pass"` makes an element run its own action *and*
let the click continue to whatever is underneath — it is additive, not a
redirect. Both controls separate from it, so the attribute name and the value
each carry the behavior; a nonsense value behaves exactly like the attribute
being absent, which is the silent-ignore rule skin readers share with verbs.
`visible-off` is the calibration: it proves in the same fixture that the click
coordinate is over the bottom button and that attributes on the top button are
honored, so the negatives are negatives about `clickthrough` and not about aim.

**Unresolved next question.** Only `pass` was tested, because it is the only
value the reader compares in that window. The historical-installer excavation
(2026-09-07) later read the named boolean parser the loader falls back to: it
accepts only `yes`/`true`/`no`/`false`, so the one untested state was boolean
true; the `yes` and `TRUE` variants settled it on 2026-09-07 (second-pass table
above), and the third pass settled containers and layers. What it does on a container (`<panel>`/`<group>`) rather than a
`<button>`, and whether the pass-through reaches more than one layer down are
all open. The other 20 candidates are untested leads.

### Two facts the fixture setup established

- **A skin folder needs an image beside the XML.** With only `skin.xml` present,
  VirtualDJ refuses the skin with a modal *"Impossible to open skin `<name>`"*
  and keeps the current one — while `load_skin` still returns `true`. The
  identical XML loaded once `skin.png` and `preview.png` were added. This is a
  transport-result trap of the kind Evidence Standards warns about: the channel's
  own `true` said nothing, and the failure was only visible on screen.
- **The skin list is not cached.** A folder created while VirtualDJ is running
  loads immediately, verified by copying a known-good skin to a new name — so
  the refusal above was never a stale-index effect.

### `load_skin`, incidentally

Confirmed on the same run and recorded on the verb (`just get-verb load_skin`):

- **In query position it returns the current skin**, as `<Folder>/:<xml basename>`
  (`DeathDisco Grave Raver v1/:skin`) or a bare folder name for a skin whose
  identity has no variation part. That makes it its own restore oracle.
- **In execute position it switches skins by name**, and the argument must match
  the identity the query form returns: `load_skin 'DeathDisco Grave Raver v1'`
  did nothing, `load_skin 'DeathDisco Grave Raver v1/:skin'` switched.
- **The result is always `true`**, including for a skin that fails to open. Do
  not read it as success.

## Known-Position Fixture And `get_time` Discrimination

Build 18.0.9598, HTTP, 2026-09-06. Deck 1 loaded and **stopped** (no playback
drift, no audio), `display_time` left on the operator's `remain` setting.

### Why a new fixture was needed

The stored arg-form probe could not tell `get_time 'cue1'` from
`get_time 'a-word-it-has-never-seen'`. Both answer, and none of the ten existing
fixtures puts a cue, a loop start and a loop end at *different* positions — so
in every state available, the forms that were supposed to disagree returned the
same number. Separation was impossible by construction, not absent.

`known_positions` (`tools/fixtures.py`, `just fixtures`) is that state, and
`tools/probe_known_positions.py` (`just known-positions`) establishes it, proves
it, probes it and restores it. The positions are read by an oracle that is **not**
`get_time`:

| Position | Oracle |
| --- | --- |
| cue 1 | `cue_pos 1 mseconly` |
| loop start | `get_loop_in_time on` |
| loop end | `get_loop_out_time on` |
| playhead | `get_position` × `get_time 'total'` |

Nothing assumes the numbers it asked for. Quantize moves them —
`set_cue 1 15000ms` landed on **14496** on a 120 BPM fixture whose grid is offset
from zero — so the run reads all four back and **aborts rather than probe** if any
two coincide. Two independent runs, the fixture torn down and rebuilt between
them with different numbers, and the form order reversed in the second.

### Result

Two runs × two phases (before and after moving cue 1), all four agreeing.
Run 1, phase 1: cue 14496, loop in 18496, loop out 34496, playhead 11000,
total 90000, `display_time` = `remain`.

| Form | Value | Reads |
| --- | --- | --- |
| *(bare)* | 79000 | `remain` — follows the `display_time` setting |
| `elapsed` | 11000 | the playhead |
| `remain` | 79000 | |
| `total` | 90000 | |
| `absolute` | 79000 | **keeps the `display_time` mode** — a modifier, not a mode |
| **`cue1`** | **14496** | **cue 1, exactly** |
| `cue` | 0 | the *active* cue — nothing is active yet |
| **`loopin`** | **18496** | **the loop start, exactly** |
| **`loopout`** | **34496** | **the loop end, exactly** |
| `to_lyrics` | 0 | no lyrics in the fixture — unresolved |
| `short` | 11000 | behaves as an unrecognized tail |
| `qzqzqz` / `wvwvwv` | 11000 / 11000 | **CONTROL: both fall back to `elapsed`** |

**The controls are the point.** An unrecognized tail does not fall back to the
bare form — it falls back to `elapsed`, while bare returned `remain` throughout.
So "bare differs from my argument" was never evidence the argument was read, and
the three targets are confirmed by matching their *own* oracle exactly, in four
phases, and by tracking a position when it moves.

### The perturbation, and the one conditional rule

Moving cue 1 (14496 → 70496 in run 1, 24496 → 60496 in run 2) while the loop
endpoints were held: `cue1` tracked it exactly both times, `loopout` did not
move, and the nonsense controls tracked the playhead. That is what separates
"reads this position" from "happened to equal it once".

The move seeks outside the active loop, which **deactivates** the loop while
leaving both stored endpoints readable — and that exposed the one conditional
result:

- **`get_time 'loopin'` reads the loop start only while a loop is active.** With
  the loop exited it returns the loop-**out** value (34496 / 44496) while
  `get_loop_in_time on` still reports the in point (18496 / 28496). Reproduced in
  both runs. Recorded as `reads_its_position_only_while_a_loop_is_active`, not as
  instability: the rule is reproducible, and the two channels genuinely disagree
  in that state.
- `loopout` and `cue1` are unconditional — exact in all four phases.
- `cue` is not a synonym for `cue1`: it reads the **active** cue, which was `0`
  until the one-argument `set_cue 1` (which stores the playhead) made cue 1 the
  active one, after which it matched `cue1`. Consistent across both runs.

### Setup verbs established on the way

Recorded on the verbs (`just get-verb <name>`):

- **`loop N` lays an N-beat loop ENDING at the playhead** — the in point is N
  beats *before* the current position. Not stated in the catalog and easy to get
  backwards.
- **`loop_out` after `loop_in` did not produce the expected loop** on a stopped
  deck: it made a 4-beat loop unrelated to either the loop-in point or the
  playhead. Not chased — `loop N` was used instead — and recorded here as an
  open observation rather than a claim about `loop_out`.
- **`goto <signed number>` is beats**, relative to the playhead.
- **`set_cue 1 <ms>` and bare `set_cue 1` both work**, and the bare form also
  makes that cue the *active* cue.
- **`get_position` is a coarse oracle** — two decimals, so ±450 ms on a 90 s
  track. Fine for asserting distinctness, not for matching a position exactly.

### What was not resolved

`to_lyrics` returned `0` in every phase; the fixture has no lyrics, so the state
does not discriminate it, and that is a property of the fixture rather than of
the verb. `cue` was only ever seen reading cue 1; whether `cue2`, `cue3` … exist
as tails was not probed. Nothing here tested a *playing* deck, deliberately — a
stopped deck was chosen so no result could be drift.

## Video FX Over HTTP: What The Channel Can And Cannot Reach

Build 18.0.9598, HTTP, 2026-09-06. Task 1's remainder was framed as "rendering
behavior, needs video output". Most of it is — but three of the four questions
turned out to be answerable without rendering anything, and one of them found a
verb that does not do what its parameter says.

State was recorded and restored: video effect `Karaoke` with slider 1 at `1`,
inactive, cycle index `0.18`; all four values verified identical afterwards.

### `get_video_fx_slider_label` ignores its index

| Selected effect | Its slider labels | `get_video_fx_slider_label 0…99` |
| --- | --- | --- |
| `Karaoke` (1 slider) | `PRES` | `PRES` for every index |
| `Colorize` (5 sliders) | `COL` `STR` `SAT` `SPD` `BRI` | **`COL` for every index** |

The control is the name-addressed helper on the same effect:
`get_effect_slider_label 'Colorize' 1…5` returns all five labels and `''` for
index 6, so the labels exist and are reachable — this verb simply never reads
its argument. **Use `get_effect_slider_label '<effect>' <n>`**, which also needs
no selection. Recorded as `Fail` on the verb.

### `video_fx_slider` does index — in both positions

Not the same defect. Query `video_fx_slider n` returned Colorize's five values
(`0, 1, 1, 0, 0.5`), matching `effect_slider 'Colorize' n` exactly; execute
`video_fx_slider 3 0.25` moved slider 3 and nothing else, and setting it back to
`1` restored precisely that slider. So the label helper is broken on its own,
not as part of a broken family.

### Default scope is `master`, not the active deck

`video_fx_select` bare and `deck master video_fx_select` both read `0.18`, while
`deck 1 video_fx_select` reads `0`. The video FX chain hangs off the master
output, and an unscoped video verb addresses it.

### `video_fx` could not be activated over this channel

`video_fx on`, bare `video_fx`, `deck 1 video_fx on` and `deck master video_fx on`
all returned `false` and left the query at `no` — with no track loaded and again
with an audio-only track on deck 1. **A bounded negative, not a broken verb:**
selection and sliders work fine over HTTP, so activation is gated on video output
this channel cannot supply. That gate is exactly what still keeps the rendering
half of task 1 open.

`video_fx_clear` returned `true` and left the *selection* intact, but nothing was
active when it ran, so all that shows is that it does not deselect.

### The video `+1` cycle, walked

Stepping `video_fx_select +1` from Colorize traversed **17** effects and wrapped
cleanly on the 18th: Colorize, Blur Black Bars, Blur, Boom Auto, Boom, Slideshow,
Visuals, Camera, Cover, Text, Screen Grab, Lyrics, Karaoke, Strobe, Shake,
Spectral, Negative. That matches the FX catalog's `video_fx` category exactly and
contains **none** of the four category-unknown effects (`Lottery`, `Sweep`,
`Title`, `Vocals`) — so as currently enabled they are in no cycle. Whether
enabling one in the FX list editor puts it there is still a GUI question.

### Trap worth repeating

`video_fx_select 'Colorize'` returns **`false`** and selects Colorize. The body
is the verb's own result, never transport success — read the selection back with
`deck master get_effect_name 'video'`.

## Release FX: The Arming Path Does Not Exist In Script

Build 18.0.9598, HTTP, 2026-09-06. This closes the description half of task 3 and
**overturns its working diagnosis**. Nothing was left changed: the deck 1 slot
assignments (`Phaser`, ``, `Delay`, `Flanger`, `Echo Out`, `Echo Out`) were
identical before and after.

### The diagnosis that was wrong

The 2026-07-26 pass concluded the release sliders were "inert without an armed
release FX, which needs a momentary control HTTP can't drive". That is not the
obstacle. Two independent reasons:

1. **`effect_releaseslider_active` is documented to activate without one** —
   "Control the effect release specific slider *and auto activate the effect*" —
   and it does nothing. `effect_releaseslider_active 50%` returned `true` and left
   `is_releasefx` at `no`, its own query at `0`, and every numbered slot inactive,
   with deck 1 empty, loaded, and playing, scoped and unscoped.
2. **The pad surface would run the same script.**
   `tests/Pads/Reference - Release FX Test.xml` fires plain
   `effect_releaseslider 25%`, with no `down`/`up` wrapper, so a pad press is the
   same call this channel already makes.

### What is actually missing: there is no verb to arm the slot

The verb table — VirtualDJ's own list, where absence disproves a name — holds
exactly **three** release names:

| Verb | Kind |
| --- | --- |
| `effect_releaseslider` | drive a slider on the release slot |
| `effect_releaseslider_active` | the same, plus auto-activate |
| `is_releasefx` | query whether *this* effect is the release one |

There is **no selection verb**. Nothing named `effect_releasefx`,
`effect_release_select`, `releasefx` or any near spelling exists, and
`effect_select 'releasefx' 'Echo Out'` returned `false` and changed nothing
(scoped and unscoped, numbered slots untouched). So the three verbs *drive* a
slot armed somewhere else; VDJScript cannot arm it.

Where "somewhere else" is: the binary carries `Deck %i release effects` and
`Master release effects` beside `Deck %i color effects`, `Sampler color effects`,
`Deck %i merge effects` and `MIX FX` — the FX-list-editor category headings. And
`settings.xml` stores `<effects>` as **eight** comma-separated entries per deck
(six script slots plus two more, the eighth being `Echo Out` on all four decks)
with `<masterEffects>` holding nine. Positions past the six exist; script slot
numbers do not reach them — `get_effect_name 7` and `8` read empty and
`is_releasefx 0…10` is `no` throughout.

`releasefx` appears in script in exactly one vocabulary: the `effect_gui` group
(`effect_show_gui` / `effect_dock_gui`). `effect_show_gui 'releasefx'` returned
`true` with the query still `no` and nothing on screen; `effect_dock_gui
'releasefx'` returned `false`.

### `is_releasefx` never answered `yes`

Tried bare, deck-scoped, with slot arguments `0`–`10`, and with the names of
effects this instance really has configured — `Echo Out`, `Phaser`, `Delay`,
`Reverb`, `Cut`, `Backspin`. All `no`. The earlier negative was therefore not a
matter of naming the wrong effect; the slot is simply unarmed, and with no verb
to arm it this query cannot be made to answer `yes` from script.

Its catalog wording, "query if **this effect** is in the release effect slot",
reads as effect-scoped — the question an effect's own plugin GUI would ask about
itself. That is consistent with every reading here but is **not** established:
no surface was found where it answers `yes`.

### How to describe these separately from ordinary deck FX

- Ordinary deck FX: `effect_select <slot> '<name>'`, `effect_slider <slot> <n> <v>`,
  `effect_active <slot>` — all three addressable and all three verifiable by
  read-back.
- Release FX: **no selector**, and the two sliders write to a slot the script
  cannot create. Their `true` is the verb's own result and means nothing about
  whether an effect exists to receive it. Guard a skin or pad on
  `is_releasefx` before showing release controls, and expect it to read `no`
  unless a release effect was configured in the app's own FX lists.

### The one thing still unobserved

No armed release slot was ever seen, so no release-FX *behavior* has been
watched. That needs an operator to assign a release effect in VirtualDJ's FX
lists first; the harness for the moment after that already exists at
`tests/Pads/Reference - Release FX Test.xml`.

## Video FX Rendering: The Gate Was The Video Window

Build 18.0.9598, HTTP plus the video window, 2026-09-06. This supersedes the
bounded negative recorded earlier the same day and closes task 1's rendering
half. Everything was restored and verified: video effect back to `Karaoke` with
slider 1 at `1`, `Colorize` sliders back to `0,1,1,0,0.5`, transition back to
`Fade` with both sliders at `0`, crossfader `0`, window closed, both decks empty.

### The precondition

`video_fx` could not be activated over HTTP with no track, with an audio track,
or **even with a real video loaded** — every scope returned `false` and left the
query at `no`. The missing piece was not a video source and not a momentary
control: it was the **video window**. `video` (catalog: "Open/close video window")
opens it, and the identical `video_fx on` call then flipped the query to `yes`.

A paused deck is enough — the window renders the current frame — so none of this
needs playback or makes sound.

The execute result is `false` whether or not it works, so read `video_fx` back.

### Four rendering passes

Fixtures generated with ffmpeg into the fixture cache, never the user's library:
a 30 s `testsrc2` colour-bar pattern and a 30 s white clip.

| Verb | What was watched | Result |
| --- | --- | --- |
| `video_fx` | `Negative` on the colour-bar pattern | every colour inverted (red→cyan, green→magenta, yellow→blue) |
| `video_fx_slider` | `Colorize` slider 1 (COL/hue) `0.1` → `0.7` | rendered tint went amber → magenta |
| `video_fx_clear` | `Colorize` actively tinting | render returned to the unprocessed source |
| `video_transition_slider` | `Blinds` slider 2 (NB) `0.15` → `0.95`, crossfader at `0.5` | ~5 thick blinds → ~15 thin ones |

**`video_fx_clear` deactivates only.** After it, `video_fx` read `no` while the
selection stayed `Colorize` and slider 1 kept its `0.7` value — so it is neither
a deselect nor a slider reset. That is the question the earlier pass could not
answer, having only ever run it with nothing active.

The transition test needed two *different* videos, so the crossfade would be
visible at all: the same file on both decks renders identically at any
crossfader position and would have proved nothing.

### One loose observation, not a claim

`video_crossfader 0%` did not stick while both decks held videos — the query
kept reading `0.52` — and the same call set it to `0` immediately once the decks
were empty. `video_crossfader_auto` ("automatically move video crossfader based
on deck activity") is the obvious suspect and was not tested. Noted so the next
person restoring this state checks the read-back rather than assuming.

### Still open

Whether enabling one of the four category-unknown effects (`Lottery`, `Sweep`,
`Title`, `Vocals`) in the FX list editor puts it into a `+1` cycle. That is a
settings-UI action with no verb, and it is the last piece of task 1.

## Editor-Hidden Verbs: Behavior, Not Existence

Build 18.0.9598, HTTP, 2026-09-06. Task 6's framing was right — all 38 names with
`flags == 256` are already proven real by verb-table membership, so this pass was
about what they *do*. Every one is now recorded as Pass, Partial, Fail or
explicitly blocked; none is left as active untested work. State restored: pad page
back to `1 CUE`, deck volume back to `1`, both decks empty.

Two names were never executed, deliberately: **`crash`**, which is named exactly
what it does and is now marked blocked, and `browser_colorfilter_edit`, which
opens a modal dialog nothing here needed.

### The Flip family — the whole feature, characterised

Six verbs, and the catalog documents five of them despite the editor hiding them.
Driven end to end on a disposable generated fixture track with the deck volume at
zero, so nothing was audible:

| Verb | Behavior |
| --- | --- |
| `flip_record` | Toggle. First press → `flip_get_status` reads `Rec Standby`; **recording begins on the first cue press**, after which the status counts up. Second press stops it. |
| `flip_get_status` | **Text query, and the display string a skin wants**: `''` idle, `Rec Standby`, `Rec MM:SS`, `Play MM:SS`. Not in the catalog at all. |
| `flip_load` | Reports whether a flip exists for the loaded track — read `no` on a fresh track and flipped to `yes` the instant recording stopped. |
| `flip_play` | Jumps to the flip start and plays it; query `yes` during playback. Pausing the deck does **not** clear it; unloading does. |
| `flip_loop` | Toggle, query `no` → `yes`. Whether it actually repeats at the flip end was not watched. |
| `flip_arm` | Toggle, query `no` → `yes`. The catalog's auto-start-on-reaching-the-flip claim was not watched. |

The observed sequence — `Rec Standby` → `Rec 00:02` → `Rec 00:15` → stop →
`flip_load` yes → `Play 00:02` → `Play 00:04` — matches the catalog text exactly,
so these are the vendor's own semantics confirmed, not inference.

### `effect_beats_sliderindex` — verified against an independent oracle

Takes an effect **name** and returns the 1-based index of that effect's
beats/length slider. Checked against the FX catalog, which was built by a separate
sweep, on effects with three distinct answers:

| Effect | Length slider in the catalog | Verb returns |
| --- | --- | --- |
| `BrakeStart` | S1 | **1** |
| `Backspin`, `Echo`, `VinylBrake` | S2 | **2** |
| `Beat Brake`, `Reverb` | none | **0** |
| `qzqzqz` (control) | — | **0** |

So it is genuinely per-effect and not a constant `2`. The one limit: `0` conflates
"no beats slider" with "unknown effect", so it cannot be used to probe existence.

### The pad-page trio, and a trap in it

- **`get_pad_page_name <n>`** — a 1-based index into the ordered page list, returning
  `1 CUE`, `2 SYNC`, `3 FX`, `3-FX`, `4 PHRASE` … in the same order as
  `settings.xml`'s `padsPagesOrder`. Index only: bare and a page *name* both error.
- **`pad_page_favorite <n>`** — yes/no, but only for **1–4**; index 5 and up return
  `E_INVALIDARG` on an instance with dozens of pages. So it addresses a four-slot
  favourites bank, not a per-page flag.
- **`pad_page_insplit '<name>'`** — takes a page **name**, not an index (numeric
  arguments all answer `no`), and it discriminates properly: `'1 CUE'` answered
  `yes` while every other real page name and two nonsense controls answered `no`.
  **But it tracks the current page.** Switching to `2 SYNC` moved the `yes` with it
  and switching back moved it back. With no split layout configured, "is part of a
  split" and "is the current page" cannot be separated, so the catalog's split
  meaning stays unconfirmed — do not build a split indicator on it yet.
- `pad_page_split` returns `''` bare and `no` with any argument, real or nonsense.
  Two return shapes, nothing established.

### `all_decks` and `combine_query` are not query-position verbs

Both return `error:-2147467259` bare and deck-scoped, while every other
editor-hidden verb in the same sweep answered something. That is the
not-implemented code, consistent with script-structural prefixes that only parse
in execute position — which was not tested. `browser_colorfilter_edit` gives a
*different* code, `error:-2147467263`, matching its action-only kind.

### Return shapes only

`is_colorfx` `no`, `masterbpm` `120` (the app default with nothing loaded, so it
does not separate "reads the master BPM" from "reads a constant"),
`pad_pressure_switch` `yes`, `sampler_inputgain` `1`, `send_nothing` `''`,
`shoutout` `no`, `stem_volume` `0`, `timecode_no_jump` `no`,
`load_security_shown` `no`. `hot_cue_stutter` and `setting_if_unchanged` both
require an argument (`E_INVALIDARG` bare). Each is recorded Partial with the state
that would move it named, rather than as a behavior claim.

### Ten hardware-gated names — but two different gates

Corrected the same day: "hardware-gated" was too flat a label, and the two tiers
have very different prospects.

**Needs an attached controller** — `controllerscreen_action` (one with a screen)
and `assign_related_controller`. This is the *weaker* gate: the operator owns
controllers, and a DDJ-GRV6 drove the task 5 mapper work, so these become testable
whenever one is plugged in. Nothing was attached during this pass —
`get_controller_name` returned `''`, which is the presence oracle to check first.

**Needs specific vendor hardware that is not here and cannot be substituted** —
the five `rane_*` names (Rane hardware), `ns7_get_drift` (a Numark NS7), and
`motorwheel2` / `motorwheel3` (motorised platters). These stay out of reach.

Query position separates none of this: `controllerscreen_action` and
`assign_related_controller` both return `error:-2147467263`, the action-only code,
which says nothing about whether hardware is present. Verb-table membership already
proves every one of these names; blocked is a statement about reachability, not
about existence.

## Verb Index Inversion: What The Prose And The Artifacts Disagreed About

2026-09-06, offline. `tools/extract_verb_index.py` now builds
`docs/vdjscript-verb-index.json` from `tests/verb-table.json` +
`docs/vdjscript-verbs.json` + the coverage audit, instead of parsing
`docs/VDJScript Verbs.md`. The output schema is unchanged and both consumers —
`lint_mappers.py` and `verbdb.py bootstrap` — keep working. The reconciliation
below is the point of the task; the rewrite is not.

### The defect was live, and it is reproducible

`lint_mappers.py` reads the index. Before the inversion, a mapper containing
verbs this repo has *locally tested* was linted like this:

```
WARN  <map value='F13'> unknown verb 'flip_record' (closest known: 'record')
WARN  <map value='F14'> unknown verb 'flip_play' (closest known: 'blink_play')
WARN  <map value='F15'> unknown verb 'get_pad_page_name' (closest known: 'get_sample_name')
```

All three are real — verb-table membership proves it and the editor-hidden pass
characterised all three the day before. Every one of the 37 editor-hidden names
was missing from the index, because the prose never listed them. After the
inversion the same file lints with **0 verb warnings**.

### The whole diff was 36 entries, and it split exactly as predicted

959 of the 995 shared entries differed only by an empty `"aliases": []` the old
generator emitted. Of the 36 real differences:

**Artifacts correcting the prose — 30 alias facts.** The verb table decides
aliases structurally (records sharing an `id`; `flags & 1` marks the alias
spelling), and it knows 17 pairs the prose did not:

| Canonical | Alias the prose missed |
| --- | --- |
| `browser_zoom` | `browser` |
| `eq_high` / `eq_low` / `eq_mid` | `eq_high_slider` / `eq_low_slider` / `eq_mid_slider`, `eq_med` |
| `eq_kill_mid` | `eq_kill_med` |
| `get_hasheadphones` | `get_hasheadphone` |
| `goto_beat_in_bar` | `goto_bar` |
| `jogwheel` | `jog_wheel` |
| `pitch` | `pitch_slider`, `pitch2_slider` |
| `prelisten` | `preview` |
| `scratchbank_unload` | `sampler_unload_from_deck` |
| `touchwheel` | `scratch_wheel` |
| `touchwheel_touch` | `scratch_wheel_touch`, `scratchwheel_touch`, `speedwheel_touch` |

And **three claims the table contradicts outright**, both cases of the prose
naming the wrong canonical:

- The prose made `pitch2` canonical for `pitch2_slider`. All four of `pitch`,
  `pitch2`, `pitch_slider`, `pitch2_slider` share **id 722**, and `pitch` is the
  member without the alias flag — `pitch2` is itself an alias.
- The prose made `scratch_wheel_touch` canonical for `scratchwheel_touch` and
  `speedwheel_touch`. All four share **id 153** under `touchwheel_touch`.

No index name was contradicted on *existence*: every one of the 995 prose names
is in the verb table. The prose never invented a verb — it only mis-ranked
aliases and omitted the hidden set.

**Curated facts with no artifact home — 2, and they were repaired rather than
dropped.** `auto_bpm_transition` and `auto_bpm_transition_options` carried richer
prose than the store ("an optional parameter forces which BPM it lands on",
`auto_bpm_transition_options 'stems' 'vocal'`), so the store was updated to hold
them before switching. Every other alias row that lost a description had only
`Official alias of X` boilerplate, which the row's `canonical` field now states
structurally.

### The schema gap the inversion exposed

Six names the store carries are absent from the verb table, and the table is
*silent* on them rather than negative: `ONINIT`, `while_pressed` and `deck` are
mapper/skin structural keywords rather than verbs, and `browser_filter`,
`browser_search` and `none` are names this repo disproved. Both groups need to
stay addressable and neither is a verb, so index rows now carry
`not_in_verb_table: true` rather than being silently promoted or dropped. A
proper `kind` for "structural keyword, not a verb" is the store field this
exposes; it is not added yet.

### Also fixed

`lint_mappers.py` raised `ValueError` on any path outside the repo — `relative_to`
throws — so asking it to lint a scratch file produced a traceback instead of a
lint. It reports the absolute path now.

## Shared Enumerations: The Colour Table Confirmed, The Pad-Page Table Unreachable

Build 18.0.9598, HTTP, 2026-09-06. Task 13 probes the enumerations
`binary-vocabularies.json` recovered as *structures*. Two groups were taken far
enough to conclude something; the conclusions are opposite, and the second is the
more instructive.

### `colors` — the table is the vocabulary, and it is readable without touching anything

`color '<name>'` in **query position resolves a name**: it echoes the canonical
spelling for a recognized colour and returns `transparent` for everything else.
That makes the whole 26-member group classifiable read-only, with a free floor.

**24 of 26 echo themselves** — `beige`, `black`, `blue`, `cyan`, `darkblue`,
`darkcyan`, `darkgray`, `darkgreen`, `darkmagenta`, `darkorange`, `darkred`,
`darkyellow`, `gray`, `green`, `lightgray`, `magenta`, `marine`, `orange`,
`pink`, `red`, `transparent`, `violet`, `white`, `yellow`. Sixteen of those were
in the group's `novel` list: named by the binary table and by no per-verb source.

Controls: `qzqzqz`, `wvwvwv`, `zzz123` and the two-word `bright red` all returned
`transparent`. `RED` returned `red`, so matching is case-insensitive.

**`none` and `reset` are undiscriminated, not disproved.** They also return
`transparent` — but `transparent` is itself a real member, so this observable
cannot separate "recognized, means transparent" from "unrecognized, fell to the
floor". They stay unconfirmed.

**Group-level conclusion:** for `color`, the serialised table *is* the accepted
vocabulary. Nothing outside it resolved, and everything inside it resolved except
the two whose meaning collides with the floor.

### `pad_pages` — the verb accepts anything, so the table cannot be probed through it

The opposite outcome, and worth recording precisely so nobody retries it.

Executing `pad_page 'sampler'` and `pad_page 'cueloop'` both returned `true` and
the query then reported that name as the current page — which looks like
confirmation until the control is run. **`pad_page 'qzqzqz'` behaved identically**:
`true`, and the current page became `qzqzqz`. The verb accepts an arbitrary
string and reports it back.

So the binary's 17 pad-page names are **undiscriminated through this verb**, not
unconfirmed by it — a distinction the probe rules exist for. Confirming them needs
an observable that reflects what the page actually *contains*, not what it is
called. (Restored to `1 CUE` afterwards.)

In query position with an argument, `pad_page` is an is-current predicate:
`'1 CUE'` → `yes`, every other name → `no`, real or invented. That is also why the
first read looked like a clean negative for the whole table: nothing was current.

### Colour siblings do not share the resolver

Checked while the colour vocabulary was in hand, because it is tempting to assume
one colour vocabulary across the family:

| Verb | Query-position behavior |
| --- | --- |
| `color` | resolves: canonical name, or `transparent` |
| `browsed_file_color` | **echoes ANY argument verbatim**, `qzqzqz` included — resolves nothing |
| `sampler_color` | bare returns a **hex** value (`#4D94F6`), not a name |
| `get_browsed_color` | bare/`red`/`blue` error, `marine` echoes, `qzqzqz` → `transparent`; identical across three runs, so stable but context-dependent and not interpretable here |
| `cue_color`, `loop_color`, `pad_color` | error in every form with no cue/loop/pad context prepared |

`browsed_file_color` is the trap: it looks like a resolver and confirms nothing,
because a nonsense token comes straight back.

## Contextual Parameters: Three Verbs Off The Worklist, One Wall

Build 18.0.9598, HTTP, 2026-09-06. Task 13b's method — build the state a
documented parameter needs, then re-probe — applied to three verbs from the
repaired cross-check worklist. Deck 1 was restored and the restoration verified;
deck 2 held one of the operator's own tracks throughout and was never touched.

### `get_sample_info` — the shape was the obstacle, not the state

All three documented fields confirmed, both nonsense controls returning `''`:

| Form | Value |
| --- | --- |
| `get_sample_info 1 'group'` | `Drums` |
| `get_sample_info 1 'length'` | `4bt` — a beat value for a loop, exactly as documented |
| `get_sample_info 1 'pos'` | `00:00.0` |
| `get_sample_info 1 'fullpath'` | the `.vdjsample` path |
| `get_sample_info 1 'bpm'` | `135.0` |
| `get_sample_info 1 'qzqzqz'` / `'wvwvwv'` | *(empty)* |

**The shape is slot-first** — `get_sample_info <slot> <field>` — and that is the
whole reason this sat unconfirmed. A single-argument probe errors on every token,
real ones included, so the sweep read the documented fields as indistinguishable
from nonsense. No new fixture was needed at all; the state had been there since
the `sampler_slots_differ` fixture landed. This is the failure mode task 12
predicted when it measured 114 verbs whose vendor examples are value-shaped.

`'name'` returns `''` here — `get_sample_name` is the verb for that.

### `get_saved_loop` — two confirmed, one undiscriminated, one out of context

Fixture built and torn down: a 32-beat loop laid on a disposable track with
`loop_save`, then `loop_delete 1`, with the deletion verified (`error:1`
afterwards).

- **`length` → `32bt`**, matching the loop actually saved, and **`name` →
  `Saved Loop 1`**. Both separate from two agreeing nonsense controls.
- The index is optional: `get_saved_loop 'name'` and `get_saved_loop 1 'name'`
  agree.
- **`pos` is undiscriminated.** It returns `18.5`, which does match the saved
  loop-in at 18496 ms — but bare and both nonsense tokens return `18.5` too, so
  `pos` is the default and this observable cannot separate it from the floor.
- **`next` is out of context, not refuted.** `error:1` in every form; with one
  saved loop behind the playhead there is no upcoming loop to report.

### `get_slip_time` — a wall, and the bare form is why

`error:-2147467259` (E_FAIL) in **every** form — bare, `'min'`, `'sec'`, `'msec'`
and two nonsense controls — with no track, and again with a track loaded,
`slip_mode` confirmed `yes`, the deck playing, and the playhead jumped so a slip
divergence should exist.

Because the **bare** form errors too, no token can separate from anything: the
three documented units are untested, not refuted. Either it needs a live slip
divergence this channel cannot create, or it is a controller-display helper.
Recorded `Fail` for reachability over HTTP, which is not the same as the verb
being broken.

### What this says about the worklist

Two of the three were not waiting on a *fixture* at all — one was waiting on the
right argument **shape**, and one only needed a loop saved. The remaining
`documented_but_not_probe_confirmed` count is what
`just action-catalog --cross-check` reports; it is worth re-checking each entry's
documented *example* for its shape before assuming a state is missing.

## Argument Positions: A Question The Other Probers Cannot Ask

Build 18.0.9598, HTTP, query-only, 2026-09-06. Task 12's named next feature,
motivated by the `get_sample_info` result the same day: every existing prober
asks "is this token recognized", one token at a time, and is blind to a verb
whose keyword lives in the second position. `get_sample_info <slot> <field>`
errors on every single-token probe — real fields included — so all three of its
documented fields were filed as indistinguishable from nonsense when they were
simply being asked in the wrong shape.

**Method** (`tools/probe_arg_positions.py`, `just probe-arg-positions`): hold a
verb's attested shape, vary ONE position between two values *of its own class*,
and see whether the returned value moves. Varying within the class is the point
— a difference then means the position was read, not that the verb rejected a
type it never accepts. Nonsense is still sent, but only to separate "reads it"
from "ignores everything here". Keyword positions are varied only with keywords
the verb is actually attested to take; inventing two words would test the floor
and nothing else. The baseline is re-read last, so a verb whose own value drifts
is reported `unstable` rather than scored as reading every position.

**Result: 37 verbs probed, 0 unstable, 8 read at least one position, and 4 read
one beyond the first** — the class of fact no artifact here carried.

| Verb | Shape | Finding |
| --- | --- | --- |
| `get_effect_slider_label` | `NUM NUM` | both read — slot, and slider index (`STR` → `SPD`, real Colorize labels). Independently confirmed earlier the same day, so it doubles as the method's calibration |
| `effect_slider_active` | `NUM NUM` | both read: slot 1 → `0.73` vs slot 2 → `0`, index 1 → `0.73` vs index 2 → `0.99` |
| **`effect_arm_slider`** | `NUM NUM` | **position 1 IGNORED**, position 2 read. Slot 1 and slot 2 both return `0.73`, as does nonsense there; only the slider index moves the value |
| `get_next_karaoke_song` | `STR NUM` | both read. `'artist' 1` → `Deadmau5`; `'singer'` → `''`; index `2` → error, while a *nonsense* index returned a different song title, so position 2 selects the upcoming song and falls back to a default rather than erroring on garbage |

`effect_arm_slider` against `effect_slider_active` is the pair worth keeping:
identical shapes, and one of them is not slot-scoped. Nothing short of varying
the slot position on its own would have shown that.

**Two limits, stated so the verdicts are not over-read.** `reads` means the
returned value moved when that position changed — it does not prove the verb
interprets the argument the way the docs say. And `ignored` is a statement about
*this state*: a position that changes nothing with the current decks and effects
may well be read in another.

## Source Modules, Joined At Read Time

2026-09-06. The module extraction itself landed separately (`tests/action-modules-9246.json`,
`tools/extract_action_modules.py`), including the grading pass that backfilled
`section` only where a module's already-sectioned members agree — 31 verbs of the
233 that had none, leaving 124 deliberately unsectioned rather than guessed.

Those 124 are exactly why the module is worth reaching from the query layer, so
it is now joined at read time the way the verb table and contracts already are:

- **`just get-verb <name>`** gains a `module` block with the module name, the
  build it was read from, and the module's section grade where it has one.
- **`just list-verbs --module=<name>`** filters on it. The case that shows the
  value: `--module=action_macro` returns `macro_play`, `macro_record` and the
  whole `flip_*` family together. Their store `section` is `Hidden Button
  Editor`, which is a *flag* rather than a topic and appears across a dozen
  modules, so section search could never have grouped them.
- **`just topic <term>`** consults it as a derived signal — no tag needed, since
  Atomix's own module names are already topical.

Nothing is copied into the store by this change; the artifact stays
authoritative and a re-extraction is picked up without a migration.

## Old Appendix Keywords Re-Probed

2026-09-07, HTTP, build 18.0.9598. The historical vendor-text diff
(`tests/build-history-2026-09-06/vendor-text-diff.json` →
`documented_parameters_lost`) lists keywords the 2019 and 2023 appendices quoted
and the current one does not. The one usable in query position was taken live.
State: deck 1 empty before and after; a library track carrying saved loops
(`Lick It [Mix] … Valentino Khan`, 146,150 ms) loaded onto it for the probe and
unloaded afterwards. Two nonsense controls, `qzqzqz` and `zzqqx`.

| Query | Result |
| --- | --- |
| `get_saved_loop 1 'name'` | `INTRO` |
| `get_saved_loop 1 'pos'` | `0.04` |
| `get_saved_loop 1 'length'` | `8bt` |
| **`get_saved_loop 1 'len'`** | **`3.81`** |
| `get_saved_loop 1 'qzqzqz'`, `'zzqqx'`, bare `get_saved_loop 1` | `0.04` |
| `get_saved_loop 'next' 'length'` / `'len'` / `'qzqzqz'` | `8bt` / `3.81` / `0.04` |
| `get_saved_loop 'length'` / `'len'` / `'qzqzqz'` | `8bt` / `3.81` / `error:1` |
| `get_saved_loop 2 …` (any tail) | `error:1` |

**Reading.** `len` and `length` both separate from the controls and from each
other, so `len` is a recognized form in its own right, not a retired spelling of
`length`: it answers in seconds (3.81 s at 126 BPM is 8 beats), `length` in
beats. An unrecognized tail falls back to the position, and with no index the
verb reads the next saved loop, where an unrecognized tail is an error rather
than a fallback. Index `2` erroring on a track the database shows with several
loops was not chased; the index may be a slot number rather than an ordinal.

**Total-time family, same track.** `get_totaltime_min` = `get_time_min 'total'`
= `2`, consistent with the equivalence the 2019 appendix stated and the current
one dropped (one sample; both read the same, so it is consistent, not proven).
`get_totaltime_ms` = `get_time_ms 'total'` = `15` while `get_time 'total'` =
`146150`: the `_ms` verbs return the hundredths digits of the displayed time
(`2:26.15`), which is what the current appendix's "1/100th seconds" means and
what the 2019 "milliseconds" text got wrong. A nonsense tail on
`get_totaltime_min` was ignored.

## Documented Parameters Taken Live 2026-09-07

HTTP, build 18.0.9598. Entries from `just action-catalog --cross-check` →
`documented_but_not_probe_confirmed` that a query and a loaded library track
can settle. Deck 1 empty before and after; the same saved-loop track as the
section above loaded for the probe; pitch read, moved `+1%`, and set back;
`get_pitch` read `0` on reload and after unload. Two nonsense controls
(`qzqzqz`, `zzqqx`) beside every candidate.

| Verb | Confirmed | Undiscriminated (not refuted) | Note |
| --- | --- | --- | --- |
| `get_loaded_song` | `album`, `title`, `artist`, `playcount` | | nonsense field → `error:-2147024809`; bare → empty; `playcount` → empty on a never-played track |
| `get_key` | `harmonic` (`08A`) | `musical` | bare, `musical` and both controls all `Am` because keyDisplay was already musical |
| `get_saved_loop` | `next` | `pos` | `'next' 'length'` → `8bt`; a nonsense selector → `error:1`; `pos` is what an unrecognized tail falls back to, so it cannot separate |
| `get_pitch_zero` | `absolute` | | at pitch +4.17% in a ±33% range: `'absolute' 5%` → `yes`; bare `5%`, `20%`, `'absolute' 0.1%`, `'qzqzqz' 5%` → `no` |
| `get_date` | format string | | `'%Y'` → `2026`, `'%A'` → `Monday`; a tail without a `%` directive is echoed, so the catalog's `format` is a placeholder |
| `get_limiter` | | `master`, `booth`, `headphones` | everything `0` with nothing playing |
| `get_time_sign` | | `elapsed`, `remain`, `total` | `1` at 43 ms and at 14,812 ms, every tail and both controls; a negative sign needs a state not built here |
| `get_time_hour` | | `elapsed`, `remain` | `0` throughout on a 2:26 track |

**Setup trap.** After the track loaded, `get_pitch` read `3.17` although the
slider had been `0`; `pitch +1%` moved it to `4.17`, and `pitch 3.17` (no unit)
put it at `33`. Reloading the track later read `0`, so the transient value was
not the slider. When restoring pitch, write the unit (`pitch 3.17%`) or use
`pitch_reset`, and verify with a reload rather than trusting the readback on an
empty deck.

**Side observation, not chased.** The database stores this track's key as
`Abm` and `get_key` returned `Am` while the deck read a non-zero pitch; the
display may fold pitch into the key.

## Documented Parameters Taken Live 2026-09-07 (second batch)

Same method and same track as the section above; browser selection left as
found (a different track, rating 0); sampler and automix state as found.

| Verb | Confirmed | Placeholder (doc's own words) | Undiscriminated (not refuted) | Note |
| --- | --- | --- | --- | --- |
| `get_browsed_song` | `title`, `playcount`, `artist` | | | nonsense field → `error:-2147024809`; bare → empty |
| `browsed_song` | `rating` | | | in query position it is an equality predicate: `'rating' 0` → `yes`, `'rating' 9` → `no`, nonsense field with `0` → `no`; the catalog only documents the setter |
| `sampler_loop` | `current` | | `play` | `current` → `yes` like bare; `play` alone → `error:-2147024809` like nonsense — it is the fourth token of the documented 4-token action form, not a query tail, so it stays untested rather than refuted |
| `get_time` | `to_lyrics` | | | `0` with no lyrics where nonsense fell back to elapsed (`44`) |
| `get_version` | | `2026` | | bare, `'2026'` and nonsense all `2026`; the prose quotes an example result |
| `get_text` | | `title`, `on`, `off` | | the verb echoes its argument; each quoted word echoed exactly as nonsense did |
| `get_artist_before_feat` | | `featuring` | | "with 'featuring' stripped" is prose; all three forms returned the artist |
| `get_song_event` | | | `current`, `next` | `error:-2147467259` (E_FAIL) on every form on a loaded, stopped deck; the earlier direct-query confirmation used a state this run did not build |
| `get_automix_song` | | | `title` | E_FAIL on every form with the automix list as found |
| `get_slip_time` | | | `sec`, `min`, `msec` | E_FAIL on every form with slip off |
| `filter_label` | | | `name` | `DELAY` on every form |
| `effects_used` | | | `deck` | `no` on every form with no effect active |

Recorded in `LOCAL_CONFIRMED` / `LOCAL_PLACEHOLDERS` in
[tools/extract_action_catalog.py](../tools/extract_action_catalog.py) and on the
verbs. Deck 1 empty before and after.

## Documented Parameters Taken Live 2026-09-07 (fixtures)

HTTP, build 18.0.9598, the `fx_slot_1_on` and `deck2_playing` fixtures from
[tools/fixtures.py](../tools/fixtures.py), two nonsense controls per candidate.
Deck 1 empty before and after; deck 2's own track restored, stopped.

**`fx_slot_1_on` (Phaser in slot 1).**

| Query | Result |
| --- | --- |
| `effect_active 'Phaser'` / `'flanger'` / `'qzqzqz'` / bare | `yes` / `no` / `no` / `yes` |
| `effect_select 1 'Phaser'` / `'echo'` / `'qzqzqz'` | `yes` / `no` / `no` |
| `effect_select 'Phaser'` / `'qzqzqz'` | `yes` / `no` |
| `effect_select_multi 'Phaser'` / `'qzqzqz'` | `yes` / `no` |
| `effects_used` bare / `'deck'` / nonsense | all `yes`; `get_effects_used` all `1` |
| `effect_colorfx` any tail, `effect_list` any tail | `error:-2147024809` (no ColorFX selected; `get_colorfx_name` was E_FAIL) |
| `filter_label` any tail | `DELAY` |

**Reading.** The effect-name argument is confirmed in query position for
`effect_active`, `effect_select` (with and without a slot) and
`effect_select_multi`: the loaded name answers `yes`, another catalog name and
nonsense answer `no`. The catalog's `flanger` and `echo` are example members of
the FX catalog, not keywords, and are recorded as placeholders. `effects_used
'deck'` is undiscriminated: every tail answered the same in both fixtures.

**`deck2_playing` (deck 2 playing the fixture track).**

| Query | Result |
| --- | --- |
| `get_song_event 'current' 'volume'` / `'next' 'volume'` | `1` / `0.74` |
| `get_song_event 'current' 'hasbeats'` / `'next' 'hasbeats'` | `yes` / `no` |
| `get_song_event 'current' 'remaining'` / `'next' 'remaining'` | `154` / `158` |
| `get_song_event 'qzqzqz' 'volume'`, `'current' 'qzqzqz'` | empty |
| `get_song_event 'volume'` (no selector) | `1` — selector defaults to `current` |
| `get_song_event` bare, and every form on a stopped deck | `error:-2147467259` |
| `get_level` bare / `vocal` / `sampler` / `mic` / `db` / nonsense, two reads | all `0` |
| `get_vu_meter` bare / `vocal` / `mic` / `sampler` / nonsense | all `0` |
| `get_limiter` bare / `master` / `booth` / `headphones` / nonsense | all `0` |
| `get_time_sign` any tail | `1` |

**Reading.** `current`/`next` and the fields `volume`, `hasbeats`, `remaining`
are confirmed, and both nonsense positions separate (empty). The verb needs a
*playing* deck: every form on the loaded-but-stopped deck in the earlier batch
was E_FAIL. The level and VU meters read `0` on a playing deck in this setup,
so their tails stay undiscriminated — the fixture track plays but the metered
path shows nothing here, which is a setup question (output routing, deck
volume) before it is a verb question.

**Fixture trap.** `--establish X --teardown` establishes and *then* tears down
in one run; running it after a separate `--establish X` restores the state the
second establish saw, which left deck 1 holding the fixture track. Use
`--establish X --hold N --teardown` in one process and query during the hold.

## Skin Reader Candidates Taken Live 2026-09-07

The clickthrough series carried the first name out of the binary skin-reader
extraction to a live test; this run carried the rest — the `just skin-candidates`
list and the eight element names `element_dispatch` accepts that appear in no
skin and no doc. Build 18.0.9598, deck-skin surface, fixture
[tests/Skins/reader-candidates-probe/](../tests/Skins/reader-candidates-probe/),
every series run forward and reversed with identical rows both times. The
per-candidate outcomes and their tables live in the fixture README and in
[Skin SDK.md](Skin%20SDK.md); what belongs here is the run.

**The discriminator needed a second form before it could read anything.**
Standing a candidate tag alone over a button separates a click-taking element
from a dropped one, but not from a *container*: an empty `<pannel>` — a tag the
switch is known to accept — lets the click through exactly as an unknown tag
does. Wrapping the button in the candidate instead fixed it, and the nonsense
control answered the question that made the series readable: **a dropped tag
takes its subtree with it**, so an unbuilt child is what an unknown tag looks
like. Both forms were needed: `multibutton` takes a click standing alone and
does *not* build a child, so either form alone would have mislabelled it.

**A calibration that fails voids its series, and says so.** The `root-*` series
hangs each candidate off `<skin>` rather than inside the `<panel>`, in case a
`<rack>` only constructs at the root. Its calibration row — a known `<group>`
holding the same button — did not deliver the click either, so no row in that
series is interpretable. It is kept, and reported as void, because the
calibration is itself the finding: nothing outside the `<panel>` built a
clickable object here.

**`forceshow` is the negative with the most work behind it.** A lone panel
shows whatever it forces, nonsense included, so the first series could not
discriminate at all. The second built the shape shipped skins actually use —
two `@`-named panels in one `group=` — and flipped the app's own layout
settings under it: `skin3FxLayout` and `skin6FxLayout` are the only
`skin*Layout` strings in the binary, and both states were tried, each with the
skin reloaded after the change, and once more through `effect_3slots_layout`,
the verb that flips one of them. The visible panel never moved. The branch that
reads the vocabulary was never reached; `8pads`/`16pads`/`timecode` have no
setting of that shape to be keyed to, and `pad_has_16pads` suggests the pads
values are controller-conditional, which this machine cannot present.

**Two candidates were not reached at all.** `applyfx` and `setdeck` sit in the
panel/menu-item construction window with no attribute or element to attach them
to, and the probe's only observable is click routing, so no fixture here could
discriminate them from being ignored. Sizing them needs the H4-style read of
the panel builder — which `getParam` call each string is an argument to — not
another skin variant.

**Two live findings fell out of the setup rather than the probe.** `setting` in
query position answers `yes`/`no` for a real setting name and
`error:-2147024809` for an unknown one, which is an existence discriminator for
setting names; in execute position `setting 'name' 1` sets, a bare
`setting 'name'` toggles, and a *quoted* value is accepted-and-ignored. Both are
recorded on the verb records, with `effect_3slots_layout` confirmed as a toggle
of `skin3FxLayout`.

**Method notes for the next run of this kind.** Loading a skin occasionally
stalls the HTTP interface for several seconds — a timeout there is not a result,
and the runner retries rather than recording one. The probe skins scale to the
window, so the runner's `--calibrate` clicks the one variant whose answer is
known before any series runs. Probe fixtures are excluded from the XML
inventory (`EXCLUDE` in `tools/extract_xml_inventory.py`): they carry nonsense
tags by design, and counting them corrupts the one thing that inventory
measures.

## `auto_bpm_transition`: The Observable Was Wrong, Not The Parameters

The open task the 10b note left: re-test `source_original`, `target_original` and
`target_current` with two decks at different BPMs, reading the resulting BPM over
time. Run 2026-09-07, build 18.0.9598, both decks **stopped** (the transition
runs on a stopped deck, so this made no sound). Prober:
[tools/probe_bpm_transition.py](../tools/probe_bpm_transition.py), artifact
`tests/bpm-transition-forms.json`, two runs with the form order reversed.

**The state no fixture builds.** Three landmarks have to be distinct at once:
deck 1 holds a 100 BPM track, deck 2 a 120 BPM track pitched to 132
(`pitch 132 bpm`), so `source_original` = 100, `target_original` = 120 and
`target_current` = 132 are three different numbers and the *landing point* says
which the verb was told to use. `fixtures.py` generates one tempo, and one
tempo cannot separate a source original from a target original — both would be
120 — so the prober generates a 100 BPM counterpart beside it.

| Form | Lands on | Verdict |
| --- | --- | --- |
| bare | 120 | the default is the target's **original** BPM |
| `source_original` | **100** | **confirmed** — nothing else lands there |
| `target_current` | **132** | **confirmed**, and the only form that leaves the transition engaged |
| `all` | 132 | lands like `target_current`, but disengages |
| `target_original` | 120 | names the default; cannot separate from an ignored tail |
| `zzqqx`, `vfnrbq` | 120 | the floor, and they agree |

**So the earlier negative was an observable failure, not a verb fact.** Both the
arg-form sweep and the execute-position pass had one observable — the boolean
saying whether a transition is *running* — and what these parameters change is
where it lands. Two of the three separate cleanly the moment the observable can
see the landing.

**`target_original` is undiscriminated, not refuted, and it cannot be
discriminated by this route at all**: it names the default, so it lands exactly
where an ignored tail lands. The catalog's note that behavior differs when
`smartPlay` or `autoBPMMatch` are on was the obvious lever — `smart_play`
executed bare toggles the setting, and `setting 'smartPlay'` follows it — but
with it off the default is still 120. Separating it needs a different
observable, not a different state. It stays on the worklist
(`documented_but_not_probe_confirmed`) with the reason recorded here, since the
cross-check only takes `recognized-…` forms from the artifact.

**Two method findings, both of which corrupted a run before they were fixed.**

- **The verb is a toggle, so a form that leaves a transition engaged poisons the
  next form.** `target_current` leaves it running; the next `auto_bpm_transition`
  then *stops* that transition instead of starting one, and the deck sits still
  — which reads exactly like a settled result. The first full run recorded
  `target_original` as landing on 132 in one order and 120 in the other purely
  because of what preceded it. The prober now waits for disengagement before
  every form and aborts if one will not stop; both runs then agreed on every row.
- **A form that lands where the deck already sits is stable from the first
  read.** A settle loop that stops as soon as the value repeats calls that
  settled before the transition has begun, so the loop watches for a minimum
  window regardless.

**Incidental, and worth knowing before the next two-deck probe:** with this
machine's `autoBPMMatch` = `smart`, the two decks are BPM-linked — setting either
deck's pitch drags the other, in both directions, with `beatlock` reporting `no`
on both decks and no transition running. Turning `smart_play` off does not
release it. So a two-deck probe cannot hold the source at its own original BPM
while the target sits pitched; the prober asserts the three landmarks, which are
properties of the tracks plus the target's pitch, and merely records the
source's current BPM rather than requiring it.

**`pitch` arithmetic, since it cost a restore.** `get_pitch` reports a percent
*change* (0 = none) but `pitch N%` sets an absolute slider position where `100%`
is no change, so feeding a reading straight back (`pitch 0%`) drives the slider
to its floor. Restore with `pitch (100 + reading)%`.

**`timecode_cd_mode` closed the same day.** The 2026-09-03 execute-form probe
turned it on and nothing turned it back off, and the prediction was that it is
runtime-only and would clear on restart. Re-read 2026-09-07, after VirtualDJ had
restarted: `no`. Recorded on the verb record; still one-way within a session.

## `all`: Recognized By The Sweep, Inert Where It Was Tested

The other open follow-up in 10b: the shared-lexicon pass found `all` recognized
on 26 verbs — the whole sampler family plus `loop_load`, `loop_select`,
`load_skin`, `load_pulse`, `effect_stems`, `effect_dock_gui`,
`apply_audio_config` — with what it *does* unknown, and named the
`sampler_slots_differ` fixture as the follow-up. That fixture now exists (slots
1, 2, 3 hold different samples of group `Drums`, slot 5 is ungrouped, slot 8 is
empty), so the question is answerable. Run 2026-09-07, build 18.0.9598.

**Query position: `all` returns exactly what bare returns, on every verb tried.**
`sampler_loaded`, `get_sample_name`, `sampler_play` and `sampler_volume` each
answered identically for bare, `all`, `current`, `0` and the focused slot's own
number, while an empty slot and a junk token returned `no` / `error:1` / `0`.

**Which is a correction to how the sweep read it.** On these verbs an
unrecognized tail *errors*, so "separates from the nonsense control" is
satisfied by any token the parser accepts, whether or not it changes the
answer. That is why `all` scored `recognized` on 26 verbs. **Where junk errors,
separation from junk is evidence of parsing, not of meaning** — the second
comparison, against the *bare* form, is what distinguishes a token that says
something from one that is merely accepted. The arg-form artifact records
`same_as_bare_everywhere`, and for this class of verb that flag is the finding.

**Vocabulary of the sampler slot argument**, from the same reads: `all`,
`current`, `0`, `on` and `off` are accepted (all answering as the focused slot);
`auto`, `every`, `any`, `selected`, `first`, `last`, `group`, `deck`, `sampler`
and two junk controls are not. `auto` is worth noting — `sampler_loaded <n>
'auto'` is a documented pad-page form, and bare `sampler_loaded auto` is not
accepted, which matches the earlier finding that the `auto` form tested
unreliable.

**Execute position, on a verb whose state is readable and restorable:** `all`
did nothing. `sampler_volume all 0.7` and `sampler_volume_nogroup all 0.3` left
every slot untouched, exactly as a nonsense slot token did, while `current` and
a slot number both moved volumes in the same session. So on these two verbs
`all` is parsed and inert. That is not a claim about the other 24 — `sampler_stop
all` is the shape one would expect to mean "every slot", and confirming it needs
samples actually playing, which is audible and was not run.

**The by-product is worth more than the answer.** The same probes settled the
`sampler_volume` / `sampler_volume_nogroup` pair, which no source here
described: **`sampler_volume` is group-scoped.** `sampler_volume 1 0.5` moved
slots 1, 2 and 3 together — `get_sample_info <slot> 'group'` reports all three
as `Drums` — and left ungrouped slot 5 alone; `sampler_volume_nogroup current
0.4` moved only slot 1. The slot argument selects *which sample*, and the verb
name decides whether its group comes with it. Every volume was read before,
restored after, and verified back at 1.

## Documented Parameters, 2026-09-07: Nine Verbs Closed And A Triage Of The Rest

Task 13b's premise is that the remaining documented-but-unconfirmed parameters
need *fixtures*. This pass says that is true of only part of them, and sorts the
rest by what they actually need. HTTP, build 18.0.9598. Every reading below has
two nonsense controls that agree with each other; a token counts only where it
differs from **both the controls and the bare form**.

### Closed without any fixture at all

- **`param_cast` — ten of thirteen types, from a chained expression.** It is a
  pipeline verb, so `get_var '$v' & param_cast <type>` *is* the state. With
  v = 12.7: `integer` 13 against `int_trunc` 12 (the documented
  rounding-versus-truncation split, settled in one read), `frac` 0.7, `000`
  013, `percentage` 1270%, `ms` 13ms, `beats` 12.7bt, `float`/`text` 12.7, and
  `boolean` yes at 12.7 / no at 0. On a string source `text 5` cut
  "Chapter & Verse" to "Chapt" and `text 3` to "Cha", so the optional character
  limit holds too. `artist` raises E_INVALIDARG exactly as the nonsense types
  do — it is the doc example's argument to `get_browsed_song`, and is now a
  placeholder. `relative` and `absolute` returned the input unchanged: they act
  on a slider parameter, and a query chain has none, so they stay
  undiscriminated.
- **`param_equal` is a plain string compare**, so its three "parameters" are the
  example's operands: `param_equal 'zzqqx' 'zzqqx'` is yes and
  `param_equal 'audio' 'zzqqx'` is no. The documented backtick shape does hold —
  ``param_equal `get_browsed_song 'type'` 'audio'`` yes, `'video'` no.
- **`get_key 'musical'`**, by flipping the app's own `keyDisplay` setting rather
  than by building a deck state. At `keyDisplay = Harmonic` bare and a nonsense
  tail both read `02A` while `musical` read `Ebm`; the earlier run had the
  mirror image. Each tail forces its own notation and the setting only decides
  what *bare* shows. Restored.
- **`filter_label 'name'` and `'clean'`**, each in the knob position where it can
  separate: at filter 0.75 `name` gave the ColorFX name where bare and both
  controls gave `> 50%`; at the centre `clean` gave `OFF` where bare and both
  controls gave the name. Bare shows the name at rest and the value while the
  knob moves.
- **The sampler `siren` entries are placeholders, and the shape they belong to is
  confirmed.** `sampler_volume 'Dystopia Breaks'` (a sample actually loaded)
  returns that sample's volume, where the catalog's `siren` and a nonsense name
  both return 0.

### Closed by execute-with-readback, restored afterwards

**`browser_window`: all six zone names.** Each token makes exactly its own zone
active and two nonsense tokens change nothing; the zone was read first and put
back. The by-product is structural: `automix`, `sidelist` and `sampler` leave
**both** their own name and `sideview` reading yes, so those three are panes
*inside* the sideview rather than peers of it, while `folders` and `songs` are
standalone.

### Recognized in query position, where the floor is an error

`auto_cue on`/`off`, `cross_assign left`, `prelisten_output auto`,
`search_options composer` and `show_splitpanel sideview` each answer where the
bare form and both controls do not (or answer differently from both). For a verb
with no bare query form, a field name that answers *at all* is the discriminator.
These are recorded as recognized vocabulary, not as confirmed behavior — which
mode or output is selected was not established. `show_splitpanel 'sidelist'`
failed exactly as the controls did, but panel names belong to the loaded skin,
so that is a fact about this skin rather than about the verb.

### The triage: why each remaining entry is stuck

The error code the *bare* query returns sorts the rest, and it says which
instrument each needs:

| Bare returns | Meaning | Verbs | What they need |
| --- | --- | --- | --- |
| `error:-2147467263` (E_NOTIMPL) | **no query implementation at all** | `automix_editor_movetrack`, `browser_move`, `cue_color`, `effect_disable_all`, `effect_list_edit`, `invert_deck`, `karaoke_load`, `playlist_load`, `sidelist_load`, `stem_pad` | execute position plus an **external** observable; no fixture can help, because the query channel cannot see them at all |
| `error:-2147467259` (E_FAIL) | query exists, failed in this state | `get_automix_song`, `mix_and_load_next`, `padfx` | the missing state — an automix list, a pad context |
| answers, but token = bare = controls | reads, cannot discriminate here | `broadcast`, `effects_used`, `hot_cue`, `leftcross`, `linein`, `mixermode`, `pitch_zero`, `sampler_output`, `sampler_rec`, `slicer`, `timecode_mode`, `timecode_reset_pitch`, `video_transition`, `effect_arm_stem`, `sync_hint` | a state where the tokens would differ — the fixture case 13b was written for |

**That E_NOTIMPL row is the useful half of this pass.** Ten of the remaining
verbs are action-only: they are on a worklist that is being worked by a
query-position prober, and no amount of fixture-building will move them. They
belong with `auto_bpm_transition` — execute the verb, watch something else —
and that is a different instrument, exactly as the 13b note predicted.

### The automix fixture, and what it did not unblock

Built the same day, since `get_automix_song` was one of the three E_FAIL
entries and an automix-list fixture was on 13b's still-to-build list.
`automix_populated` adds the browser selection with `playlist_add` and empties
the list again with `playlist_clear`.

**It needed a new guard, and the guard is the point.** Every other fixture
restores what it found; this one restores by *resetting* — it empties a list.
That is only safe when the list was already empty, so `Fixture` now takes
`preconditions`, checked once before setup and never polled, and the fixture
refuses to establish when they do not hold. It refused for real during this run,
on a list left populated by hand, which is the behavior wanted.

**And it did not unblock the verb it was built for.** With one track queued and
then two — `get_playlist_time` moving `error:1` → `04:30` → `09:01`, so the
state is demonstrably live — `get_automix_song` returned E_FAIL on every form,
bare and both nonsense controls included, and so did `get_automix_position`.
`automix` read `no` throughout: these want automix actually **running**, which
plays audio, not merely a queued list. So `title` stays untested rather than
refuted, for the same structural reason as `get_slip_time`: where the bare form
fails, no tail can separate. What the fixture did confirm is `get_playlist_time`,
which reads the list directly.

One side effect worth knowing: `playlist_add` also **loads the first queued
track onto an empty deck**. The fixture's own deck restore undoes it; a hand-run
`playlist_add` will not.

## Shared Enumerations, 2026-09-08: Three Groups, One Pattern

Task 13 asks whether the tables the binary serialises are the verbs' accepted
vocabularies. The colour table said yes; these three say something sharper.
HTTP, build 18.0.9598, two or three agreeing nonsense controls throughout.

**`song_fields` (41 members) — the two song verbs take the same 16, and reject
the same 25.** `get_loaded_song` and `get_browsed_song` agree exactly, on two
different tracks: `album`, `artist`, `author`, `bpm`, `comment`, `composer`,
`filename`, `filepath`, `genre`, `grouping`, `key`, `label`, `remix`,
`remixer`, `title`, `year` answer; everything else raises E_INVALIDARG. The
floor is clean here in a way it usually is not — a real but *empty* field
returns `''`, an unknown one errors, so "no value" and "no such field" are
distinguishable. `author` returned the artist on both tracks, so it is an
alias; `album` and `title` differed on the browsed track, so they are not.
The 25 rejected members are recognisable as somebody else's vocabulary: the
RIFF chunk ids (`iart`, `icmt`, `icop`, `ignr`, `inam`, `iprd`, `isbj`, `isft`,
`strn`) and the two-letter forms (`al`, `ar`, `au`, `by`, `re`, `ti`, `ve`)
belong to a file-tag reader, not to these verbs.

**`audio_channels` (15 members) — `effect_arm_deck` takes four.** `master`,
`mic`, `sampler`, `aux`; the other eleven return the bare answer exactly as the
controls do. This negative is stronger than the usual "failed to separate",
because the fixture makes the direction knowable: with only the DECK arm
engaged, bare and an ignored tail both read `yes`, while any channel the verb
actually reads must read `no` — which is precisely what the four accepted names
did. `master` is new; the catalog documents only aux/mic/sampler.

**`settings_pages` (19 members) — the verb's vocabulary is the dialog's tab
list, and the table is something else.** `settings '<page>'` in query position
answers whether the Settings dialog is showing that page, so with the dialog
closed everything reads `no` and the group is unprobeable. With it open, nine
names select themselves and drop the previous page: **audio, broadcast,
controllers, extensions, interface, licenses, options, record, tutorials** —
exactly the tabs down the left of the dialog. Four of them (`tutorials`,
`interface`, `licenses`, `extensions`) are **not in the serialised table at
all**, and fourteen of the table's members (`all`, `automation`, `automix`,
`browser`, `controls`, `internet`, `karaoke`, `modified`, `performance`,
`sampler`, `skins`, `tags`, `timecode`, `video`) are not accepted by the verb.
That table is a different enumeration — the category filter inside the Options
page is the obvious candidate — and reading it as this verb's argument list
would have produced fourteen wrong entries and missed four right ones.

**The pattern across all three: a serialised table is a table, not a
signature.** Each group is shared by several consumers and every verb takes its
own subset — sometimes a subset that is not even contained in the table. So a
group-level conclusion has to name *which verb* it holds for, and a table
member that a verb rejects is evidence about that verb, not about the member.

**Two operational findings about the settings dialog**, both learned by
tripping over them:

- **Opening it stalls the HTTP interface** for several seconds — the modal
  blocks the message loop. A timeout there is not a result; the sweep needs a
  retrying client.
- **It cannot be closed from script.** Bare `settings`, `settings 'close'` and
  `settings 'off'` all return `false` and leave it open. Closing it took a
  click on the dialog's own X, verified by the query returning to `no`. So a
  settings-page sweep is not a pure-HTTP probe: budget a GUI click for the way
  out before opening it.

## Documented Parameters, 2026-09-08: Enumerable Vocabularies And Two Doc Misreadings

HTTP, build 18.0.9598. Another pass over `just action-catalog --cross-check` →
`documented_but_not_probe_confirmed`, this time picking entries by *how they
fail* rather than by verb family. Two or more agreeing nonsense controls beside
every candidate. Deck 2 held a library track throughout and was never executed
against; deck 1 was empty before and after every probe. Worklist 54 verbs / 97
tokens → 43 / 77.

### The floor tells you which method will work

A first sweep asked one question of all 54 worklist verbs — bare, `zzqqx`,
`wubfar` in query position — and the *error codes* sorted them into groups that
each want a different instrument:

| Floor | Verbs | What can be learned in query position |
| --- | --- | --- |
| `E_NOTIMPL` bare **and** tailed | `automix_editor_movetrack`, `browser_move`, `cue_color`, `effect_disable_all`, `effect_list_edit`, `invert_deck`, `karaoke_load`, `padshift_pressure`, `playlist_load`, `sidelist_load`, `stem_pad` | nothing — these have no query implementation at all, so their tails are an execute-position question |
| `E_INVALIDARG` bare **and** tailed | `hot_cue`, `effect_colorfx`, `effect_list`, `loop_color`, `padshift` | nothing in query position; every form is rejected, slot numbers included |
| `E_INVALIDARG` bare, **answers** tailed | `browser_sort`, `sideview_sort`, `browsed_file_color`, `os2l_button`, `os2l_scene`, `sync_hint`, `show_splitpanel` | the tail is required, so the comparison is value-against-value |
| answers bare, **`E_INVALIDARG`** tailed | `sampler_loop`, `param_cast` | **the verb rejects what it does not know, so its vocabulary is enumerable by acceptance** |
| answers everything | the rest | only a state where the forms disagree |

The fourth row is the useful one and it had not been used before. Where junk
*errors*, separation from junk proves parsing and nothing else — the `all`
section above is the warning — but for a token whose **meaning the appendix
already states**, parsing is exactly the missing half. That turns "confirm a
documented parameter" into a question the channel answers directly.

### `param_cast` — the vocabulary is a closed, exactly-matched set

`absolute` and `relative` are accepted where `zzqqx`, `wubfar`, `seconds` and
`hex` raise `E_INVALIDARG`, and they answer in a class of their own: `''`,
where every cast type returns `error:1`. That split is the appendix's own
distinction — they change how a value is applied rather than casting it.

Matching is exact, not prefix: `int` and `percent` are accepted, `inte`,
`integ`, `intx`, `integerx`, `perc`, `beat`, `fra`, `tex`, `abso` and
`relativ` are not. The digit format generalises past the documented `000` —
`0`, `00`, `0000` and `00.0` are all accepted.

### `browser_sort` / `sideview_sort` — a membership oracle for the sort fields

In query position both answer `no` for a real sort field and `yes` for anything
else, so the enumeration can be read straight off. **36 names**, identical for
both verbs, stable across two runs:

```
album artist author bitrate bpm bpmdiff color comment composer drive field1
field2 filename filepath filesize firstplay firstseen genre grouping key
keydiff label lastplay length order playcount pos position rating remix
remixer stars title track type year
```

Five nonsense controls answer `yes`, and so do the plausible near-misses:
`play_count`, `date`, `added`, `random`, `folder`, `user1`, `user2`,
`linkedvideo`, `hascue`, `hasstems`, `duration`, `albumartist`, `camelot`.
`field3`..`field11` are rejected while `field1`/`field2` are accepted, which
matches the two custom fields the app exposes. Exactly one leading `+` or `-`
is accepted (`++title`, `*title`, `~title` are not), and matching is
case-insensitive (`TITLE`, `ArTiSt`).

What the boolean *means* is not established. The reading consistent with junk
answering `yes` is that an unparsed key falls back to the current sort and so
trivially matches it — which predicts that a real key answers `yes` once the
browser is actually sorted by it. That prediction is untested: confirming it
needs an execute, and no verb reads the current sort back, so there would be
nothing to restore to.

### `get_slip_time` — the earlier Fail was the wrong enabler

The 2026-09-06 run recorded this verb as unreachable: `E_FAIL` in every form,
"with slip_mode confirmed on". **`slip_mode` and `slip` are independent
states.** `deck 1 slip_mode on` leaves `deck 1 slip` reading `no` and
`get_slip_time` still erroring; `deck 1 slip on` leaves `slip_mode` reading
`no` and makes the verb answer. Verified both ways in one run.

With slip engaged and the shadow playhead parked past a minute — position set
to 60,465 ms, then `goto_start` so the playhead and the shadow diverge:

| form | run 1 | run 2 | run 3 |
| --- | --- | --- | --- |
| bare | 65387 | 66548 | 67708 |
| `min` | 1 | 1 | 1 |
| `sec` | 5 | 6 | 7 |
| `msec` | 437 | 598 | 758 |
| `zzqqx` | 65449 | 66610 | 67771 |
| `wubfar` | 65462 | 66622 | 67783 |

`min`·60000 + `sec`·1000 + `msec` reproduces the bare value to within the ~12 ms
the clock drifts between two queries, which is the check that clinches it. Both
controls return the bare value, so the units are read and an unknown tail is
ignored. **The shadow clock advances in real time even with the deck stopped**,
which puts this verb in the `get_cpu` class: three runs a second apart, not one.

### `effect_arm_stem` — the tokenizer read the wrong sentence

The appendix says: *"Select/unselect a stem to be used with "stems" as slot for
effect_ actions. Accepted stem names are Vocal, HiHat, Bass, Instru, Kick. They
can be combined using "+"."* The parameter tokenizer takes quoted spans, so it
extracted `stems` — the **slot** name — and missed the unquoted sentence that
lists the actual vocabulary.

All five stem names confirmed. In query position `instru`, `kick`, `hihat` and
`bass` answer `no` where bare, `vocal` and four nonsense controls answer `yes`;
bare is the aggregate, which is why an unrecognized tail lands on `yes`.
Executing a stem's own token toggles exactly that stem — `kick` no→yes,
`vocal` yes→no, nothing else moving — and the arm was restored to vocal-only
and verified. `vocals`, `instrumental`, `drums`, `melody`, `rhythm`, `stems`,
`stem`, `aux`, `mic`, `mixfx` and `all` all behave as the controls do.

The `+` combinator holds and comes with three rules the doc does not give:

- `kick+bass` toggles both, case-insensitively (`Kick+Bass`).
- **No surrounding space.** `kick + bass` returns `true` and changes nothing.
- An unknown member is dropped while the known ones still apply
  (`kick+zzqqx` toggles kick).
- In **query** position `+` is a conjunction: with only vocal armed,
  `vocal+kick` → `no` and `vocal+vocal` → `yes`.

### `pitch <n> bpm` — a two-token execute form whose second token is required

On the 120 BPM fixture track: `pitch 130 bpm` → `get_bpm` 130, pitch 0.63;
`pitch 100 bpm` → 100, 0.25. `pitch 130 zzqqx`, `pitch 130 wubfar` **and the
bare `pitch 130`** all returned `false` and left the deck at 120 / 0.5. So the
tail is not an optional modifier — without it the whole form is rejected. This
is the fourth confirmed two-token grammar, after `get_song_event`,
`browsed_song` and `auto_bpm_transition_options`.

### `hot_cue` — the appendix is naming other buttons

*"if no cue point is set, or if 'cue', 'cue_stop' or 'cue_play' is pressed, set
one at the current position"* describes **which other button was pressed**, not
`hot_cue`'s own tail. Measured: all three, and both nonsense controls, set cue 1
at the playhead and left the deck paused, identically. (Incidental: the cue
landed at 10,496 ms from a 10,000 ms playhead — `hot_cue` snaps to the beat.)
Moved to `documented_example_placeholders`.

### A third bucket: parameters that name the default

Three worklist entries are real vocabulary that **no state can separate**,
because they select what the verb does anyway. They were being re-probed each
pass, so `cross_check` now reports them as
`documented_but_names_the_default` rather than as unconfirmed work:

- `effects_used 'deck'` — with a deck effect on, bare/`deck`/junk all `yes` and
  `master` `no`; with a **master** effect on instead (`deck master
  effect_active 1 on`), bare/`deck`/junk all `no` and `master` `yes`. So bare
  *is* the deck scope — which also refutes the appendix's "Active when there are
  any effects activated" — and `master` is the token that carries information.
- `mixermode 'internal'` — `external` answers `no` where bare, `internal` and
  both controls answer `yes`. Separating `internal` means switching the audio
  config to an external mixer, which is the user's setup, not a fixture.
- `auto_bpm_transition 'target_original'` — established in the section above.

### Also settled, and why the rest is stuck

- **`loaded_song 'rating' <n>`** is an equality predicate like `browsed_song`:
  `yes` at the track's own rating (0, read independently through
  `get_loaded_song 'rating'`), `no` at 1..5, and `no` for two nonsense field
  names at any value.
- **`sampler_loop 'play'` is rejected in query position** — `E_INVALIDARG`,
  where bare and the undocumented `current` answer `yes`. Not a refutation of
  the verb's action tail: the execute path parses its own.
- **`browsed_file_color` echoes any tail verbatim**, junk included, so no
  query-position comparison can ever separate `red` or `reset`. The 2026-09-06
  record already said this; it is repeated here so the next pass does not spend
  another round on it.
- `slicer`, `sampler_bank`, `sampler_output`, `sampler_rec`, `linein`,
  `motorwheel`, `broadcast`, `timecode_reset_pitch`, `video_transition`,
  `pitch_zero`, `leftcross`, `get_limiter`, `get_level` and `get_vu_meter` all
  answered the bare value for every documented token and both controls — the
  states that would separate them are a pad surface, an audio input, a
  broadcast session, timecode hardware, or a meter that is not reading zero.
- **`get_time_hour` is the one clearly buildable state left**: it wants a track
  longer than an hour. Total 2h05m with the playhead at 1h10m makes `elapsed` 1,
  `remain` 0 and `total` 2, and reading it once with `display_time` on `elapsed`
  and once on `remain` (bare and junk follow the setting) separates all three;
  `absolute` needs the playhead where pitched and unpitched remaining time fall
  on opposite sides of an hour boundary, e.g. 3,700 s in at +12%.

## Long-Track Time Readers, 2026-09-12

Local test, HTTP, running instance `get_build` returned `9598`. Artifact:
`tests/long-time-forms.json`; regenerate with `just probe-long-time`, inspect with
`just long-time-forms`. Per-verb conclusions are in the store.

The generated FLAC is 7500 seconds, verified by ffprobe. At 4200 seconds with zero
pitch, `get_time_hour elapsed/remain/total` returned 1/0/2. Bare followed the selected
display mode. At 3750 seconds and +12 percent pitch, `absolute` returned 1 while
pitched elapsed and remain returned 0. Its value at zero pitch under both display
modes confirms that it retains the selected mode. `elapsed` matched both junk tokens
in every phase and the independent elapsed-time arithmetic: it names the fallback,
not a separately discriminated token. The fractional 4207.125-second phase separated
remain from elapsed for the lower-unit readers. `get_time_sign` remained 1 throughout;
negative-sign behavior is not established. Raw readings include reversed form order
and two independently established runs with restoration verified.

Two setup failures preceded the retained capture. Unscaled `get_position` serialized
too coarsely to assert 3700 seconds; `get_position & param_multiply 7500000` returns
the position in milliseconds before HTTP rounding. The final midpoint was 3750 seconds.
Repeated `deck 1 display_time 'remain'` writes also exposed a restoration trap: from
remain, another such write changed the readback to elapsed; a third restored remain.
Each write returned true and the independent elapsed/remain/total queries showed the
change. The earlier timing hypothesis was wrong. The final runner checks the current
mode before writing and verifies the mode, empty deck, stopped transport and original
pitch after unloading. The original remain mode and zero pitch were restored.

No personal media was loaded: the runner refuses an occupied deck. Generated audio
is temporary; the checked-in artifact contains only synthetic-media measurements.
