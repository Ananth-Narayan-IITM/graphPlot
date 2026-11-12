"""Streamlines generated with the PyVista/VTK integrator."""

from __future__ import annotations

import numpy as np
from matplotlib.collections import LineCollection

from graphplot.data.field import FieldData


def plot_streamlines(
    axes,
    data: FieldData,
    field: str,
    *,
    association: str = "auto",
    seed_points=None,
    n_seeds: int = 20,
    seed_axis: str = "y",
    seed_position: float | None = None,
    seed_margin: float = 0.02,
    integration_direction: str = "forward",
    integrator_type: int = 45,
    surface_streamlines: bool = True,
    initial_step_length: float = 0.1,
    min_step_length: float = 0.01,
    max_step_length: float = 0.5,
    max_steps: int = 2000,
    terminal_speed: float = 1e-12,
    max_error: float = 1e-6,
    interpolator_type: str = "cell",
    color: str = "black",
    linewidth: float = 0.8,
    arrowsize: float = 1.0,
    zorder: int = 6,
) -> LineCollection:
    """Generate streamlines from a vector field and plot them as lines."""
    import pyvista as pv

    if integration_direction not in ("forward", "backward", "both"):
        raise ValueError(
            "integration_direction must be 'forward', 'backward' or 'both'."
        )
    if integrator_type not in (2, 4, 45):
        raise ValueError("integrator_type must be 2, 4 or 45.")

    if association == "auto":
        association = data.association(field)

    if association == "cell":
        mesh = data.dataset.cell_data_to_point_data(pass_cell_data=True)
    else:
        mesh = data.dataset.copy()
    mesh.set_active_vectors(field, preference="point")

    if seed_points is None:
        points = _seed_points(
            data.bounds,
            n_seeds=n_seeds,
            seed_axis=seed_axis,
            seed_position=seed_position,
            seed_margin=seed_margin,
        )
    else:
        points = np.asarray(seed_points, dtype=float)
        if points.ndim != 2 or points.shape[1] not in (2, 3):
            raise ValueError("seed_points must have shape (N, 2) or (N, 3).")
        if points.shape[1] == 2:
            zmid = 0.5 * (data.bounds[4] + data.bounds[5])
            points = np.column_stack((points, np.full(len(points), zmid)))

    source = pv.PolyData(points)
    streamlines = mesh.streamlines_from_source(
        source,
        vectors=field,
        integrator_type=integrator_type,
        integration_direction=integration_direction,
        surface_streamlines=surface_streamlines,
        initial_step_length=initial_step_length,
        min_step_length=min_step_length,
        max_step_length=max_step_length,
        max_steps=max_steps,
        terminal_speed=terminal_speed,
        max_error=max_error,
        interpolator_type=interpolator_type,
        compute_vorticity=False,
    )
    if streamlines.n_points == 0:
        raise RuntimeError(
            "VTK generated no streamlines. Check the seed line and vector field."
        )

    raw_lines = np.asarray(streamlines.lines)
    segments: list[np.ndarray] = []
    offset = 0
    while offset < len(raw_lines):
        n_points = int(raw_lines[offset])
        ids = raw_lines[offset + 1 : offset + 1 + n_points]
        segment = np.asarray(streamlines.points[ids])[:, :2]
        if len(segment) >= 2:
            segments.append(segment)
        offset += n_points + 1

    collection = LineCollection(
        segments,
        colors=color,
        linewidths=linewidth,
        zorder=zorder,
    )
    axes.add_collection(collection)

    if arrowsize > 0:
        zmid = 0.5 * (data.bounds[4] + data.bounds[5])
        for segment in segments:
            if len(segment) < 4:
                continue
            middle = len(segment) // 2
            p0 = segment[middle - 1]
            p1 = segment[middle]
            direction = p1 - p0

            # Polyline point order depends on the integration direction. Use
            # the local velocity to orient the arrow, so backward-integrated
            # segments do not show reversed arrows.
            point_id = mesh.find_closest_point((p1[0], p1[1], zmid))
            velocity = np.asarray(mesh.point_data[field][point_id])[:2]
            if np.dot(direction, velocity) < 0:
                p0, p1 = p1, p0

            axes.annotate(
                "",
                xy=p1,
                xytext=p0,
                arrowprops={
                    "arrowstyle": "-|>",
                    "color": color,
                    "lw": linewidth,
                    "mutation_scale": 8.0 * arrowsize,
                },
                zorder=zorder + 1,
            )

    xmin, xmax, ymin, ymax = data.bounds2d
    axes.set_xlim(xmin, xmax)
    axes.set_ylim(ymin, ymax)
    axes.set_aspect("equal", adjustable="box")
    axes.grid(False)
    return collection


def _seed_points(
    bounds,
    *,
    n_seeds: int,
    seed_axis: str,
    seed_position: float | None,
    seed_margin: float,
) -> np.ndarray:
    xmin, xmax, ymin, ymax, zmin, zmax = bounds
    if n_seeds < 1:
        raise ValueError("n_seeds must be greater than zero.")
    if seed_axis not in ("x", "y"):
        raise ValueError("seed_axis must be 'x' or 'y'.")
    if not 0.0 <= seed_margin < 0.5:
        raise ValueError("seed_margin must be in [0, 0.5).")

    if seed_position is None:
        seed_position = xmin if seed_axis == "y" else ymin

    zmid = 0.5 * (zmin + zmax)
    if seed_axis == "y":
        span = ymax - ymin
        values = np.linspace(
            ymin + seed_margin * span, ymax - seed_margin * span, n_seeds
        )
        return np.column_stack(
            (np.full(n_seeds, seed_position), values, np.full(n_seeds, zmid))
        )

    span = xmax - xmin
    values = np.linspace(xmin + seed_margin * span, xmax - seed_margin * span, n_seeds)
    return np.column_stack(
        (values, np.full(n_seeds, seed_position), np.full(n_seeds, zmid))
    )
