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
3. **Vtable length** — extension interfaces (sliders: ~22 slots vs 12) are
   visible as extra slots.

The class<->verb join is a checked bijection: every one of the 955 distinct ids
matches exactly one class via `ACTION_<spelling>`, no class is left over, and no
id matches under two spellings. Chained-fixup pointers are decoded by masking to
the low 40 bits, which carries the unslid vmaddr on this image layout (verified:
955/955 name pointers resolve).

This is Tier-2 structural evidence: it predicts capability, return type, and
family; Tier-1 sweeps confirm behavior. Located by anchoring, never by address.

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

    out_verbs = {}
    for vid, cls in class_of_id.items():
        ov = over[cls]
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
        }
        fam = family(cls)
        if fam:
            rec["family"] = fam
        for name in ids[vid]:
            out_verbs[name] = rec

    # agreement with the HTTP existence sweep (kind is Tier-1)
    sweep = json.load(open(SWEEP))["verbs"]
    agree = {"query": [0, 0], "action-only": [0, 0]}
    for name, s in sweep.items():
        rec = out_verbs.get(name)
        if not rec or s.get("status") != "exists":
            continue
        k = s.get("kind")
        if k == "query":
            agree["query"][1] += 1
            if rec["queries"] or rec["query_text"] or rec["extended_interface"]:
                agree["query"][0] += 1
        elif k == "action-only":
            agree["action-only"][1] += 1
            if rec["executes"]:
                agree["action-only"][0] += 1

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
    if errs:
        sys.exit("action contracts check FAILED:\n  - " + "\n  - ".join(errs))
    ag = {k: v["rate"] for k, v in s["sweep_agreement"].items()}
    print(f"action contracts check passed: {s['classes']} classes / "
          f"{s['distinct_ids']} ids (bijection), slots {s['slot_labels']}, "
          f"families {s['families']}, sweep agreement {ag}")


def main() -> None:
    if len(sys.argv) > 2 and sys.argv[1] == "--get":
        return cmd_get(sys.argv[2])
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        return cmd_check()
    print(json.dumps(build(), indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
