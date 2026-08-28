from postprocess.style import PublicationStyle
from matplotlib.lines import Line2D
from matplotlib.offsetbox import (
    AnchoredOffsetbox,
    DrawingArea,
    HPacker,
    TextArea,
    VPacker,
)


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
            raise ValueError("At least one of y_error or x_error must be provided.")
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
                markerfacecolor=item["markerfacecolor"],
                markeredgecolor=item["markeredgecolor"],
                markeredgewidth=item["markeredgewidth"],
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
                markerfacecolor=item["markerfacecolor"],
                markeredgecolor=item["markeredgecolor"],
                markeredgewidth=item["markeredgewidth"],
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

        return len(self.datasets) + len(self.errorbars)

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
        groups=None,
        **kwargs,
    ):
        """
        Create a legend for the plotted datasets.

        Parameters
        ----------
        axes
            Matplotlib Axes.

        location
            Legend location.

        frameon
            Whether to draw a legend frame.

        ncol
            Number of legend columns.

        fontsize
            Legend font size.

        groups
            Optional grouped legend specification.

            Example
            -------
            groups=[
                {
                    "title": "Experiment",
                    "labels": [
                        "Experiment 1",
                        "Experiment 2",
                    ],
                },
                {
                    "title": "Numerical",
                    "labels": [
                        "Case 1",
                        "Case 2",
                    ],
                },
            ]

            If groups is None, a normal legend is
            created.

        Returns
        -------
        matplotlib.legend.Legend or None
        """

        # -----------------------------------------------------
        # Standard legend
        # -----------------------------------------------------

        if groups is None:
            handles, labels = axes.get_legend_handles_labels()

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

        # -----------------------------------------------------
        # Grouped legend
        # -----------------------------------------------------

        handles, labels = axes.get_legend_handles_labels()

        artist_map = {
            label: handle
            for handle, label in zip(handles, labels)
            if label and not label.startswith("_")
        }

        grouped_handles = []
        grouped_labels = []

        from matplotlib.lines import Line2D

        for group in groups:
            title = group.get(
                "title",
                None,
            )

            labels_in_group = group.get(
                "labels",
                [],
            )

            # ---------------------------------------------
            # Group heading
            # ---------------------------------------------

            if title is not None:
                grouped_handles.append(
                    Line2D(
                        [],
                        [],
                        linestyle="None",
                        marker=None,
                    )
                )

                grouped_labels.append(title)

            # ---------------------------------------------
            # Group datasets
            # ---------------------------------------------

            for label in labels_in_group:
                if label not in artist_map:
                    raise ValueError(
                        "Legend label '{}' was not "
                        "found among plotted datasets.".format(label)
                    )

                grouped_handles.append(artist_map[label])

                grouped_labels.append(label)

        if not grouped_handles:
            return None

        return axes.legend(
            grouped_handles,
            grouped_labels,
            loc=location,
            frameon=frameon,
            ncol=ncol,
            fontsize=fontsize,
            **kwargs,
        )

    # =====================================================
    # Grouped / table legend
    # =====================================================

    def legend_table(
        self,
        axes,
        groups,
        location="lower center",
        bbox_to_anchor=(0.5, -0.05),
        fontsize=None,
        handle_length=35,
        column_spacing=35,
        row_spacing=6,
    ):
        """
        Create a grouped table-style legend.

        Layout
        ------

                        Group 1          Group 2
        Case 1              line             line
        Case 2              line             line

        Parameters
        ----------
        axes
            Matplotlib Axes.

        groups
            Dictionary mapping group names to dictionaries
            of case names and Matplotlib artists.

            Example
            -------
            {
                "Temperature": {
                    "Case 1": line_1,
                    "Case 2": line_2,
                },
                "Pressure": {
                    "Case 1": line_3,
                    "Case 2": line_4,
                },
            }

        fontsize
            Text size.

        handle_length
            Length of the legend line representation.

        column_spacing
            Horizontal spacing between columns.

        row_spacing
            Vertical spacing between rows.

        Returns
        -------
        AnchoredOffsetbox
            The grouped legend artist.
        """

        if not groups:
            return None

        group_names = list(groups.keys())

        if len(group_names) == 0:
            return None

        # -----------------------------------------------------
        # Determine case names
        # -----------------------------------------------------

        first_group = groups[group_names[0]]

        case_names = list(first_group.keys())

        if not case_names:
            raise ValueError("Each legend group must contain at least one case.")

        # -----------------------------------------------------
        # Make sure all groups have identical cases
        # -----------------------------------------------------

        for group_name in group_names:
            current_cases = list(groups[group_name].keys())

            if current_cases != case_names:
                raise ValueError(
                    "All legend groups must contain "
                    "the same case names in the "
                    "same order."
                )

        # -----------------------------------------------------
        # Font size
        # -----------------------------------------------------

        if fontsize is None:
            fontsize = axes.figure._get_renderer_cache() if False else 8

        # -----------------------------------------------------
        # Helper: create text
        # -----------------------------------------------------

        def make_text(
            text,
            bold=False,
        ):

            return TextArea(
                str(text),
                textprops={
                    "fontsize": fontsize,
                    "fontweight": ("bold" if bold else "normal"),
                    "ha": "center",
                    "va": "center",
                },
            )

        # -----------------------------------------------------
        # Helper: create line representation
        # -----------------------------------------------------

        def make_handle(handle):

            drawing = DrawingArea(
                handle_length,
                14,
                0,
                0,
            )

            # -------------------------------------------------
            # Line properties
            # -------------------------------------------------

            color = (
                handle.get_color()
                if hasattr(
                    handle,
                    "get_color",
                )
                else "black"
            )

            linewidth = (
                handle.get_linewidth()
                if hasattr(
                    handle,
                    "get_linewidth",
                )
                else 1.5
            )

            linestyle = (
                handle.get_linestyle()
                if hasattr(
                    handle,
                    "get_linestyle",
                )
                else "-"
            )

            # -------------------------------------------------
            # Marker properties
            # -------------------------------------------------

            marker = (
                handle.get_marker()
                if hasattr(
                    handle,
                    "get_marker",
                )
                else "None"
            )

            markersize = (
                handle.get_markersize()
                if hasattr(
                    handle,
                    "get_markersize",
                )
                else 4.0
            )

            markerfacecolor = (
                handle.get_markerfacecolor()
                if hasattr(
                    handle,
                    "get_markerfacecolor",
                )
                else color
            )

            markeredgecolor = (
                handle.get_markeredgecolor()
                if hasattr(
                    handle,
                    "get_markeredgecolor",
                )
                else color
            )

            markeredgewidth = (
                handle.get_markeredgewidth()
                if hasattr(
                    handle,
                    "get_markeredgewidth",
                )
                else 1.0
            )

            # -------------------------------------------------
            # Reconstruct legend handle
            # -------------------------------------------------

            line = Line2D(
                [0, handle_length],
                [7, 7],
                color=color,
                linewidth=linewidth,
                linestyle=linestyle,
                marker=marker,
                markersize=markersize,
                markerfacecolor=markerfacecolor,
                markeredgecolor=markeredgecolor,
                markeredgewidth=markeredgewidth,
            )

            drawing.add_artist(line)

            return drawing

        # -----------------------------------------------------
        # Header row
        #
        #          Case 1     Case 2
        # Temperature
        # -----------------------------------------------------

        header_cells = []

        # Empty first column
        header_cells.append(make_text(""))

        # Group headings
        for group_name in group_names:
            group_header = make_text(
                group_name,
                bold=False,
            )

            # Span the width of all case columns
            group_header_box = HPacker(
                children=[
                    group_header,
                ],
                align="center",
                sep=0,
            )

            header_cells.append(group_header_box)

        header_row = HPacker(
            children=header_cells,
            align="center",
            sep=column_spacing,
        )

        # -----------------------------------------------------
        # Data rows
        # -----------------------------------------------------

        rows = []

        for case_name in case_names:
            cells = []

            # Case name
            cells.append(make_text(case_name))

            # One cell for each group
            for group_name in group_names:
                handle = groups[group_name][case_name]

                cells.append(make_handle(handle))

            row = HPacker(
                children=cells,
                align="center",
                sep=column_spacing,
            )

            rows.append(row)

        # -----------------------------------------------------
        # Stack header + rows
        # -----------------------------------------------------

        table = VPacker(
            children=[
                header_row,
                *rows,
            ],
            align="center",
            sep=row_spacing,
        )

        # -----------------------------------------------------
        # Place table on figure
        # -----------------------------------------------------

        legend = AnchoredOffsetbox(
            loc=location,
            child=table,
            frameon=False,
            bbox_to_anchor=bbox_to_anchor,
            bbox_transform=axes.figure.transFigure,
            borderpad=0.0,
            pad=0.0,
        )

        axes.figure.add_artist(legend)

        return legend
