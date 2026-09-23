# Unknown attribute before or after a valid attribute

Local test on 2026-09-24, desktop build 18.0.9644, arm64. Text `color="#00FF00"`
and button `visibility="off"` each have a baseline and an unknown attribute before
or after them. Both `zzinvalidalpha` and `zzinvalidbeta` are tested; nonsense color
values are red and nonsense visibility values are `on`, opposing the valid value.

**All text remained green and all visibility-gated buttons stayed hidden in both
reloads.** An unconditional cyan button remained visible. Thus these unknown
attribute names did not stop the valid attribute being applied, in either order.
This tests distinct names in well-formed XML, not malformed XML or duplicate keys.

[Round 1](round-1.png) and [round 2](round-2.png) are live CUA screenshots of the
synthetic fixture, with reversed rows and fresh labels in the second reload.
[result-9644.json](result-9644.json) records observations and evidence hashes;
[run-9644.jsonl](run-9644.jsonl) contains HTTP write intents/readbacks and cleanup.
The original skin was restored between and after rounds, empty/stopped decks were
verified, and the byte-checked fixture installation was removed.

`probe.py` reuses the explicit-step runner from the sibling
[element fixture](../element-validity-probe/README.md). Preserve existing captures
before another run. Synthetic nonsense attributes are excluded from the inventory.
