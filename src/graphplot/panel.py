"""Axes-level plotting API."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from matplotlib.axes import Axes

from graphplot.data.field import FieldData
from graphplot.data.series import Data1D
from graphplot.data.table import Table
from graphplot.io.load import load
from graphplot.plots.contour import plot_field_contour
from graphplot.plots.legend import grouped_legend, table_legend
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
        self.last_legend: object | None = None
        self._line_count = 0

    # ------------------------------------------------------------------
    # 1D plots
    # ------------------------------------------------------------------

    def line(
        self,
        data,
        y=None,
        *,
        x=None,
        label: str | None = None,
        role: str | None = None,
        color=None,
        linestyle=None,
        marker=None,
        **kwargs,
    ) -> Panel:
        """Plot one or more 1D series.

        ``data`` may be a path, a :class:`Table`, a :class:`Data1D`, or an
        array. For tabular input, ``x`` and ``y`` are column names or indices.
        """
        series = self._as_series(data, x=x, y=y)
        if isinstance(series, list):
            for item in series:
                self._plot_series(
                    item,
                    label=None,
                    role=role,
                    color=color,
                    linestyle=linestyle,
                    marker=marker,
                    **kwargs,
                )
            return self
        return self._plot_series(
            series,
            label=label,
            role=role,
            color=color,
            linestyle=linestyle,
            marker=marker,
            **kwargs,
        )

    def errorbar(
        self,
        data,
        y=None,
        *,
        x=None,
        yerr=None,
        xerr=None,
        label: str | None = None,
        color=None,
        marker="o",
        linestyle="none",
        capsize: float = 3.0,
        **kwargs,
    ) -> Panel:
        """Plot a series with error bars."""
        series = self._as_series(data, x=x, y=y)
        if isinstance(series, list):
            for item in series:
                self._errorbar_series(
                    item,
                    yerr=yerr,
                    xerr=xerr,
                    label=None,
                    color=color,
                    marker=marker,
                    linestyle=linestyle,
                    capsize=capsize,
                    **kwargs,
                )
            return self
        return self._errorbar_series(
            series,
            yerr=yerr,
            xerr=xerr,
            label=label,
            color=color,
            marker=marker,
            linestyle=linestyle,
            capsize=capsize,
            **kwargs,
        )

    def fill_between(
        self,
        x,
        y1,
        y2=0.0,
        *,
        label: str | None = None,
        **kwargs,
    ) -> Panel:
        """Fill the area between two curves."""
        artist = self.ax.fill_between(x, y1, y2, label=label, **kwargs)
        self._register(artist)
        return self

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

    def legend(
        self,
        *,
        loc: str = "best",
        ncol: int = 1,
        ncols: int | None = None,
        frameon: bool = False,
        fontsize: float | None = None,
        title: str | None = None,
        groups=None,
        **kwargs,
    ):
        """Create a standard or grouped legend.

        ``groups`` may be a list of ``{"title": ..., "labels": [...]}``
        dictionaries or a mapping from group title to labels.
        """
        if ncols is not None:
            ncol = ncols
        if groups is not None:
            legend = grouped_legend(
                self.ax,
                groups,
                loc=loc,
                ncol=ncol,
                frameon=frameon,
                fontsize=fontsize,
                title=title,
                **kwargs,
            )
        else:
            legend = self.ax.legend(
                loc=loc,
                ncol=ncol,
                frameon=frameon,
                fontsize=fontsize,
                title=title,
                **kwargs,
            )
        self.last_legend = legend
        return self

    def legend_table(
        self,
        groups,
        *,
        location: str = "lower center",
        bbox_to_anchor=(0.5, -0.12),
        fontsize: float | None = None,
        handle_length: float = 32,
        column_spacing: float = 30,
        row_spacing: float = 5,
    ):
        """Create a table-style legend with group headings and case rows."""
        legend = table_legend(
            self.figure.figure,
            groups,
            location=location,
            bbox_to_anchor=bbox_to_anchor,
            fontsize=fontsize or self.figure.style.legend_size,
            handle_length=handle_length,
            column_spacing=column_spacing,
            row_spacing=row_spacing,
        )
        self.last_legend = legend
        return self

    def twinx(self) -> Panel:
        """Create a panel sharing the x-axis with this panel."""
        panel = Panel(self.figure, self.ax.twinx(), self.row, self.column)
        panel._is_twin = True
        return panel

    def twiny(self) -> Panel:
        """Create a panel sharing the y-axis with this panel."""
        panel = Panel(self.figure, self.ax.twiny(), self.row, self.column)
        panel._is_twin = True
        return panel

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

    def _as_series(self, data, *, x=None, y=None) -> Data1D | list[Data1D]:
        if isinstance(data, Data1D):
            return data

        if isinstance(data, (str, Path)):
            data = load(data)

        if isinstance(data, Table):
            x_key = _default_column(data, x, "x", 0)
            if isinstance(y, (list, tuple)):
                return [data.series(x_key, item) for item in y]
            y_key = _default_column(data, y, "y", 1)
            return data.series(x_key, y_key)

        array = np.asarray(data, dtype=float)
        if y is None:
            if array.ndim == 2 and array.shape[1] >= 2:
                return Data1D(array[:, 0], array[:, 1])
            raise ValueError(
                "y is required when plotting a one-dimensional array. "
                "Pass line(x, y) or line(table, y='column')."
            )
        y_array = np.asarray(y, dtype=float)
        if array.ndim != 1 or y_array.ndim != 1:
            raise ValueError("x and y arrays must be one-dimensional.")
        return Data1D(array, y_array)

    def _plot_series(
        self,
        series: Data1D,
        *,
        label=None,
        role=None,
        color=None,
        linestyle=None,
        marker=None,
        **kwargs,
    ) -> Panel:
        style = self.figure.style
        index = self._line_count
        color = kwargs.pop("c", color) or style.color(index)
        linestyle = kwargs.pop("ls", linestyle)
        if linestyle is None:
            linestyle = _role_linestyle(role, style.linestyle(index))
        if marker is None:
            marker = style.marker(index) if role == "experimental" else None

        artist = self.ax.plot(
            series.x,
            series.y,
            label=label or series.label,
            color=color,
            linestyle=linestyle,
            marker=marker,
            **kwargs,
        )[0]
        self._line_count += 1
        self._register(artist)
        return self

    def _errorbar_series(
        self,
        series: Data1D,
        *,
        yerr=None,
        xerr=None,
        label=None,
        color=None,
        marker="o",
        linestyle="none",
        capsize=3.0,
        **kwargs,
    ) -> Panel:
        style = self.figure.style
        index = self._line_count
        color = kwargs.pop("c", color) or style.color(index)
        container = self.ax.errorbar(
            series.x,
            series.y,
            yerr=series.yerr if yerr is None else yerr,
            xerr=series.xerr if xerr is None else xerr,
            label=label or series.label,
            color=color,
            marker=marker,
            linestyle=linestyle,
            capsize=capsize,
            **kwargs,
        )
        self._line_count += 1
        self._register(container)
        return self

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


def _default_column(table: Table, key, preferred: str, index: int):
    if key is not None:
        return key
    return preferred if preferred in table.columns else index


def _role_linestyle(role: str | None, fallback: str) -> str:
    if role is None:
        return fallback
    return {
        "numerical": "-",
        "analytical": "--",
        "experimental": "none",
        "reference": "-.",
    }.get(role, fallback)
