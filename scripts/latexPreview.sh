#!/usr/bin/env bash
# Build a LaTeX document containing every output/*.pdf_tex file.
# Each figure is placed on its own page, preceded by a short description.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="${REPO}/output"
TEX="${OUT}/latexPreview.tex"
PDF="${OUT}/latexPreview.pdf"

if ! command -v pdflatex >/dev/null 2>&1; then
    echo "pdflatex was not found. Install a LaTeX distribution first." >&2
    exit 1
fi

if [[ ! -d "${OUT}" ]]; then
    echo "No output directory found. Run: bash scripts/runExamples.sh" >&2
    exit 1
fi

mapfile -t figures < <(find "${OUT}" -maxdepth 1 -type f -name '*.pdf_tex' | sort)
if [[ ${#figures[@]} -eq 0 ]]; then
    echo "No .pdf_tex files found in ${OUT}." >&2
    echo "Run: bash scripts/runExamples.sh" >&2
    exit 1
fi

description_for() {
    local name="$1"
    case "${name}" in
        *vtpContour*)
            echo "VTP contour figure. Compare the axis labels, tick labels and colorbar label with the font-size reference."
            ;;
        *linePlot*)
            echo "1D line comparison. Compare the legend entries, axis labels and tick labels with the document text."
            ;;
        *groupedLegend*)
            echo "Grouped legend figure. Check that the group headings and legend entries match the document font."
            ;;
        *dualAxis*)
            echo "Dual y-axis figure with a table-style legend. Check both y-axis labels and the legend rows."
            ;;
        *)
            echo "Generated figure. Compare all text with the reference paragraphs on the previous page."
            ;;
    esac
}

{
    cat <<'EOF'
\documentclass[10pt,a4paper]{article}
\usepackage[a4paper,margin=25mm]{geometry}
\usepackage[T1]{fontenc}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{xcolor}
\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=blue}
\pagestyle{plain}

\title{\textbf{graphPlot figure gallery}\\[0.5em]
\large PDF+TeX preview}
\author{graphPlot 2.0}
\date{\today}

\begin{document}
\maketitle
\thispagestyle{empty}

\clearpage
\section*{How to read this preview}
This document includes every \texttt{.pdf\_tex} file found in \texttt{output/}.
Each figure is placed on its own page. The PDF\_TeX files do not contain a fixed
font size: all labels, ticks, legends and math inherit the font size in effect
where the file is included.

\section*{Font-size reference}
This preview uses 10 pt body text by default. Compare the reference paragraphs
below with the text inside each figure.

\noindent{\fontsize{8}{9.6}\selectfont 8 pt: The quick brown fox jumps over the lazy dog.}\par
\vspace{0.5em}
\noindent{\fontsize{9}{10.8}\selectfont 9 pt: The quick brown fox jumps over the lazy dog.}\par
\vspace{0.5em}
\noindent{\fontsize{10}{12}\selectfont 10 pt: The quick brown fox jumps over the lazy dog.}\par
\vspace{0.5em}
\noindent{\fontsize{11}{13.2}\selectfont 11 pt: The quick brown fox jumps over the lazy dog.}\par
\vspace{1em}
\noindent Math reference: $\gamma_{\mathrm{DV}}$, $u(x)=\sin(2\pi x)$,
$\nabla\cdot\mathbf{u}=0$.

\vfill
\noindent\textit{In the paper, control the size around the include:
\texttt{\{\textbackslash small \textbackslash input\{fig.pdf\_tex\}\}} or
\texttt{\{\textbackslash fontsize\{9\}\{11\}\textbackslash selectfont
\textbackslash input\{fig.pdf\_tex\}\}}.}
\clearpage
EOF

    for file in "${figures[@]}"; do
        name="$(basename "${file}" .pdf_tex)"
        description="$(description_for "${name}")"
        cat <<EOF
\section*{\texttt{\detokenize{${name}}}}
${description}

\vspace{1em}
\begin{center}
\def\svgwidth{\columnwidth}
\input{output/${name}.pdf_tex}
\end{center}
\clearpage
EOF
    done

    echo '\end{document}'
} > "${TEX}"

cd "${REPO}"
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="${OUT}" "${TEX}" > "${OUT}/latexPreview.log"
pdflatex -interaction=nonstopmode -halt-on-error -output-directory="${OUT}" "${TEX}" >> "${OUT}/latexPreview.log"

rm -f "${OUT}/latexPreview.aux" "${OUT}/latexPreview.log" "${OUT}/latexPreview.out"

echo "LaTeX preview written to:"
echo "  ${PDF}"
echo
echo "Included figures:"
for file in "${figures[@]}"; do
    echo "  $(basename "${file}")"
done
