import pytest
from postprocess.style.publication import (
    PublicationStyle,
)
from postprocess.style.colors import (
    DEFAULT_COLORS,
    COLORBLIND_COLORS,
    GRAYSCALE_COLORS,
    BLACKWHITE_COLORS,
    get_colors,
    validate_palette,
)


# =========================================================
# Built-in schemes
# =========================================================


def test_default_color_scheme():

    colors = get_colors("default")

    assert colors == DEFAULT_COLORS
    assert colors is not DEFAULT_COLORS


def test_colorblind_color_scheme():

    colors = get_colors("colorblind")

    assert colors == COLORBLIND_COLORS
    assert colors is not COLORBLIND_COLORS


def test_grayscale_color_scheme():

    colors = get_colors("grayscale")

    assert colors == GRAYSCALE_COLORS
    assert colors is not GRAYSCALE_COLORS


def test_blackwhite_color_scheme():

    colors = get_colors("blackwhite")

    assert colors == BLACKWHITE_COLORS
    assert colors is not BLACKWHITE_COLORS


def test_blackwhite_alias():

    colors = get_colors("bw")

    assert colors == BLACKWHITE_COLORS


# =========================================================
# Custom palette
# =========================================================


def test_custom_palette():

    palette = [
        "#264653",
        "#2A9D8F",
        "#E9C46A",
        "#F4A261",
        "#E76F51",
    ]

    colors = get_colors(palette)

    assert colors == palette
    assert colors is not palette


def test_custom_tuple_palette():

    palette = (
        "#264653",
        "#2A9D8F",
        "#E9C46A",
    )

    colors = get_colors(palette)

    assert colors == list(palette)


# =========================================================
# Palette validation
# =========================================================


def test_validate_palette_rejects_empty():

    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        validate_palette([])


def test_validate_palette_rejects_invalid_type():

    with pytest.raises(
        TypeError,
        match="list or tuple",
    ):
        validate_palette("#264653")


# =========================================================
# Unknown scheme
# =========================================================


def test_unknown_color_scheme():

    with pytest.raises(
        ValueError,
        match="Unknown color scheme",
    ):
        get_colors("does_not_exist")


def test_publication_style_custom_palette():

    palette = [
        "#264653",
        "#2A9D8F",
        "#E9C46A",
    ]

    style = PublicationStyle(color_scheme=palette)

    assert style.colors == palette

    assert style.color(0) == palette[0]
    assert style.color(1) == palette[1]
    assert style.color(2) == palette[2]

    # Palette should repeat when index exceeds
    # the number of available colors.

    assert style.color(3) == palette[0]
    assert style.color(4) == palette[1]
