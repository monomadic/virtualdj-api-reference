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

- **Nothing you write will be reported as a syntax error.** Wrong script silently does
  something else. Assume nothing; test it.
- `&` **separates statements**, it is not "and". `a & b` runs both.
- **Never put cleanup after a ternary.** In `cond ? a : b & c`, the `& c` belongs to the
  *false branch*. Put unconditional actions first: `c & cond ? a : b`.
- **Ternary branches must be verbs**, not literals. `on ? get_version : get_clock` works;
  `on ? 'A' : 'B'` errors. Neither branch may be empty.
- **Quote any argument containing a space.** `'Beat Grid'` works, bare `Beat Grid` does
  not. Single and double quotes are equivalent; quotes are optional for single tokens.
- **`&&` is boolean AND and short-circuits hard**: if the left side is false the whole
  script returns `no` and a following ternary never runs. Use a plain ternary instead.
- **Backticks only interpolate in XML attribute contexts**, not everywhere.
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

Consequences: you cannot lint VDJScript by feeding it to VirtualDJ, a working script is no
evidence that its syntax is right, and a typo in a verb argument produces a no-op rather
than a complaint. `tools/lint_mappers.py` resolves leading verbs against the verb index
precisely because the app will not.

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

**A trailing chain binds to the false branch** (`Pad`). In `cond ? a : b & c`, `c` runs only
when `cond` is false — observed `a=1 b=0 c=0` when true, `a=0 b=1 c=1` when false. This is
the most common way to get a script wrong, because it reads like `c` always runs.

```vdjscript
cleanup & cond ? action_a : action_b     # correct: cleanup always runs
cond ? action_a : action_b & cleanup     # WRONG: cleanup is part of the false branch
```

**Nesting associates the standard way** (`Pad`, `HTTP`): `a ? b ? c : d : e` parses as
`a ? (b ? c : d) : e`, so clamped selection composes safely.

```vdjscript
var_equal '$phrase_len' 16 ? phrase_sync 16 : phrase_sync 32
```

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

`&&` is boolean AND over queries, and it binds tighter than `?`, so `a && b ? c : d` uses
`a && b` as the condition. But it **short-circuits destructively** (`HTTP`):

| Script | Result | |
| --- | --- | --- |
| `on && on ? get_version : get_clock` | `2026` | true branch |
| `on && off ? get_version : get_clock` | `02:15 PM` | false branch, as expected |
| `off && on ? get_version : get_clock` | `no` | **ternary never ran** |
| `off && off ? get_version : get_clock` | `no` | **ternary never ran** |
| `off ? get_version : get_clock` | `02:15 PM` | plain ternary is fine |

A false *left* operand aborts the whole script and yields `no`; the conditional is
discarded. A false right operand behaves normally. Unless you have tested the exact shape,
prefer a plain ternary or a nested one over `&&` in front of a conditional.

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

Argument *matching* is a per-verb matter, not grammar — effect names are case-insensitive
but not space-insensitive, some verbs require a signed number, some ignore computed
values. Those live on the verb record: `just get-verb <name>`.

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

- **Branch extent with chains on both sides**: `play ? a & b : c & d` — whether the true
  branch takes the whole `a & b`.
- **`&&` in action (non-query) position** — everything above is query-context evidence.
- **Operator-lookalike arguments**: verbs or parameters named `on`, `off`, `true`, `false`,
  `nothing` in argument position, where a constant and a value collide.
- **Backtick boundaries in nested quoting**: `` param_equal "`get_text 'x'`" "x" ? on : off ``.
- **`while_pressed` and other trailing modifiers** — placement rules relative to `&` and `?`.
- **Comment syntax**, if any exists.
- **Statement count limits** and whether long `&` chains are truncated.

Recording an answer: put the observation in
[VDJScript Local Test Tracker](VDJScript%20Local%20Test%20Tracker.md) with the build and
surface, then promote the rule into the matching section above.
