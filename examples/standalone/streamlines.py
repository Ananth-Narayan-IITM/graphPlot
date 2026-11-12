"""Standalone streamlines — no figureSettings.py needed.

Run from the repository root:

    graphPlot examples/standalone/streamlines.py
"""

import graphplot as gp

data = gp.load("data/zNormal.vtp")

fig = gp.Figure(width=3.4, height=3.0)
fig.contour(data, "gammaDV", levels=24, cmap="Blues", alpha=0.55)
fig.streamlines(
    data,
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

fig.save("output/standalone/streamlines", formats=["png", "pdf_tex"])
fig.close()
