"""Filled contour plots from scattered tabular data."""

import numpy as np
import matplotlib.tri as mtri
from matplotlib.ticker import FixedLocator, FuncFormatter, MaxNLocator

from postprocess.layout.colors import ColorScale


class DataContourPlot:
    """Plot a scalar field sampled at scattered ``(x, y)`` locations.

    Logarithmic axes are handled by transforming coordinates before creating
    the triangulation. This makes the interpolation geometry consistent with
    the displayed log-scaled coordinate system. Tick labels are formatted in
    the original physical coordinates.

    Parameters
    ----------
    data : TabularData, mapping, or object with named columns
        Input data. Mapping values should be one-dimensional arrays.
    x, y, field : str
        Names of the independent-variable columns and scalar field.
    x_scale, y_scale : {"linear", "log"}
        Coordinate scales. Each axis is configured independently.
    interpolation : {"linear"}
        Interpolation method. Linear triangulation is currently supported.
    levels : int or sequence, optional
        Number of filled color bands, or explicit contour levels.
    cmap : str, optional
        Matplotlib colormap.
    vmin, vmax : float, optional
        Color limits. If omitted, the sample-data range is used.
    max_triangle_edge : float, optional
        Mask triangles whose longest edge exceeds this length in transformed
        coordinate space. Useful for preventing contours bridging large gaps.
    """

    def __init__(
        self,
        data,
        x,
        y,
        field,
        x_scale="linear",
        y_scale="linear",
        interpolation="linear",
        levels=25,
        cmap="plasma",
        vmin=None,
        vmax=None,
        max_triangle_edge=None,
    ):
        self.data = data
        self.x_name = x
        self.y_name = y
        self.field = field
        self.x_scale = self._validate_scale(x_scale, "x_scale")
        self.y_scale = self._validate_scale(y_scale, "y_scale")
        if interpolation != "linear":
            raise ValueError("Only interpolation='linear' is currently supported.")

        self.x = self._column(x)
        self.y = self._column(y)
        self.values = self._column(field)
        if not (len(self.x) == len(self.y) == len(self.values)):
            raise ValueError("X, Y, and field columns must have equal lengths.")
        if len(self.x) < 3:
            raise ValueError("At least three samples are required for a 2D contour.")
        if not (
            np.isfinite(self.x).all()
            and np.isfinite(self.y).all()
            and np.isfinite(self.values).all()
        ):
            raise ValueError("X, Y, and field columns must contain only finite values.")
        if self.x_scale == "log" and np.any(self.x <= 0):
            raise ValueError(
                "All X coordinates must be positive for a logarithmic axis."
            )
        if self.y_scale == "log" and np.any(self.y <= 0):
            raise ValueError(
                "All Y coordinates must be positive for a logarithmic axis."
            )
        if max_triangle_edge is not None and max_triangle_edge <= 0:
            raise ValueError("max_triangle_edge must be positive when supplied.")

        points = np.column_stack((self.x, self.y))
        if np.unique(points, axis=0).shape[0] != len(points):
            raise ValueError("Duplicate (x, y) sample coordinates were found.")

        self.x_plot = np.log10(self.x) if self.x_scale == "log" else self.x.copy()
        self.y_plot = np.log10(self.y) if self.y_scale == "log" else self.y.copy()
        self.triangulation = mtri.Triangulation(self.x_plot, self.y_plot)
        self._mask_large_triangles(max_triangle_edge)

        self.levels = levels
        self.scale = ColorScale(
            levels=levels if np.isscalar(levels) else len(levels) - 1,
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
        )
        self.explicit_levels = (
            None if np.isscalar(levels) else np.asarray(levels, dtype=float)
        )
        if self.explicit_levels is not None:
            if self.explicit_levels.ndim != 1 or len(self.explicit_levels) < 2:
                raise ValueError("Explicit levels must contain at least two values.")
            if not np.all(np.diff(self.explicit_levels) > 0):
                raise ValueError("Explicit contour levels must be strictly increasing.")

    def _column(self, name):
        try:
            if hasattr(self.data, "get_column"):
                values = self.data.get_column(name)
            else:
                values = self.data[name]
        except (KeyError, TypeError) as exc:
            available = getattr(self.data, "columns", None)
            suffix = f" Available columns: {available}" if available is not None else ""
            raise KeyError(f"Required column {name!r} was not found.{suffix}") from exc
        values = np.asarray(values, dtype=float)
        if values.ndim != 1:
            raise ValueError(f"Column {name!r} must be one-dimensional.")
        return values

    @staticmethod
    def _validate_scale(scale, name):
        if scale not in ("linear", "log"):
            raise ValueError(f"{name} must be 'linear' or 'log'.")
        return scale

    def _mask_large_triangles(self, max_triangle_edge):
        if max_triangle_edge is None:
            return
        triangles = self.triangulation.triangles
        xx = self.x_plot[triangles]
        yy = self.y_plot[triangles]
        lengths = np.stack(
            (
                np.hypot(xx[:, 0] - xx[:, 1], yy[:, 0] - yy[:, 1]),
                np.hypot(xx[:, 1] - xx[:, 2], yy[:, 1] - yy[:, 2]),
                np.hypot(xx[:, 2] - xx[:, 0], yy[:, 2] - yy[:, 0]),
            ),
            axis=1,
        )
        self.triangulation.set_mask(np.max(lengths, axis=1) > max_triangle_edge)

    @staticmethod
    def _log_tick_formatter(value, _position):
        exponent = int(round(value))
        if abs(value - exponent) < 1e-8:
            return rf"$10^{{{exponent}}}$"
        return f"{10.0**value:g}"

    def _configure_axis(self, axes, axis):
        scale = self.x_scale if axis == "x" else self.y_scale
        values = self.x_plot if axis == "x" else self.y_plot
        setter = axes.set_xscale if axis == "x" else axes.set_yscale
        locator_setter = (
            axes.xaxis.set_major_locator
            if axis == "x"
            else axes.yaxis.set_major_locator
        )
        formatter_setter = (
            axes.xaxis.set_major_formatter
            if axis == "x"
            else axes.yaxis.set_major_formatter
        )
        if scale == "log":
            # Coordinates are already transformed for correct log-space interpolation.
            # Keep Matplotlib axes linear and format transformed ticks as physical values.
            low = int(np.floor(np.min(values)))
            high = int(np.ceil(np.max(values)))
            locator_setter(FixedLocator(np.arange(low, high + 1)))
            formatter_setter(FuncFormatter(self._log_tick_formatter))
        else:
            setter("linear")
            locator_setter(MaxNLocator(nbins=6))

    def plot(
        self,
        axes,
        scale=None,
        show_points=True,
        show_contour_lines=True,
        contour_levels=None,
        contour_labels=False,
        point_size=42,
        point_edgecolor="black",
        point_facecolor="white",
        point_linewidth=1.2,
        contour_linecolor="white",
        contour_linewidth=0.7,
        rasterize=True,
    ):
        """Draw the filled contour and optionally sample points and isolines.

        Returns the filled-contour mappable, suitable for ``figure.add_colorbar``.
        """
        if scale is None:
            scale = self.scale
        scale.resolve(self.values)
        levels = self.explicit_levels
        if levels is None:
            levels = scale.levels_array
        elif scale.vmin is not None or scale.vmax is not None:
            levels = np.linspace(
                scale._vmin or levels[0], scale._vmax or levels[-1], scale.levels + 1
            )

        filled = axes.tricontourf(
            self.triangulation,
            self.values,
            levels=levels,
            cmap=scale.colormap,
            norm=scale.norm,
            extend="neither",
        )

        if show_contour_lines:
            if contour_levels is None:
                contour_levels = MaxNLocator(nbins=8).tick_values(
                    float(np.min(self.values)), float(np.max(self.values))
                )
                contour_levels = contour_levels[
                    (contour_levels >= np.min(self.values))
                    & (contour_levels <= np.max(self.values))
                ]
            lines = axes.tricontour(
                self.triangulation,
                self.values,
                levels=contour_levels,
                colors=contour_linecolor,
                linewidths=contour_linewidth,
            )
            if contour_labels:
                axes.clabel(lines, inline=True, fontsize=8, fmt="%.2g")

        if show_points:
            axes.scatter(
                self.x_plot,
                self.y_plot,
                s=point_size,
                facecolors=point_facecolor,
                edgecolors=point_edgecolor,
                linewidths=point_linewidth,
                zorder=5,
            )

        self._configure_axis(axes, "x")
        self._configure_axis(axes, "y")
        axes.set_xlim(np.min(self.x_plot), np.max(self.x_plot))
        axes.set_ylim(np.min(self.y_plot), np.max(self.y_plot))
        axes.grid(True, which="major", linestyle=":", linewidth=0.5, alpha=0.45)
        return filled
