#!/usr/bin/env python3
"""Emit selected-scope predictions, independent of live result artifacts."""
import json
from pathlib import Path
from runtime_grammar_scopes import validate, FIXTURE

cases=[]
for name,script,expected,question,site in [
 ('bare','get_deck',[['1'],['2']],'Does the default query follow the selected deck?','getDeck@0x10047dab0'),
 ('default','deck default get_deck',[['1'],['2']],'Does explicit default follow selection?','getDeck@0x10047da36'),
 ('out-of-range','deck 99 get_deck',[['1'],['2']],'Does an out-of-range numeric deck fall back to selection rather than always deck 1?','getDeckSafe@0x10047e085'),
 ('zero','deck 0 get_deck',[['1'],['2']],'Does numeric zero select the default context?','getDeck@0x10047da05'),
 ('one','deck 1 get_deck',[['1'],['1']],'Does explicit deck 1 remain independent of selected deck?','getDeck@0x10047dabe'),
 ('two','deck 2 get_deck',[['2'],['2']],'Does explicit deck 2 remain independent of selected deck?','getDeck@0x10047dabe'),
 ('left','deck left get_deck',[['1'],['1']],'Does left stay on deck 1 in this skin despite changing selection?','getDeck@0x10047db0d'),
 ('right','deck right get_deck',[['2'],['2']],'Does right stay on deck 2 in this skin despite changing selection?','getDeck@0x10047dacd'),
 ('active','deck active get_deck',[['1'],['2']],'Does active follow selection with all decks unloaded and stopped?','getDeck@0x10047db02'),
 ('zone','zone 2 get_deck',[['2'],['2']],'Does zone 2 dispatch independently of the selected deck?','IAction::deckMatch@0x10059c6a4'),
 ('quoted',"deck '2' get_deck",[['error:-2147467259']]*2,'Does quoting a deck number fail in both selected contexts?','IAction::deckMatch@0x10059c6a4'),
 ('backtick','deck `constant 2` get_deck',[['2'],['2']],'Does a computed deck prefix resolve to its returned number in both contexts?','IAction::getDeckFromString@0x100597000'),
 ('numeric-junk','deck 2zzqqx get_deck',[['error:-2147467259']]*2,'Does junk adjacent to the deck number fail rather than use its numeric prefix?','numberMatch@0x10059c5cb'),
]:
 # Link each hypothesis to a bounded body even where this file does not claim a decoded branch.
 manifest=json.loads(Path('tests/runtime-parser-9246/manifest.json').read_text())
 label=site.split('@')[0]
 site=label+'@'+manifest['symbols'][label]['start']
 contrast='deck 3 get_deck'; ce=[['3'],['3']]
 cases.append(dict(id='scope-'+name,group='selected-scope',fixture=FIXTURE,hypothesis=question,
    script=script,expected=expected,controls=['deck zzqqx get_deck','deck vvnnz get_deck'],
    contrasts=[dict(script=contrast,expected=ce)],binary_sites=[site]))
suite=validate(dict(description='Predictions for selection fixture; not selector facts.',cases=cases))
Path('tests/runtime-grammar-scope-cases.json').write_text(json.dumps(suite,indent=2)+'\n')
