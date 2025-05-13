#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: version environment variable is not set." >&2
  exit 1
fi

awk -v ver="$1" '{sub(/^version = "[^"]*"$/, "version = \"" ver "\""); print}' pyproject.toml > tmp
mv tmp pyproject.toml
