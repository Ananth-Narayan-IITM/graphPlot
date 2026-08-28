"""
Tutorial: Shared colorbar
=========================

Demonstrates how multiple panels can share
one colorbar using PublicationFigure.
"""

import numpy as np
import matplotlib.pyplot as plt

from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)


# =========================================================
# Figure configuration
# =========================================================

figure_config = FigureConfig(
    width=6.8,
    height=3.4,
)


# =========================================================
# Create figure
# =========================================================

figure = PublicationFigure(
    figure_config,
    nrows=1,
    ncols=2,
)


# =========================================================
# Get panels
# =========================================================

ax0 = figure.panel(0, 0)
ax1 = figure.panel(0, 1)


# =========================================================
# Create example data
# =========================================================

x = np.linspace(
    0.0,
    5.0,
    100,
)

y = np.linspace(
    0.0,
    5.0,
    100,
)

X, Y = np.meshgrid(
    x,
    y,
)

Z = np.sin(X) * np.cos(Y)

Z2 = np.cos(X) * np.sin(Y)


# =========================================================
# Create contours
# =========================================================

contour0 = ax0.contourf(
    X,
    Y,
    Z,
    levels=20,
    cmap="viridis",
    vmin=-1.0,
    vmax=1.0,
)

contour1 = ax1.contourf(
    X,
    Y,
    Z2,
    levels=20,
    cmap="viridis",
    vmin=-1.0,
    vmax=1.0,
)


# =========================================================
# Panel labels
# =========================================================

figure.label_panels()


# =========================================================
# Common labels
# =========================================================

figure.set_common_xlabel(
    r"$x$"
)

figure.set_common_ylabel(
    r"$y$"
)


# =========================================================
# Shared colorbar
# =========================================================

figure.add_shared_colorbar(
    contour0,
    axes=[
        ax0,
        ax1,
    ],
    orientation="horizontal",
    label=r"$\gamma_{\mathrm{DV}}$",
)
# =========================================================
# Layout
# =========================================================

figure.adjust_layout(
    left=0.10,
    right=0.90,
    bottom=0.14,
    top=0.94,
    wspace=0.08,
)


# =========================================================
# Export
# =========================================================

figure.save(
    "output/tutorial_shared_colorbar"
)

print(
    "Shared-colorbar figure generated successfully."
)