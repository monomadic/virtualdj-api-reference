set shell := ["zsh", "-eu", "-o", "pipefail", "-c"]

# Every recipe runs `{{python}}`, never a bare `python3`. It is the project venv
# when `just install` has been run and the system interpreter otherwise, so a
# fresh clone still works and a bootstrapped one is insulated from the day
# Homebrew moves its default python and the site-packages go with it. That day
# is not hypothetical: it happened on 2026-09-09, numpy vanished, and the only
# symptom was `just check` reporting an action-catalog drift — see `just doctor`.
python := if path_exists(justfile_directory() / ".venv/bin/python3") == "true" { justfile_directory() / ".venv/bin/python3" } else { "python3" }

# Variadic recipes forward "$@" rather than an interpolated string, so an
# argument like evidence="... (2026-07-22) ..." survives verbatim instead of
# being re-split and glob-expanded by the shell.
set positional-arguments

default:
    @just --list

# Run once per clone, and again after a python upgrade moves the interpreter
# out from under an existing venv. `--clear` because the venv is derived state:
# requirements.txt and .python-version are the source of truth, and recreating
# it is a second. Everything else in this file then runs against .venv.
# Create .venv and install requirements.txt with uv.
install:
    @command -v uv >/dev/null || { \
        echo "uv not found. Install it with:  brew install uv" >&2; \
        echo "  (or: curl -LsSf https://astral.sh/uv/install.sh | sh)" >&2; \
        exit 1; }
    uv venv --clear
    uv pip install --python .venv/bin/python3 -r requirements.txt
    @.venv/bin/python3 tools/doctor.py

# The headers are third-party and deliberately NOT vendored: they carry an Atomix
# copyright with no license text and the download page states no terms, so this
# repo fetches them rather than redistributing them. vendor/ stays gitignored.
# Fetch the Atomix plugin SDK headers into vendor/vdj-sdk/ (`--force` to re-fetch).
download-sdk *args:
    @{{python}} tools/download_sdk.py "$@"

# Interpreter, packages, uv, which VirtualDJ is installed against what the
# artifacts are anchored to, and whether the live probe channel answers. Only
# the python section can fail; the rest are notices worth reading before work.
# Environment health in one screen, `brew doctor` style.
doctor:
    @{{python}} tools/doctor.py

# The first startable task in TASKS.md (HISTORY.md holds finished ones). Refuses to select if any status line
# in the file is malformed, rather than skipping the task it cannot read.
next-task:
    @{{python}} tools/task_queue.py next

# Every task with its state; `*` marks the startable ones.
task-queue *args:
    @{{python}} tools/task_queue.py list "$@"

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
      "TASKS.md"

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
    @{{python}} -c 'from pathlib import Path; import re; text=Path("docs/Official VDJScript Coverage Audit.md").read_text(); count=re.search(r"Official verb/alias names parsed: (\d+)", text); gap=re.search(r"The formal local-test gap is (\d+) official names", text); print("Official names parsed: {}".format(count.group(1) if count else "unknown")); print("Formal local-test gap: {}".format(gap.group(1) if gap else "unknown"))'
    @printf "\nTask queue:\n"
    @{{python}} tools/task_queue.py list

# `"$@"` rather than an interpolated {{script}}: interpolation puts the script
# through zsh, which expands a VDJScript global like $ct_top before the request
# is built and leaves `get_var "$ct_top"` querying an empty name.
vdj-query script:
    @curl -sS -m 5 -G 'http://localhost/query' --data-urlencode "script=$1"; echo

vdj-execute script:
    @curl -sS -m 5 -G 'http://localhost/execute' --data-urlencode "script=$1"; echo

vdj-up:
    @curl -sS -m 3 -G 'http://localhost/query' --data-urlencode 'script=get_version' >/dev/null 2>&1 \
      && echo "VirtualDJ HTTP interface reachable on http://localhost/" \
      || { echo "VirtualDJ HTTP interface NOT reachable (is VirtualDJ running with the network interface enabled?)"; exit 1; }

# Serve the store, FX catalog, XML inventory, grammar, linters and the live HTTP
# probe channel to any MCP client over stdio. Zero dependencies; stdout is
# protocol only. `vdj_execute` stays disabled unless VDJ_MCP_EXECUTE=1.
# Registration and tool list: docs/MCP Server.md
mcp-serve:
    @{{python}} tools/mcp_server.py

# Smoke-test the MCP server without a client: lists tools and calls a few.
mcp-check:
    {{python}} tools/doctor.py --deps-only
    @{{python}} tools/mcp_server.py --self-check

inventory:
    {{python}} tools/extract_xml_inventory.py

# --- skin/pad/mapper XML element inventory ----------------------------------

# One element, every source joined — inventory row, its doc section, the binary's
# reader vocabulary, live probe results (negatives included), real usage, and which
# attributes no doc explains. The counterpart to `just verb`.
element name *args:
    @{{python}} tools/element_summary.py "$@"

# The bare inventory row, as `get-verb` is to `verb`.
get-xml-element element:
    @{{python}} tools/xmldb.py get "{{element}}"

# Skin and video-skin elements; --family=all includes pads, mappers and samplerbanks.
list-skin-elements *args:
    @{{python}} tools/xmldb.py search --family=skin "$@"

# Compatibility for existing scripts and frozen planning references.
[private]
list-xml-elements *args:
    @{{python}} tools/xmldb.py search "$@"

xml-stats:
    @{{python}} tools/xmldb.py stats

verb-index:
    {{python}} tools/extract_verb_index.py

# --- verb record store (docs/vdjscript-verbs.json) ---------------------------
# Flat names on purpose: the argument is always data, never a subcommand, so a
# verb called `search` or `get` can never be mistaken for a command.

get-verb name:
    @{{python}} tools/verbdb.py get "{{name}}"

# EVERYTHING about one verb on one screen: store record, vendor description,
# real usages, argument shapes with return evidence, every tail candidate by
# source, vocabulary groups, probe state. `--format=json` for structure.
verb name *args:
    @{{python}} tools/verb_summary.py "{{name}}" {{args}}

list-verbs *args:
    @{{python}} tools/verbdb.py search "$@"

put-verb name *assignments:
    @{{python}} tools/verbdb.py put "$@"

next-incomplete-verb:
    @{{python}} tools/verbdb.py next-incomplete

verb-stats:
    @{{python}} tools/verbdb.py stats

# Non-alias records with no `section`, with their b9246 source module where one
# exists. A query on the store; fill one with `just put-verb <name> section=...`.
uncategorized-verbs *args:
    @{{python}} tools/verbdb.py uncategorized {{args}}

# The section vocabulary with per-section verb and tested counts; the names to
# pass to `list-verbs --section=`. A query on the store, never written down.
list-verb-categories *args:
    @{{python}} tools/verbdb.py sections {{args}}

# Contract coverage across every verb, per dimension, recounted from the
# artifacts. `--settled` names the finished verbs, `--frontier` names what each
# dimension is waiting on. Read-only; touches no live instance.
coverage *args:
    @{{python}} tools/coverage_report.py "$@"

# Generated owned bank; see tests/README.md for preparation and bounded live scope.
probe-sampler-contracts *args:
    @{{python}} tools/probe_sampler_contracts.py "$@"

# Prints frozen cases by default; --run plays quiet generated samples and restores.
probe-sampler-playback *args:
    @{{python}} tools/probe_sampler_playback.py "$@"

# Requires empty stopped deck 1. Generates temporary audio and verifies restoration.
probe-long-time:
    {{python}} tools/probe_long_time.py --run

long-time-forms name="":
    @{{python}} tools/probe_long_time.py --get "{{name}}"

# --- human-facing reference page ---------------------------------------------
# Fill design/human-api-reference.template.html from the verb store, skin inventory and evidence
# artifacts (the same join `just verb` makes) into the git-ignored build/ tree.
# A rendered copy of store data: regenerate it, never commit it.
# Render the human-facing reference page; `--open` shows it in the default browser, `--out PATH` picks the file
build-reference *flags:
    @{{python}} tools/render_reference.py {{flags}}

# --- native effects catalog (swept via the HTTP interface) -------------------

get-fx effect:
    @{{python}} tools/fxdb.py get "{{effect}}"

list-fx *args:
    @{{python}} tools/fxdb.py search "$@"

fx-stats:
    @{{python}} tools/fxdb.py stats

# --- verb existence probe (HTTP error-code sweep) ---------------------------
# Does this name exist, and what kind is it? Answered from the sweep artifact.
# Re-run the sweep with `just sweep-verb-existence` (needs `just vdj-up`).

verb-probe name:
    @{{python}} tools/sweep_verb_existence.py --get "{{name}}"

# AUTHORITATIVE: is this a real verb? Reads VirtualDJ's own verb table.
verb-table name:
    @{{python}} tools/extract_verb_table.py --get "{{name}}"

# The exact build-stamped phrase to quote in prose. Copy it; never recall a build number.
verb-table-stamp:
    @{{python}} tools/extract_verb_table.py --stamp

extract-verb-table:
    @{{python}} tools/extract_verb_table.py > tests/verb-table.json.tmp
    @mv tests/verb-table.json.tmp tests/verb-table.json

# STRUCTURAL CONTRACT: capability, query return type, family from ACTION_ RTTI.
verb-contract name:
    @{{python}} tools/extract_action_contracts.py --get "{{name}}"

# The call-graph addresses behind one verb's traces (roots, callees, unvisited).
verb-traces name:
    @{{python}} tools/extract_action_contracts.py --traces "{{name}}"

extract-action-contracts:
    @{{python}} tools/extract_action_contracts.py > tests/action-contracts.json.tmp
    @mv tests/action-contracts.json.tmp tests/action-contracts.json

# OBSERVED TYPE: what a query verb actually returns over HTTP (Tier 1).
verb-return-type name:
    @{{python}} tools/sweep_return_types.py --get "{{name}}"

sweep-return-types:
    @{{python}} tools/sweep_return_types.py > tests/verb-return-types.json.tmp
    @mv tests/verb-return-types.json.tmp tests/verb-return-types.json

# --- prepared state (fixtures) ----------------------------------------------
# Argument forms can only be told apart in a state where they would disagree.
# Each fixture verifies its own preconditions and refuses to report success
# otherwise. `fixture-establish` changes live app state; some make sound.

fixtures:
    @{{python}} tools/fixtures.py --list

fixture-verify name:
    @{{python}} tools/fixtures.py --verify "{{name}}"

fixture-establish name *args:
    {{python}} tools/fixtures.py --establish "{{name}}" {{args}}

# Send every vendor snippet through /query and classify the outcome.
corpus-parses *args:
    {{python}} tools/check_corpus_parses.py {{args}} > tests/corpus-parse-results.json.tmp
    @mv tests/corpus-parse-results.json.tmp tests/corpus-parse-results.json

# Argument tails Atomix wrote in shipped scripts — attested without a probe.
attested-tails *args:
    @{{python}} tools/extract_attested_tails.py {{args}}

# The Button Editor's own action descriptions — the official appendix prose,
# offline. `--cross-check` diffs documented parameters against probe findings.
# Historical installers: vendor prose and shipped-skin usages the current app no longer carries.
vendor-history-diff root="/tmp/vdj-history-20260906":
    @{{python}} tools/diff_vendor_history.py --root {{root}} --output tests/build-history-2026-09-06/vendor-text-diff.json

action-catalog *args:
    @{{python}} tools/extract_action_catalog.py {{args}}

# Every VDJScript snippet Atomix wrote: catalog examples + shipped Built-In XML
# + every factory controller mapping decoded from controllers.dat (needs
# `just controllers-vendor`) + wiki transcriptions + statements compiled into
# the app binary.
script-corpus *args:
    @{{python}} tools/extract_script_corpus.py {{args}}

# Do the vendor XML copies under examples/*/Built-In still match the installed
# app? A VirtualDJ update silently ages them, and the corpus then attests a
# value the vendor no longer ships. `--refresh` re-copies; re-extract after.
bundle-copies *args:
    @{{python}} tools/check_bundle_copies.py {{args}}

# Argument VOCABULARIES: shared enumerations (stem names, colours, sideview
# pages) recovered as structures from the binary — pointer tables and the
# switch functions that walk them. Tier 2: members are leads for the prober.
binary-vocab *args:
    @{{python}} tools/extract_binary_vocabularies.py {{args}}

extract-binary-vocabularies:
    @{{python}} tools/extract_binary_vocabularies.py > tests/binary-vocabularies.json.tmp
    @mv tests/binary-vocabularies.json.tmp tests/binary-vocabularies.json

# SOURCE MODULE: which of Atomix's own `action_*.cpp` files implements a verb,
# from the unstripped build's STABS. Tier 2 — it groups a verb, and says nothing
# about whether it works. `--sections` says which modules map cleanly onto a
# store section; `extract-action-modules` needs the b9246 pkg expanded.
action-modules *args:
    @{{python}} tools/extract_action_modules.py {{args}}

extract-action-modules app:
    @{{python}} tools/extract_action_modules.py --app "{{app}}" > tests/action-modules-9246.json.tmp
    @mv tests/action-modules-9246.json.tmp tests/action-modules-9246.json

# TAIL GRAMMAR: which trailing tokens a verb actually recognizes (Tier 1).
# Every candidate is measured against nonsense controls, in every fixture.
verb-arg-forms name:
    @{{python}} tools/probe_arg_forms.py --get "{{name}}"

# Needs `just vdj-up`. Establishes each fixture in turn; some make sound.
# The tool writes the artifact itself, atomically, and only for a real run —
# `--dry-run` and `--check` leave it untouched; `--merge FILE` updates it itself.
# (A shell redirect here once truncated the evidence on every dry run.)
probe-arg-forms *args:
    {{python}} tools/probe_arg_forms.py --out tests/verb-arg-forms.json {{args}}

# EXECUTE-position tails. WRITES to the running instance: allowlisted settings
# verbs only, each round-trip tested first, every value restored and verified.
probe-execute-forms *args:
    {{python}} tools/probe_execute_forms.py --out tests/verb-execute-forms.json {{args}}

# Corroborating structured sources (superseded by verb-table for existence).
binary-verb name:
    @{{python}} tools/extract_binary_verbs.py --get "{{name}}"

extract-binary-verbs:
    @{{python}} tools/extract_binary_verbs.py > tests/binary-verbs.json.tmp
    @mv tests/binary-verbs.json.tmp tests/binary-verbs.json

sweep-verb-existence:
    @{{python}} tools/sweep_verb_existence.py > tests/verb-existence-sweep.json.tmp
    @mv tests/verb-existence-sweep.json.tmp tests/verb-existence-sweep.json

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
    @{{python}} tools/plugin_introspect.py prepare "$@"

plugin-status:
    @{{python}} tools/plugin_introspect.py status

plugin-collect:
    @{{python}} tools/plugin_introspect.py collect > tests/plugin-introspection.json.tmp
    @mv tests/plugin-introspection.json.tmp tests/plugin-introspection.json
    @{{python}} tools/plugin_introspect.py --check

# Follow-up capture: deck context for the silent query verbs, and each recovered
# keyword paired with a nonsense control on the same verb.
plugin-prepare-leads:
    @{{python}} tools/plugin_introspect.py prepare --leads

# Any other capture: `just plugin-collect-as controls` -> tests/plugin-introspection-controls.json
plugin-collect-as name:
    @{{python}} tools/plugin_introspect.py collect > "tests/plugin-introspection-{{name}}.json.tmp"
    @mv "tests/plugin-introspection-{{name}}.json.tmp" "tests/plugin-introspection-{{name}}.json"
    @echo "wrote tests/plugin-introspection-{{name}}.json"

plugin-collect-leads:
    @{{python}} tools/plugin_introspect.py collect > tests/plugin-introspection-leads.json.tmp
    @mv tests/plugin-introspection-leads.json.tmp tests/plugin-introspection-leads.json
    @{{python}} tools/plugin_introspect.py leads-report

# OBSERVED NATIVE TYPE: which channel a verb answers on, and with what.
plugin-probe name:
    @{{python}} tools/plugin_introspect.py --get "{{name}}"

# --- cross-corpus topic search ----------------------------------------------
# One term -> matching verbs, effects, XML elements, REAL example files, docs,
# and known quirks. Start here for "how do I do X"; drill in with get-verb etc.

topic *args:
    @{{python}} tools/topic.py "$@"

lint-skins *paths:
    {{python}} tools/lint_skins.py "$@"

lint-mappers *paths:
    {{python}} tools/lint_mappers.py "$@"

check:
    just check-lyrics-cache
    just check-linked-sid
    just check-runtime-grammar
    {{python}} tools/mcp_server.py --self-check
    {{python}} tools/probe_long_time.py --check
    {{python}} tools/check_bundle_copies.py
    {{python}} tools/lint_pads.py
    {{python}} tools/lint_skins.py
    {{python}} tools/lint_mappers.py
    {{python}} tools/extract_verb_index.py --check
    {{python}} tools/verbdb.py check
    {{python}} tools/fxdb.py check
    {{python}} tools/sweep_verb_existence.py --check
    {{python}} tools/extract_binary_verbs.py --check
    {{python}} tools/extract_verb_table.py --check
    {{python}} tools/extract_action_contracts.py --check
    {{python}} tools/test_reference.py
    {{python}} tools/test_sysicon_atlas.py
    {{python}} tools/test_action_tail_bounds.py
    {{python}} tools/test_contract_assessment.py
    {{python}} tools/test_coverage_section.py
    {{python}} tools/test_sampler_contracts.py
    {{python}} tools/test_sampler_playback.py
    {{python}} tools/action_tail_leads.py --check
    {{python}} tools/sweep_return_types.py --check
    {{python}} tools/plugin_introspect.py --check
    {{python}} tools/plugin_skin.py --check
    {{python}} tools/topic.py check
    {{python}} tools/fixtures.py --check
    {{python}} tools/probe_arg_forms.py --check
    {{python}} tools/probe_known_positions.py --check
    {{python}} tools/probe_bpm_transition.py --check
    {{python}} tools/probe_arg_positions.py --check
    {{python}} tools/probe_execute_forms.py --check
    {{python}} tools/extract_action_catalog.py --check
    {{python}} tools/extract_script_corpus.py --check
    {{python}} tools/extract_attested_tails.py --check
    {{python}} tools/extract_binary_vocabularies.py --check
    {{python}} tools/extract_action_modules.py --check
    {{python}} tools/check_corpus_parses.py --check
    {{python}} tools/extract_xml_inventory.py --check
    {{python}} tools/extract_skin_readers.py --check
    {{python}} tools/extract_skin_classes.py --check
    {{python}} tools/check_reference_status.py
    {{python}} tools/task_queue.py check
    {{python}} tools/task_queue.py selftest
    git diff --check

# What the skin XML readers in the binary actually compare against, and which
# of those names appear in no shipped skin and no SDK doc.
skin-readers:
    @{{python}} tools/extract_skin_readers.py > tests/skin-reader-vocabulary.json.tmp
    @mv tests/skin-reader-vocabulary.json.tmp tests/skin-reader-vocabulary.json
    @echo "wrote tests/skin-reader-vocabulary.json"

skin-reader name:
    @{{python}} tools/extract_skin_readers.py --get "{{name}}"

skin-candidates:
    @{{python}} tools/extract_skin_readers.py --candidates

# get_time's position arguments against three independently known positions.
# Writes to a live VirtualDJ (deck 1, stopped, no audio) and restores it.
known-positions:
    @{{python}} tools/probe_known_positions.py --run > tests/get-time-positions.json.tmp
    @mv tests/get-time-positions.json.tmp tests/get-time-positions.json
    @echo "wrote tests/get-time-positions.json"
    @{{python}} tools/probe_known_positions.py --check

# auto_bpm_transition's three documented parameters, read by WHERE the pair of
# decks settles rather than by whether a transition is running. Writes to a live
# VirtualDJ (decks 1 and 2, stopped, no audio) and restores both.
bpm-transition:
    @{{python}} tools/probe_bpm_transition.py --run > tests/bpm-transition-forms.json.tmp
    @mv tests/bpm-transition-forms.json.tmp tests/bpm-transition-forms.json
    @echo "wrote tests/bpm-transition-forms.json"
    @{{python}} tools/probe_bpm_transition.py --check

# Which ARGUMENT POSITIONS a verb reads: hold the attested shape, vary one
# position within its own class, see whether the answer moves. Query-only.
# `just probe-arg-positions --keywords=attested,catalog,vocab` widens the second
# keyword source; the default two are what the queue ratified.
probe-arg-positions *args:
    @{{python}} tools/probe_arg_positions.py --run "$@" > tests/verb-arg-positions.json.tmp
    @mv tests/verb-arg-positions.json.tmp tests/verb-arg-positions.json
    @{{python}} tools/probe_arg_positions.py --check

# Which verbs a probe run would reach and what evidence each rests on. Needs no
# live VirtualDJ, so coverage is measurable before the instance is up.
probe-arg-positions-plan *args:
    @{{python}} tools/probe_arg_positions.py --plan "$@"

verb-arg-positions name:
    @{{python}} tools/probe_arg_positions.py --get "{{name}}"

# Confirm argument keywords against their nonsense controls in any capture.
plugin-keyword-report capture *args:
    @{{python}} tools/plugin_introspect.py keyword-report --capture "tests/plugin-introspection-{{capture}}.json" {{args}}

# Re-sweep the delayed probe list right now, without restarting VirtualDJ.
# Set the app up by hand first (load a track, highlight a song), then trigger.
plugin-go:
    @{{python}} tools/plugin_introspect.py go

# Collect the delayed/triggered capture: `just plugin-collect-late prepared`
plugin-collect-late name:
    @{{python}} tools/plugin_introspect.py collect --late > "tests/plugin-introspection-{{name}}.json.tmp"
    @mv "tests/plugin-introspection-{{name}}.json.tmp" "tests/plugin-introspection-{{name}}.json"
    @echo "wrote tests/plugin-introspection-{{name}}.json"

# GetSongBuffer: the raw PCM of the loaded song, at any position. No other
# channel exposes it — this is the input side of the waveform questions.
# Needs a track loaded; `just plugin-songbuffer` then `just plugin-go`.
plugin-songbuffer:
    @{{python}} tools/plugin_introspect.py songbuffer

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
    @{{python}} tools/plugin_skin.py prepare {{ if xml == "" { "" } else { "--xml " + xml } }}

plugin-skin-log:
    @{{python}} tools/plugin_skin.py log

# Toggling the panel is what makes VirtualDJ re-ask for the XML.
plugin-skin-reload:
    @curl -sS -m 6 -G 'http://localhost/execute' --data-urlencode "script=deck 1 effect_show_gui 'VDJIntrospectSkin'" >/dev/null
    @sleep 1
    @curl -sS -m 6 -G 'http://localhost/execute' --data-urlencode "script=deck 1 effect_show_gui 'VDJIntrospectSkin'" >/dev/null
    @echo 'panel re-opened; run `just plugin-skin-log` to see the new call'

plugin-songbuffer-report:
    @{{python}} tools/plugin_introspect.py songbuffer-report

# OnKey/mouse events — the only channel that might carry press vs release.
plugin-keylog:
    @{{python}} tools/plugin_introspect.py keylog

# Atlas cells joined to wiki names, live results and binary candidates.
sysicon-atlas *args:
    @{{python}} tools/sysicon_atlas.py "$@"

# The skin object classes and the elements that build them (Tier 2 leads).
# Bare: a read-time summary. `--element panel` says which class builds an element,
# `--get CSkinPanel` the whole record, `--attributes CSkinPanel` just its attribute
# candidates. Read the artifact's own `limitations` before citing: absence
# establishes nothing.
skin-classes *args:
    @{{python}} tools/extract_skin_classes.py "$@"

# Every skin object class, one line each. Filters: --base, --has-attr,
# --element-backed, --format=json. Untruncated, as the other list-* are.
list-skin-classes *args:
    @{{python}} tools/extract_skin_classes.py --list "$@"

# Historical skin class source provenance (Tier 2; many-to-many STABS relation).
skin-modules *args:
    @{{python}} tools/extract_skin_modules.py {{args}}

extract-skin-modules app:
    @{{python}} tools/extract_skin_modules.py --app "{{app}}" > tests/skin-modules-9246.json.tmp
    @mv tests/skin-modules-9246.json.tmp tests/skin-modules-9246.json

# Tier-2 bounded method/helper literal leads and ranked live probe queue.
action-tail-leads *args:
    @{{python}} tools/action_tail_leads.py {{args}}

extract-action-tail-leads:
    @{{python}} tools/action_tail_leads.py --generate > tests/action-tail-leads.json.tmp
    @mv tests/action-tail-leads.json.tmp tests/action-tail-leads.json

# H4: frozen candidate tests, exact-script HTTP observations, bounded binary evidence.
runtime-grammar *args:
    @{{python}} tools/runtime_grammar_probes.py "$@"

# Paired editor appearance and HTTP results, with failed predictions retained.
runtime-grammar-editor *args:
    @{{python}} tools/runtime_grammar_editor.py "$@"

extract-runtime-parser app:
    @{{python}} tools/extract_runtime_parser.py --app "{{app}}" --output tests/runtime-parser-9246

runtime-parser-frontier *args:
    @{{python}} tools/runtime_parser_frontier.py --report "$@"

# Say what each queued indirect site actually is: factory, vtable, or artifact.
frontier-closure *args:
    @{{python}} tools/resolve_frontier_sites.py "$@"

# Which deck-wrapper token was in flight at an exit. Read-only payloads, journal
# flushed before each send, process identity checked after every probe.
probe-deck-targets *args:
    @{{python}} tools/probe_deck_targets.py "$@"

# Are bare names per-deck, $ shared and @ a separate name? Writes probe variables
# under a zzprobescope name and sets them back to 0, verifying the teardown.
probe-variable-scope *args:
    @{{python}} tools/probe_variable_scope.py "$@"

# Whether the request pattern alone precedes an exit: fresh vs reused connection.
probe-http-stability *args:
    @{{python}} tools/probe_http_stability.py "$@"

# H4: deck-scope keywords with selection and master pinned to DIFFERENT decks.
# Needs four unloaded, stopped decks; it refuses to mutate anything otherwise.
runtime-grammar-master *args:
    @{{python}} tools/runtime_grammar_master.py "$@"

check-runtime-grammar:
    @{{python}} tools/test_runtime_parser_branch_routes.py
    @{{python}} tools/test_runtime_grammar_audit.py
    @{{python}} tools/runtime_grammar_probes.py --audit > /dev/null
    @{{python}} tools/test_runtime_grammar_playing.py
    @{{python}} tools/build_runtime_editor_help_cases.py --check
    @{{python}} tools/build_runtime_quote_consumer_cases.py --check
    @{{python}} tools/build_runtime_quote_consumer_cases.py --arity-controls --check
    @{{python}} tools/build_runtime_unmatched_quote_cases.py --check
    @{{python}} tools/build_runtime_setting_eval_cases.py --check
    @{{python}} tools/build_runtime_setting_eval_cases.py --discrimination --check
    @{{python}} tools/build_runtime_setting_eval_cases.py --types --check
    @{{python}} tools/test_runtime_setting_eval.py
    @{{python}} tools/test_runtime_quote_consumer.py
    @{{python}} tools/build_runtime_boundary_cases.py --check
    @{{python}} tools/build_runtime_boundary_confirmation.py --check
    @{{python}} tools/runtime_grammar_probes.py --check --artifact tests/runtime-grammar-boundary-9598.json > /dev/null
    @{{python}} tools/runtime_grammar_probes.py --check --artifact tests/runtime-grammar-boundary-confirmation-9598.json > /dev/null
    @{{python}} tools/test_runtime_grammar_editor.py
    @{{python}} tools/runtime_grammar_editor.py --check > /dev/null
    @{{python}} tools/runtime_parser_frontier.py --check > /dev/null
    @{{python}} tools/resolve_frontier_sites.py --check > /dev/null
    @{{python}} tools/test_runtime_grammar_actions.py
    @{{python}} tools/test_runtime_grammar_scopes.py
    @{{python}} tools/test_runtime_grammar_master.py
    @{{python}} tools/runtime_grammar_master.py --check > /dev/null
    @{{python}} tools/runtime_grammar_probes.py --check --artifact tests/runtime-grammar-actions-initial-9598.json
    @{{python}} tools/runtime_grammar_probes.py --check --artifact tests/runtime-grammar-actions-9598.json
    @{{python}} tools/runtime_grammar_probes.py --check --artifact tests/runtime-grammar-scopes-initial-9598.json
    @{{python}} tools/runtime_grammar_probes.py --check --artifact tests/runtime-grammar-scopes-second-attempt-9598.json
    @{{python}} tools/runtime_grammar_probes.py --check --artifact tests/runtime-grammar-scopes-9598.json
    @{{python}} tools/runtime_grammar_probes.py --check --artifact tests/runtime-grammar-action-fallback-9598.json
    @{{python}} tools/runtime_grammar_probes.py --check --artifact tests/runtime-grammar-action-default-initial-9598.json
    @{{python}} tools/runtime_grammar_probes.py --check --artifact tests/runtime-grammar-action-default-9598.json
    @{{python}} tools/runtime_grammar_probes.py --check --artifact tests/runtime-grammar-scope-followup-9598.json
    @{{python}} tools/runtime_grammar_probes.py --check --artifact tests/runtime-grammar-whitespace-9598.json
    @{{python}} tools/test_runtime_grammar_probes.py
    @{{python}} tools/runtime_grammar_probes.py --check
    @{{python}} tools/runtime_grammar_probes.py --check --artifact tests/runtime-grammar-live-9598.json
    @{{python}} tools/runtime_grammar_probes.py --check --artifact tests/runtime-grammar-followup-9598.json

# The decoded archive the corpus mines, under gitignored vendor/ (vendor copyright,
# like the SDK headers). One tree per archive, keyed by app build AND the
# archive's own revision — vendor/controllers/18.0.9598-r2241/ — with the
# committed manifest at tests/controllers-manifests/<key>.json. Idempotent: an
# existing key is verified, never overwritten, so decoding on a new build ADDS
# a record; then `just script-corpus > tests/vdjscript-corpus.json` to re-anchor.
controllers-vendor:
    @uv run tools/read_controllers.py --vendor
    @{{python}} tools/extract_script_corpus.py --vendor-check

# Every controller archive with a committed manifest, and which are decoded here.
controllers-archives *args:
    @{{python}} tools/controller_archives.py {{args}}

# What changed in controllers.dat between two builds, from the manifests alone:
# `just controllers-diff 18.0.9583 18.0.9598`, `--root mapper`, `--format=json`.
controllers-diff older newer *args:
    @{{python}} tools/controllers_diff.py "{{older}}" "{{newer}}" {{args}}

# Decode every original device/mapper/audio XML member; output dir must be new.
controllers-extract *args:
    @uv run tools/read_controllers.py "$@"

# Offline vocabulary and mapper cross-checks; --path /device/slider or --device DDJGRV6.
controllers *args:
    @{{python}} tools/controller_schema_inventory.py "$@"

# Linked-track SID calculation from prepared metadata, or an offline snapshot audit.
linked-sid *args:
    @{{python}} tools/linked_sid.py "$@"

# Historical symbol-bounded SID extraction; requires capstone, writes JSON to stdout.
extract-linked-sid *args:
    @{{python}} tools/extract_linked_sid.py "$@"

# Execute historical reducer/hash instructions on synthetic inputs; requires unicorn.
probe-linked-sid-binary *args:
    @{{python}} tools/probe_linked_sid_binary.py "$@"

check-linked-sid:
    @{{python}} tools/test_linked_sid.py

# Every stored linked-track relationship; missing metadata stays visible by SID.
list-linked-tracks *args:
    @{{python}} tools/list_linked_tracks.py "$@"

# Lyric key conversions, payload parsing and offline cache inspection.
lyrics-cache *args:
    @{{python}} tools/lyrics_cache.py "$@"

# Historical lyric-cache binary capture; capstone required, JSON on stdout.
extract-lyrics-cache *args:
    @{{python}} tools/extract_lyrics_cache.py "$@"

# Synthetic original-instruction tests; Unicorn required, JSON on stdout.
probe-lyrics-binary *args:
    @{{python}} tools/probe_lyrics_binary.py "$@"

check-lyrics-cache:
    @{{python}} tools/test_lyrics_cache.py
