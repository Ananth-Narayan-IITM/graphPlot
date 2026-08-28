"""
Example 11B — Multiple Datasets with Dual Y-Axes
=================================================

Demonstrates:

    - multiple datasets on the left Y-axis
    - multiple datasets on the right Y-axis
    - common X-axis
    - common legend

Left Y-axis:
    Temperature cases

Right Y-axis:
    Pressure cases
"""

import numpy as np

from postprocess.data.data1d import Data1D
from postprocess.plots.line import LinePlot
from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)
from matplotlib.lines import Line2D


# =========================================================
# Data
# =========================================================

x = np.linspace(
    0.0,
    1.0,
    200,
)


# ---------------------------------------------------------
# Left-axis quantities
# ---------------------------------------------------------

temperature_1 = 300.0 + 50.0 * np.sin(2.0 * np.pi * x)

temperature_2 = 310.0 + 40.0 * np.sin(2.0 * np.pi * x + 0.2)


# ---------------------------------------------------------
# Right-axis quantities
# ---------------------------------------------------------

pressure_1 = 100.0 + 20.0 * np.cos(2.0 * np.pi * x)

pressure_2 = 110.0 + 15.0 * np.cos(2.0 * np.pi * x + 0.3)


# =========================================================
# Data containers
# =========================================================

temperature_data_1 = Data1D(
    x=x,
    y=temperature_1,
)

temperature_data_2 = Data1D(
    x=x,
    y=temperature_2,
)

pressure_data_1 = Data1D(
    x=x,
    y=pressure_1,
)

pressure_data_2 = Data1D(
    x=x,
    y=pressure_2,
)


# =========================================================
# Figure
# =========================================================

figure_config = FigureConfig(
    width=3.4,
    height=3.2,
    dpi=600,
)

figure = PublicationFigure(figure_config)


# =========================================================
# Primary / left axis
# =========================================================

ax_left = figure.axes


left_plot = LinePlot()


left_plot.add(
    temperature_data_1,
    label="Temperature — Case 1",
    role="numerical",
)


left_plot.add(
    temperature_data_2,
    label="Temperature — Case 2",
    role="experimental",
)


left_lines = left_plot.plot(ax_left)


assert len(left_lines) == 2


ax_left.set_xlabel(r"$x\;(\mathrm{m})$")

ax_left.set_ylabel(r"$T\;(\mathrm{K})$")

ax_left.set_title(r"Multiple datasets with dual Y-axes")


# =========================================================
# Secondary / right axis
# =========================================================

ax_right = ax_left.twinx()


right_plot = LinePlot()


right_plot.add(
    pressure_data_1,
    label="Pressure — Case 1",
    role="numerical",
)


right_plot.add(
    pressure_data_2,
    label="Pressure — Case 2",
    role="experimental",
)


right_lines = right_plot.plot(ax_right)


assert len(right_lines) == 2


ax_right.set_ylabel(r"$p\;(\mathrm{Pa})$")


# =========================================================
# Common legend
# =========================================================

# =========================================================
# Grouped / table legend
# =========================================================

groups = {
    "Temperature": {
        "Case 1": left_lines[0],
        "Case 2": left_lines[1],
    },
    "Pressure": {
        "Case 1": right_lines[0],
        "Case 2": right_lines[1],
    },
}


legend = left_plot.legend_table(
    ax_left,
    groups,
    location="lower center",
    bbox_to_anchor=(
        0.5,
        -0.04,
    ),
    fontsize=8,
)

assert legend is not None
# =========================================================
# Layout
# =========================================================

figure.figure.tight_layout(
    pad=1.2,
    rect=(
        0.0,
        0.14,
        1.0,
        1.0,
    ),
)


# =========================================================
# Export
# =========================================================

figure.export(
    "output/example_11b_multiple_dual_y_axis",
    formats=[
        "png",
        # "pdf_tex",
    ],
)


print("Example 11B completed successfully.")
