"""
Color schemes for publication figures.
"""


# =========================================================
# Colorblind-safe categorical palette
# =========================================================

COLORBLIND_COLORS = [
    "#0072B2",  # blue
    "#E69F00",  # orange
    "#009E73",  # green
    "#D55E00",  # vermillion
    "#CC79A7",  # purple
    "#56B4E9",  # sky blue
    "#F0E442",  # yellow
    "#000000",  # black
]


# =========================================================
# Standard publication palette
# =========================================================

DEFAULT_COLORS = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
]


# =========================================================
# Grayscale
# =========================================================

GRAYSCALE_COLORS = [
    "#000000",
    "#404040",
    "#707070",
    "#999999",
    "#BFBFBF",
    "#D9D9D9",
]


# =========================================================
# Black and white
# =========================================================

BLACKWHITE_COLORS = [
    "#000000",
]


# =========================================================
# Color scheme resolver
# =========================================================
def get_colors(scheme):
    """
    Return the requested color scheme.

    Parameters
    ----------
    scheme : str or sequence
        Available named schemes:

            - default
            - colorblind
            - grayscale
            - blackwhite

        A list or tuple may also be supplied to define
        a custom categorical palette.
    """

    if isinstance(
        scheme,
        (list, tuple),
    ):
        return validate_palette(scheme)

    scheme = scheme.lower()

    if scheme == "default":
        return list(DEFAULT_COLORS)

    if scheme == "colorblind":
        return list(COLORBLIND_COLORS)

    if scheme == "grayscale":
        return list(GRAYSCALE_COLORS)

    if scheme in (
        "blackwhite",
        "bw",
    ):
        return list(BLACKWHITE_COLORS)

    raise ValueError(
        f"Unknown color scheme '{scheme}'. "
        "Available schemes: default, colorblind, "
        "grayscale, blackwhite, or a custom "
        "list/tuple of colors."
    )


def validate_palette(colors):
    """
    Validate a custom categorical color palette.

    Parameters
    ----------
    colors : sequence
        Sequence of Matplotlib-compatible colors.

    Returns
    -------
    list
        Validated copy of the palette.

    Raises
    ------
    ValueError
        If the palette is empty.
    TypeError
        If colors is not a sequence.
    """

    if not isinstance(
        colors,
        (list, tuple),
    ):
        raise TypeError("Custom colors must be provided as a list or tuple.")

    if len(colors) == 0:
        raise ValueError("Custom color palette cannot be empty.")

    return list(colors)
