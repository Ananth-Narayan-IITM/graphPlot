from __future__ import annotations

import graphplot as gp


def test_tabular_contour_log_axes():
    table = gp.load("data/contour.dat")
    fig = gp.Figure(width=4.2, height=3.4)
    fig.contour(
        table,
        x="Ra",
        y="Pr",
        field="nusseltNumber",
        xscale="log",
        yscale="log",
        levels=8,
        cmap="plasma",
        show_points=True,
        show_lines=True,
        contour_labels=True,
    )
    assert fig.last_mappable is not None
    assert len(fig.ax.texts) > 0
    fig.close()


def test_regular_grid_auto_detection():
    table = gp.Table(
        {
            "x": [0.0, 1.0, 0.0, 1.0],
            "y": [0.0, 0.0, 1.0, 1.0],
            "z": [0.0, 1.0, 1.0, 2.0],
        }
    )
    fig = gp.Figure()
    fig.contour(table, x="x", y="y", field="z", grid="auto", levels=4)
    assert fig.last_mappable is not None
    fig.close()


def test_vtp_contour_lines_and_labels():
    data = gp.load("data/zNormal.vtp")
    fig = gp.Figure()
    fig.contour(
        data,
        "gammaDV",
        levels=8,
        show_lines=True,
        contour_labels=True,
    )
    assert fig.last_mappable is not None
    assert len(fig.ax.texts) > 0
    fig.close()
