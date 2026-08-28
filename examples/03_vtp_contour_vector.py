"""
Example 03 — VTP Contour + Velocity Vectors
============================================

Create a publication-ready scalar contour with
the velocity vector field overlaid.

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
VectorPlot
 ↓
Title + labels + colorbar
 ↓
PDF + PDF_TeX
"""

from postprocess.io.vtp import read_vtp

from postprocess.plots.contour import (
    ContourPlot,
)

from postprocess.plots.vector import (
    VectorPlot,
)

from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)


# =========================================================
# User configuration
# =========================================================

INPUT_FILE = "data/zNormal.vtp"

FIELD = "gammaDV"

VECTOR_FIELD = "U"

TITLE = (
    r"$\gamma_{\mathrm{DV}}$ distribution "
    r"with velocity field"
)

X_LABEL = r"$x\;(m)$"

Y_LABEL = r"$y\;(m)$"

COLORBAR_LABEL = (
    r"$\gamma_{\mathrm{DV}}\;(1/s)$"
)

OUTPUT_FILE = (
    "output/example_03_vtp_contour_vector"
)


# =========================================================
# Read VTP
# =========================================================

data = read_vtp(
    INPUT_FILE
)


# =========================================================
# Create publication figure
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
# Scalar contour
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
# Velocity vectors
# =========================================================

vector_plot = VectorPlot(
    data,
    field=VECTOR_FIELD,
    association="cell",
)

vectors = vector_plot.plot(
    figure.axes,

    # Preserve vector magnitude.
    normalize=False,

    # Control the number of arrows.
    density=20,

    # Arrow scaling.
    scale=20,

    # Arrow appearance.
    width=0.002,

    color="black",
)


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
        # "pdf",
        "png",
        "pdf_tex",
    ],
)


print(
    "Example 03 completed successfully."
)