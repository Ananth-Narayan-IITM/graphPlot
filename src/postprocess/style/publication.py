"""
Central publication style definition.
"""

from .colors import get_colors
from .lines import get_linestyles
from .markers import get_markers


class PublicationStyle:
    """
    Central visual style for scientific figures.

    Parameters
    ----------
    color_scheme : str
        Color scheme.

    line_scheme : str
        Line style scheme.

    marker_scheme : str
        Marker scheme.
    """

    def __init__(
        self,
        color_scheme="colorblind",
        line_scheme="publication",
        marker_scheme="publication",
    ):

        self.color_scheme = color_scheme
        self.line_scheme = line_scheme
        self.marker_scheme = marker_scheme

        self.colors = get_colors(
            color_scheme
        )

        self.linestyles = get_linestyles(
            line_scheme
        )

        self.markers = get_markers(
            marker_scheme
        )

    # =====================================================
    # Color
    # =====================================================

    def color(self, index):
        """
        Return a color according to index.
        """

        return self.colors[
            index % len(self.colors)
        ]

    # =====================================================
    # Line style
    # =====================================================

    def linestyle(self, index):
        """
        Return a line style according to index.
        """

        return self.linestyles[
            index % len(self.linestyles)
        ]

    # =====================================================
    # Marker
    # =====================================================

    def marker(self, index):
        """
        Return a marker according to index.
        """

        return self.markers[
            index % len(self.markers)
        ]

    # =====================================================
    # Dataset role
    # =====================================================

    def dataset_style(
        self,
        index,
        role=None,
    ):
        """
        Return the visual style for a dataset.

        Parameters
        ----------
        index : int
            Dataset index.

        role : str, optional
            Dataset role.

            Supported roles:

            - numerical
            - analytical
            - experimental
            - reference
        """

        if role is None:

            return {
                "color": self.color(index),
                "linestyle": self.linestyle(index),
                "marker": None,
            }

        role = role.lower()

        # -------------------------------------------------
        # Numerical
        # -------------------------------------------------

        if role == "numerical":

            return {
                "color": self.color(index),
                "linestyle": "-",
                "marker": None,
            }

        # -------------------------------------------------
        # Analytical
        # -------------------------------------------------

        if role == "analytical":

            return {
                "color": self.color(index),
                "linestyle": "--",
                "marker": None,
            }

        # -------------------------------------------------
        # Experimental
        # -------------------------------------------------

        if role == "experimental":

            return {
                "color": self.color(index),
                "linestyle": "None",
                "marker": self.marker(index),
            }

        # -------------------------------------------------
        # Reference
        # -------------------------------------------------

        if role == "reference":

            return {
                "color": self.color(index),
                "linestyle": "-.",
                "marker": self.marker(index),
            }

        raise ValueError(
            "Unknown dataset role '{}'. "
            "Available roles: numerical, analytical, "
            "experimental, reference.".format(role)
        )