#!/usr/bin/env python3
"""Emit frozen H4 action predictions; never learns expectations from captures."""
import json
from pathlib import Path
from runtime_grammar_actions import FIXTURES, PREFIXES, validate

cases = []

def add(name, fixture, tail, expected, hypothesis, contrast_tail, contrast_expected, site):
    prefix = PREFIXES[fixture]
    script = lambda t: prefix + (' ' + t if t else '')
    cases.append(dict(id=name, group=fixture, fixture=fixture, hypothesis=hypothesis,
                      script=script(tail), expected=expected,
                      controls=[script('zzqqx'), script('vvnnz')],
                      contrasts=[dict(script=script(contrast_tail), expected=contrast_expected)],
                      binary_sites=[site]))

z = 'parser_zoom_levels'
base = [['0.25'], ['0.65']]
for name, tail, expected, question in [
    ('float', '0.25', [['0.25'], ['0.25']], 'Does an unsigned decimal set an absolute zoom?'),
    ('plus-float', '+0.25', [['0.5'], ['0.9']], 'Does an explicit plus flag add to the current zoom?'),
    ('minus-float', '-0.25', [['0'], ['0.4']], 'Does an explicit minus flag subtract from current zoom?'),
    ('percent', '25%', [['0.25'], ['0.25']], 'Does percent convert to normalized absolute zoom?'),
    ('plus-percent', '+25%', [['0.5'], ['0.9']], 'Does signed percent retain relative behavior?'),
    ('integer', '1', base, 'Does this consumer reject integer-typed input?'),
    ('integer-zero', '0', base, 'Does integer zero differ from floating zero?'),
    ('float-zero', '0.0', [['0'], ['0']], 'Does floating zero set zoom to zero?'),
    ('upper-clamp', '2.0', [['1'], ['1']], 'Does an absolute decimal above one clamp?'),
    ('lower-clamp', '-2.0', [['0'], ['0']], 'Does a negative relative decimal clamp below zero?'),
    ('comma', '0,25', [['0.25'], ['0.25']], 'Does decimal comma survive into this stateful consumer?'),
    ('milliseconds', '25ms', base, 'Does zoom reject a duration parameter?'),
    ('beats', '25bt', base, 'Does zoom reject a beat-length parameter?'),
    ('bare-default', 'default', base, 'Does a typed default flag differ from quoted text?'),
    ('all-flag', 'all', base, 'Does zoom reject the all flag?'),
    ('value-flag', 'value', base, 'Does zoom reject the value flag without a supplied parameter?'),
    ('backtick', '`constant 0.25`', base, 'Does zoom leave a backtick operand unevaluated?'),
    ('quoted-backtick', "'`constant 0.25`'", base, 'Does quoting a backtick operand still leave zoom unchanged?'),
    ('trailing-text', '0.25 zzqqx', [['0.25'], ['0.25']], 'Does a later ordinary text argument leave the first decimal effective?'),
]:
    contrast = '0.0' if expected != [['0'], ['0']] else '0.25'
    contrast_expected = [['0'], ['0']] if contrast == '0.0' else [['0.25'], ['0.25']]
    add('zoom-'+name,z,tail,expected,question,contrast,contrast_expected,'ACTION_zoom::onExecute@0x1005c9310')

b = 'parser_beatlock_levels'
base = [['no'], ['yes']]
for name, tail, expected, question in [
    ('bare', '', [['yes'], ['no']], 'Does the absent argument toggle each baseline?'),
    ('on', 'on', [['yes'], ['yes']], 'Does the on token set both baselines on?'),
    ('off', 'off', [['no'], ['no']], 'Does the off token set both baselines off?'),
    ('toggle', 'toggle', [['yes'], ['no']], 'Does toggle invert both baselines?'),
    ('integer', '1', [['yes'], ['yes']], 'Does an unsigned integer one set on?'),
    ('zero', '0', [['no'], ['no']], 'Does an unsigned integer zero set off?'),
    ('minus-one', '-1', [['yes'], ['no']], 'Does signed integer input toggle rather than assign?'),
    ('plus-zero', '+0', [['yes'], ['no']], 'Does relative zero toggle rather than set off?'),
    ('plus-one', '+1', [['yes'], ['no']], 'Does relative one toggle rather than set on?'),
    ('float', '1.0', base, 'Does the switch consumer reject a float one?'),
    ('float-zero', '0.0', base, 'Does the switch consumer reject floating zero?'),
    ('percent', '100%', base, 'Does the switch consumer reject a percent parameter?'),
    ('quoted-on', "'on'", base, 'Does quoted on remain text rather than a boolean token?'),
    ('double-quoted-on', '"on"', base, 'Does double-quoted on remain text?'),
    ('default', 'default', base, 'Does the switch reject a default flag?'),
    ('all', 'all', base, 'Does the switch reject an all flag?'),
    ('value', 'value', base, 'Does the switch reject a value flag without supplied value?'),
    ('backtick', '`constant 1`', base, 'Does the switch reject unevaluated backtick text?'),
    ('quoted-backtick', "'`constant 1`'", base, 'Does quoted backtick text remain unevaluated here?'),
    ('punctuation-stop', '#zzqqx', [['yes'], ['no']], 'Does punctuation leave the switch with no parameter, unlike ordinary junk text?'),
]:
    contrast = 'off' if expected != [['no'], ['no']] else 'on'
    ce = [['no'], ['no']] if contrast == 'off' else [['yes'], ['yes']]
    add('switch-'+name,b,tail,expected,question,contrast,ce,'IActionSwitch::onExecute@0x100147f18')

a = 'parser_all_decks_asymmetric'
for name, tail, expected, question in [
    ('bare', '', [['yes']*4, ['no']*4], 'Does absent-argument all-deck dispatch synchronize to the inverse of deck 1, instead of toggling each deck independently?'),
    ('on', 'on', [['yes']*4]*2, 'Does explicit on reach every configured deck?'),
    ('off', 'off', [['no']*4]*2, 'Does explicit off reach every configured deck?'),
    ('toggle', 'toggle', [['yes','no','yes','no'], ['no','yes','no','yes']], 'Does an explicit toggle differ from an absent argument under all-deck dispatch?'),
    ('integer', '1', [['yes']*4]*2, 'Does integer one survive all-deck dispatch?'),
    ('quoted-on', "'on'", FIXTURES[a]['baselines'], 'Does quoted on leave every deck unchanged?'),
]:
    contrast = 'off' if expected != [['no']*4]*2 else 'on'
    ce = [['no']*4]*2 if contrast == 'off' else [['yes']*4]*2
    add('all-decks-'+name,a,tail,expected,question,contrast,ce,'ACTION_all_decks::onExecute@0x1000fe392')

suite = validate(dict(description='Frozen action predictions from 18.0.9246; live results may disagree.', cases=cases))
Path('tests/runtime-grammar-action-cases.json').write_text(json.dumps(suite, indent=2)+'\n')
