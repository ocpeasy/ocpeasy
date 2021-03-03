# OCPeasy - Command Line Interface

![](https://github.com/ocpeasy/ocpeasy/workflows/ocpeasy-ubuntu-ci/badge.svg)
[![Website shields.io](https://img.shields.io/website-up-down-green-red/https/www.ocpeasy.org)](https://www.ocpeasy.org/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPI download month](https://img.shields.io/pypi/dm/ocpeasy.svg)](https://pypi.python.org/pypi/ocpeasy/)
![](https://raw.githubusercontent.com/ocpeasy/ocpeasy/master/badges/coverage.svg)
[![PyPI license](https://img.shields.io/pypi/l/ocpeasy.svg)](https://pypi.python.org/pypi/ocpeasy/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ocpeasy.svg)](https://pypi.python.org/pypi/ocpeasy/)
[![PyPI version fury.io](https://badge.fury.io/py/ocpeasy.svg)](https://pypi.python.org/pypi/ocpeasy/)


## Introduction

OCPeasy consists in a CLI to facilitate the deployment of OpenShift applications, generating the configuration based on your project requirements.

## Pre-requisites (Development)

- Poetry is required to develop and test locally the CLI.

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

- pre-commit is required to ensure linting (with flake8) and formatting (with black) are applied before each commit

`make config_precommit`

## Get started

### Prerequisites (end user):

- `oc` corresponding to the version used by OpenShift server (https://docs.openshift.com/container-platform/4.1/release_notes/versioning-policy.html)
<!-- - `curl`
- `(Windows 10 only) WSL installed` -->

### Appendix

The default install location is `~/.poetry/bin/poetry`

I added the following to my `.zshrc`

`export PATH=$PATH:$HOME/.poetry/bin`

## Roadmap

- [x] Configuring Tests/Linting
- [x] Generate Project yaml `ocpeasy.yml`
- [x] Generate Stage folder `<rootProject>/<.ocpeasy>/<stage>/[stagesFiles].yml`
- [x] Supporting CLI invocation from `ocpeasy` directly
- [ ] Supporting environment variables
- [ ] Schema based validation
- [ ] Composing existing stages with modules (e.g.: Databases, Caches, Messaging Queue, other applications etc...)
- [ ] Support SSH Keys for cloning (read: https://stackoverflow.com/questions/28291909/gitpython-and-ssh-keys)

## Examples

### Pre-requisite

- `oc login`

### Multi-stage deployment

- `ocpeasy scaffold`
- `ocpeasy createStage` (create a new dev stage for your project)
- `ocpeasy deploy --stageId=dev`
- `ocpeasy createStage` (create a new prod stage for your project)
- `ocpeasy deploy --stageId=prod`

### Using OCPeasy behind a proxy

- `ocpeasy scaffold --proxy=http://proxy.acme-corp.net:3450`

## License

Copyright 2021 ocpeasy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
