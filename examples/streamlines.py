"""Streamlines over a scalar contour.

Run from anywhere:

    graphPlot examples/streamlines.py
"""

from figureSettings import project

import graphplot as gp

DATA = gp.load("data/zNormal.vtp")

fig = project.figure(height=3.0)
fig.contour(
    DATA,
    "gammaDV",
    levels=24,
    cmap="Blues",
    alpha=0.55,
)
fig.streamlines(
    DATA,
    "U",
    seed_axis="y",
    seed_position=2.5,
    n_seeds=28,
    integration_direction="both",
    color="black",
    linewidth=0.55,
    arrowsize=0.9,
)
fig.colorbar(label=r"$\gamma_{\mathrm{DV}}$ [1/s]")
fig.xlabel("$x$", unit="m")
fig.ylabel("$y$", unit="m")

project.save(fig, "streamlines")
fig.close()
