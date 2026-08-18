# Shuffleboard — Quickstart

## 1. Install

```bash
pip install -r requirements.txt
```

numpy and pymunk. Nothing else.

## 2. Run a batch

```bash
python simulate.py --trials 200 --max-turns 200 --seed 1
```

Plays 200 independent games, each capped at 200 turns, and summarises how many turns each took
to reach 148.

`--seed` makes the run reproducible, which matters here — the whole model is stochastic, so
comparing two parameter sets without a fixed seed compares noise.

## 3. Watch a single game

```bash
python run_until_max.py --seed 1 --max-turns 1000
```

Plays turn after turn until the maximum score is reached, reporting the best score so far.

**Always pass a finite `--max-turns`.** The default is unlimited, and since 148 is rare a run
can continue for a very long time.

## 4. See more detail

```bash
python simulate.py --trials 20 --max-turns 200 --seed 1 --verbose
```

`--verbose` reports per-turn and per-sub-turn detail rather than just the summary.

## 5. Export the numbers

```bash
python simulate.py --trials 500 --max-turns 200 --seed 1 --csv results.csv
```

Per-trial results, for analysing elsewhere. `simulate.py` only.

## What to expect

Typical turns score **70–130**. Reaching 148 needs all 30 disks in exactly `[7, 7, 9, 7]`, and
disks blocking the arches make that uncommon — so a batch of 200 trials may contain few
successes, which is the finding rather than a fault.

## Then what

- [Usage](./usage.md) — which script to use when
- [Configuration](./configuration.md) — tuning the physics
- [Architecture](./architecture.md) — how a turn is actually simulated
