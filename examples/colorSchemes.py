"""Compare categorical color schemes.

Run from anywhere:

    graphPlot examples/colorSchemes.py
"""

import numpy as np
from figureSettings import project

import graphplot as gp

x = np.linspace(0.0, 1.0, 120)

for scheme, suffix in (
    ("colorblind", "Colorblind"),
    ("grayscale", "Grayscale"),
    ("blackwhite", "BlackWhite"),
):
    style = gp.Style.from_preset("paper", color_scheme=scheme)
    fig = project.figure(style=style)
    fig.line(x, np.sin(2 * np.pi * x), label="Case 1")
    fig.line(x, np.cos(2 * np.pi * x), label="Case 2")
    fig.line(x, np.sin(4 * np.pi * x), label="Case 3")
    fig.xlabel("$x$", unit="m")
    fig.ylabel("$u$", unit="m/s")
    fig.legend(loc="best")
    project.save(fig, f"colorSchemes{suffix}")
    fig.close()
