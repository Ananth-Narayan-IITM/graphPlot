"""
Example 01 — VTP Contour
========================

Create a publication-ready contour plot from a VTP file.

Workflow
--------
VTP
 ↓
read_vtp()
 ↓
ContourPlot
 ↓
PublicationFigure
 ↓
labels + title + colorbar
 ↓
PDF + PDF_TeX
"""

from postprocess.io.vtp import read_vtp

from postprocess.plots.contour import (
    ContourPlot,
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

TITLE = (
    r"$\gamma_{\mathrm{DV}}$ distribution"
)

X_LABEL = r"$x\;(m)$"

Y_LABEL = r"$y\;(m)$"

COLORBAR_LABEL = (
    r"$\gamma_{\mathrm{DV}}\;(1/s)$"
)

OUTPUT_FILE = (
    "output/example_01_vtp_contour"
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
        "png",
        "pdf_tex",
    ],
)


print(
    "Example 01 completed successfully."
)