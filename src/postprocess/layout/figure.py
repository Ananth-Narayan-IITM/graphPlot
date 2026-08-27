from dataclasses import dataclass
from typing import Optional, Tuple

import matplotlib.pyplot as plt


@dataclass
class FigureConfig:
    """
    Configuration for publication figures.
    """

    width: float = 3.5
    height: float = 2.8

    dpi: int = 300

    aspect: str = "equal"

    xlim: Optional[Tuple[float, float]] = None
    ylim: Optional[Tuple[float, float]] = None


class PublicationFigure:
    """
    Wrapper around a Matplotlib figure.
    """

    def __init__(self, config: FigureConfig):

        self.config = config

        self.figure, self.axes = plt.subplots(
            figsize=(config.width, config.height),
            dpi=config.dpi,
        )

        self.axes.set_aspect(config.aspect)

        if config.xlim is not None:
            self.axes.set_xlim(config.xlim)

        if config.ylim is not None:
            self.axes.set_ylim(config.ylim)

    def save(self, filename: str):

        self.figure.savefig(
            filename,
            bbox_inches="tight",
        )

    def close(self):

        plt.close(self.figure)