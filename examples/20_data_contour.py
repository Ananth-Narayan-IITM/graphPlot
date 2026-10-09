"""Example 20: filled contour from scattered tabular data.

Run from the repository root with:
    python examples/20_data_contour.py

The output is written to ``output/20_data_contour``.
"""

from pathlib import Path

from postprocess.io.tabular import read_table
from postprocess.layout.figure import FigureConfig, PublicationFigure
from postprocess.plots.dataContour import DataContourPlot

INPUT_FILE = "data/contour.dat"
OUTPUT_FILE = "output/20_data_contour"

# Read named columns from the whitespace-delimited table.
data = read_table(INPUT_FILE)

# Create the publication figure. A wide layout is useful for log-log contours.
figure = PublicationFigure(FigureConfig(width=6.2, height=4.8, aspect="auto"))

contour_plot = DataContourPlot(
    data,
    x="Ra",
    y="Pr",
    field="nusseltNumber",
    x_scale="log",
    y_scale="log",
    interpolation="linear",
    levels=25,
    cmap="plasma",
    # Optional: set a maximum triangle edge length in transformed coordinates.
    max_triangle_edge=None,
)

contour = contour_plot.plot(
    figure.axes,
    show_points=True,
    show_contour_lines=True,
    contour_labels=True,
)

figure.set_labels(xlabel=r"$Ra$", ylabel=r"$Pr$")
figure.add_colorbar(contour, label=r"$Nu$", labelpad=25)
figure.export(OUTPUT_FILE, formats=["png", "pdf_tex"])

print(f"Contour example completed: {OUTPUT_FILE}")
