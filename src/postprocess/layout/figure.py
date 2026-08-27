from dataclasses import dataclass
from typing import Optional, Tuple

import matplotlib.pyplot as plt

from postprocess.layout.colorbar import add_colorbar
from postprocess.export.latex import (
    LaTeXTextRegistry,
)


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
    ):

        self.config = config

        # -------------------------------------------------
        # Figure dimensions
        # -------------------------------------------------

        width = float(config.width)

        if config.height is None:

            height = (
                width *
                float(config.height_ratio)
            )

        else:

            height = float(config.height)

        # -------------------------------------------------
        # Create figure
        # -------------------------------------------------

        self.figure, self.axes = plt.subplots(
            figsize=(width, height),
            dpi=int(config.dpi),
        )

        # -------------------------------------------------
        # Aspect
        # -------------------------------------------------

        self.axes.set_aspect(
            config.aspect
        )

        # -------------------------------------------------
        # Limits
        # -------------------------------------------------

        if config.xlim is not None:

            self.axes.set_xlim(
                config.xlim
            )

        if config.ylim is not None:

            self.axes.set_ylim(
                config.ylim
            )

        # -------------------------------------------------
        # Grid
        # -------------------------------------------------

        self.axes.grid(
            config.show_grid
        )

        # -------------------------------------------------
        # LaTeX registry
        # -------------------------------------------------

        self.latex_registry = (
            LaTeXTextRegistry()
        )

        self._latex_artists = []

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