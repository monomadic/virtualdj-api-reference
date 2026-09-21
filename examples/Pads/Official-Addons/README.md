# Atomix-Published Pad Page Add-ons

Pad pages that Atomix publishes through the VirtualDJ add-on catalog rather than shipping in
the app bundle, copied from this machine's VirtualDJ install.

## Provenance

Authorship comes from the app's own add-on catalog, `https://virtualdj.com/live/addons.php?os=mac`,
fetched 2026-09-21. The catalog gives `author: "Atomix Productions"`, and the public listing page
(`https://virtualdj.com/plugins/?addonid=<id>`) credits the "Development Team" account.
`download.virtualdj.com` refuses a direct download (`AccessDenied`), so the only copy available
is the one the app installed.

| File | Add-on id | Catalog `lastdate` | Installed file | SHA-256 | Installed mtime |
| --- | --- | --- | --- | --- | --- |
| [A-BPM TR.xml](A-BPM%20TR.xml) | 81637 | 2023-09-21 | `~/Library/Application Support/VirtualDJ/Pads/A-BPM TR.xml` | `bb1c8538fd599fabb75228c17a93e83fb4ecb1b905071da747e9487b224a3ff8` | 2026-09-21 |
| [DJC Buttons.xml](DJC%20Buttons.xml) | 80676 | 2017-10-31 | `~/Library/Application Support/VirtualDJ/Pads/DJC Buttons.xml` | `0704dc64ff53e1cdbe27cf6b2a95e1e840caf898cf047be8d113238868e99300` | 2026-09-21 |
| [Piano Play.xml](Piano%20Play.xml) | 81892 | 2025-08-21 | `~/Library/Application Support/VirtualDJ/Pads/Piano Play.xml` | `73851b3886fd3d437a0d33b1619d637ae219798765f7446b84bdb133bdb81f88` | 2026-09-21 |
| [Stems Inverted.xml](Stems%20Inverted.xml) | 81380 | 2021-10-09 | `~/Library/Application Support/VirtualDJ/Pads/Stems Inverted.xml` | `2747e4a8c1cb3e6ab710fc3d7521cb3d0b402ea0604d4dbbf7579fc8f48de2f4` | 2026-09-21 |
| [Stems Split 3-Band.xml](Stems%20Split%203-Band.xml) | 81631 | 2023-09-15 | `~/Library/Application Support/VirtualDJ/Pads/Stems Split 3-Band.xml` | `6c47de25737e3e015ecbb552ddc99ff4094d0c00053578eec1d47919be71edb7` | 2026-05-08 |
| [Stems Split 4-Band.xml](Stems%20Split%204-Band.xml) | 81632 | 2023-09-15 | `~/Library/Application Support/VirtualDJ/Pads/Stems Split 4-Band.xml` | `5e5316c0b4ce0ce9ea35e29e449dff93fac32ec945f9eaa7b1d21213a308dead` | 2026-09-21 |

Copied 2026-09-21 on installed VirtualDJ bundle `18.0.9644`.

Rows whose installed mtime is 2026-09-21 were fresh Extensions-browser installs, copied within minutes.
`Stems Split 3-Band.xml` was installed earlier (mtime 2026-05-08). A pad page is a plain XML file
the Pads editor can rewrite in place, so nothing proves that copy is still byte-identical to the
published add-on. Before citing an exact line from it, compare it against a fresh install.

Evidence tier: `Published pad page` (Tier 2, see [Evidence Standards](../../../docs/Evidence%20Standards.md)).
It is an Atomix-written executable example, not proof that a verb works.
