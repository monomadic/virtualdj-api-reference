#!/usr/bin/env python3
"""Check saved native object trees and paired controls without vendor execution."""
import json
import offline_parser as base
from probe_skin_composition import fixtures
from check_offline_xml import require


def check():
    data = json.loads((base.ROOT / 'tests/offline-skin-composition-9246.json').read_text())
    prep = data['preparation']
    expected = json.loads(base.manifest_for('18.0.9246').read_text())
    require(data['suite_finished'] and data['all_cases_completed'], 'unfinished suite')
    require(prep['build'] == '18.0.9246' and prep['source_sha256'] == expected['binary_sha256'], 'wrong binary')
    layout_bytes = (base.ROOT / 'tests/skin-composition-layout-9246.json').read_bytes()
    require(base.digest(layout_bytes) == prep['composition_layout_sha256'], 'layout changed')
    require(json.loads(layout_bytes)['binary_sha256'] == prep['source_sha256'], 'layout source mismatch')
    require(prep['composition_host_source_sha256'] == base.digest((base.ROOT / 'tools/plugin/offline_composition_host.cpp').read_bytes()), 'host source changed: recapture required')
    require(prep['composition_cases'] == [list(c) for c in fixtures()], 'prepared cases changed')
    require([(r['name'], r['xml']) for r in data['runs']] == fixtures(), 'missing or changed cases')
    trees = {}
    for row in data['runs']:
        require(not row.get('timeout') and row['returncode'] == 0 and row['completed'], 'worker failed')
        require(not row['stderr'], 'unexpected worker diagnostics')
        events = [json.loads(line) for line in row['stdout'].splitlines()]
        require(events == row['events'], 'raw output mismatch')
        require(events[:4] == [
            {'event': 'sandbox_controls_passed', 'home_read_denied': True, 'outside_write_denied': True, 'network_denied': True},
            {'event': 'guards_passed'}, {'event': 'composition_guards_passed'},
            {'event': 'window_load_result', 'accepted': True},
        ], 'missing guards or load')
        require(events[-1:] == [{'event': 'complete'}], 'missing completion')
        snapshots = events[4:-1]
        require([(e['event'], e['stage']) for e in snapshots] == [('composition', s) for s in ['loaded', 'resized', 'restored']], 'snapshot sequence changed')
        loaded, resized, restored = [e['tree'] for e in snapshots]
        require(loaded == restored, 'layout restoration failed')
        require(loaded['class'] == 'CSkinWindow' and loaded['current_rect'] == [0, 0, 320, 200], 'bad root')
        require(resized['current_rect'] == [0, 0, 640, 400] and resized['definition_rect'] == loaded['definition_rect'], 'resize did not preserve definition rect')
        require([loaded['children'][i]['class'] for i in [0, -1]] == ['CSkinGrabZone', 'CSkinGrabZone'], 'generated grab zones missing')
        require(resized['children'][-1]['current_rect'] == [304, 384, 16, 16], 'native grab-zone layout changed')
        trees[row['name']] = (loaded['children'][1:-1], resized['children'][1:-1])

    expected_rects = {
        'flat': [[10, 15, 30, 20], [100, 50, 60, 25]],
        'expressions': [[80, 40, 30, 20]], 'deck': [[10, 15, 30, 20]],
        'class': [[12, 18, 80, 24]], 'class_override': [[12, 18, 45, 16]],
        'class_partial_override': [[12, 18, 45, 24]], 'class_forward': [[12, 18, 0, 0]],
        'unknown_class': [[12, 18, 45, 16]], 'unknown_wrapper': [],
    }
    for name, rects in expected_rects.items():
        loaded, resized = trees[name]
        require([n['current_rect'] for n in loaded] == rects, name + ': geometry changed')
        require(all(n['class'] == 'CSkinButton' and not n['children'] for n in loaded), name + ': hierarchy changed')
        require(loaded == resized, name + ': unexpected resize behavior')
    for name, child_rect, resized_rect in [
        ('nested', [7, 9, 30, 20], [40, 31, 200, 229]),
        ('nested_relative', [47, 39, 30, 20], [40, 30, 200, 214]),
    ]:
        loaded, resized = trees[name]
        require(len(loaded) == 1 and loaded[0]['class'] == 'CSkinPanel', 'panel hierarchy changed')
        require(loaded[0]['current_rect'] == [40, 30, 200, 100] and resized[0]['current_rect'] == resized_rect, 'panel geometry changed')
        children = loaded[0]['children']
        require(len(children) == 1 and children[0]['class'] == 'CSkinButton' and children[0]['current_rect'] == child_rect, 'nested coordinates changed')
        require(resized[0]['children'] == children, 'child resize changed')
    require(trees['deck'][0][0]['deck_field'] == 1 and trees['flat'][0][0]['deck_field'] == 0, 'deck propagation changed')
    return {'build': '18.0.9246', 'native_composition': 'paired hierarchy, class, coordinate and unknown-name cases verified', 'layout_round_trip': 'all captured trees restored', 'scope': 'offline native observations; live-app parity and general resize semantics unverified'}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
