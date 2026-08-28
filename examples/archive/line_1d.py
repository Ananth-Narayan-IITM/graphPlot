from postprocess.io.tabular import read_1d
from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)
from postprocess.plots.line import LinePlot
from postprocess.style import (
    LegendManager,
    PublicationStyle,
)

# =========================================================
# Read datasets
# =========================================================
legend = LegendManager()
numerical = read_1d(
    "data/numerical.dat",
    x_column=0,
    y_column=1,
    label="Numerical",
    x_label=r"$x$",
    y_label=r"$f(x)$",
    x_unit="m",
)

analytical = read_1d(
    "data/analytical.dat",
    x_column=0,
    y_column=1,
    label="Analytical",
    x_label=r"$x$",
    y_label=r"$f(x)$",
    x_unit="m",
)

experiment = read_1d(
    "data/experiment.dat",
    x_column=0,
    y_column=1,
    label="Experiment",
    x_label=r"$x$",
    y_label=r"$f(x)$",
    x_unit="m",
)

# =========================================================
# Figure configuration
# =========================================================

figure_config = FigureConfig(
    width=4.5,
    height=3.5,
)


# =========================================================
# Figure
# =========================================================

figure = PublicationFigure(figure_config)


# =========================================================
# Style
# =========================================================

style = PublicationStyle(color_scheme="colorblind")

# =========================================================
# Line plot
# =========================================================

plot = LinePlot(style=style)

plot.add(
    numerical,
    label="Numerical",
    role="numerical",
)

plot.add(
    analytical,
    label="Analytical",
    role="analytical",
)

plot.add_errorbar(
    experiment,
    y_error=0.02,
    label="Experiment",
    role="experimental",
)

plot.plot(figure.axes)

# =========================================================
# Axis labels
# =========================================================

figure.axes.set_xlabel(r"$x$ (m)")

figure.axes.set_ylabel(r"$f(x)$")


# =========================================================
# Legend
# =========================================================

plot.legend(
    figure.axes,
    location="lower left",
    frameon=False,
)


# =========================================================
# Grid
# =========================================================
legend.render(
    figure.axes,
    location="best",
    frameon=False,
    ncol=2,
)
# figure.axes.grid(
#     False
# )


# =========================================================
# Export
# =========================================================

figure.save(
    "output/test_1d_multiple",
)
