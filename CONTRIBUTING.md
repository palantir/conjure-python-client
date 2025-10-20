# Contributing

The team welcomes contributions!  To make code changes to one of the Conjure repos:

- Fork the repo and make a branch
- Write your code (ideally with tests) and make sure the CircleCI build passes
- Open a PR (optionally linking to a github issue)

## Local Development

### Prerequisites
- Python3 (On macOS: `brew install python3`)
- [pipenv](https://github.com/pypa/pipenv) (`pip3 install pipenv`)

_We recommend [VSCode](https://code.visualstudio.com/) to work on python projects._

### One-time setup for development

1. Fork the repo
2. Create the virtual environment `PIPENV_VENV_IN_PROJECT=1 pipenv --python 3 shell`
3. Install all dependencies `pipenv install --dev`
4. Download and generate integration test dependencies `./scripts/prepare_integration_tests.sh`
5. From within a pipenv shell, run `code .` to open a new VSCode window.

### Development tips

- Use `python setup.py format` to quickly reformat all code using [Black](https://github.com/ambv/black)
- Run `tox` to run all unit tests, integration tests, mypy, and lint. Use `-e` for individual tasks e.g. `tox -e py3`, `tox -e lint`.
