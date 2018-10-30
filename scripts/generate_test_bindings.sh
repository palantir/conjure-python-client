#!/usr/bin/env bash

set -e

CONJURE_PYTHON="build/conjure-python/bin/conjure-python"

$CONJURE_PYTHON generate build/resources/verification-server-api.conjure.json test --packageVersion 0.0.0 --packageName generated
rm test/setup.py
