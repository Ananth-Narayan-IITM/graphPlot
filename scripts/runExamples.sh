#!/usr/bin/env bash
# Run every example and write the figures to <repo>/output/.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="${HOME}/.venvs/graphPlot"
OUT="${REPO}/output"

clean=0
if [[ "${1:-}" == "--clean" ]]; then
    clean=1
    shift
fi

if [[ ! -d "${REPO}/examples" ]]; then
    echo "No examples directory found in ${REPO}." >&2
    exit 1
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
        \( -name '*.png' -o -name '*.pdf' -o -name '*.pdf_tex' -o -name '*.svg' \
        -o -name 'latexPreview.*' \) \
        -delete
fi

cd "${REPO}"
for script in "${REPO}"/examples/*.py; do
    case "$(basename "${script}")" in
        figureSettings.py) continue ;;
    esac
    echo "==> $(basename "${script}")"
    "${runner[@]}" "${script}"
done

echo
echo "Main examples completed. Outputs are in:"
echo "  ${OUT}"
echo
find "${OUT}" -maxdepth 1 -type f | sort

echo
echo "Standalone examples"
echo "-------------------"
standalone_args=()
if [[ "${clean}" -eq 1 ]]; then
    standalone_args+=(--clean)
fi
bash "${REPO}/scripts/runStandaloneExamples.sh" "${standalone_args[@]}"
