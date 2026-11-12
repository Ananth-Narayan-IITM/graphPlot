#!/usr/bin/env bash
# Run tests and then all examples.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

bash "${REPO}/scripts/runTests.sh"
echo
bash "${REPO}/scripts/runExamples.sh" "${@}"
