"""Tabular comparison of reference and present work for several parameters.

Rows  : T = 0, 10, 20, 30
Columns: Reference, Present work

The same ``zNormal.vtp`` is used in every panel as a placeholder. Replace each
contour call with the corresponding case file when the real data is available.
Run from anywhere:

    graphPlot examples/comparisonTable.py
"""

from figureSettings import comparison

import graphplot as gp

DATA = gp.load("data/zNormal.vtp")
values = DATA.field("gammaDV")
vmin = float(values.min())
vmax = float(values.max())

temperatures = (0, 10, 20, 30)
fig = comparison.figure(
    nrows=len(temperatures),
    ncols=2,
    sharex=True,
    sharey=True,
)

contour = None
for row, temperature in enumerate(temperatures):
    for column, heading in enumerate(("Reference", "Present work")):
        panel = fig[row, column]
        panel.contour(
            DATA,
            "gammaDV",
            levels=24,
            vmin=vmin,
            vmax=vmax,
            cmap="viridis",
        )

        if row == 0:
            panel.title(heading)
        if column == 0:
            panel.ax.set_ylabel(rf"$T={temperature}$", labelpad=10)
        if row < len(temperatures) - 1:
            panel.ax.tick_params(labelbottom=False)
        if column > 0:
            panel.ax.tick_params(labelleft=False)

        contour = panel.last_mappable

fig.common_labels(x="$x$ [m]", y="$y$ [m]")
fig.colorbar(
    contour,
    axes=fig.panels_flat,
    label=r"$\gamma_{\mathrm{DV}}$ [1/s]",
    location="right",
    shrink=0.65,
    pad=0.02,
)
comparison.save(fig, "comparisonTable")
fig.close()
