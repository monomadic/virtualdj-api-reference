# TODO

The active queue. It has one goal: a **complete verb syntax** and a **complete skin syntax**,
recovered from the binary.

- **Verb syntax:** the statement grammar, and for every verb which argument positions it reads,
  the keywords it recognizes at each position, how it converts each argument (number, text,
  evaluated expression), and what an unrecognized token falls back to.
- **Skin syntax:** every element and the role it plays (object, child slot, wrapper, directive),
  its attributes with reader type and default per context, its children, and the expansion
  rules for templates, classes, includes and conditions.

**Out of scope:** what a verb *does* and how an element *renders*. Those need live behaviour
evidence and belong to the retired tasks in [RETIRED.md](RETIRED.md). So do linters,
compilers and other consumers of the result. Tasks that land move to [HISTORY.md](HISTORY.md).

## Rules

- **Status line.** Every `### <id>. <title>` task has exactly one `Status:` line, as the first
  line under its heading, holding one word: `Ready`, `Blocked`, `Conditional`, `Parking lot` or
  `Done`. Explanation goes in the `Note:` below it. `just next-task` selects the first `Ready`
  task and refuses to select when any status is unreadable. `just check` fails on a `Done`
  task left here; move the block to `HISTORY.md` instead.
- **Evidence tier.** Everything this queue produces is Tier 2 under
  [Evidence Standards](docs/Evidence%20Standards.md): it shows what the parser accepts and what
  a reader consumes, not that anything works. Say so in every artifact. Do not promote a
  syntax finding to `test_status=Pass`.
- **Build stamp.** Recovery runs on the symbol-rich 18.0.9246 arm64 build. Every finding
  carries its build, binary hash and routine identity. Do not merge 9246 results into a
  9644 record; task B1 carries them across.
- **Where results go.** Per-verb findings go into a build-stamped artifact under `tests/` and
  are read through `just verb`. Per-element findings go into `tests/skin-structure-9246.json`
  and `docs/skin-attribute-contracts.json`, read through `just skin-structure` and
  `just skin-attributes`. Do not write Markdown copies of either. Run narrative goes in the
  topical doc each task names.
- **Absence is not rejection.** A name missing from a trace, or a null from the factory, is
  "not observed on this path", never "unknown". Reserve "not accepted" for a context whose
  dispatch and reader routes are accounted for.

## Tasks

### V1. Close the statement grammar on the offline parser host

Status: Ready

Note: The offline parser host calls the native `IAction::create` on 9246 and 9644, but only
over a fixed allowlist and only for `is_using`. Two things stand between it and a closed
grammar: compound action objects have not been decoded, and the host cannot take arbitrary
input.

1. Recover the object layout for compound actions from the named 9246 routines: `&` chains,
   `?:`, backtick and parenthesised evaluation, and the `deck` / `not` wrappers. Extend
   `tests/parser-object-layout-9246.json` the same way the parameter layout was recovered.
2. Replace the fixed suite with a generated one, keeping the host's isolation. Inputs: every
   example in [VDJScript Grammar](docs/VDJScript%20Grammar.md), the frozen runtime-grammar
   cases (`just runtime-grammar --audit`), vendor corpus snippets as inputs only, and nonsense
   controls.
3. Run the same inputs through both hosted builds. Any difference is a grammar change between
   9246 and 9644.

Done when every rule in the Grammar doc has an offline case whose native parse tree matches
it, the cases are checked in `just check`, and any rule the tree contradicts is corrected in
the Grammar doc. Evaluation stays out: the host parses and never runs a script.

Read first: [Offline Parser Host](docs/Offline%20Parser%20Host.md), the Grammar summary,
retired task H4 in [HISTORY.md](HISTORY.md#h4-runtime-argument-parsing-from-the-named-iactioncreate).

### K1. Finish the skin element inventory and factory dispatch

Status: Ready

Note: Continues step 1 of retired task S6. The checkpoint is `tests/skin-structure-9246.json`
(`just skin-structure`). [Native Skin Child Relationships](docs/Native%20Skin%20Child%20Relationships.md)
already shows tags whose role depends on their parent: `rack/unit/panel` builds a resize
panel, `stack/item` an ordinary panel, while `group`, `deck` and `setdeck` flatten into their
owner.

1. Resolve the window's separate initialization, which the checkpoint lists as unresolved.
2. Map the factory's dispatch: tag to class, alias and case handling, and the default and
   custom-class branches. Recognizing a name is a separate claim from creating an object.
3. Give every name reached through a named child lookup or wrapper a role (object, child
   slot, wrapper or directive) and the class it produces in each parent context.

Done when every tag the 9246 factory and named child lookups recognize has a role and a
code-path reference, and every dispatch branch that is not resolved is listed as such.

Progress (2026-10-02): steps 1 and 2 are done; step 3 is partial. The window binds through
`CSkinWindow::load`. `just skin-dispatch` holds the factory's gates, comparison rule,
selectors and directives, the reviewed container loaders, and every name-matching site
with its role. What is left is listed by `just skin-dispatch --unresolved`, plus the child
lookups with role `unknown` and the tag compares in functions not yet reviewed. Findings:
[Skin Tag Dispatch](docs/Skin%20Tag%20Dispatch.md).

### V2. Recover each verb's argument syntax from its named consumer

Status: Ready

Note: The keyword candidates in `tests/action-contracts.json` say which literals a verb
compares against, but not at which position, nor how arguments are fetched. The named 9246
`ACTION_*` methods (`tests/action-vtables-9246.json`) can answer that per verb:

- which parameter indices it reads, and through which getter (`getParam`, `getParamEval`);
- the conversion it applies to each (`toFloat`, `toString`, boolean helpers);
- the keyword set at each position, and the branch an unrecognized token takes.

Work by shared consumer family, largest first; the shared time reader and `is_using` are
the pilots (`tools/is_using_keywords.py`, [Runtime Memory Probe](docs/Runtime%20Memory%20Probe.md)).
Check every recovered form with the V1 host for its native parameter tags and payloads.
Where `just vdj-up` answers, calibrate a sample per family with `tools/probe_arg_forms.py`
against nonsense controls. That keeps the static reading honest, and it is not a behaviour
claim.

Done when every verb in the 9246 vtable artifact either has its argument syntax recovered or
a named reason it is open: indirect consumer, unresolved helper, inlined fetch, or
conflicting evidence. One query has to answer which verbs are open and why.
Steps A1–A4 of `docs/Verb Tail and Linter Tasks.md` are the
detailed method.

### K2. Recover attributes and children for every element context

Status: Ready

Note: Steps 2–3 of retired task S6, over the K1 inventory. For each element in each parent
context, record:

- its own attributes, with reader, type, default and conversion;
- its direct children and the class each one produces;
- the parents it is accepted under.

Define each shared reader once and reference it from every element that uses it, as the
checkpoint already does. Read beyond the constructors as well: an attribute read only in a
draw, update or query method is still syntax, and a construction-only trace misses it. Where
the static reading is ambiguous, settle it with the watchpoint host
(`just offline-xml-unknowns`) or the child host (`just skin-child-probe`).

Done when every K1 entry is either structurally closed (all reader routes accounted for) or
lists the routes it still has open. Closure is about structure, not rendering.

### K3. Recover template, class, include and condition expansion

Status: Ready

Note: The factory host never sees these rules because the skin loader applies them first.
The [Offline Skin Host](docs/Offline%20Skin%20Host.md) now runs `CSkinEngine::load` through
`loadEnd()`, so the loader stage can be observed. Recover the rules for the template and
class mechanism, includes, and conditional constructs, including plain `group` turning into
a panel when it has `visibility`. Each rule needs paired fixtures in that host: one expanded
form and one control.

Done when every expansion directive the 9246 loader handles has a stated rule and a fixture,
or is listed as unresolved. Whether a condition evaluates to true is a behaviour question
and stays out.

### B1. Carry the recovered syntax to the current build

Status: Ready

Note: Everything above is recovered on 9246, but the installed build is 9644, which has no
symbols and has verbs 9246 lacks (`just verb-table-stamp`). The action classes still map to
verb ids through RTTI on stripped builds (`just verb-contract`), so each consumer can be
paired across builds by its vtable slot and compared by normalized instruction hash.

- A routine that is unchanged keeps its 9246 findings, restamped for 9644.
- A routine that changed is recovered again.
- A verb added after 9246 is recovered without names, or from live probes.

Do this as a pilot first: one verb family and one element family, before V2 and K2 scale
up. That shows whether carrying across is cheap or needs a recovery per build. Done when the
pilot reports its unchanged, changed and new sets, and the method is written down where the
next build can repeat it.

## Parking lot

- **Consumers of the result.** Linters driven by the recovered syntax instead of the corpus,
  a Rust port, a skin previewer on the offline host. Revisit once V2 and K2 close.
- **Behaviour.** Live confirmation of what verbs do and how elements render. Start from the
  relevant block in [RETIRED.md](RETIRED.md).
