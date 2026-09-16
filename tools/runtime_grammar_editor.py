"""Join frozen editor-help predictions to separate UI and HTTP observations.

Visible help is an appearance observation, never an acceptance verdict.
"""
import argparse
import hashlib
import json
from pathlib import Path
from runtime_grammar_probes import check_capture, separation

ROOT = Path(__file__).resolve().parents[1]
HTTP = ROOT / 'tests/runtime-grammar-editor-help-http-9598.json'
UI = ROOT / 'tests/runtime-grammar-editor-help-ui-9598.json'


def compare(capture, ui):
    summary = ui['summary']
    assert isinstance(summary.get('screenshots_persisted'), bool), 'missing screenshot retention status'
    assert summary.get('screenshot_provenance'), 'missing screenshot provenance'
    assert summary['status'] == capture['summary']['status'] == 'complete'
    for key in ('build', 'suite', 'suite_sha256'):
        assert summary[key] == capture['summary'][key], key
    assert summary['channel'] == 'agent driving Button Editor UI via CUA'
    assert all(c['fixture'] == summary['fixture'] for c in capture['cases'])
    restoration = ui['restoration']
    if summary['screenshots_persisted']:
        references = [ui['original_evidence'], *restoration['evidence'],
                      *(r['evidence'] for rows in ui['passes'] for r in rows)]
        for reference in references:
            path = (ROOT / reference['path']).resolve()
            assert path.is_relative_to(ROOT / 'tests'), 'screenshot must be under tests/'
            assert path.is_file(), f'missing screenshot: {path}'
            assert hashlib.sha256(path.read_bytes()).hexdigest() == reference['sha256'], 'screenshot hash mismatch'
    assert all(restoration[k] is True for k in ('verified', 'reopened_verified', 'editor_closed'))
    assert restoration['test_scripts_executed'] is False
    assert restoration['action'] == ui['original_action']
    assert restoration['button_name'] == ui['original_button_name']
    required = {s for c in capture['cases'] for s in
                [c['script'], *c['controls'], *(x['script'] for x in c['contrasts'])]}
    passes = ui['passes']
    assert len(passes) == 2
    assert [r['script'] for r in passes[1]] == list(reversed([r['script'] for r in passes[0]]))
    observed = []
    for rows in passes:
        assert len(rows) == len(required)
        assert {r['script'] for r in rows} == required
        assert all(r['source_verified_visually'] is True and r['evidence'] for r in rows)
        assert all(r['help_for'] in ui['help_identifiers'] for r in rows)
        observed.append({r['script']: r['help_for'] for r in rows})
    assert observed[0] == observed[1], 'unstable help observations'
    help_for = observed[0]
    results = []
    for case in capture['cases']:
        prediction = case['editor_prediction']
        checks = {
            'candidate_help': help_for[case['script']] == prediction['help_for'],
            'control_help': all(help_for[s] == prediction['control_help'] for s in case['controls']),
            'contrast_help': all(help_for[c['script']] == prediction['contrast_help'] for c in case['contrasts']),
        }
        results.append({
            'id': case['id'], 'script': case['script'],
            'runtime_verdict': case['verdict'], 'runtime_separation': separation(case),
            'editor_predictions': {k: 'held' if v else 'prediction-not-held' for k, v in checks.items()},
            'observed_help': {s: help_for[s] for s in [case['script'], *case['controls']]},
            'combined_verdict': 'held-in-fixture' if all(checks.values()) and case['verdict'] == 'held-in-fixture' else 'prediction-not-held',
        })
    return {'build': summary['build'], 'fixture': summary['fixture'],
            'scope': summary['scope'],
            'ui_evidence': {k: summary[k] for k in ('screenshots_persisted', 'screenshot_provenance')},
            'restoration_verified': True, 'cases': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='validate provenance and observations; failed predictions remain valid evidence')
    parser.add_argument('--http', type=Path, default=HTTP, help='paired HTTP capture')
    parser.add_argument('--ui', type=Path, default=UI, help='UI observation capture')
    args = parser.parse_args()
    report = compare(check_capture(args.http), json.loads(args.ui.read_text()))
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
