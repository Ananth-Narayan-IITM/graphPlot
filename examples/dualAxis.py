"""Dual y-axis plot with a table-style legend.

Run from anywhere:

    graphPlot examples/dualAxis.py
"""

import numpy as np

import graphplot as gp

x = np.linspace(0.0, 1.0, 150)
temperature = 300.0 + 40.0 * np.sin(2 * np.pi * x)
pressure = 100.0 + 20.0 * np.cos(2 * np.pi * x)

fig = gp.Figure(width=3.6, height=3.0, layout=None)
left = fig.line(x, temperature, label="Case 1", color="black")
right = fig.twinx().line(x, pressure, label="Case 1", color="#D55E00")

left.xlabel("$x$", unit="m")
left.ylabel("$T$", unit="K")
right.ylabel("$p$", unit="Pa")

left.legend_table(
    {
        "Temperature": {"Case 1": left.last_artist},
        "Pressure": {"Case 1": right.last_artist},
    },
    bbox_to_anchor=(0.5, 0.0),
)
fig.subplots_adjust(left=0.20, right=0.80, bottom=0.30, top=0.96)
fig.save("output/dualAxis", formats=["png", "pdf_tex"])
fig.close()
