# Attribute validity canary

Local test: 2026-09-24, VirtualDJ 18.0.9644, arm64, desktop skin.

See [the report](../../../docs/Skin%20Element%20Validity.md#attributes-and-script-valued-attributes)
for interpretation. [result-9644.json](result-9644.json) records the observations,
fixture and screenshot hashes; [run-9644.jsonl](run-9644.jsonl) contains the HTTP
intents, independent readbacks and verified restoration.

[Round 1](round-1.png) and [round 2](round-2.png) were captured live through CUA.
Rows reverse and revision labels change between reloads in the same process.
The original skin was restored between and after rounds, decks remained empty
and stopped, and the test installation was removed after byte verification.
No button actions were clicked, no media loaded, and no probe variables changed.

Visible in both rounds: baseline, unknown-alpha, unknown-beta, visibility-on, misspelled-visibility.

Not visible in both rounds: visibility-off, invalid-value-alpha, invalid-value-beta.

`probe.py` reuses the explicit-step runner documented in the sibling
[element fixture](../element-validity-probe/README.md). Preserve existing captures;
the begin step refuses an existing journal/state. These are synthetic negative
controls, deliberately excluded from the XML vocabulary inventory.
