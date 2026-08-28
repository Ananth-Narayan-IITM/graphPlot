"""
Example 09 — Grouped / Structured Legend
========================================

Demonstrates a publication-oriented grouped legend.

The figure contains:

    Experiment
        Experiment 1
        Experiment 2
        Experiment 3

    Numerical
        Case 1
        Case 2
        Case 3

The datasets are plotted on the same axes.
"""

import numpy as np

from postprocess.data.data1d import Data1D
from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)
from postprocess.plots.line import LinePlot

# =========================================================
# Independent variable
# =========================================================

x = np.linspace(
    0.0,
    1.0,
    200,
)


# =========================================================
# Experimental datasets
# =========================================================

x_exp = np.array(
    [
        0.00,
        0.10,
        0.20,
        0.30,
        0.40,
        0.50,
        0.60,
        0.70,
        0.80,
        0.90,
        1.00,
    ]
)


experiment_1 = Data1D(
    x=x_exp,
    y=(np.sin(2.0 * np.pi * x_exp) + 0.02),
)

experiment_2 = Data1D(
    x=x_exp,
    y=(np.sin(2.0 * np.pi * x_exp) - 0.015),
)

experiment_3 = Data1D(
    x=x_exp,
    y=(np.sin(2.0 * np.pi * x_exp) + 0.01),
)


# =========================================================
# Numerical datasets
# =========================================================

numerical_1 = Data1D(
    x=x,
    y=np.sin(2.0 * np.pi * x),
)

numerical_2 = Data1D(
    x=x,
    y=(np.sin(2.0 * np.pi * x) * np.exp(-0.3 * x)),
)

numerical_3 = Data1D(
    x=x,
    y=(np.sin(2.0 * np.pi * x) * np.exp(-0.6 * x)),
)


# =========================================================
# Figure
# =========================================================

figure_config = FigureConfig(
    width=3.4,
    height=3.0,
    dpi=600,
)

figure = PublicationFigure(figure_config)


# =========================================================
# Line plot
# =========================================================

line_plot = LinePlot()


# ---------------------------------------------------------
# Experimental
# ---------------------------------------------------------

line_plot.add(
    experiment_1,
    label="Experiment 1",
    role="experimental",
)

line_plot.add(
    experiment_2,
    label="Experiment 2",
    role="experimental",
)

line_plot.add(
    experiment_3,
    label="Experiment 3",
    role="experimental",
)


# ---------------------------------------------------------
# Numerical
# ---------------------------------------------------------

line_plot.add(
    numerical_1,
    label="Case 1",
    role="numerical",
)

line_plot.add(
    numerical_2,
    label="Case 2",
    role="numerical",
)

line_plot.add(
    numerical_3,
    label="Case 3",
    role="numerical",
)


# =========================================================
# Plot
# =========================================================

lines = line_plot.plot(figure.axes)

assert len(lines) == 6


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

figure.set_title(r"Grouped numerical and experimental data")


# =========================================================
# Grouped legend
# =========================================================

legend = line_plot.legend(
    figure.axes,
    location="upper right",
    frameon=False,
    fontsize=8,
    ncols=2,
    groups=[
        {
            "title": "Experiment",
            "labels": [
                "Experiment 1",
                "Experiment 2",
                "Experiment 3",
            ],
        },
        {
            "title": "Numerical",
            "labels": [
                "Case 1",
                "Case 2",
                "Case 3",
            ],
        },
    ],
)

assert legend is not None


# =========================================================
# Export
# =========================================================

figure.export(
    "output/example_09_grouped_legend",
    formats=[
        "png",
        "pdf_tex",
    ],
)


print("Example 09 completed successfully.")
