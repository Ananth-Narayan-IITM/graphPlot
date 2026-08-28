"""
Example 10B — Two-Panel Figure with Shared X-Axis
==================================================

Demonstrates:

    - vertically stacked panels
    - shared x-axis
    - independent y-axis quantities
    - publication-oriented formatting

Panel (a):
    Temperature-like quantity

Panel (b):
    Pressure-like quantity
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


temperature = 300.0 + 50.0 * np.sin(2.0 * np.pi * x)


pressure = 100.0 + 20.0 * np.cos(2.0 * np.pi * x)


temperature_data = Data1D(
    x=x,
    y=temperature,
    x_label=r"$x$",
    y_label=r"$T$",
)


pressure_data = Data1D(
    x=x,
    y=pressure,
    x_label=r"$x$",
    y_label=r"$p$",
)


# =========================================================
# Figure
# =========================================================

figure_config = FigureConfig(
    width=3.4,
    height=5.2,
    dpi=600,
)

figure = PublicationFigure(figure_config)


# =========================================================
# Create shared-x layout
# =========================================================

figure.figure.clear()

ax1, ax2 = figure.figure.subplots(
    2,
    1,
    sharex=True,
)


# =========================================================
# Panel (a) — Temperature
# =========================================================

temperature_plot = LinePlot()

temperature_plot.add(
    temperature_data,
    label="Temperature",
    role="numerical",
)

temperature_lines = temperature_plot.plot(ax1)

assert len(temperature_lines) == 1


ax1.set_ylabel(r"$T\;(\mathrm{K})$")

ax1.set_title(r"(a) Temperature distribution")

temperature_plot.legend(
    ax1,
    location="best",
    frameon=False,
)


# =========================================================
# Panel (b) — Pressure
# =========================================================

pressure_plot = LinePlot()

pressure_plot.add(
    pressure_data,
    label="Pressure",
    role="numerical",
)

pressure_lines = pressure_plot.plot(ax2)

assert len(pressure_lines) == 1


ax2.set_ylabel(r"$p\;(\mathrm{Pa})$")

ax2.set_xlabel(r"$x\;(\mathrm{m})$")

ax2.set_title(r"(b) Pressure distribution")

pressure_plot.legend(
    ax2,
    location="best",
    frameon=False,
)


# =========================================================
# Layout
# =========================================================

figure.figure.tight_layout(
    pad=1.2,
)


# =========================================================
# Export
# =========================================================

figure.export(
    "output/example_10b_shared_x",
    formats=[
        "png",
        # "pdf_tex",
    ],
)


print("Example 10B completed successfully.")
