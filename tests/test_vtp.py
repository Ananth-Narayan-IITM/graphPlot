from __future__ import annotations

import numpy as np

import graphplot as gp


def test_load_vtp_fields():
    data = gp.load("data/zNormal.vtp")
    assert isinstance(data, gp.FieldData)
    assert data.n_points > 0
    assert data.n_cells > 0
    assert "gammaDV" in data.fields
    assert data.association("gammaDV") == "cell"

    values = data.field("gammaDV")
    assert values.shape == (data.n_cells,)
    assert np.isfinite(values).all()

    polygons = data.cell_polygons()
    assert len(polygons) == data.n_cells
    assert polygons[0].shape[1] == 2


def test_vector_component_selection():
    data = gp.load("data/zNormal.vtp")
    assert data.field("U", component="x").shape == (data.n_cells,)
    assert data.field("U", component=1).shape == (data.n_cells,)


def test_bounds():
    data = gp.load("data/zNormal.vtp")
    xmin, xmax, ymin, ymax = data.bounds2d
    assert xmin < xmax
    assert ymin < ymax
