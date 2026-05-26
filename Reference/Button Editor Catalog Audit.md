# Button Editor Catalog Audit

Local cross-check against the VDJScript catalog bundled with VirtualDJ's Button Editor.

Source app: `/Applications/VirtualDJ.app`

Observed on 2026-05-26:

- VirtualDJ app version: `8.5.9307`
- VirtualDJ bundle build: `18.0.9336`
- Main executable SHA-256: `233f36a8d454d0fe90e7bb1c57b9550a4ea8aa3ee0a9f219624c24aa8aaa59f1`
- Language pack: `/Applications/VirtualDJ.app/Contents/Resources/languages.zip`
- Language XML build: `9320`

## Purpose

The Button Editor has a built-in searchable action catalog with categories, action names, and descriptions. This audit records the local source for the description text and compares it with the official appendix and the runtime-looking string table in the executable.

This is a documentation cross-check, not a replacement for the official appendix. Treat it as `Built-in app resource` evidence: stronger than community examples for existence and prose, but not sufficient by itself to prove behavior, parameter coverage, or current public support.

## Bundled Language Catalog

The action descriptions are stored in `Resources/languages.zip`, inside per-language XML files. In `English.xml`, the descriptions are under `<Actions>`, for example `get_beatpos` has the same prose shown in the Button Editor UI.

Counts from the installed app:

| Source | Count |
| --- | ---: |
| `English.xml` `<Actions>` unique tags | 812 |
| Union of `<Actions>` tags across all languages | 813 |
| `<Actions>` tags present in every language | 810 |
| `<tooltips>` unique tags across all languages | 144 |
| `<skintooltips>` unique tags across all languages | 33 |

Only three action tags vary by language:

| Tag | Notes |
| --- | --- |
| `dualdeckmode_decks` | Missing from English but present in Spanish, Dutch, Greek, German, Italian, and Chinese. |
| `edit_lyrics` | Present in English, Spanish, and Dutch only. |
| `video_source` | Missing from Japanese and Arabic only. |

The multilingual union is therefore the best Button Editor catalog source, not English alone.

The language XML does not appear to encode the per-action Button Editor category mapping shown in the UI. Category labels such as `flow`, `param`, `repeat`, `skin`, `system`, `variables`, and `window` are visible as executable strings near `DLGActionWizard`; the action-to-category mapping likely lives in code or a compiled table and still needs separate extraction.

## Runtime String Table Cross-Check

The main executable is a universal Mach-O binary. Plain `strings` exposes two contiguous alphabetical VDJScript-looking blocks from `action_deck` through `zoom_vertical`.

Initial counts:

| Source | Count |
| --- | ---: |
| Binary block 1 | 957 |
| Binary block 2 | 967 |
| Official appendix audit | 991 |
| Button Editor language action union | 813 |

The second binary block includes aliases not seen in the first block, including `close`, `get_album`, `get_artist`, `get_beat`, `get_beatpos`, `get_bpm`, `get_title`, `get_vu_meter`, `pitch`, and `video_crossfader`.

## Interpretation

The local evidence now points to at least three overlapping catalogs:

- The official VDJScript appendix: public names and aliases; currently parsed in this repo as 991 names.
- The Button Editor language catalog: user-facing action descriptions; currently 813 action tags across bundled languages.
- The executable string block: runtime-looking action names; currently 967 names in the richer block.
- The Button Editor category mapping: visible in the UI, but not yet extracted as structured data.

None of these is identical to the others. The Button Editor catalog omits sparse or helper-style official names such as `deck_has_error`, `get_mixfx_active`, and `system`, while the binary block contains runtime/internal-looking names not currently in the official appendix.

Use this hierarchy when updating the API reference:

1. `Official` remains authoritative for public name coverage.
2. `Built-in app resource` can supply Button Editor description evidence and discover localized catalog-only names.
3. Binary string-table evidence can identify runtime candidates, but candidate names need official, bundled-resource, shipped XML, or local behavior evidence before promotion into ordinary user-facing recommendations.

## Reproduction

Run:

```sh
python3 tools/extract_vdjscript_catalogs.py
```

The helper is read-only and compares the installed app's language catalog, executable string block, and this repo's official coverage audit.
