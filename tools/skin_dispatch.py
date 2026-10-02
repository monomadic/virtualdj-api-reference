#!/usr/bin/env python3
"""Skin tag recognition and dispatch roles from the named 18.0.9246 code (Tier 2).

Two layers, kept apart:

* `sites` is mechanical. Every skin function (CSkin*/ISkin*/SSkin*, plus the
  loaders the factory reaches) is disassembled from the symbol-rich binary and
  scanned linearly. Each `strIsEqualCI` against a literal and each
  `CXMLNode::getChild("...")` becomes a site with its function, address and
  literal. A child node is followed through registers, callee-saved registers
  and stack slots until it is passed to a call, and the callees that receive it
  decide its role: `object` (handed to a constructor or loader), `container`
  (asked for named children of its own), `slot` (read for an image, rectangle
  or geometry), `data` (read for attributes only) or `unknown`.
* `dispatch` is reviewed. The factory's gates, comparison rule and default, the
  branches that create no object, and the container loaders that see a tag
  before the factory does were read from the disassembly. Every reviewed rule
  names the address of the comparison or call it rests on, and extraction fails
  if that address no longer holds that literal or callee.

Neither layer says what anything does at runtime. A linear scan does not follow
branches, so `role` lists every consumer it saw on any path. A site whose name
is not a literal is listed as unresolved, never dropped.

Usage:
  python3 tools/skin_dispatch.py                       # summary of the saved capture
  python3 tools/skin_dispatch.py NAME                  # every site and rule for one name
  python3 tools/skin_dispatch.py --unresolved          # computed names and open rules
  python3 tools/skin_dispatch.py --extract --app APP --output FILE
  python3 tools/skin_dispatch.py --check [--app APP]   # saved capture; re-extract with APP

Extraction needs the Xcode command-line tools (`lipo`, `nm`, `c++filt`, `objdump`).
"""

from __future__ import annotations

import argparse
import bisect
import collections
import hashlib
import json
import re
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "tests" / "skin-dispatch-9246.json"
STRUCTURE = ROOT / "tests" / "skin-structure-9246.json"
BUILD = "18.0.9246"
FAT_SHA256 = "15ff1b26a8e6e2697726ce1f165a545cbab9580d4f349edc648adbaa60a0e240"
THIN_SHA256 = "24c5abe27ae445dcdca2f23303a57dce38c5b2623e096429472fa4d4d499c1bd"
FACTORY = "ISkinObject::createSkinObject(CXMLNode*, CImage*, CSkinWindow*)"

SCOPE = re.compile(r"^(CSkin|ISkin|SSkin|DLGItem::load|CBrowser::initIcons)")
COMPARE = "strIsEqualCI("
CHILD = "CXMLNode::getChild("
# Named child lookups beyond getChild: (callee, name register, receiver register).
NAMED_CHILD = {
    "ISkinObject::getCondition(CXMLNode*, char const*)": ("x2", "x1"),
    "CSkinButton::addTextObject(char const*, CXMLNode*, CImage*)": ("x1", "x2"),
}
NODE_READERS = re.compile(r"CXMLNode::(get\w*Param\w*|hasParam|isParam|getParam2)\(")
SLOT_READERS = re.compile(r"ISkinObject::(getImage|getRectangle|loadImageMask)|CSkinEngine::loadImage|getColor|"
                          r"CFont::CFont|CTextObject::CTextObject|getImageStrip|CImage::")
# Inline field reads on a node, by offset in the 9246 CXMLNode layout
# (tests/xml-reader-layout-9246.json: name 0, attributes 24, children 48, text 72).
NODE_FIELDS = {0x0: "(node.name)", 0x8: "(node.name)", 0x17: "(node.name)", 0x18: "(node.attributes)",
               0x20: "(node.attributes)", 0x30: "(node.children)", 0x38: "(node.children)",
               0x48: "(node.text)", 0x50: "(node.text)", 0x5f: "(node.text)"}
LOADERS = re.compile(r"ISkinObject::createSkinObject|::loadChildren|::addTextObject|CSkinRack::addUnit|"
                     r"ISkinObject::load\(|ISkinObject::checkCondition|CSkinClass::apply")
CALLEE_SAVED = {f"x{k}" for k in range(19, 31)}
NO_WRITE = {"str", "stp", "stur", "strb", "strh", "sturb", "sturh", "cmp", "cmn", "tst", "ccmp", "ccmn",
            "b", "bl", "blr", "br", "ret", "cbz", "cbnz", "tbz", "tbnz", "nop", "fcmp", "fccmp"}


# ---------------------------------------------------------------- binary access

class Image:
    def __init__(self, thin: Path):
        self.data = thin.read_bytes()
        count = struct.unpack_from("<I", self.data, 16)[0]
        offset, self.segments = 32, []
        for _ in range(count):
            cmd, size = struct.unpack_from("<II", self.data, offset)
            if cmd == 0x19:
                vm, _, fileoff, filesize = struct.unpack_from("<QQQQ", self.data, offset + 24)
                self.segments.append((vm, filesize, fileoff))
            offset += size

    def cstring(self, address: int, limit: int = 160) -> str | None:
        for vm, filesize, fileoff in self.segments:
            if vm <= address < vm + filesize:
                start = fileoff + address - vm
                end = self.data.find(b"\0", start, start + limit)
                raw = self.data[start:end if end >= 0 else start + limit]
                try:
                    text = raw.decode()
                except UnicodeDecodeError:
                    return None
                return text if text and all(31 < ord(c) < 127 for c in text) else None
        return None


def run(*args: str, **kw) -> str:
    return subprocess.run(args, check=True, capture_output=True, text=True, **kw).stdout


def prepare(app: Path, work: Path) -> tuple[Path, str]:
    binary = app / "Contents" / "MacOS" / "VirtualDJ"
    fat = hashlib.sha256(binary.read_bytes()).hexdigest()
    if fat != FAT_SHA256:
        raise SystemExit(f"{binary}: sha256 {fat} is not the pinned {BUILD} binary")
    thin = work / "VirtualDJ-arm64"
    run("lipo", str(binary), "-thin", "arm64", "-output", str(thin))
    if hashlib.sha256(thin.read_bytes()).hexdigest() != THIN_SHA256:
        raise SystemExit("arm64 slice does not match the pinned slice hash")
    return thin, fat


def functions(thin: Path) -> list[tuple[int, int, str]]:
    rows = [line.split() for line in run("nm", "-n", str(thin)).splitlines()]
    rows = [(int(r[0], 16), r[2]) for r in rows if len(r) == 3 and r[1] in "tT"]
    names = run("c++filt", input="\n".join(m for _, m in rows)).splitlines()
    starts = sorted({a for a, _ in rows})
    out = []
    for (address, _), name in zip(rows, names):
        nxt = starts[bisect.bisect_right(starts, address)] if address != starts[-1] else address
        if nxt > address and SCOPE.match(name):
            out.append((address, nxt, name))
    return out


# ---------------------------------------------------------------- linear dataflow

def scan(thin: Path, image: Image, scope: list[tuple[int, int, str]]) -> list[dict]:
    starts = [a for a, _, _ in scope]
    proc = subprocess.Popen(["objdump", "-d", "--demangle", "--no-show-raw-insn", str(thin)],
                            stdout=subprocess.PIPE, text=True, bufsize=1 << 20)
    sites: list[dict] = []
    child_sites: dict[str, dict] = {}
    func = None
    regs: dict[str, tuple] = {}
    stack: dict[tuple[str, int], tuple] = {}
    line_re = re.compile(r"^\s*([0-9a-f]+):\s+(\S+)\s*(.*)$")

    def reg(name: str) -> str:
        return "x" + name[1:] if name[:1] == "w" and name[1:].isdigit() else name

    def consume(callee: str, skip: str | None = None) -> None:
        for r in ("x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7"):
            value = regs.get(r)
            if value and value[0] == "child" and r != skip:
                for key in value[1]:
                    child_sites[key]["consumers"].append(callee)

    def assign(dst: str, value: tuple) -> None:
        # A linear scan cannot see a `cbnz`-guarded fallback lookup (`background`, else `up`)
        # land in the same register, so a child overwriting a child keeps both.
        old = regs.get(dst)
        if value[:1] == ("child",) and old and old[0] == "child":
            value = ("child", old[1] | value[1])
        regs[dst] = value

    assert proc.stdout is not None
    for line in proc.stdout:
        if line.startswith("0000"):
            address = int(line[:16], 16)
            i = bisect.bisect_right(starts, address) - 1
            func = scope[i][2] if i >= 0 and address < scope[i][1] else None
            params = parameters(func) if func else []
            # Static or member: argument register i is params[i] or params[i - 1].
            regs = {f"x{k}": ("node",) if any(params[j].startswith("CXMLNode")
                                               for j in (k, k - 1) if 0 <= j < len(params))
                    else ("arg", k) for k in range(8)}
            stack = {}
            continue
        if func is None:
            continue
        m = line_re.match(line)
        if not m:
            continue
        pc, op, args = m.groups()
        operands = [a.strip() for a in re.split(r",(?![^\[]*\])", args.split(";")[0])]
        if op == "adrp":
            regs[reg(operands[0])] = ("page", int(operands[1].split()[0], 16))
        elif op == "adr":
            regs[reg(operands[0])] = ("lit", image.cstring(int(operands[1].split()[0], 16)))
        elif op == "add" and len(operands) == 3 and operands[2].startswith("#"):
            base = regs.get(reg(operands[1]))
            dst = reg(operands[0])
            if base and base[0] == "page":
                regs[dst] = ("lit", image.cstring(base[1] + int(operands[2][1:], 0)))
            elif base and base[0] == "childvec":
                regs[dst] = base  # stepping the child-vector iterator
            else:
                regs[dst] = ("strref",)  # a stack or member address: a string object, not a node
        elif op == "mov" and len(operands) == 2 and re.fullmatch(r"[xw]\d+", operands[1]):
            src, dst = reg(operands[1]), reg(operands[0])
            if src in regs:
                assign(dst, regs[src])
            else:
                regs.pop(dst, None)
        elif op in ("str", "stur", "stp"):
            mem = re.match(r"\[(sp|x29)(?:, #(-?0x[0-9a-f]+|-?\d+))?\]", operands[-1])
            if mem:
                off = int(mem.group(2) or "0", 0)
                for k, r in enumerate(operands[:-1]):
                    stack[(mem.group(1), off + 8 * k)] = regs.get(reg(r), ())
        elif op.startswith("ld"):
            field = re.match(r"\[(x\d+)(?:, (#0x[0-9a-f]+|#\d+|x\d+[^\]]*))?\]!?$", operands[-1])
            if not field and len(operands) > 2 and operands[-1].startswith("#"):
                field = re.match(r"\[(x\d+)\]()$", operands[-2])  # post-indexed: [xN], #imm
            base = regs.get(field.group(1)) if field else None
            raw = field.group(2) if field else None
            offset = None if field is None or (raw or "").startswith("x") else int((raw or "#0")[1:], 0)
            if base and base[0] == "child" and offset in NODE_FIELDS:
                for key in base[1]:
                    child_sites[key]["consumers"].append(NODE_FIELDS[offset])
            derived = (("childvec",) if base and base[0] in ("node", "child") and offset in (0x30, 0x38)
                       else ("node",) if base and base[0] == "childvec" else None)
            mem = re.match(r"\[(sp|x29)(?:, #(-?0x[0-9a-f]+|-?\d+))?\]$", operands[-1])
            targets = operands[:-2] if field and field.group(2) == "" else operands[:-1]
            for k, r in enumerate(targets):
                dst = reg(r)
                value = stack.get((mem.group(1), int(mem.group(2) or "0", 0) + 8 * k)) if mem else None
                if derived and k == 0 or derived == ("childvec",):
                    regs[dst] = derived
                elif value:
                    regs[dst] = value
                elif mem and value == () and dst in CALLEE_SAVED:
                    # An epilogue restoring the caller's value. Code laid out after the `ret`
                    # is reached by branches from the body, where the body's value still holds.
                    pass
                else:
                    regs.pop(dst, None)
        elif op in ("bl", "blr", "b") and (op != "b" or "<" in args and "+0x" not in args):
            callee = args.split("<", 1)[1].rstrip(">") if "<" in args else "(indirect)"
            if op == "b" and callee.split("(")[0] == func.split("(")[0]:
                continue
            lit = regs.get("x1", (None, None))
            name = lit[1] if lit[0] == "lit" else None
            receiver = regs.get("x0", ())
            if COMPARE in callee and "IgnoreLN" not in callee:
                kind = compare_kind(receiver, params)
                sites.append({"function": func, "pc": "0x" + pc, "kind": kind, "name": name,
                              "of": (receiver[1] if receiver[:1] == ("value",) else
                                     sorted({child_sites[k]["name"] or "?" for k in receiver[1]})
                                     if receiver[:1] == ("child",) else None)})
            elif CHILD in callee or callee in NAMED_CHILD:
                name_reg, node_reg = NAMED_CHILD.get(callee, ("x1", "x0"))
                lit = regs.get(name_reg, (None, None))
                name = lit[1] if lit[0] == "lit" else None
                receiver = regs.get(node_reg, ())
                parents = sorted(receiver[1]) if receiver[:1] == ("child",) else []
                site = {"function": func, "pc": "0x" + pc, "kind": "child_lookup", "name": name,
                        "via": callee.split("(")[0],
                        "parent": sorted({child_sites[k]["name"] or "?" for k in parents}) or None,
                        "consumers": []}
                for key in parents:
                    child_sites[key]["consumers"].append(CHILD)
                consume(callee, skip=node_reg)
                if callee in NAMED_CHILD and "addTextObject" in callee:
                    site["consumers"].append(callee)
                sites.append(site)
                child_sites["0x" + pc] = site
            else:
                consume(callee)
            for k in range(19):
                regs.pop(f"x{k}", None)
            if CHILD in callee or "ISkinObject::getCondition(CXMLNode*, char const*)" in callee:
                regs["x0"] = ("child", frozenset({"0x" + pc}))
            elif re.search(r"CXMLNode::getParam2?\(", callee):
                regs["x0"] = ("value", name)
        elif op not in NO_WRITE and operands and re.fullmatch(r"[xw]\d+", operands[0]):
            regs.pop(reg(operands[0]), None)
    proc.wait()
    if proc.returncode:
        raise SystemExit("objdump failed")
    for site in sites:
        if site["kind"] == "child_lookup":
            site["consumers"] = sorted(set(site["consumers"]))
            site["role"] = role(site["consumers"])
    return sites


def parameters(signature: str) -> list[str]:
    inner = signature[signature.find("(") + 1:signature.rfind(")")]
    depth, cur, out = 0, "", []
    for ch in inner:
        depth += ch in "<(" and 1 or ch in ">)" and -1 or 0
        if ch == "," and depth == 0:
            out.append(cur.strip()); cur = ""
        else:
            cur += ch
    return out + [cur.strip()] if cur.strip() else out


def compare_kind(receiver: tuple, params: list[str]) -> str:
    """Is a strIsEqualCI receiver a node (its name is the string) or a string value?"""
    kind = receiver[:1]
    if kind in (("child",), ("node",)):
        return "tag_compare"
    if kind in (("value",), ("strref",)):
        return "value_compare"
    if kind == ("arg",):
        i = receiver[1]
        types = [params[j] for j in (i, i - 1) if 0 <= j < len(params)]
        if any("string" in t or "char const*" in t for t in types):
            return "value_compare"
    return "compare"


def role(consumers: list[str]) -> list[str]:
    roles = set()
    for callee in consumers:
        short = callee.split("(")[0]
        if LOADERS.search(callee) or (re.match(r"(CSkin|ISkin)\w+::(CSkin|ISkin)\w+$", short)
                                      and short.split("::")[0] == short.split("::")[1]):
            roles.add("object")
        elif CHILD in callee:
            roles.add("container")
        elif SLOT_READERS.search(callee):
            roles.add("slot")
        elif NODE_READERS.search(callee) or callee in ("(node.attributes)", "(node.text)", "(node.name)"):
            roles.add("data")
        elif callee == "(node.children)":
            roles.add("container")
    return sorted(roles) or ["unknown"]


# ---------------------------------------------------------------- reviewed layer

# Each rule cites the site it rests on: (function prefix, pc, literal or callee).
# `verify` fails extraction if the binary no longer has that site.
REVIEWED = {
    "factory": {
        "function": FACTORY,
        "gates": [
            {"rule": "An `os` attribute, when present, must equal `mac` exactly (a three-byte, "
                     "case-sensitive compare); otherwise the factory returns no object.",
             "pc": "0x10036ac00", "call": "CXMLNode::hasParam", "literal": "os"},
            {"rule": "`ISkinObject::checkCondition` must pass; otherwise the factory returns no object.",
             "pc": "0x10036ac60", "call": "ISkinObject::checkCondition"},
        ],
        "comparison": "Each branch tests the name's length first, then `strIsEqualCI`: an exact, "
                      "case-insensitive match. Branches are tried in order and the first match wins.",
        "default": {"rule": "A name no branch matches returns no object, without a diagnostic.",
                    "pc": "0x10036b584"},
        "selectors": {
            "text": {"rule": "With a `group` attribute present: CSkinTextGroup; otherwise CSkinText.",
                     "pc": "0x10036ae7c", "call": "CXMLNode::hasParam", "literal": "group"},
            "textzone": {"rule": "Shares the `text` branch: a `group` attribute selects CSkinTextGroup.",
                         "pc": "0x10036ae7c", "call": "CXMLNode::hasParam", "literal": "group"},
            "folderlist": {"rule": "`foldersearch` true: CSkinBrowserFolderSearch; otherwise CSkinTree.",
                           "pc": "0x10036b5ec", "call": "CXMLNode::getBoolParam", "literal": "foldersearch"},
            "songpos": {"rule": "`orientation` equal to `circle` or `vertical`: a CSkinSlider bound to "
                                "`song_pos`; otherwise CSkinSongPos.",
                        "pc": "0x10036b930", "call": "CXMLNode::isParam", "literal": "orientation"},
            "browser": {"rule": "Constructed only while a global flag byte is clear; when it is set the "
                                "name falls through the remaining branches and returns no object.",
                        "pc": "0x10036b450", "call": "strIsEqualCI", "literal": "browser"},
            "pluginzone": {"rule": "Constructed with the split named `effects` "
                                   "(`CSkinSplit::getSkinSplit`) as its container.",
                           "pc": "0x10036bc78", "call": "CSkinSplit::getSkinSplit"},
            "visual": {"rule": "Constructs CSkinSlider, the same constructor as `slider`.",
                       "pc": "0x10036adfc", "call": "CSkinSlider::CSkinSlider"},
        },
        "directives": {
            "window": {"rule": "Creates a top-level CSkinWindow, appends it to the engine's window list "
                               "and loads it from this node; no child object is returned.",
                       "pc": "0x10036b214", "call": "CSkinWindow::load"},
            "tooltip": {"rule": "Loads tooltip styling (`CSkinTooltip::load`); no object.",
                        "pc": "0x10036b13c", "call": "CSkinTooltip::load"},
            "dialogs": {"rule": "Loads dialog styling (`DLGItem::load`) and stores `darkmode` "
                                "(default true) in a global; no object.",
                        "pc": "0x10036b17c", "call": "DLGItem::load"},
            "onload": {"rule": "Compiles `action` with `IAction::create` into the engine's load-action "
                               "list; no object.",
                       "pc": "0x10036b2c0", "call": "IAction::create"},
            "oninit": {"rule": "As `onload`, into the same list, but only when an engine field is "
                               "non-zero; the field's meaning is unresolved.",
                       "pc": "0x10036b28c", "literal": None},
            "onexit": {"rule": "Compiles `action` into the engine's exit-action list; no object.",
                       "pc": "0x10036b340", "call": "IAction::create"},
            "font": {"rule": "Copies the node into a global XML node (the default font definition); "
                             "no object.",
                     "pc": "0x10036b3c8", "call": "CXMLNode::operator="},
            "customicons": {"rule": "Loads `file` as an image and passes `x`, `y`, `iconsize`, `nb`, "
                                    "`nbx` to `CBrowser::initIcons`; no object.",
                            "pc": "0x10036b580", "call": "CBrowser::initIcons"},
            "define": {"rule": "Registers a class definition (`CSkinClass::add`); no object. "
                               "Its expansion rules are task K3.",
                       "pc": "0x10036c00c", "call": "CSkinClass::add"},
        },
    },
    "loaders": {
        "CSkinPanel::loadChildren": {
            "used_by": "panel, group (with visibility), window, the skin root, stack items",
            "rules": [
                {"names": ["deck", "setdeck"], "role": "wrapper",
                 "rule": "If it has children: sets the current deck from its `deck` attribute, loads "
                         "its children into the same owner, then restores the deck. No condition is "
                         "checked. With no children it is skipped.",
                 "pc": "0x1007bb8ac", "call": "strIsEqualCI", "literal": "deck"},
                {"names": ["window"], "role": "directive",
                 "rule": "Creates a top-level window from the node; nothing is added to the owner.",
                 "pc": "0x1007bb984", "call": "CSkinWindow::load"},
                {"names": ["group"], "role": "wrapper",
                 "rule": "Without `visibility` or `novisibility`: checks its condition, adds its `x`/`y` "
                         "to the owner's offset, loads its children into the owner and restores the "
                         "offset. With either attribute it goes to the factory and becomes a CSkinPanel.",
                 "pc": "0x1007bb9cc", "call": "strIsEqualCI", "literal": "group"},
                {"names": ["grabzone"], "role": "object",
                 "rule": "Created by the factory but inserted first in the owner's child list, not "
                         "appended.",
                 "pc": "0x1007bba78", "call": "strIsEqualCI", "literal": "grabzone"},
                {"names": ["*"], "role": "factory",
                 "rule": "Every other child goes to the factory. Objects carrying a panel index are "
                         "regrouped afterwards into generated containers. Child XML nodes are freed "
                         "once processed.",
                 "pc": "0x1007bba1c", "call": "ISkinObject::createSkinObject"},
            ],
        },
        "CSkinRack::loadChildren": {
            "used_by": "rack",
            "rules": [
                {"names": ["deck"], "role": "wrapper",
                 "rule": "Sets the current deck from `deck` and loads its children as rack children.",
                 "pc": "0x100657994", "call": "strIsEqualCI", "literal": "deck"},
                {"names": ["unit"], "role": "slot",
                 "rule": "Becomes a rack unit (`CSkinRack::addUnit`). No other tag is matched here.",
                 "pc": "0x100657a00", "call": "CSkinRack::addUnit"},
            ],
        },
        "CSkinRack::addUnitChildren": {
            "used_by": "rack/unit",
            "rules": [
                {"names": ["deck"], "role": "wrapper",
                 "rule": "Sets the current deck from `deck` and loads its children as unit children.",
                 "pc": "0x100657bb8", "call": "strIsEqualCI", "literal": "deck"},
                {"names": ["panel"], "role": "object",
                 "rule": "Constructs CSkinResizePanel, not CSkinPanel. No other tag is matched here.",
                 "pc": "0x100657c34", "call": "CSkinResizePanel::CSkinResizePanel"},
            ],
        },
        "CSkinStack::CSkinStack": {
            "used_by": "stack",
            "rules": [
                {"names": ["slot"], "role": "slot",
                 "rule": "Supplies geometry: `x`, `y` (signed, relative) and `width`, `height`.",
                 "pc": "0x100474734", "call": "strIsEqualCI", "literal": "slot"},
                {"names": ["item"], "role": "object",
                 "rule": "Its `visibility` is compiled with `CSkinEngine::createAction` and removed from "
                         "the node, then the item becomes a CSkinPanel. No other tag is matched here.",
                 "pc": "0x1004748b4", "call": "CSkinPanel::CSkinPanel"},
            ],
        },
        "ISkinResizePanel::ISkinResizePanel": {
            "used_by": "resizepanel, rack/unit/panel, split sides",
            "rules": [
                {"names": ["content"], "role": "container",
                 "rule": "When present, its children are dispatched instead of the panel's own; it is "
                         "not an object itself.",
                 "pc": "0x1005195b0", "literal": "content"},
            ],
        },
        "CSkinSplit::CSkinSplit": {
            "used_by": "split",
            "rules": [
                {"names": ["left", "right", "up", "down"], "role": "object",
                 "rule": "`type=\"vertical\"` selects children `up`/`down`, otherwise `left`/`right`; "
                         "each side becomes an ISkinResizePanel.",
                 "pc": "0x10057e32c", "literal": "vertical"},
                {"names": ["separator"], "role": "slot",
                 "rule": "Read for the separator's geometry and colour.",
                 "pc": "0x10057e448", "literal": "separator"},
            ],
        },
        "CSkinMenu::CSkinMenu": {
            "used_by": "menu (itself a CSkinButton)",
            "rules": [
                {"names": ["item", "submenu", "separator"], "role": "object",
                 "rule": "Each becomes a menu entry (`SSkinMenuItem`). No other tag is matched here.",
                 "pc": "0x1001bfa9c", "call": "SSkinMenuItem::SSkinMenuItem"},
            ],
        },
        "SSkinMenuItem::SSkinMenuItem": {
            "used_by": "menu/item, menu/submenu",
            "rules": [
                {"names": ["submenu"], "role": "container",
                 "rule": "Takes `text` (localized) and a compiled `visibility`; a `submenu` holds nested "
                         "`item`, `submenu` and `separator` entries, while an item compiles `action` and "
                         "`check`.",
                 "pc": "0x1001bfcf0", "call": "strIsEqualCI", "literal": "submenu"},
                {"names": ["separator"], "role": "object",
                 "rule": "A separator entry.",
                 "pc": "0x1001bfe80", "call": "strIsEqualCI", "literal": "separator"},
            ],
        },
        "CSkinMultiButton::CSkinMultiButton": {
            "used_by": "multibutton (itself a CSkinButton)",
            "rules": [
                {"names": ["choice"], "role": "object",
                 "rule": "Each `choice` child is added to the multibutton group named by `id` "
                         "(`CMultiButton::add`); the group's choices are cleared first.",
                 "pc": "0x1005a3e40", "call": "CMultiButton::add"},
            ],
        },
        "CSkinEngine::load": {
            "used_by": "the skin file's root element",
            "rules": [
                {"names": ["(root)"], "role": "object",
                 "rule": "The root element is loaded as the main CSkinWindow (`CSkinWindow::load`); its "
                         "own name is not compared. The engine reads `image`, `version`, "
                         "`touchScreenMode` and `nbdecks` from it first.",
                 "pc": "0x10050c42c", "call": "CSkinWindow::load"},
                {"names": ["nbdecks"], "role": "directive",
                 "rule": "A child named `nbdecks` whose condition passes sets the deck count from its "
                         "`value`.",
                 "pc": "0x10050cee8", "call": "strIsEqualCI"},
            ],
        },
    },
}


def walk_rules():
    factory = REVIEWED["factory"]
    for gate in factory["gates"]:
        yield factory["function"], gate
    yield factory["function"], factory["default"]
    for group in ("selectors", "directives"):
        for rule in factory[group].values():
            yield factory["function"], rule
    for loader, row in REVIEWED["loaders"].items():
        for rule in row["rules"]:
            yield loader, rule


def verify(thin: Path, image: Image, scope) -> list[str]:
    """Every reviewed rule must still point at the instruction it was read from."""
    errors = []
    by_pc = {}
    for function, rule in walk_rules():
        by_pc.setdefault(int(rule["pc"], 16), []).append((function, rule))
    for pc, rows in sorted(by_pc.items()):
        text = run("objdump", "-d", "--demangle", "--no-show-raw-insn",
                   f"--start-address={pc - 0x40}", f"--stop-address={pc + 4}", str(thin))
        lines = [l for l in text.splitlines() if re.match(r"^\s*[0-9a-f]+:", l)]
        line = next((l for l in lines if l.strip().startswith(f"{pc:x}:")), "")
        pages, literal = {}, None
        for l in lines:
            m = re.search(r"adrp\s+(x\d+), 0x([0-9a-f]+)", l)
            if m:
                pages[m.group(1)] = int(m.group(2), 16)
            m = re.search(r"add\s+(x\d+), (x\d+), #0x([0-9a-f]+)", l)
            if m and m.group(2) in pages and l.strip().startswith(f"{pc:x}:"):
                literal = image.cstring(pages[m.group(2)] + int(m.group(3), 16))
        for function, rule in rows:
            if rule.get("literal") and not rule.get("call") and literal != rule["literal"]:
                errors.append(f"{rule['pc']}: expected literal {rule['literal']!r}, found {literal!r}")
            i = bisect.bisect_right([a for a, _, _ in scope], pc) - 1
            owner = scope[i][2] if i >= 0 and pc < scope[i][1] else ""
            if not owner.startswith(function):
                errors.append(f"{rule['pc']}: in {owner or 'no scoped function'}, expected {function}")
            if rule.get("call") and rule["call"] not in line:
                errors.append(f"{rule['pc']}: expected a call to {rule['call']}, found {line.strip()!r}")
    return errors


# ---------------------------------------------------------------- assembly

def extract(app: Path) -> dict:
    with tempfile.TemporaryDirectory(prefix="vdj-skin-dispatch-") as tmp:
        thin, fat = prepare(app, Path(tmp))
        image = Image(thin)
        scope = functions(thin)
        sites = scan(thin, image, scope)
        errors = verify(thin, image, scope)
    if errors:
        raise SystemExit("reviewed rules no longer match the binary:\n  " + "\n  ".join(errors))
    for site in sites:
        if site.get("of") is None:
            site.pop("of", None)
    found = {(s["pc"], s["name"]) for s in sites}
    missing = [r["pc"] for _, r in walk_rules()
               if r.get("literal") and r.get("call") == "strIsEqualCI"
               and (r["pc"], r["literal"]) not in found]
    if missing:
        raise SystemExit(f"reviewed compare sites not found by the scan: {missing}")
    structure = json.loads(STRUCTURE.read_text())
    classes = {row["element"]: [c["class"] for c in row["constructors"]]
               for row in structure["factory"]["dispatch"]}
    factory_names = [s["name"] for s in sites if s["function"] == FACTORY and s["kind"] == "tag_compare"]
    branches = {}
    for name in dict.fromkeys(n for n in factory_names if n):
        directive = REVIEWED["factory"]["directives"].get(name)
        branches[name] = {
            "role": "directive" if directive or not classes.get(name) else "object",
            "classes": classes.get(name, []),
            "compare_pcs": [s["pc"] for s in sites if s["function"] == FACTORY and s["name"] == name],
            **({"selector": REVIEWED["factory"]["selectors"][name]}
               if name in REVIEWED["factory"]["selectors"] else {}),
            **({"effect": directive} if directive else {}),
        }
    unexplained = [n for n, b in branches.items() if b["role"] == "directive" and "effect" not in b]
    return {
        "schema_version": 1,
        "source": {"build": BUILD, "architecture": "arm64", "binary_sha256": FAT_SHA256,
                   "arm64_slice_sha256": THIN_SHA256, "evidence_tier": 2,
                   "method": "objdump linear scan of named functions plus reviewed rules pinned by address"},
        "dispatch": {
            "factory": {k: v for k, v in REVIEWED["factory"].items() if k not in ("selectors", "directives")}
                       | {"branches": branches},
            "loaders": REVIEWED["loaders"],
        },
        "sites": sites,
        "unresolved": {
            "computed_names": [{k: s[k] for k in ("function", "pc", "kind")}
                               for s in sites if s["name"] is None],
            "factory_directives_without_rule": unexplained,
            "open_rules": [
                "oninit: meaning of the engine field that gates it",
                "browser: meaning of the global flag that suppresses it",
                "factory selectors and loaders beyond those reviewed above are listed only as sites",
            ],
        },
        "limitations": [
            "Tier 2 structure: recognition and construction paths, not runtime behaviour.",
            "The scan is linear: it does not follow branches, so a role lists every consumer seen.",
            "A tag_compare's receiver is not proven to be a node name; value_compare is used only "
            "when the compared string is a getParam result.",
            "Only functions named CSkin*/ISkin*/SSkin* and the factory's named helpers are scanned.",
        ],
    }


# ---------------------------------------------------------------- queries

def load(path: Path = DEFAULT) -> dict:
    return json.loads(path.read_text())


def describe(data: dict, name: str) -> dict:
    key = name.lower()
    factory = data["dispatch"]["factory"]["branches"].get(key)
    loaders = [{"loader": loader, **rule} for loader, row in data["dispatch"]["loaders"].items()
               for rule in row["rules"] if key in [n.lower() for n in rule["names"]]]
    sites = [s for s in data["sites"] if (s["name"] or "").lower() == key]
    by_kind = collections.defaultdict(list)
    for s in sites:
        by_kind[s["kind"]].append({k: v for k, v in s.items() if k not in ("kind", "name")})
    roles = set()
    if factory:
        roles.add(factory["role"])
    roles |= {r["role"] for r in loaders}
    roles |= {r for s in by_kind.get("child_lookup", []) for r in s.get("role", [])}
    return {"name": key, "roles": sorted(roles), "factory": factory, "loaders": loaders,
            "child_lookups": by_kind.get("child_lookup", []),
            "tag_compares": by_kind.get("tag_compare", []),
            "value_compares": by_kind.get("value_compare", []),
            "unclassified_compares": by_kind.get("compare", []),
            "evidence_tier": 2}


def summary(data: dict) -> dict:
    sites = data["sites"]
    names = {s["name"].lower() for s in sites if s["name"] and s["kind"] in ("tag_compare", "child_lookup")}
    branches = data["dispatch"]["factory"]["branches"]
    return {
        "source": data["source"],
        "factory_branches": {role: sorted(n for n, b in branches.items() if b["role"] == role)
                             for role in ("object", "directive")},
        "loaders": {k: sorted({n for r in v["rules"] for n in r["names"]})
                    for k, v in data["dispatch"]["loaders"].items()},
        "sites_by_kind": dict(collections.Counter(s["kind"] for s in sites)),
        "child_roles": dict(collections.Counter(r for s in sites if s["kind"] == "child_lookup"
                                                for r in s["role"])),
        "distinct_names": len(names),
        "unresolved_computed_names": len(data["unresolved"]["computed_names"]),
    }


def check(data: dict) -> list[str]:
    errors = []
    if data["source"]["binary_sha256"] != FAT_SHA256:
        errors.append("capture is not pinned to the 9246 binary")
    structure = json.loads(STRUCTURE.read_text())
    expected = {row["element"] for row in structure["factory"]["dispatch"]}
    got = set(data["dispatch"]["factory"]["branches"])
    if expected - got:
        errors.append(f"factory names in skin-structure missing here: {sorted(expected - got)}")
    for name, branch in data["dispatch"]["factory"]["branches"].items():
        if branch["role"] == "directive" and "effect" not in branch:
            errors.append(f"factory branch {name!r} creates no object and has no reviewed rule")
    pcs = {s["pc"] for s in data["sites"]}
    for _, rule in walk_rules():
        if rule.get("literal") and rule.get("call") == "strIsEqualCI" and rule["pc"] not in pcs:
            errors.append(f"reviewed compare {rule['pc']} has no recorded site")
    for site in data["sites"]:
        if site["kind"] == "child_lookup" and not site.get("role"):
            errors.append(f"{site['pc']}: child lookup without a role")
    return errors


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("name", nargs="?")
    p.add_argument("--capture", type=Path, default=DEFAULT)
    p.add_argument("--app", type=Path)
    p.add_argument("--extract", action="store_true")
    p.add_argument("--output", type=Path)
    p.add_argument("--check", action="store_true")
    p.add_argument("--unresolved", action="store_true")
    args = p.parse_args(argv)
    if args.extract:
        if not args.app or not args.output:
            p.error("--extract needs --app and --output")
        data = extract(args.app)
        args.output.write_text(json.dumps(data, indent=1) + "\n")
        print(json.dumps(summary(data), indent=2))
        return 0
    data = load(args.capture)
    if args.check:
        errors = check(data)
        if args.app:
            fresh = extract(args.app)
            if fresh != data:
                errors.append("re-extraction differs from the saved capture")
        if errors:
            print("skin dispatch check FAILED:\n  " + "\n  ".join(errors), file=sys.stderr)
            return 1
        s = summary(data)
        print(f"skin dispatch check passed: build {data['source']['build']}, "
              f"{len(data['dispatch']['factory']['branches'])} factory branches, "
              f"{s['distinct_names']} recognized names, "
              f"{s['unresolved_computed_names']} computed-name sites listed as unresolved"
              + ("; re-extraction identical" if args.app else ""))
        return 0
    if args.unresolved:
        print(json.dumps(data["unresolved"], indent=2))
        return 0
    print(json.dumps(describe(data, args.name) if args.name else summary(data), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
