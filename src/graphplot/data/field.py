"""VTK field data wrapper used by contour, mesh, vector and streamline plots."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import numpy as np


class FieldData:
    """A PyVista dataset together with field-selection helpers.

    The wrapper keeps PyVista optional at the API level: users can pass a
    :class:`FieldData` object, a VTP path, or the raw vector/scalar name
    directly to plotting methods.
    """

    def __init__(self, dataset, filename: str | Path | None = None) -> None:
        self.dataset = dataset
        self.filename = None if filename is None else Path(filename)

    @property
    def point_data(self) -> dict[str, np.ndarray]:
        """Point-associated arrays."""
        return dict(self.dataset.point_data)

    @property
    def cell_data(self) -> dict[str, np.ndarray]:
        """Cell-associated arrays."""
        return dict(self.dataset.cell_data)

    @property
    def fields(self) -> dict[str, str]:
        """Mapping from field name to association (``point`` or ``cell``)."""
        fields: dict[str, str] = {}
        for name in self.point_data:
            fields[name] = "point"
        for name in self.cell_data:
            fields.setdefault(name, "cell")
        return fields

    @property
    def bounds(self) -> tuple[float, float, float, float, float, float]:
        """Dataset bounds ``(xmin, xmax, ymin, ymax, zmin, zmax)``."""
        return tuple(float(value) for value in self.dataset.bounds)

    @property
    def bounds2d(self) -> tuple[float, float, float, float]:
        """XY bounds ``(xmin, xmax, ymin, ymax)``."""
        xmin, xmax, ymin, ymax, _, _ = self.bounds
        return xmin, xmax, ymin, ymax

    @property
    def n_points(self) -> int:
        """Number of mesh points."""
        return int(self.dataset.n_points)

    @property
    def n_cells(self) -> int:
        """Number of mesh cells."""
        return int(self.dataset.n_cells)

    @property
    def points(self) -> np.ndarray:
        """Point coordinates as an ``(n, 3)`` array."""
        return np.asarray(self.dataset.points)

    @property
    def cell_centers(self) -> np.ndarray:
        """Cell-centre coordinates as an ``(n, 3)`` array."""
        return np.asarray(self.dataset.cell_centers().points)

    def vectors(
        self,
        name: str,
        association: str = "auto",
    ) -> tuple[np.ndarray, np.ndarray]:
        """Return coordinates and vector components for a vector field.

        Returns ``(coordinates, vectors)`` where ``coordinates`` has shape
        ``(n, 3)`` and ``vectors`` has shape ``(n, 2)`` or ``(n, 3)``.
        """
        if association not in ("auto", "cell", "point"):
            raise ValueError("association must be 'auto', 'cell' or 'point'.")
        if association == "auto":
            association = self.association(name)

        if association == "cell":
            values = np.asarray(self.dataset.cell_data[name])
            coordinates = self.cell_centers
        else:
            values = np.asarray(self.dataset.point_data[name])
            coordinates = self.points

        if values.ndim != 2 or values.shape[1] < 2:
            raise ValueError(
                f"Field {name!r} is not a vector field with at least two components."
            )
        return coordinates, values

    def association(self, name: str) -> str:
        """Return ``'cell'`` or ``'point'`` for a field name."""
        if name in self.dataset.cell_data:
            return "cell"
        if name in self.dataset.point_data:
            return "point"
        available = ", ".join(self.fields) or "<none>"
        raise KeyError(f"Field {name!r} not found. Available fields: {available}")

    def field(
        self,
        name: str,
        association: str = "auto",
        component: str | int | None = None,
    ) -> np.ndarray:
        """Return a scalar field.

        Parameters
        ----------
        name
            Field name.
        association
            ``"auto"``, ``"cell"`` or ``"point"``. With ``"auto"`` cell data is
            preferred when a name exists in both locations.
        component
            For vector fields, select ``"x"``, ``"y"``, ``"z"`` or an integer
            component.
        """
        if association not in ("auto", "cell", "point"):
            raise ValueError("association must be 'auto', 'cell' or 'point'.")

        if association == "auto":
            association = self.association(name)
        elif association == "cell" and name not in self.dataset.cell_data:
            available = ", ".join(self.dataset.cell_data) or "<none>"
            raise KeyError(
                f"Cell field {name!r} not found. Available cell fields: {available}"
            )
        elif association == "point" and name not in self.dataset.point_data:
            available = ", ".join(self.dataset.point_data) or "<none>"
            raise KeyError(
                f"Point field {name!r} not found. Available point fields: {available}"
            )

        data = (
            self.dataset.cell_data[name]
            if association == "cell"
            else self.dataset.point_data[name]
        )
        values = np.asarray(data)

        if component is not None:
            values = _select_component(values, component, name)

        if values.ndim == 1:
            return values.astype(float, copy=False)
        if values.ndim == 2 and values.shape[1] == 1:
            return values[:, 0].astype(float, copy=False)
        if values.ndim == 2:
            raise ValueError(
                f"Field {name!r} has {values.shape[1]} components. "
                "Select one with component='x', 'y', 'z' or an integer."
            )
        raise ValueError(f"Field {name!r} has unsupported shape {values.shape}.")

    def cell_indices(self) -> list[np.ndarray]:
        """Return the point indices of every cell."""
        faces = getattr(self.dataset, "faces", None)
        if faces is not None:
            faces = np.asarray(faces)
            cells: list[np.ndarray] = []
            index = 0
            while index < len(faces):
                n_points = int(faces[index])
                if n_points <= 0:
                    break
                cells.append(faces[index + 1 : index + 1 + n_points])
                index += n_points + 1
            if len(cells) == self.n_cells:
                return cells

        connectivity = np.asarray(self.dataset.cell_connectivity)
        offsets = np.asarray(self.dataset.offset)
        cells = []
        for cell_id in range(self.dataset.n_cells):
            start = int(offsets[cell_id])
            stop = int(offsets[cell_id + 1])
            cells.append(connectivity[start:stop])
        return cells

    def cell_polygons(self) -> list[np.ndarray]:
        """Return each cell as an ``(n, 2)`` polygon of XY coordinates."""
        points = self.points
        return [points[cell][:, :2] for cell in self.cell_indices()]

    def triangles(self) -> np.ndarray:
        """Return a fan triangulation of all cells as an ``(n, 3)`` array."""
        triangles: list[tuple[int, int, int]] = []
        for cell in self.cell_indices():
            if len(cell) < 3:
                continue
            for index in range(1, len(cell) - 1):
                triangles.append((int(cell[0]), int(cell[index]), int(cell[index + 1])))
        return np.asarray(triangles, dtype=int).reshape(-1, 3)

    def iter_cell_polygons(self) -> Iterator[np.ndarray]:
        """Yield cell polygons one at a time."""
        yield from self.cell_polygons()

    def __repr__(self) -> str:
        source = "" if self.filename is None else f", file={self.filename.name!r}"
        return (
            f"FieldData(points={self.n_points}, cells={self.n_cells}, "
            f"fields={list(self.fields)}{source})"
        )


def _select_component(
    values: np.ndarray, component: str | int, name: str
) -> np.ndarray:
    if values.ndim != 2:
        raise ValueError(f"component was requested but field {name!r} is scalar.")
    if isinstance(component, str):
        index = {"x": 0, "y": 1, "z": 2}.get(component.lower())
        if index is None:
            raise ValueError("component must be 'x', 'y', 'z' or an integer.")
    else:
        index = int(component)
    if index < 0 or index >= values.shape[1]:
        raise IndexError(
            f"Component {component!r} is out of range for field {name!r} "
            f"with {values.shape[1]} components."
        )
    return values[:, index]
