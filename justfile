set shell := ["zsh", "-eu", "-o", "pipefail", "-c"]

# Variadic recipes forward "$@" rather than an interpolated string, so an
# argument like evidence="... (2026-07-22) ..." survives verbatim instead of
# being re-split and glob-expanded by the shell.
set positional-arguments

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

# --- skin/pad/mapper XML element inventory ----------------------------------

get-xml-element element:
    @python3 tools/xmldb.py get "{{element}}"

find-xml-elements *args:
    @python3 tools/xmldb.py search "$@"

xml-stats:
    @python3 tools/xmldb.py stats

verb-index:
    python3 tools/extract_verb_index.py

# --- verb record store (docs/vdjscript-verbs.json) ---------------------------
# Flat names on purpose: the argument is always data, never a subcommand, so a
# verb called `search` or `get` can never be mistaken for a command.

get-verb name:
    @python3 tools/verbdb.py get "{{name}}"

find-verbs *args:
    @python3 tools/verbdb.py search "$@"

put-verb name *assignments:
    @python3 tools/verbdb.py put "$@"

next-incomplete-verb:
    @python3 tools/verbdb.py next-incomplete

verb-stats:
    @python3 tools/verbdb.py stats

# --- native effects catalog (swept via the HTTP interface) -------------------

get-fx effect:
    @python3 tools/fxdb.py get "{{effect}}"

find-fx *args:
    @python3 tools/fxdb.py search "$@"

fx-stats:
    @python3 tools/fxdb.py stats

# --- verb existence probe (HTTP error-code sweep) ---------------------------
# Does this name exist, and what kind is it? Answered from the sweep artifact.
# Re-run the sweep with `just sweep-verb-existence` (needs `just vdj-up`).

verb-probe name:
    @python3 tools/sweep_verb_existence.py --get "{{name}}"

# AUTHORITATIVE: is this a real verb? Reads VirtualDJ's own verb table.
verb-table name:
    @python3 tools/extract_verb_table.py --get "{{name}}"

extract-verb-table:
    @python3 tools/extract_verb_table.py > tests/verb-table.json

# STRUCTURAL CONTRACT: capability, query return type, family from ACTION_ RTTI.
verb-contract name:
    @python3 tools/extract_action_contracts.py --get "{{name}}"

extract-action-contracts:
    @python3 tools/extract_action_contracts.py > tests/action-contracts.json

# OBSERVED TYPE: what a query verb actually returns over HTTP (Tier 1).
verb-return-type name:
    @python3 tools/sweep_return_types.py --get "{{name}}"

sweep-return-types:
    @python3 tools/sweep_return_types.py > tests/verb-return-types.json

# --- prepared state (fixtures) ----------------------------------------------
# Argument forms can only be told apart in a state where they would disagree.
# Each fixture verifies its own preconditions and refuses to report success
# otherwise. `fixture-establish` changes live app state; some make sound.

fixtures:
    @python3 tools/fixtures.py --list

fixture-verify name:
    @python3 tools/fixtures.py --verify "{{name}}"

fixture-establish name *args:
    python3 tools/fixtures.py --establish "{{name}}" {{args}}

# Corroborating structured sources (superseded by verb-table for existence).
binary-verb name:
    @python3 tools/extract_binary_verbs.py --get "{{name}}"

extract-binary-verbs:
    @python3 tools/extract_binary_verbs.py > tests/binary-verbs.json

sweep-verb-existence:
    @python3 tools/sweep_verb_existence.py > tests/verb-existence-sweep.json

# --- plugin channel: native typed queries (task 10a) -------------------------
# A read-only C++ plugin asks GetInfo/GetStringInfo directly, so return types are
# observed rather than inferred from HTTP's rendered text. Needs the Atomix SDK
# headers under vendor/ (not vendored here — see docs/Plugin SDK.md).
#
#   just plugin-build --install   # build + drop into VirtualDJ's plugin folder
#   (restart VirtualDJ)
#   just plugin-prepare           # write the probe list
#   (restart VirtualDJ — the sweep runs at plugin load)
#   just plugin-status            # confirm it ran
#   just plugin-collect           # normalize the capture into tests/

plugin-build *args:
    @tools/plugin/build.sh "$@"

plugin-prepare *args:
    @python3 tools/plugin_introspect.py prepare "$@"

plugin-status:
    @python3 tools/plugin_introspect.py status

plugin-collect:
    @python3 tools/plugin_introspect.py collect > tests/plugin-introspection.json
    @python3 tools/plugin_introspect.py --check

# Follow-up capture: deck context for the silent query verbs, and each recovered
# keyword paired with a nonsense control on the same verb.
plugin-prepare-leads:
    @python3 tools/plugin_introspect.py prepare --leads

# Any other capture: `just plugin-collect-as controls` -> tests/plugin-introspection-controls.json
plugin-collect-as name:
    @python3 tools/plugin_introspect.py collect > "tests/plugin-introspection-{{name}}.json"
    @echo "wrote tests/plugin-introspection-{{name}}.json"

plugin-collect-leads:
    @python3 tools/plugin_introspect.py collect > tests/plugin-introspection-leads.json
    @python3 tools/plugin_introspect.py leads-report

# OBSERVED NATIVE TYPE: which channel a verb answers on, and with what.
plugin-probe name:
    @python3 tools/plugin_introspect.py --get "{{name}}"

# --- cross-corpus topic search ----------------------------------------------
# One term -> matching verbs, effects, XML elements, REAL example files, docs,
# and known quirks. Start here for "how do I do X"; drill in with get-verb etc.

topic *args:
    @python3 tools/topic.py "$@"

lint-skins *paths:
    python3 tools/lint_skins.py "$@"

lint-mappers *paths:
    python3 tools/lint_mappers.py "$@"

check:
    python3 tools/lint_pads.py
    python3 tools/lint_skins.py
    python3 tools/lint_mappers.py
    python3 tools/extract_verb_index.py --check
    python3 tools/verbdb.py check
    python3 tools/fxdb.py check
    python3 tools/sweep_verb_existence.py --check
    python3 tools/extract_binary_verbs.py --check
    python3 tools/extract_verb_table.py --check
    python3 tools/extract_action_contracts.py --check
    python3 tools/sweep_return_types.py --check
    python3 tools/plugin_introspect.py --check
    python3 tools/plugin_skin.py --check
    python3 tools/topic.py check
    python3 tools/fixtures.py --check
    python3 tools/extract_xml_inventory.py --check
    python3 tools/check_reference_status.py
    git diff --check

# Confirm argument keywords against their nonsense controls in any capture.
plugin-keyword-report capture *args:
    @python3 tools/plugin_introspect.py keyword-report --capture "tests/plugin-introspection-{{capture}}.json" {{args}}

# Re-sweep the delayed probe list right now, without restarting VirtualDJ.
# Set the app up by hand first (load a track, highlight a song), then trigger.
plugin-go:
    @python3 tools/plugin_introspect.py go

# Collect the delayed/triggered capture: `just plugin-collect-late prepared`
plugin-collect-late name:
    @python3 tools/plugin_introspect.py collect --late > "tests/plugin-introspection-{{name}}.json"
    @echo "wrote tests/plugin-introspection-{{name}}.json"

# GetSongBuffer: the raw PCM of the loaded song, at any position. No other
# channel exposes it — this is the input side of the waveform questions.
# Needs a track loaded; `just plugin-songbuffer` then `just plugin-go`.
plugin-songbuffer:
    @python3 tools/plugin_introspect.py songbuffer

# --- runtime skin loop (task 10a follow-on) ---------------------------------
# The Sound Effect build made with `tools/plugin/build.sh --skin --install`
# answers OnGetUserInterface with VDJINTERFACE_SKIN and serves these two files
# fresh on every call, so a skin edit costs a panel re-open, not a restart:
#
#   just plugin-skin-prepare              # write skin.png + the probe skin.xml
#   just plugin-skin-prepare tests/Skins/runtime-probe/my.xml
#   just plugin-skin-reload               # close + re-open the panel (needs HTTP)
#   just plugin-skin-log                  # how many times VirtualDJ asked
plugin-skin-prepare *xml:
    @python3 tools/plugin_skin.py prepare {{ if xml == "" { "" } else { "--xml " + xml } }}

plugin-skin-log:
    @python3 tools/plugin_skin.py log

# Toggling the panel is what makes VirtualDJ re-ask for the XML.
plugin-skin-reload:
    @curl -sS -m 6 -G 'http://localhost/execute' --data-urlencode "script=deck 1 effect_show_gui 'VDJIntrospectSkin'" >/dev/null
    @sleep 1
    @curl -sS -m 6 -G 'http://localhost/execute' --data-urlencode "script=deck 1 effect_show_gui 'VDJIntrospectSkin'" >/dev/null
    @echo 'panel re-opened; run `just plugin-skin-log` to see the new call'

plugin-songbuffer-report:
    @python3 tools/plugin_introspect.py songbuffer-report

# OnKey/mouse events — the only channel that might carry press vs release.
plugin-keylog:
    @python3 tools/plugin_introspect.py keylog
