"""Grouped legend with numerical and experimental headings.

Run from the repository root:

    python examples/04_grouped_legend.py
"""

import numpy as np

import graphplot as gp

x = np.linspace(0.0, 1.0, 120)

fig = (
    gp.Figure(width=3.8, height=2.8)
    .line(x, np.sin(2 * np.pi * x), label="Case 1", role="numerical")
    .line(x, np.cos(2 * np.pi * x), label="Case 2", role="numerical")
    .line(
        x[::10], np.sin(2 * np.pi * x[::10]) + 0.02, label="Exp. 1", role="experimental"
    )
    .line(
        x[::10], np.cos(2 * np.pi * x[::10]) - 0.02, label="Exp. 2", role="experimental"
    )
    .xlabel("$x$", unit="m")
    .ylabel("$u$", unit="m/s")
)
fig.legend(
    groups=[
        {"title": "Numerical", "labels": ["Case 1", "Case 2"]},
        {"title": "Experiment", "labels": ["Exp. 1", "Exp. 2"]},
    ],
    ncol=2,
    loc="upper right",
)
fig.save("output/04_grouped_legend", formats=["png", "pdf_tex"])
fig.close()
