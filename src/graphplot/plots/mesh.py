"""Computational mesh overlay."""

from __future__ import annotations

from matplotlib.collections import PolyCollection

from graphplot.data.field import FieldData


def plot_mesh(
    axes,
    data: FieldData,
    *,
    edgecolor: str = "black",
    facecolor: str = "none",
    linewidth: float = 0.15,
    alpha: float = 0.3,
    rasterize: bool = False,
    **kwargs,
) -> PolyCollection:
    """Overlay the original mesh on an axes."""
    collection = PolyCollection(
        data.cell_polygons(),
        facecolors=facecolor,
        edgecolors=edgecolor,
        linewidths=linewidth,
        alpha=alpha,
        **kwargs,
    )
    collection.set_rasterized(bool(rasterize))
    axes.add_collection(collection)
    xmin, xmax, ymin, ymax = data.bounds2d
    axes.set_xlim(xmin, xmax)
    axes.set_ylim(ymin, ymax)
    axes.set_aspect("equal", adjustable="box")
    axes.grid(False)
    return collection
