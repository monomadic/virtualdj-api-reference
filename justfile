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

find-verb name:
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

inventory:
    python3 tools/extract_xml_inventory.py

check:
    python3 tools/lint_pads.py
    python3 tools/check_reference_status.py
    git diff --check
