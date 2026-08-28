"""
Example 15 — CFD Visualization with Geometry Dimensions
========================================================

Demonstrates:

    - Cell-based contour
    - Computational mesh
    - Velocity vectors
    - Streamlines
    - Geometry dimensions
    - Dimension arrows
    - Geometry annotations
    - LaTeX labels
    - Publication-quality export

The dimensions are based on the physical geometry bounds.
"""

from pathlib import Path

from postprocess.io.vtp import read_vtp

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

from postprocess.plots.vector import (
    VectorPlot,
)

from postprocess.plots.streamline import (
    StreamlinePlot,
)

from postprocess.plots.annotation import (
    AnnotationPlot,
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
# Figure
# =========================================================

figure_config = FigureConfig(
    width=3.4,
    height=3.4,
    dpi=600,
)

figure = PublicationFigure(figure_config)

axes = figure.axes


# =========================================================
# Contour
# =========================================================

contour_plot = ContourPlot(
    data,
    field="gammaDV",
    association="cell",
)

contour = contour_plot.plot(
    axes,
)

assert contour is not None


# =========================================================
# Mesh
# =========================================================

mesh_plot = MeshPlot(
    data,
)

mesh = mesh_plot.plot(
    axes,
    edgecolor="black",
    facecolor="none",
    linewidth=0.15,
    alpha=0.35,
)

assert mesh is not None

mesh.set_zorder(3)


# =========================================================
# Velocity vectors
# =========================================================

vector_plot = VectorPlot(
    data,
    field="U",
    association="cell",
)

vectors = vector_plot.plot(
    axes,
    normalize=True,
    density=18,
    scale=25,
    width=0.002,
    color="black",
    alpha=0.85,
    pivot="mid",
    zorder=5,
)

assert vectors is not None


# =========================================================
# Streamlines
# =========================================================

streamline_plot = StreamlinePlot(
    data,
    field="U",
    association="cell",
)

streamlines = streamline_plot.plot(
    axes,
    n_seeds=20,
    seed_axis="y",
    seed_position=None,
    seed_margin=0.02,
    integration_direction="forward",
    integrator_type=45,
    surface_streamlines=True,
    initial_step_length=0.1,
    min_step_length=0.01,
    max_step_length=0.5,
    max_steps=2000,
    max_length=None,
    terminal_speed=1e-12,
    max_error=1e-6,
    interpolator_type="cell",
    color="black",
    linewidth=0.8,
    arrowsize=1.0,
    zorder=6,
)

assert streamlines is not None


# =========================================================
# Physical geometry dimensions
# =========================================================

x_min, x_max, y_min, y_max = data.mesh.bounds

geometry_width = x_max - x_min

geometry_height = y_max - y_min


# =========================================================
# Dimension styling
# =========================================================

dimension_color = "black"

dimension_linewidth = 0.8

# These values are deliberately small because
# AnnotationPlot.add_arrow() uses data coordinates.
dimension_headwidth = 0.04
dimension_headlength = 0.07


# =========================================================
# Horizontal dimension: L
# =========================================================

dimension_y = y_min - 0.10 * geometry_height


# Dimension line
AnnotationPlot.add_line(
    axes,
    start=(
        x_min,
        dimension_y,
    ),
    end=(
        x_max,
        dimension_y,
    ),
    color=dimension_color,
    linewidth=dimension_linewidth,
    zorder=10,
)


# Left extension line
AnnotationPlot.add_line(
    axes,
    start=(
        x_min,
        y_min,
    ),
    end=(
        x_min,
        dimension_y,
    ),
    color=dimension_color,
    linewidth=dimension_linewidth,
    zorder=10,
)


# Right extension line
AnnotationPlot.add_line(
    axes,
    start=(
        x_max,
        y_min,
    ),
    end=(
        x_max,
        dimension_y,
    ),
    color=dimension_color,
    linewidth=dimension_linewidth,
    zorder=10,
)


# Left arrowhead
AnnotationPlot.add_arrow(
    axes,
    start=(
        x_min + 0.10 * geometry_width,
        dimension_y,
    ),
    end=(
        x_min,
        dimension_y,
    ),
    color=dimension_color,
    linewidth=dimension_linewidth,
    headwidth=dimension_headwidth,
    headlength=dimension_headlength,
    zorder=10,
)


# Right arrowhead
AnnotationPlot.add_arrow(
    axes,
    start=(
        x_max - 0.10 * geometry_width,
        dimension_y,
    ),
    end=(
        x_max,
        dimension_y,
    ),
    color=dimension_color,
    linewidth=dimension_linewidth,
    headwidth=dimension_headwidth,
    headlength=dimension_headlength,
    zorder=10,
)


# Dimension label
AnnotationPlot.add_text(
    axes,
    x=(x_min + 0.50 * geometry_width),
    y=(dimension_y - 0.025 * geometry_height),
    text=r"$L$",
    fontsize=10,
    ha="center",
    va="top",
    zorder=11,
)


# =========================================================
# Vertical dimension: H
# =========================================================

dimension_x = x_min - 0.10 * geometry_width


# Dimension line
AnnotationPlot.add_line(
    axes,
    start=(
        dimension_x,
        y_min,
    ),
    end=(
        dimension_x,
        y_max,
    ),
    color=dimension_color,
    linewidth=dimension_linewidth,
    zorder=10,
)


# Bottom extension line
AnnotationPlot.add_line(
    axes,
    start=(
        x_min,
        y_min,
    ),
    end=(
        dimension_x,
        y_min,
    ),
    color=dimension_color,
    linewidth=dimension_linewidth,
    zorder=10,
)


# Top extension line
AnnotationPlot.add_line(
    axes,
    start=(
        x_min,
        y_max,
    ),
    end=(
        dimension_x,
        y_max,
    ),
    color=dimension_color,
    linewidth=dimension_linewidth,
    zorder=10,
)


# Bottom arrowhead
AnnotationPlot.add_arrow(
    axes,
    start=(
        dimension_x,
        y_min + 0.10 * geometry_height,
    ),
    end=(
        dimension_x,
        y_min,
    ),
    color=dimension_color,
    linewidth=dimension_linewidth,
    headwidth=dimension_headwidth,
    headlength=dimension_headlength,
    zorder=10,
)


# Top arrowhead
AnnotationPlot.add_arrow(
    axes,
    start=(
        dimension_x,
        y_max - 0.10 * geometry_height,
    ),
    end=(
        dimension_x,
        y_max,
    ),
    color=dimension_color,
    linewidth=dimension_linewidth,
    headwidth=dimension_headwidth,
    headlength=dimension_headlength,
    zorder=10,
)


# Dimension label
AnnotationPlot.add_text(
    axes,
    x=(dimension_x - 0.025 * geometry_width),
    y=(y_min + 0.50 * geometry_height),
    text=r"$H$",
    fontsize=10,
    ha="right",
    va="center",
    rotation=90,
    zorder=11,
)


# =========================================================
# Geometry annotation
# =========================================================

AnnotationPlot.add_text(
    axes,
    x=(x_min + 0.50 * geometry_width),
    y=(y_max + 0.035 * geometry_height),
    text=r"Computational domain",
    fontsize=8,
    ha="center",
    va="bottom",
    zorder=11,
)


# =========================================================
# Axes labels
# =========================================================

axes.set_xlabel(r"$x\;(\mathrm{m})$")

axes.set_ylabel(r"$y\;(\mathrm{m})$")


# =========================================================
# Aspect ratio
# =========================================================

axes.set_aspect(
    "equal",
    adjustable="box",
)


# =========================================================
# Grid
# =========================================================

axes.grid(False)


# =========================================================
# Expanded limits
# =========================================================

axes.set_xlim(
    x_min - 0.16 * geometry_width,
    x_max + 0.02 * geometry_width,
)

axes.set_ylim(
    y_min - 0.16 * geometry_height,
    y_max + 0.08 * geometry_height,
)


# =========================================================
# Layout
# =========================================================

figure.figure.tight_layout(
    pad=1.0,
)


# =========================================================
# Export
# =========================================================

figure.export(
    "output/example_15_vtp_cfd_geometry_dimensions",
    formats=[
        "png",
        # "pdf_tex",
    ],
)


print("Example 15 completed successfully.")
