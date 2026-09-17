"""Bounded structural review of H4's remote entry and unlinked list helper.

Raw direct-branch scans are candidate discovery, not disassembly or proof that
an unreferenced function is dead. This emits no runtime grammar claims.
"""
import argparse
import bisect
import subprocess
import hashlib
import json
import re
import struct
from pathlib import Path
from extract_runtime_parser import x86_slice, function_starts, bounded_disassembly

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'tests/runtime-parser-9246/manifest.json'
OUT = ROOT / 'tests/runtime-parser-branch-routes.json'
EVALUATION_TARGETS = ('IAction::getParamEval', 'IAction::getFloatParamEval',
                      'IAction::getBoolParam',
                      'IParamValuesAction::getValues(SActionParam*, SActionParam*)',
                      'IParamValuesAction::getValues(float*, float*)')


def boolean_cache_arguments(functions):
    """Review only a nearby straight-line r8 setup, not general dataflow."""
    rows = []
    for caller in functions:
        for call in caller['calls']:
            if call['target'] != 'IAction::getBoolParam' or not call['verified_instruction']:
                continue
            lines = caller['assembly']
            index = next(i for i, line in enumerate(lines)
                         if line.startswith(call['site'][2:].zfill(16) + '\t'))
            setup = None
            disposition = 'unresolved'
            for line in reversed(lines[max(1, index-5):index]):
                if re.search(r'\t(?:j\w*|callq|retq)\t?', line):
                    break
                if re.search(r',\s*%r8(?:d)?(?:\s|$)', line):
                    setup = line
                    if re.search(r'\txorl\s+%r8d, %r8d$', line):
                        disposition = 'null'
                    elif re.search(r'\tleaq\s+[^,]*\(%rbx\), %r8$', line):
                        disposition = 'object-relative-address'
                    break
            rows.append({'caller': caller['symbol'], 'call_site': call['site'],
                         'cache_argument': disposition, 'setup_instruction': setup})
    return {'scope': 'x86_64 SysV fifth argument (r8, including this). Nearby straight-line instruction review only; no indirect/inlined caller inventory, runtime execution or cache-reuse proof. Symbolized displacement names are not field identities.',
            'calls': rows}


def scan(binary):
    manifest = json.loads(MANIFEST.read_text())
    data = binary.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert digest == manifest['source']['sha256'], 'binary differs from bounded capture'
    base = x86_slice(data)
    pos = base + 32
    segments = []
    for _ in range(struct.unpack_from('<I', data, base + 16)[0]):
        cmd, length = struct.unpack_from('<II', data, pos)
        if cmd == 0x19:
            name = data[pos+8:pos+24].rstrip(b'\0').decode()
            vm, _, fileoff, filesize = struct.unpack_from('<QQQQ', data, pos+24)
            if filesize and name != '__LINKEDIT':
                segments.append((name, vm, data[base+fileoff:base+fileoff+filesize]))
        pos += length
    target = int(manifest['symbols']['IAction::getListParam']['start'], 16)
    branches, pointers = [], []
    eval_targets = {int(manifest['symbols'][name]['start'], 16): name
                    for name in EVALUATION_TARGETS}
    eval_candidates = []
    for name, vm, chunk in segments:
        if name == '__TEXT':
            for opcode, kind in ((b'\xe8', 'call-rel32'), (b'\xe9', 'jump-rel32')):
                offset = 0
                while True:
                    offset = chunk.find(opcode, offset)
                    if offset < 0 or offset + 5 > len(chunk):
                        break
                    destination = vm + offset + 5 + struct.unpack_from('<i', chunk, offset+1)[0]
                    if destination == target:
                        branches.append({'site': hex(vm+offset), 'kind': kind})
                    if destination in eval_targets:
                        eval_candidates.append({'site': hex(vm+offset), 'kind': kind,
                                                'target': eval_targets[destination]})
                    offset += 1
        offset = 0
        while True:
            offset = chunk.find(struct.pack('<Q', target), offset)
            if offset < 0:
                break
            pointers.append({'segment': name, 'site': hex(vm+offset)})
            offset += 1
    # Identify immediate-byte mode writes, then verify them inside bounded bodies.
    nm = subprocess.check_output(['nm', '-arch', 'x86_64', str(binary)], text=True)
    symbols = {}
    remote_address = None
    for line in nm.splitlines():
        parts = line.split()
        if len(parts) != 3:
            continue
        if parts[2] == '__ZN7IAction8isRemoteE':
            remote_address = int(parts[0], 16)
        if parts[1].lower() == 't':
            symbols[int(parts[0], 16)] = parts[2]
    assert remote_address is not None
    starts = function_starts(binary)
    eval_callers = {}
    for call in eval_candidates:
        index = bisect.bisect_right(starts, int(call['site'], 16))-1
        start, end = starts[index:index+2]
        if start not in eval_callers:
            mangled = symbols[start]
            body = bounded_disassembly(binary, mangled, start, end)
            eval_callers[start] = {'symbol': mangled, 'start': hex(start), 'end_exclusive': hex(end),
                                  'assembly': body.splitlines(), 'assembly_sha256': hashlib.sha256(body.encode()).hexdigest(), 'calls': []}
        instruction = next((line for line in eval_callers[start]['assembly']
                            if line.startswith(call['site'][2:].zfill(16))), '')
        target_symbol = manifest['symbols'][call['target']]['mangled']
        call['verified_instruction'] = target_symbol in instruction and ('callq' in instruction or 'jmp' in instruction)
        eval_callers[start]['calls'].append(call)
    entry_symbol = '__ZN26ACTION_get_pioneer_display7onQueryER12SActionParam'
    entry_start = next(address for address, name in symbols.items() if name == entry_symbol)
    entry_end = starts[bisect.bisect_right(starts, entry_start)]
    entry_body = bounded_disassembly(binary, entry_symbol, entry_start, entry_end)
    entry_routes = []
    for caller in eval_callers.values():
        for line in entry_body.splitlines():
            if caller['symbol'] in line and ('callq' in line or '\tjmp\t' in line):
                entry_routes.append({'site': hex(int(line.split()[0], 16)),
                                     'callee': caller['symbol'], 'target': caller['start']})
    entrypoints = [{'symbol': entry_symbol, 'start': hex(entry_start), 'end_exclusive': hex(entry_end),
                   'assembly': entry_body.splitlines(), 'assembly_sha256': hashlib.sha256(entry_body.encode()).hexdigest(),
                   'routes': entry_routes}]
    writers = {}
    for name, vm, chunk in segments:
        if name != '__TEXT':
            continue
        offset = 0
        while True:
            offset = chunk.find(b'\xc6\x05', offset)
            if offset < 0 or offset + 7 > len(chunk):
                break
            if vm + offset + 7 + struct.unpack_from('<i', chunk, offset+2)[0] == remote_address:
                index = bisect.bisect_right(starts, vm+offset)-1
                start, end = starts[index:index+2]
                if start not in writers:
                    mangled = symbols[start]
                    body = bounded_disassembly(binary, mangled, start, end)
                    writers[start] = {'symbol': mangled, 'start': hex(start), 'end_exclusive': hex(end),
                                      'assembly': body.splitlines(), 'assembly_sha256': hashlib.sha256(body.encode()).hexdigest(), 'writes': []}
                site = hex(vm+offset)
                assert any(site[2:].zfill(16) in line and 'isRemote' in line for line in writers[start]['assembly'])
                writers[start]['writes'].append({'site': site, 'value': chunk[offset+6]})
            offset += 1
    create = manifest['symbols']['IAction::create']
    assembly = (MANIFEST.parent / create['file']).read_text()
    assert hashlib.sha256(assembly.encode()).hexdigest() == create['asm_sha256']
    remote_literals = []
    for line in assembly.splitlines():
        match = re.match(r'([0-9a-f]{16})\s', line)
        if match and 0x100596f45 <= int(match[1], 16) < 0x1005974cf and 'literal pool for:' in line:
            remote_literals.append({'site': hex(int(match[1], 16)), 'instruction': line})
    return {
        'source': {'bundle_version': '18.0.9246', 'architecture': 'x86_64', 'binary_sha256': digest},
        'claim_scope': 'Tier-2 structural observations only; no dead-code or runtime-behavior conclusion',
        'mode_writer_scan_scope': 'C6 05 RIP-relative immediate-byte writes to the nm-resolved isRemote address, verified inside LC_FUNCTION_STARTS-bounded bodies; not an exhaustive dataflow analysis.',
        'remote_mode_writers': list(writers.values()),
        'evaluation_callers': {
            'targets': list(EVALUATION_TARGETS),
            'scan_scope': 'E8/E9 rel32 candidates in __TEXT, checked against LC_FUNCTION_STARTS-bounded disassembly. Does not enumerate indirect callers or inlined copies, or prove live instruction execution.',
            'functions': list(eval_callers.values())},
        'evaluation_entrypoints': entrypoints,
        'boolean_cache_arguments': boolean_cache_arguments(list(eval_callers.values())),
        'remote_entry': {
            'gate': 'IAction::create@0x100596f45',
            'normal_parser_entry': '0x1005974cf',
            'alternate_route': '0x100598365',
            'factory_call': '0x1005983b4', 'factory_byte_offset': '0x1e8',
            'stored_action_id_instruction': '0x1005983bd',
            'text_parameter_assignment': '0x100598422',
            'literal_checks': remote_literals,
            'question': 'With isRemote independently established, which checked heads rejoin ordinary parsing and which reach the source-text wrapper?',
            'fixture_obligation': 'parser_remote_mode: establish and independently verify the actual isRemote creation context before interpreting any paired local/remote query results.',
            'status': 'mode-establishment-not-measured',
            'transport_limit': 'A Remote-protocol subscription has not been shown to set this global; HTTP is not a substitute for this fixture.'},
        'list_helper': {
            'symbol': 'IAction::getListParam', 'target': hex(target),
            'scan_scope': 'E8/E9 rel32 encodings in __TEXT, and exact 64-bit target-address bytes in file-backed non-LINKEDIT segments; positive matches require instruction/data review.',
            'direct_branch_candidates': branches, 'address_candidates': pointers,
            'status': 'reachability-not-established',
            'question': 'Is this captured helper reachable from the recovered parser/dispatch paths, or an unused/out-of-scope utility?',
            'next_action': 'Resolve indirect or inlined equivalents before requiring a live consumer test; absence of these encodings alone is not an unreachability proof.'}}


def load_report():
    result = json.loads(OUT.read_text())
    manifest = json.loads(MANIFEST.read_text())
    assert result['source']['binary_sha256'] == manifest['source']['sha256']
    assert result['evaluation_callers']['targets'] == list(EVALUATION_TARGETS)
    name, address = result['remote_entry']['gate'].split('@')
    symbol = manifest['symbols'][name]
    assert int(symbol['start'], 16) <= int(address, 16) < int(symbol['end_exclusive'], 16)
    for writer in result['remote_mode_writers']:
        body = '\n'.join(writer['assembly']) + '\n'
        assert hashlib.sha256(body.encode()).hexdigest() == writer['assembly_sha256']
        for write in writer['writes']:
            assert int(writer['start'], 16) <= int(write['site'], 16) < int(writer['end_exclusive'], 16)
            assert any(line.startswith(write['site'][2:].zfill(16)) and 'isRemote' in line
                       for line in writer['assembly'])
    for caller in result.get('evaluation_callers', {}).get('functions', []):
        body = '\n'.join(caller['assembly']) + '\n'
        assert hashlib.sha256(body.encode()).hexdigest() == caller['assembly_sha256']
        for call in caller['calls']:
            assert int(caller['start'], 16) <= int(call['site'], 16) < int(caller['end_exclusive'], 16)
            instruction = next((line for line in caller['assembly']
                                if line.startswith(call['site'][2:].zfill(16))), '')
            verified = manifest['symbols'][call['target']]['mangled'] in instruction and ('callq' in instruction or 'jmp' in instruction)
            assert call['verified_instruction'] == verified
    for entry in result.get('evaluation_entrypoints', []):
        body = '\n'.join(entry['assembly']) + '\n'
        assert hashlib.sha256(body.encode()).hexdigest() == entry['assembly_sha256']
        for route in entry['routes']:
            assert int(entry['start'], 16) <= int(route['site'], 16) < int(entry['end_exclusive'], 16)
            instruction = next(line for line in entry['assembly'] if line.startswith(route['site'][2:].zfill(16)))
            assert route['callee'] in instruction and ('callq' in instruction or '\tjmp\t' in instruction)
            assert any(c['symbol'] == route['callee'] and c['start'] == route['target']
                       for c in result['evaluation_callers']['functions'])
    assert result['boolean_cache_arguments'] == boolean_cache_arguments(
        result['evaluation_callers']['functions']), 'boolean cache argument review differs'
    return result


def caller_report(target):
    """Compact checked call sites, including rejected byte-scan candidates."""
    result = load_report()
    if target not in result['evaluation_callers']['targets']:
        raise ValueError(f'symbol was not included in the caller scan: {target}')
    calls = []
    for caller in result['evaluation_callers']['functions']:
        for call in caller['calls']:
            if call['target'] == target:
                instruction = next((line for line in caller['assembly']
                                    if line.startswith(call['site'][2:].zfill(16) + '\t')), None)
                calls.append({'caller': caller['symbol'], **call,
                              'instruction': instruction,
                              'assembly_sha256': caller['assembly_sha256']})
    return {'source': result['source'], 'scope': result['evaluation_callers']['scan_scope'],
            'target': target, 'calls': calls, 'live_coverage_claim': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    print(json.dumps(scan(args.binary) if args.binary else load_report(), indent=2))


if __name__ == '__main__':
    main()
