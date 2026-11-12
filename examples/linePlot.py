"""Numerical and experimental line comparison.

Run from anywhere:

    graphPlot examples/linePlot.py
"""

from figureSettings import project

fig = (
    project.figure()
    .line("data/numerical.dat", label="Numerical", role="numerical")
    .line("data/experiment.dat", label="Experiment", role="experimental")
    .xlabel("$x$", unit="m")
    .ylabel("$u$", unit="m/s")
    .legend(loc="best")
)
project.save(fig, "linePlot")
fig.close()
