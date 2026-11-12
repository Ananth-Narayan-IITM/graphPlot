"""VTP contour with a mesh overlay.

Run from anywhere:

    graphPlot examples/vtpContourMesh.py
"""

import graphplot as gp

fig = (
    gp.Figure(width=3.4, height=3.0)
    .contour("data/zNormal.vtp", "gammaDV", levels=32)
    .mesh("data/zNormal.vtp", linewidth=0.12, alpha=0.3)
    .xlabel("$x$", unit="m")
    .ylabel("$y$", unit="m")
)

fig.colorbar(label=r"$\gamma_{\mathrm{DV}}$ [1/s]")
fig.save("output/vtpContourMesh", formats=["png", "pdf_tex"])
fig.close()
