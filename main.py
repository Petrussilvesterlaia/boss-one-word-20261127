#!/usr/bin/env python3
"""One Word for the Boss -- make.fun entry.

Writes exactly one word describing a boss to /output/entry.txt.
The word is the whole entry: no spaces, no sentence, no explanation,
and no trailing newline.
"""

import hashlib
import os
import sys

WORD = "Hoverer"
OUTPUT_PATH = "/output/entry.txt"
MAX_LENGTH = 30


def validate(word):
    """Check the entry word against the competition gate."""
    if not isinstance(word, str):
        raise ValueError("entry must be a string")
    if not word:
        raise ValueError("entry must not be empty")
    if len(word) > MAX_LENGTH:
        raise ValueError("entry must be at most 30 characters")
    if word != word.strip():
        raise ValueError("entry must not start or end with whitespace")
    if not word.strip():
        raise ValueError("entry must not be only whitespace")
    if any(ch.isspace() for ch in word):
        raise ValueError("entry must be a single word with no spaces")
    if "\n" in word or "\r" in word:
        raise ValueError("entry must contain no newline")
    return True


def verify_readback(path, expected):
    """Read the file back and confirm it is byte-for-byte the word."""
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")
    if text != expected:
        raise ValueError("read-back mismatch: file does not equal the entry word")
    if raw.endswith(b"\n") or raw.endswith(b"\r"):
        raise ValueError("file must not end with a newline")
    if len(text) < 1 or len(text) > MAX_LENGTH:
        raise ValueError("file length outside the 1-30 character gate")
    if len(raw) != len(expected.encode("utf-8")):
        raise ValueError("file byte length does not match the entry word")
    if any(ch.isspace() for ch in text):
        raise ValueError("file must hold a single word with no whitespace")
    return True


def main():
    validate(WORD)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(WORD)
    verify_readback(OUTPUT_PATH, WORD)
    digest = hashlib.sha256(WORD.encode("utf-8")).hexdigest()
    print(f"Wrote {len(WORD)}-character entry to {OUTPUT_PATH}: {WORD}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
