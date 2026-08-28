"""
Example 06 — Basic 1D Line Plot
===============================

Demonstrates the simplest publication-oriented line plot:

    Data1D
        ↓
    LinePlot
        ↓
    PublicationFigure
        ↓
    labels / title / legend
        ↓
    PDF + PDF_TeX export

This example intentionally uses synthetic data so that the
workflow is completely self-contained.
"""

import numpy as np

from postprocess.data.data1d import Data1D
from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)
from postprocess.plots.line import LinePlot

# =========================================================
# Data
# =========================================================

x = np.linspace(
    0.0,
    1.0,
    100,
)

y = np.sin(2.0 * np.pi * x)


data = Data1D(
    x=x,
    y=y,
    label="Numerical",
    x_label=r"$x$",
    y_label=r"$f(x)$",
    x_unit="m",
)


# =========================================================
# Figure
# =========================================================

figure_config = FigureConfig(
    width=3.4,
    height=2.8,
    dpi=600,
)

figure = PublicationFigure(figure_config)


# =========================================================
# Line plot
# =========================================================

line_plot = LinePlot()

line_plot.add(
    data,
    label="Numerical",
    role="numerical",
    color="black",
    linewidth=1.5,
    linestyle="-",
)

lines = line_plot.plot(figure.axes)

assert len(lines) == 1

# =========================================================
# Labels
# =========================================================

figure.set_labels(
    xlabel=r"$x\;(m)$",
    ylabel=r"$f(x)$",
)


# =========================================================
# Title
# =========================================================

figure.set_title(r"Basic 1D line plot")


# =========================================================
# Legend
# =========================================================

figure.axes.legend(
    frameon=False,
)


# =========================================================
# Export
# =========================================================

figure.export(
    "output/example_06_basic_line",
    formats=[
        "png",
        "pdf_tex",
    ],
)


print("Example 06 completed successfully.")
