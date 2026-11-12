#!/usr/bin/env bash
# One-time local installation for systems where `pip install .` is blocked by
# PEP 668 (externally managed Python).
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${HOME}/.venvs/graphPlot"
BIN="${HOME}/.local/bin"

python3 -m venv "${VENV}"
"${VENV}/bin/pip" install --upgrade pip
"${VENV}/bin/pip" install "${REPO}[dev]"

mkdir -p "${BIN}"
ln -sf "${VENV}/bin/graphPlot" "${BIN}/graphPlot"
ln -sf "${VENV}/bin/graphplot" "${BIN}/graphplot"

echo "Installed graphPlot into ${VENV}"
echo "Command: ${BIN}/graphPlot"
"${BIN}/graphPlot" --version
