from pathlib import Path

from postprocess.io.vtp import read_vtp
from postprocess.layout.colors import (
    ColorScale,
)
from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)
from postprocess.plots.contour import ContourPlot
from postprocess.plots.mesh import MeshPlot
from postprocess.plots.streamline import StreamlinePlot
from postprocess.style.publication import (
    PublicationStyle,
)

# =========================================================
# Configuration
# =========================================================

INPUT_FILE = Path("data/zNormal.vtp")

FIELD = "gammaDV"

OUTPUT_FILE = Path(f"output/{FIELD}")


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

COLORBAR_LABEL = r"$\gamma$ (1/s)"


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

data = read_vtp(INPUT_FILE)

print(f"Reading: {data.filename}")

print(f"Points:  {data.n_points}")

print(f"Cells:   {data.n_cells}")

print(f"Bounds:  {data.bounds}")


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

figure = PublicationFigure(figure_config)


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
    mesh_plot = MeshPlot(data)

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
# Annotations
# =========================================================

# AnnotationPlot.add_text(
#     figure.axes,
#     x=2.5,
#     y=4.5,
#     text=r"$\mathrm{Test}$",
#     fontsize=10,
# )

# AnnotationPlot.add_arrow(
#     figure.axes,
#     start=(0.5, 2.5),
#     end=(1.5, 2.5),
#     linewidth=0.8,
# )

# AnnotationPlot.add_marker(
#     figure.axes,
#     position=(2.5, 2.5),
#     marker="o",
#     size=35,
# )

# AnnotationPlot.add_line(
#     figure.axes,
#     start=(0.5, 1.0),
#     end=(4.5, 1.0),
#     linewidth=0.8,
#     linestyle="--",
# )

# AnnotationPlot.add_rectangle(
#     figure.axes,
#     xy=(1.0, 1.8),
#     width=1.5,
#     height=1.0,
#     linewidth=0.8,
# )

# =========================================================
# Geometry overlay test
# =========================================================

# GeometryPlot.add_rectangle(
#     figure.axes,
#     xy=(0.0, 3.0),
#     width=1.5,
#     height=1.0,
#     linewidth=0.8,
# )

# GeometryPlot.add_polygon(
#     figure.axes,
#     points=[
#         (0.5, 2.0),
#         (1.0, 2.5),
#         (0.5, 3.0),
#     ],
#     linewidth=0.8,
# )

# GeometryPlot.add_line(
#     figure.axes,
#     start=(0.0, 2.5),
#     end=(5.0, 2.5),
#     linewidth=0.6,
#     linestyle="--",
# )

# GeometryPlot.add_dimension(
#     figure.axes,
#     start=(1.0, 1.0),
#     end=(4.0, 1.0),
#     offset=-0.25,
#     text=r"$L = 3$ m",
# )

# =========================================================
# Vector field
# =========================================================

# vector_plot = VectorPlot(
#     data,
#     field="U",
#     association="cell",
# )
# vector_plot.plot(
#     figure.axes,
#     density=20,
#     scale=20,
#     width=0.002,
#     color="black",
#     normalize=False,
# )

# =========================================================
# Streamlines
# =========================================================

streamline_plot = StreamlinePlot(
    data,
    field="U",
    association="cell",
)

streamline_plot.plot(
    figure.axes,
    n_seeds=50,
    seed_axis="y",
    seed_position=0.05,
    seed_margin=0.05,
    integration_direction="both",
    integrator_type=45,
    surface_streamlines=True,
    initial_step_length=0.05,
    min_step_length=0.005,
    max_step_length=0.25,
    max_steps=1000,
    max_length=10.0,
    interpolator_type="cell",
    color="blue",
    linewidth=0.8,
    arrowsize=1.0,
)
# =========================================================
# Export
# =========================================================

figure.export(
    OUTPUT_FILE,
    formats=[
        "png",
        # "pdf",
        # "pdf_tex",
    ],
)


# =========================================================
# Close
# =========================================================

figure.close()

print("Figure generated successfully.")
