from __future__ import annotations

import graphplot as gp


def test_multipanel_indexing_and_labels(tmp_path):
    fig = gp.Figure(width=6.0, height=4.0, nrows=2, ncols=2)
    assert fig[0, 0] is fig.panel(0, 0)
    assert fig[1, 1].row == 1
    assert fig[1, 1].column == 1
    assert len(fig.panels_flat) == 4

    fig.label_panels()
    fig.common_labels(x="$x$", y="$y$")
    path = tmp_path / "panels.png"
    fig.figure.savefig(path, bbox_inches="tight", dpi=80)
    assert path.exists()
    fig.close()


def test_single_panel_delegation():
    fig = gp.Figure()
    assert fig.ax is fig[0, 0].ax
    assert fig.last_artist is None
    fig.xlabel("$x$", unit="m")
    assert fig.ax.get_xlabel() == "$x$ [m]"
    fig.close()


def test_save_pdf_and_pdf_tex_do_not_overwrite(tmp_path):
    fig = gp.Figure()
    fig.contour("data/zNormal.vtp", "gammaDV")
    paths = fig.save(tmp_path / "figure", formats=["pdf", "pdf_tex"])
    assert paths["pdf"].name == "figure.pdf"
    assert paths["pdf_tex_graphics"].name == "figure_tex.pdf"
    assert paths["pdf_tex"].name == "figure.pdf_tex"
    fig.close()
