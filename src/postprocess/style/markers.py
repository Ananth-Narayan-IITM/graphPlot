"""
Marker schemes for publication figures.
"""

PUBLICATION_MARKERS = [
    "o",
    "s",
    "^",
    "D",
    "v",
    "<",
    ">",
    "P",
    "X",
]


BLACKWHITE_MARKERS = [
    "o",
    "s",
    "^",
    "D",
    "v",
    "<",
    ">",
    "P",
    "X",
]


def get_markers(scheme):
    """
    Return the requested marker sequence.
    """

    scheme = scheme.lower()

    if scheme == "publication":
        return list(PUBLICATION_MARKERS)

    if scheme in ("blackwhite", "bw"):
        return list(BLACKWHITE_MARKERS)

    raise ValueError(
        f"Unknown marker scheme '{scheme}'. Available schemes: publication, blackwhite."
    )
