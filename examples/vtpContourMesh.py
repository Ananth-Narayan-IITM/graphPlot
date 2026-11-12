"""VTP contour with a mesh overlay.

Run from anywhere:

    graphPlot examples/vtpContourMesh.py
"""

from pathlib import Path

import graphplot as gp

ROOT = Path(__file__).resolve().parents[1]
VTP = ROOT / "data" / "zNormal.vtp"

fig = (
    gp.Figure(width=3.4, height=3.0)
    .contour(VTP, "gammaDV", levels=32)
    .mesh(VTP, linewidth=0.12, alpha=0.3)
    .xlabel("$x$", unit="m")
    .ylabel("$y$", unit="m")
)

fig.colorbar(label=r"$\gamma_{\mathrm{DV}}$ [1/s]")
fig.save(ROOT / "output" / "vtpContourMesh", formats=["png", "pdf_tex"])
fig.close()
