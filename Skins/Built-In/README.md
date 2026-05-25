# Built-In VirtualDJ Skins

This folder contains skin XML and assets copied from the local VirtualDJ application bundle.

Source:

- App bundle: `/Applications/VirtualDJ.app/Contents/Resources/`
- VirtualDJ version: `8.5.9307`
- Bundle version: `18.0.9336`
- Copied on: `2026-05-24`

Treat these files as `Built-in skin` evidence: semi-official executable examples of skin XML shipped by Atomix. They are stronger provenance than community skins, but they are not the same as prose API documentation. Prefer curated local skeletons and documented patterns for new work, and use this folder to inspect how VirtualDJ's shipped skins exercise the skin engine.

Do not hand-edit these copies. Refresh them from the app bundle when updating to a new VirtualDJ build, then review the diff.

Refresh commands:

```sh
mkdir -p Skins/Built-In/Desktop Skins/Built-In/Remote Skins/Built-In/Lite Skins/Built-In/Plugin-UI
unzip -o -q /Applications/VirtualDJ.app/Contents/Resources/skin.zip -d Skins/Built-In/Desktop
unzip -o -q /Applications/VirtualDJ.app/Contents/Resources/remoteskin.zip -d Skins/Built-In/Remote
cp -p /Applications/VirtualDJ.app/Contents/Resources/Lite.xml Skins/Built-In/Lite/
cp -p /Applications/VirtualDJ.app/Contents/Resources/lite.png Skins/Built-In/Lite/
cp -p Skins/Built-In/Desktop/gfx-basic.png Skins/Built-In/Lite/
cp -p /Applications/VirtualDJ.app/Contents/Resources/AFX_beatgrid.xml Skins/Built-In/Plugin-UI/
cp -p /Applications/VirtualDJ.app/Contents/Resources/AFX_BeatGrid.png Skins/Built-In/Plugin-UI/
```

Important parser note: these files are kept as shipped. Some built-in skin XML does not pass generic `xmllint` checks because the VirtualDJ skin parser accepts VDJScript-heavy attributes, raw `&` / `&&`, and other constructs that are not strict XML. Do not "fix" these copies unless the goal is to maintain a separate normalized fixture.

## Desktop

Extracted from `/Applications/VirtualDJ.app/Contents/Resources/skin.zip`.

- [Desktop/Starter.xml](Desktop/Starter.xml)
- [Desktop/Essentials.xml](Desktop/Essentials.xml)
- [Desktop/Performance.xml](Desktop/Performance.xml)
- [Desktop/Pro.xml](Desktop/Pro.xml)
- [Desktop/Vertical.xml](Desktop/Vertical.xml)
- Shared assets: `gfx-basic.png`, `gfx-pro.png`, `icons_daylight.png`, preview PNGs, and `order`

## Lite

Copied from loose app-bundle resources:

- [Lite/Lite.xml](Lite/Lite.xml)
- `lite.png`
- `gfx-basic.png` copied from the desktop skin bundle so the skin XML has its referenced base image beside it.

## Remote

Extracted from `/Applications/VirtualDJ.app/Contents/Resources/remoteskin.zip`.

- [Remote/16x10T.xml](Remote/16x10T.xml)
- [Remote/16x9P.xml](Remote/16x9P.xml)
- [Remote/16x9T.xml](Remote/16x9T.xml)
- [Remote/19x9P.xml](Remote/19x9P.xml)
- [Remote/3x4T.xml](Remote/3x4T.xml)
- [Remote/4x3T.xml](Remote/4x3T.xml)
- [Remote/9x16P.xml](Remote/9x16P.xml)
- [Remote/9x16T.xml](Remote/9x16T.xml)
- [Remote/9x19P.xml](Remote/9x19P.xml)
- Shared assets: `tablet.png`, landscape/portrait preview PNGs, and phone preview JPGs

## Plugin UI

Copied from loose app-bundle resources:

- [Plugin-UI/AFX_beatgrid.xml](Plugin-UI/AFX_beatgrid.xml)
- `AFX_BeatGrid.png`

This appears to be a compact built-in effect/plugin UI skin rather than a full desktop skin, but it is useful evidence for small plugin GUI XML patterns.
