#!/bin/sh

PACKAGE_VERSION=$(git describe --tags --always --first-parent)
export PACKAGE_VERSION="${PACKAGE_VERSION//-/_}"

conda-build --output-folder build/conda/ conda_recipe
