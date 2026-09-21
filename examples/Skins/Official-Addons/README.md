# Atomix-Published Skin Add-ons

Skins that Atomix publishes through the VirtualDJ add-on catalog rather than shipping in the
app bundle, copied from this machine's VirtualDJ install. Mostly controller-specific layouts
and screen skins for controllers with built-in displays, which the bundle's own skins do not cover.

## Provenance

Authorship comes from the app's own add-on catalog, `https://virtualdj.com/live/addons.php?os=mac`
(the endpoint the app's Extensions browser reads), fetched 2026-09-21. The catalog gives
`author: "Atomix Productions"` for every entry below. The public listing page
(`https://virtualdj.com/plugins/?addonid=<id>`) credits the same add-ons to the site's
"Development Team" account.

Each folder is the unzipped contents of the zip VirtualDJ installed. None of these files was
downloaded directly: `download.virtualdj.com` answers `AccessDenied` without the app's
login-signed URL, so every copy here came through the app's own installer. The zip hash lets a
later copy be compared with this one.

| Folder | Add-on id | Catalog name | Catalog `lastdate` | Installed zip (under `~/Library/Application Support/VirtualDJ/`) | Zip SHA-256 | `<skin author=>` in XML |
| --- | --- | --- | --- | --- | --- | --- |
| [American Audio VMS5/](American%20Audio%20VMS5/) | 81741 | American Audio VMS5 | 2024-06-18 | `Skins/American Audio VMS5.zip` | `ec7c9ff97d5d8d707b42374da88731d70b4cc520741568498cf1075172a599d2` | `Atomix Productions` |
| [Denon Prime4 Screen/](Denon%20Prime4%20Screen/) | 81106 | Denon DJ Prime 4 Screen | 2025-12-21 | `Skins/Denon Prime4 Screen.zip` | `763c68f1ea07bd98619dc0b43fb81899e2b28f6f1c66aad98606af569b626b66` | `Atomix Productions` |
| [Denon PRIMEGO Screen/](Denon%20PRIMEGO%20Screen/) | 81540 | Denon DJ Prime GO Screen | 2025-12-21 | `Skins/Denon PRIMEGO Screen.zip` | `86709953ad9392fa00b0749a3f2456c87c5d5e400f65171ce785c74562cc39f1` | none |
| [Denon SCLIVE4 Screen/](Denon%20SCLIVE4%20Screen/) | 81554 | Denon DJ SC Live 4 Screen | 2025-12-21 | `Skins/Denon SCLIVE4 Screen.zip` | `d54839e183b30e218ccb20ad2620a5d05c3b3153a8946e8fc8951cb918949cd6` | none |
| [MIDI36/](MIDI36/) | 81827 | MIDI36 | 2025-03-13 | `Skins/MIDI36.zip` | `122b432e806568621270c38af28cbdece16b0276d7e94bd813aeec183bce191d` | `Atomix Productions` |
| [Remote 8 Default Skin/](Remote%208%20Default%20Skin/) | 80266 | Remote 8 Default Skin | 2015-06-11 | `RemoteSkins/Remote 8 Default Skin.zip` (a byte-identical copy also sits in `Skins/`) | `b4be08842e0da2da81efa666eddc15e41967484cab0ea18c849b1ad741eeb73f` | none |
| [American Audio 10MXR v8/](American%20Audio%2010MXR%20v8/) | 80495 | American Audio 10MXR v8 | 2016-12-01 | `Skins/American Audio 10MXR v8.zip` | `8c8a6e264accdd805dc72fcbc3b2f310d3b04a9e383766863e73ef81e846f817` | `Atomix Productions` |
| [American Audio 14MXR v8/](American%20Audio%2014MXR%20v8/) | 80494 | American Audio 14MXR v8 | 2016-12-01 | `Skins/American Audio 14MXR v8.zip` | `27a67a06440be8740d1a869867e01100ea47c93ccb94b8945f219637cfb0f37c` | `Atomix Productions` |
| [American Audio 19MXR v8/](American%20Audio%2019MXR%20v8/) | 80496 | American Audio 19MXR v8 | 2016-12-01 | `Skins/American Audio 19MXR v8.zip` | `212c30f29f332de9162b3cf5b0f054ae4ccd579e3da96ed0ea909bdf35c12d60` | `Atomix Productions` |
| [American Audio VMS2/](American%20Audio%20VMS2/) | 80286 | American Audio VMS2 | 2015-07-17 | `Skins/American Audio VMS2.zip` | `b549c210f3c6098c1e15a1f244e0a7e53882a78d47c59fcde720cc865bf298ec` | `Atomix Productions` |
| [Denon Prime2 Screen/](Denon%20Prime2%20Screen/) | 81109 | Denon DJ Prime 2 Screen | 2025-12-21 | `Skins/Denon Prime2 Screen.zip` | `0f8893d48e0cbf17f62108ca075cc719852f00056db39baa093fb6b8ecae5e26` | none |
| [Denon SC5000 Screen/](Denon%20SC5000%20Screen/) | 81108 | Denon DJ SC5000 Screen | 2025-12-21 | `Skins/Denon SC5000 Screen.zip` | `adee11ea0dd8a68fb567bf16eb3cd0ef34655eb1f11157b1b3be463a77f6f2b8` | none |
| [Denon SCLIVE2 Screen/](Denon%20SCLIVE2%20Screen/) | 81555 | Denon DJ SC Live 2 Screen | 2025-12-21 | `Skins/Denon SCLIVE2 Screen.zip` | `4663856cf7412c49ccc527b30d89f3945d0ba7a2f76fd498f0fa3728680110c7` | none |
| [Gemini GMX/](Gemini%20GMX/) | 81742 | Gemini GMX | 2024-06-18 | `Skins/Gemini GMX.zip` | `f203f2556e6f4aafacb5d2321e4dc72cf7325a0e472e0c2adb9c3935964663ea` | `Atomix Productions` |
| [Stanton DJC4/](Stanton%20DJC4/) | 81743 | Stanton DJC4 | 2024-06-18 | `Skins/Stanton DJC4.zip` | `03ddab39acea2104db44e27311b0a22aff91b2d2113bcbf8e835e304afe62786` | `Atomix Productions` |
| [Hercules RMX2/](Hercules%20RMX2/) | 81744 | Hercules RMX2 | 2024-06-18 | `Skins/Hercules RMX2.zip` | `118fd6a843dde692df55078f638732ef637452b0c5e7f9f9d3a6fd02e3f57181` | `Atomix Productions` |
| [Numark IDJLIVE II/](Numark%20IDJLIVE%20II/) | 80046 | Numark IDJLIVE II | 2014-08-29 | `Skins/Numark IDJLIVE II.zip` | `c16916da2ddea58cb100d6bfdd8110d7e6a4e7d0aacb9fc9647e963634ba5a38` | `Atomix Productions` |
| [Numark Mixstream Pro Screen/](Numark%20Mixstream%20Pro%20Screen/) | 81430 | Numark Mixstream Pro Screen | 2025-12-21 | `Skins/Numark Mixstream Pro Screen.zip` | `f7bd5cee1842256705930bf7d08e34bf3815a9759cf303332d506ea624da327e` | none |
| [Numark Party Mix Pro/](Numark%20Party%20Mix%20Pro/) | 80658 | Numark Party Mix Pro | 2017-09-19 | `Skins/Numark Party Mix Pro.zip` | `ff4439099a514c3ec7f3fb5b147d535918d2cf70fd464217aa59b80fae80fc2b` | `Atomix Productions` |
| [PartyMix/](PartyMix/) | 80430 | PartyMix | 2016-08-06 | `Skins/PartyMix.zip` | `fd6babf5677933334965558b4664e951a772d0d9049a52419609a6b718b48ebe` | `Atomix Productions` |
| [Pioneer DDJ-Ergo v8/](Pioneer%20DDJ-Ergo%20v8/) | 80248 | Pioneer DDJ-Ergo v8 | 2015-05-10 | `Skins/Pioneer DDJ-Ergo v8.zip` | `cf521d2dc174751f4b9b913f0322ea5b7d99b8fad912daa0c4b2659273084bf5` | `Atomix Productions` |
| [Pioneer DDJ-RZX Screens/](Pioneer%20DDJ-RZX%20Screens/) | 80833 | Pioneer DDJ-RZX Screens | 2026-01-17 | `Skins/Pioneer DDJ-RZX Screens.zip` | `f6f26fd8da32b246a9396e1a921129023c20360768e2963be236aa987f234a05` | `Atomix Productions` |
| [Pioneer DDJ-WeGO V8/](Pioneer%20DDJ-WeGO%20V8/) | 80152 | Pioneer DDJ-WeGO V8 | 2014-11-21 | `Skins/Pioneer DDJ-WeGO V8.zip` | `f67b4b2b46036b192694dbe17c7df5e0c4321cedd5adf45b4e997a1c47bf5e9c` | `Atomix Productions` |
| [Pioneer DDJ-WeGO2 V8/](Pioneer%20DDJ-WeGO2%20V8/) | 80153 | Pioneer DDJ-WeGO2 V8 | 2014-11-21 | `Skins/Pioneer DDJ-WeGO2 V8.zip` | `2d8dd3c817c4cc3cbcf3e267a5897449346f5b6dd3c63410d70b2d659f8e2d0e` | `Atomix Productions` |
| [Pioneer XDJ-R1 v8/](Pioneer%20XDJ-R1%20v8/) | 80369 | Pioneer XDJ-R1 | 2016-02-19 | `Skins/Pioneer XDJ-R1 v8.zip` | `fbc530ba03e48ce6af4c051d55299bb2417ecee6c9d14280de8d8c30ce400879` | `Atomix Productions` |
| [Reloop Touch Skin/](Reloop%20Touch%20Skin/) | 80685 | Reloop Touch Skin | 2025-12-21 | `Skins/Reloop Touch Skin.zip` | `f03a8493612ef4cbcae5e0b7002e7d087716a635c630355bcfd7cadfb13d7a69` | none |
| [skin2018/](skin2018/) | 81676 | VirtualDJ 8 Old Default | 2023-11-21 | `Skins/skin2018.zip` | `a84c142fd2b17f291bd3bc9824e337ae8d67dc4e939f67a23a1a9d4924726acc` | `Atomix Productions` |
| [Traktor Kontrol D2 Screen/](Traktor%20Kontrol%20D2%20Screen/) | 81420 | Traktor Kontrol D2 Screen | 2025-12-21 | `Skins/Traktor Kontrol D2 Screen.zip` | `93fbbecc9dc507b6017f7c16000bbbbc040533f7806b4329601cf7f7c7526228` | `Atomix Productions` |
| [Traktor Kontrol S5 Screens/](Traktor%20Kontrol%20S5%20Screens/) | 81890 | Traktor Kontrol S5 Screens | 2025-12-21 | `Skins/Traktor Kontrol S5 Screens.zip` | `b9b736ee85695e41cc90543f5ff9984cd7f3f8f034c16c5bf2ae07bd6a94a091` | `Atomix Productions` |
| [Traktor Kontrol S8 Screens/](Traktor%20Kontrol%20S8%20Screens/) | 81399 | Traktor Kontrol S8 Screens | 2025-12-21 | `Skins/Traktor Kontrol S8 Screens.zip` | `fecdfa4acefc97bb9686ebb53202c25681b8fdd64f451fe16c8fedb753a8393a` | `Atomix Productions` |
| [Traktor X1 MK3 Screens/](Traktor%20X1%20MK3%20Screens/) | 81710 | Traktor X1 MK3 Screens | 2024-02-26 | `Skins/Traktor X1 MK3 Screens.zip` | `7763ebb5c3eb01e0575636c838c5d568da9b3090b9eb6cd82a3f3282b62beac0` | `Atomix Productions` |
| [Traktor Z1 MK2 Screens/](Traktor%20Z1%20MK2%20Screens/) | 81793 | Traktor Z1 MK2 Screens | 2024-11-25 | `Skins/Traktor Z1 MK2 Screens.zip` | `969805cdac764988883690b5201ac4528188319db567a6aa777ab1e9f5fcd6cb` | `Atomix Productions` |

Copied 2026-09-21 on installed VirtualDJ bundle `18.0.9644`. The first six rows were already installed before that day. The rest were installed through the Extensions browser on 2026-09-21 or 2026-09-22 and copied within minutes of installing, so they are fresh installs. Gemini GMX and Stanton DJC4 went in on 2026-09-22. The catalog describes both as "auto-installed when device is first connected". The add-ons are versioned by their
catalog `lastdate`, not by app build.

Evidence tier: `Published skin` (Tier 2, see [Evidence Standards](../../../docs/Evidence%20Standards.md)).
These are Atomix-written executable examples, just as the [Built-In/](../Built-In/) skins are,
but a file loading without complaint is not proof that any verb in it works.

## Notes

- The three Denon screen skins and the controller manifest (`tests/controllers-manifests/`, `skinName` / `skinAddonId`)
  refer to the same add-ons, and VirtualDJ fetches them when the matching controller connects.
  They set `hidden="true"`, so they are not offered in the ordinary skin picker.
- `Remote 8 Default Skin` is the 2015 VirtualDJ 8 Remote skin set (`skinP169`, `skinP32`,
  `skinT1610`, `skinT43`, `skin7T`). It predates the current Remote skins in
  [Built-In/Remote/](../Built-In/Remote/). [Application Internals](../../../docs/Application%20Internals.md)
  already mentions these file names.
- `American Audio VMS5/skin.xml` declares `name="American Audio VMS4"` even though its comment names the VMS5.
  That is kept as shipped.
- Do not hand-edit these copies. To refresh one, reinstall it through VirtualDJ's Extensions browser, then
  unzip it over the folder and update the hash and `lastdate` above.
- `skin2018/` is the catalog's "VirtualDJ 8 Old Default": the 2018-era default skin in 2-, 4- and 6-deck variants.
  The folder keeps the installed zip's name so it can be traced back to that file.
- Every Atomix skin add-on in the catalog as fetched on 2026-09-21 is copied here.
  The controller definitions are in [Mappers/Official-Addons/](../../Mappers/Official-Addons/README.md) and the sampler banks in
  [Samplerbanks/Official-Addons/](../../Samplerbanks/Official-Addons/README.md). The catalog's Atomix effect entries are compiled plugins
  or listings of built-in effects, so they have no XML to copy.
- Deliberately excluded: `Photon.zip`. Its XML says `author="Atomix Productions"` and the controller
  manifest auto-installs it, but the catalog credits add-on 81121 to `Rune (DJ-In-Norway)`. Also
  excluded is `Hercules RMX2 BLACK.zip`, a community variant; the Atomix add-on is `Hercules RMX2` (81744), copied above.
  `Numark N4.zip` (80696) is by `OldSkoolScouse`, not Atomix.
