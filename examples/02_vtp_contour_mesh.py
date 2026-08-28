"""
Example 02 — VTP Contour + Computational Mesh
==============================================

Create a publication-ready contour plot with the
computational mesh overlaid.

Workflow
--------
VTP
 ↓
read_vtp()
 ↓
PublicationFigure
 ↓
ContourPlot
 ↓
MeshPlot
 ↓
Title + labels + colorbar
 ↓
PDF + PDF_TeX
"""

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

# =========================================================
# User configuration
# =========================================================

INPUT_FILE = "data/zNormal.vtp"

FIELD = "gammaDV"

TITLE = r"$\gamma_{\mathrm{DV}}$ distribution"

X_LABEL = r"$x\;(m)$"

Y_LABEL = r"$y\;(m)$"

COLORBAR_LABEL = r"$\gamma_{\mathrm{DV}}\;(1/s)$"

OUTPUT_FILE = "output/example_02_vtp_contour_mesh"


# =========================================================
# Read VTP
# =========================================================

data = read_vtp(INPUT_FILE)


# =========================================================
# Create publication figure
# =========================================================

figure_config = FigureConfig(
    width=3.4,
    height=3.0,
    dpi=1200,
)

figure = PublicationFigure(figure_config)


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
# Computational mesh
# =========================================================

mesh_plot = MeshPlot(data)

mesh = mesh_plot.plot(
    figure.axes,
    edgecolor="black",
    facecolor="none",
    linewidth=0.4,
    alpha=1.0,
)

# Rasterize mesh as well.
# This keeps the PDF compact when the mesh contains
# thousands of cells.
mesh.set_rasterized(True)


# =========================================================
# Axis labels
# =========================================================

figure.set_labels(
    xlabel=X_LABEL,
    ylabel=Y_LABEL,
)


# =========================================================
# Title
# =========================================================

figure.set_title(TITLE)


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


print("Example 02 completed successfully.")
