#!/usr/bin/env python3
"""Check reference status drift and fixture inventory."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "Reference" / "Official VDJScript Coverage Audit.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def audit_numbers(errors: list[str]) -> tuple[str, str]:
    text = read(AUDIT)
    count_match = re.search(r"Official verb/alias names parsed: (\d+)", text)
    gap_match = re.search(r"The formal local-test gap is (\d+) official names", text)
    if not count_match:
        errors.append(f"{rel(AUDIT)}: missing official-name count")
    if not gap_match:
        errors.append(f"{rel(AUDIT)}: missing local-test gap count")
    return (
        count_match.group(1) if count_match else "",
        gap_match.group(1) if gap_match else "",
    )


def check_count_consistency(count: str, gap: str, errors: list[str]) -> None:
    if not count or not gap:
        return

    required = {
        ROOT / "Reference" / "VDJScript Verbs.md": [
            f"{count}/{count}",
            f"remaining {gap} sparse or hardware-specific official names",
        ],
        ROOT / "Reference" / "VDJScript Local Test Tracker.md": [
            f"parses to {count} official",
            f"gap is {gap} official names",
        ],
    }

    for path, phrases in required.items():
        text = read(path)
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"{rel(path)}: missing expected status phrase: {phrase!r}")

    stale_patterns = (
        r"\b989\b",
        r"remaining 21 sparse",
        r"21 sparse or hardware-specific official names",
        r"21 official names still marked",
    )
    scan_paths = [ROOT / "README.md", ROOT / "AGENTS.md"] + sorted((ROOT / "Reference").glob("*.md"))
    for path in scan_paths:
        text = read(path)
        for pattern in stale_patterns:
            if re.search(pattern, text):
                errors.append(f"{rel(path)}: stale status pattern still present: {pattern}")


def check_needs_local_test_count(gap: str, errors: list[str]) -> None:
    if not gap:
        return
    text = read(AUDIT)
    try:
        section = text.split("## Needs Local Test", 1)[1].split("\n## ", 1)[0]
    except IndexError:
        errors.append(f"{rel(AUDIT)}: missing Needs Local Test section")
        return

    names = re.findall(r"`([^`]+)`", section)
    expected = int(gap)
    if len(names) != expected:
        errors.append(
            f"{rel(AUDIT)}: Needs Local Test section lists {len(names)} names, expected {expected}"
        )


def check_tracked_generated_files(errors: list[str]) -> None:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    generated = [
        line
        for line in result.stdout.splitlines()
        if line.endswith(".pyc") or "__pycache__/" in line
    ]
    for path in generated:
        errors.append(f"{path}: generated Python cache file is tracked")


def check_markdown_links(errors: list[str]) -> None:
    link_re = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    roots = [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "Reference", ROOT / "xml", ROOT / "tests"]
    roots.append(ROOT / "TODO.md")
    files: list[Path] = []
    for root in roots:
        if root.is_file():
            files.append(root)
        elif root.exists():
            files.extend(sorted(root.rglob("*.md")))

    for path in files:
        text = read(path)
        for lineno, line in enumerate(text.splitlines(), 1):
            for match in link_re.finditer(line):
                target = match.group(1).split("#", 1)[0]
                if not target or "://" in target or target.startswith("mailto:"):
                    continue
                if target.startswith("<") and target.endswith(">"):
                    target = target[1:-1]
                candidate = (path.parent / unquote(target)).resolve()
                if not candidate.exists():
                    errors.append(f"{rel(path)}:{lineno}: broken local link {match.group(1)!r}")


def check_test_fixture_inventory(errors: list[str]) -> None:
    readmes = [
        ROOT / "tests" / "README.md",
        ROOT / "tests" / "Pads" / "README.md",
    ]
    fixture_names = sorted(path.name for path in (ROOT / "tests" / "Pads").glob("Reference - *.xml"))
    for readme in readmes:
        text = read(readme)
        for name in fixture_names:
            if name not in text:
                errors.append(f"{rel(readme)}: missing fixture inventory entry for {name!r}")


def main() -> int:
    errors: list[str] = []
    count, gap = audit_numbers(errors)
    check_count_consistency(count, gap, errors)
    check_needs_local_test_count(gap, errors)
    check_tracked_generated_files(errors)
    check_markdown_links(errors)
    check_test_fixture_inventory(errors)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Reference status check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
