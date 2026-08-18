# Shuffleboard — Installation

## Requirements

Python 3, plus two packages:

| Package | For |
|---|---|
| [pymunk](https://www.pymunk.org/) | 2D rigid-body physics |
| [numpy](https://numpy.org/) | Numerics |

## Install

```bash
git clone https://github.com/willtheorangeguy/shuffleboard.git
cd shuffleboard
pip install -r requirements.txt
```

A virtual environment is worth using, since pymunk pulls in a compiled extension:

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Verify

```bash
python simulate.py --trials 1 --max-turns 20 --seed 1
```

One short trial. If it prints a score summary, everything is working.

## Notes

There is no packaging and no console script — both entry points are run directly with
`python`. Nothing is installed system-wide.

## Next

[Quickstart](./quickstart.md), or [Usage](./usage.md).
