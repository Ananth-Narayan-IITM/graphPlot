"""Tabular contour with logarithmic axes, sample points and labels.

Run from anywhere:

    graphPlot examples/tabularContour.py
"""

from figureSettings import project

import graphplot as gp

data = gp.load("data/contour.dat")

fig = project.figure(width=4.2, height=3.4)
fig.contour(
    data,
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

project.save(fig, "tabularContour")
fig.close()
