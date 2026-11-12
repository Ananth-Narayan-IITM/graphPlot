"""Named-column tabular data."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import Any

import numpy as np

from graphplot.data.series import Data1D


class Table(Mapping[str, np.ndarray]):
    """Named numeric columns with optional units.

    Parameters
    ----------
    columns
        Mapping from column name to one-dimensional values.
    units
        Optional mapping from column name to unit string.
    metadata
        Optional metadata such as the source filename.
    """

    def __init__(
        self,
        columns: Mapping[str, np.ndarray],
        units: Mapping[str, str] | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        if not columns:
            raise ValueError("The table contains no columns.")
        self._columns = {
            str(name): np.asarray(values, dtype=float)
            for name, values in columns.items()
        }
        lengths = {len(values) for values in self._columns.values()}
        if len(lengths) != 1:
            raise ValueError("All columns must contain the same number of rows.")
        self.units = dict(units or {})
        self.metadata = dict(metadata or {})

    def __getitem__(self, name: str) -> np.ndarray:
        try:
            return self._columns[name]
        except KeyError as exc:
            available = ", ".join(self._columns)
            raise KeyError(
                f"Column {name!r} not found. Available: {available}"
            ) from exc

    def __iter__(self) -> Iterator[str]:
        return iter(self._columns)

    def __len__(self) -> int:
        return len(self._columns)

    @property
    def columns(self) -> tuple[str, ...]:
        """Column names in input order."""
        return tuple(self._columns)

    @property
    def n_rows(self) -> int:
        """Number of rows."""
        return len(next(iter(self._columns.values())))

    def series(
        self,
        x: str | int,
        y: str | int,
        *,
        label: str | None = None,
        x_label: str | None = None,
        y_label: str | None = None,
    ) -> Data1D:
        """Build a :class:`Data1D` from two columns."""
        x_name = self._resolve_name(x)
        y_name = self._resolve_name(y)
        return Data1D(
            self[x_name],
            self[y_name],
            label=label if label is not None else y_name,
            x_label=x_label if x_label is not None else x_name,
            y_label=y_label if y_label is not None else y_name,
            metadata={"units": dict(self.units), **self.metadata},
        )

    def _resolve_name(self, key: str | int) -> str:
        if isinstance(key, int):
            try:
                return self.columns[key]
            except IndexError as exc:
                raise IndexError(f"Column index {key} is out of range.") from exc
        if key not in self._columns:
            available = ", ".join(self._columns)
            raise KeyError(f"Column {key!r} not found. Available: {available}")
        return key

    def info(self) -> str:
        """Return a short human-readable summary."""
        lines = [f"Table: {self.n_rows} rows, {len(self)} columns"]
        for name in self.columns:
            unit = self.units.get(name)
            suffix = f" [{unit}]" if unit else ""
            lines.append(f"  {name}{suffix}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"Table(rows={self.n_rows}, columns={list(self.columns)})"
