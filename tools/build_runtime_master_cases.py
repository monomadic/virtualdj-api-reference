#!/usr/bin/env python3
"""Freeze the asymmetric-master predictions before the run; originals stay frozen.

Baselines are (selection, master) = (1, 2) then (2, 3), so each hypothesis has
its own two-baseline signature: master ['2','3'], selection ['1','2'],
constant-1 ['1','1'], constant-2 ['2','2'].
"""
import json
from pathlib import Path
from runtime_grammar_master import validate, FIXTURE

FOLLOWS_MASTER = [['2'], ['3']]
FOLLOWS_SELECTION = [['1'], ['2']]
STOPPED = {'deck 1 play': 'no', 'deck 2 play': 'no', 'deck 3 play': 'no', 'deck 4 play': 'no'}

rows = [
    ('master', 'deck master get_deck', FOLLOWS_MASTER,
     'With the master deck pinned away from the selection, does `master` follow the master '
     'deck rather than the selection or a constant deck 1?', {}, 'scope-followup-master'),
    ('active', 'deck active get_deck', FOLLOWS_MASTER,
     'The earlier run saw `active` return 1 while master was also 1; with the two pulled '
     'apart, does `active` track the master deck rather than a constant?', STOPPED, 'scope-active'),
    ('playing', 'deck playing get_deck', FOLLOWS_SELECTION,
     'With no deck playing, does `playing` fall back to the selected deck?', STOPPED, None),
    ('default', 'deck default get_deck', FOLLOWS_SELECTION,
     'Does explicit default still follow the selection when the master deck is elsewhere?',
     {}, 'scope-default'),
    ('bare', 'get_deck', FOLLOWS_SELECTION,
     'Does the unscoped query still follow the selection when the master deck is elsewhere?',
     {}, 'scope-bare'),
    ('left', 'deck left get_deck', [['1'], ['1']],
     'Does `left` stay on deck 1 regardless of selection and master?', {}, 'scope-left'),
    ('right', 'deck right get_deck', [['2'], ['2']],
     'Does `right` stay on deck 2 regardless of selection and master?', {}, 'scope-right'),
    ('leftvideo', 'deck leftvideo get_deck', [['1'], ['1']],
     'Does `leftvideo` resolve to the left deck rather than the selection or master?', {}, None),
    ('rightvideo', 'deck rightvideo get_deck', [['2'], ['2']],
     'Does `rightvideo` resolve to the right deck rather than the selection or master?', {}, None),
] + [
    (f'mixer{n}', f'deck mixer{n} get_deck', [[str(n)], [str(n)]],
     f'Does `mixer{n}` name mixer channel {n} independently of selection and master?', {}, None)
    for n in (1, 2, 3, 4)
]

manifest = json.loads(Path('tests/runtime-parser-9246/manifest.json').read_text())
sites = [label + '@' + manifest['symbols'][label]['start']
         for label in ['getDeck', 'IAction::deckMatch']]

cases = []
for name, script, expected, hypothesis, context, prior in rows:
    # The oracle must predict something this case does not, or it proves nothing.
    contrast = [['3'], ['3']] if expected != [['3'], ['3']] else [['4'], ['4']]
    case = dict(id='master-scope-' + name, fixture=FIXTURE, group='master-scope', script=script,
                expected=expected, hypothesis=hypothesis, required_context=context,
                controls=['deck zzqqx get_deck', 'deck vvnnz get_deck'],
                contrasts=[dict(script='deck ' + contrast[0][0] + ' get_deck', expected=contrast)],
                binary_sites=sites)
    if prior:
        case['prior_case'] = prior
    cases.append(case)

out = Path('tests/runtime-grammar-master-cases.json')
out.write_text(json.dumps(validate({'cases': cases}), indent=2) + '\n')
print(f'{len(cases)} cases -> {out}')
