# VirtualDJ API Reference

Community-maintained reference for VirtualDJ skinning, pad pages, and VDJScript.
VirtualDJ does not publish a comprehensive developer reference; this repo fills that gap.

## What is here

- **`Reference/`** — Markdown documentation: VDJScript verb reference, skin SDK, waveform elements, pad-page schema, effects, options, filter syntax, mapper format, application internals
- **`xml/Pads/`** — focused pad page XML examples for ColorFX, samplers, cues, transport, reference patterns, and copied built-in pad pages; see [xml/Pads/README.md](xml/Pads/README.md)
- **`xml/Skins/`** — skin examples, copied built-in skins, and build-system demos; GraveRaver is intentionally minimal and only demonstrates the XInclude workflow
- **`xml/Mappers/`** — real working controller/keyboard mapper XML copied from a local install; ground truth for the mapper format
- **`xml/Samplerbanks/`** — sampler-bank XML copied from the app bundle (a third XML format alongside skins and pads)
- **`tests/`** — reproducible documentation test harnesses, including pad-page XML fixtures

## Where to start

| Goal | File |
| --- | --- |
| Pick the next active maintenance task | [TODO.md](TODO.md) |
| Route a topic to the right docs and fixtures | [INDEX.yml](INDEX.yml) |
| Understand the repo structure and source labeling | [Reference/README.md](Reference/README.md) |
| Pick the right VDJScript verb or pattern | [Reference/VirtualDJ Reference.md](Reference/VirtualDJ%20Reference.md) |
| Look up a specific verb | [Reference/VDJScript Verbs.md](Reference/VDJScript%20Verbs.md) |
| Check official verb coverage | [Reference/Official VDJScript Coverage Audit.md](Reference/Official%20VDJScript%20Coverage%20Audit.md) |
| Choose the next completeness pass | [Reference/Completeness Roadmap.md](Reference/Completeness%20Roadmap.md) |
| Choose or maintain a pad page | [xml/Pads/README.md](xml/Pads/README.md) |
| Look up the pad-page XML format | [Reference/Pad Page XML.md](Reference/Pad%20Page%20XML.md) |
| Build skin waveforms | [Reference/Skin Waveforms.md](Reference/Skin%20Waveforms.md) |
| Check skin/pad XML doc coverage | [Reference/Skin XML Inventory.md](Reference/Skin%20XML%20Inventory.md) (generated; `just inventory`) |
| Run or update a test harness | [tests/README.md](tests/README.md) |
| Build or study a skin | [Reference/Skin SDK.md](Reference/Skin%20SDK.md) · [Reference/Skin Runtime Findings.md](Reference/Skin%20Runtime%20Findings.md) · [xml/Skins/README.md](xml/Skins/README.md) · [xml/Skins/ModularSkeleton/](xml/Skins/ModularSkeleton/) |
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
| `Built-in app resource` | Command name, description, or UI catalog entry observed in non-skin/non-pad app resources |
| `Binary compiled table` | Structured command metadata observed in compiled executable tables |
| `Binary symbol table` | Demangled implementation symbols observed in the VirtualDJ executable |
| `Binary string-table` | Command-looking string observed in the VirtualDJ executable; discovery only |
| `Local test` | Reproduced in VirtualDJ locally |
| `Inference` | Conclusion drawn from the above sources |

Unlabeled files are raw material not yet normalized to this standard.

## Status

- Current official coverage and local-test gap counts are tracked in [Reference/Official VDJScript Coverage Audit.md](Reference/Official%20VDJScript%20Coverage%20Audit.md).
- Active next tasks are tracked in [TODO.md](TODO.md); the broader evidence backlog remains in [Reference/Completeness Roadmap.md](Reference/Completeness%20Roadmap.md).
- Skin SDK coverage is broad; the waveform element family is documented in `Reference/Skin Waveforms.md` and remaining element gaps are tracked mechanically in the generated `Reference/Skin XML Inventory.md`
- Controller mapper XML format: rewritten around the real `<map value="">` + device-definition split, with real working mappers in `xml/Mappers/Local/`; custom device-definition XML is official-doc-derived and not yet load-tested locally

Contributions and corrections welcome.
