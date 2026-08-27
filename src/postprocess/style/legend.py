"""
Legend management for publication figures.
"""


class LegendManager:
    """
    Central manager for publication legends.

    Handles data legends and explanatory/reference
    legend entries.
    """

    def __init__(self):

        self.reference_entries = []

    # =====================================================
    # Reference entries
    # =====================================================

    def add_reference(
        self,
        label,
        handle=None,
    ):
        """
        Add an explanatory/reference legend entry.

        Parameters
        ----------
        label : str
            Text displayed in the legend.

        handle : optional
            Matplotlib artist representing the entry.
        """

        self.reference_entries.append(
            {
                "label": label,
                "handle": handle,
            }
        )

        return self

    # =====================================================
    # Render
    # =====================================================

    def render(
        self,
        axes,
        location="best",
        frameon=False,
        ncol=1,
        fontsize=None,
        bbox_to_anchor=None,
        columnspacing=1.5,
        handlelength=2.0,
        handletextpad=0.5,
        borderaxespad=0.5,
        **kwargs,
    ):
        """
        Render the legend.
        """

        handles, labels = (
            axes.get_legend_handles_labels()
        )

        # -------------------------------------------------
        # Add reference entries
        # -------------------------------------------------

        for entry in self.reference_entries:

            if entry["handle"] is not None:

                handles.append(
                    entry["handle"]
                )

            else:

                handles.append(
                    None
                )

            labels.append(
                entry["label"]
            )

        # -------------------------------------------------
        # Nothing to display
        # -------------------------------------------------

        if not labels:
            return None

        legend = axes.legend(
            handles,
            labels,
            loc=location,
            frameon=frameon,
            ncol=ncol,
            fontsize=fontsize,
            bbox_to_anchor=bbox_to_anchor,
            columnspacing=columnspacing,
            handlelength=handlelength,
            handletextpad=handletextpad,
            borderaxespad=borderaxespad,
            **kwargs,
        )

        return legend