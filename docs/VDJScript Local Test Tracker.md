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
Follow-up: Structural map (labels/counts) captured for all 95 in the dump and queryable via `just get-fx / find-fx / fx-stats`. NOT yet captured: normalized slider defaults (get_effect_slider_default) and reset-value text, which need a per-slider reset pass; and an audio-vs-video classification for the 95 (the sweep cannot currently tell them apart). No hand-transcription into Effects Engines.md — query the dump instead.
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
| Native effect parameter examples | Existing pad pages provide working presets, but the repo does not yet have a systematic effect-by-effect slider/button map. | Pad XML and skin/custom button controls for selected native effects. | Use [Reference - FX Introspection Test.xml](../tests/Pads/Reference%20-%20FX%20Introspection%20Test.xml) as a starter fixture; for each native effect, load it in slot 1, record counts, labels, defaults, button count, and tested `effect_slider`/`padfx` presets with VirtualDJ build/effect version. | v2026-m b9482; full pass TBD | None required | Partial | Per-effect map (deck FX slot 1, v2026-m b9482) started in `docs/Effects Engines.md`: **Backspin** — 2 sliders, 0 buttons: S1 `Strength`/`STR` (%, e.g. `0%`), S2 `Length`/`LEN` (beats, e.g. `4 bt`). **Flanger** — 4 sliders, 2 buttons: S1 `Strength`/`STR` (`50%` reset), S2 `Speed`/`LEN` (`8 bt` reset), S3 `Feedback`/`FBCK` (`50%` reset), S4 `LFO Amp`/`LFO` (`50%` reset); B1 `Tone`/`TONE`, B2 `Phase`/`PHASE`. **Echo** — 6 sliders, 4 buttons: S1 `Strength`/`STR` (`52%` reset), S2 `Length`/`LEN` (`1/2 bt` reset), S3 `Feedback`/`FB` (`52%` reset), S4 `Filter`/`FILT` (`OFF` reset), S5 `Lowpass`/`LP` (`20 Hz` reset), S6 `Highpass`/`HP` (`20000 Hz` reset); B1 `Reverse`/`REV`, B2 `Freeze`/`FRZ`, B3 `Mute Source`/`MUTE`, B4 `Lock On Max`/`LCK`. **Reverb** — 4 sliders, 2 buttons: S1 `Strength`/`STR` (`50%` reset), S2 `Decay`/`DEC` (`50%` reset), S3 `Room Size`/`SIZE` (`50%` reset), S4 `Brightness`/`BRI` (`50.0%` reset); B1 `Low Cut`/`LOW`, B2 `Hi Cut`/`HI`. **Beat Grid** — 1 slider, 2 buttons: S1 `Slot`/`SLOT` (`Slot 1` reset); B1 `Mode`/`>>`, B2 `Video`/`VIDEO`. Reset changed the slot readback from `Slot 3` to `Slot 1`; the GUI showed the mode choices as `SNGL` and `CONT`. The canonical selector is `'Beat Grid'`: the earlier `'BeatGrid'` loader left the previous effect selected, so affected fixtures/examples were corrected. **Beat Brake** — 4 sliders, 1 button: S1 `Strength`/`STR` (`50%` reset), S2 `Pattern`/`PAT` (`Pat 1` reset), S3 `Bars`/`BARS` (`2 bars` reset), S4 `HPF`/`HPF` (`Off` reset); B1 `Quantize`/`QUANT`. **BrakeStart** — 1 slider, 1 button: S1 `Length`/`LEN` (`2.76 s` reset); B1 `Restart Play`/`RESTART`. The live name corrected the stale catalog spelling `Break Start`. **Choppa** — 3 sliders, 1 button: S1 `Strength`/`STR` (`100%` reset), S2 `Length`/`LEN` (`Pat 1` reset), S3 `Invert`/`INV` (`Off` reset); B1 `Quantize`/`QUANT`. **Cut** — 4 sliders, 4 buttons: S1 `Strength`/`STR` (`52%` reset), S2 `Length`/`LEN` (`1/2 bt` reset), S3 `Duty`/`DUTY` (`50%` reset), S4 `Swing`/`SWING` (`0%` reset); B1 `Low Cut`/`LOW`, B2 `High Cut`/`HIGH`, B3 `Mute Beats`/`INV`, B4 `Video`/`VIDEO`. **Cyclone** — 3 sliders, 0 buttons: S1 `Strength`/`STR` (`50%` reset), S2 `Length`/`LEN` (`1/2 bt` reset), S3 `Delay`/`DELAY` (`203 ms` reset). **Delay** — 4 sliders, 2 buttons: S1 `Strength`/`STR` (`52%` reset), S2 `Length`/`LEN` (`1/2 bt` reset), S3 `Swing`/`SWING` (`0%` reset), S4 `LR Ratio`/`LR` (`0%` reset); B1 `Low Cut`/`LC`, B2 `High Cut`/`HC`. Counts and `effect_has_*` positions matched the visible controls. The by-name default pad remained hardcoded to Backspin, so its `0.5` was excluded for the other effects. **Superseded by the full sweep (VirtualDJ 2026, HTTP interface, 2026-07-22):** [tools/sweep_fx_introspection.py](../tools/sweep_fx_introspection.py) captured counts, short+full labels, normalized defaults, live value text, and length/beats flags for all **119** installed effects into [tests/fx-introspection-dump.json](../tests/fx-introspection-dump.json). Query it with `just get-fx <effect>` / `just find-fx` rather than reading either the dump or the prose above; the hand-written entries here are kept only as the provenance of the original method. Spot-checked identical to the hand map. |
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
