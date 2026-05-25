# VirtualDJ Skins

This folder contains local skin references, build-system demos, and copied built-in VirtualDJ skins.

## What To Use

| Path | Status | Notes |
| --- | --- | --- |
| [ModularSkeleton/](ModularSkeleton/) | Canonical | Minimal modular skin scaffold. Use this for build-time XInclude, class defines, named colors, and installable flattened output. |
| [Built-In/](Built-In/) | Built-in | App-bundle desktop, Lite, Remote, and small plugin UI skins copied from VirtualDJ `8.5.9307` / bundle `18.0.9336`. Use as semi-official executable examples. |
| [SDK Example - Custom Browser Skin/](SDK%20Example%20-%20Custom%20Browser%20Skin/) | Official example | Local copy of a focused SDK-style browser skin example. |
| [GraveRaver/](GraveRaver/) | Build demo | Intentionally minimal XInclude build demo, not a polished skin design reference. |

## Maintenance Notes

- Do not hand-edit files under [Built-In/](Built-In/). Refresh them from the app bundle and review diffs when VirtualDJ is updated.
- Built-in skin XML is preserved as shipped and may not pass generic XML linters because the VirtualDJ skin parser accepts VDJScript-heavy attributes and raw `&` / `&&` forms.
- Use [ModularSkeleton/](ModularSkeleton/) when creating new local skin examples.
