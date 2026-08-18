# Shuffleboard — Usage

Two scripts, answering two different questions.

| Script | Question | Use when |
|---|---|---|
| `simulate.py` | How long does it *usually* take? | You want statistics across many games |
| `run_until_max.py` | Can this configuration get there at all? | You want to watch one game through |

Both share the same physics engine and the same aiming strategy, so results are comparable.

## `simulate.py` — batch trials

```bash
python simulate.py --trials 200 --max-turns 200 --seed 1
```

| Flag | Effect |
|---|---|
| `--trials` | How many independent games to play |
| `--max-turns` | Give up on a game after this many turns |
| `--seed` | Fixes the random stream, making the run reproducible |
| `--verbose` | Per-turn and per-sub-turn detail |
| `--csv results.csv` | Write per-trial results for analysis elsewhere |

`--max-turns` matters more than it looks: since 148 is rare, a game without a cap can run a
long time, and one stuck game holds up the whole batch.

## `run_until_max.py` — a single game

```bash
python run_until_max.py --seed 1 --max-turns 1000
```

Plays turn after turn until the maximum score is reached, reporting the best score so far so
you can watch progress.

**Always pass a finite `--max-turns`.** The default is unlimited.

## Reproducibility

The model is stochastic — launch speed and aim both carry noise. Without `--seed`, two runs of
the same configuration differ, so comparing parameter changes without fixing the seed compares
noise rather than the change.

Fix the seed when comparing; vary it when estimating a distribution.

## Reading the output

Both scripts report the best score observed so far. Typical turns land in the **70–130**
range; 148 requires the exact `[7, 7, 9, 7]` distribution and is uncommon.

A batch with few or no successes is a result, not a failure — see [FAQ](./faq.md).

## Tuning the physics

Every physics and aiming parameter is a flag, shared by both scripts — launch speed, aim
noise, friction, restitution, damping, timestep, and the settling thresholds. See
[Configuration](./configuration.md).
