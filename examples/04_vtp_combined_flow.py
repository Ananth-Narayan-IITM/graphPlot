"""
Example 04 — Combined VTP Flow Visualization
=============================================

Demonstrates a complete CFD visualization containing:

    - scalar contour
    - computational mesh
    - velocity vectors
    - streamlines
    - annotations

This example is intended as a reusable template for
publication-quality CFD figures.
"""

from postprocess.io.vtp import read_vtp

from postprocess.plots.contour import ContourPlot
from postprocess.plots.mesh import MeshPlot
from postprocess.plots.vector import VectorPlot
from postprocess.plots.streamline import StreamlinePlot
from postprocess.plots.annotation import AnnotationPlot

from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)


# =========================================================
# Configuration
# =========================================================

INPUT_FILE = "data/zNormal.vtp"

FIELD = "gammaDV"
VECTOR_FIELD = "U"

TITLE = (
    r"$\gamma_{\mathrm{DV}}$ distribution"
)

X_LABEL = r"$x\;(m)$"
Y_LABEL = r"$y\;(m)$"

COLORBAR_LABEL = (
    r"$\gamma_{\mathrm{DV}}\;(1/s)$"
)

OUTPUT_FILE = (
    "output/example_04_vtp_combined_flow"
)


# =========================================================
# Read data
# =========================================================

data = read_vtp(
    INPUT_FILE
)


# =========================================================
# Figure
# =========================================================

figure_config = FigureConfig(
    width=3.4,
    height=3.0,
    dpi=600,
)

figure = PublicationFigure(
    figure_config
)


# =========================================================
# Contour
# =========================================================

contour_plot = ContourPlot(
    data,
    field=FIELD,
)

contour = contour_plot.plot(
    figure.axes,
    rasterize=True,
)


# =========================================================
# Mesh
# =========================================================

mesh_plot = MeshPlot(
    data
)

mesh = mesh_plot.plot(
    figure.axes,
    edgecolor="black",
    facecolor="none",
    linewidth=0.15,
    alpha=0.35,
)

mesh.set_rasterized(True)


# =========================================================
# Velocity vectors
# =========================================================

vector_plot = VectorPlot(
    data,
    field=VECTOR_FIELD,
    association="cell",
)

vectors = vector_plot.plot(
    figure.axes,
    normalize=False,
    density=20,
    scale=20,
    width=0.002,
    color="black",
)


# =========================================================
# Streamlines
# =========================================================

streamline_plot = StreamlinePlot(
    data,
    field=VECTOR_FIELD,
)


streamlines = streamline_plot.plot(
    figure.axes,

    # Number of automatically generated seeds.
    n_seeds=50,

    # Distribute seeds along the y direction.
    seed_axis="y",

    # Keep a small margin from the boundaries.
    seed_margin=0.01,

    # Use the accurate adaptive RK45 integrator.
    integrator_type=45,

    # Constrain streamlines to the 2-D surface.
    surface_streamlines=True,

    # Integration controls.
    initial_step_length=0.1,
    min_step_length=0.01,
    max_step_length=0.5,
    max_steps=2000,

    # Stop integration when velocity becomes negligible.
    terminal_speed=1e-12,

    # RK45 error tolerance.
    max_error=1e-6,

    # Interpolate velocity from cells.
    interpolator_type="cell",

    # Publication styling.
    color="black",
    linewidth=0.7,
    arrowsize=1.0,
)
# =========================================================
# Annotation
# =========================================================

AnnotationPlot.add_text(
    figure.axes,
    x=0.15,
    y=0.85,
    text=r"Flow direction",
    fontsize=9,
    ha="left",
    va="center",
)
AnnotationPlot.add_arrow(
    figure.axes,
    start=(0.15, 0.70),
    end=(0.65, 0.70),
    color="black",
    linewidth=1.0,
    headwidth=0.08,
    headlength=0.12,
)
# =========================================================
# Labels
# =========================================================

figure.set_labels(
    xlabel=X_LABEL,
    ylabel=Y_LABEL,
)

figure.set_title(
    TITLE
)


# =========================================================
# Colorbar
# =========================================================

figure.add_colorbar(
    contour,
    label=COLORBAR_LABEL,
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


print(
    "Example 04 completed successfully."
)