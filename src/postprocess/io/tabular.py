"""Readers for tabular scientific data."""

from collections.abc import Mapping
from pathlib import Path

import numpy as np

from postprocess.data.data1d import Data1D


class TabularData(Mapping):
    """Named columns read from a CSV or whitespace-delimited text file.

    Columns are available using ``data["column_name"]`` or
    ``data.get_column("column_name")``. The object intentionally has no pandas
    dependency and stores each column as a NumPy array.
    """

    def __init__(self, columns, metadata=None):
        if not columns:
            raise ValueError("The input table contains no columns.")

        self._columns = {
            str(name): np.asarray(values) for name, values in columns.items()
        }
        lengths = {len(values) for values in self._columns.values()}
        if len(lengths) != 1:
            raise ValueError("All table columns must have the same number of rows.")

        self.metadata = dict(metadata or {})

    def __getitem__(self, name):
        try:
            return self._columns[name]
        except KeyError as exc:
            available = ", ".join(self._columns)
            raise KeyError(
                f"Column {name!r} not found. Available columns: {available}"
            ) from exc

    def __iter__(self):
        return iter(self._columns)

    def __len__(self):
        return len(self._columns)

    @property
    def columns(self):
        """Column names in the order they appeared in the input."""
        return tuple(self._columns)

    @property
    def n_rows(self):
        """Number of data rows."""
        return len(next(iter(self._columns.values())))

    def get_column(self, name):
        """Return a named column as a NumPy array."""
        return self[name]


def read_table(filename, delimiter=None, skiprows=0, comments="#", names=True):
    """Read a named-column CSV or whitespace-delimited data table.

    Parameters
    ----------
    filename : str or pathlib.Path
        Path to the input file. The first non-skipped, non-comment line is
        interpreted as the header when ``names=True``.
    delimiter : str or None, optional
        Column separator. ``None`` means arbitrary whitespace. If omitted,
        comma-separated input is selected for ``.csv`` files and whitespace
        separation is used for other extensions.
    skiprows : int, optional
        Number of physical rows to skip before parsing.
    comments : str or None, optional
        Comment marker understood by NumPy's text reader.
    names : bool, optional
        Whether the first data row contains column names. Defaults to ``True``.

    Returns
    -------
    TabularData
        Named NumPy columns and source-file metadata.
    """
    path = Path(filename)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    if delimiter is None and path.suffix.lower() == ".csv":
        delimiter = ","

    loaded = np.genfromtxt(
        path,
        delimiter=delimiter,
        skip_header=skiprows,
        comments=comments,
        names=names,
        dtype=float if not names else None,
        encoding="utf-8",
        autostrip=True,
    )

    if names:
        if loaded.dtype.names is None:
            raise ValueError(f"Could not read column names from {path}.")
        loaded = np.atleast_1d(loaded)
        columns = {name: np.asarray(loaded[name]) for name in loaded.dtype.names}
    else:
        matrix = np.asarray(loaded)
        if matrix.ndim == 1:
            matrix = matrix.reshape(1, -1)
        columns = {f"column_{i}": matrix[:, i] for i in range(matrix.shape[1])}

    if not columns or any(np.asarray(col).size == 0 for col in columns.values()):
        raise ValueError(f"No data rows found in {path}.")

    return TabularData(columns, metadata={"filename": str(path.resolve())})


def read_1d(
    filename,
    x_column=0,
    y_column=1,
    delimiter=None,
    skiprows=0,
    comments="#",
    label=None,
    x_label=None,
    y_label=None,
    x_unit=None,
    y_unit=None,
):
    """Read two-column 1D scientific data (backward-compatible API)."""
    filename = Path(filename)
    if not filename.exists():
        raise FileNotFoundError(f"File not found: {filename}")

    data = np.loadtxt(
        filename,
        delimiter=delimiter,
        skiprows=skiprows,
        comments=comments,
        ndmin=2,
    )
    n_columns = data.shape[1]
    for name, index in (("x_column", x_column), ("y_column", y_column)):
        if index < 0 or index >= n_columns:
            raise IndexError(f"{name}={index} but file contains {n_columns} columns.")

    return Data1D(
        x=data[:, x_column],
        y=data[:, y_column],
        label=label,
        x_label=x_label,
        y_label=y_label,
        x_unit=x_unit,
        y_unit=y_unit,
        metadata={"filename": str(filename)},
    )
