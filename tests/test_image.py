from __future__ import annotations

import matplotlib.image as mpimg

import graphplot as gp


def test_reference_image():
    fig = gp.Figure(width=3.0, height=3.0)
    fig.image("data/ref1.jpg")
    assert isinstance(fig.last_artist, mpimg.AxesImage)
    fig.close()
