import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from postprocess.io.vtp import read_vtp
from postprocess.plots.contour import (
    ContourPlot,
)

INPUT_FILE = "data/zNormal.vtp"


def test_contour_creation():

    data = read_vtp(INPUT_FILE)

    plot = ContourPlot(
        data,
        field="gammaDV",
    )

    assert plot.field == "gammaDV"

    assert plot.values is not None


def test_contour_plot():

    data = read_vtp(INPUT_FILE)

    plot = ContourPlot(
        data,
        field="gammaDV",
    )

    figure, axes = plt.subplots()

    collection = plot.plot(axes)

    assert collection is not None

    assert collection in (axes.collections)

    plt.close(figure)
