#!/usr/bin/env python3
"""The Excuse That Almost Works - deterministic entry generator.

The program scores 14 hand-written one-line excuses against the judge's
brief, picks the strongest, and writes it to /output/entry.txt.

Judge's weights (most important first):
  1. On topic: a gamer texting the boss to skip work on GTA 6 launch week.
  2. Believability: a real, specific, boring workplace detail, not a wild story.
  3. Humour from the excuse's own logic or detail, not a bolted-on joke.
  4. Hurried-text tone: one line, plain words, no setup, no explanation,
     no signature.
  5. A fresh angle: not a dead grandmother, a flat tyre, or a sudden fever.

Scoring per candidate (each dimension 0-10):
  total = believability * 3 + humour * 2 + hurried + fresh_angle
"""

import os

# (text, believability, humour, hurried, fresh_angle)
CANDIDATES = [
    ("The dentist moved my filling to nine and I can't eat or talk "
     "properly till lunch.", 9, 7, 8, 7),
    ("My boiler broke and the plumber is coming between nine and twelve, "
     "I have to be in.", 8, 5, 7, 6),
    ("My prescription is only ready at ten and the pharmacy closes early "
     "today so I have to go then.", 7, 4, 6, 5),
    ("My car failed its MOT and the garage can only fit me in first thing "
     "this morning.", 9, 6, 8, 6),
    ("My phone died overnight so I'm texting from my neighbour's, I can't "
     "get in till it's charged.", 6, 9, 8, 9),
    ("My train was cancelled and the next one doesn't get in till half "
     "past ten.", 8, 3, 8, 4),
    ("The locksmith is coming to change the front door lock and I have to "
     "wait in for him.", 8, 4, 7, 6),
    ("My washing machine flooded the kitchen and I'm waiting on the "
     "emergency plumber.", 7, 6, 7, 6),
    ("The doctor moved my blood test to nine thirty and I can't eat "
     "anything till after it.", 8, 5, 7, 5),
    ("My cat knocked my laptop off the table and the screen is cracked, "
     "I need it fixed first.", 6, 7, 6, 7),
    ("The gas engineer is doing the annual safety check and the slot is "
     "eight till twelve.", 9, 3, 7, 5),
    ("My glasses broke and I can't see the screen till the optician opens "
     "at nine.", 7, 6, 7, 7),
    ("The lift in my building is stuck and the engineer says nobody can "
     "leave till it's fixed.", 5, 6, 6, 6),
    ("My landlord is showing the flat to new tenants at nine and I have "
     "to be there.", 7, 4, 6, 5),
]


def score(candidate):
    _, believability, humour, hurried, fresh_angle = candidate
    return believability * 3 + humour * 2 + hurried + fresh_angle


def pick_best(candidates):
    """Highest total wins; the earliest candidate wins an exact tie."""
    best = None
    best_score = -1
    for candidate in candidates:
        total = score(candidate)
        if total > best_score:
            best = candidate
            best_score = total
    return best, best_score


def validate(entry):
    """Gate: 1-140 characters, at most 20 words, a single line."""
    words = entry.split()
    assert entry.strip(), "entry must not be only white space"
    assert 1 <= len(entry) <= 140, "entry must be 1-140 characters"
    assert len(words) <= 20, "entry must be at most 20 words"
    assert "\n" not in entry.strip(), "entry must be a single line"
    return len(words), len(entry)


# First draft: the highest-scoring candidate, used as written.
DRAFT_ENTRY = (
    "The dentist moved my filling to nine and I can't eat or talk "
    "properly till lunch."
)

# Revised entry (second pass, after re-reading the draft against the brief):
# - "I can't eat or talk properly" -> "I can't talk right": eating is
#   irrelevant to calling in sick, and "right" is shorter and more
#   colloquial than "properly" - a hurried text does not say "properly".
# - Added a "Sorry," opener: a real text to a boss opens with an apology,
#   and it sells the hurried, real-person tone the judge weighs fourth.
# - Dropping "eat or" also cuts one word, keeping the line tight; a long
#   excuse sounds rehearsed, and a rehearsed one is already a confession.
FINAL_ENTRY = (
    "Sorry, the dentist moved my filling to nine and I can't talk "
    "right till lunch."
)


def main():
    best, best_score = pick_best(CANDIDATES)
    print("best candidate (%d points): %s" % (best_score, best[0]))
    entry = FINAL_ENTRY
    word_count, char_count = validate(entry)
    print("entry: %d words, %d characters" % (word_count, char_count))
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(entry)
    print("wrote /output/entry.txt")


if __name__ == "__main__":
    main()
