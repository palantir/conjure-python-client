#!/usr/bin/env bash

set -e

CONJURE_PYTHON="build/conjure-python/bin/conjure-python"

$CONJURE_PYTHON generate build/resources/verification-api.conjure.json test --packageVersion 0.0.0 --packageName generated
rm test/setup.py

# HACKHACK to handle the package name change without needing the new generator
GENERATED_DIR=test/generated/conjure_verification
case $(uname -s) in
    Linux*)
        find $GENERATED_DIR -name "*.py" -type f -exec sed -i 's/from conjure/from conjure_python_client/g' {} \;
        find $GENERATED_DIR -name "*.py" -type f -exec sed -i 's/from httpremoting/from conjure_python_client/g' {} \;
    ;;
    Darwin*)
        find $GENERATED_DIR -name "*.py" -type f -exec sed -i '' 's/from conjure/from conjure_python_client/g' {} \;
        find $GENERATED_DIR -name "*.py" -type f -exec sed -i '' 's/from httpremoting/from conjure_python_client/g' {} \;
    ;;
    *) echo "Unsupported OS" >&2; exit 1;;
esac