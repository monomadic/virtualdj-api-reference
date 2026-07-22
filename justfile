set shell := ["zsh", "-eu", "-o", "pipefail", "-c"]

default:
    @just --list

next-task:
    @awk '\
      /^### / { if (seen && ready) exit; title=$0; block=$0 "\n"; seen=1; ready=0; next } \
      seen { block=block $0 "\n" } \
      /^Status: Ready$/ && seen { ready=1 } \
      END { if (seen && ready) printf "%s", block } \
    ' TODO.md

# Grep the authored verb prose/examples. For record lookups use `just get-verb`.
grep-verb-docs name:
    @rg -n --fixed-strings "{{name}}" \
      "docs/VDJScript Verbs.md" \
      "docs/Official VDJScript Coverage Audit.md" \
      "docs/VDJScript Local Test Tracker.md" \
      "docs/Undocumented VDJScript Candidates.md" \
      "docs/Effects Engines.md" \
      "docs/Effects Usage.md" \
      "examples/Pads" \
      "tests"

needs-test:
    @rg -n "Needs local test|Untested|Partial|Status: Needs local test|Status: Partial" \
      "docs/Official VDJScript Coverage Audit.md" \
      "docs/VDJScript Local Test Tracker.md" \
      "docs/Completeness Roadmap.md" \
      "docs/Undocumented VDJScript Candidates.md" \
      "TODO.md"

official-needs-test:
    @awk '\
      /^## Needs Local Test/ { in_section=1; next } \
      in_section && /^## / { exit } \
      in_section && NF { print } \
    ' "docs/Official VDJScript Coverage Audit.md"

tracker-untested:
    @rg -n "\| .* \| .* \| .* \| Untested \|" "docs/VDJScript Local Test Tracker.md"

tracker-partial:
    @rg -n "\| .* \| .* \| .* \| Partial \|" "docs/VDJScript Local Test Tracker.md"

thin-verbs:
    @rg -n '^\| `[^`]+` \| — \|' "docs/VDJScript Verbs.md"

status:
    @python3 -c 'from pathlib import Path; import re; text=Path("docs/Official VDJScript Coverage Audit.md").read_text(); count=re.search(r"Official verb/alias names parsed: (\d+)", text); gap=re.search(r"The formal local-test gap is (\d+) official names", text); print("Official names parsed: {}".format(count.group(1) if count else "unknown")); print("Formal local-test gap: {}".format(gap.group(1) if gap else "unknown"))'
    @printf "\nReady queue:\n"
    @rg -n "^### |^Status: Ready$" TODO.md

vdj-query script:
    @curl -sS -m 5 -G 'http://localhost/query' --data-urlencode "script={{script}}"; echo

vdj-execute script:
    @curl -sS -m 5 -G 'http://localhost/execute' --data-urlencode "script={{script}}"; echo

vdj-up:
    @curl -sS -m 3 -G 'http://localhost/query' --data-urlencode 'script=get_version' >/dev/null 2>&1 \
      && echo "VirtualDJ HTTP interface reachable on http://localhost/" \
      || { echo "VirtualDJ HTTP interface NOT reachable (is VirtualDJ running with the network interface enabled?)"; exit 1; }

inventory:
    python3 tools/extract_xml_inventory.py

verb-index:
    python3 tools/extract_verb_index.py

# --- verb record store (docs/vdjscript-verbs.json) ---------------------------
# Flat names on purpose: the argument is always data, never a subcommand, so a
# verb called `search` or `get` can never be mistaken for a command.

get-verb name:
    @python3 tools/verbdb.py get "{{name}}"

find-verbs *args:
    @python3 tools/verbdb.py search {{args}}

put-verb name *assignments:
    @python3 tools/verbdb.py put "{{name}}" {{assignments}}

next-incomplete-verb:
    @python3 tools/verbdb.py next-incomplete

verb-stats:
    @python3 tools/verbdb.py stats

# --- native effects catalog (swept via the HTTP interface) -------------------

get-fx effect:
    @python3 tools/fxdb.py get "{{effect}}"

find-fx *args:
    @python3 tools/fxdb.py search {{args}}

fx-stats:
    @python3 tools/fxdb.py stats

lint-skins *paths:
    python3 tools/lint_skins.py {{paths}}

lint-mappers *paths:
    python3 tools/lint_mappers.py {{paths}}

check:
    python3 tools/lint_pads.py
    python3 tools/lint_skins.py
    python3 tools/lint_mappers.py
    python3 tools/extract_verb_index.py --check
    python3 tools/verbdb.py check
    python3 tools/fxdb.py check
    python3 tools/extract_xml_inventory.py --check
    python3 tools/check_reference_status.py
    git diff --check
