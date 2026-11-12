"""Numerical and experimental line comparison.

Run from anywhere:

    graphPlot examples/linePlot.py
"""

import graphplot as gp

fig = (
    gp.Figure(width=3.4, height=2.6)
    .line("data/numerical.dat", label="Numerical", role="numerical")
    .line("data/experiment.dat", label="Experiment", role="experimental")
    .xlabel("$x$", unit="m")
    .ylabel("$u$", unit="m/s")
    .legend(loc="best")
)
fig.save("output/linePlot", formats=["png", "pdf_tex"])
fig.close()
