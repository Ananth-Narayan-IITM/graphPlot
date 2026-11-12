"""VTP contour with a publication colorbar.

Run from anywhere:

    graphPlot examples/vtpContours.py
"""

from figureSettings import project

fig = (
    project.figure(height=3.0)
    .contour("data/zNormal.vtp", "gammaDV", levels=32, cmap="viridis")
    .xlabel("$x$", unit="m")
    .ylabel("$y$", unit="m")
)

fig.colorbar(label=r"$\gamma_{\mathrm{DV}}$ [1/s]")
project.save(fig, "vtpContours")
fig.close()
