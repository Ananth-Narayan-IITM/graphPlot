from __future__ import annotations

from matplotlib.collections import PolyCollection

import graphplot as gp


def test_contour_from_vtp(tmp_path):
    fig = gp.Figure(width=3.4, height=3.0)
    fig.contour("data/zNormal.vtp", "gammaDV", levels=16, cmap="viridis")
    fig.xlabel("$x$", unit="m").ylabel("$y$", unit="m")

    assert isinstance(fig.last_artist, PolyCollection)
    assert fig.last_mappable is fig.last_artist

    colorbar = fig.colorbar(label=r"$\gamma_{\mathrm{DV}}$ [1/s]")
    assert colorbar is not None

    paths = fig.save(tmp_path / "contour", formats=["png", "pdf_tex"])
    assert paths["png"].exists()
    assert paths["pdf_tex"].exists()
    fig.close()


def test_contour_field_required_with_multiple_fields():
    fig = gp.Figure()
    try:
        fig.contour("data/zNormal.vtp")
    except ValueError as exc:
        assert "field is required" in str(exc)
    else:
        raise AssertionError("Expected a ValueError")
    finally:
        fig.close()


def test_mesh_overlay(tmp_path):
    fig = gp.Figure(width=3.4, height=3.0)
    fig.contour("data/zNormal.vtp", "gammaDV")
    fig.mesh("data/zNormal.vtp", linewidth=0.1, alpha=0.2)
    assert len(fig.artists) == 2
    path = tmp_path / "mesh.png"
    fig.figure.savefig(path, bbox_inches="tight", dpi=100)
    assert path.exists()
    fig.close()
