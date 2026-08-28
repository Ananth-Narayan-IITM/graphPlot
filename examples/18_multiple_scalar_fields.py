"""
Example 18 — Multiple Scalar Fields
====================================

Demonstrates:

    - Multi-panel CFD visualization
    - Multiple scalar fields
    - Common color scale for the same field
    - Independent color scale for another field
    - Independent colormaps
    - Shared colorbar for related panels
    - Separate colorbar for a different quantity
    - Explicit colorbar tick control
    - Panel labels
    - Common X/Y labels
    - Publication-quality export

The available example VTP contains gammaDV and U.

Therefore:

    gammaDV
        -> primary scalar field

    phi
        -> derived scalar field used only to
           demonstrate an independent scalar scale
"""

from pathlib import Path

import numpy as np
from matplotlib.collections import (
    PolyCollection,
)

from postprocess.io.vtp import (
    read_vtp,
)
from postprocess.layout.colors import (
    ColorScale,
)
from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)
from postprocess.plots.contour import (
    ContourPlot,
)
from postprocess.plots.mesh import (
    MeshPlot,
)

# =========================================================
# Input
# =========================================================

INPUT_FILE = Path("data/zNormal.vtp")


# =========================================================
# Read VTP
# =========================================================

data = read_vtp(INPUT_FILE)


# =========================================================
# Geometry
# =========================================================

x_min, x_max, y_min, y_max = data.mesh.bounds


# =========================================================
# Primary scalar field
# =========================================================

gamma = np.asarray(
    data.get_field(
        "gammaDV",
        "cell",
    )
)


# =========================================================
# Derived scalar field
# =========================================================
#
# This is deliberately created only for demonstrating
# independent scalar-field normalization.
#
# It is NOT intended to represent a physical quantity.
# =========================================================

gamma_min = np.nanmin(gamma)

gamma_max = np.nanmax(gamma)

if gamma_max == gamma_min:
    phi = np.zeros_like(gamma)

else:
    gamma_normalized = (gamma - gamma_min) / (gamma_max - gamma_min)

    phi = gamma_normalized**2


# =========================================================
# Figure configuration
# =========================================================

figure_config = FigureConfig(
    width=7.0,
    height=8.0,
    dpi=600,
    aspect="equal",
)


# =========================================================
# Figure
# =========================================================

figure = PublicationFigure(
    figure_config,
    nrows=2,
    ncols=2,
    sharex=True,
    sharey=True,
)


# =========================================================
# Panels
# =========================================================

ax00 = figure.panel(
    0,
    0,
)

ax01 = figure.panel(
    0,
    1,
)

ax10 = figure.panel(
    1,
    0,
)

ax11 = figure.panel(
    1,
    1,
)


# =========================================================
# Common gammaDV color scale
# =========================================================

gamma_scale = ColorScale(
    levels=30,
    cmap="viridis",
    vmin=gamma_min,
    vmax=gamma_max,
)

gamma_scale.resolve(gamma)


# =========================================================
# Panel (a) — gammaDV
# =========================================================

contour_a_plot = ContourPlot(
    data,
    field="gammaDV",
    association="cell",
)

contour_a = contour_a_plot.plot(
    ax00,
    scale=gamma_scale,
)

assert contour_a is not None


# =========================================================
# Panel (b) — gammaDV + mesh
# =========================================================

contour_b_plot = ContourPlot(
    data,
    field="gammaDV",
    association="cell",
)

contour_b = contour_b_plot.plot(
    ax01,
    scale=gamma_scale,
)

assert contour_b is not None


# =========================================================
# Mesh — Panel (b)
# =========================================================

mesh_plot_b = MeshPlot(data)

mesh_b = mesh_plot_b.plot(
    ax01,
    edgecolor="black",
    facecolor="none",
    linewidth=0.15,
    alpha=0.35,
)

assert mesh_b is not None


# =========================================================
# Independent phi color scale
# =========================================================

phi_min = np.nanmin(phi)

phi_max = np.nanmax(phi)

phi_scale = ColorScale(
    levels=30,
    cmap="plasma",
    vmin=phi_min,
    vmax=phi_max,
)

phi_scale.resolve(phi)


# =========================================================
# Mesh polygons
# =========================================================

polygons = data.mesh.polygons


# =========================================================
# Panel (c) — phi
# =========================================================

phi_collection_c = ax10.add_collection(
    PolyCollection(
        polygons,
        array=phi,
        cmap=phi_scale.colormap,
        norm=phi_scale.norm,
        edgecolors="none",
        linewidths=0.0,
        antialiased=True,
    )
)

assert phi_collection_c is not None


# =========================================================
# Panel (d) — phi + mesh
# =========================================================

phi_collection_d = ax11.add_collection(
    PolyCollection(
        polygons,
        array=phi,
        cmap=phi_scale.colormap,
        norm=phi_scale.norm,
        edgecolors="none",
        linewidths=0.0,
        antialiased=True,
    )
)

assert phi_collection_d is not None


# =========================================================
# Mesh — Panel (d)
# =========================================================

mesh_plot_d = MeshPlot(data)

mesh_d = mesh_plot_d.plot(
    ax11,
    edgecolor="black",
    facecolor="none",
    linewidth=0.15,
    alpha=0.35,
)

assert mesh_d is not None


# =========================================================
# Axis configuration
# =========================================================

for ax in (
    ax00,
    ax01,
    ax10,
    ax11,
):
    ax.set_xlim(
        x_min,
        x_max,
    )

    ax.set_ylim(
        y_min,
        y_max,
    )

    ax.set_aspect(
        "equal",
        adjustable="box",
    )

    ax.grid(False)


# =========================================================
# Panel labels
# =========================================================

figure.label_panels(
    labels=[
        "(a)",
        "(b)",
        "(c)",
        "(d)",
    ],
    x=0.02,
    y=0.97,
    fontsize=10,
)


# =========================================================
# Layout
# =========================================================
#
# IMPORTANT:
#
# No colorbars have been created yet.
#
# Therefore adjust_layout() establishes the geometry of
# the four panels without colorbars stealing space.
# =========================================================

figure.adjust_layout(
    left=0.09,
    right=0.97,
    bottom=0.17,
    top=0.97,
    wspace=0.08,
    hspace=0.42,
)


# =========================================================
# Get final panel positions
# =========================================================
#
# Positions are in figure coordinates:
#
#       x0, y0, width, height
#
# This allows the colorbars to automatically align with
# the panel layout.
# =========================================================

pos00 = ax00.get_position()
pos01 = ax01.get_position()
pos10 = ax10.get_position()
pos11 = ax11.get_position()


# =========================================================
# Horizontal extent for colorbars
# =========================================================
#
# Align the colorbars with the complete width of the
# two-panel grid.
# =========================================================

colorbar_x0 = min(
    pos00.x0,
    pos01.x0,
    pos10.x0,
    pos11.x0,
)

colorbar_x1 = max(
    pos00.x1,
    pos01.x1,
    pos10.x1,
    pos11.x1,
)

colorbar_width = colorbar_x1 - colorbar_x0


# =========================================================
# Gamma colorbar position
# =========================================================
#
# Place gammaDV colorbar in the gap between the two rows.
# =========================================================

upper_row_bottom = min(
    pos00.y0,
    pos01.y0,
)

lower_row_top = max(
    pos10.y1,
    pos11.y1,
)

row_gap = upper_row_bottom - lower_row_top

gamma_bar_height = 0.018

gamma_bar_y = lower_row_top + 0.50 * row_gap - 0.5 * gamma_bar_height


# =========================================================
# Phi colorbar position
# =========================================================
#
# Place phi colorbar below the lower panels.
# =========================================================

phi_bar_height = 0.018

phi_bar_y = pos10.y0 - 0.075


# =========================================================
# Create dedicated colorbar axes
# =========================================================
#
# We intentionally use dedicated axes rather than
# figure.add_shared_colorbar().
#
# This prevents Matplotlib from changing the geometry of
# the four CFD panels.
# =========================================================

gamma_cbar_ax = figure.figure.add_axes(
    [
        colorbar_x0 + 0.08 * colorbar_width,
        gamma_bar_y,
        0.84 * colorbar_width,
        gamma_bar_height,
    ]
)


phi_cbar_ax = figure.figure.add_axes(
    [
        colorbar_x0 + 0.08 * colorbar_width,
        phi_bar_y,
        0.84 * colorbar_width,
        phi_bar_height,
    ]
)


# =========================================================
# GammaDV colorbar
# =========================================================

gamma_colorbar = figure.figure.colorbar(
    contour_a,
    cax=gamma_cbar_ax,
    orientation="horizontal",
)


# =========================================================
# GammaDV ticks
# =========================================================

gamma_ticks = np.linspace(
    gamma_min,
    gamma_max,
    5,
)

gamma_colorbar.set_ticks(gamma_ticks)

gamma_colorbar.set_label(
    r"$\gamma_{\mathrm{DV}}$",
    labelpad=4,
)

gamma_colorbar.ax.tick_params(
    labelsize=8,
    pad=2,
)


# =========================================================
# Phi colorbar
# =========================================================

phi_colorbar = figure.figure.colorbar(
    phi_collection_c,
    cax=phi_cbar_ax,
    orientation="horizontal",
)


# =========================================================
# Phi ticks
# =========================================================

phi_ticks = np.linspace(
    phi_min,
    phi_max,
    5,
)

phi_colorbar.set_ticks(phi_ticks)

phi_colorbar.set_label(
    r"$\phi$",
    labelpad=4,
)

phi_colorbar.ax.tick_params(
    labelsize=8,
    pad=2,
)


# =========================================================
# Common X/Y labels
# =========================================================
#
# These are deliberately added AFTER the colorbars so that
# their position is independent of colorbar creation.
# =========================================================

figure.set_common_xlabel(
    r"$x\;(\mathrm{m})$",
    x=0.5,
    y=0.025,
)

figure.set_common_ylabel(
    r"$y\;(\mathrm{m})$",
    x=0.025,
    y=0.5,
)


# =========================================================
# Export
# =========================================================

OUTPUT_FILE = "output/example_18_multiple_scalar_fields"

figure.export(
    OUTPUT_FILE,
    formats=[
        "png",
        "pdf",
        # "pdf_tex",
    ],
)


# =========================================================
# Close
# =========================================================

figure.close()


print("Example 18 completed successfully.")
