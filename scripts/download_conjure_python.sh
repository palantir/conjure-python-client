#!/usr/bin/env bash

set -ex

VERSION=3.3.0
ARTIFACT_NAME="conjure-python-${VERSION}"
DOWNLOAD_OUTPUT="build/downloads/conjure-python.tgz"

mkdir -p build/downloads
curl -L "https://palantir.bintray.com/releases/com/palantir/conjure/python/conjure-python/${VERSION}/${ARTIFACT_NAME}.tgz" -o "$DOWNLOAD_OUTPUT"

tar xf "$DOWNLOAD_OUTPUT" -C build
rm -rf "build/conjure-python"
mv -f "build/$ARTIFACT_NAME" build/conjure-python
