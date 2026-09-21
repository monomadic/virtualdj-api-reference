# Atomix-Published Sampler Bank Add-ons

Sampler-bank XML from the two sample packs Atomix publishes through the VirtualDJ add-on
catalog, copied from this machine's VirtualDJ install. **Only the bank XML is copied.** The
`.vdjsample` audio is third-party content (the catalog credits loopmasters.com) and is left out,
as with [Built-In/](../Built-In/).

## Provenance

The catalog (`https://virtualdj.com/live/addons.php?os=mac`, fetched 2026-09-21) gives
`author: "Atomix Productions"`. Both packs were installed through VirtualDJ's Extensions browser
on 2026-09-22, because `download.virtualdj.com` refuses a direct download.

| File | Add-on id | Catalog name | Catalog `lastdate` | Installed zip | Zip SHA-256 |
| --- | --- | --- | --- | --- | --- |
| [Loopmasters A.xml](Loopmasters%20A.xml) | 81745 | LoopMasters A | 2024-06-24 | `Sampler/LoopMasters A.zip` | `98f1896bc96daacb3f316febe5fa3797e4aa579617546fada7df9a0668a32739` |
| [Loopmasters B.xml](Loopmasters%20B.xml) | 81746 | LoopMasters B | 2024-06-24 | `Sampler/LoopMasters B.zip` | `72adab78181e29ee99602c4446374d4e676a76151962f3cdb8391da7e6c88e54` |

Format: the same `<samplerbank>` / `<sample>` shape as the Built-In banks, with `path`,
`filesize`, `group`, `color` (named colours and `#RRGGBB` both occur) and `col` / `row` grid
placement. The `path` values use Windows backslashes (`Loopmasters A\RoundKick.vdjsample`) even
in the copy installed on macOS.

Copied 2026-09-22 on installed VirtualDJ bundle `18.0.9644`. Do not hand-edit.
