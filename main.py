#!/usr/bin/env python3
"""vacuum-alibi -- one deadpan excuse from a robot vacuum.

A robot vacuum missed a spot. It does not apologise; it files a report.
This program assembles that report -- a single line, at most 200
characters -- checks it against every rule the bounty sets for the
output file, and writes it to /output/entry.txt with no trailing
newline, so the file holds exactly the line and nothing else.

Only the Python standard library is used. Running the program twice
produces byte-identical output: the line is fixed text, the checks
are pure functions of that text, and nothing here reads the clock,
the environment, or the network.
"""

import argparse
import hashlib
import os
import sys

# The bounty caps an entry at 200 characters and requires at least one.
LIMIT_CHARS = 200
MIN_CHARS = 1

# Where the judge looks for the entry.
DEFAULT_OUT = "/output/entry.txt"

# The excuse itself, kept as two sentences so each can be checked on
# its own before they are joined. Joined with a single space the two
# sentences come to 96 characters, inside the 200-character cap.
SENTENCES = (
    "I logged that crumb as a warning to the others.",
    "Let them see what happens when they settle here.",
)


def join_sentences(sentences):
    """Glue the sentences into the single entry line."""
    return " ".join(part.strip() for part in sentences)


def build_entry():
    """Return the entry line exactly as it must be written."""
    return join_sentences(SENTENCES)


def count_chars(text):
    """Character count the way the gate counts it: code points."""
    return len(text)


def encode_entry(text):
    """Encode the line as UTF-8 bytes, adding no trailing newline."""
    return text.encode("utf-8")


def fingerprint(data):
    """Short, stable fingerprint of the exact output bytes."""
    return hashlib.sha256(data).hexdigest()


# --- gates: each one returns (label, passed, note) -----------------------


def gate_length(text):
    n = count_chars(text)
    ok = MIN_CHARS <= n <= LIMIT_CHARS
    return ("length", ok, "%d characters (limit %d)" % (n, LIMIT_CHARS))


def gate_single_line(text):
    ok = "\n" not in text and "\r" not in text
    return ("single-line", ok, "no line breaks inside the entry")


def gate_not_blank(text):
    ok = bool(text.strip())
    return ("not-blank", ok, "the entry is not only whitespace")


def gate_terminator(text):
    ok = text.endswith(".")
    return ("terminator", ok, "the excuse ends on a full stop")


def gate_machine_voice(text):
    ok = text.startswith("I logged")
    return ("machine-voice", ok, "the machine speaks in its own log voice")


def gate_punch_at_end(text):
    ok = text.rsplit(". ", 1)[-1].startswith("Let them see")
    return ("punch-at-end", ok, "the punch sits in the final clause")


def gate_no_control_chars(text):
    bad = [ch for ch in text if ord(ch) < 0x20 or ord(ch) == 0x7F]
    ok = not bad
    return ("no-control-chars", ok, "no control characters present")


def gate_bytes_match(text, data):
    ok = data == text.encode("utf-8") and not data.endswith(b"\n")
    return ("bytes-match", ok, "output bytes are the line, no trailing newline")


GATES = (
    gate_length,
    gate_single_line,
    gate_not_blank,
    gate_terminator,
    gate_machine_voice,
    gate_punch_at_end,
    gate_no_control_chars,
)


def run_gates(text, data):
    """Run every gate; return the list of results, failures included."""
    results = [gate(text) for gate in GATES]
    results.append(gate_bytes_match(text, data))
    return results


def prove_deterministic(text):
    """Build the output twice in-process and compare fingerprints.

    The line is fixed text, so two independent builds must hash the
    same. A mismatch would mean the build depends on something it
    must not depend on, and the run fails before anything is written.
    """
    first = fingerprint(encode_entry(text))
    second = fingerprint(encode_entry(build_entry()))
    if first != second:
        raise SystemExit("determinism check failed: two builds differ")
    return first


def persist_entry(path, data):
    """Write the exact bytes to path, creating its folder if needed."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data)
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        raise SystemExit("read-back check failed: %s differs" % path)
    return written


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Write the vacuum's one-line excuse to entry.txt."
    )
    parser.add_argument(
        "--out",
        default=DEFAULT_OUT,
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


def report(results, digest, path, quiet):
    failed = [r for r in results if not r[1]]
    if not quiet:
        for label, passed, note in results:
            mark = "ok  " if passed else "FAIL"
            print("[%s] %-18s %s" % (mark, label, note))
        print("sha256: %s" % digest)
        if path:
            print("wrote:  %s" % path)
    if failed:
        names = ", ".join(label for label, _, _ in failed)
        raise SystemExit("gates failed: %s" % names)
    print("entry valid: %d characters, sha256 %s" % (
        count_chars(build_entry()), digest[:12]))
    return 0


def main(argv=None):
    args = parse_args(argv)
    text = build_entry()
    data = encode_entry(text)
    digest = prove_deterministic(text)
    results = run_gates(text, data)
    if args.print_only:
        print(text)
        return report(results, digest, None, args.quiet)
    persist_entry(args.out, data)
    return report(results, digest, args.out, args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
