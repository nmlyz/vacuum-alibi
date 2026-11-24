# vacuum-alibi

[![make.fun · u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7](https://make.fun/badge/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7.svg)](https://make.fun/bounty/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7)
[![rank](https://make.fun/badge/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7/nmlyz/vacuum-alibi/rank.svg)](https://make.fun/bounty/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7)
[![reward](https://make.fun/badge/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7/nmlyz/vacuum-alibi/reward.svg)](https://make.fun/bounty/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7)

A robot vacuum skipped a crumb on its round. It does not apologise. It files the crumb in its log as a warning to the others, and lets them draw their own conclusions. This repository is the little clerk program that types up that log line and files it.

> "I logged that crumb as a warning to the others. Let them see what happens when they settle here."

## Usage

```sh
python3 main.py
```

The excuse lands in `/output/entry.txt` as one line, 96 characters, with no trailing newline. The program also prints a short report of the checks it ran. Use `--out <path>` to file it somewhere else, or `--print-only` to see the line without writing a file.

## What the program checks

The excuse is held as two clauses, each checked on its own before the line is written:

- length within the 1–200 character limit, and exactly one line
- not blank, ends on a full stop, single spaces only
- written in the machine's own log voice, with the punch in the final clause
- no control characters, and the output bytes are the line itself — UTF-8, no trailing newline

Before writing, the line is built twice and both builds must produce identical bytes; after writing, the file is read back and compared. Run the program twice and the file comes out byte-identical.

## Requirements

Python 3.8 or newer, standard library only — nothing to install.

---

<sub>Entered on [make.fun](https://make.fun/?ref=23ae7fx0&utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7)</sub>
