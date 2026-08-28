"""
Example 10C — Four-Panel Publication Figure
=============================================

Demonstrates how to create a 2 x 2 publication figure.

Panels:

    (a) Temperature
    (b) Pressure
    (c) Velocity
    (d) Residual

All four panels are independent axes.
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


velocity = 2.0 + 0.5 * np.sin(4.0 * np.pi * x)


residual = 1.0e-1 * np.exp(-5.0 * x)


temperature_data = Data1D(
    x=x,
    y=temperature,
)


pressure_data = Data1D(
    x=x,
    y=pressure,
)


velocity_data = Data1D(
    x=x,
    y=velocity,
)


residual_data = Data1D(
    x=x,
    y=residual,
)


# =========================================================
# Figure
# =========================================================

figure_config = FigureConfig(
    width=6.8,
    height=5.6,
    dpi=600,
)

figure = PublicationFigure(figure_config)


# =========================================================
# Create 2 x 2 layout
# =========================================================

figure.figure.clear()

axes = figure.figure.subplots(
    2,
    2,
)

ax1 = axes[0, 0]
ax2 = axes[0, 1]
ax3 = axes[1, 0]
ax4 = axes[1, 1]


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

ax1.set_xlabel(r"$x\;(\mathrm{m})$")

ax1.set_ylabel(r"$T\;(\mathrm{K})$")

ax1.set_title(r"(a) Temperature")

temperature_plot.legend(
    ax1,
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

ax2.set_xlabel(r"$x\;(\mathrm{m})$")

ax2.set_ylabel(r"$p\;(\mathrm{Pa})$")

ax2.set_title(r"(b) Pressure")

pressure_plot.legend(
    ax2,
    frameon=False,
    location="upper right",
)


# =========================================================
# Panel (c) — Velocity
# =========================================================

velocity_plot = LinePlot()

velocity_plot.add(
    velocity_data,
    label="Velocity",
    role="numerical",
)

velocity_lines = velocity_plot.plot(ax3)

assert len(velocity_lines) == 1

ax3.set_xlabel(r"$x\;(\mathrm{m})$")

ax3.set_ylabel(r"$U\;(\mathrm{m/s})$")

ax3.set_title(r"(c) Velocity")

velocity_plot.legend(
    ax3,
    frameon=False,
    location="upper right",
)


# =========================================================
# Panel (d) — Residual
# =========================================================

residual_plot = LinePlot()

residual_plot.add(
    residual_data,
    label="Residual",
    role="numerical",
)

residual_lines = residual_plot.plot(ax4)

assert len(residual_lines) == 1

ax4.set_xlabel(r"$x\;(\mathrm{m})$")

ax4.set_ylabel(r"$R$")

ax4.set_title(r"(d) Residual")

residual_plot.legend(
    ax4,
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
    "output/example_10c_four_panel",
    formats=[
        "png",
        # "pdf_tex",
    ],
)


print("Example 10C completed successfully.")
