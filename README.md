# VirtualDJ API Reference

Community-maintained reference for VirtualDJ skinning, pad pages, and VDJScript.
VirtualDJ does not publish a comprehensive developer reference; this repo fills that gap.

## What is here

- **`Reference/`** — Markdown documentation: VDJScript verb reference, skin SDK, effects, options, filter syntax, application internals
- **`Pads/`** — focused pad page XML examples for ColorFX, samplers, cues, transport, reference patterns, and copied built-in pad pages; see [Pads/README.md](Pads/README.md)
- **`Skins/`** — skin examples, copied built-in skins, and build-system demos; GraveRaver is intentionally minimal and only demonstrates the XInclude workflow
- **`Test/`** — reproducible documentation test harnesses, including pad-page XML fixtures

## Where to start

| Goal | File |
| --- | --- |
| Understand the repo structure and source labeling | [Reference/README.md](Reference/README.md) |
| Pick the right VDJScript verb or pattern | [Reference/VirtualDJ Reference.md](Reference/VirtualDJ%20Reference.md) |
| Look up a specific verb | [Reference/VDJScript Verbs.md](Reference/VDJScript%20Verbs.md) |
| Check official verb coverage | [Reference/Official VDJScript Coverage Audit.md](Reference/Official%20VDJScript%20Coverage%20Audit.md) |
| Choose or maintain a pad page | [Pads/README.md](Pads/README.md) |
| Run or update a test harness | [Test/README.md](Test/README.md) |
| Build or study a skin | [Reference/Skin SDK.md](Reference/Skin%20SDK.md) · [Reference/Skin Runtime Findings.md](Reference/Skin%20Runtime%20Findings.md) · [Skins/README.md](Skins/README.md) · [Skins/ModularSkeleton/](Skins/ModularSkeleton/) |
| Work with effects | [Reference/Effects Usage.md](Reference/Effects%20Usage.md) · [Reference/Native Effects.md](Reference/Native%20Effects.md) |
| Map a controller or keyboard | [Reference/Mapper XML.md](Reference/Mapper%20XML.md) |
| Understand macOS paths and databases | [Reference/Application Internals.md](Reference/Application%20Internals.md) |
| Inspect or create `.vdjstems` sidecars | [Reference/Stem File Format.md](Reference/Stem%20File%20Format.md) |

## Agent Entry Point

`AGENTS.md` is intentionally retained for Claude, Codex, and other coding
agents that look for that filename. This `README.md` is the human-facing
overview; `AGENTS.md` keeps the operational shortcuts and repo-specific guardrails.

## Reliability

Every fact in the reference docs is labeled by source:

| Label | Meaning |
| --- | --- |
| `Official` | Current VirtualDJ manual or VDJPedia |
| `Official forum` | Post by VirtualDJ staff, CTO, or support |
| `Community` | Non-staff forum guidance |
| `Published skin` | Observed in a working public skin |
| `Built-in skin` | Observed in skin XML shipped inside the VirtualDJ app bundle |
| `Published pad page` | Observed in a working public pad page |
| `Built-in pad page` | Observed in pad-page XML shipped inside the VirtualDJ app bundle |
| `Local test` | Reproduced in VirtualDJ locally |
| `Inference` | Conclusion drawn from the above sources |

Unlabeled files are raw material not yet normalized to this standard.

## Status

- VDJScript reference has official-name parity with the appendix: 991/991 official verb/alias names are present, missing names are 0, and the compact official remainder is empty. The remaining formal gap is 20 official names still marked `Needs local test`: sparse helpers such as `deck_has_error` and `system`; optional deck/controller setup for `dualdeckmode_decks`; and hardware-specific controller helpers.
- Skin SDK coverage is broad but `<visual type="...">` types not yet fully documented
- Controller mapper XML format: initial reference added in `Reference/Mapper XML.md`

Contributions and corrections welcome.
