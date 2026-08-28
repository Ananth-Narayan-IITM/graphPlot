import numpy as np

from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)


def test_two_horizontal_colorbars_can_be_created():

    figure_config = FigureConfig(
        width=7.0,
        height=8.0,
        dpi=600,
        aspect="equal",
    )

    figure = PublicationFigure(
        figure_config,
        nrows=2,
        ncols=2,
        sharex=True,
        sharey=True,
    )

    ax00 = figure.panel(
        0,
        0,
    )

    ax01 = figure.panel(
        0,
        1,
    )

    ax10 = figure.panel(
        1,
        0,
    )

    ax11 = figure.panel(
        1,
        1,
    )

    # -----------------------------------------------------
    # Create two independent scalar mappables
    # -----------------------------------------------------

    values_1 = np.linspace(
        0.0,
        1.0,
        100,
    )

    values_2 = np.linspace(
        0.0,
        10.0,
        100,
    )

    image_1 = ax00.imshow(
        values_1.reshape(10, 10),
        cmap="viridis",
        vmin=0.0,
        vmax=1.0,
    )

    image_2 = ax10.imshow(
        values_2.reshape(10, 10),
        cmap="plasma",
        vmin=0.0,
        vmax=10.0,
    )

    # -----------------------------------------------------
    # Layout first
    # -----------------------------------------------------

    figure.adjust_layout(
        left=0.09,
        right=0.97,
        bottom=0.17,
        top=0.97,
        wspace=0.08,
        hspace=0.42,
    )

    # -----------------------------------------------------
    # Dedicated colorbar axes
    # -----------------------------------------------------

    colorbar_ax_1 = figure.figure.add_axes(
        [
            0.20,
            0.45,
            0.60,
            0.018,
        ]
    )

    colorbar_ax_2 = figure.figure.add_axes(
        [
            0.20,
            0.08,
            0.60,
            0.018,
        ]
    )

    colorbar_1 = figure.figure.colorbar(
        image_1,
        cax=colorbar_ax_1,
        orientation="horizontal",
    )

    colorbar_2 = figure.figure.colorbar(
        image_2,
        cax=colorbar_ax_2,
        orientation="horizontal",
    )

    # -----------------------------------------------------
    # Assertions
    # -----------------------------------------------------

    assert colorbar_1.orientation == "horizontal"

    assert colorbar_2.orientation == "horizontal"

    assert colorbar_1.ax is colorbar_ax_1

    assert colorbar_2.ax is colorbar_ax_2

    # The two colorbars must occupy different
    # vertical positions.

    assert colorbar_ax_1.get_position().y0 != colorbar_ax_2.get_position().y0

    # -----------------------------------------------------
    # Close
    # -----------------------------------------------------

    figure.close()
