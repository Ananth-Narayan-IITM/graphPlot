"""Standalone velocity-vector plot — no figureSettings.py needed.

Run from the repository root:

    graphPlot examples/standalone/velocityVectors.py
"""

import graphplot as gp

data = gp.load("data/zNormal.vtp")

fig = gp.Figure(width=3.4, height=3.0)
fig.mesh(data, edgecolor="0.8", linewidth=0.06, alpha=0.35)
fig.vectors(
    data,
    "U",
    density=18,
    length=0.12,
    min_magnitude=0.03,
    color="black",
    width=0.002,
)
fig.xlabel("$x$", unit="m")
fig.ylabel("$y$", unit="m")

fig.save("output/standalone/velocityVectors", formats=["png", "pdf_tex"])
fig.close()
