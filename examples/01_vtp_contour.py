"""VTP contour with a publication colorbar.

Run from the repository root:

    python examples/01_vtp_contour.py
"""

import graphplot as gp

fig = (
    gp.Figure(width=3.4, height=3.0)
    .contour("data/zNormal.vtp", "gammaDV", levels=32, cmap="viridis")
    .xlabel("$x$", unit="m")
    .ylabel("$y$", unit="m")
)

fig.colorbar(label=r"$\gamma_{\mathrm{DV}}$ [1/s]")
fig.save("output/01_vtp_contour", formats=["png", "pdf_tex"])
fig.close()
