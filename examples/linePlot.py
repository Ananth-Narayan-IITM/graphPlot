"""Numerical and experimental line comparison.

Run from anywhere:

    graphPlot examples/linePlot.py
"""

from pathlib import Path

import graphplot as gp

ROOT = Path(__file__).resolve().parents[1]

fig = (
    gp.Figure(width=3.4, height=2.6)
    .line(ROOT / "data" / "numerical.dat", label="Numerical", role="numerical")
    .line(ROOT / "data" / "experiment.dat", label="Experiment", role="experimental")
    .xlabel("$x$", unit="m")
    .ylabel("$u$", unit="m/s")
    .legend(loc="best")
)
fig.save(ROOT / "output" / "linePlot", formats=["png", "pdf_tex"])
fig.close()
