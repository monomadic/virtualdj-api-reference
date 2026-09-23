# Desktop element nesting canary

Local test: 2026-09-24, VirtualDJ build 18.0.9644, arm64. See
[the mechanism report](../../../docs/Skin%20Element%20Validity.md) for interpretation.

[result-9644.json](result-9644.json) records observations and hashes.
[Round 1](round-1.png) and [round 2](round-2.png) are live CUA screenshots of the
synthetic fixture. The second revision reverses rows and changes all child labels.
Both show the bare, panel, group and pannel child; neither shows children under
the two nonsense wrappers or the valid button/textzone leaves. The leaves' own
red rectangle/yellow text render. This is a container discriminator, not a global
element validator. A negative does not identify why the child did not render.

[run-9644.jsonl](run-9644.jsonl) journals HTTP intents/readbacks and cleanup.
The original skin was restored between rounds and after the test, with its
identity and empty/stopped decks checked. No media or probe variables were
changed. The synthetic installation was removed only after byte verification.
These checks do not claim every application setting was compared.

The earlier [initial attempt](run-9644-initial.jsonl) reached skin readback but
the CUA window was the custom Now Playing plugin; it supplies no rendering
evidence. Its original skin was restored and fixture uninstalled before retry.
The custom plugin window was then closed, allowing CUA to observe the main skin.
The listener's executable was separately checked against the installed app;
the other running 9246 instance is not the source of these screenshots.

`probe.py` is the explicit-step reproducer: `begin`, `install`, `load`,
`restore`, then `install --round 2`, `load --round 2`, `restore`,
`uninstall --round 2`. Capture the live main window after each `load` and before
`restore`. It only permits the recorded build with empty stopped decks at begin.
The script refuses to start over an existing journal/state file. Preserve those
as a dated prior capture and use a fresh checkout/capture destination for another
run; do not overwrite confirmed evidence. The state file in `/tmp` retains the
original skin identity for restoration. No uncertain write is retried.

The script shares the PNG encoder from the sibling conditional-child fixture.
The XML revisions are synthetic project-authored inputs, never vendor evidence.
