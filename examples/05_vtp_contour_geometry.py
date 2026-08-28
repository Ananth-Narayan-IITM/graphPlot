"""
Example 05 — VTP Contour with Geometry and Dimensions
======================================================

Demonstrates a publication-oriented CFD figure containing:

    - scalar contour
    - geometry representation
    - dimension lines
    - dimension arrows
    - dimension labels

The geometry is deliberately constructed using the
AnnotationPlot primitives so that the example also
demonstrates how custom geometry can be added to an
existing CFD result.
"""

from postprocess.io.vtp import read_vtp
from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)
from postprocess.plots.annotation import AnnotationPlot
from postprocess.plots.contour import ContourPlot

# =========================================================
# Configuration
# =========================================================

INPUT_FILE = "data/zNormal.vtp"

FIELD = "gammaDV"

OUTPUT_FILE = "output/example_05_vtp_contour_geometry"


# =========================================================
# Read VTP
# =========================================================

data = read_vtp(INPUT_FILE)


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
# Contour
# =========================================================

contour_plot = ContourPlot(
    data,
    field=FIELD,
    association="cell",
)

contour = contour_plot.plot(figure.axes)


# =========================================================
# Geometry schematic
# =========================================================
#
# A small rectangular geometry is placed in the
# upper-right corner of the CFD domain.
#
# Geometry:
#
#       <------ L ------>
#
#       ┌────────────────┐
#       │                │
#       │    Geometry    │
#       │                │
#       └────────────────┘
#                ↑
#                │ H
#                ↓
#
# =========================================================

geometry_x = 1.0
geometry_y = 4.0

geometry_width = 1.0
geometry_height = 0.65


geometry = AnnotationPlot.add_rectangle(
    figure.axes,
    xy=(
        geometry_x,
        geometry_y,
    ),
    width=geometry_width,
    height=geometry_height,
    edgecolor="black",
    facecolor="white",
    linewidth=1.0,
    alpha=0.9,
)

assert geometry is not None


# =========================================================
# Horizontal dimension
# =========================================================

dimension_y = geometry_y - 0.20

# Dimension line

dimension_line = AnnotationPlot.add_line(
    figure.axes,
    start=(
        geometry_x,
        dimension_y,
    ),
    end=(
        geometry_x + geometry_width,
        dimension_y,
    ),
    color="black",
    linewidth=0.8,
)

assert dimension_line is not None


# Left dimension arrow

AnnotationPlot.add_arrow(
    figure.axes,
    start=(
        geometry_x + 0.08,
        dimension_y,
    ),
    end=(
        geometry_x,
        dimension_y,
    ),
    color="black",
    linewidth=0.8,
    headwidth=0.06,
    headlength=0.08,
)


# Right dimension arrow

AnnotationPlot.add_arrow(
    figure.axes,
    start=(
        geometry_x + geometry_width - 0.08,
        dimension_y,
    ),
    end=(
        geometry_x + geometry_width,
        dimension_y,
    ),
    color="black",
    linewidth=0.8,
    headwidth=0.06,
    headlength=0.08,
)


# Horizontal dimension label

AnnotationPlot.add_text(
    figure.axes,
    x=(geometry_x + geometry_width / 2),
    y=(dimension_y - 0.10),
    text=r"$L = 1.0\;m$",
    fontsize=8,
    ha="center",
    va="top",
)


# =========================================================
# Vertical dimension
# =========================================================

dimension_x = geometry_x + geometry_width + 0.20

# Dimension line

vertical_dimension_line = AnnotationPlot.add_line(
    figure.axes,
    start=(
        dimension_x,
        geometry_y,
    ),
    end=(
        dimension_x,
        geometry_y + geometry_height,
    ),
    color="black",
    linewidth=0.8,
)

assert vertical_dimension_line is not None


# Bottom arrow

AnnotationPlot.add_arrow(
    figure.axes,
    start=(
        dimension_x,
        geometry_y + 0.08,
    ),
    end=(
        dimension_x,
        geometry_y,
    ),
    color="black",
    linewidth=0.8,
    headwidth=0.06,
    headlength=0.08,
)


# Top arrow

AnnotationPlot.add_arrow(
    figure.axes,
    start=(
        dimension_x,
        geometry_y + geometry_height - 0.08,
    ),
    end=(
        dimension_x,
        geometry_y + geometry_height,
    ),
    color="black",
    linewidth=0.8,
    headwidth=0.06,
    headlength=0.08,
)


# Vertical dimension label

AnnotationPlot.add_text(
    figure.axes,
    x=(dimension_x + 0.08),
    y=(geometry_y + geometry_height / 2),
    text=r"$H = 0.65\;m$",
    fontsize=8,
    ha="left",
    va="center",
    rotation=90,
)


# =========================================================
# Axis labels
# =========================================================

figure.set_labels(
    xlabel=r"$x\;(m)$",
    ylabel=r"$y\;(m)$",
)


# =========================================================
# Title
# =========================================================

figure.set_title(r"$\gamma_{\mathrm{DV}}$ distribution")


# =========================================================
# Colorbar
# =========================================================

figure.add_colorbar(
    contour,
    label=r"$\gamma_{\mathrm{DV}}$",
)


# =========================================================
# Export
# =========================================================

figure.export(
    OUTPUT_FILE,
    formats=[
        "png",
        "pdf_tex",
    ],
)


print("Example 05 completed successfully.")
