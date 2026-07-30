#!/usr/bin/env python3
r"""Extract per-verb contract structure from VirtualDJ's ACTION_ class RTTI.

The verb table (tools/extract_verb_table.py) settles *existence*; this tool reads
the **implementation classes** behind it. Every distinct verb id has exactly one
C++ class named `ACTION_<name>`, and although the symbol table is stripped on
current builds, the Itanium RTTI graph survives intact in the binary:

    name string (__TEXT,__const, length-prefixed)
      <- std::type_info object (__DATA_CONST,__const): [abi vptr][name ptr][bases...]
      <- vtable (__DATA_CONST,__const): [offset-to-top 0][typeinfo ptr][fn slots...]

Three layers of contract fall out, all serialised data:

1. **Hierarchy** — the base class is a contract taxonomy (`IActionSwitch` toggles,
   `IActionSlider`/`IActionSlider2` continuous 0..1, `IParamValuesAction`
   enum-keyword args, ...) and multiple-inheritance mixins scope context
   (`IActionPlugin`, `IActionSampler`, ...).
2. **Vtable override matrix** — which slots a class overrides versus `IAction`'s
   defaults gives its capabilities. Slot meanings are CALIBRATED at build time
   from verbs whose kind is HTTP-proven, never hard-coded: `clear_search`
   (action-only) pins onExecute, `loaded` (query) pins the generic onQuery, and
   `get_title`'s extra override pins the specialized text query. The generic
   query slot returns a variant — bools, numbers, AND text all flow through it
   (the return-type sweep proved this: ~160 classes override only the generic
   slot yet answer with ints/floats/text) — so this tool claims capability, not
   concrete type. Concrete types are Tier-1 observation:
   tests/verb-return-types.json. The remaining slots are recorded raw; leads:
   slot 5's membership skews to argument-taking verbs, slot 7's to
   menu/options providers, and slots 8/9 are a near-identical pair
   (probably press/release — surviving lambda names mention `onUp`).
3. **Method-body fingerprints** — light static analysis of each verb's own
   overridden methods (addresses known exactly from the vtable):
   - `arg_demand_slots`: slots whose method materializes E_INVALIDARG
     (0x80070057, a MOVZ/MOVK pair; callees followed one BL level). A method
     that can demand an argument takes one. Reproduces 108/110 of the
     HTTP-proven needs-args verbs, and — invisible to the bare-query sweep —
     flags query verbs that answer bare but validate an OPTIONAL argument.
   - `method_strings`: per-slot string references recovered by decoding
     ADRP/ADD pairs (format strings, enum keywords, UI labels).
   - `keyword_candidates`: literals from a method that ALSO calls a
     string-comparison (`_strcasecmp`, `_memcmp`, …, named through the
     indirect symbol table) — i.e. the verb matches its argument against
     keywords. Finds real, undocumented enum arguments: `get_time short`,
     `loaded opposite`, `get_bpm absolute|ghost`, `browser_window sidelist`.
   Param *types* are NOT extractable this way: param access is inlined, and
   the library calls a verb makes describe what it does with an argument, not
   how it fetches one (`_strcasecmp` appears in numeric-arg verbs too). Types
   remain a Tier-1 probe job.
4. **Vtable length** — extension interfaces (sliders: ~22 slots vs 12) are
   visible as extra slots.

Keyword candidates are a DISCOVERY channel, not a confirmation: probed live,
optional-arg verbs silently ignore unrecognized words (`browser_window bogus`
answers the same as `browser_window sidelist`), so confirming a keyword needs
prepared state where the forms would differ, never an error code.

The class<->verb join is a checked bijection: every one of the 955 distinct ids
matches exactly one class via `ACTION_<spelling>`, no class is left over, and no
id matches under two spellings. Pointers are decoded by masking to the low 40
bits, which carries the unslid vmaddr on this image layout (verified: 955/955
name pointers resolve). This build uses classic LC_DYLD_INFO_ONLY, so __stubs
are named through DYSYMTAB's indirect symbol table.

This is Tier-2 structural evidence: it predicts capability and family;
Tier-1 sweeps confirm behavior and supply concrete types. Located by anchoring, never by address.

    python3 tools/extract_action_contracts.py > tests/action-contracts.json
    python3 tools/extract_action_contracts.py --get hot_cue
    python3 tools/extract_action_contracts.py --check
"""
import json
import re
import struct
import sys

BINARY = "/Applications/VirtualDJ.app/Contents/MacOS/VirtualDJ"
ARTIFACT = "tests/action-contracts.json"
VERB_TABLE = "tests/verb-table.json"
SWEEP = "tests/verb-existence-sweep.json"
ARM64 = 0x0100000C
MASK = 0xFFFFFFFFFF  # chained fixups: low 40 bits carry the unslid vmaddr
CALIBRATION = {  # verb -> what its HTTP-proven kind pins (see build())
    "clear_search": "execute",
    "loaded": "query",
    "get_title": "query_text",
}
FAMILY_BASES = {
    "IActionSwitch": "toggle",
    "IActionSlider": "slider",
    "IActionSlider2": "slider",
}
MIXIN_PREFIXES = ("IActionPlugin", "IActionSampler", "IActionSamplerGroup",
                  "IThread")


def slice_offset(data: bytes) -> int:
    if struct.unpack_from(">I", data, 0)[0] not in (0xCAFEBABE, 0xCAFEBABF):
        return 0
    for i in range(struct.unpack_from(">I", data, 4)[0]):
        cpu, _sub, off, _size, _al = struct.unpack_from(">5I", data, 8 + i * 20)
        if cpu == ARM64:
            return off
    raise SystemExit("no arm64 slice")


def sections(data: bytes, base: int):
    ncmds = struct.unpack_from("<I", data, base + 16)[0]
    off, out = base + 32, []
    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack_from("<II", data, off)
        if cmd == 0x19:
            seg = data[off + 8:off + 24].rstrip(b"\0").decode()
            soff = off + 72
            for _s in range(struct.unpack_from("<I", data, off + 64)[0]):
                name = data[soff:soff + 16].rstrip(b"\0").decode()
                addr, size = struct.unpack_from("<QQ", data, soff + 32)
                fileoff = struct.unpack_from("<I", data, soff + 48)[0]
                out.append((seg, name, addr, size, fileoff))
                soff += 80
        off += cmdsize
    return out


def build() -> dict:
    data = open(BINARY, "rb").read()
    base = slice_offset(data)
    secs = sections(data, base)

    def sec(segn, secn):
        return next(s for s in secs if s[0] == segn and s[1] == secn)

    tconst, dconst, text = sec("__TEXT", "__const"), sec("__DATA_CONST", "__const"), sec("__TEXT", "__text")
    tblob = data[base + tconst[4]: base + tconst[4] + tconst[3]]
    dblob = data[base + dconst[4]: base + dconst[4] + dconst[3]]

    def dword(vm):
        i = vm - dconst[2]
        if 0 <= i <= len(dblob) - 8:
            return struct.unpack_from("<Q", dblob, i)[0]
        return None

    def class_name_at(vm):
        """Read a length-prefixed mangled class name at a __TEXT,__const vmaddr."""
        i = vm - tconst[2]
        if 0 <= i < len(tblob):
            m = re.match(rb"(\d+)([A-Za-z_][A-Za-z0-9_]*)", tblob[i:i + 160])
            if m and len(m.group(2)) >= int(m.group(1)):
                return m.group(2)[:int(m.group(1))].decode()
        return None

    # typeinfo objects: a __DATA_CONST word whose masked value reads back as an
    # ACTION* class name; the typeinfo starts one word earlier (abi vptr).
    ti_by_name, name_of_ti = {}, {}
    for i in range(0, len(dblob) - 8, 8):
        s = class_name_at(struct.unpack_from("<Q", dblob, i)[0] & MASK)
        if s and s.startswith("ACTION"):
            ti = dconst[2] + i - 8
            ti_by_name[s], name_of_ti[ti] = ti, s

    def base_name(ti_addr):
        np = dword(ti_addr + 8)
        return class_name_at(np & MASK) if np else None

    def bases_of(ti):
        """si_class: one base at +16. vmi_class: count at +16 high word, bases at +24."""
        w = dword(ti + 16)
        if w is None:
            return []
        if class_name_at(dword(w & MASK) & MASK if dword(w & MASK) else -1) or \
           base_name(w & MASK):
            return [base_name(w & MASK)]
        count = w >> 32
        if 1 <= count <= 8:
            out = []
            for k in range(count):
                b = dword(ti + 24 + k * 16)
                if b is not None:
                    out.append(base_name(b & MASK))
            return [b for b in out if b]
        return []

    # vtables: [offset-to-top 0][typeinfo ptr][fn slots ...]
    def find_vtable(ti):
        for i in range(8, len(dblob) - 8, 8):
            if struct.unpack_from("<Q", dblob, i)[0] & MASK == ti and \
               struct.unpack_from("<Q", dblob, i - 8)[0] & MASK == 0:
                return dconst[2] + i + 8
        return None

    def slots(vt, limit=64):
        out = []
        for k in range(limit):
            w = dword(vt + k * 8)
            if w is None:
                break
            t = w & MASK
            if t == 0 or not (text[2] <= t < text[2] + text[3]):
                break
            out.append(t)
        return out

    # --- method-body analysis helpers (light arm64 decoding) ------------------
    text_lo, text_hi = text[2], text[2] + text[3]

    # __stubs naming, via SYMTAB + DYSYMTAB's indirect symbol table (this build
    # uses classic LC_DYLD_INFO_ONLY, not chained fixups)
    ncmds = struct.unpack_from("<I", data, base + 16)[0]
    o, symoff = base + 32, None
    indirectsymoff = nindirect = stroff = None
    for _ in range(ncmds):
        cmd, size = struct.unpack_from("<II", data, o)
        if cmd == 0x2:
            symoff, _nsyms, stroff, _ss = struct.unpack_from("<4I", data, o + 8)
        elif cmd == 0xB:
            indirectsymoff, nindirect = struct.unpack_from("<II", data, o + 56)
        o += size
    stubs = next((s for s in secs if s[1] == "__stubs"), None)
    stub_res1 = stub_ent = None
    if stubs:
        o = base + 32
        for _ in range(ncmds):
            cmd, size = struct.unpack_from("<II", data, o)
            if cmd == 0x19:
                soff = o + 72
                for _s in range(struct.unpack_from("<I", data, o + 64)[0]):
                    if data[soff:soff + 16].rstrip(b"\0") == b"__stubs":
                        stub_res1 = struct.unpack_from("<I", data, soff + 68)[0]
                        stub_ent = struct.unpack_from("<I", data, soff + 72)[0]
                    soff += 80
            o += size

    def stub_name(vm):
        if not stubs or symoff is None or indirectsymoff is None or not stub_ent:
            return None
        i = (vm - stubs[2]) // stub_ent
        k = (stub_res1 or 0) + i
        if not (0 <= i < stubs[3] // stub_ent) or not (0 <= k < nindirect):
            return None
        idx = struct.unpack_from("<I", data, base + indirectsymoff + k * 4)[0]
        if idx in (0x40000000, 0x80000000):
            return None
        p = base + symoff + idx * 16
        strx = struct.unpack_from("<I", data, p)[0]
        q = base + stroff + strx
        e = data.find(b"\0", q)
        return data[q:e].decode(errors="replace")

    STRCMP = {"_strcasecmp", "_strncasecmp", "_strcmp", "_strncmp", "_memcmp"}

    def body(fn, max_insns=4000):
        off = base + text[4] + (fn - text_lo)
        out = []
        for k in range(max_insns):
            if off + k * 4 + 4 > base + text[4] + text[3]:
                break
            w = struct.unpack_from("<I", data, off + k * 4)[0]
            out.append((fn + k * 4, w))
            if w == 0xD65F03C0 and k > 2:  # RET
                break
        return out

    def bl_targets(insns):
        """(local __text targets, names of __stubs library calls)"""
        local, lib = [], []
        s_lo = stubs[2] if stubs else 0
        s_hi = s_lo + (stubs[3] if stubs else 0)
        for pc, w in insns:
            if (w & 0xFC000000) == 0x94000000:  # BL
                imm = w & 0x03FFFFFF
                if imm & (1 << 25):
                    imm -= 1 << 26
                t = pc + imm * 4
                if s_lo <= t < s_hi:
                    nm = stub_name(t)
                    if nm:
                        lib.append(nm)
                elif text_lo <= t < text_hi:
                    local.append(t)
        return local, lib

    def has_invalidarg(insns):
        # E_INVALIDARG 0x80070057 as MOVZ w?,#0x57 + MOVK w?,#0x8007,lsl#16
        mz = any((w & 0xFFFFFFE0) == 0x52800AE0 for _, w in insns)
        mk = any((w & 0xFFFFFFE0) == 0x72B000E0 for _, w in insns)
        return mz and mk

    cstr_secs = [(s, data[base + s[4]: base + s[4] + s[3]])
                 for s in secs if s[1] in ("__cstring",) or
                 (s[0] == "__TEXT" and s[1] == "__const")]

    def cstr(vm):
        for s, blob in cstr_secs:
            i = vm - s[2]
            if 0 <= i < len(blob):
                e = blob.find(b"\0", i)
                if e > i:
                    try:
                        return blob[i:e].decode()
                    except UnicodeDecodeError:
                        return None
        return None

    def string_refs(insns, cap=16):
        pages, out = {}, []
        for pc, w in insns:
            if (w & 0x9F000000) == 0x90000000:  # ADRP
                immlo = (w >> 29) & 3
                immhi = (w >> 5) & 0x7FFFF
                imm = (immhi << 2) | immlo
                if imm & (1 << 20):
                    imm -= 1 << 21
                pages[w & 31] = (pc & ~0xFFF) + (imm << 12)
            elif (w & 0xFF800000) == 0x91000000:  # ADD imm
                rn = (w >> 5) & 31
                if rn in pages:
                    imm12 = (w >> 10) & 0xFFF
                    if (w >> 22) & 1:
                        imm12 <<= 12
                    s = cstr(pages[rn] + imm12)
                    if s and 1 < len(s) < 48 and s.isprintable() and s not in out:
                        out.append(s)
                        if len(out) >= cap:
                            break
        return out

    # the shared root: IAction's own typeinfo + vtable give the default slots
    ia_ti = None
    for i in range(0, len(dblob) - 8, 8):
        if class_name_at(struct.unpack_from("<Q", dblob, i)[0] & MASK) == "IAction":
            ia_ti = dconst[2] + i - 8
            break
    if ia_ti is None:
        raise SystemExit("IAction typeinfo not found")
    root_slots = slots(find_vtable(ia_ti))
    if len(root_slots) < 8:
        raise SystemExit(f"IAction vtable looks wrong ({len(root_slots)} slots)")

    # walk every ACTION class
    vt_addr, over, chain, nslots = {}, {}, {}, {}
    for nm, ti in ti_by_name.items():
        vt = find_vtable(ti)
        if vt is None:
            continue
        ss = slots(vt)
        vt_addr[nm], nslots[nm] = vt, len(ss)
        over[nm] = [k for k in range(2, len(ss))
                    if k >= len(root_slots) or ss[k] != root_slots[k]]
        chain[nm] = bases_of(ti)

    # join to the verb table: ACTION_<spelling> per id, checked as a bijection
    table = json.load(open(VERB_TABLE))
    verbs = table["verbs"]
    ids = {}
    for name, rec in verbs.items():
        ids.setdefault(rec["id"], []).append(name)
    class_of_id, orphan_ids, double = {}, [], []
    for vid, group in ids.items():
        hits = [n for n in group if f"ACTION_{n}" in vt_addr]
        if not hits:
            orphan_ids.append(vid)
        elif len(hits) > 1:
            double.append(vid)
        else:
            class_of_id[vid] = f"ACTION_{hits[0]}"
    unmatched = sorted(set(vt_addr) - set(class_of_id.values()))

    # calibrate slot meanings from HTTP-proven kinds — never hard-coded
    pin = {v: sorted(set(over[class_of_id[verbs[v]["id"]]]) & set(range(len(root_slots))))
           for v in CALIBRATION}
    if len(pin["clear_search"]) != 1 or len(pin["loaded"]) != 1:
        raise SystemExit(f"slot calibration ambiguous: {pin}")
    slot_of = {"execute": pin["clear_search"][0], "query": pin["loaded"][0]}
    rest = [s for s in pin["get_title"] if s not in slot_of.values()]
    if len(rest) != 1:
        raise SystemExit(f"slot calibration ambiguous: {pin}")
    slot_of["query_text"] = rest[0]
    if len(set(slot_of.values())) != 3:
        raise SystemExit(f"slot calibration collided: {slot_of}")

    def family(nm, seen=None):
        seen = seen or set()
        for b in chain.get(nm, []):
            if b in FAMILY_BASES:
                return FAMILY_BASES[b]
            if b and b.startswith(("ACTION", "I")) and b not in seen and b in chain:
                f = family(b, seen | {nm})
                if f:
                    return f
        return None

    def analyze_methods(cls):
        """arg-demand fingerprint, string refs, and keyword candidates."""
        vt = vt_addr[cls]
        demands, strings, keywords = [], {}, []
        for slot in over[cls]:
            w = dword(vt + slot * 8)
            if w is None:
                continue
            fn = w & MASK
            if not (text_lo <= fn < text_hi):
                continue
            b = body(fn)
            local, lib = bl_targets(b)
            callees = list(dict.fromkeys(local))[:10]
            hit = has_invalidarg(b)
            compares = any(x in STRCMP for x in lib)
            ss = string_refs(b)
            for t in callees:
                cb = body(t, 800)
                if not hit and has_invalidarg(cb):
                    hit = True
                if not compares:
                    _l, clib = bl_targets(cb)
                    compares = compares or any(x in STRCMP for x in clib)
            if hit:
                demands.append(slot)
            if ss:
                strings[str(slot)] = ss
            if compares:
                keywords += [s for s in ss
                             if 2 < len(s) < 24 and s.replace("_", "").isalnum()
                             and not s.startswith("ACTION")]
        return demands, strings, sorted(set(keywords))

    out_verbs = {}
    for vid, cls in class_of_id.items():
        ov = over[cls]
        demands, mstrings, keywords = analyze_methods(cls)
        rec = {
            "class": cls,
            "base": chain[cls][0] if chain.get(cls) else None,
            "mixins": [b for b in chain.get(cls, [])[1:]
                       if b and b.startswith(MIXIN_PREFIXES)],
            "vtable_len": nslots[cls],
            "overridden_slots": ov,
            "executes": slot_of["execute"] in ov,
            "queries": slot_of["query"] in ov,
            "query_text": slot_of["query_text"] in ov,
            "extended_interface": nslots[cls] > len(root_slots),
            "arg_demand_slots": demands,
        }
        if mstrings:
            rec["method_strings"] = mstrings
        if keywords:
            rec["keyword_candidates"] = keywords
        fam = family(cls)
        if fam:
            rec["family"] = fam
        for name in ids[vid]:
            out_verbs[name] = rec

    # agreement with the HTTP existence sweep (kind is Tier-1)
    sweep = json.load(open(SWEEP))["verbs"]
    agree = {"query": [0, 0], "action-only": [0, 0], "needs-args": [0, 0]}
    optional_args = []
    for name, s in sweep.items():
        rec = out_verbs.get(name)
        if not rec or s.get("status") != "exists":
            continue
        k = s.get("kind")
        if k == "query":
            agree["query"][1] += 1
            if rec["queries"] or rec["query_text"] or rec["extended_interface"]:
                agree["query"][0] += 1
            if rec["arg_demand_slots"]:
                optional_args.append(name)
        elif k == "action-only":
            agree["action-only"][1] += 1
            if rec["executes"]:
                agree["action-only"][0] += 1
        elif k == "needs-args":
            agree["needs-args"][1] += 1
            if rec["arg_demand_slots"]:
                agree["needs-args"][0] += 1

    from collections import Counter
    fams = Counter(r.get("family", "plain") for r in
                   (out_verbs[ids[v][0]] for v in class_of_id))
    return {
        "summary": {
            "classes": len(vt_addr),
            "distinct_ids": len(ids),
            "ids_with_class": len(class_of_id),
            "orphan_ids": orphan_ids,
            "double_matched_ids": double,
            "unmatched_classes": unmatched,
            "iaction_slots": len(root_slots),
            "slot_labels": slot_of,
            "families": dict(fams),
            "arg_demand_verbs": sum(1 for vid in class_of_id
                                    if out_verbs[ids[vid][0]]["arg_demand_slots"]),
            "optional_arg_queries": sorted(optional_args),
            "keyword_verbs": sum(1 for vid in class_of_id
                                 if out_verbs[ids[vid][0]].get("keyword_candidates")),
            "sweep_agreement": {
                k: {"agree": a, "total": t,
                    "rate": round(a / t, 4) if t else None}
                for k, (a, t) in agree.items()},
        },
        "verbs": out_verbs,
    }


def cmd_get(name: str) -> None:
    data = json.load(open(ARTIFACT))
    rec = data["verbs"].get(name)
    if rec is None:
        print(json.dumps({"name": name, "has_contract": False,
                          "hint": "not in the verb table, or id unresolved"},
                         indent=1))
        return
    print(json.dumps({"name": name, **rec}, indent=1))


def cmd_check() -> None:
    data = json.load(open(ARTIFACT))
    s = data["summary"]
    errs = []
    if s["ids_with_class"] != s["distinct_ids"]:
        errs.append(f"bijection broken: {s['ids_with_class']}/{s['distinct_ids']} ids matched")
    if s["orphan_ids"] or s["double_matched_ids"] or s["unmatched_classes"]:
        errs.append(f"orphans={s['orphan_ids'][:5]} doubles={s['double_matched_ids'][:5]} "
                    f"unmatched={s['unmatched_classes'][:5]}")
    if len(set(s["slot_labels"].values())) != 3:
        errs.append(f"slot calibration collided: {s['slot_labels']}")
    for kind, st in s["sweep_agreement"].items():
        if st["total"] and st["rate"] is not None and st["rate"] < 0.85:
            errs.append(f"sweep agreement for {kind} too low: {st}")
    if s.get("arg_demand_verbs", 0) < 100:
        errs.append(f"arg-demand fingerprint looks broken: "
                    f"{s.get('arg_demand_verbs')} verbs")
    if s.get("keyword_verbs", 0) < 50:
        errs.append(f"keyword detection looks broken (stub naming?): "
                    f"{s.get('keyword_verbs')} verbs")
    if errs:
        sys.exit("action contracts check FAILED:\n  - " + "\n  - ".join(errs))
    ag = {k: v["rate"] for k, v in s["sweep_agreement"].items()}
    print(f"action contracts check passed: {s['classes']} classes / "
          f"{s['distinct_ids']} ids (bijection), slots {s['slot_labels']}, "
          f"families {s['families']}, {s['arg_demand_verbs']} arg-demanding, "
          f"{s['keyword_verbs']} with keywords, sweep agreement {ag}")


def main() -> None:
    if len(sys.argv) > 2 and sys.argv[1] == "--get":
        return cmd_get(sys.argv[2])
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        return cmd_check()
    print(json.dumps(build(), indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
