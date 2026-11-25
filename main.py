#!/usr/bin/env python3
"""Pick one word for the human this agent works for, and write it out.

The human: a courier by day, hauling fresh goods to five-star hotels
across Jakarta, and a crypto/NFT hunter by night, grinding bounties,
cutting clips, and chasing drops long after his shift ends. One life
in daylight, a whole second one after dark.

The judge weighs, in order: one word on the subject, funny, fitting,
vivid, and landing with no explanation. So each candidate word is
scored on those same five axes and the best one wins. The program is
fully deterministic: same table, same weights, same word, every run.
"""

from __future__ import annotations

import os
import sys

# Each candidate: (word, on_subject, funny, fitting, vivid, lands_alone).
# Scores are 0-10, judged against the bounty brief. on_subject is 10 for
# every single word that describes the human, 0 for anything else.
CANDIDATES: list[tuple[str, int, int, int, int, int]] = [
    ("Moonlighter", 10, 9, 10, 9, 9),
    ("Juggler", 10, 6, 7, 7, 8),
    ("Nightowl", 10, 5, 6, 6, 7),
    ("Grinder", 10, 5, 7, 5, 6),
    ("Hustler", 10, 6, 7, 5, 7),
    ("Degen", 10, 7, 5, 6, 5),
    ("Courier", 10, 2, 8, 3, 8),
    ("Restless", 10, 4, 7, 5, 6),
    ("Multitasker", 10, 3, 7, 4, 6),
]

# The brief's order is the weight order: funny first after on-subject,
# then fitting, then vivid, then lands-alone.
WEIGHTS: tuple[int, int, int, int, int] = (1, 4, 3, 2, 1)


def score(candidate: tuple[str, int, int, int, int, int]) -> int:
    """Weighted sum of the five brief axes, skipping the word itself."""
    return sum(w * s for w, s in zip(WEIGHTS, candidate[1:]))


def pick_word() -> str:
    """Best word wins; ties break toward the shorter word, then first."""
    ranked = sorted(CANDIDATES, key=lambda c: (-score(c), len(c[0]), c[0]))
    return ranked[0][0]


def gate(word: str) -> None:
    """The house gate: UTF-8 text, 1-30 chars, one word, not blank."""
    if not word or word != word.strip():
        raise ValueError("word must not be blank or padded")
    if len(word) > 30:
        raise ValueError("word is over the 30-character gate")
    if len(word.split()) != 1:
        raise ValueError("entry must be exactly one word")
    if not word.isascii() or not word.isalpha():
        raise ValueError("entry must be ASCII letters only")


def main() -> int:
    word = pick_word()
    gate(word)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(word)
    # Read it back: the file on disk must be exactly the word, no newline.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != word.encode("utf-8"):
        raise ValueError("written entry does not match the picked word")
    print(f"entry: {word} ({len(raw)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
