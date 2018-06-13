#!/bin/bash

PACKAGE_VERSION=$(git describe --tags --always --first-parent)
export PACKAGE_VERSION="${PACKAGE_VERSION//-/_}"

conda-build --python 2.7 --output-folder build/conda/ conda_recipe
