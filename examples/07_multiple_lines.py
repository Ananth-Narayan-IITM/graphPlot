"""
Example 07 — Multiple Numerical Line Plots
===========================================

Demonstrates how to plot multiple Data1D datasets
on the same axes.

Workflow:

    Data1D × 3
        ↓
    LinePlot
        ↓
    add(...)
        ↓
    plot(...)
        ↓
    PublicationFigure
        ↓
    PDF + PDF_TeX
"""

import numpy as np

from postprocess.data.data1d import Data1D
from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)
from postprocess.plots.line import LinePlot

# =========================================================
# Create datasets
# =========================================================

x = np.linspace(
    0.0,
    1.0,
    100,
)


y1 = np.sin(2.0 * np.pi * x)

y2 = np.sin(2.0 * np.pi * x) * np.exp(-0.8 * x)

y3 = np.sin(4.0 * np.pi * x) * 0.5


data_1 = Data1D(
    x=x,
    y=y1,
    label="Case 1",
    x_label=r"$x$",
    y_label=r"$f(x)$",
    x_unit="m",
)

data_2 = Data1D(
    x=x,
    y=y2,
    label="Case 2",
    x_label=r"$x$",
    y_label=r"$f(x)$",
    x_unit="m",
)

data_3 = Data1D(
    x=x,
    y=y3,
    label="Case 3",
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
    data_1,
    label="Case 1",
    role="numerical",
)


line_plot.add(
    data_2,
    label="Case 2",
    role="numerical",
)


line_plot.add(
    data_3,
    label="Case 3",
    role="numerical",
)


# =========================================================
# Plot all datasets
# =========================================================

lines = line_plot.plot(figure.axes)

assert len(lines) == 3


# =========================================================
# Axis labels
# =========================================================

figure.set_labels(
    xlabel=r"$x\;(m)$",
    ylabel=r"$f(x)$",
)


# =========================================================
# Title
# =========================================================

figure.set_title(r"Comparison of numerical cases")


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
    "output/example_07_multiple_lines",
    formats=[
        "png",
        "pdf_tex",
    ],
)


print("Example 07 completed successfully.")
