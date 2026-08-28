"""
Example 10D — 2x2 Publication Figure
=====================================

Demonstrates a paper-oriented multi-panel figure with:

    - 2 x 2 layout
    - shared x-axis within each column
    - independent y-axes
    - multiple datasets
    - common legend
    - panel labels
"""

import numpy as np

from postprocess.data.data1d import Data1D
from postprocess.plots.line import LinePlot
from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)


# =========================================================
# Data
# =========================================================

x = np.linspace(
    0.0,
    1.0,
    200,
)


# Numerical data
temperature_num = 300.0 + 50.0 * np.sin(2.0 * np.pi * x)

pressure_num = 100.0 + 20.0 * np.cos(2.0 * np.pi * x)

velocity_num = 2.0 + 0.5 * np.sin(4.0 * np.pi * x)

residual_num = 1.0e-1 * np.exp(-5.0 * x)


# Experimental/reference data
sample = np.linspace(
    0.0,
    1.0,
    12,
)

temperature_exp = 300.0 + 50.0 * np.sin(2.0 * np.pi * sample)

pressure_exp = 100.0 + 20.0 * np.cos(2.0 * np.pi * sample)

velocity_exp = 2.0 + 0.5 * np.sin(4.0 * np.pi * sample)

residual_exp = 1.0e-1 * np.exp(-5.0 * sample)


# =========================================================
# Data containers
# =========================================================

temperature_data = Data1D(
    x=x,
    y=temperature_num,
)

temperature_reference = Data1D(
    x=sample,
    y=temperature_exp,
)


pressure_data = Data1D(
    x=x,
    y=pressure_num,
)

pressure_reference = Data1D(
    x=sample,
    y=pressure_exp,
)


velocity_data = Data1D(
    x=x,
    y=velocity_num,
)

velocity_reference = Data1D(
    x=sample,
    y=velocity_exp,
)


residual_data = Data1D(
    x=x,
    y=residual_num,
)

residual_reference = Data1D(
    x=sample,
    y=residual_exp,
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
# 2 x 2 layout
#
# Share x-axis within each column.
# =========================================================

figure.figure.clear()

axes = figure.figure.subplots(
    2,
    2,
    sharex="col",
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
    label="Numerical",
    role="numerical",
)

temperature_plot.add(
    temperature_reference,
    label="Experimental",
    role="experimental",
)

temperature_lines = temperature_plot.plot(ax1)

assert len(temperature_lines) == 2

ax1.set_ylabel(r"$T\;(\mathrm{K})$")

ax1.set_title(r"(a) Temperature")


# =========================================================
# Panel (b) — Pressure
# =========================================================

pressure_plot = LinePlot()

pressure_plot.add(
    pressure_data,
    label="Numerical",
    role="numerical",
)

pressure_plot.add(
    pressure_reference,
    label="Experimental",
    role="experimental",
)

pressure_lines = pressure_plot.plot(ax2)

assert len(pressure_lines) == 2

ax2.set_ylabel(r"$p\;(\mathrm{Pa})$")

ax2.set_title(r"(b) Pressure")


# =========================================================
# Panel (c) — Velocity
# =========================================================

velocity_plot = LinePlot()

velocity_plot.add(
    velocity_data,
    label="Numerical",
    role="numerical",
)

velocity_plot.add(
    velocity_reference,
    label="Experimental",
    role="experimental",
)

velocity_lines = velocity_plot.plot(ax3)

assert len(velocity_lines) == 2

ax3.set_xlabel(r"$x\;(\mathrm{m})$")

ax3.set_ylabel(r"$U\;(\mathrm{m/s})$")

ax3.set_title(r"(c) Velocity")


# =========================================================
# Panel (d) — Residual
# =========================================================

residual_plot = LinePlot()

residual_plot.add(
    residual_data,
    label="Numerical",
    role="numerical",
)

residual_plot.add(
    residual_reference,
    label="Experimental",
    role="experimental",
)

residual_lines = residual_plot.plot(ax4)

assert len(residual_lines) == 2

ax4.set_xlabel(r"$x\;(\mathrm{m})$")

ax4.set_ylabel(r"$R$")

ax4.set_title(r"(d) Residual")


# =========================================================
# Common legend
# =========================================================

handles, labels = ax1.get_legend_handles_labels()

figure.figure.legend(
    handles,
    labels,
    loc="lower center",
    ncol=2,
    frameon=False,
    bbox_to_anchor=(
        0.5,
        -0.01,
    ),
)


# =========================================================
# Layout
# =========================================================

figure.figure.tight_layout(
    pad=1.2,
    rect=(
        0.0,
        0.06,
        1.0,
        1.0,
    ),
)

# =========================================================
# Export
# =========================================================

figure.export(
    "output/example_10d_shared_axes_common_legend",
    formats=[
        "png",
        # "pdf_tex",
    ],
)


print("Example 10D completed successfully.")
