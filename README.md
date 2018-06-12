# conjure-python-client

## Local development

### Dependencies

Dependencies are managed using [pipenv](https://github.com/pypa/pipenv).  Run `pip install pipenv` to add it globally. Python 2.X and 3.X are both required.  Run `brew install python3`.

1. **`PIPENV_VENV_IN_PROJECT=1 pipenv --python 3 shell`** - creates a Virtualenv `.venv` folder in the root of this repo.

1. **`pipenv install --dev`** - installs all dependencies, including those necessary to run tests.

### IDEs

[VSCode](https://code.visualstudio.com/download) is the recommended IDE.  It gives you go-to-definition, renaming, syntax-highlighting and the ability to run individual tests.

From within a pipenv shell, run `code .` to open a new VSCode window.

### Code style

Run `python setup.py format` to reformat all code using [Black](https://github.com/ambv/black).

### Tests

The `tox` command orchestrates all testing.  Tests must pass in both python 2.7 and python 3.  We also run the [`mypy` static type checker](http://mypy-lang.org/) and the [pycodestyle](https://pypi.org/project/pycodestyle/) style guide checker.

Within a pipenv shell, you can run `tox` from your terminal:

```bash
$ tox # (slow) runs all the tests

GLOB sdist-make: /Users/dfox/conjure-python-client/setup.py
py27 create: /Users/dfox/conjure-python-client/.tox/py27
py27 installdeps: pytest==3.2.5, pytest-pylint==0.9.0, pytest-html==1.16.1
py27 inst: /Users/dfox/conjure-python-client/.tox/dist/conjure-lib-1.2.3.zip
py27 installed: astroid==1.6.4,backports.functools-lru-cache==1.5,certifi==2018.4.16,chardet==3.0.4,configparser==3.5.0,conjure-lib==1.2.3,enum34==1.1.6,futures==3.2.0,idna==2.6,isort==4.3.4,lazy-object-proxy==1.3.1,mccabe==0.6.1,py==1.5.3,pylint==1.9.1,pytest==3.2.5,pytest-html==1.16.1,pytest-metadata==1.7.0,pytest-pylint==0.9.0,requests==2.18.4,singledispatch==3.4.0.3,six==1.11.0,typing==3.6.4,urllib3==1.22,wrapt==1.10.11
py27 runtests: PYTHONHASHSEED='2020466283'

...

  py27: commands succeeded
  py3: commands succeeded
  mypy27: commands succeeded
  mypy3: commands succeeded
  lint: commands succeeded
  congratulations :)
```
