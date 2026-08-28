import numpy as np

import matplotlib.pyplot as plt

from matplotlib.collections import PolyCollection

from postprocess.data.mesh import Mesh
from postprocess.data.dataset import DataSet
from postprocess.plots.mesh import MeshPlot


# =========================================================
# Fixtures / test data
# =========================================================

def make_test_dataset():

    points = np.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [1.0, 1.0],
        [0.0, 1.0],
        [2.0, 0.0],
        [2.0, 1.0],
    ])

    cells = [
        [0, 1, 2, 3],
        [1, 4, 5, 2],
    ]

    mesh = Mesh(
        points=points,
        cells=cells,
    )

    return DataSet(
        mesh=mesh,
    )


# =========================================================
# Creation
# =========================================================

def test_mesh_plot_creation():

    data = make_test_dataset()

    plot = MeshPlot(
        data
    )

    assert plot.data is data
    assert plot.mesh is data.mesh


# =========================================================
# Plot
# =========================================================

def test_mesh_plot_returns_collection():

    data = make_test_dataset()

    plot = MeshPlot(
        data
    )

    figure, axes = plt.subplots()

    collection = plot.plot(
        axes
    )

    assert isinstance(
        collection,
        PolyCollection,
    )

    plt.close(figure)


# =========================================================
# Geometry
# =========================================================

def test_mesh_plot_contains_all_cells():

    data = make_test_dataset()

    plot = MeshPlot(
        data
    )

    figure, axes = plt.subplots()

    collection = plot.plot(
        axes
    )

    assert len(
        collection.get_paths()
    ) == data.mesh.n_cells

    plt.close(figure)


# =========================================================
# Axis limits
# =========================================================

def test_mesh_plot_sets_axis_limits():

    data = make_test_dataset()

    plot = MeshPlot(
        data
    )

    figure, axes = plt.subplots()

    plot.plot(
        axes
    )

    assert axes.get_xlim() == (
        0.0,
        2.0,
    )

    assert axes.get_ylim() == (
        0.0,
        1.0,
    )

    plt.close(figure)


# =========================================================
# Styling
# =========================================================

def test_mesh_plot_edge_and_face_style():

    data = make_test_dataset()

    plot = MeshPlot(
        data
    )

    figure, axes = plt.subplots()

    collection = plot.plot(
        axes,
        edgecolor="black",
        facecolor="none",
        linewidth=0.15,
        alpha=0.35,
    )

    # No face should be painted by the mesh.
    assert collection.get_facecolors().size == 0

    # Cell boundaries should be black.
    edgecolors = collection.get_edgecolors()

    assert edgecolors.shape[0] == 1

    assert np.allclose(
        edgecolors[0][:3],
        [0.0, 0.0, 0.0],
    )

    # Requested transparency.
    assert collection.get_alpha() == 0.35

    # Requested line width.
    assert np.isclose(
        collection.get_linewidths()[0],
        0.15,
    )

    plt.close(figure)


# =========================================================
# Rasterization
# =========================================================

def test_mesh_can_be_rasterized():

    data = make_test_dataset()

    plot = MeshPlot(
        data
    )

    figure, axes = plt.subplots()

    collection = plot.plot(
        axes,
        edgecolor="black",
        facecolor="none",
    )

    collection.set_rasterized(
        True
    )

    assert collection.get_rasterized() is True

    plt.close(figure)