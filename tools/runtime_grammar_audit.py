"""Join reviewed H4 branch families to exact capture rows; never infer branch coverage."""
import hashlib
import json
from collections import Counter
from pathlib import Path
from runtime_grammar_probes import separation, check_capture

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / 'tests/runtime-grammar-obligations.json'


def report():
    plan = json.loads(PLAN.read_text())
    manifest_path = ROOT / 'tests/runtime-parser-9246/manifest.json'
    manifest = json.loads(manifest_path.read_text())
    captures = {}

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
        evidence = []
        for source in obligation['sources']:
            capture = read_capture(source['capture'])
            matches = [c for c in capture['cases'] if c['group'] == source['group']]
            assert matches, source
            for case in matches:
                evidence.append({'capture': source['capture'], 'case': case['id'],
                    'fixture': case['fixture'], 'build': capture['summary']['build'],
                    'script': case['script'], 'verdict': case['verdict'],
                    'separation': separation(case) if capture['summary']['status'] == 'complete' else 'not-run'})
        rows.append({**obligation, 'evidence': evidence,
                     'result_counts': dict(Counter((e['verdict'] + '/' + e['separation']) for e in evidence))})
    corpus = []
    for ref in plan['editor_corpus']:
        capture = read_capture(ref['capture'])
        case = next(c for c in capture['cases'] if c['id'] == ref['case'])
        corpus.append({**ref, 'fixture': case['fixture'], 'script': case['script'],
                       'status': 'needs-screenshot-backed-span-or-guard-observation'})
    return {'scope': plan['scope'], 'binary_build': manifest['source']['bundle_version'],
            'completion_claim': False, 'obligations': rows, 'editor_corpus': corpus,
            'symbols_without_family_mapping': sorted(set(manifest['symbols']) - {o['symbol'] for o in rows})}
