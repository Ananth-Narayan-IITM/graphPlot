"""Velocity vectors drawn as scaled arrows.

Run from anywhere:

    graphPlot examples/velocityVectors.py
"""

from figureSettings import project

import graphplot as gp

DATA = gp.load("data/zNormal.vtp")

fig = project.figure(height=3.0)
fig.mesh(DATA, edgecolor="0.8", linewidth=0.06, alpha=0.35)
fig.vectors(
    DATA,
    "U",
    density=18,
    length=0.12,
    min_magnitude=0.03,
    color="black",
    width=0.002,
)
fig.xlabel("$x$", unit="m")
fig.ylabel("$y$", unit="m")

project.save(fig, "velocityVectors")
fig.close()
