# Shuffleboard — Documentation

A top-down physics simulation of sjoelen, built to answer one question: how many turns does it
actually take to reach the maximum score of 148?

```
shuffleboard/
├── docs/
│   ├── README.md          this page
│   ├── quickstart.md      run your first batch
│   ├── installation.md    dependencies
│   ├── usage.md           the two scripts and when to use each
│   ├── configuration.md   every physics and aiming flag
│   ├── architecture.md    the simulation, scoring, and aiming strategy
│   ├── faq.md             why 148 is rare, is it realistic
│   ├── troubleshooting.md slow runs, disks never settling
│   └── roadmap.md         known gaps and non-goals
├── simulate.py            batch trials, with statistics and CSV export
├── run_until_max.py       one game, played until it reaches 148
└── rules.txt              the rules of sjoelen
```

## Pages

- [Quickstart](./quickstart.md) — install and run a batch
- [Installation](./installation.md) — Python, numpy, pymunk
- [Usage](./usage.md) — `simulate.py` versus `run_until_max.py`
- [Configuration](./configuration.md) — the physics and aiming flags
- [Architecture](./architecture.md) — how a turn is simulated and scored
- [FAQ](./faq.md) — why 148 is rare, how realistic the model is
- [Troubleshooting](./troubleshooting.md) — slow runs, unstable physics
- [Roadmap](./roadmap.md) — known gaps and non-goals

## The result, up front

**148 is rare.** It requires all 30 disks to finish in exactly `[7, 7, 9, 7]` — seven disks in
every gate plus the two extras in the value-4 gate, the only distribution that yields the
maximum. Disks pile up and block the arches, so a single turn rarely funnels all 30 through.

Typical turns score in the **70–130** range. That gap is the thing the simulator exists to
measure.
