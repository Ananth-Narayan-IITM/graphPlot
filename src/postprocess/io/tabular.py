from pathlib import Path

import numpy as np

from postprocess.data.data1d import Data1D


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
    """
    Read two-column 1D scientific data.

    Parameters
    ----------
    filename:
        Input file.

    x_column:
        Column containing x data.

    y_column:
        Column containing y data.

    delimiter:
        Column delimiter.

        None:
            whitespace separated

        ",":
            CSV

    skiprows:
        Number of rows to skip.

    comments:
        Comment character.
    """

    filename = Path(filename)

    if not filename.exists():
        raise FileNotFoundError(f"File not found: {filename}")

    data = np.loadtxt(
        filename,
        delimiter=delimiter,
        skiprows=skiprows,
        comments=comments,
    )

    if data.ndim != 2:
        raise ValueError("Expected a tabular dataset.")

    n_columns = data.shape[1]

    if x_column >= n_columns:
        raise IndexError(f"x_column={x_column} but file contains {n_columns} columns.")

    if y_column >= n_columns:
        raise IndexError(f"y_column={y_column} but file contains {n_columns} columns.")

    return Data1D(
        x=data[:, x_column],
        y=data[:, y_column],
        label=label,
        x_label=x_label,
        y_label=y_label,
        x_unit=x_unit,
        y_unit=y_unit,
        metadata={
            "filename": str(filename),
        },
    )
