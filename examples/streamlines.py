"""Streamlines from a velocity field.

Run from anywhere:

    graphPlot examples/streamlines.py
"""

from figureSettings import project

import graphplot as gp

DATA = gp.load("data/zNormal.vtp")

fig = project.figure(height=3.0)
fig.mesh(DATA, edgecolor="0.8", linewidth=0.06, alpha=0.35)
fig.streamlines(
    DATA,
    "U",
    seed_axis="y",
    seed_position=2.5,
    n_seeds=16,
    integration_direction="both",
    color="black",
    linewidth=0.7,
    arrowsize=0.9,
)
fig.xlabel("$x$", unit="m")
fig.ylabel("$y$", unit="m")

project.save(fig, "streamlines")
fig.close()
