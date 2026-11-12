from __future__ import annotations

import numpy as np

from graphplot.io.tabular import read_table


def test_read_named_columns():
    table = read_table("data/contour.dat")
    assert table.columns == ("Pr", "Ra", "nusseltNumber")
    assert table.n_rows == 18
    assert np.isclose(table["Pr"][0], 0.004)


def test_read_csv_with_units(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("x [m],u [m/s]\n0.0,1.0\n0.5,2.0\n1.0,3.0\n", encoding="utf-8")
    table = read_table(path)
    assert table.columns == ("x", "u")
    assert table.units == {"x": "m", "u": "m/s"}
    assert np.allclose(table["u"], [1.0, 2.0, 3.0])


def test_read_openfoam_vector_columns(tmp_path):
    path = tmp_path / "probe"
    path.write_text(
        "# Probe 0 (0.1 0.2 0)\n"
        "# Time        0             1\n"
        "0.0001  (0.10 0.20 0.00)  (0.30 0.40 0.00)\n"
        "0.0002  (0.11 0.21 0.00)  (0.31 0.41 0.00)\n",
        encoding="utf-8",
    )
    table = read_table(path)
    assert "0_x" in table.columns
    assert "0_y" in table.columns
    assert "1_z" in table.columns
    assert np.isclose(table["0_x"][1], 0.11)


def test_read_headerless_whitespace(tmp_path):
    path = tmp_path / "line.xy"
    path.write_text("0.0 1.0\n0.5 2.0\n1.0 3.0\n", encoding="utf-8")
    table = read_table(path)
    assert table.columns == ("column_0", "column_1")
    assert np.allclose(table["column_1"], [1.0, 2.0, 3.0])
