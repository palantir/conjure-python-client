#!/bin/sh

if [ -z ${CONDA_BUILD+x} ]; then
    echo "CONDA_BUILD is unset, set this to be the path to the conda-build command before running '$(basename "$0")'"
    exit 1
fi

PACKAGE_VERSION=$(git describe --tags --always --first-parent)
export PACKAGE_VERSION="${PACKAGE_VERSION//-/_}"

$CONDA_BUILD --output-folder build/conda/ conda_recipe
