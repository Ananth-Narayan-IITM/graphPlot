from __future__ import annotations

import numpy as np

import graphplot as gp


def test_line_from_file_and_arrays():
    fig = gp.Figure()
    fig.line("data/numerical.dat", label="Numerical", role="numerical")
    fig.line("data/experiment.dat", label="Experiment", role="experimental")
    assert len(fig.artists) == 2
    assert fig.ax.get_xlabel() == ""
    fig.close()


def test_multiple_y_columns(tmp_path):
    path = tmp_path / "multi.dat"
    path.write_text("x a b\n0 1 2\n1 2 3\n", encoding="utf-8")
    fig = gp.Figure()
    fig.line(path, y=["a", "b"])
    assert len(fig.artists) == 2
    fig.close()


def test_errorbar():
    fig = gp.Figure()
    x = np.linspace(0.0, 1.0, 5)
    fig.errorbar(x, x**2, yerr=0.05 * np.ones_like(x), label="Data")
    assert len(fig.artists) == 1
    fig.close()


def test_grouped_legend():
    fig = gp.Figure()
    x = np.linspace(0.0, 1.0, 10)
    fig.line(x, x, label="Case 1", role="numerical")
    fig.line(x, x**2, label="Case 2", role="numerical")
    fig.line(x, x + 0.1, label="Experiment 1", role="experimental")
    fig.legend(
        groups=[
            {"title": "Numerical", "labels": ["Case 1", "Case 2"]},
            {"title": "Experiment", "labels": ["Experiment 1"]},
        ],
        ncol=2,
    )
    assert fig.last_legend is not None
    assert len(fig.last_legend.legend_handles) == 5
    fig.close()


def test_twinx_and_table_legend(tmp_path):
    fig = gp.Figure(width=4.0, height=3.0)
    x = np.linspace(0.0, 1.0, 10)
    left = fig.line(x, np.sin(x), label="Case 1", color="black")
    right = fig.twinx().line(x, np.cos(x), label="Case 1", color="red")
    left.legend_table(
        {
            "Temperature": {"Case 1": left.last_artist},
            "Pressure": {"Case 1": right.last_artist},
        }
    )
    assert left.last_legend is not None
    path = tmp_path / "twinx.png"
    fig.figure.savefig(path, bbox_inches="tight", dpi=80)
    assert path.exists()
    fig.close()
