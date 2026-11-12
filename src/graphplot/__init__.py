"""graphPlot public API."""

from __future__ import annotations

from graphplot._checks import check
from graphplot.data.field import FieldData
from graphplot.data.series import Data1D
from graphplot.data.table import Table
from graphplot.figure import Figure
from graphplot.io.load import load, load_field, load_table
from graphplot.panel import Panel
from graphplot.project import Project
from graphplot.style import Style

__version__ = "2.0.0"

__all__ = [
    "Data1D",
    "FieldData",
    "Figure",
    "Panel",
    "Project",
    "Style",
    "Table",
    "check",
    "load",
    "load_field",
    "load_table",
]
