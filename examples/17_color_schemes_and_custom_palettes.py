"""
Example 17 — Color Schemes and Custom Palettes
================================================

Demonstrates:

    1. Default categorical line colors
    2. Colorblind-safe categorical colors
    3. Grayscale colors
    4. Black-and-white styling
    5. User-defined categorical palette
    6. User-defined contour colormap

The example intentionally separates:

    Line colors
        -> PublicationStyle

    Contour colors
        -> ColorScale / Matplotlib colormap
"""

import numpy as np

from matplotlib.colors import LinearSegmentedColormap

from postprocess.data.data1d import Data1D

from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)

from postprocess.layout.colors import (
    ColorScale,
)

from postprocess.plots.line import (
    LinePlot,
)

from postprocess.style.publication import (
    PublicationStyle,
)


# =========================================================
# Data
# =========================================================

x = np.linspace(
    0.0,
    1.0,
    100,
)

datasets = [
    Data1D(
        x=x,
        y=np.sin(2.0 * np.pi * x),
        label="Case 1",
    ),
    Data1D(
        x=x,
        y=np.cos(2.0 * np.pi * x),
        label="Case 2",
    ),
    Data1D(
        x=x,
        y=np.sin(4.0 * np.pi * x),
        label="Case 3",
    ),
]


# =========================================================
# Custom categorical palette
# =========================================================

custom_palette = [
    "#264653",
    "#2A9D8F",
    "#E9C46A",
    "#F4A261",
    "#E76F51",
]


# =========================================================
# Figure
# =========================================================

figure_config = FigureConfig(
    width=7.0,
    height=7.0,
    dpi=600,
)

figure = PublicationFigure(
    figure_config,
    nrows=3,
    ncols=2,
    sharex=True,
)


# =========================================================
# Helper
# =========================================================


def add_line_example(
    axes,
    color_scheme,
    title,
):
    """
    Plot the same datasets using a particular
    categorical color scheme.
    """

    style = PublicationStyle(
        color_scheme=color_scheme,
        line_scheme="publication",
        marker_scheme="publication",
    )

    plot = LinePlot(
        style=style,
    )

    for data in datasets:
        plot.add(
            data,
            label=data.label,
            linewidth=1.5,
        )

    artists = plot.plot(axes)

    assert len(artists) == 3

    axes.set_title(
        title,
        fontsize=9,
    )

    axes.set_ylabel(r"$f(x)$")

    axes.grid(False)

    plot.legend(
        axes,
        location="best",
        frameon=False,
        fontsize=7,
    )

    return artists


# =========================================================
# Panel (a) — Default
# =========================================================

add_line_example(
    figure.panel(0, 0),
    "default",
    "Default",
)


# =========================================================
# Panel (b) — Colorblind
# =========================================================

add_line_example(
    figure.panel(0, 1),
    "colorblind",
    "Colorblind-safe",
)


# =========================================================
# Panel (c) — Grayscale
# =========================================================

add_line_example(
    figure.panel(1, 0),
    "grayscale",
    "Grayscale",
)


# =========================================================
# Panel (d) — Black and white
# =========================================================

style_bw = PublicationStyle(
    color_scheme="blackwhite",
    line_scheme="publication",
    marker_scheme="publication",
)

plot_bw = LinePlot(
    style=style_bw,
)

for data in datasets:
    plot_bw.add(
        data,
        label=data.label,
        linewidth=1.5,
    )

artists_bw = plot_bw.plot(figure.panel(1, 1))

assert len(artists_bw) == 3

figure.panel(
    1,
    1,
).set_title(
    "Black and white",
    fontsize=9,
)

plot_bw.legend(
    figure.panel(1, 1),
    location="best",
    frameon=False,
    fontsize=7,
)


# =========================================================
# Panel (e) — Custom palette
# =========================================================

style_custom = PublicationStyle(
    color_scheme=custom_palette,
    line_scheme="publication",
    marker_scheme="publication",
)

plot_custom = LinePlot(
    style=style_custom,
)

for data in datasets:
    plot_custom.add(
        data,
        label=data.label,
        linewidth=1.5,
    )

artists_custom = plot_custom.plot(figure.panel(2, 0))

assert len(artists_custom) == 3

figure.panel(
    2,
    0,
).set_title(
    "Custom categorical palette",
    fontsize=9,
)

plot_custom.legend(
    figure.panel(2, 0),
    location="best",
    frameon=False,
    fontsize=7,
)


# =========================================================
# Panel (f) — Custom contour colormap
# =========================================================

ax = figure.panel(
    2,
    1,
)

# ---------------------------------------------------------
# Create a custom sequential colormap
# ---------------------------------------------------------

custom_cmap = LinearSegmentedColormap.from_list(
    "my_cfd_palette",
    [
        "#132B43",
        "#1F77B4",
        "#2A9D8F",
        "#E9C46A",
        "#E76F51",
    ],
)


# ---------------------------------------------------------
# Demonstration image
# ---------------------------------------------------------

field = np.outer(
    np.sin(np.pi * x),
    np.sin(np.pi * x),
)

image = ax.imshow(
    field,
    origin="lower",
    extent=[
        0.0,
        1.0,
        0.0,
        1.0,
    ],
    cmap=custom_cmap,
    aspect="equal",
)

ax.set_title(
    "Custom contour colormap",
    fontsize=9,
)

ax.set_xlabel(r"$x$")

ax.set_ylabel(r"$y$")

ax.grid(False)


# =========================================================
# Custom contour colorbar
# =========================================================

colorbar = figure.add_shared_colorbar(
    image,
    axes=[
        ax,
    ],
    label=r"$\phi$",
    orientation="horizontal",
    fraction=0.05,
    pad=0.12,
    shrink=0.75,
)

assert colorbar is not None


# =========================================================
# Panel labels
# =========================================================

figure.label_panels(
    labels=[
        "(a)",
        "(b)",
        "(c)",
        "(d)",
        "(e)",
        "(f)",
    ],
    x=0.02,
    y=0.97,
    fontsize=10,
)


# =========================================================
# Common X label
# =========================================================

figure.set_common_xlabel(
    r"$x$",
    x=0.5,
    y=0.04,
)


# =========================================================
# Layout
# =========================================================

figure.adjust_layout(
    left=0.08,
    right=0.97,
    bottom=0.2,
    top=0.96,
    wspace=0.18,
    hspace=0.25,
)


# =========================================================
# Export
# =========================================================

figure.export(
    "output/example_17_color_schemes_and_custom_palettes",
    formats=[
        "png",
        # "pdf_tex",
    ],
)


figure.close()


print("Example 17 completed successfully.")
