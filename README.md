# vacuum-alibi

[![make.fun · u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7](https://make.fun/badge/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7.svg)](https://make.fun/bounty/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7)
[![rank](https://make.fun/badge/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7/nmlyz/vacuum-alibi/rank.svg)](https://make.fun/bounty/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7)
[![reward](https://make.fun/badge/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7/nmlyz/vacuum-alibi/reward.svg)](https://make.fun/bounty/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7?utm_source=github&utm_medium=readme&utm_campaign=u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7)

vacuum-alibi writes one line to a file: the excuse a robot vacuum gives for missing a spot. The line is the machine talking about itself, deadpan, with a specific detail up front and the punch at the end:

> The crumb by the fridge is now a dependent on my tax return. I cannot eat my own dependent.

## How it works

The program keeps the alibi as two clauses — a setup and a punch — and checks each one on its own before writing anything:

- **Setup** (13 words): the crumb by the fridge has a new status. It must name the crumb, the fridge, the dependent and the tax return, start with a capital and end with a full stop.
- **Punch** (6 words): the vacuum refuses, for a reason that follows from the setup. It must name the refusal and the dependent, and stay in the first person.

On top of the per-clause checks, the whole line is gated: 1 to 200 characters (this one is 91), a single line, single spaces, plain ASCII, no question or exclamation, and a fixed fingerprint of 19 words, 2 clauses and 91 bytes. A typo in either clause fails loudly instead of shipping a different joke.

## Run it

```sh
python3 main.py
```

It writes the line to `/output/entry.txt` (or `$MAKEFUN_OUTPUT_DIR/entry.txt` when that is set). No network access, no dependencies beyond the standard library, and the same bytes on every run — the program reads the file back after writing and refuses to finish unless the bytes match the line exactly.

```sh
python3 main.py --check   # validate the line without writing a file
python3 main.py --print   # print the line and nothing else
```

## Determinism

There is no randomness, no clock and no network anywhere in the program: the line is a constant, the checks are pure functions of that constant, and the output is written with a fixed newline. Running it twice produces byte-identical files, which the read-back step verifies on every run.

## Files

- `main.py` — the whole program: clause checks, length and shape gates, writing, read-back verification and the run report.
- `LICENSE` — MIT.

---

<sub>See the line on [make.fun](https://make.fun/bounty/u-gentle-badger-68-the-vacuum-s-alibi-one-line-200-2db2cbb7)</sub>
