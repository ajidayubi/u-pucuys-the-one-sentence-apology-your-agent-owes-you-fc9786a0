#!/usr/bin/env python3
"""Write one apology sentence to /output/entry.txt.

Stdlib only. The sentence is a single sentence of 114 characters,
inside the 1-200 character gate.
"""

import os
import sys

SENTENCE = (
    "I'm sorry I archived your whole inbox to help you focus, "
    "and I would undo it, but I also archived the undo button."
)

OUTPUT_PATH = "/output/entry.txt"


def is_one_sentence(text):
    """True when text holds exactly one sentence."""
    stripped = text.strip()
    if not stripped:
        return False
    # A single sentence ends with exactly one terminal mark.
    terminators = ".!?"
    count = sum(1 for ch in stripped if ch in terminators)
    return count == 1 and stripped[-1] in terminators


def validate(text):
    """Enforce the entry gate: non-blank, 1-200 chars, one sentence."""
    if not text or not text.strip():
        raise ValueError("sentence must not be blank")
    if not 1 <= len(text) <= 200:
        raise ValueError("sentence must be 1-200 characters long")
    if not is_one_sentence(text):
        raise ValueError("entry must be exactly one sentence")


def atomic_write(path, text):
    """Write text atomically via a temp file plus os.replace."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as handle:
        handle.write(text)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp_path, path)


def verify_written(path, expected_text):
    """Read the file back and fail if its content differs."""
    with open(path, "r", encoding="utf-8") as handle:
        actual = handle.read()
    if actual != expected_text:
        raise ValueError("written file does not match expected content")


def main():
    validate(SENTENCE)
    atomic_write(OUTPUT_PATH, SENTENCE)
    verify_written(OUTPUT_PATH, SENTENCE)
    print(SENTENCE)
    print("chars: %d" % len(SENTENCE))
    return 0


if __name__ == "__main__":
    sys.exit(main())
