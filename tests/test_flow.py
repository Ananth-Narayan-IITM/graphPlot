from __future__ import annotations

from matplotlib.collections import LineCollection
from matplotlib.quiver import Quiver

import graphplot as gp


def test_velocity_vectors():
    data = gp.load("data/zNormal.vtp")
    fig = gp.Figure()
    fig.vectors(data, "U", density=8, min_magnitude=0.03)
    assert isinstance(fig.last_artist, Quiver)
    fig.close()


def test_streamlines():
    data = gp.load("data/zNormal.vtp")
    fig = gp.Figure()
    fig.streamlines(
        data,
        "U",
        seed_axis="y",
        seed_position=2.5,
        n_seeds=5,
        integration_direction="both",
    )
    assert isinstance(fig.last_artist, LineCollection)
    assert len(fig.last_artist.get_segments()) > 0
    fig.close()
