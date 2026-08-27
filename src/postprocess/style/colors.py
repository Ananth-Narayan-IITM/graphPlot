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
    scheme : str
        Available schemes:

        - default
        - colorblind
        - grayscale
        - blackwhite
    """

    scheme = scheme.lower()

    if scheme == "default":
        return list(DEFAULT_COLORS)

    if scheme == "colorblind":
        return list(COLORBLIND_COLORS)

    if scheme == "grayscale":
        return list(GRAYSCALE_COLORS)

    if scheme in ("blackwhite", "bw"):
        return list(BLACKWHITE_COLORS)

    raise ValueError(
        "Unknown color scheme '{}'. "
        "Available schemes: default, colorblind, "
        "grayscale, blackwhite.".format(scheme)
    )