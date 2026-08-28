import matplotlib.pyplot as plt
import numpy as np

from postprocess.data.data1d import Data1D
from postprocess.plots.line import LinePlot


def test_grouped_legend_two_columns():

    x = np.linspace(
        0.0,
        1.0,
        20,
    )

    data = []

    for i in range(6):
        data.append(
            Data1D(
                x=x,
                y=x + i,
            )
        )

    line_plot = LinePlot()

    line_plot.add(
        data[0],
        label="Experiment 1",
        role="experimental",
    )

    line_plot.add(
        data[1],
        label="Experiment 2",
        role="experimental",
    )

    line_plot.add(
        data[2],
        label="Experiment 3",
        role="experimental",
    )

    line_plot.add(
        data[3],
        label="Case 1",
        role="numerical",
    )

    line_plot.add(
        data[4],
        label="Case 2",
        role="numerical",
    )

    line_plot.add(
        data[5],
        label="Case 3",
        role="numerical",
    )

    figure, axes = plt.subplots()

    line_plot.plot(axes)

    legend = line_plot.legend(
        axes,
        ncol=2,
        groups=[
            {
                "title": "Experiment",
                "labels": [
                    "Experiment 1",
                    "Experiment 2",
                    "Experiment 3",
                ],
            },
            {
                "title": "Numerical",
                "labels": [
                    "Case 1",
                    "Case 2",
                    "Case 3",
                ],
            },
        ],
    )

    assert legend is not None

    # Six datasets + two group headings.
    assert len(legend.legend_handles) == 8

    plt.close(figure)


def test_grouped_legend_preserves_groups_and_markers():

    # -----------------------------------------------------
    # Data
    # -----------------------------------------------------

    x = np.linspace(
        0.0,
        1.0,
        20,
    )

    data_1 = Data1D(
        x=x,
        y=np.sin(2.0 * np.pi * x),
    )

    data_2 = Data1D(
        x=x,
        y=np.cos(2.0 * np.pi * x),
    )

    data_3 = Data1D(
        x=x,
        y=2.0 * np.sin(2.0 * np.pi * x),
    )

    data_4 = Data1D(
        x=x,
        y=2.0 * np.cos(2.0 * np.pi * x),
    )

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure, axes = plt.subplots()

    # -----------------------------------------------------
    # Temperature
    # -----------------------------------------------------

    temperature_plot = LinePlot()

    temperature_plot.add(
        data_1,
        label="Case 1",
        color="black",
        linestyle="-",
        marker=None,
    )

    temperature_plot.add(
        data_2,
        label="Case 2",
        color="red",
        linestyle="None",
        marker="s",
    )

    temperature_lines = temperature_plot.plot(axes)

    # -----------------------------------------------------
    # Pressure
    # -----------------------------------------------------

    pressure_plot = LinePlot()

    pressure_plot.add(
        data_3,
        label="Case 1",
        color="black",
        linestyle="-",
        marker=None,
    )

    pressure_plot.add(
        data_4,
        label="Case 2",
        color="red",
        linestyle="None",
        marker="s",
    )

    pressure_lines = pressure_plot.plot(axes)

    # -----------------------------------------------------
    # Group definition
    # -----------------------------------------------------

    groups = {
        "Temperature": {
            "Case 1": temperature_lines[0],
            "Case 2": temperature_lines[1],
        },
        "Pressure": {
            "Case 1": pressure_lines[0],
            "Case 2": pressure_lines[1],
        },
    }

    # -----------------------------------------------------
    # Create grouped legend
    # -----------------------------------------------------

    legend = temperature_plot.legend_table(
        axes,
        groups,
        location="lower center",
        bbox_to_anchor=(
            0.5,
            -0.05,
        ),
        fontsize=8,
    )

    # -----------------------------------------------------
    # Legend must be created
    # -----------------------------------------------------

    assert legend is not None

    # -----------------------------------------------------
    # Verify groups
    # -----------------------------------------------------

    assert list(groups.keys()) == [
        "Temperature",
        "Pressure",
    ]

    assert list(groups["Temperature"].keys()) == [
        "Case 1",
        "Case 2",
    ]

    assert list(groups["Pressure"].keys()) == [
        "Case 1",
        "Case 2",
    ]

    # -----------------------------------------------------
    # Verify line handles
    # -----------------------------------------------------

    assert temperature_lines[0].get_marker() in (None, "None")

    assert pressure_lines[0].get_marker() in (None, "None")

    # -----------------------------------------------------
    # Verify marker handles
    # -----------------------------------------------------

    assert temperature_lines[1].get_marker() == "s"

    assert pressure_lines[1].get_marker() == "s"

    # -----------------------------------------------------
    # Verify legend was attached to the figure
    # -----------------------------------------------------

    assert legend in (axes.figure.artists)

    plt.close(figure)


def test_final_validation_comparison():

    import numpy as np

    from postprocess.data.data1d import (
        Data1D,
    )
    from postprocess.plots.line import (
        LinePlot,
    )
    from postprocess.style.publication import (
        PublicationStyle,
    )

    x_numerical = np.linspace(
        0.0,
        1.0,
        20,
    )

    y_numerical = np.sin(x_numerical)

    x_experiment = np.linspace(
        0.0,
        1.0,
        10,
    )

    y_experiment = np.sin(x_experiment)

    numerical = Data1D(
        x=x_numerical,
        y=y_numerical,
    )

    experiment = Data1D(
        x=x_experiment,
        y=y_experiment,
    )

    style = PublicationStyle(
        color_scheme="colorblind",
    )

    plot = LinePlot(
        style=style,
    )

    plot.add(
        numerical,
        label="Numerical",
    )

    plot.add(
        experiment,
        label="Experiment",
    )

    assert len(plot.datasets) == 2

    assert plot.datasets[0]["label"] == "Numerical"

    assert plot.datasets[1]["label"] == "Experiment"
