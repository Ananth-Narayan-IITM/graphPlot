from typing import Sequence, Tuple

import matplotlib.patches as patches


class GeometryPlot:
    """
    Utilities for plotting physical geometry and
    scientific reference geometry.

    All coordinates are in data coordinates.
    """

    # =====================================================
    # Line
    # =====================================================

    @staticmethod
    def add_line(
        axes,
        start,
        end,
        linewidth=1.0,
        linestyle="-",
        color="black",
        **kwargs,
    ):
        """
        Draw a straight line between two points.
        """

        x0, y0 = start
        x1, y1 = end

        return axes.plot(
            [x0, x1],
            [y0, y1],
            linewidth=linewidth,
            linestyle=linestyle,
            color=color,
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
        linewidth=1.0,
        linestyle="-",
        edgecolor="black",
        facecolor="none",
        **kwargs,
    ):
        """
        Draw a rectangle.

        Parameters
        ----------
        xy:
            Lower-left corner.

        width:
            Width in data coordinates.

        height:
            Height in data coordinates.
        """

        rectangle = patches.Rectangle(
            xy,
            width,
            height,
            linewidth=linewidth,
            linestyle=linestyle,
            edgecolor=edgecolor,
            facecolor=facecolor,
            **kwargs,
        )

        axes.add_patch(rectangle)

        return rectangle

    # =====================================================
    # Polygon
    # =====================================================

    @staticmethod
    def add_polygon(
        axes,
        points,
        linewidth=1.0,
        linestyle="-",
        edgecolor="black",
        facecolor="none",
        closed=True,
        **kwargs,
    ):
        """
        Draw a polygon.

        Parameters
        ----------
        points:
            Sequence of (x, y) coordinates.
        """

        polygon = patches.Polygon(
            points,
            closed=closed,
            linewidth=linewidth,
            linestyle=linestyle,
            edgecolor=edgecolor,
            facecolor=facecolor,
            **kwargs,
        )

        axes.add_patch(polygon)

        return polygon

    # =====================================================
    # Dimension
    # =====================================================

    @staticmethod
    def add_dimension(
        axes,
        start,
        end,
        offset=0.15,
        text=None,
        linewidth=0.8,
        color="black",
        fontsize=9,
        text_offset=0.05,
        arrowstyle="<->",
        **kwargs,
    ):
        """
        Add a dimension line between two points.

        The dimension is offset perpendicular to the
        measured line.

        Parameters
        ----------
        start:
            First measurement point.

        end:
            Second measurement point.

        offset:
            Perpendicular offset of the dimension line.

        text:
            Dimension label.

        text_offset:
            Additional offset for the text.

        arrowstyle:
            Arrow style used for the dimension line.
        """

        from matplotlib.patches import FancyArrowPatch

        x0, y0 = start
        x1, y1 = end

        dx = x1 - x0
        dy = y1 - y0

        length = (dx ** 2 + dy ** 2) ** 0.5

        if length == 0.0:
            raise ValueError(
                "Dimension start and end points "
                "cannot be identical."
            )

        # -------------------------------------------------
        # Unit normal
        # -------------------------------------------------

        nx = -dy / length
        ny = dx / length

        # -------------------------------------------------
        # Offset dimension points
        # -------------------------------------------------

        p0 = (
            x0 + offset * nx,
            y0 + offset * ny,
        )

        p1 = (
            x1 + offset * nx,
            y1 + offset * ny,
        )

        # -------------------------------------------------
        # Extension lines
        # -------------------------------------------------

        axes.plot(
            [x0, p0[0]],
            [y0, p0[1]],
            color=color,
            linewidth=linewidth,
        )

        axes.plot(
            [x1, p1[0]],
            [y1, p1[1]],
            color=color,
            linewidth=linewidth,
        )

        # -------------------------------------------------
        # Dimension arrow
        # -------------------------------------------------

        arrow = FancyArrowPatch(
            p0,
            p1,
            arrowstyle=arrowstyle,
            mutation_scale=10,
            linewidth=linewidth,
            color=color,
            **kwargs,
        )

        axes.add_patch(arrow)

        # -------------------------------------------------
        # Dimension text
        # -------------------------------------------------

        if text is not None:

            tx = (
                0.5 * (p0[0] + p1[0])
                + text_offset * nx
            )

            ty = (
                0.5 * (p0[1] + p1[1])
                + text_offset * ny
            )

            angle = 0.0

            axes.text(
                tx,
                ty,
                text,
                fontsize=fontsize,
                ha="center",
                va="center",
                rotation=angle,
            )

        return arrow