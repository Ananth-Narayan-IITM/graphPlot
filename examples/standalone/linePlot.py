"""Standalone line plot — no figureSettings.py needed.

Run from the repository root:

    graphPlot examples/standalone/linePlot.py
"""

import numpy as np

import graphplot as gp

x = np.linspace(0.0, 1.0, 120)

fig = gp.Figure(width=3.4, height=2.6)
fig.line(x, np.sin(2 * np.pi * x), label="Numerical", role="numerical")
fig.line(x, np.cos(2 * np.pi * x), label="Analytical", role="analytical")
fig.xlabel("$x$", unit="m")
fig.ylabel("$u$", unit="m/s")
fig.legend(loc="best")

fig.save("output/standalone/linePlot", formats=["png", "pdf_tex"])
fig.close()
