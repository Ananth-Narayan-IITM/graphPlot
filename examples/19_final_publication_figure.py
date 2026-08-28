"""
Example 19 — Final Publication Figure
=====================================

Final integrated example demonstrating a publication-ready
CFD and validation figure.

Panels:

    (a) gammaDV contour
    (b) gammaDV contour + mesh
    (c) numerical vs experiment
    (d) numerical vs analytical

Demonstrates:

    - VTP contour
    - mesh overlay
    - 1D numerical data
    - experimental data
    - analytical data
    - 2x2 layout
    - panel labels
    - shared color scale
    - horizontal colorbar
    - grouped legends
    - publication styling
    - PDF/PNG export
"""

from pathlib import Path

import numpy as np

from postprocess.data.data1d import (
    Data1D,
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
from postprocess.plots.line import (
    LinePlot,
)
from postprocess.plots.mesh import (
    MeshPlot,
)
from postprocess.style.publication import (
    PublicationStyle,
)

# =========================================================
# Input files
# =========================================================

VTP_FILE = Path("data/zNormal.vtp")

NUMERICAL_FILE = Path("data/numerical.dat")

ANALYTICAL_FILE = Path("data/analytical.dat")

EXPERIMENT_FILE = Path("data/experiment.dat")


# =========================================================
# Read VTP
# =========================================================

vtp = read_vtp(VTP_FILE)


# =========================================================
# Read 1D data
# =========================================================

numerical = np.loadtxt(NUMERICAL_FILE)

analytical = np.loadtxt(ANALYTICAL_FILE)

experiment = np.loadtxt(EXPERIMENT_FILE)


# =========================================================
# Create Data1D objects
# =========================================================

numerical_data = Data1D(
    x=numerical[:, 0],
    y=numerical[:, 1],
)

analytical_data = Data1D(
    x=analytical[:, 0],
    y=analytical[:, 1],
)

experiment_data = Data1D(
    x=experiment[:, 0],
    y=experiment[:, 1],
)


# =========================================================
# Publication style
# =========================================================

style = PublicationStyle(
    color_scheme="colorblind",
)


# =========================================================
# Figure
# =========================================================

figure_config = FigureConfig(
    width=7.0,
    height=7.2,
    dpi=600,
    aspect="auto",
)

figure = PublicationFigure(
    figure_config,
    nrows=2,
    ncols=2,
    sharex=False,
    sharey=False,
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
# gammaDV
# =========================================================

gamma = np.asarray(
    vtp.get_field(
        "gammaDV",
        "cell",
    )
)

gamma_min = np.nanmin(gamma)

gamma_max = np.nanmax(gamma)


# =========================================================
# Shared gammaDV scale
# =========================================================

gamma_scale = ColorScale(
    levels=30,
    cmap="viridis",
    vmin=gamma_min,
    vmax=gamma_max,
)

gamma_scale.resolve(gamma)


# =========================================================
# Panel (a)
# =========================================================

contour_plot_a = ContourPlot(
    vtp,
    field="gammaDV",
    association="cell",
)

contour_a = contour_plot_a.plot(
    ax00,
    scale=gamma_scale,
)

assert contour_a is not None


# =========================================================
# Panel (b)
# =========================================================

contour_plot_b = ContourPlot(
    vtp,
    field="gammaDV",
    association="cell",
)

contour_b = contour_plot_b.plot(
    ax01,
    scale=gamma_scale,
)

assert contour_b is not None


# =========================================================
# Mesh overlay
# =========================================================

mesh_plot = MeshPlot(vtp)

mesh = mesh_plot.plot(
    ax01,
    edgecolor="black",
    facecolor="none",
    linewidth=0.15,
    alpha=0.35,
)

assert mesh is not None


# =========================================================
# Numerical / Experimental line plot
# =========================================================

comparison_plot = LinePlot(
    style=style,
)


# Numerical
comparison_plot.add(
    numerical_data,
    label="Numerical",
)


# Experiment
comparison_plot.add(
    experiment_data,
    label="Experiment",
)


comparison_artists = comparison_plot.plot(ax10)

assert len(comparison_artists) == 2


# =========================================================
# Numerical / Analytical line plot
# =========================================================

analytical_plot = LinePlot(
    style=style,
)


# Numerical
analytical_plot.add(
    numerical_data,
    label="Numerical",
)


# Analytical
analytical_plot.add(
    analytical_data,
    label="Analytical",
)


analytical_artists = analytical_plot.plot(ax11)

assert len(analytical_artists) == 2


# =========================================================
# Line plot legends
# =========================================================

comparison_plot.legend(
    ax10,
    location="best",
    frameon=False,
    ncol=1,
    fontsize=8,
)


analytical_plot.legend(
    ax11,
    location="best",
    frameon=False,
    ncol=1,
    fontsize=8,
)


# =========================================================
# CFD axis limits
# =========================================================

x_min, x_max, y_min, y_max = vtp.mesh.bounds


ax00.set_xlim(
    x_min,
    x_max,
)

ax00.set_ylim(
    y_min,
    y_max,
)

ax01.set_xlim(
    x_min,
    x_max,
)

ax01.set_ylim(
    y_min,
    y_max,
)


# =========================================================
# CFD aspect ratio
# =========================================================

ax00.set_aspect(
    "equal",
    adjustable="box",
)

ax01.set_aspect(
    "equal",
    adjustable="box",
)


# =========================================================
# Validation axis labels
# =========================================================

ax10.set_xlabel(
    r"$x$",
)

ax10.set_ylabel(
    r"$y$",
)

ax11.set_xlabel(
    r"$x$",
)

ax11.set_ylabel(
    r"$y$",
)


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
# Common Y label for CFD panels
# =========================================================

figure.set_common_ylabel(
    r"$y\;(\mathrm{m})$",
    x=0.025,
    y=0.72,
)


# =========================================================
# gammaDV colorbar
# =========================================================

gamma_colorbar = figure.add_shared_colorbar(
    contour_a,
    axes=[
        ax00,
        ax01,
    ],
    label=r"$\gamma_{\mathrm{DV}}$",
    orientation="horizontal",
    fraction=0.065,
    pad=0.08,
    shrink=0.75,
)

assert gamma_colorbar is not None


# =========================================================
# Colorbar ticks
# =========================================================

gamma_colorbar.set_ticks(
    np.linspace(
        gamma_min,
        gamma_max,
        5,
    )
)

gamma_colorbar.ax.tick_params(
    labelsize=8,
    pad=2,
)


# =========================================================
# Layout
# =========================================================

figure.adjust_layout(
    left=0.10,
    right=0.97,
    bottom=0.10,
    top=0.97,
    wspace=0.25,
    hspace=0.35,
)


# =========================================================
# Export
# =========================================================

OUTPUT_FILE = "output/example_19_final_publication_figure"

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


print("Example 19 completed successfully.")
