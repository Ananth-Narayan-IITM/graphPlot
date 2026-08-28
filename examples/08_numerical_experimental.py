"""
Example 08 — Numerical + Experimental Line Plot
================================================

Demonstrates how to compare numerical and experimental
datasets on the same axes.

Workflow:

    Data1D
       │
       ├── Numerical
       │
       └── Experimental
              ↓
          LinePlot
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
# Numerical data
# =========================================================

x_numerical = np.linspace(
    0.0,
    1.0,
    200,
)

y_numerical = np.sin(2.0 * np.pi * x_numerical)


numerical = Data1D(
    x=x_numerical,
    y=y_numerical,
    label="Numerical",
    x_label=r"$x$",
    y_label=r"$f(x)$",
    x_unit="m",
)


# =========================================================
# Experimental data
# =========================================================
#
# Experimental measurements deliberately use fewer
# and different x locations than the numerical solution.
# =========================================================

x_experimental = np.array(
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


y_experimental = np.sin(2.0 * np.pi * x_experimental) + np.array(
    [
        0.02,
        -0.015,
        0.01,
        -0.02,
        0.015,
        -0.01,
        0.02,
        -0.015,
        0.01,
        -0.02,
        0.015,
    ]
)


experimental = Data1D(
    x=x_experimental,
    y=y_experimental,
    label="Experiment",
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
    numerical,
    label="Numerical",
    role="numerical",
)


line_plot.add(
    experimental,
    label="Experiment",
    role="experimental",
)


# =========================================================
# Plot
# =========================================================

lines = line_plot.plot(figure.axes)

assert len(lines) == 2


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

figure.set_title(r"Numerical and experimental comparison")


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
    "output/example_08_numerical_experimental",
    formats=[
        "png",
        "pdf_tex",
    ],
)


print("Example 08 completed successfully.")
