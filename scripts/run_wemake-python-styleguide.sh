#!/bin/bash
# From https://github.com/wemake-services/wemake-python-styleguide/blob/0.18.0/scripts/entrypoint.sh

# Default values:
: "${INPUT_PATH:=$1}"

# Diagnostic output:
echo "Linting path: $INPUT_PATH"
echo 'flake8 --version:'
flake8 --version
echo '================================='
echo


output=$(flake8 $INPUT_PATH)
status="$?"


# Sets the output variable for Github Action API:
# See: https://help.github.com/en/articles/development-tools-for-github-action
echo "output=$output" >> $GITHUB_OUTPUT
echo '================================'
echo

# Fail the build in case status code is not 0:
if [ "$status" != 0 ]; then
  echo "$output"
  echo "Process failed with the status code: $status"
  exit "$status"
fi