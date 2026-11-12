from __future__ import annotations

import pytest

import graphplot as gp


def test_project_defaults_and_save(tmp_path):
    project = gp.Project(
        width=4.0,
        height=3.0,
        formats=("png",),
        output_dir=tmp_path,
        style="paper",
    )
    assert project.formats == ("png",)
    assert project.style is not None

    fig = project.figure()
    assert list(fig.figure.get_size_inches()) == [4.0, 3.0]
    paths = project.save(fig, "figure")
    assert paths["png"].exists()
    fig.close()


def test_project_figure_override():
    project = gp.Project(width=3.4, height=2.6)
    fig = project.figure(width=5.0)
    assert list(fig.figure.get_size_inches())[0] == 5.0
    fig.close()


def test_project_with_returns_copy():
    project = gp.Project(formats=["png"], output_dir="figures")
    other = project.with_(formats=("pdf_tex",))
    assert project.formats == ("png",)
    assert other.formats == ("pdf_tex",)
    assert other.output_dir.name == "figures"


def test_project_is_not_a_figure():
    with pytest.raises(AttributeError, match="project.figure"):
        gp.Project().contour("data/zNormal.vtp", "gammaDV")
