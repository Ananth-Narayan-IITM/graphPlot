"""VTK/VTP readers."""

from __future__ import annotations

from pathlib import Path

from graphplot.data.field import FieldData


def read_vtk(filename: str | Path) -> FieldData:
    """Read a VTP, VTU or VTK file with PyVista."""
    path = Path(filename)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    try:
        import pyvista as pv
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise ImportError(
            "Reading VTP/VTU files requires PyVista. Install it with "
            "`pip install pyvista` or `pip install graphPlot`."
        ) from exc

    dataset = pv.read(path)
    if dataset.n_points == 0:
        raise ValueError(f"{path} contains no points.")
    return FieldData(dataset, filename=path)
