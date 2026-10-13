#!/usr/bin/env python3
"""Choose a named VirtualDJ binary for method discovery.

The installed build is kept visible for a separate current-build comparison.
Never silently substitute a stripped binary for the named discovery source.
"""

from __future__ import annotations

import argparse
import json
import plistlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = ROOT.parent / 'virtualdj-api-reference-resources' / 'unpacked'
CURRENT = Path('/Applications/VirtualDJ.app')


def build(app: Path) -> str:
    return str(plistlib.loads((app / 'Contents/Info.plist').read_bytes())['CFBundleVersion'])


def named(app: Path) -> bool:
    binary = app / 'Contents/MacOS/VirtualDJ'
    result = subprocess.run(['nm', '-arch', 'arm64', '-j', str(binary)],
                            capture_output=True, text=True, check=False)
    return result.returncode == 0 and '__ZN11ISkinObject' in result.stdout


def sources() -> list[dict]:
    rows = []
    for app in sorted(RESOURCES.glob('*/vdj.pkg/Payload/VirtualDJ.app')):
        if (app / 'Contents/MacOS/VirtualDJ').exists():
            rows.append({'app': str(app), 'build': build(app),
                         'arm64_skin_symbols': named(app)})
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--path', action='store_true',
                        help='print only the preferred symbol-rich app path')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    rows = sources()
    named_rows = [row for row in rows if row['arm64_skin_symbols']]
    preferred = max(named_rows, key=lambda row: tuple(map(int, row['build'].split('.')))) if named_rows else None
    current = {'app': str(CURRENT), 'build': build(CURRENT)} if CURRENT.exists() else None
    if args.path:
        if preferred is None:
            parser.error('no symbol-rich arm64 skin binary found; specify a source explicitly')
        print(preferred['app'])
    elif args.json:
        print(json.dumps({'preferred_named': preferred, 'installed_current': current,
                          'historical_sources': rows}, indent=2))
    else:
        print('method discovery:')
        print(f"  {preferred['app']} (build {preferred['build']}, arm64 symbols)"
              if preferred else '  no symbol-rich arm64 skin binary found')
        print('current-build comparison:')
        print(f"  {current['app']} (build {current['build']})" if current else
              '  no installed VirtualDJ found')
        print('Use historical symbols to identify methods; verify addresses and'
              ' behavior separately on the installed build.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
