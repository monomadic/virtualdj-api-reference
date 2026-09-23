# Valid and unknown siblings inside a valid container

Local test on 2026-09-24, desktop build 18.0.9644, arm64. Each test container
holds a valid textzone and a well-formed self-closing unknown tag. The baseline
panel holds just the textzone. Both `zzinvalidalpha` and `zzinvalidbeta` were
tested before and after the valid child inside panels. Group controls place
alpha before and beta after the valid child.

**Every valid child rendered in both reloads.** The unknown sibling did not
suppress the whole container or prevent a later valid sibling from rendering
in these cases. This does not test malformed XML or every skin surface.

[Round 1](round-1.png) and [round 2](round-2.png) are live CUA screenshots of the
synthetic fixture. The second reload reverses the rows and changes their labels.
[result-9644.json](result-9644.json) retains observations and evidence hashes;
[run-9644.jsonl](run-9644.jsonl) records HTTP write intents and independent
readbacks. The original skin was restored between rounds and after the test,
empty/stopped decks were verified, and the byte-checked installation was removed.

`probe.py` uses the explicit-step runner documented in the sibling
[element validity fixture](../element-validity-probe/README.md). Preserve existing
captures before another run; the runner refuses an existing journal/state file.
These synthetic nonsense tags are excluded from the XML vocabulary inventory.
