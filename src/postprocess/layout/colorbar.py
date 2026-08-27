import matplotlib.pyplot as plt
from typing import Optional

def add_colorbar(
    figure,
    axes,
    contour,
    label: Optional[str] = None,
    ticks=None,
):

    colorbar = figure.colorbar(
        contour,
        ax=axes,
        pad=0.02,
    )

    if label is not None:
        colorbar.set_label(label)

    if ticks is not None:
        colorbar.set_ticks(ticks)

    return colorbar