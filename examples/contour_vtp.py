from pathlib import Path

from postprocess.io.vtp import read_vtp

from postprocess.plots.contour import ContourPlot
from postprocess.plots.mesh import MeshPlot

from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)

from postprocess.layout.colors import (
    ColorScale,
)

from postprocess.style.publication import (
    PublicationStyle,
)


# =========================================================
# Configuration
# =========================================================

INPUT_FILE = Path(
    "data/zNormal.vtp"
)

FIELD = "gammaDV"

OUTPUT_FILE = Path(
    f"output/{FIELD}"
)


# =========================================================
# Visualization
# =========================================================

SHOW_CONTOURS = True
SHOW_MESH = False


# =========================================================
# Color scale
# =========================================================

LEVELS = 30
CMAP = "viridis"

VMIN = None
VMAX = None


# =========================================================
# Mesh
# =========================================================

MESH_COLOR = "black"
MESH_LINEWIDTH = 0.25
MESH_ALPHA = 0.5


# =========================================================
# Figure
# =========================================================

FIGURE_WIDTH = 3.5
FIGURE_HEIGHT_RATIO = 0.8

ASPECT = "equal"

SHOW_GRID = False


# =========================================================
# Labels
# =========================================================

X_LABEL = r"$x$ (m)"
Y_LABEL = r"$y$ (m)"

COLORBAR_LABEL = (
    r"$\gamma$ (1/s)"
)


# =========================================================
# Publication style
# =========================================================

# IMPORTANT:
#
# For PDF+TeX export, keep Matplotlib's external
# LaTeX rendering disabled.
#
# The LaTeX text will be handled by the PDF_TeX
# output instead.

style = PublicationStyle(
    font_size=10,
    use_latex=False,
)

style.apply()


# =========================================================
# Read VTP
# =========================================================

data = read_vtp(
    INPUT_FILE
)

print(
    f"Reading: {data.filename}"
)

print(
    f"Points:  {data.n_points}"
)

print(
    f"Cells:   {data.n_cells}"
)

print(
    f"Bounds:  {data.bounds}"
)


# =========================================================
# Color scale
# =========================================================

scale = ColorScale(
    levels=LEVELS,
    cmap=CMAP,
    vmin=VMIN,
    vmax=VMAX,
)


# =========================================================
# Figure
# =========================================================

figure_config = FigureConfig(
    width=FIGURE_WIDTH,
    height_ratio=FIGURE_HEIGHT_RATIO,
    aspect=ASPECT,
    show_grid=SHOW_GRID,
    dpi=600,
)

figure = PublicationFigure(
    figure_config
)


# =========================================================
# Contour
# =========================================================

contour = None

if SHOW_CONTOURS:

    contour_plot = ContourPlot(
        data,
        field=FIELD,
        association="cell",
    )

    contour = contour_plot.plot(
        figure.axes,
        scale=scale,
        rasterize=True,
    )


# =========================================================
# Mesh
# =========================================================

if SHOW_MESH:

    mesh_plot = MeshPlot(
        data
    )

    mesh_plot.plot(
        figure.axes,
        color=MESH_COLOR,
        linewidth=MESH_LINEWIDTH,
        alpha=MESH_ALPHA,
    )


# =========================================================
# Labels
# =========================================================

figure.set_labels(
    xlabel=X_LABEL,
    ylabel=Y_LABEL,
)


# =========================================================
# Colorbar
# =========================================================

if contour is not None:

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
        # "png",
        # "pdf",
        "pdf_tex",
    ],
)


# =========================================================
# Close
# =========================================================

figure.close()

print(
    "Figure generated successfully."
)