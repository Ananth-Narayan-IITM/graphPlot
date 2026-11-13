"""Figure container and publication layout."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from graphplot.export import save_figure
from graphplot.panel import Panel
from graphplot.style import Style
from graphplot.tex import as_plain, tag_latex, with_unit


class Figure:
    """A publication figure with one or more panels.

    Single-panel figures forward plotting methods directly to their panel, so
    ``fig.contour(...)`` works without an explicit ``fig.panel(0, 0)``.
    """

    def __init__(
        self,
        width: float = 3.4,
        height: float | None = None,
        *,
        nrows: int = 1,
        ncols: int = 1,
        style: Style | str | None = None,
        dpi: int | None = None,
        height_ratio: float = 0.75,
        layout: str | None = "constrained",
        sharex: bool | str = False,
        sharey: bool | str = False,
        **subplots_kwargs,
    ) -> None:
        if style is None:
            style = Style()
        elif isinstance(style, str):
            style = Style.from_preset(style)
        self.style = style
        style.apply()

        self.dpi = int(dpi or style.dpi)
        width = float(width)
        height = float(height) if height is not None else width * float(height_ratio)

        subplots_kwargs.setdefault("sharex", sharex)
        subplots_kwargs.setdefault("sharey", sharey)
        subplots_kwargs.setdefault("squeeze", False)
        if layout is not None:
            subplots_kwargs.setdefault("layout", layout)

        self.figure, axes = plt.subplots(
            nrows=nrows,
            ncols=ncols,
            figsize=(width, height),
            **subplots_kwargs,
        )
        self.figure.set_dpi(self.dpi)
        self.nrows = int(nrows)
        self.ncols = int(ncols)
        self._axes_array = np.asarray(axes, dtype=object).reshape(
            self.nrows, self.ncols
        )
        self.panels = [
            [
                Panel(self, self._axes_array[row, col], row, col)
                for col in range(self.ncols)
            ]
            for row in range(self.nrows)
        ]
        self.axes = [panel.ax for row in self.panels for panel in row]
        self._main_panel = self.panels[0][0] if self.nrows * self.ncols == 1 else None
        self._last_mappable = None

    # ------------------------------------------------------------------
    # Panel access
    # ------------------------------------------------------------------

    def panel(self, row: int = 0, column: int = 0) -> Panel:
        """Return a panel by zero-based row and column."""
        if not 0 <= row < self.nrows:
            raise IndexError(f"Panel row {row} is out of range.")
        if not 0 <= column < self.ncols:
            raise IndexError(f"Panel column {column} is out of range.")
        return self.panels[row][column]

    def __getitem__(self, key) -> Panel:
        if isinstance(key, tuple):
            return self.panel(*key)
        if isinstance(key, int):
            if key < 0:
                key += self.nrows * self.ncols
            return self.panels[key // self.ncols][key % self.ncols]
        raise TypeError("Use fig[row, col] or fig[index].")

    def __iter__(self):
        return iter(self.axes)

    def __len__(self) -> int:
        return self.nrows * self.ncols

    def __getattr__(self, name: str):
        # Delegate axes-level convenience methods for single-panel figures.
        if name.startswith("_"):
            raise AttributeError(name)
        main = self.__dict__.get("_main_panel")
        if main is not None and hasattr(main, name):
            return getattr(main, name)
        raise AttributeError(f"{type(self).__name__!r} has no attribute {name!r}")

    # ------------------------------------------------------------------
    # Labels and layout
    # ------------------------------------------------------------------

    def common_labels(
        self,
        *,
        x: str | None = None,
        y: str | None = None,
        x_unit: str | None = None,
        y_unit: str | None = None,
        **kwargs,
    ) -> Figure:
        """Add figure-level x/y labels."""
        if x is not None:
            value = with_unit(x, x_unit)
            artist = self.figure.supxlabel(as_plain(value), **kwargs)
            tag_latex(artist, value)
        if y is not None:
            value = with_unit(y, y_unit)
            artist = self.figure.supylabel(as_plain(value), **kwargs)
            tag_latex(artist, value)
        return self

    def label_panels(
        self,
        labels: list[str] | tuple[str, ...] | None = None,
        *,
        x: float = 0.02,
        y: float = 0.98,
        **kwargs,
    ) -> Figure:
        """Add panel labels such as ``(a)``, ``(b)``, ..."""
        count = self.nrows * self.ncols
        if labels is None:
            labels = [f"({chr(ord('a') + index)})" for index in range(count)]
        if len(labels) != count:
            raise ValueError(f"Expected {count} panel labels, got {len(labels)}.")
        for panel, label in zip(self.panels_flat, labels, strict=False):
            panel.label(label, x=x, y=y, **kwargs)
        return self

    @property
    def panels_flat(self) -> list[Panel]:
        """All panels in row-major order."""
        return [panel for row in self.panels for panel in row]

    def tight_layout(self, **kwargs) -> Figure:
        """Apply Matplotlib tight layout."""
        self.figure.tight_layout(**kwargs)
        return self

    def subplots_adjust(self, **kwargs) -> Figure:
        """Forward to ``Figure.subplots_adjust``."""
        self.figure.subplots_adjust(**kwargs)
        return self

    def suptitle(self, title, **kwargs) -> Figure:
        """Add a figure-level title."""
        artist = self.figure.suptitle(as_plain(title), **kwargs)
        tag_latex(artist, title)
        return self

    # ------------------------------------------------------------------
    # Colorbars
    # ------------------------------------------------------------------

    def colorbar(
        self,
        mappable=None,
        *,
        label=None,
        axes=None,
        location: str = "right",
        **kwargs,
    ):
        """Add a colorbar, using the last contour by default."""
        if mappable is None:
            mappable = self._last_mappable
        if mappable is None:
            raise ValueError(
                "No mappable was supplied and no contour has been drawn yet."
            )
        if axes is None:
            axes = self._main_panel.ax if self._main_panel is not None else self.axes
        if isinstance(axes, Panel):
            axes = axes.ax
        elif isinstance(axes, (list, tuple)):
            axes = [panel.ax if isinstance(panel, Panel) else panel for panel in axes]

        colorbar = self.figure.colorbar(mappable, ax=axes, location=location, **kwargs)
        if label is not None:
            colorbar.set_label(as_plain(label))
            for axis in (colorbar.ax.yaxis, colorbar.ax.xaxis):
                if axis.label.get_text():
                    tag_latex(axis.label, label)
        return colorbar

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def save(
        self,
        filename: str | Path,
        *,
        formats: str | tuple[str, ...] | list[str] = ("pdf_tex", "png"),
        dpi: int | None = None,
        transparent: bool = False,
        pad_inches: float = 0.02,
        pdf_tex_text_size: str = "inherit",
        **savefig_kwargs,
    ) -> dict[str, Path]:
        """Save the figure and return the generated paths.

        ``pdf_tex_text_size="inherit"`` (default) lets the surrounding LaTeX
        document control the text size. Use ``"figure"`` to preserve the
        Matplotlib point sizes inside the PDF_TeX file.
        """
        return save_figure(
            self,
            filename,
            formats=formats,
            dpi=dpi,
            transparent=transparent,
            pad_inches=pad_inches,
            pdf_tex_text_size=pdf_tex_text_size,
            **savefig_kwargs,
        )

    def show(self) -> None:
        """Display the figure interactively."""
        plt.show()

    def close(self) -> None:
        """Close the underlying Matplotlib figure."""
        plt.close(self.figure)

    def __enter__(self) -> Figure:
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.close()

    def __repr__(self) -> str:
        return (
            f"Figure(rows={self.nrows}, columns={self.ncols}, "
            f"size={self.figure.get_size_inches().tolist()})"
        )
