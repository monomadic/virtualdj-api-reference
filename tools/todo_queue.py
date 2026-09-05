#!/usr/bin/env python3
"""Parse, validate, and select from the TODO.md task queue.

`TODO.md` is the repository's only active planning state, and `just next-task`
picks work out of it. The selector used to grep for an exact `Status: Ready`
line, so every decorated variant that had accumulated in the file --
`Status: **Ready.**`, `Status: Ready -- reframed`, `Status: Ready, but low
expected yield` -- was silently invisible, and the queue looked empty while
most of it was startable.

The fix is a machine-readable status line: one line, one state word from a
closed vocabulary, with every explanation moved to a following `Note:`
paragraph. This module is the parser for that convention. A status line it
cannot read is an error that stops the run, never a task it quietly skips.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TODO = ROOT / "TODO.md"
FIXTURES = ROOT / "tests" / "todo-status"

# The closed vocabulary. The state describes what is true of the task *now*:
# for a task whose first pass landed, it describes the remaining work, not the
# part that is finished -- that narrative belongs in the Note.
STATES = {
    "Ready": "startable now with the listed files and fixtures",
    "Blocked": "needs hardware or an external source not available here",
    "Conditional": "start only when the named trigger occurs",
    "Parking lot": "deliberately deferred; not the next best use of time",
    "Done": "complete; kept as the record of what was established",
}

SELECTABLE = ("Ready",)

HEADING = re.compile(r"^### (?P<id>[^.]+)\.\s*(?P<title>.+?)\s*$")
STATUS = re.compile(r"^Status:(?P<value>.*)$")


class Task:
    def __init__(self, ident: str, title: str, state: str, line: int, block: list[str]):
        self.ident = ident
        self.title = title
        self.state = state
        self.line = line
        self.block = block

    @property
    def selectable(self) -> bool:
        return self.state in SELECTABLE


def parse(text: str, source: str) -> tuple[list[Task], list[str]]:
    """Return (tasks, errors). A task with an unreadable status is an error and
    is not returned, so it can never be selected by accident."""
    lines = text.splitlines()
    errors: list[str] = []
    tasks: list[Task] = []

    starts = [i for i, line in enumerate(lines) if HEADING.match(line)]
    # A `## ` section heading ends the preceding task block.
    for pos, start in enumerate(starts):
        end = len(lines)
        for i in range(start + 1, len(lines)):
            if HEADING.match(lines[i]) or lines[i].startswith("## "):
                end = i
                break
        block = lines[start:end]
        match = HEADING.match(lines[start])
        assert match is not None
        ident, title = match.group("id").strip(), match.group("title")

        status_lines = [
            (start + offset + 1, STATUS.match(line))
            for offset, line in enumerate(block)
            if STATUS.match(line)
        ]
        if not status_lines:
            errors.append(
                f"{source}:{start + 1}: task {ident!r} has no `Status:` line"
            )
            continue
        if len(status_lines) > 1:
            where = ", ".join(str(n) for n, _ in status_lines)
            errors.append(
                f"{source}:{start + 1}: task {ident!r} has {len(status_lines)} "
                f"`Status:` lines (lines {where}); exactly one is required"
            )
            continue

        status_line, status_match = status_lines[0]
        assert status_match is not None

        # The status must be the first prose in the block: a status buried
        # below narrative is one a reader will not trust as current.
        first_prose = next(
            (start + offset + 1 for offset, line in enumerate(block[1:], start=1) if line.strip()),
            None,
        )
        if first_prose != status_line:
            errors.append(
                f"{source}:{status_line}: task {ident!r} has its `Status:` line "
                f"below other prose (first prose is line {first_prose}); the "
                "status must be the first line under the heading"
            )
            continue

        value = status_match.group("value").strip()
        if value not in STATES:
            errors.append(
                f"{source}:{status_line}: task {ident!r} has unreadable status "
                f"{value!r}; expected exactly one of "
                f"{', '.join(sorted(STATES))} with any explanation moved to a "
                "following `Note:` paragraph"
            )
            continue

        tasks.append(Task(ident, title, value, start + 1, block))

    seen: dict[str, Task] = {}
    for task in tasks:
        if task.ident in seen:
            errors.append(
                f"{source}:{task.line}: duplicate task identifier {task.ident!r} "
                f"(already used at line {seen[task.ident].line})"
            )
        else:
            seen[task.ident] = task

    return tasks, errors


def load(path: Path = TODO) -> tuple[list[Task], list[str]]:
    return parse(path.read_text(encoding="utf-8"), str(path.relative_to(ROOT)))


def cmd_check(_args: argparse.Namespace) -> int:
    tasks, errors = load()
    if errors:
        print("TODO.md status metadata is malformed:", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1
    if not any(task.selectable for task in tasks):
        print(
            "TODO.md: no task is startable; every task is Done, Blocked, "
            "Conditional, or parked. If that is wrong, a status is wrong.",
            file=sys.stderr,
        )
        return 1
    ready = sum(1 for task in tasks if task.selectable)
    print(f"todo queue OK: {len(tasks)} tasks, {ready} startable")
    return 0


def cmd_next(_args: argparse.Namespace) -> int:
    tasks, errors = load()
    if errors:
        print("TODO.md status metadata is malformed; refusing to select:", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1
    for task in tasks:
        if task.selectable:
            print("\n".join(task.block).rstrip())
            return 0
    print("No startable task in TODO.md.", file=sys.stderr)
    return 1


def cmd_list(args: argparse.Namespace) -> int:
    tasks, errors = load()
    if args.format == "json":
        payload = {
            "tasks": [
                {
                    "id": task.ident,
                    "title": task.title,
                    "status": task.state,
                    "selectable": task.selectable,
                    "line": task.line,
                }
                for task in tasks
            ],
            "errors": errors,
        }
        print(json.dumps(payload, indent=2))
        return 1 if errors else 0

    width = max((len(task.state) for task in tasks), default=0)
    for task in tasks:
        marker = "*" if task.selectable else " "
        print(f"{marker} {task.state:<{width}}  {task.ident}. {task.title}")
    for error in errors:
        print(f"  ERROR {error}", file=sys.stderr)
    return 1 if errors else 0


def cmd_selftest(_args: argparse.Namespace) -> int:
    """Run the parser over the recorded regression fixtures.

    The malformed fixture holds the real forms this file actually contained
    before the convention landed, so a future selector rewrite cannot go back
    to skipping them.
    """
    expectations = json.loads((FIXTURES / "expected.json").read_text(encoding="utf-8"))
    failures: list[str] = []
    for name, expected in sorted(expectations.items()):
        path = FIXTURES / name
        tasks, errors = parse(path.read_text(encoding="utf-8"), name)
        # Selection refuses outright when anything in the file is malformed,
        # so the expectation records what `next` would really hand back.
        selected = (
            None
            if errors
            else next((task.ident for task in tasks if task.selectable), None)
        )
        if selected != expected["next"]:
            failures.append(
                f"{name}: selected {selected!r}, expected {expected['next']!r}"
            )
        got = [task.ident for task in tasks]
        if got != expected["parsed"]:
            failures.append(f"{name}: parsed {got}, expected {expected['parsed']}")
        for fragment in expected["errors"]:
            if not any(fragment in error for error in errors):
                failures.append(
                    f"{name}: expected an error containing {fragment!r}; got {errors}"
                )
        if len(errors) != len(expected["errors"]):
            failures.append(
                f"{name}: {len(errors)} errors, expected {len(expected['errors'])}: {errors}"
            )

    for failure in failures:
        print(f"  {failure}", file=sys.stderr)
    if failures:
        print(f"todo_queue selftest FAILED ({len(failures)})", file=sys.stderr)
        return 1
    print(f"todo_queue selftest OK ({len(expectations)} fixtures)")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="alias for the `check` command")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("check", help="validate every task's status metadata").set_defaults(func=cmd_check)
    sub.add_parser("next", help="print the first startable task block").set_defaults(func=cmd_next)
    listing = sub.add_parser("list", help="print every task with its state")
    listing.add_argument("--format", choices=("text", "json"), default="text")
    listing.set_defaults(func=cmd_list)
    sub.add_parser("selftest", help="run the status-line regression fixtures").set_defaults(
        func=cmd_selftest
    )

    args = parser.parse_args(argv)
    if args.check or args.command is None:
        return cmd_check(args)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
