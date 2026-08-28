"""
Tutorial: Scaling a 1D scientific dataset
==========================================

This example demonstrates:

1. Reading a 1D dataset from file.
2. Inspecting the Data1D object.
3. Scaling the x-coordinate.
4. Scaling the y-coordinate.
5. Chaining scale operations.
6. Confirming that the original dataset is unchanged.
7. Plotting the scaled dataset.
8. Exporting a publication-quality figure.
"""


# =========================================================
# Imports
# =========================================================

from postprocess.io.tabular import read_1d
from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)
from postprocess.plots.line import LinePlot
from postprocess.style import PublicationStyle

# =========================================================
# 1. Read the original dataset
# =========================================================

data = read_1d(
    "data/test_1d.dat",
    x_column=0,
    y_column=1,
    label="Original",
    x_label=r"$x$",
    y_label=r"$f(x)$",
    x_unit="m",
)


# =========================================================
# 2. Inspect the dataset
# =========================================================

print("\n" + "=" * 60)
print("Original dataset")
print("=" * 60)

print(data)

print("Number of points :", data.size)

print("x range          :", data.x_min, "to", data.x_max)

print("y range          :", data.y_min, "to", data.y_max)

print("x label          :", data.x_label)
print("y label          :", data.y_label)

print("x unit           :", data.x_unit)
print("y unit           :", data.y_unit)


# =========================================================
# 3. Scale x
# =========================================================
#
# x_scaled = x / L
#
# Here L = 0.5 m
#

L = 0.5

x_scaled = data.scale_x(
    L,
    label=r"$x/L$",
    unit=None,
)


print("\n" + "=" * 60)
print("After x scaling")
print("=" * 60)

print(x_scaled)

print("x label :", x_scaled.x_label)
print("x unit  :", x_scaled.x_unit)


# =========================================================
# 4. Scale y
# =========================================================
#
# y_scaled = y / Y_ref
#
# Here Y_ref = 1.0
#

Y_ref = 1.0

scaled = x_scaled.scale_y(
    Y_ref,
    label=r"$f/f_{\mathrm{ref}}$",
    unit=None,
)


print("\n" + "=" * 60)
print("After x and y scaling")
print("=" * 60)

print(scaled)

print("x label :", scaled.x_label)
print("y label :", scaled.y_label)

print("x unit  :", scaled.x_unit)
print("y unit  :", scaled.y_unit)


# =========================================================
# 5. Verify that original data is unchanged
# =========================================================

print("\n" + "=" * 60)
print("Original dataset after scaling")
print("=" * 60)

print("x range :", data.x_min, "to", data.x_max)

print("y range :", data.y_min, "to", data.y_max)

print("Original x label :", data.x_label)
print("Original y label :", data.y_label)


# =========================================================
# 6. Create publication figure
# =========================================================

figure_config = FigureConfig(
    width=3.4,
    height=2.6,
)

figure = PublicationFigure(figure_config)


# =========================================================
# 7. Publication style
# =========================================================

style = PublicationStyle(color_scheme="colorblind")


# =========================================================
# 8. Plot
# =========================================================

plot = LinePlot(style=style)

plot.add(
    scaled,
    label="Scaled data",
    role="numerical",
)

plot.plot(figure.axes)


# =========================================================
# 9. Axis labels
# =========================================================

figure.axes.set_xlabel(scaled.x_label)

figure.axes.set_ylabel(scaled.y_label)


# =========================================================
# 10. Export
# =========================================================

figure.save("output/scaling_1d")


print("\nFigure generated successfully.")
print("Output: output/scaling_1d")
