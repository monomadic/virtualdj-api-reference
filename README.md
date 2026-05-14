# VirtualDJ API Reference

Community-maintained reference for VirtualDJ skinning, pad pages, and VDJScript.
VirtualDJ does not publish a comprehensive developer reference; this repo fills that gap.

## What is here

- **`Reference/`** — Markdown documentation: VDJScript verb reference, skin SDK, effects, options, filter syntax, application internals
- **`Pads/`** — focused pad page XML examples for ColorFX, samplers, cues, transport, and reference patterns
- **`Skins/`** — skin examples and build-system demos; GraveRaver is intentionally minimal and only demonstrates the XInclude workflow

## Where to start

| Goal | File |
| --- | --- |
| Understand the repo structure and source labeling | [Reference/README.md](Reference/README.md) |
| Pick the right VDJScript verb or pattern | [Reference/VirtualDJ Reference.md](Reference/VirtualDJ%20Reference.md) |
| Look up a specific verb | [Reference/VDJScript Verbs.md](Reference/VDJScript%20Verbs.md) |
| Check official verb coverage | [Reference/Official VDJScript Coverage Audit.md](Reference/Official%20VDJScript%20Coverage%20Audit.md) |
| Build a skin | [Reference/Skin SDK.md](Reference/Skin%20SDK.md) · [Skins/ModularSkeleton/](Skins/ModularSkeleton/) |
| Work with effects | [Reference/Effects Usage.md](Reference/Effects%20Usage.md) · [Reference/Native Effects.md](Reference/Native%20Effects.md) |
| Map a controller or keyboard | [Reference/Mapper XML.md](Reference/Mapper%20XML.md) |
| Understand macOS paths and databases | [Reference/Application Internals.md](Reference/Application%20Internals.md) |

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
| `Local test` | Reproduced in VirtualDJ locally |
| `Inference` | Conclusion drawn from the above sources |

Unlabeled files are raw material not yet normalized to this standard.

## Status

- VDJScript verb reference covers ~865 of 989 official verbs (~87%); EQ, `get_browsed_*`, `cue_*`, FX routing, mixer-bypass, browser, automix, and getter clusters added in recent passes
- Skin SDK coverage is broad but `<visual type="...">` types not yet fully documented
- Controller mapper XML format: initial reference added in `Reference/Mapper XML.md`

Contributions and corrections welcome.
