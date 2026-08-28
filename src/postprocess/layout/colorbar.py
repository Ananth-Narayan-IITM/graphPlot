from typing import Optional


def add_colorbar(
    figure,
    axes,
    mappable,
    label: Optional[str] = None,
    ticks=None,
    orientation="vertical",
    pad=0.02,
    fraction=0.046,
):
    """
    Add a colorbar to a figure.

    Parameters
    ----------
    figure
        Matplotlib figure.

    axes
        Matplotlib axes.

    mappable
        Scalar mappable returned by a plot.

    label
        Colorbar label.

    ticks
        Optional colorbar ticks.

    orientation
        "vertical" or "horizontal".

    pad
        Distance between axes and colorbar.

    fraction
        Fraction of axes occupied by colorbar.
    """

    colorbar = figure.colorbar(
        mappable,
        ax=axes,
        orientation=orientation,
        pad=pad,
        fraction=fraction,
    )

    if label is not None:
        colorbar.set_label(label)

    if ticks is not None:
        colorbar.set_ticks(ticks)

    return colorbar
