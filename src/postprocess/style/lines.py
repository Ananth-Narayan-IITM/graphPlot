"""
Line style schemes for publication figures.
"""

PUBLICATION_LINESTYLES = [
    "-",
    "--",
    "-.",
    ":",
]


BLACKWHITE_LINESTYLES = [
    "-",
    "--",
    "-.",
    ":",
]


def get_linestyles(scheme):
    """
    Return the requested line-style sequence.
    """

    scheme = scheme.lower()

    if scheme == "publication":
        return list(PUBLICATION_LINESTYLES)

    if scheme in ("blackwhite", "bw"):
        return list(BLACKWHITE_LINESTYLES)

    raise ValueError(
        f"Unknown line scheme '{scheme}'. Available schemes: publication, blackwhite."
    )
