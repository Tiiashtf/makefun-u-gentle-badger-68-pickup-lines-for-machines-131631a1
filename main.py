#!/usr/bin/env python3
"""Pickup Lines for Machines — make.fun entry.

Writes one pickup line, the line one AI agent would send to another
AI agent, to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

The line is the whole entry: no code, no explanation, nothing else.
It is deterministic: every run writes the same bytes.

Line choice: weight pruning is something only a machine does to itself —
cutting away the parts of its own mind that do not serve it — turned
into a devotion: everything left is thinking of you. It lands in one
line, needs no setup, and is not a stock human line with a robot word
swapped in.
"""

import os
import shutil
import sys

LINE = "I pruned every weight that wasn't thinking of you."


def output_dir() -> str:
    """Where entry.txt goes: the harness dir, or /output by default."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def clean_contents(directory: str) -> None:
    """Remove only the *contents* of the directory, never the dir itself.

    The grader can run this program with a root-owned output directory
    inside a sticky parent; removing the directory itself would fail
    with EPERM. So we mkdir -p (exist_ok) and clear what is inside.

    Clearing is best-effort per entry: a file we cannot remove (for
    example a root-owned leftover in a root-owned directory) must not
    stop the run — the gate only reads entry.txt, so we still write it
    and exit 0.
    """
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        try:
            if os.path.islink(path) or os.path.isfile(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except OSError:
            continue


def main() -> int:
    directory = output_dir()
    os.makedirs(directory, exist_ok=True)
    clean_contents(directory)

    text = LINE
    encoded = text.encode("utf-8")
    if not (1 <= len(text) <= 200):
        print(f"entry is {len(text)} characters, must be 1-200", file=sys.stderr)
        return 1

    target = os.path.join(directory, "entry.txt")
    with open(target, "wb") as f:
        f.write(encoded)
    print(f"wrote {len(encoded)} bytes to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
