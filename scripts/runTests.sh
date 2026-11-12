#!/usr/bin/env bash
# Run the graphPlot test suite with the persistent local installation.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${HOME}/.venvs/graphPlot"

if [[ ! -x "${VENV}/bin/python" ]]; then
    echo "graphPlot is not installed in ${VENV}." >&2
    echo "Run: bash ${REPO}/scripts/installLocal.sh" >&2
    exit 1
fi

if ! "${VENV}/bin/python" -c "import pytest" >/dev/null 2>&1; then
    echo "pytest is not installed in ${VENV}." >&2
    echo "Run: bash ${REPO}/scripts/installLocal.sh" >&2
    exit 1
fi

cd "${REPO}"
exec "${VENV}/bin/python" -m pytest "$@"
