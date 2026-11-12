"""VTP contour with a publication colorbar.

Run from anywhere:

    graphPlot examples/vtpContours.py
"""

import graphplot as gp

fig = (
    gp.Figure(width=3.4, height=3.0)
    .contour("data/zNormal.vtp", "gammaDV", levels=32, cmap="viridis")
    .xlabel("$x$", unit="m")
    .ylabel("$y$", unit="m")
)

fig.colorbar(label=r"$\gamma_{\mathrm{DV}}$ [1/s]")
fig.save("output/vtpContours", formats=["png", "pdf_tex"])
fig.close()
