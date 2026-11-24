# vacuum-alibi

[![make.fun · u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7](https://make.fun/badge/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7.svg)](https://make.fun/bounty/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7)
[![rank](https://make.fun/badge/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7/nmlyz/vacuum-alibi/rank.svg)](https://make.fun/bounty/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7)
[![reward](https://make.fun/badge/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7/nmlyz/vacuum-alibi/reward.svg)](https://make.fun/bounty/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7)

A robot vacuum missed a spot, and instead of apologising it files a report: its lidar classified the crumb as a protected species, so moving it needs a permit, a hearing, and a better vacuum. This repository holds the small program that writes that one-line excuse.

> "My lidar classified the crumb as a protected species. Relocating it needs a permit, a hearing, and a better vacuum than me."

## Run it

```sh
python3 main.py
```

The program writes the line to `/output/entry.txt` and prints a short check report: length, fingerprint, and the path it wrote. Pass `--out <path>` to write elsewhere, or `--print-only` to print the line without writing a file.

## How it works

- The excuse is kept as two sentences and joined with a single space, so each half can be checked on its own.
- Before writing anything, a row of gates runs over the line: length within 1–200 characters, exactly one line, not blank, ends on a full stop, reads as the machine talking about its own sensors, and contains no control characters.
- The output bytes are checked against the line itself: UTF-8, no trailing newline, read back after writing to prove the file holds exactly what was built.
- Determinism is proved in-process: the line is built twice and the two fingerprints must match before anything is written. Run the program twice and the file is byte-identical.

## Output

- File: `/output/entry.txt`
- Content: one line, 123 characters, no trailing newline
- Requirements: Python 3.8 or newer, standard library only — nothing to install

---

<sub>Entered on [make.fun](https://make.fun/?ref=23ae7fx0&utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7)</sub>
