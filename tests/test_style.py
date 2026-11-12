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
