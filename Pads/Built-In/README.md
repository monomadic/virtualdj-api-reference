# Built-In VirtualDJ Pad Pages

This folder contains pad-page XML copied as-is from the local VirtualDJ application bundle.

Source:

- Path: `/Applications/VirtualDJ.app/Contents/Resources/pads_*.xml`
- VirtualDJ version: `8.5.9307`
- Bundle version: `18.0.9336`
- Copied on: `2026-05-24`

Treat these files as `Built-in pad page` evidence: semi-official executable examples of shipped VirtualDJ pad-page XML. They are stronger provenance than community pad pages, but they are not the same as prose API documentation. Prefer curated root-level reference pages for copy/paste patterns, and use this folder when you need to see how Atomix's shipped pages exercise VDJScript in real pad XML.

Do not hand-edit these copies. Refresh them from the app bundle when updating to a new VirtualDJ build, then review the diff.

Refresh command:

```sh
cp -p /Applications/VirtualDJ.app/Contents/Resources/pads_*.xml Pads/Built-In/
```

Included files:

- [pads_beatjump.xml](pads_beatjump.xml)
- [pads_cueloop.xml](pads_cueloop.xml)
- [pads_dmx.xml](pads_dmx.xml)
- [pads_hotcues.xml](pads_hotcues.xml)
- [pads_keycue.xml](pads_keycue.xml)
- [pads_loop.xml](pads_loop.xml)
- [pads_loop_roll.xml](pads_loop_roll.xml)
- [pads_manual_loop.xml](pads_manual_loop.xml)
- [pads_remix_points.xml](pads_remix_points.xml)
- [pads_sampler.xml](pads_sampler.xml)
- [pads_sampler_velocity.xml](pads_sampler_velocity.xml)
- [pads_saved_loops.xml](pads_saved_loops.xml)
- [pads_scratch.xml](pads_scratch.xml)
- [pads_scratchbank.xml](pads_scratchbank.xml)
- [pads_slicer.xml](pads_slicer.xml)
- [pads_stems.xml](pads_stems.xml)
- [pads_stems+fx.xml](pads_stems+fx.xml)

Nearby app resources such as `AUDIO FX.xml`, `FAMOUS.xml`, `INSTRUMENTS.xml`, and `VIDEO & SCRATCH.xml` are sampler banks rather than pad pages, so they are intentionally not copied here.
