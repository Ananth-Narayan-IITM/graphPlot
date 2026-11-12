#!/usr/bin/env bash
# Run the standalone examples (no figureSettings.py) and write to output/standalone/.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${HOME}/.venvs/graphPlot"
OUT="${REPO}/output/standalone"

clean=0
if [[ "${1:-}" == "--clean" ]]; then
    clean=1
    shift
fi

if [[ -x "${VENV}/bin/graphPlot" ]]; then
    runner=("${VENV}/bin/graphPlot")
elif command -v graphPlot >/dev/null 2>&1; then
    runner=("$(command -v graphPlot)")
else
    echo "graphPlot was not found." >&2
    echo "Run: bash ${REPO}/scripts/installLocal.sh" >&2
    exit 1
fi

mkdir -p "${OUT}"
if [[ "${clean}" -eq 1 ]]; then
    find "${OUT}" -maxdepth 1 -type f \
        \( -name '*.png' -o -name '*.pdf' -o -name '*.pdf_tex' -o -name '*.svg' \) \
        -delete
fi

cd "${REPO}"
for script in "${REPO}"/examples/standalone/*.py; do
    echo "==> $(basename "${script}")"
    "${runner[@]}" "${script}"
done

echo
echo "Standalone outputs are in:"
echo "  ${OUT}"
find "${OUT}" -maxdepth 1 -type f | sort
