#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

isort ./*.py
black  ./*.py