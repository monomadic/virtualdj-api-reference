#!/usr/bin/env python3
"""What the older installers' vendor text and shipped skins say that the current ones do not.

    python3 tools/diff_vendor_history.py --root /tmp/vdj-history-20260906 \
        --output tests/build-history-2026-09-06/vendor-text-diff.json

Two comparisons, both against the currently installed app, both provenance-stamped
(build, archive, member, exact source text) so a recovered line can be cited:

- `languages.zip` -> `English.xml` -> `<Actions>`: verbs described only in an older
  appendix, descriptions whose text changed, and quoted parameter keywords the current
  text no longer carries (the old keyword may be a still-accepted alias, or a rename —
  that is a probe lead, never a supported-form claim).
- the shipped skin archives: verbs that a historical shipped skin used in a script
  attribute and no current shipped skin uses. `skin2018.zip` stopped shipping after
  9.0.7607, so most of these are its usages.

Every verb name is matched against the current verb table; a token that is a verb
name inside a quoted argument (`sampler_mode 'hold'`) still matches, so read the
snippet, not just the name. Vendor text and vendor script are Tier 2 leads.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_action_catalog import catalog  # noqa: E402

BUILDS = ('5308', '7607', '9246', '9583')
SKIN_ARCHIVES = ('skin.zip', 'skin2018.zip', 'remoteskin.zip', 'videoskinlive.zip',
                 'videoskinbroadcast.zip', 'videoskinkaraoke.zip')
ATTR = re.compile(r'\b(?:action|query|visibility|novisibility|condition|textaction|'
                  r'dblaction|color|text)="([^"]*)"')
TOK = re.compile(r"[a-z][a-z0-9_]+")


def app_for(root: Path, key: str) -> Path:
    apps = list((root / key).glob('vdj.pkg/Payload/*.app'))
    if len(apps) != 1:
        raise RuntimeError(f'Expected one app for {key}, found {len(apps)}')
    return apps[0]


def bundle_version(app: Path) -> str:
    import plistlib
    with open(app / 'Contents/Info.plist', 'rb') as fh:
        return plistlib.load(fh)['CFBundleVersion']


def skin_usages(app: Path, names: set[str]) -> dict[str, list[dict]]:
    """verb -> every (archive, member, attribute value) that mentions it."""
    out: dict[str, list[dict]] = {}
    for archive in SKIN_ARCHIVES:
        path = app / 'Contents/Resources' / archive
        if not path.exists():
            continue
        with zipfile.ZipFile(path) as z:
            for member in z.namelist():
                if not member.lower().endswith('.xml'):
                    continue
                text = z.read(member).decode('utf-8', 'replace')
                for value in ATTR.findall(text):
                    for tok in set(TOK.findall(value)):
                        if tok in names:
                            out.setdefault(tok, []).append(
                                {'archive': archive, 'member': member, 'source': value})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--current', type=Path, default=Path('/Applications/VirtualDJ.app'))
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()

    names = set(json.load(open('tests/verb-table.json'))['verbs'])
    cur_cat = catalog(args.current, 'English.xml')
    cur_build = bundle_version(args.current)
    cur_skin = skin_usages(args.current, names)

    report = {
        'current_build': cur_build,
        'evidence': 'vendor prose and vendor script from installer payloads; Tier 2 leads, no runtime results',
        'samples': {},
        'described_only_historically': {},
        'description_changed': {},
        'documented_parameters_lost': {},
        'skin_usages_lost': {},
    }
    for key in BUILDS:
        app = app_for(args.root, key)
        build = bundle_version(app)
        cat = catalog(app, 'English.xml')
        report['samples'][key] = {'build': build, 'described_verbs': len(cat)}
        for name, entry in cat.items():
            if name not in cur_cat:
                report['described_only_historically'].setdefault(name, {})[build] = entry['text']
                continue
            if entry['text'] != cur_cat[name]['text']:
                report['description_changed'].setdefault(name, {})[build] = entry['text']
            lost = sorted(set(entry['documented_parameters']) - set(cur_cat[name]['documented_parameters']))
            if lost:
                report['documented_parameters_lost'].setdefault(name, {})[build] = lost
        for verb, uses in skin_usages(app, names).items():
            if verb in cur_skin:
                continue
            slot = report['skin_usages_lost'].setdefault(verb, {})
            # one example per (archive, member) per build keeps the file readable
            seen = set()
            for u in uses:
                k = (u['archive'], u['member'])
                if k in seen:
                    continue
                seen.add(k)
                slot.setdefault(build, []).append(u)
    for name, texts in report['description_changed'].items():
        texts['current'] = cur_cat[name]['text']
    report['summary'] = {k: len(report[k]) for k in (
        'described_only_historically', 'description_changed',
        'documented_parameters_lost', 'skin_usages_lost')}
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'current_build': cur_build, **report['summary']}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
