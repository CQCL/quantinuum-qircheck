# quantinuum-qircheck

[![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)](https://tketusers.slack.com/join/shared_invite/zt-18qmsamj9-UqQFVdkRzxnXCcKtcarLRA#)
[![Stack Exchange](https://img.shields.io/badge/StackExchange-%23ffffff.svg?style=for-the-badge&logo=StackExchange)](https://quantumcomputing.stackexchange.com/tags/pytket)

This repository contains the quantinuumqircheck package.

Some useful links:
- [API Documentation](https://tket.quantinuum.com/extensions/pytket-qir/)

## Getting started

`quantinuumqircheck` is available for Python 3.10, 3.11 and 3.12, on Linux, MacOS
and Windows. To install, run:

```shell
pip install quantinuumqircheck
```

## Bugs, support and feature requests

Please file bugs and feature requests on the Github
[issue tracker](https://github.com/CQCL/quantinuum-qircheck/issues).

There is also a Slack channel for discussion and support. Click [here](https://tketusers.slack.com/join/shared_invite/zt-18qmsamj9-UqQFVdkRzxnXCcKtcarLRA#/shared-invite/email) to join.

## Development

First setup your virtual environment (or ignore if you already have it):

```sh
python -m venv .venv
source .venv/bin/activate
```

Then install required dependencies:

```sh
pip install -U pip setuptools
pip install build pre-commit pytest wheel mypy~=1.4 black~=23.7 pylint~=2.17 ruff==0.0.282
pre-commit install
```

Then install this extension in editable mode, simply change to this directory, and run:

```shell
pip install -e .
```

You could also use `make` targets such as:

```sh
make install    # for installation
make dev        # for editable install
make lint       # run linters and formatters
make tests      # for running tests
make build      # for source and wheel distribution packages
make clean      # to clean up autogenerated files
```

## Contributing

Pull requests are welcome. To make a PR, first fork the repo, make your proposed
changes on the `main` branch, and open a PR from your fork. If it passes
tests and is accepted after review, it will be merged in.

### Code style

#### Formatting

All code should be formatted using
[black](https://black.readthedocs.io/en/stable/), with default options. This is
checked on the CI.

#### Type annotation

On the CI, [mypy](https://mypy.readthedocs.io/en/stable/) is used as a static
type checker and all submissions must pass its checks. You should therefore run
`mypy` locally on any changed files before submitting a PR. You can run the script `./mypy-check`
(passing as a single argument the root directory of the module to test).

#### Linting

We use [ruff](https://github.com/astral-sh/ruff) and [pylint](https://pypi.org/project/pylint/)
on the CI to check compliance with a set of style requirements (listed in `ruff.toml` and `.pylintrc`).
You should run `pylint` over any changed files before submitting a PR, to catch any issues.

An easy way to meet all formatting and linting requirements is to issue `pre-commit run --all-files`
or `make lint` before sending a PR.

### Tests

To run the tests:

1. `cd` into the `tests` directory;
2. ensure you have installed `pytest`, `hypothesis`, and any modules listed in
the `test-requirements.txt` file (all via `pip`);
3. run `pytest`.

When adding a new feature, please add a test for it. When fixing a bug, please
add a test that demonstrates the fix.
