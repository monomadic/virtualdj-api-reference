#!/usr/bin/env python3
"""Reproduce the post-cleanup linked SID; audit an offline extra.db snapshot.

This deliberately does not claim to port CTagEngine::cleanup. --prepared means
artist/title/remix already have the values passed to SDBInfo::getSID().
Audit compares that stage against stored metadata and reports only aggregates.
"""
import argparse
import datetime
import hashlib
import json
import sqlite3
from pathlib import Path

ARTIFACT = Path(__file__).resolve().parents[1] / 'tests/linked-sid-9246.json'
MASK = (1 << 64) - 1


def load_evidence():
    return json.loads(ARTIFACT.read_text())


def reduce_field(value, evidence):
    """Port strAddReduced for valid Unicode text (C strings stop at NUL)."""
    tables = {table['first_codepoint'] + i: byte
              for table in evidence['unicode_tables']
              for i, byte in enumerate(bytes.fromhex(table['bytes_hex']))}
    output = bytearray()
    stop = evidence['literals']['stop_characters']['text']
    for index, char in enumerate(value):
        cp = ord(char)
        if char == '\0' or char in stop or value.startswith('www.', index):
            break
        if 97 <= cp <= 122:
            output.append(cp - 32)
        elif 65 <= cp <= 90:
            output.append(cp)
        elif cp == 0xdf:
            output.extend(evidence['literals']['sharp_s']['text'].encode())
        elif 0x4e00 <= cp <= 0x9fff or 0xe00 <= cp <= 0xe7f:
            output.extend(char.encode('utf-8'))
        elif 97 <= tables.get(cp, 0) <= 122:
            output.append(tables[cp] - 32)
        # Other ASCII (including digits), unmapped Unicode, combining marks,
        # and nonletter transliterations contribute no bytes.
    return bytes(output)


def calculate(artist, title, remix='', evidence=None):
    evidence = evidence or load_evidence()
    algorithm = evidence['algorithm']
    # The native API consumes NUL-terminated strings, including remix find().
    artist, title, remix = (s.split('\0')[0] for s in (artist, title, remix))
    reduced = reduce_field(artist, evidence) + reduce_field(title, evidence)
    excluded = any(word in remix for word in algorithm['remix_excluded_if_contains'])
    if not excluded:
        reduced += reduce_field(remix, evidence)
    if reduced.decode('utf-8') in algorithm['rejected_reduced_strings']:
        unsigned = 0
    else:
        unsigned = int(algorithm['offset_basis'], 16)
        for byte in reduced:
            unsigned = ((unsigned * int(algorithm['prime'], 16)) ^ byte) & MASK
    return {'sid_signed': unsigned if unsigned < (1 << 63) else unsigned - (1 << 64),
            'sid_unsigned': unsigned, 'sid_hex': f'{unsigned:016x}',
            'reduced_utf8_hex': reduced.hex(), 'remix_excluded': excluded,
            'linkable': unsigned != 0,
            'scope': 'Post-cleanup metadata only; no CTagEngine::cleanup implementation.'}


def audit(snapshot):
    """Offline snapshot only; refuse a WAL that could change the row set."""
    snapshot = snapshot.resolve()
    wal = Path(str(snapshot) + '-wal')
    if wal.exists() and wal.stat().st_size:
        raise ValueError('Use a consistent offline snapshot; nonempty WAL is present')
    before = snapshot.read_bytes()
    evidence = load_evidence()
    db = sqlite3.connect(snapshot.as_uri() + '?mode=ro&immutable=1', uri=True)
    try:
        if db.execute('pragma quick_check').fetchone()[0] != 'ok':
            raise ValueError('Snapshot quick_check failed')
        rows = db.execute('select sid, artist, title, remix from track_data').fetchall()
        matches = sum(calculate(a or '', t or '', r or '', evidence)['sid_signed'] == sid
                      for sid, a, t, r in rows)
        edges, missing = db.execute('''select count(*), coalesce(sum(
            not exists(select 1 from track_data where sid=r.sid1) or
            not exists(select 1 from track_data where sid=r.sid2)),0)
            from related_tracks r''').fetchone()
    finally:
        db.close()
    if snapshot.read_bytes() != before:
        raise ValueError('Snapshot changed during audit')
    return {'observed': datetime.date.today().isoformat(), 'evidence_tier': 2,
            'scope': 'Read-only on-disk snapshot corroboration; row creation build unknown; no live write/readback.',
            'snapshot_sha256': hashlib.sha256(before).hexdigest(),
            'algorithm_source': evidence['source'], 'rows': len(rows), 'matches': matches,
            'mismatches': len(rows)-matches, 'relationship_rows': edges, 'edges_missing_track_data': missing,
            'private_metadata_emitted': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--artist', default='')
    p.add_argument('--title', default='')
    p.add_argument('--remix', default='')
    p.add_argument('--prepared', action='store_true', help='Acknowledge post-cleanup input requirement')
    p.add_argument('--audit', type=Path, metavar='OFFLINE_SNAPSHOT')
    p.add_argument('--evidence', action='store_true', help='Print compact source and algorithm evidence')
    a = p.parse_args()
    if a.audit:
        result = audit(a.audit)
    elif a.evidence:
        e = load_evidence()
        result = {k: e[k] for k in ('source', 'scope', 'algorithm', 'literals')}
    elif a.prepared:
        result = calculate(a.artist, a.title, a.remix)
    else:
        p.error('Use --prepared for post-cleanup metadata, --audit for a snapshot, or --evidence')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
