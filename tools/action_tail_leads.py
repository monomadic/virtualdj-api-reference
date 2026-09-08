#!/usr/bin/env python3
"""Rank Tier-2 verb literal leads; historical names annotate slots, never addresses.

Regenerate after action-contracts, action-catalog and binary-vocabularies.
Uses committed b9246 symbol/STABS artifacts by class spelling only. Direct helper
literals remain co-occurrence leads: no argument-to-comparison dataflow is proved.
Query output is JSON; no Markdown mirror or verb-store status promotion.

Two joins keep the queue honest, and they live on different sides of the artifact:

* **Helper fan-out** is binary-derived and baked in. A helper reached by many
  unrelated ACTION_ classes can be the script evaluator's own dispatch rather
  than one verb's argument matcher, and its literal dump would otherwise
  outrank the specific finds. `helper_stats` measures both signals per helper
  and labels the dispatchers; their literals are ranked separately and never
  counted as recovering a worklist tail.
* **The verb store is live state, so it is joined at query time**, never
  hashed into the artifact. The catalog cross-check knows what the arg-form
  prober confirmed; it does not know what was settled through the store and the
  tracker, so it keeps offering tails that are already closed. Tokens a tested
  record quotes in its evidence move to `recorded_worklist_tails` and the verb
  drops out of priority 0. Recorded means *observed*, not *confirmed*: the
  negative results belong there too ("'siren' is the doc's example file, not
  vocabulary"), because neither is fresh probe work. The exception is an
  evidence entry that calls its own result UNDISCRIMINATED — the token was
  probed and did not separate, so it stays open and carries the flag.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verbdb  # noqa: E402  (store API; the JSON layout stays behind it)

ARTIFACT = Path('tests/action-tail-leads.json')
INPUTS = ['action-contracts', 'action-catalog', 'binary-vocabularies',
          'action-modules-9246', 'action-vtables-9246']
# Calibrated on build 18.0.9598, where the two signals separate cleanly and
# neither does alone: the pad helper is shared by 4 classes but holds 4
# literals of which 25% are verb ids, the song-field helper holds 63 literals
# for 3 classes at 16%, and the evaluator dispatch is 12 classes at 71%.
DISPATCHER_FANOUT = 4
DISPATCHER_VERB_ID_FRACTION = 0.5
# A tested status only accounts for a tail the evidence names as a token. House
# style quotes them ('min', 'sec'); prose that merely uses the word does not
# count, so an unquoted mention leaves the tail open.
TESTED = {'Pass', 'Fail', 'N/A'}
# The house marker for "probed, did not separate". Entry-scoped on purpose:
# over-keeping a tail costs one probe, dropping a live one costs the finding.
UNRESOLVED = 'UNDISCRIMINATED' 


def helper_stats(contracts):
    """Per helper function: how many classes reach it, and what it holds."""
    verbs, seen = set(contracts['verbs']), {}
    for rec in contracts['verbs'].values():
        for trace in rec['method_traces'].values():
            for helper in trace['helper_keyword_candidates']:
                s = seen.setdefault(helper['function'], {'classes': set(), 'literals': set()})
                s['classes'].add(rec['class'])
                s['literals'].update(helper['names'])
    out = {}
    for fn, s in sorted(seen.items()):
        fraction = round(len(s['literals'] & verbs) / len(s['literals']), 2)
        out[fn] = {'function': fn, 'fanout': len(s['classes']),
                   'literal_count': len(s['literals']),
                   'verb_id_fraction': fraction,
                   'shared_with': sorted(s['classes']),
                   'dispatcher': (len(s['classes']) >= DISPATCHER_FANOUT
                                  and fraction >= DISPATCHER_VERB_ID_FRACTION),
                   'evidence_tier': 2}
    return out


def build():
    data = {n: json.loads(Path(f'tests/{n}.json').read_text()) for n in INPUTS}
    contracts = data['action-contracts']
    work = data['action-catalog']['cross_check']['documented_but_not_probe_confirmed']
    modules = {v: m for m, vs in data['action-modules-9246']['modules'].items() for v in vs}
    helpers = helper_stats(contracts)
    rows = []
    seen = set()
    for verb, rec in sorted(contracts['verbs'].items()):
        if rec['class'] in seen:
            continue
        seen.add(rec['class'])
        canonical = rec['class'].removeprefix('ACTION_')
        aliases = [v for v, r in contracts['verbs'].items() if r['class'] == rec['class']]
        pending = sorted({t for v in aliases for t in work.get(v, [])})
        old = data['action-vtables-9246'].get(rec['class'], [])
        leads = []
        for slot, trace in rec['method_traces'].items():
            for helper in trace['helper_keyword_candidates']:
                stat = helpers[helper['function']]
                leads.append({**{k: v for k, v in helper.items() if k != 'names'},
                              'names': sorted(set(helper['names'])),
                              'slot': int(slot), 'root': trace['root'],
                              'helper_fanout': stat['fanout'],
                              'dispatcher': stat['dispatcher'], 'evidence_tier': 2})
        own = rec.get('keyword_candidates', [])
        groups = {name: {'members': group['members'], 'member_signals': group['member_signals'],
                         'association': {v: group['verbs'][v] for v in aliases if v in group['verbs']},
                         'evidence_tier': 2}
                  for name, group in data['binary-vocabularies']['groups'].items()
                  if any(v in group['verbs'] for v in aliases)}
        specific = {n for r in leads if not r['dispatcher'] for n in r['names']}
        dispatched = {n for r in leads if r['dispatcher'] for n in r['names']}
        # A dispatcher dump never counts as recovering a documented tail.
        names = set(own) | specific
        if not names and not dispatched and not pending and not groups:
            continue
        query = rec['queries'] or rec['query_bool'] or rec['query_text']
        rows.append({'verb': canonical, 'aliases': aliases,
                     'priority': 0 if pending else 1,
                     'worklist_tails': pending,
                     'worklist_recovered': sorted(set(pending) & names),
                     'own_keyword_candidates': own, 'helper_leads': leads,
                     'associated_vocabularies': groups,
                     'helper_only_candidates': sorted(specific - set(own)),
                     'dispatcher_candidates': sorted(dispatched - set(own) - specific),
                     'shared_helpers': [helpers[fn] for fn in sorted({r['function'] for r in leads})],
                     'historical': {'build': data['action-modules-9246']['summary']['build'],
                                    'module': modules.get(canonical), 'slot_names': old,
                                    'join': 'class spelling and slot index; not current method identity'},
                     'channel': 'delayed plugin GetInfo/GetStringInfo, then HTTP fixture' if query
                                else 'HTTP execute only with allowlist, independent readback and verified restoration',
                     'test': 'Hold attested argument shape fixed; vary one position against bare and two nonsense controls. Record HRESULT separately from value; repeat time-varying reads in independent runs.',
                     'evidence_tier': 2})
    rows.sort(key=lambda r: (r['priority'], not bool(r['worklist_recovered']),
                             not bool(r['helper_only_candidates']), r['verb']))
    dispatchers = [h for h in helpers.values() if h['dispatcher']]
    return {'source': contracts['source'],
            'inputs': {n: hashlib.sha256(Path(f'tests/{n}.json').read_bytes()).hexdigest() for n in INPUTS},
            'summary': {'queue_verbs': len(rows), 'worklist_verbs': sum(r['priority'] == 0 for r in rows),
                        'helper_leads': sum(len(l['names']) for r in rows for l in r['helper_leads']),
                        'helper_records': sum(len(r['helper_leads']) for r in rows),
                        'helper_functions': len(helpers), 'dispatcher_helpers': len(dispatchers),
                        'dispatcher_leads': sum(len(l['names']) for r in rows
                                                for l in r['helper_leads'] if l['dispatcher'])},
            'limitations': contracts['limitations'] + [
                'Historical symbols and STABS partitions already exist; no cross-build address mapping is inferred.',
                'Shared vocabulary groups and pointer tables remain available through just binary-vocab --verb NAME; membership is not a call-path proof.',
                'Numeric values, durations, names, indices, expressions and other open-value tails require corpus shapes and live probes; an empty literal set proves no absence.',
                'Dispatcher labelling is a ranking signal calibrated on this build, not a verdict: a dispatcher dump can still contain real tails, and a specific helper can still contain UI labels.',
                'Worklist tails come from the catalog cross-check and are filtered against the verb store at query time, so a generated artifact read directly still lists tails already recorded.',
                'A recorded tail is an observation, not a confirmation: the join demotes probed-and-negative tails alongside probed-and-confirmed ones.'],
            'queue': rows}


def recorded_tails(aliases, tails, store):
    """Tails a tested store record already quotes as a token in its evidence."""
    out = {}
    for verb in aliases:
        rec = store.get(verb)
        if not rec or rec.get('test_status') not in TESTED:
            continue
        for index, evidence in enumerate(rec.get('evidence', [])):
            for tail in tails:
                if tail in out:
                    continue
                if re.search(r"""['"`]%s['"`]""" % re.escape(tail), evidence):
                    out[tail] = {'verb': verb, 'test_status': rec['test_status'],
                                 'evidence_index': index, 'read': f'just get-verb {verb}',
                                 'undiscriminated': UNRESOLVED in evidence}
    return dict(sorted(out.items()))


def resolve(d):
    """Join the live verb store: settled tails leave the queue, verbs re-rank."""
    store = verbdb.load_store()
    rows = []
    for row in d['queue']:
        recorded = recorded_tails(row['aliases'], row['worklist_tails'], store)
        still_open = [t for t in row['worklist_tails']
                      if t not in recorded or recorded[t]['undiscriminated']]
        rows.append({**row,
                     'recorded_worklist_tails': recorded,
                     'open_worklist_tails': still_open,
                     'worklist_recovered': sorted(set(still_open) & set(row['worklist_recovered'])),
                     'priority': 0 if still_open else (1 if not row['worklist_tails'] else 2)})
    rows.sort(key=lambda r: (r['priority'], not bool(r['worklist_recovered']),
                             not bool(r['helper_only_candidates']), r['verb']))
    return {**d, 'queue': rows,
            'store_join': {'recorded_verbs': sum(1 for r in rows if r['recorded_worklist_tails']),
                           'recorded_tails': sum(len(r['recorded_worklist_tails']) for r in rows),
                           'open_worklist_verbs': sum(1 for r in rows if r['priority'] == 0),
                           'rule': "a tested store record quoting the tail as a token accounts for it, "
                                   "negative results included; an entry marked UNDISCRIMINATED does not. "
                                   "Unquoted prose never counts, and the store is read live rather than hashed"}}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--generate', action='store_true')
    p.add_argument('--get')
    p.add_argument('--queue', action='store_true')
    p.add_argument('--check', action='store_true')
    a = p.parse_args()
    d = build() if a.generate or a.check else json.loads(ARTIFACT.read_text())
    if a.check:
        if d != json.loads(ARTIFACT.read_text()):
            raise SystemExit('action-tail-leads stale: regenerate')
        print('action-tail-leads reproducibility check passed')
        return
    if not a.generate:
        d = resolve(d)
    if a.get:
        d = next((r for r in d['queue'] if a.get in r['aliases']), {'verb': a.get, 'leads': []})
    elif not a.generate and not a.queue:
        d = {k: v for k, v in d.items() if k != 'queue'}
    print(json.dumps(d, indent=1, sort_keys=True))


if __name__ == '__main__':
    main()
