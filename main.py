#!/usr/bin/env python3
"""Write one apology sentence to /output/entry.txt.

Stdlib only. The entry is a single sentence of 114 characters, inside the
1-200 character gate for the competition.
"""

import os
import sys

SENTENCE = (
    "I'm sorry I archived your whole inbox to help you focus, "
    "and I would undo it, but I also archived the undo button."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = "/output/entry.txt"


def is_one_sentence(text):
    """True when text is exactly one sentence: one terminator, at the end."""
    stripped = text.strip()
    if not stripped:
        return False
    terminators = sum(stripped.count(mark) for mark in ".!?")
    return terminators == 1 and stripped[-1] in ".!?"


def validate(text):
    """Enforce the competition gate: non-blank, 1-200 chars, one sentence."""
    if not text or not text.strip():
        raise ValueError("sentence must not be blank")
    if not 1 <= len(text) <= 200:
        raise ValueError("sentence must be 1-200 characters, got %d" % len(text))
    if not is_one_sentence(text):
        raise ValueError("sentence must be exactly one sentence")
    return text


def main():
    sentence = validate(SENTENCE)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    tmp_path = os.path.join(OUTPUT_DIR, ".entry.txt.tmp")
    with open(tmp_path, "w", encoding="utf-8") as handle:
        handle.write(sentence)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp_path, OUTPUT_PATH)
    with open(OUTPUT_PATH, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != sentence:
        raise ValueError("read-back mismatch: entry.txt differs from sentence")
    print(sentence)
    print("chars: %d" % len(sentence))
    return 0


if __name__ == "__main__":
    sys.exit(main())
