# Shuffleboard — FAQ

## Why does it so rarely reach 148?

Because 148 has exactly one solution: all 30 disks finishing as `[7, 7, 9, 7]`. Disks pile up
in front of the arches and block them, so a single turn rarely funnels every disk through.

Typical turns score 70–130. Measuring that gap is what the simulator is for, so a batch with
few successes is the result rather than a fault.

## Is the physics realistic?

It is a plausible top-down approximation, not a validated model. Disks are rigid bodies on a
frictional plane with tunable damping and restitution; there is no spin-to-surface
interaction, no board warp, and no wear.

Treat the output as "how does turn count respond to accuracy and surface" rather than as a
prediction of a real board.

## Does it play optimally?

No. The aiming strategy is greedy — it targets whichever gate is furthest below the
score-maximising layout. It does not reason about blocking and will not sacrifice a sub-turn
to clear an arch.

So results describe **this strategy**, not the best achievable play. A better strategy would
presumably reach 148 in fewer turns.

## Why two scripts?

`simulate.py` answers "how long does it usually take" across many games. `run_until_max.py`
answers "can this configuration get there at all" for one game. Same engine underneath.

## Why does my run never finish?

`run_until_max.py` defaults to unlimited turns, and 148 is rare. Always pass a finite
`--max-turns`.

## Why do two runs give different answers?

Launch speed and aim are stochastic. Pass `--seed` to fix the random stream — without it you
are comparing noise rather than configurations.

## Can I make it reach 148 more often?

Easily — reduce `--aim-x-std` and `--aim-angle-std-deg` towards zero for a mechanically
perfect player.

Worth being clear about what that means: you have changed the game being modelled, not
improved the model. See [Configuration](./configuration.md).

## What is a sub-turn?

Each turn slides all 30 disks in up to three passes. Disks that go through a gate are scored
and removed; the rest are replayed on the next sub-turn. See [Architecture](./architecture.md).

## Why are the gates valued 2, 3, 4, 1?

That is sjoelen. The full rules are in [`rules.txt`](../rules.txt).

## How do I get the raw numbers?

```bash
python simulate.py --trials 500 --max-turns 200 --seed 1 --csv results.csv
```

`simulate.py` only.
