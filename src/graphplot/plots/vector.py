"""Velocity-vector arrows."""

from __future__ import annotations

import numpy as np

from graphplot.data.field import FieldData


def plot_vectors(
    axes,
    data: FieldData,
    field: str,
    *,
    association: str = "auto",
    density: int | None = 20,
    scale: float | str = "auto",
    length: float = 0.1,
    reference_percentile: float = 90.0,
    min_magnitude: float = 0.0,
    normalize: bool = False,
    color: str = "black",
    magnitude_color: bool = False,
    cmap: str = "viridis",
    width: float = 0.0025,
    alpha: float = 1.0,
    pivot: str = "mid",
    zorder: int = 5,
    **kwargs,
):
    """Draw a 2D velocity field as arrows.

    Parameters
    ----------
    density
        Approximate number of arrows along the smaller spatial dimension.
        ``None`` draws every vector.
    scale
        ``"auto"`` (default) chooses a scale so the longest arrow is roughly
        ``length`` times the smaller domain dimension. A number is passed
        directly to Matplotlib's quiver scale.
    length
        Target arrow length for the reference magnitude, as a fraction of the
        smaller domain dimension when ``scale="auto"``.
    reference_percentile
        Magnitude percentile used as the reference for automatic scaling.
        The default 90 makes most vectors visible while allowing the strongest
        vectors to be longer.
    min_magnitude
        Hide vectors below this magnitude. Useful for suppressing near-zero
        arrows in solid or stagnant regions.
    normalize
        Draw unit-length arrows while preserving the original direction.
    magnitude_color
        Color arrows by the original vector magnitude.
    """
    coordinates, vectors = data.vectors(field, association=association)
    x = coordinates[:, 0]
    y = coordinates[:, 1]
    u = vectors[:, 0]
    v = vectors[:, 1]

    magnitude = np.hypot(u, v)
    valid = (
        np.isfinite(x)
        & np.isfinite(y)
        & np.isfinite(u)
        & np.isfinite(v)
        & (magnitude >= float(min_magnitude))
    )
    x, y, u, v = x[valid], y[valid], u[valid], v[valid]
    magnitude = magnitude[valid]
    if x.size == 0:
        raise ValueError(
            f"Vector field {field!r} has no finite values above min_magnitude."
        )

    color_values = magnitude.copy() if magnitude_color else None

    if normalize:
        nonzero = magnitude > 0
        u = np.zeros_like(u)
        v = np.zeros_like(v)
        u[nonzero] = vectors[valid, 0][nonzero] / magnitude[nonzero]
        v[nonzero] = vectors[valid, 1][nonzero] / magnitude[nonzero]
        magnitude = np.hypot(u, v)

    if density is not None:
        selected = _downsample_indices(x, y, int(density))
        x, y, u, v = x[selected], y[selected], u[selected], v[selected]
        magnitude = magnitude[selected]
        if color_values is not None:
            color_values = color_values[selected]

    xmin, xmax, ymin, ymax = data.bounds2d
    if scale == "auto":
        if not 0.0 < reference_percentile <= 100.0:
            raise ValueError("reference_percentile must be in (0, 100].")
        reference = float(np.percentile(magnitude, reference_percentile))
        if reference <= 0:
            raise ValueError(f"Vector field {field!r} has zero magnitude.")
        target = float(length) * min(xmax - xmin, ymax - ymin)
        if target <= 0:
            raise ValueError("The data bounds are degenerate.")
        scale = reference / target
    elif not isinstance(scale, (int, float)):
        raise ValueError("scale must be 'auto' or a number.")

    quiver_kwargs = {
        "angles": "xy",
        "scale_units": "xy",
        "scale": scale,
        "width": width,
        "alpha": alpha,
        "pivot": pivot,
        "zorder": zorder,
    }
    quiver_kwargs.update(kwargs)

    if color_values is None:
        quiver = axes.quiver(x, y, u, v, color=color, **quiver_kwargs)
    else:
        quiver = axes.quiver(
            x,
            y,
            u,
            v,
            color_values,
            cmap=cmap,
            **quiver_kwargs,
        )

    axes.set_xlim(xmin, xmax)
    axes.set_ylim(ymin, ymax)
    axes.set_aspect("equal", adjustable="box")
    axes.grid(False)
    return quiver


def _downsample_indices(x, y, density):
    if density < 1:
        raise ValueError("density must be greater than zero, or None.")
    xmin, xmax = float(np.min(x)), float(np.max(x))
    ymin, ymax = float(np.min(y)), float(np.max(y))
    width = xmax - xmin
    height = ymax - ymin
    if width <= 0 or height <= 0:
        return np.arange(x.size)

    if width >= height:
        nx = density
        ny = max(1, int(density * height / width))
    else:
        ny = density
        nx = max(1, int(density * width / height))

    dx = width / nx
    dy = height / ny
    ix = np.clip(np.floor((x - xmin) / dx).astype(int), 0, nx - 1)
    iy = np.clip(np.floor((y - ymin) / dy).astype(int), 0, ny - 1)
    bins = iy * nx + ix

    selected: list[int] = []
    for identifier in np.unique(bins):
        indices = np.where(bins == identifier)[0]
        center_x = float(np.mean(x[indices]))
        center_y = float(np.mean(y[indices]))
        distance = (x[indices] - center_x) ** 2 + (y[indices] - center_y) ** 2
        selected.append(int(indices[np.argmin(distance)]))
    return np.asarray(selected, dtype=int)
