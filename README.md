<!-- Logo -->
<h1 align="center">Shuffleboard</h1>

<!-- Copy -->
<h4 align="center">A physics simulator for the Dutch shuffleboard game <em>sjoelen</em>, estimating how many turns it takes to reach a perfect 148.</h4>

<!-- Badges -->
<div align="center">
  <img alt="GitHub Issues" src="https://img.shields.io/github/issues/willtheorangeguy/shuffleboard">
  <img alt="GitHub Pull Requests" src="https://img.shields.io/github/issues-pr/willtheorangeguy/shuffleboard">
  <img alt="License" src="https://img.shields.io/github/license/willtheorangeguy/shuffleboard">
  <img alt="Python" src="https://img.shields.io/badge/python-3-blue">
</div>

<!-- Navigation -->
<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#support">Support</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

## Key Features

- Top-down rigid-body simulation of a 2.0 m × 0.4 m board with 30 disks, using pymunk.
- Full sjoelen scoring — 20 points per complete set of four, plus face values for the rest.
- An aiming strategy that targets whichever gate is furthest below the score-maximising layout.
- Batch mode for statistics across many trials, and single-run mode to watch one game reach 148.
- Every physics and aiming parameter exposed as a command-line flag.
- CSV export of per-trial results.

## Installation

```bash
pip install -r requirements.txt
```

Needs Python 3, [numpy](https://numpy.org/), and [pymunk](https://www.pymunk.org/). See [`docs/installation.md`](docs/installation.md).

## Usage

```bash
python simulate.py --trials 200 --max-turns 200 --seed 1
```

Summarises how many turns each trial took to hit 148. See [`docs/usage.md`](docs/usage.md).

## Documentation

Full documentation lives in [`docs/`](docs/README.md):
[Quickstart](docs/quickstart.md) · [Installation](docs/installation.md) · [Usage](docs/usage.md) · [Configuration](docs/configuration.md) · [Architecture](docs/architecture.md) · [FAQ](docs/faq.md) · [Troubleshooting](docs/troubleshooting.md) · [Roadmap](docs/roadmap.md)

The game's rules are in [`rules.txt`](rules.txt).

## Support

Open a [GitHub Discussion](https://github.com/willtheorangeguy/shuffleboard/discussions/new) or file an [issue](https://github.com/willtheorangeguy/shuffleboard/issues/new/choose).

## Contributing

Contributions welcome. See the org-wide [Contributing Guide](https://github.com/willtheorangeguy/.github/blob/main/CONTRIBUTING.md) and [Code of Conduct](https://github.com/willtheorangeguy/.github/blob/main/CODE_OF_CONDUCT.md).

## Credits

Physics by [pymunk](https://www.pymunk.org/), numerics by [numpy](https://numpy.org/).

## License

MIT — see [`LICENSE.md`](LICENSE.md).
