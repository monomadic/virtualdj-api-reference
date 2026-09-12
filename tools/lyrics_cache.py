#!/usr/bin/env python3
"""Read-only lyric cache inspection and recovered AudioSig/LID conversions.

Fingerprint input is a JSON array of raw Chromaprint uint32 words. It must be
VirtualDJ's selected fingerprint window, not a compressed fingerprint string.
This tool does not reproduce audio decoding/window selection or contact servers.
"""
import argparse
import base64
import collections
import datetime
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'tests/lyrics-cache-9246.json'
DEFAULT_DB = Path.home() / 'Library/Application Support/VirtualDJ/extra.db'
NUMBER = r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?'
LINE = re.compile(r'^\[(' + NUMBER + ')-(' + NUMBER + r')\] (.*)$')


def lid_from_words(words):
    if not isinstance(words, list) or any(type(w) is not int or not 0 <= w <= 0xffffffff for w in words):
        raise ValueError('Expected a JSON array of unsigned 32-bit raw fingerprint words')
    n = len(words)
    if not 2 <= n < 8192:
        raise ValueError('Use 2..8191 words for a non-sentinel serializable signature')
    bins = [16 * sum((word >> bit) & 1 for word in words) // (n+1) for bit in range(32)]
    return bytes((bins[i] << 4) | bins[i+1] for i in range(0, 32, 2)) + n.to_bytes(2, 'little')


def lid_from_audiosig(text):
    if text == '':
        return bytes(18)
    if text == '-':
        return bytes(16) + b'\x01\x00'
    # Strict input validation is intentional; native decoder tolerance is not emulated.
    try:
        raw = base64.b64decode(text, altchars=b'-_', validate=True)
    except (ValueError, base64.binascii.Error) as exc:
        raise ValueError('Expected a Base64url AudioSig encoding of exactly 18 bytes') from exc
    if len(raw) != 18 or raw[17] >= 32:
        raise ValueError('AudioSig must decode to 18 bytes with final byte below 0x20')
    return raw


def describe_lid(raw):
    if len(raw) != 18:
        raise ValueError('A lyrics LID must contain exactly 18 bytes')
    n = int.from_bytes(raw[16:], 'little')
    # Matches saveToString's explicit masking of the final byte.
    encoded = base64.urlsafe_b64encode(raw[:17] + bytes([raw[17] & 31])).decode()
    return {'lid_hex': raw.hex(), 'audiosig': '' if n == 0 else '-' if n == 1 else encoded,
            'fingerprint_word_count': n, 'native_cache_eligible': n > 1, 'audiosig_roundtrip_safe': 2 <= n < 8192,
            'histogram_nibbles': [x for byte in raw[:16] for x in (byte >> 4, byte & 15)]}


def parse_payload(text):
    """Lossless timing/text interpretation of well-formed stored lines.

Not a clone of setLyrics' permissive cross-line searches or timing repair.
Negative stored timestamps are preserved, never silently clamped.
"""
    out = {'language': None, 'custom': False, 'no_lyrics': False, 'segments': [], 'unparsed_lines': []}
    for index, line in enumerate(text.split('\n'), 1):
        if not line:
            continue
        if line.upper().startswith('#LANG='):
            out['language'] = line[6:]
        elif line == '#CUSTOM':
            out['custom'] = True
        elif line == '#NOLYRICS':
            out['no_lyrics'] = True
        else:
            match = LINE.fullmatch(line)
            if not match:
                out['unparsed_lines'].append({'line': index, 'text': line})
                continue
            start, end, word = match.groups()
            out['segments'].append({'start': float(start), 'end': float(end), 'text': word,
                                    'line_break_after': word.endswith('\\n'),
                                    'angle_marker': word.startswith('<') and word.endswith('>')})
    return out


def snapshot_rows(path):
    """An explicit offline snapshot: do not silently bypass active transactions."""
    path = path.expanduser().resolve()
    for suffix in ('-wal', '-journal'):
        side = Path(str(path)+suffix)
        if side.exists() and side.stat().st_size:
            raise ValueError('Use a consistent offline snapshot with no nonempty WAL/journal')
    before = path.read_bytes()
    db = sqlite3.connect(path.as_uri()+'?mode=ro&immutable=1', uri=True)
    try:
        if db.execute('pragma quick_check').fetchone()[0] != 'ok':
            raise ValueError('Snapshot integrity check failed')
        rows = db.execute('select lid, xml from lyrics order by lid').fetchall()
    finally:
        db.close()
    if before != path.read_bytes():
        raise ValueError('Snapshot changed during inspection')
    return rows, hashlib.sha256(before).hexdigest()


def summary(path, library=None):
    rows, sha = snapshot_rows(path)
    shapes, headers, lengths = collections.Counter(), collections.Counter(), collections.Counter()
    totals = collections.Counter()
    for lid, text in rows:
        lengths[len(lid)] += 1
        parsed = parse_payload(text)
        totals['unparsed_lines'] += len(parsed['unparsed_lines'])
        totals['segments'] += len(parsed['segments'])
        totals['negative_timestamp_segments'] += sum(s['start'] < 0 or s['end'] < 0 for s in parsed['segments'])
        totals['angle_marker_segments'] += sum(s['angle_marker'] for s in parsed['segments'])
        totals['line_break_segments'] += sum(s['line_break_after'] for s in parsed['segments'])
        if len(lid) == 18:
            totals['native_cache_eligible_rows'] += describe_lid(lid)['native_cache_eligible']
            totals['audiosig_roundtrip_safe_rows'] += describe_lid(lid)['audiosig_roundtrip_safe']
        for key in ('custom', 'no_lyrics'):
            headers[key] += bool(parsed[key])
        headers['language'] += parsed['language'] is not None
        kind = 'timed' if parsed['segments'] else 'no_lyrics' if parsed['no_lyrics'] else 'language_only' if parsed['language'] is not None and not parsed['unparsed_lines'] else 'other'
        shapes[kind] += 1
    report = {'observed': datetime.date.today().isoformat(), 'evidence_tier': 2,
              'scope': 'Offline cache structure only; row-creation builds unknown; no live behavior proof.',
              'snapshot_sha256': sha, 'algorithm_source': json.loads(EVIDENCE.read_text())['source'], 'rows': len(rows), 'lid_lengths': dict(lengths),
              'payload_kinds': dict(shapes), 'header_rows': dict(headers), 'totals': dict(totals),
              'private_metadata_emitted': False}
    if library:
        import xml.etree.ElementTree as ET
        raw = library.read_bytes()
        keys = {row[0] for row in rows}
        signatures, matching, invalid = 0, set(), 0
        import io
        for _, node in ET.iterparse(io.BytesIO(raw), events=['end']):
            if node.tag == 'Scan' and 'AudioSig' in node.attrib:
                signatures += 1
                try:
                    lid = lid_from_audiosig(node.attrib['AudioSig'])
                    if lid in keys:
                        matching.add(lid)
                except ValueError:
                    invalid += 1
            node.clear()
        report['library_comparison'] = {'xml_sha256': hashlib.sha256(raw).hexdigest(),
                                        'audiosig_attributes': signatures, 'invalid_signatures': invalid,
                                        'matching_lyrics_keys': len(matching)}
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--evidence', action='store_true')
    mode.add_argument('--list', action='store_true', help='List cache keys and metadata without lyric text')
    mode.add_argument('--summary', action='store_true', help='Aggregate statistics, never lyric text')
    mode.add_argument('--lid', help='Inspect an 18-byte key as hex')
    mode.add_argument('--audiosig', help='Decode Scan/@AudioSig')
    mode.add_argument('--fingerprint', type=Path, help='JSON array of raw Chromaprint words')
    mode.add_argument('--payload', type=Path, help='Parse a local UTF-8 lyric payload')
    mode.add_argument('--export-lid', help='Print the exact cached text for this hex LID')
    p.add_argument('--db', type=Path, default=DEFAULT_DB, help='Offline extra.db snapshot')
    p.add_argument('--library', type=Path, help='Optional database.xml for AudioSig-key comparison')
    a = p.parse_args()
    try:
        if a.evidence:
            e = json.loads(EVIDENCE.read_text())
            result = {k: e[k] for k in ('source', 'scope', 'schema', 'literals')}
        elif a.summary:
            result = summary(a.db, a.library)
        elif a.list:
            rows, _ = snapshot_rows(a.db)
            result = []
            for lid, text in rows:
                parsed = parse_payload(text)
                result.append({'lid_hex': lid.hex(), 'language': parsed['language'],
                               'custom': parsed['custom'], 'no_lyrics': parsed['no_lyrics'],
                               'segment_count': len(parsed['segments']),
                               'unparsed_line_count': len(parsed['unparsed_lines'])})
        elif a.export_lid:
            key = bytes.fromhex(a.export_lid)
            describe_lid(key)
            rows, _ = snapshot_rows(a.db)
            for lid, text in rows:
                if lid == key:
                    sys.stdout.write(text)
                    return 0
            raise ValueError('LID not found')
        elif a.payload:
            result = parse_payload(a.payload.read_text())
        else:
            raw = bytes.fromhex(a.lid) if a.lid else lid_from_audiosig(a.audiosig) if a.audiosig is not None else lid_from_words(json.loads(a.fingerprint.read_text()))
            result = describe_lid(raw)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (ValueError, OSError, sqlite3.Error) as exc:
        p.exit(1, f'Lyrics cache: {exc}\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
