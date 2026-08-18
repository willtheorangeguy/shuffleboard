# Shuffleboard — Troubleshooting

## `run_until_max.py` never finishes

Its `--max-turns` default is unlimited, and 148 is rare. Pass a finite value:

```bash
python run_until_max.py --seed 1 --max-turns 1000
```

## A batch is extremely slow

Three levers, in order of effect:

1. **`--dt`** — a smaller timestep is more accurate and proportionally slower. Raising it is
   the biggest single speedup.
2. **`--max-turns`** — one stuck game holds up the whole batch. Cap it.
3. **`--trials`** — fewer games, obviously, though this costs statistical confidence.

## Turns never seem to end

The settling test is `--stop-speed` and `--stable-steps` together: every disk must stay below
that speed for that many consecutive steps.

If disks creep indefinitely, `--stop-speed` is too low for the damping in use. Raise it, or
raise `--damping` so disks lose energy faster. `--max-time` is the backstop that ends a
sub-turn regardless.

## Disks appear to be scored while still moving

The opposite problem — `--stop-speed` too high or `--stable-steps` too low, so a drifting disk
counts as stopped. Tighten both.

## Disks stop before reaching the gates

`--damping` too high, or `--launch-speed-mean` too low. They interact, so change one at a
time and keep `--seed` fixed.

## Scores are implausibly high or low

Check `--disk-restitution` and `--wall-restitution`. Very bouncy disks scatter unrealistically;
completely inelastic ones clump and block the arches. Both distort scoring badly.

## Two runs of the same command disagree

Expected without `--seed`. Launch speed and aim are stochastic.

## `pip install -r requirements.txt` fails on pymunk

pymunk includes a compiled extension. Use a virtual environment and make sure pip is current:

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## The results changed after I tuned the physics

They should — but note that changing physics changes what is being modelled. A configuration
that reaches 148 more often may simply be an easier game. See
[Configuration](./configuration.md).
