from postprocess.style import PublicationStyle
class LinePlot:
    """
    Publication-quality 1D multi-dataset plot.

    Supports ordinary lines, markers, and error bars.
    """

    def __init__(
        self,
        style=None,
    ):

        if style is None:
            style = PublicationStyle()

        self.style = style

        self.datasets = []
        self.errorbars = []

    # =====================================================
    # Add ordinary dataset
    # =====================================================

    def add(
        self,
        data,
        label=None,
        role=None,
        color=None,
        linewidth=1.5,
        linestyle=None,
        marker=None,
        markersize=4.0,
        markerfacecolor=None,
        markeredgecolor=None,
        markeredgewidth=1.0,
        markevery=None,
        alpha=1.0,
        zorder=3,
        **kwargs,
    ):
        """
        Add a Data1D dataset.

        Parameters
        ----------
        role : str, optional
            Dataset role:

            numerical
            analytical
            experimental
            reference

            If specified, publication styling is
            automatically applied.
        """

        style = self.style.dataset_style(
            len(self.datasets),
            role=role,
        )

        if color is None:
            color = style["color"]

        if linestyle is None:
            linestyle = style["linestyle"]

        if marker is None:
            marker = style["marker"]

        self.datasets.append(
            {
                "data": data,
                "label": label,
                "color": color,
                "linewidth": linewidth,
                "linestyle": linestyle,
                "marker": marker,
                "markersize": markersize,
                "markerfacecolor": markerfacecolor,
                "markeredgecolor": markeredgecolor,
                "markeredgewidth": markeredgewidth,
                "markevery": markevery,
                "alpha": alpha,
                "zorder": zorder,
                "kwargs": kwargs,
            }
        )

        return self

    # =====================================================
    # Add error-bar dataset
    # =====================================================

    def add_errorbar(
        self,
        data,
        y_error=None,
        x_error=None,
        label=None,
        role=None,
        color=None,
        marker="o",
        markersize=4.0,
        markerfacecolor=None,
        markeredgecolor=None,
        markeredgewidth=1.0,
        linestyle="None",
        linewidth=1.0,
        capsize=3.0,
        capthick=None,
        elinewidth=None,
        alpha=1.0,
        zorder=4,
        errorevery=1,
        **kwargs,
    ):
        """
        Add a dataset with x/y error bars.

        Parameters
        ----------
        data:
            Data1D object.

        y_error:
            Uncertainty in y.

            Can be:
                scalar
                1D array
                (lower, upper)

        x_error:
            Uncertainty in x.

            Can be:
                scalar
                1D array
                (lower, upper)

        label:
            Legend label.

        color:
            Error-bar and marker color.

        marker:
            Marker style.

        markersize:
            Marker size.

        markerfacecolor:
            Marker fill color.

        markeredgecolor:
            Marker edge color.

        markeredgewidth:
            Marker edge width.

        linestyle:
            Line style.

        linewidth:
            Connecting line width.

        capsize:
            Error-bar cap size.

        capthick:
            Error-bar cap thickness.

        elinewidth:
            Error-bar line width.

        errorevery:
            Plot an error bar every N points.

        kwargs:
            Additional Matplotlib errorbar options.
        """

        if y_error is None and x_error is None:
            raise ValueError(
                "At least one of y_error or x_error "
                "must be provided."
            )
        style = self.style.dataset_style(
            len(self.datasets) + len(self.errorbars),
            role=role,
        )
        if color is None:
            color = style["color"]

        if marker is None:
            marker = style["marker"]

        self.errorbars.append(
            {
                "data": data,
                "y_error": y_error,
                "x_error": x_error,
                "label": label,
                "color": color,
                "marker": marker,
                "markersize": markersize,
                "markerfacecolor": markerfacecolor,
                "markeredgecolor": markeredgecolor,
                "markeredgewidth": markeredgewidth,
                "linestyle": linestyle,
                "linewidth": linewidth,
                "capsize": capsize,
                "capthick": capthick,
                "elinewidth": elinewidth,
                "alpha": alpha,
                "zorder": zorder,
                "errorevery": errorevery,
                "kwargs": kwargs,
            }
        )

        return self

    # =====================================================
    # Plot
    # =====================================================

    def plot(
        self,
        axes,
    ):
        """
        Plot all ordinary datasets and error-bar datasets.

        Returns
        -------
        list
            Matplotlib artists.
        """

        artists = []

        # -------------------------------------------------
        # Ordinary lines
        # -------------------------------------------------

        for item in self.datasets:

            data = item["data"]

            line = axes.plot(
                data.x,
                data.y,
                label=item["label"],
                color=item["color"],
                linewidth=item["linewidth"],
                linestyle=item["linestyle"],
                marker=item["marker"],
                markersize=item["markersize"],
                markerfacecolor=item[
                    "markerfacecolor"
                ],
                markeredgecolor=item[
                    "markeredgecolor"
                ],
                markeredgewidth=item[
                    "markeredgewidth"
                ],
                markevery=item["markevery"],
                alpha=item["alpha"],
                zorder=item["zorder"],
                **item["kwargs"],
            )

            artists.append(line[0])

        # -------------------------------------------------
        # Error bars
        # -------------------------------------------------

        for item in self.errorbars:

            data = item["data"]

            errorbar = axes.errorbar(
                data.x,
                data.y,
                yerr=item["y_error"],
                xerr=item["x_error"],
                label=item["label"],
                color=item["color"],
                marker=item["marker"],
                markersize=item["markersize"],
                markerfacecolor=item[
                    "markerfacecolor"
                ],
                markeredgecolor=item[
                    "markeredgecolor"
                ],
                markeredgewidth=item[
                    "markeredgewidth"
                ],
                linestyle=item["linestyle"],
                linewidth=item["linewidth"],
                capsize=item["capsize"],
                capthick=item["capthick"],
                elinewidth=item["elinewidth"],
                alpha=item["alpha"],
                zorder=item["zorder"],
                errorevery=item["errorevery"],
                **item["kwargs"],
            )

            artists.append(errorbar)

        return artists

    # =====================================================
    # Number of datasets
    # =====================================================

    @property
    def number_of_datasets(self):

        return (
            len(self.datasets)
            + len(self.errorbars)
        )

    # =====================================================
    # Clear
    # =====================================================

    def clear(self):

        self.datasets = []
        self.errorbars = []

    # =====================================================
    # Legend
    # =====================================================

    def legend(
        self,
        axes,
        location="best",
        frameon=False,
        ncol=1,
        fontsize=None,
        **kwargs,
    ):
        """
        Create a legend for the plotted datasets.

        The legend is only created if labeled
        artists are actually present on the axes.
        """

        handles, labels = axes.get_legend_handles_labels()

        # Remove empty/ignored labels
        valid = [
            (handle, label)
            for handle, label in zip(handles, labels)
            if label and not label.startswith("_")
        ]

        if not valid:
            return None

        handles, labels = zip(*valid)

        return axes.legend(
            handles,
            labels,
            loc=location,
            frameon=frameon,
            ncol=ncol,
            fontsize=fontsize,
            **kwargs,
        )