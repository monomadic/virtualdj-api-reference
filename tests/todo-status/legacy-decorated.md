# TODO fixture: the decorated status lines that used to be skipped

Every `Status:` line below is copied from the form `TODO.md` really carried
before the convention landed. The old `awk` selector matched `^Status: Ready$`
exactly, so all four tasks here were invisible and `just next-task` reported an
empty queue while three of them were startable. The parser must now reject each
one loudly instead of skipping it.

## Ready Tasks

### 11. Build The Verb Index From The Artifacts, Not From Prose

Status: **Ready.** Added 2026-08-11.

Bold and trailing-period decoration.

### 6. Continue Hidden Button Editor Candidate Probes

Status: Ready — reframed 2026-07-29: these are no longer "candidates". All 37 hidden names are
proven real by verb-table membership (`flags == 256`).

An explanation spilling onto a second line.

### 7. Repeat `dualdeckmode_decks` In A Better Context

Status: Ready, but low expected yield until a concrete context is identified

A qualifier appended with a comma.

### 2. Characterize FX Bank Save And Load

Status: DONE (2026-07-26, HTTP). A bank is a rack of effect SELECTIONS for slots 1-6.

A completed entry, whose whole narrative sat on the status line.
