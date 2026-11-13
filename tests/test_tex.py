from __future__ import annotations

import graphplot as gp


def test_tex_plain_fallback_is_derived():
    assert str(gp.tex(r"\RaE = 0")) == "RaE = 0"
    assert str(gp.tex(r"\mathbb{Nu}")) == "Nu"
    assert str(gp.tex(r"\text{Ra}_E")) == "Ra_E"
    assert str(gp.tex(r"\cite{wu2015}")) == "[wu2015]"


def test_tex_explicit_plain_fallback():
    label = gp.TeX(r"\Nu", plain="Nu")
    assert label.latex == r"\Nu"
    assert str(label) == "Nu"
    assert repr(label) == "TeX('\\\\Nu', plain='Nu')"


def test_tex_math_wrapper():
    label = gp.tex(r"\RaE = 0", plain="RaE = 0", math=True)
    assert label.latex == r"$\RaE = 0$"
    assert str(label) == "RaE = 0"
    assert gp.tex(r"$\Nu$", math=True).latex == r"$\Nu$"


def test_pdf_tex_preserves_raw_latex(tmp_path):
    a = gp.tex(r"\RaE = 0", plain="RaE = 0", math=True)
    b = gp.tex(r"\RaE = 20", plain="RaE = 20", math=True)

    fig = gp.Figure(width=3.4, height=2.6)
    fig.line([0.0, 1.0], [0.0, 1.0], label=a)
    fig.line([0.0, 1.0], [1.0, 0.0], label=b)
    fig.xlabel(gp.tex(r"\Nu", plain="Nu", math=True))
    fig.legend(
        groups=[
            {
                "title": gp.tex(r"Present work \cite{present}", "Present work"),
                "labels": [a, b],
            }
        ],
        ncol=1,
    )

    paths = fig.save(tmp_path / "rawLatex", formats=["pdf_tex"])
    content = paths["pdf_tex"].read_text(encoding="utf-8")
    assert r"$\RaE = 0$" in content
    assert r"$\RaE = 20$" in content
    assert r"$\Nu$" in content
    assert r"\cite{present}" in content
    assert r"\detokenize{rawLatex.pdf}" in content
    assert r"\textbackslash{}RaE" not in content
    fig.close()


def test_standard_legend_preserves_raw_latex(tmp_path):
    fig = gp.Figure(width=3.4, height=2.6)
    fig.line(
        [0.0, 1.0],
        [0.0, 1.0],
        label=gp.tex(r"\RaE = 0", plain="RaE = 0", math=True),
    )
    fig.legend(loc="best")
    paths = fig.save(tmp_path / "standardLegend", formats=["pdf_tex"])
    content = paths["pdf_tex"].read_text(encoding="utf-8")
    assert r"$\RaE = 0$" in content
    fig.close()
