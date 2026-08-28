import numpy as np
import pytest

from postprocess.layout.colors import (
    ColorScale,
)

# =========================================================
# Default color scale
# =========================================================


def test_color_scale_default():

    scale = ColorScale()

    assert scale.levels == 30
    assert scale.cmap == "viridis"
    assert scale.vmin is None
    assert scale.vmax is None


# =========================================================
# Resolve limits
# =========================================================


def test_color_scale_resolve():

    values = np.array(
        [
            0.0,
            0.25,
            0.5,
            0.75,
            1.0,
        ]
    )

    scale = ColorScale(
        levels=10,
        cmap="viridis",
    )

    scale.resolve(values)

    # User-specified limits remain None.
    assert scale.vmin is None
    assert scale.vmax is None

    # Resolved limits must come from the data.
    assert scale.limits == (
        0.0,
        1.0,
    )

    # 10 intervals -> 11 level boundaries.
    assert len(scale.levels_array) == 11

    assert scale.norm is not None
    assert scale.colormap is not None


# =========================================================
# Explicit limits
# =========================================================


def test_color_scale_explicit_limits():

    scale = ColorScale(
        levels=20,
        cmap="plasma",
        vmin=-1.0,
        vmax=2.0,
    )

    scale.resolve(
        np.array(
            [
                0.0,
                1.0,
            ]
        )
    )

    assert scale.vmin == -1.0
    assert scale.vmax == 2.0

    assert scale.limits == (
        -1.0,
        2.0,
    )


# =========================================================
# Different colormaps
# =========================================================


def test_color_scale_custom_colormap():

    scale = ColorScale(
        levels=15,
        cmap="plasma",
    )

    scale.resolve(
        np.linspace(
            0.0,
            1.0,
            20,
        )
    )

    assert scale.colormap.name == "plasma"


# =========================================================
# Invalid range
# =========================================================


def test_color_scale_invalid_range():

    scale = ColorScale(
        levels=10,
        vmin=1.0,
        vmax=1.0,
    )

    with pytest.raises(
        ValueError,
    ):
        scale.resolve(
            np.array(
                [
                    1.0,
                    1.0,
                ]
            )
        )


# =========================================================
# Independent scalar fields
# =========================================================


def test_color_scales_are_independent():

    gamma = np.linspace(
        0.0,
        1.0,
        20,
    )

    phi = np.linspace(
        0.0,
        100.0,
        20,
    )

    gamma_scale = ColorScale(
        levels=30,
        cmap="viridis",
    )

    phi_scale = ColorScale(
        levels=30,
        cmap="plasma",
    )

    gamma_scale.resolve(gamma)

    phi_scale.resolve(phi)

    assert gamma_scale.limits == (
        0.0,
        1.0,
    )

    assert phi_scale.limits == (
        0.0,
        100.0,
    )

    assert gamma_scale.colormap.name == "viridis"

    assert phi_scale.colormap.name == "plasma"


def test_color_scale_explicit_ranges_remain_independent():

    gamma = np.linspace(
        0.0,
        1.0,
        20,
    )

    phi = np.linspace(
        0.0,
        100.0,
        20,
    )

    gamma_scale = ColorScale(
        levels=20,
        cmap="viridis",
        vmin=0.0,
        vmax=1.0,
    )

    phi_scale = ColorScale(
        levels=20,
        cmap="plasma",
        vmin=0.0,
        vmax=100.0,
    )

    gamma_scale.resolve(gamma)

    phi_scale.resolve(phi)

    assert gamma_scale.limits == (
        0.0,
        1.0,
    )

    assert phi_scale.limits == (
        0.0,
        100.0,
    )

    assert gamma_scale.norm.vmin == 0.0

    assert gamma_scale.norm.vmax == 1.0

    assert phi_scale.norm.vmin == 0.0

    assert phi_scale.norm.vmax == 100.0


def test_color_scale_level_count():

    values = np.linspace(
        0.0,
        1.0,
        100,
    )

    scale = ColorScale(
        levels=30,
        cmap="viridis",
    )

    scale.resolve(values)

    assert len(scale.levels_array) == 31


def test_final_example_shared_cfd_color_scale():

    import numpy as np

    from postprocess.layout.colors import (
        ColorScale,
    )

    gamma = np.linspace(
        0.0,
        1.0,
        100,
    )

    scale = ColorScale(
        levels=30,
        cmap="viridis",
        vmin=0.0,
        vmax=1.0,
    )

    scale.resolve(gamma)

    assert scale.limits == (
        0.0,
        1.0,
    )

    assert scale.colormap.name == "viridis"

    assert scale.norm.vmin == 0.0

    assert scale.norm.vmax == 1.0

    assert len(scale.levels_array) == 31
