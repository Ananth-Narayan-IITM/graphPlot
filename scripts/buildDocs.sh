#!/usr/bin/env bash
# Build the Doxygen API documentation.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v doxygen >/dev/null 2>&1; then
    echo "doxygen was not found. Install Doxygen first." >&2
    exit 1
fi

cd "${REPO}"
doxygen Doxyfile

echo "API documentation written to:"
echo "  ${REPO}/docs/html/index.html"
