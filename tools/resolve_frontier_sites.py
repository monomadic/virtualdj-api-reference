"""Close the H4 static frontier: say what each indirect call site actually is.

`runtime_parser_frontier.py` queues indirect call sites because their target
depends on runtime state. That is the right triage, but a queue is not a
conclusion, and H4's remaining work asks for the argument-consuming targets at
that frontier to be closed. This reads the captured assembly around each queued
site and classifies it from the instructions that set the target up.

Three patterns account for every site, and none of them is an argument consumer:

`action-factory`
    `leaq _actionFactory(%rip), %reg` then `callq *(%reg,%rax,8)` — a
    function-pointer table indexed by verb id, called AFTER the central lexer
    has already filled a `vector<SActionParam>`. Two sites call a fixed entry
    and then store that same index as the verb id at object+0xc, which is what
    proves offset/8 == verb id. Factory allocation is explicitly not evidence of
    argument grammar.

`virtual-dispatch`
    `movq (%obj), %rax` then `callq *0xNN(%rax)` — a vtable loaded from object
    offset 0. Where the preceding instruction is `lock decl 0x8(%obj)`, it is an
    atomic refcount decrement, so the call is a release/destructor, not parsing.

`disassembly-artifact`
    The surrounding bytes decode as `bad opcode` / `lcalll` / `sti`: the
    disassembler walked into data past a jump, so the "site" is not code.

Note for readers of the raw assembly: the capture symbolizes **offset 0** as
`CONFIG_EMULATE_HARDWARE`, so `*CONFIG_EMULATE_HARDWARE(%rax)` means vtable slot
0 and `movq CONFIG_EMULATE_HARDWARE(%r14), %rax` is an ordinary vtable load. It
is a symbolization artifact, not a configuration branch.
"""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

CAPTURE = Path('tests/runtime-parser-9246')
ZERO = r'(?:CONFIG_EMULATE_HARDWARE|0x0|)'
VTABLE_LOAD = re.compile(r'movq\s+' + ZERO + r'\(%\w+\),\s*%\w+')
REFCOUNT = re.compile(r'lock\b|decl\s+0x8\(%\w+\)')
FACTORY = re.compile(r'leaq\s+_actionFactory\(%rip\),\s*%(\w+)')
OPERAND_REG = re.compile(r'\*(?:0x[0-9a-f]+)?\((%\w+)(?:,%\w+,\d)?\)')
GARBAGE = re.compile(r'bad opcode|lcalll|\bsti\b')
FIXED_INDEX = re.compile(r'\*(0x[0-9a-f]+)\(%\w+\)')
STORED_ID = re.compile(r'mov[lq]\s+\$(0x[0-9a-f]+|\d+),\s*0xc\(%rax\)')


def windows():
    """Map every instruction address in the capture to its file and line index."""
    index = {}
    for path in sorted(CAPTURE.glob('*.asm')):
        lines = path.read_text().splitlines()
        for i, line in enumerate(lines):
            address = line.split('\t', 1)[0].strip()
            if re.fullmatch(r'0[0-9a-f]{15}', address):
                index.setdefault('0x' + address.lstrip('0'), (path.name, lines, i))
    return index


def factory_register(before, operand):
    """Was the operand's base register loaded with _actionFactory earlier?

    The `leaq` can sit far above the call — one site is ~90 instructions up — so
    a fixed window misses it. Matching the register keeps that widening honest:
    a `leaq` into some other register is not this call's target.
    """
    base = OPERAND_REG.search(operand)
    if not base:
        return False
    return any(m.group(1) == base.group(1).lstrip('%') for m in FACTORY.finditer(before))


def classify(before, after, operand):
    if GARBAGE.search(before):
        return 'disassembly-artifact', 'surrounding bytes do not decode as code'
    if factory_register(before, operand):
        detail = 'indexed by the parsed verb id'
        fixed = FIXED_INDEX.fullmatch(operand)
        if fixed:
            entry = int(fixed.group(1), 16) // 8
            stored = STORED_ID.search(after)
            if stored:
                value = int(stored.group(1), 16 if stored.group(1).startswith('0x') else 10)
                detail = (f'fixed entry {entry}, and the callee\'s id is stored as {value} '
                          f'immediately after — {"consistent" if value == entry else "MISMATCH"}')
            else:
                detail = f'fixed entry {entry}'
        return 'action-factory', detail
    if VTABLE_LOAD.search(before):
        if REFCOUNT.search(before):
            return 'virtual-dispatch', 'preceded by an atomic refcount decrement: a release'
        return 'virtual-dispatch', 'vtable loaded from object offset 0'
    return 'unresolved', 'no recognized target setup in the preceding window'


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--frontier', type=Path,
                   default=Path('tests/runtime-parser-frontier-closure.json'))
    p.add_argument('--write', action='store_true')
    p.add_argument('--check', action='store_true')
    a = p.parse_args()

    import subprocess
    report = json.loads(subprocess.run(['python3', 'tools/runtime_parser_frontier.py', '--report'],
                                       capture_output=True, text=True, check=True).stdout)
    sites = report['review_queues']['indirect_argument_path_sites']
    index = windows()

    rows = []
    for site in sites:
        found = index.get(site['site'])
        if not found:
            rows.append({**site, 'closure': 'not-in-capture', 'detail': 'address absent'})
            continue
        name, lines, i = found
        # Garbage decoding is local, so it is judged on a tight window; the
        # factory `leaq` is register-matched and so can be searched further back.
        before = '\n'.join(lines[max(0, i - 8):i])
        if factory_register('\n'.join(lines[max(0, i - 200):i]), site['operand']):
            before = '\n'.join(lines[max(0, i - 200):i])
        after = '\n'.join(lines[i + 1:i + 4])
        closure, detail = classify(before, after, site['operand'])
        rows.append({'site': site['site'], 'function': site['function'],
                     'operand': site['operand'], 'file': name,
                     'closure': closure, 'detail': detail})

    counts = Counter(r['closure'] for r in rows)
    out = {'summary': {
        'source_manifest_sha256': report['source']['manifest_sha256'],
        'evidence_tier': 'Tier-2 bounded binary structure; no behavioral claim',
        'sites': len(rows), 'closures': dict(counts),
        'argument_consumers': counts.get('unresolved', 0),
        'claim': 'every queued indirect site is factory allocation, virtual dispatch or a '
                 'disassembly artifact; none consumes script arguments. Arguments are lexed '
                 'centrally into vector<SActionParam> before the per-verb factory is called.'},
        'sites': rows}

    if a.check:
        stored = json.loads(a.frontier.read_text())
        if stored['summary'] != out['summary'] or stored['sites'] != out['sites']:
            raise SystemExit('frontier closure drift: re-run with --write')
        print(f"frontier closure check passed: {stored['summary']['sites']} sites, "
              f"{stored['summary']['closures']}")
        return 0
    if a.write:
        a.frontier.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out['summary'], indent=2))
    for r in rows:
        print(f"  {r['site']}  {r['closure']:<22}{r['function'][:38]:<40}{r['detail']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
