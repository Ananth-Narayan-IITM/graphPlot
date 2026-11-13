from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import matplotlib.image as mpimg
import numpy as np
import pytest

import graphplot as gp

DATA = Path(__file__).resolve().parents[1] / "data" / "zNormal.vtp"


@pytest.mark.skipif(
    shutil.which("pdflatex") is None, reason="pdflatex is not installed"
)
def test_pdf_tex_compiles(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    fig = gp.Figure(width=3.4, height=3.0)
    fig.contour(DATA, "gammaDV", levels=12)
    fig.xlabel("$x$", unit="m").ylabel("$y$", unit="m")
    fig.colorbar(label=r"$\gamma_{\mathrm{DV}}$")

    paths = fig.save("figure", formats=["pdf_tex"])
    tex = paths["pdf_tex"]
    assert tex.exists()
    content = tex.read_text(encoding="utf-8")
    assert r"\begin{picture}" in content
    assert r"\put(" in content
    assert "gammaDV" not in content or "$" in content
    assert r"\fontsize" not in content

    sized = fig.save(
        "figure_sized",
        formats=["pdf_tex"],
        pdf_tex_text_size="figure",
    )
    assert r"\fontsize" in sized["pdf_tex"].read_text(encoding="utf-8")

    document = tmp_path / "document.tex"
    document.write_text(
        "\\documentclass{article}\n"
        "\\usepackage{graphicx}\n"
        "\\usepackage{amsmath}\n"
        "\\usepackage{xcolor}\n"
        "\\begin{document}\n"
        "\\begin{figure}[h]\\centering\n"
        "\\def\\svgwidth{0.9\\columnwidth}\n"
        "\\input{figure.pdf_tex}\n"
        "\\end{figure}\n"
        "\\end{document}\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", str(document)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert (tmp_path / "document.pdf").exists()

    if shutil.which("pdftoppm") is not None:
        render = subprocess.run(
            [
                "pdftoppm",
                "-r",
                "60",
                "-png",
                "-f",
                "1",
                "-l",
                "1",
                "document.pdf",
                "render",
            ],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )
        assert render.returncode == 0, render.stderr
        image = mpimg.imread(tmp_path / "render-1.png")
        assert np.nanmin(image) < 0.99
        assert np.nanstd(image) > 0.005

    fig.close()


@pytest.mark.skipif(
    shutil.which("pdflatex") is None, reason="pdflatex is not installed"
)
def test_pdf_tex_raw_latex_macros_and_citation(tmp_path):
    fig = gp.Figure(width=3.4, height=2.6)
    fig.line(
        [0.0, 1.0],
        [0.0, 1.0],
        label=gp.tex(r"\RaE = 0", plain="RaE = 0", math=True),
    )
    fig.line(
        [0.0, 1.0],
        [1.0, 0.0],
        label=gp.tex(r"\RaE = 20", plain="RaE = 20", math=True),
    )
    fig.xlabel(gp.tex(r"\Nu", plain="Nu", math=True))
    fig.legend(
        groups=[
            {
                "title": gp.tex(r"Present \cite{present}", "Present [present]"),
                "labels": [
                    gp.tex(r"\RaE = 0", plain="RaE = 0", math=True),
                    gp.tex(r"\RaE = 20", plain="RaE = 20", math=True),
                ],
            }
        ],
        ncol=1,
    )
    paths = fig.save(tmp_path / "figure", formats=["pdf_tex"])
    content = paths["pdf_tex"].read_text(encoding="utf-8")
    assert r"$\RaE = 0$" in content
    assert r"\cite{present}" in content
    assert r"$\Nu$" in content

    document = tmp_path / "document.tex"
    document.write_text(
        "\\documentclass{article}\n"
        "\\usepackage{graphicx}\n"
        "\\usepackage{amsmath,amssymb}\n"
        "\\usepackage{xcolor}\n"
        "\\newcommand{\\Nu}{\\mathbb{Nu}}\n"
        "\\newcommand{\\RaE}{\\text{Ra}_E}\n"
        "\\begin{document}\n"
        "\\begin{figure}[h]\\centering\n"
        "\\def\\svgwidth{0.9\\columnwidth}\n"
        "\\input{figure.pdf_tex}\n"
        "\\end{figure}\n"
        "\\begin{thebibliography}{9}\n"
        "\\bibitem{present} Present work.\n"
        "\\end{thebibliography}\n"
        "\\end{document}\n",
        encoding="utf-8",
    )
    for _ in range(2):
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", str(document)],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stdout + result.stderr
    assert r"\bibcite{present}{1}" in (tmp_path / "document.aux").read_text(
        encoding="utf-8"
    )
    fig.close()
