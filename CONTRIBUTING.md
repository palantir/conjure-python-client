# Contributing

The team welcomes contributions!  To make code changes to one of the Conjure repos:

- Fork the repo and make a branch
- Write your code (ideally with tests) and make sure the CircleCI build passes
- Open a PR (optionally linking to a github issue)

## Local Development

### Prerequisites
- Python2 (On macOS: `brew install python3`)
- Python3 (On macOS: `brew install python`)
- [pipenv](https://github.com/pypa/pipenv) (`pip3 install pipenv`)

### One-time setup for development

1. Fork the repo
1. Create the virtual environment `PIPENV_VENV_IN_PROJECT=1 pipenv --python 3 shell`
1. Install all dependencies `pipenv install --dev`
1. Install [VSCode](https://code.visualstudio.com/)
1. From within a pipenv shell, run `code .` to open a new VSCode window.

### Development tips

- Use `python setup.py format` to quickly reformat all code using [Black](https://github.com/ambv/black)
- Use `tox` to run all tests using both python 2 and 3

