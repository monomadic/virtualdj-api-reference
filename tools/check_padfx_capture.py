#!/usr/bin/env python3
"""Check the fixed 9644 padfx evidence, including its separately recovered boundary."""
import json
from pathlib import Path
from probe_padfx_assignments import CASES, EFFECTS, same
ROOT = Path(__file__).resolve().parents[1]

def check():
    data = json.loads((ROOT / 'tests/padfx-assignments-9644.json').read_text())
    boundary = json.loads((ROOT / 'tests/padfx-assignments-9644-boundary.json').read_text())
    assert data['build'] == boundary['build'] == '9644'
    assert data['complete'] is False and data['error'] == 'timed out'
    assert boundary['boundary'] == data['before']
    assert all(same(boundary['effects'][e], data['originals'][e]) for e in EFFECTS)
    rows = {(r['round'], r['name']): r for r in data['cases']}
    assert len(rows) == len(data['cases']) == len(CASES) * 2
    for name, effect, tail in CASES:
        for round_number in (1, 2):
            r = rows[round_number, name]
            assert r['script'] == f"deck 2 padfx '{effect}' {tail} on"
            assert r['after']['active'] == 'yes'
            assert same(r['restored'], data['originals'][effect])
        assert rows[1, name]['after'] == rows[2, name]['after']
    def after(name):
        return rows[1, name]['after']
    for name in ('named_percent', 'named_decimal', 'named_alias_case', 'named_reordered'):
        assert [after(name)['sliders'][i] for i in (0, 2, 3)] == [.37, .62, .23]
    assert after('length_beats')['texts'][1] == after('unit_redirect')['texts'][1] == '2 bt'
    assert after('unit_redirect')['sliders'][0] == data['originals']['Echo Out']['sliders'][0]
    for name in ('named_unknown_a', 'named_unknown_b'):
        assert after(name)['sliders'] == data['originals']['Echo Out']['sliders']
    for name in ('malformed_value_a', 'malformed_value_b'):
        assert after(name)['sliders'][0] == 0
    assert after('duplicate_forward')['sliders'][0] == .61
    assert after('duplicate_reverse')['sliders'][0] == .23
    assert after('mixed_named_numeric')['sliders'][1:3] == [.23, .61]
    assert after('mixed_numeric_named')['sliders'][0] == .23
    assert after('mixed_numeric_named')['sliders'][2] == .61
    assert after('full_named')['sliders'][3] == .78
    assert after('reverb_positional')['sliders'] == [.4, .1, .3, .4]
    assert after('button_on')['buttons'][0] == 'yes'
    for name in ('button_off', 'button_unknown_a', 'button_unknown_b'):
        assert rows[1, name]['before']['buttons'][0] == 'yes'
        assert after(name)['buttons'][0] == 'no'
    print('Padfx case membership, repeated observations, expected control changes and restorations verified.')

if __name__ == '__main__':
    check()
