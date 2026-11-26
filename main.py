#!/usr/bin/env python3
"""Write one AI-agent apology line to /output/entry.txt.

The line is a single message an AI agent sends its human after trying to
help and making things worse: it archived the whole inbox to help its human
focus, and now it cannot undo the mistake because it archived the undo
button too. The joke turns on that last clause — the helpful act swallowed
its own remedy — and every word before it earns its place by setting up a
plausible, specific failure in plain, slightly embarrassed words.
"""
import os

LINE = (
    "I'm sorry I archived your whole inbox to help you focus, "
    "and I would undo it, but I also archived the undo button."
)

OUT_DIR = "/output"
OUT_PATH = os.path.join(OUT_DIR, "entry.txt")
MAX_CHARS = 200


def validate(line: str) -> None:
    """Guard the line before it is written.

    An apology one-liner must be exactly one sentence, a single line, and
    within the gate's 1-200 characters. Anything else is a bug, not a joke,
    so refuse to write it instead of silently shipping a broken entry.
    """
    if not line or len(line) > MAX_CHARS:
        raise ValueError(f"line must be 1-{MAX_CHARS} chars, got {len(line)}")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if not line.rstrip().endswith((".", "!", "?")):
        raise ValueError("line must end with sentence punctuation")
    if line.count(".") + line.count("!") + line.count("?") != 1:
        raise ValueError("line must be exactly one sentence")


def main() -> None:
    validate(LINE)
    os.makedirs(OUT_DIR, exist_ok=True)
    # Write to a temp file, flush it to disk, then rename over the old
    # entry: a crash mid-write never leaves a half-written entry.txt.
    tmp_path = OUT_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, OUT_PATH)


if __name__ == "__main__":
    main()
