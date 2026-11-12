"""Standalone tabular contour — no figureSettings.py needed.

Run from the repository root:

    graphPlot examples/standalone/tabularContour.py
"""

import graphplot as gp

table = gp.load("data/contour.dat")

fig = gp.Figure(width=4.2, height=3.4)
fig.contour(
    table,
    x="Ra",
    y="Pr",
    field="nusseltNumber",
    xscale="log",
    yscale="log",
    levels=8,
    cmap="plasma",
    show_points=True,
    show_lines=True,
    contour_labels=True,
    label_fontsize=7,
    line_width=0.6,
)
fig.xlabel("$Ra$")
fig.ylabel("$Pr$")
fig.colorbar(label="$Nu$")

fig.save("output/standalone/tabularContour", formats=["png", "pdf_tex"])
fig.close()
