# CLAUDE.md

## Project Overview

Shuffleboard is a Python physics simulator for the Dutch shuffleboard game "sjoelen" (sjoelbak). It uses pymunk (2D physics engine) to estimate how many turns it takes to achieve the maximum score of 148 points.

## Repository Structure

```
simulate.py       # Core simulator — physics, scoring, aiming strategy, CLI
run_until_max.py  # Runs turns sequentially until max score (148) is reached
requirements.txt  # Dependencies: numpy, pymunk
rules.txt         # Complete sjoelbak game rules reference
```

## Setup

```bash
pip install -r requirements.txt
```

## Running

```bash
# Run batch trials (default: 10,000 trials of 50 turns each)
python simulate.py

# Run until max score achieved
python run_until_max.py
```

Both scripts accept extensive CLI flags for tuning physics parameters (launch speed, aim precision, friction, elasticity, damping, timestep, etc.). Use `--help` for details.

## Key Concepts

- **Scoring**: 4 gates worth 2, 3, 4, 1 points. Complete sets (one disk in each gate) score 20 points. Max score is 148 with 30 disks.
- **Ideal distribution**: `[7, 7, 9, 7]` disks across gates maximizes score.
- **Aiming strategy**: Deficit-based — targets the gate furthest below its ideal count, breaking ties toward higher-value gates.
- **SimConfig dataclass**: Central configuration for all physics/simulation parameters in `simulate.py`.

## Code Conventions

- Python 3 with type hints on function signatures and dataclasses
- PEP 8 style, 4-space indentation
- No test suite, linter, or CI configured
- No build system — pure Python scripts

## Architecture Notes

- `build_space()` creates the pymunk physics world (board walls + gate openings)
- `step_until_stable()` runs physics simulation with collision detection
- `simulate_subturn()` → `simulate_turn()` → `run_trials()` is the execution hierarchy
- `summarize_results()` computes statistics; `write_csv()` exports data
