"""Scalar contour plotting."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import matplotlib as mpl
import matplotlib.tri as mtri
import numpy as np
from matplotlib.collections import PolyCollection
from matplotlib.colors import BoundaryNorm, Colormap, Normalize

from graphplot.data.field import FieldData


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
            self.norm = self.norm
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
    rasterize: bool | str = "auto",
    **kwargs,
) -> PolyCollection:
    """Draw a scalar field as filled polygons or a triangulated surface."""
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

    if resolved_association == "point":
        collection = _plot_point_contour(
            axes,
            data,
            values,
            scale,
            extend=extend,
            rasterize=rasterize,
            **kwargs,
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
        if rasterize is True or (rasterize == "auto" and data.n_cells > 50_000):
            collection.set_rasterized(True)
        axes.add_collection(collection)

    xmin, xmax, ymin, ymax = data.bounds2d
    axes.set_xlim(xmin, xmax)
    axes.set_ylim(ymin, ymax)
    axes.set_aspect("equal", adjustable="box")
    axes.grid(False)
    return collection


def _plot_point_contour(
    axes,
    data: FieldData,
    values: np.ndarray,
    scale: ColorScale,
    *,
    extend: str,
    rasterize: bool | str,
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

    if rasterize is True or (rasterize == "auto" and data.n_cells > 50_000):
        collection.set_rasterized(True)
    return collection
