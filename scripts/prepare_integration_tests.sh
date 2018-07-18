#!/usr/bin/env bash

set -euo pipefail

./scripts/download_conjure_python.sh
./scripts/download_test_server.sh
./scripts/generate_test_bindings.sh
