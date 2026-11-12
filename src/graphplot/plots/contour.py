"""Scalar contour plotting for VTK fields and tabular data."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import matplotlib as mpl
import matplotlib.tri as mtri
import numpy as np
from matplotlib.collections import PolyCollection
from matplotlib.colors import BoundaryNorm, Colormap, Normalize
from matplotlib.ticker import FixedLocator, FuncFormatter, MaxNLocator

from graphplot.data.field import FieldData
from graphplot.data.table import Table


@dataclass
class ColorScale:
    """Resolved color scale for a scalar field."""

    levels: int | Sequence[float] | None = 32
    cmap: str | Colormap | Sequence[str] = "viridis"
    vmin: float | None = None
    vmax: float | None = None
    norm: Normalize | None = None
    extend: str = "neither"

    def resolve(self, values: np.ndarray) -> ColorScale:
        """Resolve limits, colormap and norm from field values."""
        values = np.asarray(values, dtype=float)
        finite = values[np.isfinite(values)]
        if finite.size == 0:
            raise ValueError("The field contains no finite values.")

        vmin = float(np.nanmin(finite)) if self.vmin is None else float(self.vmin)
        vmax = float(np.nanmax(finite)) if self.vmax is None else float(self.vmax)
        if vmin > vmax:
            raise ValueError("vmin must not be greater than vmax.")
        if vmin == vmax:
            delta = 1.0 if vmin == 0.0 else abs(vmin) * 1e-6
            vmin -= delta
            vmax += delta

        self._vmin = vmin
        self._vmax = vmax
        self.colormap = _make_cmap(self.cmap)

        if self.norm is not None:
            self.levels_array = None
            return self

        if self.levels is None:
            self.levels_array = None
            self.norm = Normalize(vmin=vmin, vmax=vmax)
            return self

        if np.isscalar(self.levels):
            levels = int(self.levels)
            if levels < 1:
                raise ValueError("levels must be greater than zero.")
            boundaries = np.linspace(vmin, vmax, levels + 1)
            self.colormap = self.colormap.resampled(levels)
        else:
            boundaries = np.asarray(self.levels, dtype=float)
            if boundaries.ndim != 1 or len(boundaries) < 2:
                raise ValueError("Explicit levels must contain at least two values.")
            if not np.all(np.diff(boundaries) > 0):
                raise ValueError("Explicit levels must be strictly increasing.")

        self.levels_array = boundaries
        try:
            self.norm = BoundaryNorm(
                boundaries,
                self.colormap.N,
                clip=False,
                extend=self.extend,
            )
        except TypeError:  # pragma: no cover - older Matplotlib
            self.norm = BoundaryNorm(boundaries, self.colormap.N, clip=False)
        return self

    @property
    def limits(self) -> tuple[float, float]:
        """Resolved color limits."""
        return self._vmin, self._vmax


def _make_cmap(cmap: str | Colormap | Sequence[str]) -> Colormap:
    if isinstance(cmap, Colormap):
        return cmap
    if isinstance(cmap, str):
        return mpl.colormaps[cmap]
    from matplotlib.colors import LinearSegmentedColormap

    return LinearSegmentedColormap.from_list("graphplot_custom", list(cmap))


def plot_field_contour(
    axes,
    data: FieldData,
    field: str,
    *,
    association: str = "auto",
    component: str | int | None = None,
    levels: int | Sequence[float] | None = 32,
    cmap: str | Colormap | Sequence[str] = "viridis",
    vmin: float | None = None,
    vmax: float | None = None,
    norm: Normalize | None = None,
    extend: str = "neither",
    show_lines: bool = False,
    contour_labels: bool = False,
    line_color: str = "black",
    line_width: float = 0.7,
    label_fontsize: float = 8,
    label_format: str | None = None,
    rasterize: bool | str = "auto",
    rasterize_threshold: int = 50_000,
    **kwargs,
):
    """Draw a scalar field from a VTK mesh."""
    resolved_association = (
        data.association(field) if association == "auto" else association
    )
    values = data.field(field, association=resolved_association, component=component)
    scale = ColorScale(
        levels=levels,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        norm=norm,
        extend=extend,
    ).resolve(values)

    line_levels = _line_levels(scale)
    if resolved_association == "point":
        collection, triangulation = _plot_point_contour(
            axes,
            data,
            values,
            scale,
            extend=extend,
            **kwargs,
        )
        if show_lines or contour_labels:
            _add_triangle_lines(
                axes,
                triangulation,
                values,
                line_levels,
                color=line_color,
                linewidth=line_width,
                labels=contour_labels,
                fontsize=label_fontsize,
                label_format=label_format,
            )
    else:
        if values.size != data.n_cells:
            raise ValueError(
                f"Field {field!r} has {values.size} values but the mesh has "
                f"{data.n_cells} cells."
            )
        collection = PolyCollection(
            data.cell_polygons(),
            array=values,
            cmap=scale.colormap,
            norm=scale.norm,
            edgecolors="none",
            linewidths=0.0,
            antialiased=False,
            **kwargs,
        )
        axes.add_collection(collection)

        if show_lines or contour_labels:
            # Approximate cell-centred isolines using a triangulation of the
            # cell centres. The filled polygons remain the exact cell values.
            centres = data.cell_centers
            triangulation = mtri.Triangulation(centres[:, 0], centres[:, 1])
            _add_triangle_lines(
                axes,
                triangulation,
                values,
                line_levels,
                color=line_color,
                linewidth=line_width,
                labels=contour_labels,
                fontsize=label_fontsize,
                label_format=label_format,
            )

    _apply_rasterize(collection, rasterize, data.n_cells, rasterize_threshold)
    xmin, xmax, ymin, ymax = data.bounds2d
    axes.set_xlim(xmin, xmax)
    axes.set_ylim(ymin, ymax)
    axes.set_aspect("equal", adjustable="box")
    axes.grid(False)
    return collection


def plot_table_contour(
    axes,
    table: Table,
    *,
    x: str | int,
    y: str | int,
    field: str | int,
    xscale: str = "linear",
    yscale: str = "linear",
    grid: str = "auto",
    levels: int | Sequence[float] | None = 25,
    cmap: str | Colormap | Sequence[str] = "viridis",
    vmin: float | None = None,
    vmax: float | None = None,
    norm: Normalize | None = None,
    extend: str = "neither",
    show_points: bool = False,
    show_lines: bool = False,
    contour_labels: bool = False,
    max_triangle_edge: float | None = None,
    point_size: float = 20,
    point_color: str = "white",
    point_edgecolor: str = "black",
    line_color: str = "black",
    line_width: float = 0.7,
    label_fontsize: float = 8,
    label_format: str | None = None,
    rasterize: bool | str = "auto",
    rasterize_threshold: int = 50_000,
    **kwargs,
):
    """Draw a filled contour from scattered or gridded tabular data."""
    if xscale not in ("linear", "log") or yscale not in ("linear", "log"):
        raise ValueError("xscale and yscale must be 'linear' or 'log'.")
    if grid not in ("auto", "regular", "triangulate"):
        raise ValueError("grid must be 'auto', 'regular' or 'triangulate'.")

    x_values = _column(table, x)
    y_values = _column(table, y)
    values = _column(table, field)
    if not (len(x_values) == len(y_values) == len(values)):
        raise ValueError("X, Y and field columns must have equal lengths.")
    if len(x_values) < 3:
        raise ValueError("At least three samples are required for a 2D contour.")

    valid = np.isfinite(x_values) & np.isfinite(y_values) & np.isfinite(values)
    x_values, y_values, values = x_values[valid], y_values[valid], values[valid]
    if len(x_values) < 3:
        raise ValueError("Fewer than three finite samples remain.")
    if xscale == "log" and np.any(x_values <= 0):
        raise ValueError("All X coordinates must be positive for a log axis.")
    if yscale == "log" and np.any(y_values <= 0):
        raise ValueError("All Y coordinates must be positive for a log axis.")
    if max_triangle_edge is not None and max_triangle_edge <= 0:
        raise ValueError("max_triangle_edge must be positive when supplied.")

    points = np.column_stack((x_values, y_values))
    if np.unique(points, axis=0).shape[0] != len(points):
        raise ValueError("Duplicate (x, y) sample coordinates were found.")

    x_plot = np.log10(x_values) if xscale == "log" else x_values.copy()
    y_plot = np.log10(y_values) if yscale == "log" else y_values.copy()
    scale = ColorScale(
        levels=levels,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        norm=norm,
        extend=extend,
    ).resolve(values)
    fill_levels = scale.levels_array if scale.levels_array is not None else 25
    line_levels = _line_levels(scale)

    regular = _regular_grid(x_plot, y_plot, values)
    use_regular = grid == "regular" or (grid == "auto" and regular is not None)
    if grid == "regular" and regular is None:
        raise ValueError("Data does not form a complete rectilinear grid.")
    if use_regular:
        x_grid, y_grid, z_grid = regular
        filled = axes.contourf(
            x_grid,
            y_grid,
            z_grid,
            levels=fill_levels,
            cmap=scale.colormap,
            norm=scale.norm,
            extend=extend,
            **kwargs,
        )
        lines = None
        if show_lines or contour_labels:
            lines = axes.contour(
                x_grid,
                y_grid,
                z_grid,
                levels=line_levels,
                colors=line_color,
                linewidths=line_width,
            )
    else:
        triangulation = mtri.Triangulation(x_plot, y_plot)
        if max_triangle_edge is not None:
            _mask_large_triangles(triangulation, max_triangle_edge)
        filled = axes.tricontourf(
            triangulation,
            values,
            levels=fill_levels,
            cmap=scale.colormap,
            norm=scale.norm,
            extend=extend,
            **kwargs,
        )
        lines = None
        if show_lines or contour_labels:
            lines = axes.tricontour(
                triangulation,
                values,
                levels=line_levels,
                colors=line_color,
                linewidths=line_width,
            )

    if contour_labels and lines is not None:
        axes.clabel(
            lines,
            inline=True,
            fontsize=label_fontsize,
            fmt=label_format or "%.3g",
        )

    if show_points:
        axes.scatter(
            x_plot,
            y_plot,
            s=point_size,
            facecolors=point_color,
            edgecolors=point_edgecolor,
            linewidths=0.8,
            zorder=5,
        )

    _apply_rasterize(filled, rasterize, len(x_plot), rasterize_threshold)
    _configure_table_axis(axes, "x", xscale, x_plot)
    _configure_table_axis(axes, "y", yscale, y_plot)
    axes.set_xlim(float(x_plot.min()), float(x_plot.max()))
    axes.set_ylim(float(y_plot.min()), float(y_plot.max()))
    return filled


def _plot_point_contour(
    axes,
    data: FieldData,
    values: np.ndarray,
    scale: ColorScale,
    *,
    extend: str,
    **kwargs,
):
    if values.size != data.n_points:
        raise ValueError(
            f"Point field has {values.size} values but the mesh has "
            f"{data.n_points} points."
        )

    points = data.points[:, :2]
    triangles = data.triangles()
    triangulation = mtri.Triangulation(points[:, 0], points[:, 1], triangles)

    if scale.levels_array is not None:
        collection = axes.tricontourf(
            triangulation,
            values,
            levels=scale.levels_array,
            cmap=scale.colormap,
            norm=scale.norm,
            extend=extend,
            **kwargs,
        )
    else:
        collection = axes.tripcolor(
            triangulation,
            values,
            cmap=scale.colormap,
            norm=scale.norm,
            shading="gouraud",
            **kwargs,
        )
    return collection, triangulation


def _add_triangle_lines(
    axes,
    triangulation,
    values,
    levels,
    *,
    color,
    linewidth,
    labels,
    fontsize,
    label_format,
):
    lines = axes.tricontour(
        triangulation,
        values,
        levels=levels,
        colors=color,
        linewidths=linewidth,
    )
    if labels:
        axes.clabel(
            lines,
            inline=True,
            fontsize=fontsize,
            fmt=label_format or "%.3g",
        )
    return lines


def _line_levels(scale: ColorScale) -> np.ndarray:
    if scale.levels_array is not None:
        return scale.levels_array
    vmin, vmax = scale.limits
    return np.linspace(vmin, vmax, 8)


def _column(table: Table, key: str | int) -> np.ndarray:
    if isinstance(key, int):
        key = table.columns[key]
    values = np.asarray(table[key], dtype=float)
    if values.ndim != 1:
        raise ValueError(f"Column {key!r} must be one-dimensional.")
    return values


def _regular_grid(x, y, z):
    x_unique = np.unique(x)
    y_unique = np.unique(y)
    if len(x_unique) * len(y_unique) != len(x):
        return None
    x_index = np.searchsorted(x_unique, x)
    y_index = np.searchsorted(y_unique, y)
    z_grid = np.full((len(y_unique), len(x_unique)), np.nan)
    z_grid[y_index, x_index] = z
    if np.isnan(z_grid).any():
        return None
    x_grid, y_grid = np.meshgrid(x_unique, y_unique)
    return x_grid, y_grid, z_grid


def _mask_large_triangles(triangulation, max_edge):
    triangles = triangulation.triangles
    x = triangulation.x[triangles]
    y = triangulation.y[triangles]
    edges = np.stack(
        (
            np.hypot(x[:, 0] - x[:, 1], y[:, 0] - y[:, 1]),
            np.hypot(x[:, 1] - x[:, 2], y[:, 1] - y[:, 2]),
            np.hypot(x[:, 2] - x[:, 0], y[:, 2] - y[:, 0]),
        ),
        axis=1,
    )
    triangulation.set_mask(np.max(edges, axis=1) > max_edge)


def _configure_table_axis(axes, axis, scale, values):
    if scale == "log":
        setter = axes.set_xscale if axis == "x" else axes.set_yscale
        setter("linear")
        low = int(np.floor(np.min(values)))
        high = int(np.ceil(np.max(values)))
        axis_object = axes.xaxis if axis == "x" else axes.yaxis
        axis_object.set_major_locator(FixedLocator(np.arange(low, high + 1)))
        axis_object.set_major_formatter(FuncFormatter(_log_tick_formatter))
    else:
        axis_object = axes.xaxis if axis == "x" else axes.yaxis
        axis_object.set_major_locator(MaxNLocator(nbins=6))


def _log_tick_formatter(value, _position):
    exponent = int(round(value))
    if abs(value - exponent) < 1e-8:
        return rf"$10^{{{exponent}}}$"
    return f"{10.0**value:g}"


def _apply_rasterize(collection, mode, count, threshold):
    if mode is True or (mode == "auto" and count > threshold):
        setter = getattr(collection, "set_rasterized", None)
        if setter is not None:
            setter(True)
            return
        for child in getattr(collection, "collections", []):
            child.set_rasterized(True)
