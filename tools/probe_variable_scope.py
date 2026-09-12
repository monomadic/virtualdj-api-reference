"""Is a bare variable deck-local, `$` global and `@` persistent — or is that folklore?

[VDJScript Grammar](../docs/VDJScript%20Grammar.md) states the three prefixes as
fact in its summary, and H4's remaining work lists variable isolation as never
having been observed. This settles it by writing distinct values through each
prefix and reading them back from a different deck.

Predictions are frozen below, before the run. Every probe variable is named with
a `zzprobe` prefix no shipped script uses, each is set back to 0 afterwards, and
the teardown is verified. `@` variables persist across restarts by claim, so the
run also reports whether the name reaches settings.xml — a persistence claim this
channel can support without a restart.
"""
import argparse
import json
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

SETTINGS = Path.home() / 'Library/Application Support/VirtualDJ/settings.xml'
NAME = 'zzprobescope'
PREFIXES = {'local': NAME, 'global': '$' + NAME, 'persistent': '@' + NAME}

# Frozen predictions, from the claims in VDJScript Grammar's summary.
PREDICTIONS = {
    'bare-is-deck-local':
        'a bare name set on deck 1 and deck 2 holds two independent values',
    'dollar-is-global':
        'a $ name set on deck 1 reads back the same from deck 2',
    'prefixes-are-separate-names':
        'bare, $ and @ forms of one name hold three different values at once',
}


def ask(endpoint, script, timeout=6.0):
    url = f'http://localhost/{endpoint}?' + urllib.parse.urlencode({'script': script})
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read().decode(errors='replace').strip()


def setvar(scope, name, value):
    return ask('execute', f"{scope}set '{name}' {value}".strip())


def getvar(scope, name):
    return ask('query', f"{scope}get_var '{name}'".strip())


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, default=Path('tests/variable-scope-probe-9598.json'))
    a = p.parse_args()

    pids = subprocess.run(['pgrep', '-f', 'MacOS/VirtualDJ'],
                          capture_output=True, text=True).stdout.split()
    if len(pids) != 1:
        raise SystemExit(f'expected one VirtualDJ process, found {pids}')

    capture = {'summary': {'mode': 'variable-scope', 'pid': pids[0],
                           'build': ask('query', 'get_build'), 'channel': 'HTTP',
                           'predictions': PREDICTIONS, 'status': 'running',
                           'claim_scope': 'readbacks for one probe name per prefix; '
                                          'persistence is inferred from settings.xml, not a restart'},
               'observations': {}, 'teardown': {}}
    o = capture['observations']

    # Before anything: the names must not already exist, or a readback proves nothing.
    o['pre_existing'] = {k: getvar(f'deck 1 ', v) for k, v in PREFIXES.items()}

    # Q1 - is a bare name deck-local?
    setvar('deck 1 ', NAME, 11)
    setvar('deck 2 ', NAME, 22)
    o['bare'] = {'deck1': getvar('deck 1 ', NAME), 'deck2': getvar('deck 2 ', NAME),
                 'unscoped': getvar('', NAME)}

    # Q2 - is a $ name global?
    setvar('deck 1 ', PREFIXES['global'], 33)
    o['dollar'] = {'deck1': getvar('deck 1 ', PREFIXES['global']),
                   'deck2': getvar('deck 2 ', PREFIXES['global'])}

    # Q3 - are the three prefixes separate names?
    setvar('deck 1 ', PREFIXES['local'], 1)
    setvar('deck 1 ', PREFIXES['global'], 2)
    setvar('deck 1 ', PREFIXES['persistent'], 3)
    o['namespaces'] = {k: getvar('deck 1 ', v) for k, v in PREFIXES.items()}

    # Q4 - does the @ name reach the settings file, as a persistence claim would need?
    o['persistent_in_settings'] = (
        NAME in SETTINGS.read_text(errors='replace') if SETTINGS.exists() else None)

    for scope in ('deck 1 ', 'deck 2 '):
        for name in PREFIXES.values():
            setvar(scope, name, 0)
    capture['teardown'] = {f'{scope.strip() or "unscoped"}|{name}': getvar(scope, name)
                           for scope in ('deck 1 ', 'deck 2 ')
                           for name in PREFIXES.values()}
    capture['summary']['teardown_clean'] = all(
        v in ('0', '') for v in capture['teardown'].values())
    capture['summary']['status'] = 'complete'
    a.out.write_text(json.dumps(capture, indent=2) + '\n')
    print(json.dumps(capture, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
