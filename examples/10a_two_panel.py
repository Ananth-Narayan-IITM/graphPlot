"""
Example 10A — Two-Panel Publication Figure
============================================

Demonstrates how to create two independent panels
within a single publication figure.

Panel (a):
    Numerical function

Panel (b):
    Another numerical function

The two axes are independent.
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
    200,
)


y1 = np.sin(2.0 * np.pi * x)


y2 = np.cos(2.0 * np.pi * x)


data_1 = Data1D(
    x=x,
    y=y1,
    x_label=r"$x$",
    y_label=r"$f(x)$",
)


data_2 = Data1D(
    x=x,
    y=y2,
    x_label=r"$x$",
    y_label=r"$g(x)$",
)


# =========================================================
# Figure
# =========================================================

figure_config = FigureConfig(
    width=6.8,
    height=2.8,
    dpi=600,
)

figure = PublicationFigure(figure_config)

# ---------------------------------------------------------
# Create a consistent 1 × 2 layout
# ---------------------------------------------------------

figure.figure.clear()

ax1, ax2 = figure.figure.subplots(
    1,
    2,
)

figure.figure.subplots_adjust(
    wspace=0.35,
)

# =========================================================
# Panel (a)
# =========================================================

plot_1 = LinePlot()

plot_1.add(
    data_1,
    label="sin",
    role="numerical",
)

lines_1 = plot_1.plot(ax1)

assert len(lines_1) == 1


ax1.set_xlabel(r"$x$")

ax1.set_ylabel(r"$f(x)$")

ax1.set_title(r"(a) Sine function")


# =========================================================
# Panel (b)
# =========================================================

plot_2 = LinePlot()

plot_2.add(
    data_2,
    label="cos",
    role="numerical",
)

lines_2 = plot_2.plot(ax2)

assert len(lines_2) == 1


ax2.set_xlabel(r"$x$")

ax2.set_ylabel(r"$g(x)$")

ax2.set_title(r"(b) Cosine function")


# =========================================================
# Legends
# =========================================================

plot_1.legend(
    ax1,
    location="best",
    frameon=False,
)

plot_2.legend(
    ax2,
    location="best",
    frameon=False,
)


# =========================================================
# Layout
# =========================================================

figure.figure.tight_layout()


# =========================================================
# Export
# =========================================================

figure.export(
    "output/example_10a_two_panel",
    formats=[
        "png",
        # "pdf_tex",
    ],
)


print("Example 10A completed successfully.")
