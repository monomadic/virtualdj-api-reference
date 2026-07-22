# Built-In VirtualDJ Video Skins

Video skins copied as-is from the local VirtualDJ application bundle. Video skins are a distinct category from deck skins: VirtualDJ renders them onto the video/broadcast output (the master video mix, karaoke, and streaming overlays), and installs them under a separate `VideoSkins/` folder rather than `Skins/`.

They use the **same `<skin>` XML format** as deck skins — see [docs/Skin SDK.md](../../../docs/Skin%20SDK.md), [docs/Skin Waveforms.md](../../../docs/Skin%20Waveforms.md), and the XML element inventory (`just find-xml-elements --family=video_skins`) — so they are useful reference material for skin authoring, especially for `<visual>` video sources and effect-introspection idioms.

Source:

- Path: `/Applications/VirtualDJ.app/Contents/Resources/videoskin{broadcast,karaoke,live}.zip`
- VirtualDJ version: `8.5.9307`
- Bundle version: `18.0.9482`
- Copied on: `2026-07-14`

Treat these as `Built-in skin` evidence: semi-official executable examples of shipped VirtualDJ video-skin XML. Like the deck-skin copies, they are kept exactly as shipped and are not guaranteed to pass strict XML parsers (VDJScript-heavy attributes, raw `&`).

Do not hand-edit these copies. Refresh from the app bundle when updating to a new VirtualDJ build, then review the diff.

Refresh command:

```sh
for s in broadcast karaoke live; do
  unzip -o -q "/Applications/VirtualDJ.app/Contents/Resources/videoskin$s.zip" -d "examples/VideoSkins/Built-In/$s"
done
```

Included skins:

| Skin | `<skin name>` | Files | Notes |
| --- | --- | --- | --- |
| [broadcast/](broadcast/broadcast.xml) | `for Broadcast` | broadcast.xml, broadcast.png, preview.png | Atomix 2018. Source of the effect-name `get_effect_slider_default 'active' <fallback>` form (line 241) — see [docs/Effects Engines.md](../../../docs/Effects%20Engines.md#effect-introspection-and-dynamic-controls). |
| [karaoke/](karaoke/karaoke.xml) | `for Karaoke` | karaoke.xml, karaoke.png, preview.jpg | Karaoke video overlay. |
| [live/](live/live.xml) | `for Live` | live.xml, live.png, preview.png | Live/streaming layout. |
