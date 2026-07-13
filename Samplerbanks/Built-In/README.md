# Built-In VirtualDJ Sampler Banks

This folder contains sampler-bank XML copied as-is from the local VirtualDJ application bundle.

Source:

- Path: `/Applications/VirtualDJ.app/Contents/Resources/*.xml` (sampler-bank files only)
- VirtualDJ version: `8.5.9307`
- Bundle version: `18.0.9482`
- Copied on: `2026-07-12`

Treat these files as `Built-in app resource` evidence: semi-official executable examples of shipped sampler-bank XML. This is a third XML format, distinct from pad pages and skins.

Format observed in these files:

- Root element: `<samplerbank>`
- Child element: `<sample path="" col="" row="" />`
  - `path` - backslash-separated path to a `.vdjsample` file, relative to the sampler content root (e.g. `Audio\Air Horn.vdjsample`)
  - `col` / `row` - zero-based grid position of the sample in the bank

User-created banks live under `~/Library/Application Support/VirtualDJ/Sampler/` on macOS. The `.vdjsample` binary format itself is not yet mapped; see `Reference/Application Internals.md`.

Do not hand-edit these copies. Refresh them from the app bundle when updating to a new VirtualDJ build, then review the diff.

Refresh command:

```sh
for f in "AUDIO FX" "FAMOUS" "INSTRUMENTS" "VIDEO & SCRATCH"; do
  cp -p "/Applications/VirtualDJ.app/Contents/Resources/$f.xml" "Samplerbanks/Built-In/$f.xml"
done
```

Included files:

- [AUDIO FX.xml](AUDIO%20FX.xml)
- [FAMOUS.xml](FAMOUS.xml)
- [INSTRUMENTS.xml](INSTRUMENTS.xml)
- [VIDEO & SCRATCH.xml](VIDEO%20&%20SCRATCH.xml)
