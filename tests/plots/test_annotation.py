import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow, Rectangle

from postprocess.plots.annotation import AnnotationPlot

# =========================================================
# Text
# =========================================================


def test_annotation_add_text():

    figure, axes = plt.subplots()

    text = AnnotationPlot.add_text(
        axes,
        x=0.5,
        y=0.5,
        text="Test",
    )

    assert text.get_text() == "Test"

    assert text.get_position() == (
        0.5,
        0.5,
    )

    plt.close(figure)


# =========================================================
# Arrow
# =========================================================


def test_annotation_add_arrow():

    figure, axes = plt.subplots()

    arrow = AnnotationPlot.add_arrow(
        axes,
        start=(0.1, 0.2),
        end=(0.8, 0.9),
    )

    assert isinstance(
        arrow,
        FancyArrow,
    )

    plt.close(figure)


# =========================================================
# Marker
# =========================================================


def test_annotation_add_marker():

    figure, axes = plt.subplots()

    marker = AnnotationPlot.add_marker(
        axes,
        position=(0.5, 0.5),
    )

    assert marker is not None

    assert len(marker.get_offsets()) == 1

    plt.close(figure)


# =========================================================
# Line
# =========================================================


def test_annotation_add_line():

    figure, axes = plt.subplots()

    line = AnnotationPlot.add_line(
        axes,
        start=(0.1, 0.2),
        end=(0.8, 0.9),
    )

    assert line is not None

    assert list(line.get_xdata()) == [0.1, 0.8]

    assert list(line.get_ydata()) == [0.2, 0.9]

    plt.close(figure)


# =========================================================
# Rectangle
# =========================================================


def test_annotation_add_rectangle():

    figure, axes = plt.subplots()

    rectangle = AnnotationPlot.add_rectangle(
        axes,
        xy=(0.2, 0.3),
        width=0.4,
        height=0.5,
    )

    assert isinstance(
        rectangle,
        Rectangle,
    )

    assert rectangle.get_width() == 0.4
    assert rectangle.get_height() == 0.5

    plt.close(figure)


def test_annotation_add_rectangle_dimensions():

    figure, axes = plt.subplots()

    rectangle = AnnotationPlot.add_rectangle(
        axes,
        xy=(1.0, 2.0),
        width=3.0,
        height=4.0,
    )

    assert rectangle.get_x() == 1.0
    assert rectangle.get_y() == 2.0
    assert rectangle.get_width() == 3.0
    assert rectangle.get_height() == 4.0

    assert rectangle.get_facecolor()[3] == 0.0

    plt.close(figure)


def test_annotation_add_line_geometry():

    figure, axes = plt.subplots()

    line = AnnotationPlot.add_line(
        axes,
        start=(1.0, 2.0),
        end=(4.0, 6.0),
        color="black",
        linewidth=1.5,
        linestyle="--",
    )

    assert list(line.get_xdata()) == [1.0, 4.0]

    assert list(line.get_ydata()) == [2.0, 6.0]

    assert line.get_color() == "black"

    assert line.get_linewidth() == 1.5

    assert line.get_linestyle() == "--"

    plt.close(figure)


def test_annotation_add_arrow_geometry():

    figure, axes = plt.subplots()

    arrow = AnnotationPlot.add_arrow(
        axes,
        start=(1.0, 2.0),
        end=(4.0, 6.0),
    )

    assert arrow is not None

    plt.close(figure)
