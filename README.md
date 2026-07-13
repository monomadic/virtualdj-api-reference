# VirtualDJ API Reference

Community-maintained reference for VirtualDJ skinning, pad pages, and VDJScript.
VirtualDJ does not publish a comprehensive developer reference; this repo fills that gap.

## What is here

- **`docs/`** — Markdown documentation: VDJScript verb reference, skin SDK, waveform elements, pad-page schema, effects, options, filter syntax, mapper format, application internals
- **`examples/Pads/`** — focused pad page XML examples for ColorFX, samplers, cues, transport, reference patterns, and copied built-in pad pages; see [examples/Pads/README.md](examples/Pads/README.md)
- **`examples/Skins/`** — skin examples, copied built-in skins, and build-system demos; GraveRaver is intentionally minimal and only demonstrates the XInclude workflow
- **`examples/Mappers/`** — real working controller/keyboard mapper XML copied from a local install; ground truth for the mapper format
- **`examples/Samplerbanks/`** — sampler-bank XML copied from the app bundle (a third XML format alongside skins and pads)
- **`tests/`** — reproducible documentation test harnesses, including pad-page XML fixtures

## Where to start

| Goal | File |
| --- | --- |
| Pick the next active maintenance task | [TODO.md](TODO.md) |
| Route a topic to the right docs and fixtures | [INDEX.yml](INDEX.yml) |
| Understand the repo structure and source labeling | [docs/README.md](docs/README.md) |
| Pick the right VDJScript verb or pattern | [docs/VirtualDJ Reference.md](docs/VirtualDJ%20Reference.md) |
| Look up a specific verb | [docs/VDJScript Verbs.md](docs/VDJScript%20Verbs.md) |
| Check official verb coverage | [docs/Official VDJScript Coverage Audit.md](docs/Official%20VDJScript%20Coverage%20Audit.md) |
| Choose the next completeness pass | [docs/Completeness Roadmap.md](docs/Completeness%20Roadmap.md) |
| Choose or maintain a pad page | [examples/Pads/README.md](examples/Pads/README.md) |
| Look up the pad-page XML format | [docs/Pad Page XML.md](docs/Pad%20Page%20XML.md) |
| Build skin waveforms | [docs/Skin Waveforms.md](docs/Skin%20Waveforms.md) |
| Check skin/pad XML doc coverage | [docs/Skin XML Inventory.md](docs/Skin%20XML%20Inventory.md) (generated; `just inventory`) |
| Look up verbs programmatically | [docs/vdjscript-verb-index.json](docs/vdjscript-verb-index.json) (generated; `just verb-index`) |
| Validate skin/mapper XML | `just lint-skins [paths]` · `just lint-mappers [paths]` · [tools/README.md](tools/README.md) |
| Run or update a test harness | [tests/README.md](tests/README.md) |
| Build or study a skin | [docs/Skin SDK.md](docs/Skin%20SDK.md) · [docs/Skin Runtime Findings.md](docs/Skin%20Runtime%20Findings.md) · [examples/Skins/README.md](examples/Skins/README.md) · [examples/Skins/ModularSkeleton/](examples/Skins/ModularSkeleton/) |
| Work with effects | [docs/Effects Usage.md](docs/Effects%20Usage.md) · [docs/Native Effects.md](docs/Native%20Effects.md) |
| Map a controller or keyboard | [docs/Mapper XML.md](docs/Mapper%20XML.md) |
| Understand macOS paths and databases | [docs/Application Internals.md](docs/Application%20Internals.md) |
| Inspect or create `.vdjstems` sidecars | [docs/Stem File Format.md](docs/Stem%20File%20Format.md) |

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

- Current official coverage and local-test gap counts are tracked in [docs/Official VDJScript Coverage Audit.md](docs/Official%20VDJScript%20Coverage%20Audit.md).
- Active next tasks are tracked in [TODO.md](TODO.md); the broader evidence backlog remains in [docs/Completeness Roadmap.md](docs/Completeness%20Roadmap.md).
- Skin SDK coverage is broad; the waveform element family is documented in `docs/Skin Waveforms.md` and remaining element gaps are tracked mechanically in the generated `docs/Skin XML Inventory.md`
- Controller mapper XML format: rewritten around the real `<map value="">` + device-definition split, with real working mappers in `examples/Mappers/Local/`; custom device-definition XML is official-doc-derived and not yet load-tested locally

Contributions and corrections welcome.
