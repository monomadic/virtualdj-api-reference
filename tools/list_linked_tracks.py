#!/usr/bin/env python3
"""Print every relationship in VirtualDJ extra.db without changing the database.

Missing track_data endpoints remain visible by SID. This lists stored edges,
not the running application's SID cache. JSON preserves duplicate/reversed rows.
"""
import argparse
import json
import sqlite3
import xml.etree.ElementTree as ET
import sys
import tempfile
from pathlib import Path

DEFAULT_LIBRARY = Path.home() / 'Library/Application Support/VirtualDJ/database.xml'
DEFAULT_DB = Path.home() / 'Library/Application Support/VirtualDJ/extra.db'
SQL = '''
SELECT r.id AS relationship_id,
       r.sid1, a.sid AS found1, a.file AS file1,
       a.artist AS artist1, a.title AS title1, a.remix AS remix1,
       r.sid2, b.sid AS found2, b.file AS file2,
       b.artist AS artist2, b.title AS title2, b.remix AS remix2
FROM related_tracks AS r
LEFT JOIN track_data AS a ON a.sid = r.sid1
LEFT JOIN track_data AS b ON b.sid = r.sid2
ORDER BY r.id
'''


def read_rows(path, immutable=False):
    uri = path.resolve().as_uri() + '?mode=ro' + ('&immutable=1' if immutable else '')
    db = sqlite3.connect(uri, uri=True, timeout=1)
    db.row_factory = sqlite3.Row
    try:
        rows = db.execute(SQL).fetchall()
    finally:
        db.close()
    result = []
    for row in rows:
        endpoints = []
        for n in (1, 2):
            endpoints.append({'sid': row[f'sid{n}'], 'resolved': row[f'found{n}'] is not None,
                              **{k: row[f'{k}{n}'] for k in ('file', 'artist', 'title', 'remix')}})
        result.append({'relationship_id': row['relationship_id'],
                       'track1': endpoints[0], 'track2': endpoints[1]})
    return result


def list_links(path):
    try:
        return read_rows(path), None
    except sqlite3.OperationalError as exc:
        if 'locked' not in str(exc).lower():
            raise
    # VirtualDJ can hold an exclusive lock. Never ignore a nonempty WAL or
    # rollback journal: a plain file copy would not capture that transaction.
    def check_sidecars():
        for suffix in ('-wal', '-journal'):
            p = Path(str(path) + suffix)
            if p.exists() and p.stat().st_size:
                raise ValueError('Database is locked with transaction data present. Close VirtualDJ and retry.')
    check_sidecars()
    before = path.read_bytes()
    check_sidecars()
    if before != path.read_bytes():
        raise ValueError('Database changed while copying. Close VirtualDJ and retry.')
    with tempfile.TemporaryDirectory(prefix='vdj-links-') as directory:
        snapshot = Path(directory) / 'extra.db'
        snapshot.write_bytes(before)
        rows = read_rows(snapshot, immutable=True)
    return rows, 'Database locked: showing a stable on-disk snapshot; unsaved application changes are not included.'


def library_index(database):
    """Map every library track's computed SID to its path.

    `extra.db` only keeps a `track_data` row for tracks VirtualDJ happened to
    record, so most endpoints of a real `related_tracks` set have no metadata at
    all. The SID is computable now, so the library itself can name them: hash
    each `<Song>`'s Author/Title/Remix and look the endpoint up.

    These are RAW tags, not the post-cleanup values `SDBInfo::getSID` receives,
    so a match is evidence and a miss is not — cleanup may have altered the
    fields. First writer wins, since one SID is a metadata equivalence class and
    can legitimately name several files.
    """
    from linked_sid import calculate
    index = {}
    for song in ET.parse(database).getroot().iter('Song'):
        tags = song.find('Tags')
        if tags is None:
            continue
        computed = calculate(tags.get('Author') or '', tags.get('Title') or '',
                             tags.get('Remix') or '')
        if computed['linkable']:
            index.setdefault(computed['sid_signed'], song.get('FilePath'))
    return index


def label(track, index=None):
    if not track['resolved']:
        named = (index or {}).get(track['sid'])
        if named:
            return f"[SID {track['sid']} -> {Path(named).name} (from library tags)]"
        return f"[unresolved SID {track['sid']}: no track_data row]"
    text = ' — '.join(s for s in (track['artist'], track['title']) if s)
    if track['remix']:
        text += f" ({track['remix']})"
    return text or (Path(track['file']).name if track['file'] else f"SID {track['sid']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', type=Path, default=DEFAULT_DB, help='Path to extra.db')
    parser.add_argument('--json', action='store_true', help='Output complete relationship records as JSON')
    parser.add_argument('--resolve-from-library', nargs='?', type=Path, const=DEFAULT_LIBRARY,
                        metavar='DATABASE_XML',
                        help='Name endpoints that have no track_data row by hashing the '
                             'library\'s own raw Author/Title/Remix tags (default: '
                             '~/Library/Application Support/VirtualDJ/database.xml)')
    args = parser.parse_args()
    index = {}
    if args.resolve_from_library:
        try:
            index = library_index(args.resolve_from_library.expanduser())
        except (OSError, ET.ParseError) as exc:
            print(f'Cannot read the library: {exc}', file=sys.stderr)
            return 1
    try:
        rows, note = list_links(args.db.expanduser().resolve())
    except (OSError, ValueError, sqlite3.Error) as exc:
        print(f'Cannot list linked tracks: {exc}', file=sys.stderr)
        return 1
    if note:
        print(note, file=sys.stderr)
    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        for row in rows:
            print(f"#{row['relationship_id']}  {label(row['track1'], index)}"
                  f"  ↔  {label(row['track2'], index)}")
            for n in (1, 2):
                track = row[f'track{n}']
                if track['file']:
                    print(f"  {n}: {track['file']}")
            print()
        missing = [row[f'track{n}']['sid'] for row in rows for n in (1, 2)
                   if not row[f'track{n}']['resolved']]
        named = sum(1 for sid in missing if sid in index)
        tail = f'; {named} of those named from library tags' if index else ''
        print(f'{len(rows)} relationship rows; {len(missing)} endpoints '
              f'without track_data metadata{tail}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
