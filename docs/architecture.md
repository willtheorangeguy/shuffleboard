# Shuffleboard — Architecture

## The two scripts

```
simulate.py        413 lines — the simulation, scoring, aiming, and batch driver
run_until_max.py   103 lines — a single game, played until it reaches 148
rules.txt          the rules being modelled
```

`run_until_max.py` reuses the simulation from `simulate.py`, so both play the same game.

## The board

A 2.0 m × 0.4 m board, simulated top-down with [pymunk](https://www.pymunk.org/) — a 2D
rigid-body engine. Gravity is irrelevant in this view; what matters is friction and damping,
which is what makes a top-down model the right choice.

Four gate arches, valued **2, 3, 4, 1** from left to right.

## A turn

Each turn slides 30 disks down the board across **up to three sub-turns**:

```
  sub-turn 1:  slide all 30 disks
                 disks through a gate  ──► scored and removed
                 disks that missed     ──► replayed next sub-turn
  sub-turn 2:  slide the remainder
  sub-turn 3:  slide what is left
```

That replay rule is why disks piling up in front of the arches matters so much — a blocked
gate does not just cost this sub-turn, it constrains the next.

## Scoring

Per the rules: **20 points for each complete set of four** — one disk in every gate — plus the
face value of every leftover disk.

The maximum is **148**, and it has exactly one solution: `[7, 7, 9, 7]`. Seven disks in each
gate makes seven complete sets, and the two remaining disks go in the value-4 gate.

## Aiming

The strategy targets whichever gate is furthest **below** that `[7, 7, 9, 7]` layout.

It is a greedy heuristic rather than a plan: it does not reason about blocking, and it does
not sacrifice a sub-turn to clear an arch. That is worth knowing when interpreting results —
the numbers describe this strategy, not optimal play. See [Roadmap](./roadmap.md).

Aim carries noise, controlled by `--aim-x-std` and `--aim-angle-std-deg`, so no two throws are
identical.

## When a turn ends

A sub-turn is over when every disk has been below `--stop-speed` for `--stable-steps`
consecutive physics steps, or when `--max-time` is reached.

Both thresholds are approximations of "the disks have stopped". Getting them wrong is the
usual cause of turns that never end or disks scored while still drifting — see
[Troubleshooting](./troubleshooting.md).

## Randomness

Launch speed and aim are both drawn from normal distributions. `--seed` fixes the stream,
which is what makes runs reproducible and comparisons meaningful.

## Why 148 is rare

All 30 disks must finish in exactly `[7, 7, 9, 7]`. Disks accumulate in front of the arches
and block them, so a single turn rarely funnels every disk through. Typical turns score
70–130.

The gap between 130 and 148 is the whole point of the simulator.
