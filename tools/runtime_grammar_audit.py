"""Join reviewed H4 branch families to exact capture rows; never infer branch coverage."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from runtime_grammar_probes import separation, check_capture

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / 'tests/runtime-grammar-obligations.json'


def symbol_triage(plan, manifest, manifest_path):
    """Validate review anchors; never turn a disposition into behavioral coverage."""
    review = plan['unmapped_symbol_triage']
    obligations = {r['id'] for r in plan['obligations']}
    unmapped = set(manifest['symbols']) - {r['symbol'] for r in plan['obligations']}
    dispositions = {'investigate-next', 'review-with-existing-family',
                    'context-fixture-needed', 'consumer-specific',
                    'editor-fixture-needed', 'support-only'}
    seen, group_ids, groups = set(), set(), []
    for group in review['groups']:
        assert group['id'] not in group_ids, 'duplicate triage group'
        group_ids.add(group['id'])
        assert group['disposition'] in dispositions
        assert group['structural_interpretation'] and group['next_action']
        assert group['related_obligations'] and set(group['related_obligations']) <= obligations
        assert group['symbols']
        symbols = []
        for row in group['symbols']:
            name = row['symbol']
            assert name in unmapped, 'triage symbol is unknown or already family-mapped'
            assert name not in seen, 'duplicate triage symbol'
            seen.add(name)
            assert bool(row.get('out_of_scope')) == (group['disposition'] == 'support-only'), \
                'out_of_scope reason belongs exactly to support-only symbols'
            symbol = manifest['symbols'][name]
            body = (manifest_path.parent / symbol['file']).read_bytes()
            assert hashlib.sha256(body).hexdigest() == symbol['asm_sha256']
            assert int(symbol['start'], 16) <= int(row['site'], 16) < int(symbol['end_exclusive'], 16)
            instruction = next((line for line in body.decode().splitlines()
                                if line.startswith(row['site'][2:].zfill(16) + '\t')), None)
            assert instruction, 'triage anchor is not an instruction'
            symbols.append({**row, 'instruction': instruction,
                            'assembly': str(manifest_path.parent.relative_to(ROOT) / symbol['file']),
                            'assembly_sha256': symbol['asm_sha256']})
        groups.append({**group, 'symbols': symbols})
    # Family fold-in is navigation: exactly the review-with-existing-family symbols, under
    # exactly the obligations their group names, with no evidence fields attached.
    expected = Counter((ob, s['symbol'], g['id']) for g in review['groups']
                       if g['disposition'] == 'review-with-existing-family'
                       for ob in g['related_obligations'] for s in g['symbols'])
    listed = Counter()
    for obligation in plan['obligations']:
        for row in obligation.get('related_symbols', []):
            assert set(row) == {'symbol', 'triage_group'}, 'related symbol carries more than navigation'
            listed[(obligation['id'], row['symbol'], row['triage_group'])] += 1
    assert listed == expected, 'related_symbols differ from the review-with-existing-family triage'
    return {**review, 'binary_build': manifest['source']['bundle_version'],
            'architecture': manifest['source']['architecture'],
            'binary_sha256': manifest['source']['sha256'],
            'groups': groups, 'live_coverage_claim': False,
            'disposition_counts': dict(Counter(g['disposition'] for g in groups for _ in g['symbols'])),
            'symbols_without_triage': sorted(unmapped - seen)}


def triage_report():
    manifest_path = ROOT / 'tests/runtime-parser-9246/manifest.json'
    return symbol_triage(json.loads(PLAN.read_text()),
                         json.loads(manifest_path.read_text()), manifest_path)


def evaluator_branch_review(plan, manifest, manifest_path):
    """Check a bounded structural partition, never infer live branch coverage."""
    review = plan['evaluator_branch_review']
    expected = {'IAction::getParamEval', 'IAction::getFloatParamEval'}
    assert {r['symbol'] for r in review['functions']} == expected
    assert len(review['functions']) == len(expected)
    categories = {'grammar-question', 'context-unmeasured', 'lifecycle-unmeasured',
                  'storage-mechanism', 'ownership-mechanism', 'caller-interface'}
    obligations = {r['id']: r for r in plan['obligations']}
    functions = []
    for row in review['functions']:
        symbol = manifest['symbols'][row['symbol']]
        body = (manifest_path.parent / symbol['file']).read_bytes()
        assert hashlib.sha256(body).hexdigest() == symbol['asm_sha256']
        branches = {}
        for line in body.decode().splitlines():
            match = re.match(r'^([0-9a-f]+)\s+(j[a-z]+)\s+(0x[0-9a-f]+)', line)
            if match and match[2] != 'jmp':
                branches[hex(int(match[1], 16))] = {'mnemonic': match[2], 'target': match[3]}
        assert branches
        assert obligations[row['behavior_obligation']]['symbol'] == row['symbol']
        assigned = [site for group in row['groups'] for site in group['sites']]
        assert len(assigned) == len(set(assigned)), 'duplicate branch classification'
        assert set(assigned) == set(branches), 'conditional branch partition differs from captured body'
        assert len({g['id'] for g in row['groups']}) == len(row['groups'])
        for group in row['groups']:
            assert group['sites'] and group['classification'] in categories
            assert group['structural_interpretation'] and group['remaining_question']
        functions.append({**row, 'assembly_sha256': symbol['asm_sha256'],
                          'conditional_branches': branches,
                          'classification_counts': dict(Counter(
                              g['classification'] for g in row['groups'] for _ in g['sites']))})
    return {**review, 'functions': functions, 'live_branch_coverage_claim': False}


def report():
    from runtime_parser_branch_routes import load_report
    routes = load_report()
    plan = json.loads(PLAN.read_text())
    manifest_path = ROOT / 'tests/runtime-parser-9246/manifest.json'
    manifest = json.loads(manifest_path.read_text())
    captures = {}

    def validate_edge(edge):
        caller = manifest['symbols'][edge['caller']]
        callee = manifest['symbols'][edge['callee']]
        assert any(c['site'] == edge['site'] and c['target'] == callee['start']
                   for c in caller['direct_calls']), edge
        assembly = (manifest_path.parent / caller['file']).read_bytes()
        assert hashlib.sha256(assembly).hexdigest() == caller['asm_sha256']
        instruction = next(line for line in assembly.decode().splitlines()
                           if line.startswith(edge['site'][2:].zfill(16)))
        assert 'callq' in instruction and callee['mangled'] in instruction, edge

    def read_capture(relative):
        if relative not in captures:
            path = ROOT / relative
            header = json.loads(path.read_text())["summary"]
            if header.get("mode") == "playing-scope-queries":
                from runtime_grammar_playing import check_capture as checker
            elif header.get("mode") == "reversible-actions":
                from runtime_grammar_actions import check_capture as checker
            elif header.get("mode") == "selected-scope-queries":
                from runtime_grammar_scopes import check_capture as checker
            else:
                checker = check_capture
            captures[relative] = checker(path)
        return captures[relative]

    rows = []
    for obligation in plan['obligations']:
        symbol = manifest['symbols'][obligation['symbol']]
        address = int(obligation['site'], 16)
        assert int(symbol['start'], 16) <= address < int(symbol['end_exclusive'], 16)
        assembly = (manifest_path.parent / symbol['file']).read_bytes()
        assert hashlib.sha256(assembly).hexdigest() == symbol['asm_sha256']
        assert obligation['site'][2:].zfill(16).encode() in assembly
        for edge in obligation.get('structural_edges', []):
            validate_edge(edge)
        for edge in obligation.get('caller_evidence', []):
            assert any(caller['symbol'] == edge['symbol'] and
                       any(call['site'] == edge['site'] and call['target'] == obligation['symbol']
                           and call['verified_instruction'] for call in caller['calls'])
                       for caller in routes['evaluation_callers']['functions']), edge
        for edge in obligation.get('entry_evidence', []):
            assert any(entry['symbol'] == edge['symbol'] and
                       any(route['site'] == edge['site'] and route['callee'] == edge['callee']
                           for route in entry['routes'])
                       for entry in routes['evaluation_entrypoints']), edge
        evidence = []
        for source in obligation['sources']:
            capture = read_capture(source['capture'])
            matches = [c for c in capture['cases'] if c['group'] == source['group']]
            if 'case_ids' in source:
                wanted = source['case_ids']
                assert wanted and len(set(wanted)) == len(wanted), source
                matches = [c for c in matches if c['id'] in wanted]
                assert {c['id'] for c in matches} == set(wanted), source
            assert matches, source
            for case in matches:
                evidence.append({'capture': source['capture'], 'case': case['id'],
                    'fixture': case['fixture'], 'build': capture['summary']['build'],
                    'script': case['script'], 'verdict': case['verdict'],
                    'separation': separation(case) if capture['summary']['status'] == 'complete' else 'not-run'})
        # An obligation with no live case is a named limit, never a silent gap or a pass.
        limit = obligation.get('limit')
        if not evidence:
            assert limit and limit['status'] == 'blocked', obligation['id']
            assert all(limit.get(k) for k in ('binary_shows', 'why_not_testable_now', 'unblock', 'affects')), obligation['id']
        else:
            assert limit is None, 'limit on an obligation with evidence: ' + obligation['id']
        rows.append({**obligation, 'evidence': evidence,
                     'result_counts': dict(Counter((e['verdict'] + '/' + e['separation']) for e in evidence))})
    corpus = []
    for ref in plan['editor_corpus']:
        capture = read_capture(ref['capture'])
        case = next(c for c in capture['cases'] if c['id'] == ref['case'])
        corpus.append({**ref, 'fixture': case['fixture'], 'script': case['script'],
                       'status': 'needs-screenshot-backed-span-or-guard-observation'})
    return {'scope': plan['scope'], 'binary_build': manifest['source']['bundle_version'],
            'unmapped_symbol_triage': symbol_triage(plan, manifest, manifest_path),
            'evaluator_branch_review': evaluator_branch_review(plan, manifest, manifest_path),
            'branch_route_review': {k: v for k, v in routes.items() if k not in ('remote_mode_writers', 'evaluation_callers', 'evaluation_entrypoints')},
            'evaluation_entrypoints': [{k: v for k, v in entry.items() if k != 'assembly'}
                                      for entry in routes.get('evaluation_entrypoints', [])],
            'evaluation_callers': [{k: v for k, v in caller.items() if k != 'assembly'}
                                   for caller in routes.get('evaluation_callers', {}).get('functions', [])],
            'mode_writer_symbols': [w['symbol'] for w in routes['remote_mode_writers']],
            'completion_claim': False, 'obligations': rows, 'editor_corpus': corpus,
            'symbols_without_family_mapping': sorted(set(manifest['symbols']) - {o['symbol'] for o in rows})}
