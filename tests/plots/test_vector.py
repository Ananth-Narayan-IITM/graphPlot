import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv
from matplotlib.quiver import Quiver

from postprocess.plots.vector import VectorPlot

# =========================================================
# Test data
# =========================================================


def make_vector_dataset():

    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [2.0, 0.0, 0.0],
            [2.0, 1.0, 0.0],
        ]
    )

    faces = np.hstack(
        [
            [4, 0, 1, 2, 3],
            [4, 1, 4, 5, 2],
        ]
    )

    mesh = pv.PolyData(
        points,
        faces,
    )

    mesh.cell_data["U"] = np.array(
        [
            [2.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
        ]
    )

    return mesh


# =========================================================
# Creation
# =========================================================


def test_vector_plot_creation():

    data = make_vector_dataset()

    plot = VectorPlot(
        data,
        field="U",
        association="cell",
    )

    assert plot.data is data
    assert plot.field == "U"


# =========================================================
# Plot
# =========================================================


def test_vector_plot_returns_quiver():

    data = make_vector_dataset()

    plot = VectorPlot(
        data,
        field="U",
        association="cell",
    )

    figure, axes = plt.subplots()

    vectors = plot.plot(
        axes,
        normalize=False,
        density=2,
        scale=20,
        width=0.002,
        color="black",
    )

    assert isinstance(
        vectors,
        Quiver,
    )

    plt.close(figure)


# =========================================================
# Vector magnitude
# =========================================================


def test_vector_plot_preserves_magnitude():

    data = make_vector_dataset()

    plot = VectorPlot(
        data,
        field="U",
        association="cell",
    )

    class DummyAxes:
        def quiver(
            self,
            x,
            y,
            u,
            v,
            **kwargs,
        ):

            return {
                "u": np.asarray(u),
                "v": np.asarray(v),
            }

    axes = DummyAxes()

    result = plot.plot(
        axes,
        normalize=False,
        density=2,
        scale=1,
    )

    magnitudes = np.sqrt(result["u"] ** 2 + result["v"] ** 2)

    assert np.allclose(
        magnitudes,
        [
            2.0,
            np.sqrt(2.0),
        ],
    )


# =========================================================
# Vector normalization
# =========================================================


def test_vector_normalization():

    data = make_vector_dataset()

    plot = VectorPlot(
        data,
        field="U",
        association="cell",
    )

    class DummyAxes:
        def quiver(
            self,
            x,
            y,
            u,
            v,
            **kwargs,
        ):

            return {
                "u": np.asarray(u),
                "v": np.asarray(v),
            }

    axes = DummyAxes()

    result = plot.plot(
        axes,
        normalize=True,
        density=2,
        scale=1,
    )

    magnitudes = np.sqrt(result["u"] ** 2 + result["v"] ** 2)

    assert np.allclose(
        magnitudes,
        1.0,
    )
