# Shuffleboard — Configuration

No config file — every parameter is a command-line flag, and both scripts accept the same
physics and aiming set.

## Run control

| Flag | Script | Effect |
|---|---|---|
| `--trials` | `simulate.py` | Number of independent games |
| `--max-turns` | both | Give up after this many turns |
| `--seed` | both | Fix the random stream |
| `--verbose` | both | Per-turn and per-sub-turn detail |
| `--csv` | `simulate.py` | Write per-trial results |

## Launch and aim

| Flag | Controls |
|---|---|
| `--launch-speed-mean` | Average speed a disk is slid at |
| `--launch-speed-std` | Spread around that speed |
| `--aim-x-std` | Lateral aiming error |
| `--aim-angle-std-deg` | Angular aiming error, in degrees |

These four are the player. Setting the two standard deviations to zero models a perfect,
mechanical player; raising them models a human one. That is the most interesting axis in the
model — how much does accuracy matter to the number of turns needed?

## Surface and collisions

| Flag | Controls |
|---|---|
| `--damping` | How quickly disks lose speed to the board |
| `--disk-friction` | Disk-to-disk friction |
| `--disk-restitution` | Disk-to-disk bounciness |
| `--wall-friction` | Disk-to-wall friction |
| `--wall-restitution` | Disk-to-wall bounciness |

These are the board. `--damping` has the largest single effect: too little and disks never
settle, too much and they stop before reaching the gates.

## Solver and settling

| Flag | Controls |
|---|---|
| `--dt` | Physics timestep |
| `--max-time` | Wall-clock or simulated cap on a single sub-turn |
| `--stop-speed` | Speed below which a disk counts as stopped |
| `--stable-steps` | Consecutive steps below `--stop-speed` before a turn is considered over |

`--stop-speed` and `--stable-steps` together decide when a turn ends. Too strict and turns
drag on while disks creep; too loose and disks are scored while still moving.

`--dt` trades accuracy for speed. A smaller timestep is more faithful and proportionally
slower — relevant when running hundreds of trials.

## A caution on tuning

The defaults are chosen to produce plausible sjoelen behaviour. Changing physics parameters
changes what the simulation is a model *of*, so a configuration that reaches 148 more often is
not necessarily a better model — it may just be an easier game.

Fix `--seed` when comparing configurations, or you are comparing noise. See
[Usage](./usage.md).
