"""One-dimensional series container."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class Data1D:
    """A one-dimensional x/y series with optional errors and metadata."""

    x: np.ndarray
    y: np.ndarray
    xerr: np.ndarray | None = None
    yerr: np.ndarray | None = None
    label: str | None = None
    x_label: str | None = None
    y_label: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.x = np.asarray(self.x, dtype=float)
        self.y = np.asarray(self.y, dtype=float)
        if self.x.ndim != 1 or self.y.ndim != 1:
            raise ValueError("x and y must be one-dimensional.")
        if len(self.x) != len(self.y):
            raise ValueError("x and y must have the same length.")
        if self.xerr is not None:
            self.xerr = np.asarray(self.xerr, dtype=float)
        if self.yerr is not None:
            self.yerr = np.asarray(self.yerr, dtype=float)

    def __len__(self) -> int:
        return len(self.x)

    def __repr__(self) -> str:
        return (
            f"Data1D(n={len(self)}, x=[{self.x.min():g}, {self.x.max():g}], "
            f"y=[{self.y.min():g}, {self.y.max():g}])"
        )

    def sorted(self) -> Data1D:
        """Return a copy sorted by x."""
        order = np.argsort(self.x)
        return Data1D(
            self.x[order],
            self.y[order],
            xerr=None if self.xerr is None else self.xerr[order],
            yerr=None if self.yerr is None else self.yerr[order],
            label=self.label,
            x_label=self.x_label,
            y_label=self.y_label,
            metadata=dict(self.metadata),
        )

    def finite(self) -> Data1D:
        """Return a copy containing only finite x/y points."""
        mask = np.isfinite(self.x) & np.isfinite(self.y)
        return Data1D(
            self.x[mask],
            self.y[mask],
            xerr=None if self.xerr is None else np.asarray(self.xerr)[mask],
            yerr=None if self.yerr is None else np.asarray(self.yerr)[mask],
            label=self.label,
            x_label=self.x_label,
            y_label=self.y_label,
            metadata=dict(self.metadata),
        )

    def scale_x(self, factor: float, label: str | None = None) -> Data1D:
        """Return a copy with x divided by ``factor``."""
        if factor == 0:
            raise ValueError("x scale cannot be zero.")
        return Data1D(
            self.x / factor,
            self.y.copy(),
            xerr=None if self.xerr is None else self.xerr / abs(factor),
            yerr=None if self.yerr is None else self.yerr.copy(),
            label=self.label,
            x_label=label or self.x_label,
            y_label=self.y_label,
            metadata=dict(self.metadata),
        )

    def scale_y(self, factor: float, label: str | None = None) -> Data1D:
        """Return a copy with y divided by ``factor``."""
        if factor == 0:
            raise ValueError("y scale cannot be zero.")
        return Data1D(
            self.x.copy(),
            self.y / factor,
            xerr=None if self.xerr is None else self.xerr.copy(),
            yerr=None if self.yerr is None else self.yerr / abs(factor),
            label=self.label,
            x_label=self.x_label,
            y_label=label or self.y_label,
            metadata=dict(self.metadata),
        )
