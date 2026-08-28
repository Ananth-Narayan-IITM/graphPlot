"""
Tutorial: Multi-panel publication figure
========================================

Demonstrates:

1. Creating a 2 x 2 publication figure.
2. Accessing individual panels.
3. Shared axes.
4. Figure-level x/y labels.
5. Automatic panel labels.
"""


# =========================================================
# Imports
# =========================================================

import numpy as np

from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)


# =========================================================
# Figure configuration
# =========================================================

figure_config = FigureConfig(
    width=6.8,
    height=5.0,
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
# Access panels
# =========================================================

ax00 = figure.panel(0, 0)
ax01 = figure.panel(0, 1)
ax10 = figure.panel(1, 0)
ax11 = figure.panel(1, 1)


# =========================================================
# Generate data
# =========================================================

x = np.linspace(
    0.0,
    2.0,
    100,
)


# =========================================================
# Plot
# =========================================================

ax00.plot(
    x,
    x**2,
)

ax01.plot(
    x,
    2.0 * x,
)

ax10.plot(
    x,
    2.0 - x,
)

ax11.plot(
    x,
    np.ones_like(x),
)


# =========================================================
# Panel labels
# =========================================================

figure.label_panels()


# =========================================================
# Common axis labels
# =========================================================

figure.set_common_xlabel(
    r"$x$"
)

figure.set_common_ylabel(
    r"$f(x)$"
)


# =========================================================
# Layout
# =========================================================

figure.adjust_layout(
    left=0.12,
    right=0.96,
    bottom=0.12,
    top=0.96,
    wspace=0.08,
    hspace=0.08,
)


# =========================================================
# Export
# =========================================================

figure.save(
    "output/tutorial_multipanel_labels"
)

print(
    "Multipanel figure generated successfully."
)