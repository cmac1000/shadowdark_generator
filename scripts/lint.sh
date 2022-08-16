#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

./scripts/format.sh
mypy ./*.py
pylint ./*.py