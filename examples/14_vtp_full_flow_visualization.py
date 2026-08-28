"""
Example 14 — Full VTP Flow Visualization
=========================================

Demonstrates a publication-quality CFD figure combining:

    1. Cell-based contour
    2. Computational mesh
    3. Cell-based velocity vectors
    4. VTK streamlines
    5. Streamline direction arrows
    6. Transparent mesh overlay
    7. Publication-quality figure formatting
    8. PDF + PDF_TeX export

Layer order:

    contour
        ↓
    mesh
        ↓
    vectors
        ↓
    streamlines
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
    alpha=0.9,
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
    # -----------------------------------------------------
    # Seeding
    # -----------------------------------------------------
    n_seeds=20,
    seed_axis="y",
    seed_position=None,
    seed_margin=0.02,
    # -----------------------------------------------------
    # Integration
    # -----------------------------------------------------
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
    # -----------------------------------------------------
    # Appearance
    # -----------------------------------------------------
    color="black",
    linewidth=0.8,
    arrowsize=1.0,
    zorder=6,
)

assert streamlines is not None


# =========================================================
# Axes
# =========================================================

axes.set_xlabel(r"$x\;(\mathrm{m})$")

axes.set_ylabel(r"$y\;(\mathrm{m})$")


# =========================================================
# Limits
# =========================================================

x_min, x_max, y_min, y_max = data.mesh.bounds

axes.set_xlim(
    x_min,
    x_max,
)

axes.set_ylim(
    y_min,
    y_max,
)


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
# Layout
# =========================================================

figure.figure.tight_layout(
    pad=1.0,
)


# =========================================================
# Export
# =========================================================

figure.export(
    "output/example_14_vtp_full_flow_visualization",
    formats=[
        "png",
        # "pdf_tex",
    ],
)


print("Example 14 completed successfully.")
