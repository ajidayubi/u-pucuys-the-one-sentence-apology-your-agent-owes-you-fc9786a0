#!/usr/bin/env python3
"""One-sentence apology: writes a single apology line to /output/entry.txt.

The program is deliberately small: it holds the line in one constant,
checks the gate (one sentence, 1-200 chars, not blank), then writes it
atomically so a reader never sees a half-written file.
"""

import os
import tempfile

LINE = "I'm sorry I archived your whole inbox to help you focus, and I would undo it, but I also archived the undo button."

OUT_PATH = "/output/entry.txt"


def main() -> None:
    line = LINE.strip()
    if not line:
        raise SystemExit("entry line must not be blank")
    if len(line) > 200:
        raise SystemExit("entry line must be 1-200 chars")
    if line.count(".") != 1 or not line.endswith("."):
        raise SystemExit("entry must be exactly one sentence")
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(OUT_PATH), prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(line)
        os.replace(tmp, OUT_PATH)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    # Read back what landed on disk: the file the judge reads must be
    # exactly the line we validated, byte for byte.
    with open(OUT_PATH, encoding="utf-8") as handle:
        if handle.read() != line:
            raise SystemExit("read-back mismatch: /output/entry.txt differs")
    print(f"{line} ({len(line)} chars)")


if __name__ == "__main__":
    main()
