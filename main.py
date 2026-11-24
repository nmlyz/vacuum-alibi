#!/usr/bin/env python3
"""vacuum-alibi: the vacuum files its excuse instead of saying sorry.

A robot vacuum skipped a crumb on its round. Rather than apologise,
it logs the crumb as a warning to every crumb that might settle there
next. This script is the clerk that types up that log line: it puts
the excuse together, puts it through its paces, and files it in
/output/entry.txt as exactly one line, with nothing after it -- not
even a newline.

Everything here is plain standard library, and the result never
changes between runs: the wording is fixed, the checks only look at
the wording, and the script never consults the clock, the network,
or the environment.
"""

import argparse
import hashlib
import sys
from pathlib import Path

# The bounty allows a single line of 1 to 200 characters.
CHAR_CAP = 200
CHAR_FLOOR = 1

# The judge reads the entry from here unless told otherwise.
DEFAULT_TARGET = "/output/entry.txt"

# The excuse, in two clauses. Each clause is checked on its own, then
# the two are set side by side with one space between them. Together
# they run to 96 characters, comfortably inside the 200-character cap.
CLAUSES = [
    "I logged that crumb as a warning to the others.",
    "Let them see what happens when they settle here.",
]


class Excuse:
    """One excuse line, from its clauses to the bytes on disk."""

    def __init__(self, clauses):
        self.clauses = [clause.strip() for clause in clauses]

    @property
    def line(self):
        """The two clauses joined with a single space."""
        return " ".join(self.clauses)

    @property
    def payload(self):
        """The line as UTF-8 bytes, with no trailing newline added."""
        return self.line.encode("utf-8")

    @property
    def digest(self):
        """Short stable fingerprint of the exact output bytes."""
        return hashlib.sha256(self.payload).hexdigest()

    def rebuild(self):
        """A second, independent build for the determinism proof."""
        return Excuse(list(self.clauses))


# --- checks: each takes an Excuse and returns (label, passed, note) ---


def check_length(excuse):
    n = len(excuse.line)
    ok = CHAR_FLOOR <= n <= CHAR_CAP
    return ("length", ok, "%d characters (cap %d)" % (n, CHAR_CAP))


def check_one_line(excuse):
    ok = "\n" not in excuse.line and "\r" not in excuse.line
    return ("one-line", ok, "no line breaks inside the entry")


def check_not_empty(excuse):
    ok = bool(excuse.line.strip())
    return ("not-empty", ok, "the entry is not only whitespace")


def check_full_stop(excuse):
    ok = excuse.line.endswith(".")
    return ("full-stop", ok, "the excuse ends on a full stop")


def check_log_voice(excuse):
    ok = excuse.line.startswith("I logged")
    return ("log-voice", ok, "the machine speaks in its own log voice")


def check_punch_last(excuse):
    ok = excuse.clauses[-1].startswith("Let them see")
    return ("punch-last", ok, "the punch sits in the final clause")


def check_no_controls(excuse):
    bad = [ch for ch in excuse.line if ord(ch) < 0x20 or ord(ch) == 0x7F]
    ok = not bad
    return ("no-controls", ok, "no control characters present")


def check_spacing(excuse):
    ok = "  " not in excuse.line
    return ("spacing", ok, "single spaces only between words")


def check_payload(excuse):
    ok = excuse.payload == excuse.line.encode("utf-8")
    ok = ok and not excuse.payload.endswith(b"\n")
    return ("payload", ok, "output bytes are the line, no trailing newline")


CHECKS = (
    check_length,
    check_one_line,
    check_not_empty,
    check_full_stop,
    check_log_voice,
    check_punch_last,
    check_no_controls,
    check_spacing,
    check_payload,
)


def run_checks(excuse):
    """Run every check; failures are reported, not hidden."""
    return [check(excuse) for check in CHECKS]


def prove_stable(excuse):
    """Build the entry twice and demand identical bytes.

    The wording is fixed, so two independent builds must hash the
    same. A mismatch would mean the build depends on something it
    must not depend on, and the run stops before anything is written.
    """
    again = excuse.rebuild()
    if again.payload != excuse.payload or again.digest != excuse.digest:
        raise SystemExit("determinism check failed: two builds differ")
    return excuse.digest


def file_entry(target, excuse):
    """Write the exact bytes, then read them back and compare."""
    path = Path(target)
    if path.parent != Path("."):
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(excuse.payload)
    written = path.read_bytes()
    if written != excuse.payload:
        raise SystemExit("read-back check failed: %s differs" % target)
    return written


def parse_cli(argv):
    parser = argparse.ArgumentParser(
        description="File the vacuum's one-line excuse as entry.txt."
    )
    parser.add_argument(
        "--out",
        default=DEFAULT_TARGET,
        help="destination file (default: %(default)s)",
    )
    parser.add_argument(
        "--print-only",
        action="store_true",
        help="print the line instead of writing a file",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="only print failures and the final summary line",
    )
    return parser.parse_args(argv)


def summarise(results, digest, excuse, target, quiet):
    failed = [r for r in results if not r[1]]
    if not quiet:
        for label, passed, note in results:
            mark = "ok  " if passed else "FAIL"
            print("[%s] %-14s %s" % (mark, label, note))
        print("sha256: %s" % digest)
        if target:
            print("wrote:  %s" % target)
    if failed:
        names = ", ".join(label for label, _, _ in failed)
        raise SystemExit("checks failed: %s" % names)
    print("entry valid: %d characters, sha256 %s" % (
        len(excuse.line), digest[:12]))
    return 0


def main(argv=None):
    args = parse_cli(argv)
    excuse = Excuse(CLAUSES)
    digest = prove_stable(excuse)
    results = run_checks(excuse)
    if args.print_only:
        print(excuse.line)
        return summarise(results, digest, excuse, None, args.quiet)
    file_entry(args.out, excuse)
    return summarise(results, digest, excuse, args.out, args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
