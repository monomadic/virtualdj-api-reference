# VDJScript Grammar

The language itself: tokens, chaining, conditionals, quoting, scope. This is the one
document to read *before* writing VDJScript, because none of it is discoverable by
lookup — the parser accepts almost anything and tells you nothing.

Not here: what an individual verb does or which argument forms it honours. Those are
per-verb facts — `just get-verb <name>`, `just find-verbs <term>`.

Provenance is per rule. `HTTP` = the [HTTP control interface](HTTP%20Control%20Interface.md)
on VirtualDJ 2026, 2026-07-22. `Pad` = the
[Grammar Battery](../tests/Pads/Reference%20-%20Grammar%20Battery%20Test.xml) pad run on
v2026-m b9482, 2026-07-14. Where a rule is proven on only one surface, it says so —
[backticks](#backticks-are-a-surface-feature-not-a-parser-feature) are the proof that this
distinction is not pedantic.

## Read this much

Enough to write correct VDJScript. If you are only editing skin layout or XML structure
and not writing script, you can stop after this section.

- **The runtime will never report a syntax error.** Wrong script silently does something
  else. Assume nothing; test it. (The *editor* is a different story — it autocompletes real
  verbs and colours ternary branches by role, so it validates far more than the runtime
  reports. See [the correction below](#correction-2026-07-30-never-reports-describes-the-runtime-not-the-application).)
- `&` **separates statements**, it is not "and". `a & b` runs both.
- **Never put cleanup after a ternary.** In `cond ? a : b & c`, the `& c` belongs to the
  *false branch*. Put unconditional actions first: `c & cond ? a : b`. Each branch takes its
  whole chain, on both sides — see [Conditionals](#conditionals).
- **Ternary branches must be verbs**, not literals. `on ? get_version : get_clock` works;
  `on ? 'A' : 'B'` errors. Neither branch may be empty.
- **A verb's value is not its truth.** `get_version` reports `2026` and is *false* as a
  condition; no slider verb is ever true. 171 of 652 query verbs are traps — check with
  `just verb-return-type <name>` before using one as a condition.
- **Quote any argument containing a space.** `'Beat Grid'` works, bare `Beat Grid` does
  not. Single and double quotes are equivalent; quotes are optional for single tokens.
- **`&&` never guards an action.** `cond && do_thing` runs `do_thing` whatever `cond` is.
  The only guard is a ternary: `cond ? do_thing : nothing`.
- **Store numbers in variables, never strings.** A string-valued variable cannot be read
  back (`get_var` returns blank) *or* compared (`var_equal` returns `yes` against
  everything). Use numeric codes.
- **Backticks only interpolate in XML attribute contexts**, not everywhere.
- **There are no comments.** `//`, `#`, `;`, `--`, `/* */` all silently discard the rest of
  the statement.
- **Variable prefixes are part of the name.** `mode` and `$mode` are different variables.
  `$` = global, `@` = persists across restarts, bare = deck-local.
- In XML, `&` must be written `&amp;`.
- Test any construct in one call: `just vdj-query 'on ? get_version : get_clock'`

## Contents

- [The parser never reports an error](#the-parser-never-reports-an-error)
- [Statements and chaining](#statements-and-chaining)
- [Conditionals](#conditionals)
- [Boolean composition with `&&`](#boolean-composition-with-)
- [Arguments and quoting](#arguments-and-quoting)
- [Variables hold numbers, not strings](#variables-hold-numbers-not-strings)
- [There is no comment syntax](#there-is-no-comment-syntax)
- [Chains stop after exactly 255 statements](#chains-stop-after-exactly-255-statements)
- [Backticks are a surface feature, not a parser feature](#backticks-are-a-surface-feature-not-a-parser-feature)
- [Variable scope prefixes](#variable-scope-prefixes)
- [Deck and scope wrappers](#deck-and-scope-wrappers)
- [XML escaping](#xml-escaping)
- [Testing a construct yourself](#testing-a-construct-yourself)
- [Not yet established](#not-yet-established)

## The parser never reports an error

This is the single most important fact about the language, and the reason every other
section exists. VirtualDJ validates the *head verb* of a statement and essentially nothing
else. Junk in argument position — stray quotes, unbalanced backticks and parens, operator
soup, extra arguments, a nonexistent deck — is silently discarded and the verb runs anyway.

`HTTP`, all returning the normal result of `get_version`:

```
get_version & & & &        get_version ''''''      get_version ```
get_version ) ) ( (        get_version !!!@@@###   get_version 1 2 3 4 5 6
deck 99 get_version        get_version & zzz_bogus
```

Only the leading verb is checked: `zzz_bogus & get_version` errors, while
`get_version & zzz_bogus` returns `2026` — the bogus second statement is dropped in
silence.

Consequences: a working script is no evidence that its syntax is right, and a typo in a verb
argument produces a no-op rather than a complaint. `tools/lint_mappers.py` resolves leading
verbs against the verb index precisely because the *runtime* will not.

### Correction (2026-07-30): "never reports" describes the runtime, not the application

The heading above, and the summary line "nothing you write will be reported as a syntax
error", were written from HTTP and mapper evidence only — the execution path. They are
accurate about that path and every example above still holds. But they were too broad about
**VirtualDJ as a whole**, and the distinction matters:

> VirtualDJ **validates considerably more than it reports.** There are two parsing surfaces.

| Surface | Behavior |
| --- | --- |
| **Runtime** (HTTP, mappers, pads, skins) | Lenient by design. Head verb checked; argument junk discarded; the verb runs. Reports almost nothing. |
| **Editor** (Button Editor / mapper Action box) | Validating. Autocomplete offers only real verbs — all 955 canonical, aliases excluded — and the highlighter colours ternary **structure**, giving the condition, true branch and false branch distinct colours. |

The editor could not colour branches by role unless a structural parser were running as you
type. So the app is not ignorant of malformed script; the failure to *tell you* is a property
of the execution surface, not a limit of VirtualDJ's knowledge. Junk in argument position is
recognised and discarded, not unnoticed.

The practical advice is unchanged: **test everything, because the runtime will not complain.**

**"You cannot lint VDJScript by feeding it to VirtualDJ" stands — tested 2026-07-30.** This
sentence was briefly withdrawn on the theory that the editor might flag unknown verbs. It does
not. `Local test` (Button Editor, screenshots), three scripts differing only in the head verb:

```vdjscript
get_version    ? get_text "A" : get_text "B"   <- real verb
zzz_bogus      ? get_text "A" : get_text "B"   <- nonsense
browser_filter ? get_text "A" : get_text "B"   <- proven not a verb (rule 1b)
```

All three render **identically** — same head-verb colour, same green true branch, same red false
branch. The highlighter parses *shape*, not vocabulary: it will happily colour a well-formed
ternary built entirely from verbs that do not exist.

So the two surfaces divide like this, and neither lints:

| Component | Knows the verb set | Validates structure |
| --- | --- | --- |
| Autocomplete | **yes** — offers exactly the 955 canonical verbs | n/a |
| Highlighter | **no** | **yes** — colours ternary branches by role |
| Runtime | head verb only | no — junk in argument position is discarded |

`tools/lint_mappers.py` therefore remains necessary, and its reason is now sharper: *no* surface
in VirtualDJ will tell you a verb is fake once you have typed it. What the highlighter *is* good
for is mapping grammar — see
[VDJScript Syntax Evidence](VDJScript%20Syntax%20Evidence.md), where branch-role colouring is
being used to settle ternary binding questions that the runtime cannot answer.

Error bodies, when you do get one, are coarse — see the
[HTTP doc](HTTP%20Control%20Interface.md) for the `E_FAIL` vs `E_INVALIDARG` split. `E_FAIL`
does not mean "unknown verb": the official verb `nothing` returns exactly what a bogus name
returns.

## Statements and chaining

`&` is a statement separator. Both sides run; it is not a boolean operator.

```vdjscript
set '$mode' 1 & load_skin
```

In a query context the value of the *first* statement is what comes back: `on & off`
returns `yes`, `off & on` returns `no` (`HTTP`). So chaining is for actions; do not chain
to build a condition.

A leading chain splits off before a ternary parses, which is the useful, safe ordering
(`Pad`, `HTTP`):

```vdjscript
set '$mode' 1 & play ? action_a : action_b
```

The `set` runs unconditionally, then the ternary evaluates independently.

## Conditionals

```vdjscript
query ? true_branch : false_branch
```

### A verb's value and its truth are different channels

**This is the biggest trap in the language and it is invisible from the value.** A condition
asks a *boolean* question. It does **not** mean "the value is non-zero" or "the value is
non-empty". `HTTP`, 2026-07-30:

```
get_version                                 -> 2026
get_version ? get_text 'T' : get_text 'F'   -> F      # returns 2026, but is FALSE
```

Swept across all 652 query verbs: **only 106 are boolean-true** in condition position, and
**171 return a value that reads as true while the verb is false**. The pattern is systematic:

| Observed return type | boolean-true |
| --- | --- |
| `float` | **0 / 68** |
| `percent` | **0 / 4** |
| `text` | 2 / 72 |
| `int` | 35 / 145 |
| `bool` | 68 / 334 (the rest are genuinely off at rest) |

By implementation family, **no slider verb is ever boolean-true (0 / 71)**. So `volume` → `1`,
`pitch` → `0.5`, `zoom` → `0.53`, `stem_color` → `white` are all **false** as conditions.

```vdjscript
volume ? action_a : action_b        # WRONG: volume reports 1, but this always takes action_b
get_bpm ? action_a : action_b       # WRONG: same trap
```

Use a verb that is boolean by design (`loaded`, `is_*`, `has_*`, toggles), or make the
comparison explicit:

```vdjscript
param_bigger 'volume' 0.5 ? action_a : action_b
var_equal '$mode' 1 ? action_a : action_b
```

Check any verb before using it as a condition — `just verb-return-type <name>` reports
`boolean_truth` alongside the value, and flags `truthiness_trap` for the 171.

This follows from the typing model in [Plugin SDK](Plugin%20SDK.md): the host exposes a numeric
channel and a text channel, and the boolean a conditional consumes is a third question that most
value-reporting verbs simply do not answer — defaulting to false.

**A trailing chain binds to the false branch** (`Pad`). In `cond ? a : b & c`, `c` runs only
when `cond` is false — observed `a=1 b=0 c=0` when true, `a=0 b=1 c=1` when false. This is
the most common way to get a script wrong, because it reads like `c` always runs.

```vdjscript
cleanup & cond ? action_a : action_b     # correct: cleanup always runs
cond ? action_a : action_b & cleanup     # WRONG: cleanup is part of the false branch
```

**Each branch takes its whole chain** (`HTTP`). With chains on both sides, the taken branch
runs all of it and the other runs none — the trailing-chain rule above is specifically
about a chain that follows the *last* branch, not about chains in general:

```vdjscript
on  ? set '$a' 1 & set '$b' 1 : set '$c' 1 & set '$d' 1   # -> a=1 b=1, c=0 d=0
off ? set '$a' 1 & set '$b' 1 : set '$c' 1 & set '$d' 1   # -> a=0 b=0, c=1 d=1
```

Corroborated independently by the Button Editor's parse hint (`Local test`, 2026-07-30): with
the cursor in each statement of `get_version ? get_text "A" & get_text "B" : get_text "C" &
get_text "D"`, the editor reports `condition: get_version` for A and B, and `condition: not
get_version` for C and D. VirtualDJ's own model is a **per-statement guard**, negated on the
false side — see [VDJScript Syntax Evidence](VDJScript%20Syntax%20Evidence.md).

**Chaining gives you `else if`** (`Local test`, Button Editor parse hint, 2026-07-30).
`a ? b : c ? d : e` is right-associative — `a ? b : (c ? d : e)` — and the guards accumulate
exactly as an else-if ladder should. Reading the editor's per-statement guard for

```vdjscript
get_version ? get_text "A" : get_version ? get_text "B" : get_text "C"
```

gives `get_version` for A, `not get_version & get_version` for B, and
`not get_version & not get_version` for C. So the chain works the way you would hope, and
this is the idiom for multi-way selection:

```vdjscript
var_equal '$mode' 1 ? do_one : var_equal '$mode' 2 ? do_two : do_default
```

Note this is the *chained* form (a ternary in the **false** branch). It is distinct from
nesting a ternary in the **true** branch, below, and the two are frequently confused.

**Nesting associates the standard way** (`Pad`, `HTTP`): `a ? b ? c : d : e` parses as
`a ? (b ? c : d) : e`, so clamped selection composes safely.

```vdjscript
var_equal '$phrase_len' 16 ? phrase_sync 16 : phrase_sync 32
```

**`nothing` is the correct null branch for actions** (`HTTP`). A ternary is the only
construct that actually guards an action:

```vdjscript
var_equal '$mode' 1 ? do_thing : nothing
```

In *query* position `nothing` has no value and errors, so this idiom is action-only.

**Branches must be verbs and must not be empty** (`HTTP`):

| Form | Result |
| --- | --- |
| `on ? get_version : get_clock` | works |
| `on ? 'A' : 'B'` | `error` — literals are not values in branch position |
| `on ? 1 : 2` | `error` |
| `off ? get_version :` | `error:1` — empty branch, taken |
| `on ? : get_version` | `error` — empty true branch |
| `off ? get_version : nothing` | `error` — `nothing` has no query value |

An empty branch only errors when execution reaches it: `on ? get_version :` returns
normally because the false branch is never taken. Do not rely on that.

## Boolean composition with `&&`

**Corrected 2026-07-30 — `&&` is not a distinct operator, and it does not bind into a
conditional.** The previous version of this section said "`&&` is boolean AND over queries, and
it binds tighter than `?`, so `a && b ? c : d` uses `a && b` as the condition", and read
`off && on ? get_version : get_clock` returning `no` as "the ternary never ran". Both were
wrong. They were inferred from returned values alone — exactly the mistake
[Evidence Standards](Evidence%20Standards.md) rule 4 warns about — and two independent checks
refute them.

**Structure** (Button Editor parse hint): in `get_version && get_bpm ? get_text "A" : get_text
"B"` the guard for the true branch is `get_bpm` — *not* `get_version && get_bpm`. Replacing
`&&` with `&` gives byte-identical guards. The condition is only the statement immediately
before the `?`.

**Behaviour** (`HTTP`, action position with independent readback — the ternary *does* run):

| Script | `$a` | `$b` | |
| --- | --- | --- | --- |
| `off && on ? set '$a' 1 : set '$b' 1` | **1** | 0 | true branch taken — condition is `on` |
| `off &  on ? set '$a' 1 : set '$b' 1` | **1** | 0 | identical to `&&` |
| `on  && on ? set '$a' 1 : set '$b' 1` | **1** | 0 | |
| `off && off ? set '$a' 1 : set '$b' 1` | 0 | **1** | false branch — condition is `off` |

So a false left operand does **not** abort anything. `off && on ? …` takes the *true* branch,
because the condition is `on`.

### What `&&` actually changes: which statement's value a query returns

`&` and `&&` are both statement separators. They differ only in the value a *query* reports
(`HTTP`, with `on`→`yes` and `off`→`no` bare):

| Script | Returns | Rule |
| --- | --- | --- |
| `on  & on ? get_version : get_clock` | `yes` | `&` always reports the **first** statement |
| `off & on ? get_version : get_clock` | `no` | " |
| `on  && on ? get_version : get_clock` | `2026` | `&&` with a **true** left reports the **right** |
| `on  && off ? get_version : get_clock` | `06:48 AM` | " (ternary took its false branch) |
| `off && on ? get_version : get_clock` | `no` | `&&` with a **false** left reports the **left** |
| `off && off ? get_version : get_clock` | `no` | " |

That is short-circuit AND semantics applied to the **reported value only** — false-left reports
the left, true-left reports the right — while both statements execute either way. It is a
value-selection rule, not a guard, and it never reaches into a following conditional.

**In action position `&&` does not guard anything** (`HTTP`). This is the dangerous half:

| Script | `$a` after |
| --- | --- |
| `off && set '$a' 1` | **1** |
| `var_equal '$x' 999 && set '$a' 1` (with `$x`=0, so false) | **1** |
| `var_equal '$x' 0 && set '$a' 1` (true) | 1 |
| `var_equal '$x' 999 ? set '$a' 1 : nothing` | 0 |

`&&` in front of an action behaves exactly like `&`: both sides run regardless. Anyone
writing `condition && action` expecting a guard gets the action unconditionally, with no
error. **Use a ternary with a `nothing` false branch.**

This row was always right, and it is now the general case rather than the exception: `&&`
never guards anything, in any position. **Treat `&&` as `&` with a different value-reporting
rule, and use a ternary whenever you mean "only if".**

## Arguments and quoting

Single quotes, double quotes, and no quotes are equivalent for a single-token argument.
Quoting becomes mandatory as soon as the value contains a space (`HTTP`):

```
get_effect_title 'Echo'         -> Echo - Deck 1
get_effect_title "Echo"         -> Echo - Deck 1
get_effect_title Echo           -> Echo - Deck 1
get_effect_title 'Beat Grid'    -> Beat Grid - Deck 1
get_effect_title "Beat Grid"    -> Beat Grid - Deck 1
get_effect_title Beat Grid      -> ''        <- silently wrong
```

The unquoted multi-word case is the trap: it does not error, it returns nothing. Quote
every string argument as a habit.

That equivalence holds for a string argument being *matched* (an effect name). It does not
hold for a **value** being stored, where quoting decides the type — see
[Variables hold numbers, not strings](#variables-hold-numbers-not-strings). `on` and `off`
are real constants that evaluate to `yes`/`no`; `true` and `false` are **not** — they store
nothing (`HTTP`).

Argument *matching* is a per-verb matter, not grammar — effect names are case-insensitive
but not space-insensitive, some verbs require a signed number, some ignore computed
values. Those live on the verb record: `just get-verb <name>`.

## Variables hold numbers, not strings

A numeric or boolean variable round-trips correctly, and quoting distinguishes the types —
`5` and `'5'` are different values (`HTTP`):

```
set '$v' 5    ->  get_var 'yes'/5     var_equal '$v' 5 -> yes    var_equal '$v' '5' -> no
set '$v' on   ->  get_var yes         var_equal '$v' on -> yes
```

A **string** variable is effectively write-only. It cannot be read and it cannot be
compared (`HTTP`, `$v` set to `'apple'`):

| Read attempt | Result |
| --- | --- |
| `get_var '$v'` | `''` — blank, as it is in pad labels too (`Pad`) |
| `var_equal '$v' 'apple'` | `yes` |
| `var_equal '$v' 'banana'` | `yes` ← wrong |
| `var_equal '$v' banana` | `yes` ← wrong |

Once a variable holds a string, `var_equal` returns `yes` against *anything*. So a
string-keyed branch is not just unreadable, it takes the true branch every time and looks
like it works.

**Store numeric codes and branch on those.** `set '$mode' 2` with
`var_equal '$mode' 2 ? … : …`, never `set '$mode' 'reverb'`.

`true` and `false` are not constants — `set '$v' true` stores nothing. Use `on`/`off` or
`1`/`0`.

## There is no comment syntax

Every common comment marker is accepted and **silently discards the rest of the statement**
(`HTTP` — in each case `$a` was set and `$b` was not):

```vdjscript
set '$a' 1 // set '$b' 1      set '$a' 1 # set '$b' 1     set '$a' 1 ; set '$b' 1
set '$a' 1 -- set '$b' 1      set '$a' 1 /*x*/ set '$b' 1
```

There is no way to annotate script inline. Put explanation in the surrounding XML comment
(`<!-- … -->`) or in the file that documents the page.

## Chains stop after exactly 255 statements

**A chain executes its first 255 statements and silently drops the rest.** `/execute` returns
`false` when that happens, so the truncation *is* reported. `HTTP` over **POST**, 2026-07-30,
with per-statement readback (`set '$cN' 1`, then querying each `$cN`):

| Statements sent | `execute` | Statements that ran |
| ---: | --- | ---: |
| 254 | `true` | 254 |
| 255 | `true` | 255 |
| 256 | `false` | **255** |
| 300 (4689 chars) | `false` | **255** |
| 400 (6289 chars) | `false` | **255** |
| 500 (7889 chars) | `false` | **255** |

255 = 2^8 − 1, and it is a **statement count, not a size**: three chains of 4689, 6289 and 7889
characters all cut at exactly the same statement. Keep generated chains under 255, and check
`execute`'s return value if you are anywhere near it.

Two *separate* transport limits sit above this and are easy to mistake for it:

- **GET has a URL-length limit around 2650 characters.** Past it the connection is reset before
  VirtualDJ sees the script, so nothing runs — for transport reasons, not language reasons.
- **POST bodies fail somewhere above ~9500 characters** with a connection reset.

### Correction (2026-07-30) — this section was wrong in four ways

The previous version said a long chain runs **nothing at all** including the first statement,
that `execute` **reports success** anyway, that the boundary was **neither** a character count
nor a statement count, and that GET and POST behaved **identically**. All four were artefacts of
testing over GET: past ~2650 characters the request never arrived, which looks exactly like
"nothing ran". Over POST the real behaviour is visible — partial execution, a `false` return,
and a clean 255-statement cutoff.

A same-day attempt to "sharpen" the ceiling to 172 statements / 2641 characters was the same
mistake once more, and is withdrawn: 2641 characters is where the **GET URL limit** falls for
that statement shape, not where VDJScript stops.

Lesson worth keeping: when a channel and a language limit can produce the same symptom,
distinguish them before measuring — here, by re-running over a different transport.

## Backticks are a surface feature, not a parser feature

`` `verb` `` evaluates and substitutes **in XML attribute string/colour contexts**. It is
not a general argument-evaluation mechanism, and the surface decides whether it works.

Proven not to substitute in HTTP argument position (`HTTP`), with `Echo` — a 6-slider
effect — loaded in slot 1:

```
get_effect_slider_count 'Echo'                 -> 6
get_effect_slider_count `get_effect_name 1`    -> 0     <- no substitution
get_effect_title `get_effect_name 1`           -> ''
```

Proven to work in a pad attribute context (`Pad`): `` set '$dst' `get_var '$src'` `` read
back `42`.

So a construct prototyped over HTTP may behave differently once pasted into a skin, and
vice versa. When a computed argument is needed and backticks are unavailable or ignored,
chain parameters instead — this works on both surfaces tested (`Pad`):

```vdjscript
get_var '$src' & param_multiply 2 & set '$dst'
```

Whether a *given verb* honours a computed argument is per-verb: `loop`, `beatjump`, and
`phrase_sync` ignore them even where the identical literal works. Check the verb record.

## Variable scope prefixes

The prefix is part of the variable's identity. `MyVar` and `$MyVar` are two different
variables, so a global must be set, toggled, and queried with `$` every time.

| Prefix | Scope |
| --- | --- |
| `name`, `#name` | local to the current deck |
| `%name` | local to a logical deck reference such as `deck left` |
| `$name` | global for the session |
| `@name`, `@%name`, `@$name` | persistent across restarts |

```vdjscript
deck 1 set 'mode' 1
toggle '$MyVar'
set '@$layout_4deck' 1 & load_skin
```

For skin-wide or controller-wide state use `$` or `@$`; a bare `set 'mode' 1` reads
differently when the same script later runs in another deck context.

## Deck and scope wrappers

A deck wrapper prefixes a statement and applies to the rest of it, including a conditional
(`HTTP`):

```
deck 1 get_version              -> 2026
deck 2 get_version              -> 2026
deck left get_version           -> 2026
deck 1 on ? get_version : get_clock  -> 2026
deck 99 get_version             -> 2026     <- nonexistent deck, accepted silently
```

`deck 99` is accepted, which is the [no-error rule](#the-parser-never-reports-an-error)
again: an out-of-range deck is not reported. `all_decks get_version` errors — `all_decks`
is action-only and has no query value, so it cannot wrap a query.

### The full target list, and brackets as threads (`Official wiki`, 2026-09-03)

From [the VDJScript wiki page](https://virtualdj.com/wiki/vdjscript.html), fetched
2026-09-03 — the deck wrapper accepts nine targets, four more than this reference had:

`deck 1` … `deck 4`, `deck left`, `deck right`, **`deck leftvideo`**, **`deck rightvideo`**,
`deck all`, **`deck default`**, `deck active`. Without a wrapper a verb applies to the default
or controller-mapped deck.

Two constructs the wiki documents that are not otherwise recorded here:

- **Brackets start a separate execution thread**, which is how a script waits without blocking
  the rest of the line:
  `( wait 1000ms & play_pause ) & action_deck 1 ? deck 2 play_pause : deck 1 play_pause`
- **`while_pressed`** at the end of a statement limits it to the duration of the button press:
  `volume 100% while_pressed`.

Argument units are `ms`, `bt` (beats) and `%`, alongside plain integers and decimals:
`nudge +100ms`, `wait 8bt`, `crossfader 50%`.

`deck leftvideo`, `deck rightvideo` and `deck default` are **not yet locally tested** — they
are recorded here on the wiki's authority alone.

### `deck all` broadcasts on execute and collapses to one deck on query (2026-09-03)

`all` is a deck target beside `1`, `left`, `active` and `master`, and it behaves differently
in the two contexts. **Executing broadcasts to every deck** (`Local test`, four-deck setup,
values restored afterwards):

```
deck all beatlock on   -> deck 1..4 beatlock all read yes
deck all beatlock off  -> deck 1..4 all read no
deck 1 beatlock on     -> only deck 1 reads yes
```

So `deck all play` does start every deck, as the name suggests.

**Querying does not aggregate — it answers from the first deck.** With deck 1 loaded and
deck 2 empty:

```
deck all get_deck    -> 1
deck all loaded      -> yes    (deck 1's answer; deck 2 reads no)
deck all get_title   -> the deck 1 title
```

An unknown target does error here (`deck qqqq loaded` -> `error:-2147467259`), so the target
slot is one of the few places the parser is not silent. Do not read a `deck all` query as
"all decks agree" — it is deck 1's value, and there is no established aggregate-query form.

## What the HTTP query surface will not evaluate (2026-09-03)

Every one of the 1,427 vendor-written snippets in
[tests/vdjscript-corpus.json](../tests/vdjscript-corpus.json) was sent through `/query`
([tools/check_corpus_parses.py](../tools/check_corpus_parses.py), gated in `just check`).
**1,099 parse. Not one contradicts a grammar claim in this document.** The failures map the
channel's boundary instead, and each class is a rule worth knowing:

| Outcome | Count | What it means |
| --- | ---: | --- |
| `parsed` | 1,099 | answered without error |
| `not-implemented` | 152 | `E_NOTIMPL` — verb exists, this form does nothing on this build |
| `other-error` | 97 | non-standard error codes |
| `no-value` | 28 | `E_FAIL` — [silence, not denial](../docs/Evidence%20Standards.md) |
| `surface-gated` | 28 | action-position verbs (`hot_cue 1`, `loop_color 3`, `custom_button 1`) sent to a query surface |
| `pipeline` | 15 | `get_bpm & param_cast` — `param_*` consumes a value flowing down the chain, and HTTP supplies none |
| `structural` | 7 | see below |
| `placeholder` | 1 | `sampler_bank X` — a documentation stand-in |

Re-running with `loop_active` established changed nothing, so these are not missing-state
failures.

**The seven residual cases are all execute-position semantics, verb by verb.** They error under
`/query` while their absolute equivalents answer:

| Vendor form | `/query` | Absolute equivalent | `/query` |
| --- | --- | --- | --- |
| `loop 50%`, `loop 200%` | `E_INVALIDARG` | `loop 4`, `loop 0.5` | `no` |
| `pitch_range +1` | `E_INVALIDARG` | `pitch_range 8` | `no` |
| `sampler_loop +1`, `-1` | `E_INVALIDARG` | `sampler_loop 1` | `yes` |
| `display_time 'elapsed,remain'` | `E_INVALIDARG` | `display_time elapsed` | `no` |

The catalog explains the first row — `loop 200%` *multiplies* the loop size and `loop 50%`
halves it, so they are adjustments, not values, and there is nothing for a query to return. The
`+1` forms are the same shape. Note the comma list is **not** a general rule: `display_time
'elapsed,remain'` is rejected while `browser_window 'folders,songs'` answers normally, so
multi-value tails are per-verb.

So: a relative or multiplying argument is execute-only, and asking a query for one is an error
rather than silence — one of the few places the parser does report a problem.

## What an unrecognized tail does in execute position (2026-09-03)

Under `/query` a bad argument is ignored and the verb answers anyway — `loaded bogusword`
returns `yes`, the [no-error rule](#the-parser-never-reports-an-error) — which is why an
argument can only be confirmed against a nonsense control.

Under `/execute` there is no single rule. Measured on 14 allowlisted settings verbs from
**both** baselines, values restored and verified (`Local test`, 2026-09-03,
[tools/probe_execute_forms.py](../tools/probe_execute_forms.py)); a toggle's signature is
what it reads after the call from `off` and from `on`:

| Verb behaviour | bare | junk tail | Seen on |
| --- | --- | --- | --- |
| **Junk suppresses the action** | flips (`yes`,`no`) | nothing (`no`,`yes`) | 9 of 10 toggles — `beatlock`, `auto_sync`, `auto_match_bpm`, `quantize_all`, `pad_bank2`, `pad_pressure_switch`, `repeat_song`, `djc_shift`, `rane_timecode_enable` |
| **Junk is ignored, action proceeds** | flips (`yes`,`no`) | flips (`yes`,`no`) | `auto_bpm_transition` |

So the practical warning for mappers stands but is verb-specific: a misspelled argument
usually makes the action do **nothing**, and on some verbs it degrades to the bare action
instead. Neither is reported as an error.

Two-baseline measurement is what separates these at all. From a single baseline, `beatlock on`
and `beatlock <junk>` both end up on and look identical; only running from both baselines
distinguishes *set* (`yes`,`yes`) from *flip* (`yes`,`no`) from *no-op* (`no`,`yes`).

### What the execute channel added over the query sweeps

Less than expected, which is itself worth recording. Across those 14 verbs — each probed with
its own recovered candidates plus the 25-token shared lexicon — exactly **one** token appeared
that the query sweeps had not found: `auto_bpm_transition all`, which is the no-op signature
on a verb whose junk tail flips, i.e. `all` is parsed and suppresses the toggle. That is
consistent with [`all` being a target keyword](#deck-all-broadcasts-on-execute-and-collapses-to-one-deck-on-query)
rather than vocabulary belonging to this verb.

*Corrected 2026-09-03, same day:* this section first read that the verbs' own candidates
(`source_original`, `target_current`, `target_original`) "behaved exactly like junk here, so
the query sweep's negative on them is corroborated". **That was wrong, and the error was the
observable, not the data.** The official verbs appendix documents all three as parameters of
`auto_bpm_transition` that force which BPM the transition lands on. The probe watched the
verb's own boolean readback — whether a transition is *running* — which cannot see which BPM
it targets, so a real parameter was indistinguishable from junk by construction.

The lesson generalises past this verb: **a signature test is only as good as its observable.**
Two-baseline signatures answer "did this token change what the verb did to its own state"; a
token that steers *how* an action runs, or that affects a different piece of state, is
invisible to it. Verbs whose tail selects a mode or a target need an observable chosen for that
tail — here, two decks at different BPMs and a readback of the resulting BPM over time. Treat
`tail-ignored-in-execute` as "not visible in this observable", never as "not a parameter".

## XML escaping

Inside XML attributes, `&` must be written `&amp;`:

```xml
<pad action="set '$mode' 1 &amp; load_skin" />
```

This is XML escaping, not VDJScript syntax — it does not apply to the HTTP channel, where
the whole script is URL-encoded instead. `<` and `>` need the usual XML entities too.

## Testing a construct yourself

The fastest way to settle a grammar question is to ask the running app. Queries are
read-only:

```bash
just vdj-query 'on ? get_version : get_clock'
```

Remember what an answer does and does not prove: a returned value means the construct
*evaluated*, not that it parsed the way you intended, and no output at all is far more
often a silently-dropped argument than a rejected script. Prefer probes whose two possible
answers are visibly different — that is why the examples above use `get_version` against
`get_clock` rather than two effects that might both be empty.

## Not yet established

Do not guess in these gaps; test and record.

- **`while_pressed` release behaviour.** It is accepted both trailing and mid-chain, and
  mid-chain it does not block the rest (`set '$a' 1 while_pressed & set '$b' 1` set both,
  `HTTP`). What happens on *release* cannot be tested over HTTP — there is no press — so
  the modifier's actual semantics still need a pad or mapper run.
- **Backtick boundaries in nested quoting**: `` param_equal "`get_text 'x'`" "x" ? on : off ``
  — and more usefully, which surfaces interpolate backticks at all, since HTTP does not.
- **The exact chain ceiling** and what drives it (parse buffer? execution budget?).
- ~~**Whether `&&`'s query-position short-circuit is deliberate** or a parse artefact~~ —
  **answered 2026-07-30**: `&&` is not a distinct operator structurally (identical parse to
  `&`, and identical action-position behaviour with readback). It only changes which
  statement's value a query reports. See
  [Boolean composition with `&&`](#boolean-composition-with-).
- **Operator-lookalike names in verb argument position**, e.g. a verb whose parameter is
  literally `on`, where a constant and a value collide. `set` is settled; other verbs are not.


Recording an answer: put the observation in
[VDJScript Local Test Tracker](VDJScript%20Local%20Test%20Tracker.md) with the build and
surface, then promote the rule into the matching section above.
