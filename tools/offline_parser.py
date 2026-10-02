#!/usr/bin/env python3
"""Build-pinned offline parser pilot. Copies only; never launches the installed app.

Preparation and execution are separate. Execution requires a tested macOS sandbox,
uses one bounded worker per case, and never evaluates a parsed action.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import plistlib
import shutil
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'tests/parser-object-layout-9644.json'


def manifest_for(build):
    if build not in ('18.0.9644', '18.0.9246'):
        raise ValueError('unsupported parser build')
    return ROOT / f'tests/parser-object-layout-{build.rsplit(".", 1)[1]}.json'


def guard_header(manifest):
    """Generate addresses and layout from the selected build, never another build."""
    routines = manifest['routines']
    layout = manifest['layout_leads']
    header = '// Generated from the selected build parser manifest.\n'
    header += 'struct Guard { uint64_t address; size_t size; const char* sha256; };\n'
    header += 'static const Guard guards[] = {\n'
    for r in routines.values():
        header += f'    {{{r["start"]}ULL, {int(r["end"],16)-int(r["start"],16)}, "{r["sha256"]}"}},\n'
    header += '};\n'
    header += f'static const uint64_t kParser = {routines["create_candidate"]["start"]}ULL, kVtable = {manifest["expected_vtable"]}ULL, kDelete = {routines["delete_destructor"]["start"]}ULL;\n'
    header += f'static const char* kUUID = "{manifest["image_uuid"]}";\n'
    for name, field in [('kRefcount','refcount_offset'), ('kBegin','parameter_begin_offset'),
                        ('kEnd','parameter_end_offset'), ('kCapacity','parameter_capacity_offset'),
                        ('kStride','parameter_stride')]:
        value = layout[field]
        if type(value) is not int or not 0 < value <= 256:
            raise ValueError('invalid bounded layout')
        header += f'static const size_t {name} = {value};\n'
    return header


def digest(data):
    return hashlib.sha256(data).hexdigest()


def commands(data):
    if len(data) < 32:
        raise ValueError('truncated header')
    header = struct.unpack_from('<IiiIIIII', data)
    if header[0] != 0xfeedfacf or header[1:3] != (0x100000c, 0):
        raise ValueError('expected thin arm64 (not arm64e)')
    end = 32 + header[5]
    if end > len(data):
        raise ValueError('truncated commands')
    rows, p = [], 32
    for _ in range(header[4]):
        if p + 8 > end:
            raise ValueError('truncated command')
        kind, size = struct.unpack_from('<II', data, p)
        if size < 8 or size % 8 or p + size > end:
            raise ValueError('invalid command size')
        rows.append((kind, data[p:p+size]))
        p += size
    if p != end:
        raise ValueError('command count/size disagree')
    return header, rows


def convert(data):
    """Preserve all section bytes and segment indices; reject unfamiliar layouts."""
    h, rows = commands(data)
    kinds = [k for k, _ in rows]
    if h[3] != 2 or kinds.count(0x80000028) != 1 or 0xd in kinds:
        raise ValueError('expected executable with one LC_MAIN and no dylib ID')
    if 0x80000022 not in kinds or 0x80000034 in kinds:
        raise ValueError('pilot expects classic dyld info, not chained fixups')
    segments, sections, initializers = [], [], []
    for kind, raw in rows:
        if kind != 0x19:
            continue
        if len(raw) < 72:
            raise ValueError('short segment')
        name = raw[8:24].rstrip(b'\0').decode()
        vm, size, off, length = struct.unpack_from('<QQQQ', raw, 24)
        n = struct.unpack_from('<I', raw, 64)[0]
        if len(raw) != 72 + 80*n or off + length > len(data):
            raise ValueError('invalid segment/section bounds')
        segments.append((name, vm, size, off, length))
        for i in range(n):
            p = 72 + 80*i
            sn = raw[p:p+16].rstrip(b'\0').decode()
            addr, sz, offset = struct.unpack_from('<QQI', raw, p+32)
            flags = struct.unpack_from('<I', raw, p+64)[0]
            if flags & 255 not in (1, 0xc, 0x12) and sz:
                if not offset or offset+sz > len(data) or not (off <= offset and offset+sz <= off+length):
                    raise ValueError('invalid file-backed section')
                sections.append((offset, sz))
                if sn == '__mod_init_func':
                    if sz % 8:
                        raise ValueError('invalid initializer array')
                    initializers.append({'address': hex(addr), 'file_offset': offset,
                                         'size': sz, 'entry_count': sz//8,
                                         'sha256': digest(data[offset:offset+sz])})
    text = [s for s in segments if s[0] == '__TEXT']
    zero = [s for s in segments if s[0] == '__PAGEZERO']
    if len(text) != 1 or len(zero) != 1 or zero[0][3:] != (0, 0) or not sections:
        raise ValueError('unexpected segment layout')
    kept = []
    for kind, raw in rows:
        if kind == 0x80000028:
            continue
        if kind == 0x19 and raw[8:24].rstrip(b'\0') == b'__PAGEZERO':
            raw = bytearray(raw)
            struct.pack_into('<QQQQ', raw, 24, text[0][1], 0, 0, 0)
        kept.append(bytes(raw))
    name = b'@rpath/libvdj-parser.dylib\0'
    size = (24 + len(name) + 7) & ~7
    kept.append(struct.pack('<IIIIII', 0xd, size, 24, 0, 0x10000, 0x10000) + name + bytes(size-24-len(name)))
    new = b''.join(kept)
    first = min(p for p, _ in sections)
    if 32 + max(len(new), h[5]) > first:
        raise ValueError('insufficient header space')
    result = bytearray(data)
    result[32:32+h[5]] = bytes(h[5])
    result[32:32+len(new)] = new
    struct.pack_into('<IiiIIIII', result, 0, *h[:3], 6, len(kept), len(new), h[6] & ~0x200000, h[7])
    commands(result)
    for p, size in sections:
        if result[p:p+size] != data[p:p+size]:
            raise ValueError('section bytes changed')
    return bytes(result), {'preferred_text': hex(text[0][1]), 'initializers': initializers,
                           'section_bytes_preserved': True, 'first_section_offset': first}


def call(args, **kw):
    result = subprocess.run([str(x) for x in args], capture_output=True, text=True, **kw)
    if result.returncode:
        raise RuntimeError(f'{args[0]} failed: {result.stderr}')
    return result


def prepare(app, work):
    info = plistlib.loads((app / 'Contents/Info.plist').read_bytes())
    manifest = manifest_for(info['CFBundleVersion'])
    expected = json.loads(manifest.read_text())
    original = app / 'Contents/MacOS/VirtualDJ'
    raw = original.read_bytes()
    if digest(raw) != expected['binary_sha256']:
        raise ValueError('binary hash differs from parser layout manifest')
    if info['CFBundleVersion'] != expected['build']:
        raise ValueError('build mismatch')
    work.mkdir(parents=True, exist_ok=False)
    (work / 'bin').mkdir()
    (work / 'Frameworks').mkdir()
    shutil.copytree(app / 'Contents/Frameworks/Breakpad.framework', work / 'Frameworks/Breakpad.framework', symlinks=True)
    (work / 'original.universal').write_bytes(raw)
    call(['lipo', work / 'original.universal', '-thin', 'arm64', '-output', work / 'original.arm64'])
    thin = (work / 'original.arm64').read_bytes()
    converted, report = convert(thin)
    lib = work / 'libvdj-parser.dylib'
    lib.write_bytes(converted)
    call(['codesign', '--force', '--sign', '-', lib])
    call(['codesign', '--verify', '--strict', lib])
    if expected['build'] == '18.0.9246':
        from extract_action_vtables import demangled, symbol_maps
        symbols, vtables = symbol_maps(demangled(lib, 'arm64'))
        retained = {}
        for key, routine in expected['routines'].items():
            if symbols.get(int(routine['start'], 16)) != routine['symbol']:
                raise ValueError('converted image lost named routine: '+key)
            retained[key] = {'symbol': routine['symbol'], 'address': routine['start']}
        if vtables.get('ACTION_is_using', -16) + 16 != int(expected['expected_vtable'], 16):
            raise ValueError('converted image lost named vtable')
        report['retained_named_routines'] = retained
    (work / 'offline_parser_guard.h').write_text(guard_header(expected))
    call(['clang++', '-std=c++17', '-arch', 'arm64', '-I', work, ROOT / 'tools/plugin/offline_parser_host.cpp', '-o', work / 'bin/host'])
    # Deny access to real user data; only this temporary tree may be written.
    home = str(Path.home().resolve())
    profile = '(version 1) (allow default)\n(deny network*)\n(deny file-write*)\n'
    profile += f'(allow file-write* (subpath {json.dumps(str(work))}))\n'
    profile += f'(deny file-read* (subpath {json.dumps(home)}))\n'
    profile += '(deny process-exec)\n'  # Permit just the initial, known host executable.
    profile += f'(allow process-exec (literal {json.dumps(str(work / "bin/host"))}))\n'
    (work / 'sandbox.sb').write_text(profile)
    report.update(build=expected['build'], arch='arm64', source_sha256=digest(raw),
                  thin_sha256=digest(thin), converted_sha256=digest(lib.read_bytes()),
                  host_sha256=digest((work / 'bin/host').read_bytes()),
                  host_source_sha256=digest((ROOT / 'tools/plugin/offline_parser_host.cpp').read_bytes()),
                  converter_source_sha256=digest(Path(__file__).read_bytes()),
                  guard_sha256=digest((work / 'offline_parser_guard.h').read_bytes()),
                  layout_manifest_sha256=digest(manifest.read_bytes()),
                  sandbox_sha256=digest((work / 'sandbox.sb').read_bytes()),
                  sandbox_profile=profile,
                  dependency_files={str(p.relative_to(work)): digest(p.read_bytes()) for p in sorted((work/'Frameworks').rglob('*')) if p.is_file() and not p.is_symlink()},
                  dependency_symlinks={str(p.relative_to(work)): str(p.readlink()) for p in sorted((work/'Frameworks').rglob('*')) if p.is_symlink()},
                  macos=call(['sw_vers']).stdout, compiler=call(['clang++', '--version']).stdout)
    (work / 'preparation.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


def validate_run(row, baseline):
    """No success from exit code alone: require exact event order and native parity."""
    if row.get('returncode') != 0 or row.get('timeout'):
        raise ValueError('worker failed or timed out')
    events = [json.loads(line) for line in row['stdout'].splitlines()]
    mode = row['mode']
    if mode == '--sandbox-check':
        if events != [{'event': 'sandbox_controls_passed', 'home_read_denied': True,
                       'outside_write_denied': True, 'network_denied': True}, {'event': 'complete'}]:
            raise ValueError('missing sandbox controls')
        return
    expected = ['before_dlopen', 'loaded', 'guards_passed']
    if mode != '--load-only':
        expected += ['before_parse', 'case']
    expected += ['complete']
    if [e['event'] for e in events] != expected:
        raise ValueError('incomplete native event sequence')
    if mode == '--load-only':
        return
    n = int(mode)
    actual = events[4]
    if events[3] != {'event': 'before_parse', 'case': n} or actual.get('case') != n:
        raise ValueError('case identity mismatch')
    for key in ('script', 'class', 'parameters', 'released'):
        if actual.get(key) != baseline[n][key]:
            raise ValueError('native comparison failed: '+key)


def baseline_rows():
    from parser_objects import check
    path = ROOT / 'tests/parser-objects-9644.jsonl'
    check(path)
    return path, [json.loads(line) for line in path.read_text().splitlines() if json.loads(line).get('event') == 'case'][:9]


def check_capture(path):
    baseline_path, baseline = baseline_rows()
    capture = json.loads(path.read_text())
    if not capture['complete'] or capture['baseline_sha256'] != digest(baseline_path.read_bytes()):
        raise ValueError('incomplete capture or changed baseline')
    build = capture['preparation']['build']
    manifest = manifest_for(build)
    if capture['preparation']['source_sha256'] != json.loads(manifest.read_text())['binary_sha256']:
        raise ValueError('wrong source binary')
    if 'layout_manifest_sha256' in capture['preparation'] and capture['preparation']['layout_manifest_sha256'] != digest(manifest.read_bytes()):
        raise ValueError('layout manifest changed')
    expected_comparison = 'same_build' if build == '18.0.9644' else 'cross_build'
    if capture.get('comparison_kind', expected_comparison) != expected_comparison:
        raise ValueError('comparison mislabeled')
    if capture.get('baseline_build', '18.0.9644') != '18.0.9644':
        raise ValueError('baseline build mislabeled')
    if [r['mode'] for r in capture['runs']] != ['--sandbox-check', '--load-only'] + [str(i) for i in range(9)]:
        raise ValueError('incomplete fixed suite')
    for row in capture['runs']:
        validate_run(row, baseline)
    return {'build': build, 'baseline_build': '18.0.9644',
            'comparison': 'same-build live baseline' if build == '18.0.9644' else 'cross-build 9644 live baseline; no same-build live parser capture',
            'parse_fields_match_live_baseline': True,
            'scope': 'class, parameter tags/payloads/text, and release; no evaluation comparison'}


def run(work, output):
    if output.exists():
        raise ValueError('capture already exists')
    prep = json.loads((work / 'preparation.json').read_text())
    manifest = manifest_for(prep['build'])
    if prep['source_sha256'] != json.loads(manifest.read_text())['binary_sha256']:
        raise ValueError('unrecognized prepared build')
    if 'layout_manifest_sha256' in prep and prep['layout_manifest_sha256'] != digest(manifest.read_bytes()):
        raise ValueError('layout manifest changed')
    for path, key in [('libvdj-parser.dylib', 'converted_sha256'), ('bin/host', 'host_sha256'), ('sandbox.sb', 'sandbox_sha256')]:
        if digest((work/path).read_bytes()) != prep[key]:
            raise ValueError('prepared artifact changed: '+path)
    for path, sha in prep['dependency_files'].items():
        if digest((work/path).read_bytes()) != sha:
            raise ValueError('dependency changed')
    for path, target in prep.get('dependency_symlinks', {}).items():
        if str((work/path).readlink()) != target:
            raise ValueError('dependency symlink changed')
    baseline_path, baseline = baseline_rows()
    result = {'scope': 'Offline copied-image parser experiment; no GetInfo/evaluation, no live app mutation.',
              'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'baseline_sha256': digest(baseline_path.read_bytes()),
              'baseline_build': '18.0.9644',
              'comparison_kind': 'same_build' if prep['build'] == '18.0.9644' else 'cross_build',
              'preparation': prep, 'runs': [], 'complete': False}
    env = {'PATH': '/usr/bin:/bin:/usr/sbin:/sbin', 'HOME': str(work), 'TMPDIR': str(work)}
    for mode in ['--sandbox-check', '--load-only'] + [str(i) for i in range(9)]:
        args = ['/usr/bin/sandbox-exec', '-f', str(work/'sandbox.sb'), str(work/'bin/host'), str(work/'libvdj-parser.dylib'), mode]
        try:
            p = subprocess.run(args, cwd=work, env=env, capture_output=True, text=True, timeout=20)
            row = {'mode': mode, 'returncode': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}
        except subprocess.TimeoutExpired as e:
            row = {'mode': mode, 'timeout': True, 'stdout': (e.stdout or b'').decode(errors='replace'), 'stderr': (e.stderr or b'').decode(errors='replace')}
        row.update(argv=args, cwd=str(work), environment=env)
        result['runs'].append(row)
        try:
            validate_run(row, baseline)
        except (ValueError, KeyError, IndexError) as e:
            result['stop_reason'] = str(e)
            output.write_text(json.dumps(result, indent=2)+'\n')
            return result
        output.write_text(json.dumps(result, indent=2)+'\n')
    result['complete'] = True
    output.write_text(json.dumps(result, indent=2)+'\n')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode', choices=['prepare', 'run', 'check'])
    p.add_argument('--work', type=Path)
    p.add_argument('--app', type=Path, default=Path('/Applications/VirtualDJ.app'))
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    if a.mode == 'check':
        if not a.output:
            p.error('--output required (existing capture to check)')
        print(json.dumps(check_capture(a.output), indent=2))
        raise SystemExit(0)
    if not a.work:
        p.error('--work required')
    work = a.work.resolve()
    if not work.is_relative_to(Path('/private/tmp')):
        p.error('worker must be under /private/tmp')
    if a.mode == 'prepare':
        r = prepare(a.app, work)
        print(json.dumps({k:v for k,v in r.items() if k != 'initializers'}, indent=2))
    else:
        if not a.output:
            p.error('--output required')
        r = run(work, a.output)
        print(json.dumps({'complete': r['complete'], 'last_run': r['runs'][-1]}, indent=2))
        raise SystemExit(0 if r['complete'] else 1)
