#!/usr/bin/env bash

set -e

PATH=env/bin:${PATH}

set -x

black --check date-group.py
flake8 date-group.py
isort -c date-group.py
mypy date-group.py
