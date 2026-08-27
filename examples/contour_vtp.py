from pathlib import Path

from postprocess.io.vtp import read_vtp

from postprocess.plots.contour import ContourPlot
from postprocess.plots.mesh import MeshPlot

from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)

from postprocess.layout.colorbar import add_colorbar

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

# ---------------------------------------------------------
# Visualization
# ---------------------------------------------------------

SHOW_CONTOURS = True
SHOW_MESH = True

# ---------------------------------------------------------
# Contour configuration
# ---------------------------------------------------------

LEVELS = 30
CMAP = "viridis"

VMIN = None
VMAX = None

# ---------------------------------------------------------
# Mesh configuration
# ---------------------------------------------------------

MESH_COLOR = "black"
MESH_LINEWIDTH = 0.25
MESH_ALPHA = 0.5

# ---------------------------------------------------------
# Figure configuration
# ---------------------------------------------------------

FIGURE_WIDTH = 3.5
FIGURE_HEIGHT = 2.8

ASPECT = "equal"

# ---------------------------------------------------------
# Labels
# ---------------------------------------------------------

X_LABEL = r"$x$ (m)"
Y_LABEL = r"$y$ (m)"

COLORBAR_LABEL = r"$\gamma_{\mathrm{DV}}$ (1/s)"


# =========================================================
# Publication style
# =========================================================

style = PublicationStyle(
    font_size=10,
    use_latex=True,
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
# Create figure
# =========================================================

figure_config = FigureConfig(
    width=FIGURE_WIDTH,
    height=FIGURE_HEIGHT,
    aspect=ASPECT,
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
        levels=LEVELS,
        cmap=CMAP,
        vmin=VMIN,
        vmax=VMAX,
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
# Axes labels
# =========================================================

figure.axes.set_xlabel(
    X_LABEL
)

figure.axes.set_ylabel(
    Y_LABEL
)


# =========================================================
# Colorbar
# =========================================================

if contour is not None:

    add_colorbar(
        figure.figure,
        figure.axes,
        contour,
        label=COLORBAR_LABEL,
    )


# =========================================================
# Export
# =========================================================

figure.save(
    OUTPUT_FILE.with_suffix(".png")
)

figure.save(
    OUTPUT_FILE.with_suffix(".pdf")
)


# =========================================================
# Close
# =========================================================

figure.close()

print(
    "Figure generated successfully."
)