# Atomix-Published Controller Add-ons

Controller device definitions (with one mapping) that Atomix publishes through the VirtualDJ
add-on catalog's "Custom Mappers" section, copied from this machine's VirtualDJ install. They are
distributed as zips that VirtualDJ installs into `Devices/`, not compiled into `controllers.dat`.
That makes them some of the few Atomix-written device definitions readable as plain XML without
`just controllers-extract`.

## Provenance

Authorship comes from the app's own add-on catalog, `https://virtualdj.com/live/addons.php?os=mac`,
fetched 2026-09-21. The catalog gives `author: "Atomix Productions"`. **It is the catalog, not the
XML `author=` attribute, that establishes authorship.** [../README.md](../README.md) explains why
that attribute proves nothing. `download.virtualdj.com` refuses a direct download (`AccessDenied`),
so both zips were installed through VirtualDJ's Extensions browser on 2026-09-22 and unzipped
here within minutes.

| Folder | Add-on id | Catalog name | Catalog `lastdate` | Catalog description | Installed zip | Zip SHA-256 |
| --- | --- | --- | --- | --- | --- | --- |
| [force-Platinum/](force-Platinum/) | 80621 | Numark Mixtrack Platinum Fix | 2023-02-15 | Fixes the hum noise from dimmed LEDs; v1.1 fixes the jog time display | `Devices/force-Platinum.zip` | `c4fe668327b62613a8143705a3d2af73a4dcaed9694a0a80ccf3728cb615a733` |
| [Traktor Kontrol S4 MK3/](Traktor%20Kontrol%20S4%20MK3/) | 80980 | Traktor Kontrol S4 MK3 | 2019-02-23 | Mapping and definition; screens and haptics not supported | `Devices/Traktor Kontrol S4 MK3.zip` | `f00463f35756cd5cfb6fce000b5cdae8a757287443695ff1351b9de673e473ad` |

Contents:

- `force-Platinum/force-Numark Mixtrack Platinum.xml` is a MIDI `<device name="NMMXTPL">`
  definition with no mapper. The `force-` prefix appears to be how the add-on replaces the
  built-in definition for the same controller (VID/PID `0x15E4`/`0x003A`). That is `Inference`
  from the file name and the catalog description, not a tested loader rule.
- `Traktor Kontrol S4 MK3/` holds a HID `<device name="TRAKTORS4MK3">` definition and a paired
  `<mapper device="TRAKTORS4MK3">` (`Traktor Kontrol S4 MK3 mapping.xml`).

Copied 2026-09-22 on installed VirtualDJ bundle `18.0.9644`. Evidence tier: Tier 2 vendor example
(see [Evidence Standards](../../../docs/Evidence%20Standards.md)). These are authoritative for
definition and mapper format vocabulary, but not proof that a verb behaves as written. Do not hand-edit them.
