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
