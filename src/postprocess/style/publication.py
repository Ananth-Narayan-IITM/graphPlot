from dataclasses import dataclass

import matplotlib as mpl


@dataclass
class PublicationStyle:
    """
    Global publication plotting style.
    """

    font_size: float = 10.0

    axes_linewidth: float = 0.8
    tick_width: float = 0.8
    tick_length: float = 3.0

    line_width: float = 1.0

    use_latex: bool = True

    def apply(self):
        """
        Apply the publication style globally.
        """

        mpl.rcParams.update(
            {
                "font.size": self.font_size,

                "axes.labelsize": self.font_size,
                "axes.titlesize": self.font_size,

                "xtick.labelsize": self.font_size,
                "ytick.labelsize": self.font_size,

                "axes.linewidth": self.axes_linewidth,

                "xtick.major.width": self.tick_width,
                "ytick.major.width": self.tick_width,

                "xtick.major.size": self.tick_length,
                "ytick.major.size": self.tick_length,

                "lines.linewidth": self.line_width,

                "axes.grid": False,

                "text.usetex": self.use_latex,

                "pdf.fonttype": 42,
                "ps.fonttype": 42,
            }
        )