"""
Example 12 — VTP Contour + Mesh + Vectors
==========================================

Demonstrates a publication-quality CFD figure combining:

    1. Cell-based contour field
    2. Computational mesh
    3. Cell-based vector field
    4. Vector normalization
    5. Vector downsampling
    6. Publication figure formatting
    7. PDF + PDF_TeX export

The contour is used as the background field, the mesh is
overlaid with transparent cell boundaries, and the vector
field is plotted on top.
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
    height=3.0,
    dpi=600,
)

figure = PublicationFigure(figure_config)


# =========================================================
# Contour
# =========================================================

contour_plot = ContourPlot(
    data,
    field="gammaDV",
    association="cell",
)


contour = contour_plot.plot(
    figure.axes,
)


assert contour is not None


# =========================================================
# Mesh
# =========================================================

mesh_plot = MeshPlot(data)


mesh = mesh_plot.plot(
    figure.axes,
    edgecolor="black",
    facecolor="none",
    linewidth=0.15,
    alpha=0.35,
)


assert mesh is not None


# Keep the mesh behind the vectors.
mesh.set_zorder(3)


# =========================================================
# Vectors
# =========================================================

vector_plot = VectorPlot(
    data,
    field="U",
    association="cell",
)


vectors = vector_plot.plot(
    figure.axes,
    normalize=True,
    density=18,
    scale=25,
    width=0.002,
    color="black",
    alpha=0.9,
    pivot="mid",
    zorder=5,
)


assert vectors is not None


# =========================================================
# Axes
# =========================================================

figure.axes.set_xlabel(r"$x\;(\mathrm{m})$")

figure.axes.set_ylabel(r"$y\;(\mathrm{m})$")


# =========================================================
# Axis limits
# =========================================================

x_min, x_max, y_min, y_max = data.mesh.bounds


figure.axes.set_xlim(
    x_min,
    x_max,
)

figure.axes.set_ylim(
    y_min,
    y_max,
)


# =========================================================
# Aspect ratio
# =========================================================

figure.axes.set_aspect(
    "equal",
    adjustable="box",
)


# =========================================================
# Grid
# =========================================================

figure.axes.grid(False)


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
    "output/example_12_vtp_contour_mesh_vector",
    formats=[
        "png",
        # "pdf_tex",
    ],
)


print("Example 12 completed successfully.")
