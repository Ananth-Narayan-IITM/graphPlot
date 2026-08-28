"""
Example 16 — Multi-panel CFD Comparison
========================================

Demonstrates a 2x2 publication-quality CFD figure.

Panels:

    (a) Contour
    (b) Contour + mesh
    (c) Contour + velocity vectors
    (d) Contour + streamlines

Demonstrates:

    - Multiple panels
    - Shared X/Y axes
    - Panel labels
    - Common axis labels
    - Shared horizontal colorbar
    - Consistent contour scale
    - Contour + mesh + vectors + streamlines
    - Publication-quality export
"""

from pathlib import Path

from postprocess.io.vtp import read_vtp

from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)

from postprocess.layout.colors import (
    ColorScale,
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

print(f"Reading: {data.filename}")

print(f"Points:  {data.n_points}")

print(f"Cells:   {data.n_cells}")

print(f"Bounds:  {data.bounds}")


# =========================================================
# Figure configuration
# =========================================================

figure_config = FigureConfig(
    width=7.0,
    height=7.0,
    dpi=600,
    aspect="equal",
)


# =========================================================
# Create figure
# =========================================================

figure = PublicationFigure(
    figure_config,
    nrows=2,
    ncols=2,
    sharex=True,
    sharey=True,
)


# =========================================================
# Get panels
# =========================================================

ax00 = figure.panel(
    0,
    0,
)

ax01 = figure.panel(
    0,
    1,
)

ax10 = figure.panel(
    1,
    0,
)

ax11 = figure.panel(
    1,
    1,
)


# =========================================================
# Geometry limits
# =========================================================

x_min, x_max, y_min, y_max = data.mesh.bounds


# =========================================================
# Common color scale
# =========================================================

values = data.get_field(
    "gammaDV",
    "cell",
)

color_scale = ColorScale(
    levels=20,
)

color_scale.resolve(values)


# =========================================================
# Panel (a)
# =========================================================

contour_a_plot = ContourPlot(
    data,
    field="gammaDV",
    association="cell",
)

contour_a = contour_a_plot.plot(
    ax00,
    scale=color_scale,
)

assert contour_a is not None


# =========================================================
# Panel (b)
# =========================================================

contour_b_plot = ContourPlot(
    data,
    field="gammaDV",
    association="cell",
)

contour_b = contour_b_plot.plot(
    ax01,
    scale=color_scale,
)

assert contour_b is not None


# ---------------------------------------------------------
# Mesh
# ---------------------------------------------------------

mesh_b_plot = MeshPlot(data)

mesh_b = mesh_b_plot.plot(
    ax01,
    edgecolor="black",
    facecolor="none",
    linewidth=0.15,
    alpha=0.35,
)

assert mesh_b is not None


# =========================================================
# Panel (c)
# =========================================================

contour_c_plot = ContourPlot(
    data,
    field="gammaDV",
    association="cell",
)

contour_c = contour_c_plot.plot(
    ax10,
    scale=color_scale,
)

assert contour_c is not None


# ---------------------------------------------------------
# Velocity vectors
# ---------------------------------------------------------

vector_c_plot = VectorPlot(
    data,
    field="U",
    association="cell",
)

vectors_c = vector_c_plot.plot(
    ax10,
    density=18,
    scale=25,
    width=0.002,
    color="black",
    alpha=0.85,
    normalize=True,
    pivot="mid",
    zorder=5,
)

assert vectors_c is not None


# =========================================================
# Panel (d)
# =========================================================

contour_d_plot = ContourPlot(
    data,
    field="gammaDV",
    association="cell",
)

contour_d = contour_d_plot.plot(
    ax11,
    scale=color_scale,
)

assert contour_d is not None


# ---------------------------------------------------------
# Streamlines
# ---------------------------------------------------------

streamline_d_plot = StreamlinePlot(
    data,
    field="U",
    association="cell",
)

streamlines_d = streamline_d_plot.plot(
    ax11,
    n_seeds=20,
    seed_axis="y",
    seed_position=None,
    seed_margin=0.02,
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
    color="black",
    linewidth=0.8,
    arrowsize=1.0,
    zorder=6,
)

assert streamlines_d is not None


# =========================================================
# Common axis limits
# =========================================================

for ax in (
    ax00,
    ax01,
    ax10,
    ax11,
):
    ax.set_xlim(
        x_min,
        x_max,
    )

    ax.set_ylim(
        y_min,
        y_max,
    )

    ax.set_aspect(
        "equal",
        adjustable="box",
    )

    ax.grid(False)


# =========================================================
# Panel labels
# =========================================================

figure.label_panels(
    labels=[
        "(a)",
        "(b)",
        "(c)",
        "(d)",
    ],
    x=0.02,
    y=0.97,
    fontsize=10,
)


# =========================================================
# Common axis labels
# =========================================================

# figure.set_common_xlabel(
#     r"$x\;(\mathrm{m})$",
#     x=0.5,
#     y=0.13,
# )
# figure.set_common_ylabel(
#     r"$y\;(\mathrm{m})$",
#     x=0.025,
#     y=0.5,
# )


# =========================================================
# Shared horizontal colorbar
# =========================================================

colorbar = figure.add_shared_colorbar(
    contour_a,
    axes=[
        ax00,
        ax01,
        ax10,
        ax11,
    ],
    label=r"$\gamma_{\mathrm{DV}}$",
    orientation="horizontal",
    fraction=0.045,
    pad=0.08,
    shrink=0.75,
)

assert colorbar is not None


# =========================================================
# Layout
# =========================================================

figure.adjust_layout(
    left=0.09,
    right=0.97,
    bottom=0.2,
    top=0.97,
    wspace=0.08,
    hspace=0.08,
)


# =========================================================
# Export
# =========================================================

OUTPUT_FILE = "output/example_16_multipanel_cfd_comparison"

figure.export(
    OUTPUT_FILE,
    formats=[
        "png",
        # "pdf_tex",
    ],
)


# =========================================================
# Close
# =========================================================

figure.close()


print("Example 16 completed successfully.")
