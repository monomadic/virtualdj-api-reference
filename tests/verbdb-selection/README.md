# Verb-selection regression fixtures

Miniature stores for the two ways `next-incomplete` went quiet, kept so a future
selector rewrite cannot reintroduce either. Run by `python3 tools/verbdb.py check`.

Each fixture is `{"store": {name: record}, "contract_names": [...]}`, where
`contract_names` stands in for the names carrying a row in
`tests/verb-return-types.json` or `tests/verb-arg-forms.json`.

| Fixture | Locks |
| --- | --- |
| `blocked-not-needs-test.json` | Records that are `blocked` without being `needs_test` must not be subtracted out of the backlog; the old formula returned a negative count for this store. |
| `audit-pool-exhausted.json` | An exhausted audit pool falls through to the contract gap and reports which pool the pick came from, instead of printing "no active incomplete verbs". |
| `both-pools-empty.json` | Real completion — both pools empty — still reports no pick. |
