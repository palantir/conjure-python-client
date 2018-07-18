#!/usr/bin/env bash

set -e

CONJURE_PYTHON="build/conjure-python/bin/conjure-python"

$CONJURE_PYTHON generate build/resources/verification-api.conjure.json test --packageVersion 0.0.0 --packageName generated
rm test/setup.py

# HACKHACK to handle the package name change without needing the new generator
GENERATED_DIR=test/generated/conjure_verification
{
    echo "from conjure_python_client import *"
    tail -n +4 "$GENERATED_DIR/__init__.py"
} > "$GENERATED_DIR/__init__.py.tmp"
mv -f "$GENERATED_DIR/__init__.py.tmp" "$GENERATED_DIR/__init__.py"