import numpy as np

from postprocess.io.vtp import read_vtp

INPUT_FILE = "data/zNormal.vtp"


def test_read_vtp():

    data = read_vtp(INPUT_FILE)

    assert data is not None

    assert data.dataset is not None

    assert data.dataset.points is not None

    assert data.dataset.faces is not None


def test_vtp_expected_fields():

    data = read_vtp(INPUT_FILE)

    expected_fields = {
        "alpha",
        "gamma",
        "gammaDV",
        "p",
        "U",
    }

    assert expected_fields.issubset(set(data.dataset.cell_data.keys()))


def test_vtp_geometry():

    data = read_vtp(INPUT_FILE)

    points = data.dataset.points

    assert points.shape[0] == 9800

    assert points.shape[1] == 3


def test_vtp_gammaDV():

    data = read_vtp(INPUT_FILE)

    values = np.asarray(data.dataset.cell_data["gammaDV"])

    assert values.ndim == 1

    assert len(values) == 9603

    assert np.all(np.isfinite(values))
