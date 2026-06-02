# Placeholder Star vs Unstar Test

Minimal skin fixture for checking how starred and unstarred define placeholders behave in skin `visibility=""`, `condition=""`, text, and text-action contexts.

Install the whole `PlaceholderConditionTest/` folder into:

```text
~/Library/Application Support/VirtualDJ/Skins/
```

Then select `Reference Placeholder Condition Test` in VirtualDJ. Each test cell has a static label and a green `TRUE` badge that appears only when the tested expression evaluates as true.

The fixture compares paired starred/unstarred placeholders for:

- direct boolean `visibility="[COMPACT]"`
- direct boolean `condition="[COMPACT]"`
- quoted string comparisons with `param_equal '[MODE]' 'compact'`
- numeric equality with `param_equal [FLAG] 1`
- width-style numeric expressions with `[WIDTH]`
- visible text replacement with `text="[LABEL]"`
- visible text-action replacement with `action="[TEXTACTION]"`

Record results with:

```text
Date:
VirtualDJ build:
Install form: expanded folder or zip
Observed TRUE badges:
Visible substitution rows:
Unexpected missing/visible badges:
Follow-up documentation change:
```

These rows are canaries, not recommendations. Do not promote a narrower starred-placeholder rule into the reference until a VirtualDJ build and observed result are recorded.
