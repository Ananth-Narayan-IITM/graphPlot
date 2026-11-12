"""VTP contour with a mesh overlay.

Run from anywhere:

    graphPlot examples/vtpContourMesh.py
"""

from figureSettings import project

fig = (
    project.figure(height=3.0)
    .contour("data/zNormal.vtp", "gammaDV", levels=32)
    .mesh("data/zNormal.vtp", linewidth=0.12, alpha=0.3)
    .xlabel("$x$", unit="m")
    .ylabel("$y$", unit="m")
)

fig.colorbar(label=r"$\gamma_{\mathrm{DV}}$ [1/s]")
project.save(fig, "vtpContourMesh")
fig.close()
