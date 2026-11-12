from __future__ import annotations

from graphplot.style import Style


def test_presets_and_overrides():
    style = Style.from_preset("ieee", font_size=7.5)
    assert style.preset == "ieee"
    assert style.font_size == 7.5
    assert style.dpi == 600
    assert style.color(0) == style.colors[0]
    assert style.marker(0) == style.markers[0]


def test_unknown_preset():
    try:
        Style.from_preset("does-not-exist")
    except ValueError as exc:
        assert "Unknown style preset" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_color_schemes():
    blackwhite = Style.from_preset("paper", color_scheme="blackwhite")
    assert blackwhite.colors == ("#000000",)
    assert blackwhite.contour_cmap == "Greys"

    grayscale = Style.from_preset("paper", color_scheme="grayscale")
    assert grayscale.contour_cmap == "Greys"
    assert len(set(grayscale.colors)) > 1

    colorblind = Style.from_preset("paper", color_scheme="colorblind")
    assert len(colorblind.colors) > 1
    assert colorblind.contour_cmap == "viridis"

    custom = Style.from_preset("paper", colors=("red", "blue"))
    assert custom.colors == ("red", "blue")


def test_color_scheme_switch_updates_derived_values():
    style = Style.from_preset("paper", color_scheme="colorblind")
    switched = style.with_(color_scheme="blackwhite")
    assert switched.colors == ("#000000",)
    assert switched.contour_cmap == "Greys"
    assert style.colors != switched.colors


def test_contour_uses_style_colormap():
    from matplotlib.collections import PolyCollection

    import graphplot as gp

    style = Style.from_preset("paper", color_scheme="blackwhite")
    fig = gp.Figure(style=style)
    fig.contour("data/zNormal.vtp", "gammaDV", levels=8)
    assert isinstance(fig.last_artist, PolyCollection)
    assert "Greys" in fig.last_artist.cmap.name
    fig.close()
