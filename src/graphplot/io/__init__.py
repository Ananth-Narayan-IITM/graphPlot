"""Input readers."""

from graphplot.io.load import load, load_field, load_table
from graphplot.io.tabular import read_1d, read_numpy, read_table
from graphplot.io.vtk import read_vtk

__all__ = [
    "load",
    "load_field",
    "load_table",
    "read_1d",
    "read_numpy",
    "read_table",
    "read_vtk",
]
