# Shuffleboard — Roadmap

Known gaps, observed from the code. Limitations, not a schedule.

No entries in `docs/internal/known-issues.md` for this repository — nothing found here was a
defect. What follows are honest boundaries of the model.

## Modelling limitations

**The aiming strategy is greedy, not optimal.** It targets whichever gate is furthest below
`[7, 7, 9, 7]` and nothing more. It does not reason about blocking, does not sacrifice a
sub-turn to clear an arch, and does not adapt as disks accumulate.

So every number this produces describes *this* strategy. A smarter one would presumably reach
148 in fewer turns, and comparing strategies would be a more interesting question than
comparing physics parameters. That is the largest open direction here.

**The physics is plausible, not validated.** Rigid disks on a frictional plane with tunable
damping and restitution. No spin-to-surface interaction, no board warp, no wear, and no
calibration against a real board.

**Settling is threshold-based.** `--stop-speed` and `--stable-steps` approximate "the disks
have stopped". Both are tunable and neither is exact.

## Gaps

**No visualisation.** The simulation is headless, so a run that behaves oddly can only be
diagnosed through `--verbose` output. pymunk can draw, and a debug renderer would make
physics tuning far easier.

**No parameter sweep.** Comparing configurations means running the script repeatedly by hand
and collecting the CSVs. A sweep mode would suit the questions the project is asking.

**No tests.** The scoring rules in particular are well-specified and easily unit-tested,
independent of the physics.

**`run_until_max.py` defaults to unlimited turns**, which is a sharp edge given how rare 148
is. Documented, but a finite default would be kinder.

## Non-goals

- **Being a game.** There is no interactive play and no opponent.
- **Predicting a specific real board.** The parameters are tunable precisely because there is
  no single correct set.
