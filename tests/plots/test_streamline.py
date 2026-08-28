import numpy as np
import matplotlib.pyplot as plt

from postprocess.io.vtp import read_vtp
from postprocess.plots.streamline import StreamlinePlot


# =========================================================
# Test data
# =========================================================

INPUT_FILE = "data/zNormal.vtp"


def make_streamline_plot():

    data = read_vtp(
        INPUT_FILE
    )

    return StreamlinePlot(
        data,
        field="U",
    )


# =========================================================
# Creation
# =========================================================

def test_streamline_plot_creation():

    plot = make_streamline_plot()

    assert plot is not None
    assert plot.field == "U"


# =========================================================
# Streamline generation
# =========================================================

def test_streamline_generation():

    plot = make_streamline_plot()

    figure, axes = plt.subplots()

    plot.plot(
        axes,
        n_seeds=10,
        seed_axis="y",
        integration_direction="forward",
        integrator_type=45,
        surface_streamlines=True,
        color="black",
        linewidth=0.8,
        arrowsize=0,
    )

    # At least one streamline must have been
    # added to the axes.
    assert len(axes.lines) > 0

    # Every plotted streamline must contain
    # more than one point.
    for line in axes.lines:

        assert len(
            line.get_xdata()
        ) > 1

        assert len(
            line.get_ydata()
        ) > 1

    plt.close(figure)


# =========================================================
# Streamline styling
# =========================================================

def test_streamline_styling():

    plot = make_streamline_plot()

    figure, axes = plt.subplots()

    plot.plot(
        axes,
        n_seeds=10,
        color="red",
        linewidth=1.5,
        arrowsize=0,
    )

    assert len(axes.lines) > 0

    for line in axes.lines:

        assert line.get_color() == "red"

        assert np.isclose(
            line.get_linewidth(),
            1.5,
        )

    plt.close(figure)


# =========================================================
# Integration direction validation
# =========================================================

def test_invalid_integration_direction():

    plot = make_streamline_plot()

    figure, axes = plt.subplots()

    try:

        plot.plot(
            axes,
            integration_direction="invalid",
        )

    except ValueError as error:

        assert (
            "integration_direction"
            in str(error)
        )

    else:

        raise AssertionError(
            "Invalid integration direction "
            "did not raise ValueError."
        )

    plt.close(figure)


# =========================================================
# Integrator validation
# =========================================================

def test_invalid_integrator():

    plot = make_streamline_plot()

    figure, axes = plt.subplots()

    try:

        plot.plot(
            axes,
            integrator_type=99,
        )

    except ValueError as error:

        assert (
            "integrator_type"
            in str(error)
        )

    else:

        raise AssertionError(
            "Invalid integrator type "
            "did not raise ValueError."
        )

    plt.close(figure)