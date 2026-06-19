#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

ruff format aiowiserbyfeller tests
ruff check aiowiserbyfeller tests --fix
