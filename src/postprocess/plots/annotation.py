from typing import Optional, Tuple

import matplotlib.patches as patches


class AnnotationPlot:
    """
    Scientific annotation utilities.

    Provides simple publication-oriented primitives:

        - text
        - arrow
        - marker
        - line
        - rectangle
    """

    # =====================================================
    # Text
    # =====================================================

    @staticmethod
    def add_text(
        axes,
        x,
        y,
        text,
        fontsize=10,
        ha="center",
        va="center",
        rotation=0,
        **kwargs,
    ):
        """
        Add text at a data-coordinate position.

        Parameters
        ----------
        axes
            Matplotlib Axes.

        x, y
            Position in data coordinates.

        text
            Text or LaTeX expression.

        fontsize
            Font size in points.

        ha
            Horizontal alignment.

        va
            Vertical alignment.

        rotation
            Rotation angle in degrees.
        """

        return axes.text(
            x,
            y,
            text,
            fontsize=fontsize,
            ha=ha,
            va=va,
            rotation=rotation,
            **kwargs,
        )

    # =====================================================
    # Arrow
    # =====================================================

    @staticmethod
    def add_arrow(
        axes,
        start,
        end,
        color="black",
        linewidth=1.0,
        headwidth=8,
        headlength=10,
        **kwargs,
    ):
        """
        Add an arrow between two data-coordinate positions.

        Parameters
        ----------
        start
            (x, y) starting point.

        end
            (x, y) ending point.
        """

        x0, y0 = start
        x1, y1 = end

        dx = x1 - x0
        dy = y1 - y0

        return axes.arrow(
            x0,
            y0,
            dx,
            dy,
            color=color,
            linewidth=linewidth,
            head_width=headwidth,
            head_length=headlength,
            length_includes_head=True,
            **kwargs,
        )

    # =====================================================
    # Marker
    # =====================================================

    @staticmethod
    def add_marker(
        axes,
        position,
        marker="o",
        size=40,
        color="black",
        edgecolor=None,
        linewidth=1.0,
        **kwargs,
    ):
        """
        Add a marker at a data-coordinate position.

        Parameters
        ----------
        position
            (x, y) position.

        marker
            Matplotlib marker style.

        size
            Marker size in points squared.
        """

        x, y = position

        if edgecolor is None:
            edgecolor = color

        return axes.scatter(
            [x],
            [y],
            marker=marker,
            s=size,
            c=color,
            edgecolors=edgecolor,
            linewidths=linewidth,
            **kwargs,
        )

    # =====================================================
    # Line
    # =====================================================

    @staticmethod
    def add_line(
        axes,
        start,
        end,
        color="black",
        linewidth=1.0,
        linestyle="-",
        **kwargs,
    ):
        """
        Add a line between two data-coordinate positions.
        """

        x0, y0 = start
        x1, y1 = end

        return axes.plot(
            [x0, x1],
            [y0, y1],
            color=color,
            linewidth=linewidth,
            linestyle=linestyle,
            **kwargs,
        )[0]

    # =====================================================
    # Rectangle
    # =====================================================

    @staticmethod
    def add_rectangle(
        axes,
        xy,
        width,
        height,
        edgecolor="black",
        facecolor="none",
        linewidth=1.0,
        linestyle="-",
        **kwargs,
    ):
        """
        Add a rectangle in data coordinates.

        Parameters
        ----------
        xy
            Lower-left corner.

        width
            Rectangle width.

        height
            Rectangle height.
        """

        rectangle = patches.Rectangle(
            xy,
            width,
            height,
            edgecolor=edgecolor,
            facecolor=facecolor,
            linewidth=linewidth,
            linestyle=linestyle,
            **kwargs,
        )

        axes.add_patch(
            rectangle
        )

        return rectangle