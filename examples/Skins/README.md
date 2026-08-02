# VirtualDJ Skins

This folder contains local skin references, build-system demos, and copied built-in VirtualDJ skins.

## What To Use

| Path | Status | Notes |
| --- | --- | --- |
| [Built-In/](Built-In/) | Built-in (official) | App-bundle desktop, Lite, Remote, and small plugin UI skins copied from VirtualDJ `8.5.9307` / bundle `18.0.9336`. Use as semi-official executable examples. |
| [SDK Example - Custom Browser Skin/](SDK%20Example%20-%20Custom%20Browser%20Skin/) | Official example | Atomix-authored (`author="Atomix Productions"` in the file) SDK-style browser skin example. |
| [ModularSkeleton/](ModularSkeleton/) | Canonical, **unofficial** | Minimal modular skin scaffold authored for this repo, not vendor content. Use this for build-time XInclude, class defines, named colors, and installable flattened output. Kept in place (not quarantined) because it is heavily referenced across the docs — see below. |
| [GraveRaver/](GraveRaver/) | Build demo, **unofficial** | Intentionally minimal XInclude build demo authored for this repo, not a polished skin design reference and not vendor content. Kept in place (not quarantined) because it is heavily referenced across the docs — see below. |

`ModularSkeleton/` and `GraveRaver/` are project-authored, not Atomix/vendor-official — do not cite either as evidence of shipped VirtualDJ behavior, only as build-pattern demonstrations. They are referenced from `README.md`, `AGENTS.md`, `docs/Resources.md`, `docs/VirtualDJ Reference.md`, `docs/Skin SDK.md`, and (GraveRaver only) `docs/Skin Runtime Findings.md`, which is why they stay in place rather than moving to a Quarantine folder like the personal Mappers/Pads examples.

## Maintenance Notes

- Do not hand-edit files under [Built-In/](Built-In/). Refresh them from the app bundle and review diffs when VirtualDJ is updated.
- Built-in skin XML is preserved as shipped and may not pass generic XML linters because the VirtualDJ skin parser accepts VDJScript-heavy attributes and raw `&` / `&&` forms.
- Use [ModularSkeleton/](ModularSkeleton/) when creating new local skin examples.
