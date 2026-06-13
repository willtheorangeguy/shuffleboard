# Shuffleboard

A physics-based simulator for the Dutch shuffleboard game *sjoelen* (a.k.a.
*sjoelbak*) that estimates how many turns it takes to reach the highest
possible score of **148**. See [`rules.txt`](rules.txt) for the full rules.

## How it works

Each turn slides 30 disks down a 2.0 m × 0.4 m board (simulated top-down with
[`pymunk`](https://www.pymunk.org/)) across up to three sub-turns. Disks that
pass through one of the four gate arches (valued 2, 3, 4, 1 from left to right)
are scored and removed; the rest are replayed on the next sub-turn. Scoring
follows the rules: 20 points per complete set of four (one disk in every gate)
plus the face value of each leftover disk.

The aiming strategy targets the gate furthest below the score-maximizing
layout of `[7, 7, 9, 7]` (seven disks in every gate plus the two extras in the
value-4 gate), which is the only distribution that yields 148.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Run a batch of trials and summarize how many turns each took to hit 148:

```bash
python simulate.py --trials 200 --max-turns 200 --seed 1
```

Run turns one after another until the maximum score is reached:

```bash
python run_until_max.py --seed 1 --max-turns 1000
```

Both scripts report the best score observed so far so you can see progress.
Pass `--verbose` for per-turn and per-sub-turn detail, and `--csv results.csv`
(simulate.py) to export per-trial results. Physics and aiming parameters
(launch speed, aim noise, friction, damping, etc.) are exposed as flags.

## A note on reaching 148

A perfect 148 requires all 30 disks to land in the exact `[7, 7, 9, 7]`
layout. Because disks pile up and block the gate, a single turn rarely funnels
all 30 through, so 148 is rare — typical turns score in the 70–130 range. Give
`run_until_max.py` a finite `--max-turns` (or be ready to stop it) rather than
relying on the unlimited default.
