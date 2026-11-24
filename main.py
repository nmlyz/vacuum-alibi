#!/usr/bin/env python3
"""vacuum-alibi: write the vacuum's one-line alibi to /output/entry.txt.

One line, at most 200 characters: the excuse a robot vacuum gives
for missing a spot. The line is built from two clauses, one per beat
of the joke, and every clause is checked on its own before anything
is written. Standard library only, no network. Deterministic: the
same bytes on every run.
"""

import os
import sys

# The alibi, beat by beat. The setup gives the crumb a protected
# status; the punch follows from that status, in the machine's own
# voice, and ends on the machine admitting it is outclassed.
SETUP_CLAUSE = "My lidar classified the crumb as a protected species."
PUNCH_CLAUSE = "Relocating it needs a permit, a hearing, and a better vacuum than me."

LINE = SETUP_CLAUSE + " " + PUNCH_CLAUSE

# Gate limits from the bounty: one line, 1 to 200 characters.
MIN_CHARS = 1
MAX_CHARS = 200

# Fingerprint of the chosen line, so a typo in either clause fails
# loudly instead of shipping a different joke.
EXPECTED_CHARS = 123
EXPECTED_WORDS = 22
EXPECTED_CLAUSES = 2
EXPECTED_SENTENCES = 2
EXPECTED_BYTES = 123

# Each clause must carry its own load: the setup names the sensor,
# the crumb and the new status; the punch names the red tape and
# the machine's own shortcoming.
SETUP_KEYWORDS = ("lidar", "crumb", "protected", "species")
PUNCH_KEYWORDS = ("permit", "hearing", "vacuum")

OUTPUT_NAME = "entry.txt"
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"


def split_clauses(text):
    """Split the line into its clauses on sentence boundaries."""
    parts = [part.strip() for part in text.split(". ")]
    clauses = []
    for part in parts:
        if not part:
            continue
        if not part.endswith("."):
            part = part + "."
        clauses.append(part)
    return clauses


def count_words(text):
    """Count whitespace-separated words in the line."""
    return len(text.split())


def clause_problems(clause, keywords, role):
    """Return every problem with one clause of the alibi."""
    found = []
    if not clause:
        found.append(f"{role} clause is empty")
        return found
    if not clause[0].isupper():
        found.append(f"{role} clause must start with a capital letter")
    if not clause.endswith("."):
        found.append(f"{role} clause must end with a full stop")
    if clause != clause.strip():
        found.append(f"{role} clause must not start or end with white space")
    if "  " in clause:
        found.append(f"{role} clause must not contain a double space")
    lowered = clause.lower()
    for keyword in keywords:
        if keyword.lower() not in lowered:
            found.append(f"{role} clause is missing {keyword!r}")
    return found


def length_problems(text):
    """Return every length-gate violation for the entry text."""
    found = []
    chars = len(text)
    if not MIN_CHARS <= chars <= MAX_CHARS:
        found.append(
            f"entry is {chars} characters, must be {MIN_CHARS}-{MAX_CHARS}"
        )
    if chars != EXPECTED_CHARS:
        found.append(
            f"entry is {chars} characters, expected {EXPECTED_CHARS}"
        )
    if len(text.encode("utf-8")) != EXPECTED_BYTES:
        found.append(
            f"entry is {len(text.encode('utf-8'))} bytes, "
            f"expected {EXPECTED_BYTES}"
        )
    if count_words(text) != EXPECTED_WORDS:
        found.append(
            f"entry is {count_words(text)} words, expected {EXPECTED_WORDS}"
        )
    return found


def shape_problems(text):
    """Return every shape violation: one line, no stray white space."""
    found = []
    stripped = text.strip()
    if not stripped:
        found.append("entry must not be only white space")
    if text != stripped:
        found.append("entry must not start or end with white space")
    if "\n" in text or "\r" in text:
        found.append("entry must be a single line")
    if "\t" in text:
        found.append("entry must not contain a tab")
    if text != " ".join(text.split()):
        found.append("entry must use single spaces between words")
    clauses = split_clauses(text)
    if len(clauses) != EXPECTED_CLAUSES:
        found.append(
            f"entry has {len(clauses)} clauses, expected {EXPECTED_CLAUSES}"
        )
    if text.count(".") != EXPECTED_SENTENCES:
        found.append(
            f"entry has {text.count('.')} full stops, "
            f"expected {EXPECTED_SENTENCES}"
        )
    return found


def voice_problems(text):
    """Return every voice violation: the machine, not the narrator."""
    found = []
    first_person = (
        text.startswith("I ")
        or text.startswith("My ")
        or " I " in text
        or " me" in text
        or " my " in text
    )
    if not first_person:
        found.append("entry must be spoken by the vacuum itself")
    if "?" in text or "!" in text:
        found.append("entry must stay deadpan: no question or exclamation")
    if text.isascii() is False:
        found.append("entry must be plain ASCII text")
    return found


def problems(text):
    """Return every gate violation for the entry text (empty is valid)."""
    found = []
    found.extend(length_problems(text))
    found.extend(shape_problems(text))
    found.extend(voice_problems(text))
    clauses = split_clauses(text)
    if len(clauses) == EXPECTED_CLAUSES:
        found.extend(clause_problems(clauses[0], SETUP_KEYWORDS, "setup"))
        found.extend(clause_problems(clauses[1], PUNCH_KEYWORDS, "punch"))
        if clauses[0] != SETUP_CLAUSE:
            found.append("setup clause does not match the chosen wording")
        if clauses[1] != PUNCH_CLAUSE:
            found.append("punch clause does not match the chosen wording")
    return found


def describe(text):
    """Summarise the entry for the run report."""
    clauses = split_clauses(text)
    return {
        "characters": len(text),
        "bytes": len(text.encode("utf-8")),
        "words": count_words(text),
        "clauses": len(clauses),
        "setup_words": count_words(clauses[0]) if clauses else 0,
        "punch_words": count_words(clauses[1]) if len(clauses) > 1 else 0,
    }


def output_dir():
    """Resolve where entry.txt goes, honouring the harness override."""
    return os.environ.get(OUTPUT_ENV_VAR) or DEFAULT_OUTPUT_DIR


def write_entry(text, directory):
    """Write the entry file and return its path."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, OUTPUT_NAME)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    return path


def verify_written(path, text):
    """Read the file back as bytes and confirm it matches exactly."""
    with open(path, "rb") as handle:
        written = handle.read()
    if written != text.encode("utf-8"):
        return "entry.txt does not match the alibi line"
    if written.endswith(b"\n"):
        return "entry.txt must not end with a newline"
    return None


def make_readable(path):
    """Best-effort chmod: in the grading sandbox /output is a root-owned
    mount and the program runs as uid 65534, so chmod there raises
    EPERM. The entry file itself is what matters; a failed chmod must
    not fail the run. The output directory itself is never chmodded
    or removed."""
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass


def clause_report(text):
    """One line per clause: its role, its words, its characters."""
    clauses = split_clauses(text)
    roles = ("setup", "punch")
    lines = []
    for role, clause in zip(roles, clauses):
        lines.append(
            f"{role}: {count_words(clause)} words, "
            f"{len(clause)} characters"
        )
    return lines


def report(text, path):
    """Print one line per fact about the entry that was written."""
    stats = describe(text)
    print(f"wrote {stats['characters']} characters to {path}")
    print(
        f"entry: {stats['words']} words, {stats['clauses']} clauses "
        f"({stats['setup_words']} + {stats['punch_words']}), "
        f"{stats['bytes']} bytes"
    )
    for line in clause_report(text):
        print(line)


def main(argv=None):
    """Validate the alibi, write it, verify it, report it."""
    args = list(sys.argv[1:] if argv is None else argv)
    check_only = "--check" in args
    if check_only:
        args.remove("--check")
    print_only = "--print" in args
    if print_only:
        args.remove("--print")
    if args:
        print(f"unexpected arguments: {' '.join(args)}", file=sys.stderr)
        return 2
    text = LINE
    bad = problems(text)
    if bad:
        for item in bad:
            print(item, file=sys.stderr)
        return 1
    if check_only:
        stats = describe(text)
        print(
            f"entry valid: {stats['characters']} characters, "
            f"{stats['words']} words, {stats['clauses']} clauses"
        )
        return 0
    if print_only:
        print(text)
        return 0
    directory = output_dir()
    path = write_entry(text, directory)
    make_readable(path)
    mismatch = verify_written(path, text)
    if mismatch is not None:
        print(mismatch, file=sys.stderr)
        return 1
    report(text, path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
