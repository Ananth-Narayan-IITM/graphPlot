"""Unified data loader."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from graphplot.data.field import FieldData
from graphplot.data.series import Data1D
from graphplot.data.table import Table
from graphplot.io.tabular import read_numpy, read_table
from graphplot.io.vtk import read_vtk

VTK_SUFFIXES = {".vtp", ".vtu", ".vtk", ".vtm"}
NUMPY_SUFFIXES = {".npy", ".npz"}


def load(filename: str | Path, **kwargs: Any) -> Table | FieldData | Data1D:
    """Load a dataset based on its file extension.

    Parameters
    ----------
    filename
        Input path. ``.vtp``/``.vtu``/``.vtk`` files become
        :class:`FieldData`; NumPy files become :class:`Table`; everything else
        is parsed as a CSV or whitespace table.
    kwargs
        Forwarded to the relevant reader.
    """
    if isinstance(filename, (Table, FieldData, Data1D)):
        return filename

    path = Path(filename)
    suffix = path.suffix.lower()
    if suffix in VTK_SUFFIXES:
        return read_vtk(path)
    if suffix in NUMPY_SUFFIXES:
        return read_numpy(path)
    return read_table(path, **kwargs)


def load_table(filename: str | Path, **kwargs: Any) -> Table:
    """Load a tabular file and require a :class:`Table` result."""
    data = load(filename, **kwargs)
    if not isinstance(data, Table):
        raise TypeError(f"{filename} did not produce a Table.")
    return data


def load_field(filename: str | Path) -> FieldData:
    """Load a VTK file and require a :class:`FieldData` result."""
    data = load(filename)
    if not isinstance(data, FieldData):
        raise TypeError(f"{filename} did not produce a FieldData.")
    return data
