from dataclasses import dataclass
from typing import Optional, Tuple
import numpy as np
import matplotlib.pyplot as plt

from postprocess.layout.colorbar import add_colorbar
from postprocess.export.latex import LaTeXTextRegistry


@dataclass
class FigureConfig:
    """
    Configuration for a publication figure.
    """

    width: float = 3.5

    height: Optional[float] = None
    height_ratio: float = 0.8

    dpi: int = 300

    aspect: str = "equal"

    xlim: Optional[Tuple[float, float]] = None
    ylim: Optional[Tuple[float, float]] = None

    show_grid: bool = False


class PublicationFigure:
    """
    Wrapper around a Matplotlib figure.

    Controls figure layout, axes, labels, colorbars,
    and export.
    """

    def __init__(
        self,
        config,
        nrows=1,
        ncols=1,
        sharex=False,
        sharey=False,
    ):

        self.config = config

        self._latex_artists = []
        self.latex_registry = LaTeXTextRegistry()

        self.nrows = nrows
        self.ncols = ncols

        width = float(config.width)

        if config.height is None:

            height = (
                width *
                float(config.height_ratio)
            )

        else:

            height = float(config.height)

        self.figure, axes = plt.subplots(
            nrows=nrows,
            ncols=ncols,
            figsize=(width, height),
            sharex=sharex,
            sharey=sharey,
        )

        self._axes_array = np.asarray(
            axes,
            dtype=object,
        )

        if nrows == 1 and ncols == 1:

            self._axes_array = (
                self._axes_array.reshape(1, 1)
            )

        elif nrows == 1:

            self._axes_array = (
                self._axes_array.reshape(1, ncols)
            )

        elif ncols == 1:

            self._axes_array = (
                self._axes_array.reshape(nrows, 1)
            )

        self.axes = axes

    def panel(
        self,
        row,
        column,
    ):
        """
        Return the axes corresponding to a panel.

        Parameters
        ----------
        row : int
            Zero-based row index.

        column : int
            Zero-based column index.

        Returns
        -------
        matplotlib.axes.Axes
            Requested panel.
        """

        if row < 0 or row >= self.nrows:
            raise IndexError(
                f"Panel row {row} is out of range."
            )

        if column < 0 or column >= self.ncols:
            raise IndexError(
                f"Panel column {column} is out of range."
            )

        return self._axes_array[row, column]
    def set_common_xlabel(
        self,
        label,
        x=0.5,
        y=0.02,
    ):
        """
        Add a common x-axis label for the entire figure.

        Parameters
        ----------
        label : str
            Common x-axis label.

        x : float, optional
            Horizontal figure coordinate.

        y : float, optional
            Vertical figure coordinate.
        """

        self.figure.text(
            x,
            y,
            label,
            ha="center",
            va="center",
        )
    def set_common_ylabel(
        self,
        label,
        x=0.02,
        y=0.5,
    ):
        """
        Add a common y-axis label for the entire figure.

        Parameters
        ----------
        label : str
            Common y-axis label.

        x : float, optional
            Horizontal figure coordinate.

        y : float, optional
            Vertical figure coordinate.
        """

        self.figure.text(
            x,
            y,
            label,
            ha="center",
            va="center",
            rotation="vertical",
        )
    def label_panels(
        self,
        labels=None,
        x=0.02,
        y=0.98,
        fontsize=None,
    ):
        """
        Add labels such as (a), (b), (c), ... to each panel.

        Parameters
        ----------
        labels : list, optional
            Custom panel labels.

        x : float, optional
            Position inside each axes in axes coordinates.

        y : float, optional
            Position inside each axes in axes coordinates.

        fontsize : float, optional
            Panel-label font size.
        """

        if labels is None:

            labels = []

            for i in range(
                self.nrows * self.ncols
            ):

                labels.append(
                    "({})".format(
                        chr(ord("a") + i)
                    )
                )

        expected = (
            self.nrows *
            self.ncols
        )

        if len(labels) != expected:

            raise ValueError(
                "Number of panel labels must "
                f"be {expected}."
            )

        index = 0

        for row in range(self.nrows):

            for column in range(self.ncols):

                ax = self.panel(
                    row,
                    column,
                )

                ax.text(
                    x,
                    y,
                    labels[index],
                    transform=ax.transAxes,
                    ha="left",
                    va="top",
                    fontsize=fontsize,
                )

                index += 1
    def adjust_layout(
        self,
        left=None,
        right=None,
        bottom=None,
        top=None,
        wspace=None,
        hspace=None,
    ):
        """
        Adjust spacing between figure panels.
        """

        self.figure.subplots_adjust(
            left=left,
            right=right,
            bottom=bottom,
            top=top,
            wspace=wspace,
            hspace=hspace,
        )
    def add_shared_colorbar(
        self,
        mappable,
        axes,
        label=None,
        orientation="vertical",
        fraction=0.046,
        pad=0.04,
        shrink=1.0,
    ):
        """
        Add one colorbar shared by multiple panels.

        Parameters
        ----------
        mappable : matplotlib.cm.ScalarMappable
            Contour/mappable returned by a plotting routine.

        axes : list
            Axes sharing the colorbar.

        label : str, optional
            Colorbar label.

        orientation : {"vertical", "horizontal"}
            Colorbar orientation.

        fraction : float
            Fraction of the axes width/height used by the colorbar.

        pad : float
            Padding between the axes and colorbar.

        shrink : float
            Colorbar length scaling.

        Returns
        -------
        matplotlib.colorbar.Colorbar
            Created colorbar.
        """

        if not isinstance(
            axes,
            (list, tuple, np.ndarray),
        ):
            axes = [axes]

        if len(axes) == 0:
            raise ValueError(
                "At least one axes is required "
                "for a shared colorbar."
            )

        if orientation not in (
            "vertical",
            "horizontal",
        ):
            raise ValueError(
                "orientation must be either "
                "'vertical' or 'horizontal'."
            )

        colorbar = self.figure.colorbar(
            mappable,
            ax=list(axes),
            orientation=orientation,
            fraction=fraction,
            pad=pad,
            shrink=shrink,
        )

        if label is not None:

            colorbar.set_label(
                label
            )

        return colorbar
    # =====================================================
    # Labels
    # =====================================================

    def set_labels(
        self,
        xlabel=None,
        ylabel=None,
    ):
        """
        Set axis labels.

        The original strings are retained so that
        they can be converted to LaTeX during PDF+TeX
        export.
        """

        if xlabel is not None:

            self.axes.set_xlabel(
                xlabel
            )

            self._latex_artists.append(
                (
                    self.axes.xaxis.label,
                    xlabel,
                )
            )

        if ylabel is not None:

            self.axes.set_ylabel(
                ylabel
            )

            self._latex_artists.append(
                (
                    self.axes.yaxis.label,
                    ylabel,
                )
            )
    # =====================================================
    # Title
    # =====================================================

    def set_title(
        self,
        title,
        **kwargs,
    ):
        """
        Set the axes title.

        The title is registered for PDF+TeX export
        so that LaTeX expressions such as
        ``$\\gamma$`` are preserved correctly.
        """

        self.axes.set_title(
            title,
            **kwargs,
        )

        self._latex_artists.append(
            (
                self.axes.title,
                title,
            )
        )
    # =====================================================
    # Limits
    # =====================================================

    def set_limits(
        self,
        xlim=None,
        ylim=None,
    ):
        """
        Set axis limits.
        """

        if xlim is not None:

            self.axes.set_xlim(
                xlim
            )

        if ylim is not None:

            self.axes.set_ylim(
                ylim
            )

    # =====================================================
    # Ticks
    # =====================================================

    def set_ticks(
        self,
        xticks=None,
        yticks=None,
    ):
        """
        Set axis tick locations.
        """

        if xticks is not None:

            self.axes.set_xticks(
                xticks
            )

        if yticks is not None:

            self.axes.set_yticks(
                yticks
            )

    # =====================================================
    # Colorbar
    # =====================================================

    def add_colorbar(
        self,
        mappable,
        label=None,
        ticks=None,
        orientation="vertical",
        pad=0.02,
        fraction=0.046,
    ):
        """
        Add a colorbar.

        Colorbar labels are registered for PDF+TeX
        export.
        """

        colorbar = add_colorbar(
            self.figure,
            self.axes,
            mappable,
            label=label,
            ticks=ticks,
            orientation=orientation,
            pad=pad,
            fraction=fraction,
        )

        if label is not None:

            self._latex_artists.append(
                (
                    colorbar.ax.yaxis.label
                    if orientation == "vertical"
                    else colorbar.ax.xaxis.label,
                    label,
                )
            )

        return colorbar

    # =====================================================
    # Standard save
    # =====================================================

    def save(
        self,
        filename,
    ):
        """
        Save the figure normally.
        """

        self.figure.savefig(
            filename,
            bbox_inches="tight",
        )

    # =====================================================
    # SVG save
    # =====================================================

    def save_svg(
        self,
        filename,
        pdftex=False,
    ):
        """
        Save the figure as SVG.

        When pdftex=True, LaTeX labels are temporarily
        replaced with plain-text placeholders so that
        Inkscape does not convert them into Unicode
        glyphs.
        """

        import matplotlib as mpl

        old_fonttype = (
            mpl.rcParams["svg.fonttype"]
        )

        replacements = []

        try:

            mpl.rcParams["svg.fonttype"] = "none"

            # -------------------------------------------------
            # Replace LaTeX labels with placeholders
            # -------------------------------------------------

            if pdftex:

                for artist, latex_text in (
                    self._latex_artists
                ):

                    placeholder = (
                        self.latex_registry.register(
                            latex_text
                        )
                    )

                    replacements.append(
                        (
                            artist,
                            latex_text,
                        )
                    )

                    artist.set_text(
                        placeholder
                    )

            # -------------------------------------------------
            # Save SVG
            # -------------------------------------------------

            self.figure.savefig(
                filename,
                format="svg",
                bbox_inches="tight",
            )

        finally:

            # -------------------------------------------------
            # Restore original labels
            # -------------------------------------------------

            for artist, original_text in (
                replacements
            ):

                artist.set_text(
                    original_text
                )

            mpl.rcParams["svg.fonttype"] = (
                old_fonttype
            )

    # =====================================================
    # Export
    # =====================================================

    def export(
        self,
        filename,
        formats,
    ):
        """
        Export the figure.

        Supported formats:

            png
            pdf
            svg
            pdf_tex
        """

        from pathlib import Path

        from postprocess.export.pdftex import (
            PDFTeXExporter,
        )

        filename = Path(
            filename
        )

        filename.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        for fmt in formats:

            # -------------------------------------------------
            # PNG
            # -------------------------------------------------

            if fmt == "png":

                self.save(
                    filename.with_suffix(
                        ".png"
                    )
                )

            # -------------------------------------------------
            # PDF
            # -------------------------------------------------

            elif fmt == "pdf":

                self.save(
                    filename.with_suffix(
                        ".pdf"
                    )
                )

            # -------------------------------------------------
            # SVG
            # -------------------------------------------------

            elif fmt == "svg":

                self.save_svg(
                    filename.with_suffix(
                        ".svg"
                    ),
                    pdftex=False,
                )

            # -------------------------------------------------
            # PDF + TeX
            # -------------------------------------------------

            elif fmt == "pdf_tex":

                svg_file = filename.with_suffix(
                    ".svg"
                )

                pdf_file = filename.with_suffix(
                    ".pdf"
                )

                # Save SVG with placeholders.
                self.save_svg(
                    svg_file,
                    pdftex=True,
                )

                exporter = PDFTeXExporter()

                exporter.export(
                    svg_file,
                    pdf_file,
                )

                # Replace placeholders with
                # original LaTeX strings.
                self.latex_registry.replace_in_file(
                    Path(
                        str(pdf_file) + "_tex"
                    )
                )

            else:

                raise ValueError(
                    "Unsupported export format: "
                    f"'{fmt}'"
                )

    # =====================================================
    # Close
    # =====================================================

    def close(self):
        """
        Close the Matplotlib figure.
        """

        plt.close(
            self.figure
        )