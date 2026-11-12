"""Axes-level plotting API."""

from __future__ import annotations

from pathlib import Path

from matplotlib.axes import Axes

from graphplot.data.field import FieldData
from graphplot.io.load import load
from graphplot.plots.contour import plot_field_contour
from graphplot.plots.mesh import plot_mesh


class Panel:
    """A single axes in a :class:`graphplot.Figure`.

    Plotting methods return ``self`` so that calls can be chained. The
    underlying Matplotlib objects remain available as ``panel.ax``,
    ``panel.artists`` and ``panel.last_artist``.
    """

    def __init__(self, figure, axes: Axes, row: int, column: int) -> None:
        self.figure = figure
        self.ax = axes
        self.row = row
        self.column = column
        self.artists: list[object] = []
        self.last_artist: object | None = None
        self.last_mappable: object | None = None

    # ------------------------------------------------------------------
    # Data plots
    # ------------------------------------------------------------------

    def contour(
        self,
        data,
        field: str | None = None,
        *,
        association: str = "auto",
        component: str | int | None = None,
        levels: int | list[float] | None = 32,
        cmap="viridis",
        vmin: float | None = None,
        vmax: float | None = None,
        norm=None,
        extend: str = "neither",
        rasterize: bool | str = "auto",
        **kwargs,
    ) -> Panel:
        """Draw a filled scalar contour from a VTP/VTU field."""
        field_data = self._as_field(data)
        if field is None:
            if len(field_data.fields) != 1:
                available = ", ".join(field_data.fields) or "<none>"
                raise ValueError(
                    "field is required when the dataset contains multiple fields. "
                    f"Available fields: {available}"
                )
            field = next(iter(field_data.fields))

        collection = plot_field_contour(
            self.ax,
            field_data,
            field,
            association=association,
            component=component,
            levels=levels,
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
            norm=norm,
            extend=extend,
            rasterize=rasterize,
            **kwargs,
        )
        self._register(collection, mappable=True)
        return self

    def mesh(self, data, **kwargs) -> Panel:
        """Overlay the computational mesh."""
        field_data = self._as_field(data)
        collection = plot_mesh(self.ax, field_data, **kwargs)
        self._register(collection)
        return self

    # ------------------------------------------------------------------
    # Labels and axes
    # ------------------------------------------------------------------

    def xlabel(self, label: str, unit: str | None = None, **kwargs) -> Panel:
        """Set the x-axis label, optionally appending a unit."""
        self.ax.set_xlabel(_with_unit(label, unit), **kwargs)
        return self

    def ylabel(self, label: str, unit: str | None = None, **kwargs) -> Panel:
        """Set the y-axis label, optionally appending a unit."""
        self.ax.set_ylabel(_with_unit(label, unit), **kwargs)
        return self

    def title(self, title: str, **kwargs) -> Panel:
        """Set the axes title."""
        self.ax.set_title(title, **kwargs)
        return self

    def xlim(self, *limits) -> Panel:
        """Set the x-axis limits."""
        self.ax.set_xlim(*limits)
        return self

    def ylim(self, *limits) -> Panel:
        """Set the y-axis limits."""
        self.ax.set_ylim(*limits)
        return self

    def xscale(self, value: str) -> Panel:
        """Set the x-axis scale."""
        self.ax.set_xscale(value)
        return self

    def yscale(self, value: str) -> Panel:
        """Set the y-axis scale."""
        self.ax.set_yscale(value)
        return self

    def ticks(self, *, x=None, y=None) -> Panel:
        """Set major tick locations."""
        if x is not None:
            self.ax.set_xticks(x)
        if y is not None:
            self.ax.set_yticks(y)
        return self

    def grid(self, visible: bool = True, **kwargs) -> Panel:
        """Toggle the axes grid."""
        self.ax.grid(visible, **kwargs)
        return self

    def tick_params(self, **kwargs) -> Panel:
        """Forward tick parameters to Matplotlib."""
        self.ax.tick_params(**kwargs)
        return self

    def aspect(self, value: str = "equal", **kwargs) -> Panel:
        """Set the axes aspect ratio."""
        self.ax.set_aspect(value, **kwargs)
        return self

    def axis_off(self) -> Panel:
        """Hide the axes frame and ticks."""
        self.ax.set_axis_off()
        return self

    def legend(self, **kwargs) -> Panel:
        """Create a legend from labelled artists."""
        self.ax.legend(**kwargs)
        return self

    def label(
        self,
        text: str,
        *,
        x: float = 0.02,
        y: float = 0.98,
        **kwargs,
    ) -> Panel:
        """Add a panel label such as ``(a)`` in axes coordinates."""
        kwargs.setdefault("ha", "left")
        kwargs.setdefault("va", "top")
        kwargs.setdefault("transform", self.ax.transAxes)
        self.ax.text(x, y, text, **kwargs)
        return self

    def text(self, x: float, y: float, text: str, **kwargs):
        """Add text in data coordinates."""
        artist = self.ax.text(x, y, text, **kwargs)
        self._register(artist)
        return self

    # ------------------------------------------------------------------
    # Figure-level convenience
    # ------------------------------------------------------------------

    def colorbar(self, mappable=None, **kwargs):
        """Add a colorbar through the parent figure."""
        return self.figure.colorbar(
            self.last_mappable if mappable is None else mappable,
            axes=self.ax,
            **kwargs,
        )

    def common_labels(self, **kwargs) -> Panel:
        """Add figure-level labels through the parent figure."""
        self.figure.common_labels(**kwargs)
        return self

    def suptitle(self, title: str, **kwargs) -> Panel:
        """Add a figure-level title."""
        self.figure.suptitle(title, **kwargs)
        return self

    def save(self, filename, **kwargs):
        """Save the parent figure."""
        return self.figure.save(filename, **kwargs)

    def close(self) -> None:
        """Close the parent figure."""
        self.figure.close()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _register(self, artist, *, mappable: bool = False) -> None:
        self.artists.append(artist)
        self.last_artist = artist
        if mappable:
            self.last_mappable = artist
            self.figure._last_mappable = artist

    def _as_field(self, data) -> FieldData:
        if isinstance(data, (str, Path)):
            data = load(data)
        if not isinstance(data, FieldData):
            raise TypeError(
                "This plot expects a VTP/VTU path or a FieldData object, "
                f"got {type(data).__name__}."
            )
        return data

    def __repr__(self) -> str:
        return f"Panel(row={self.row}, column={self.column})"


def _with_unit(label: str, unit: str | None) -> str:
    if unit is None:
        return label
    if label.endswith("]"):
        return label
    return f"{label} [{unit}]"
