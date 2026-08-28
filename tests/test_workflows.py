import matplotlib

matplotlib.use("Agg")

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from postprocess.data.data1d import Data1D
from postprocess.io.vtp import read_vtp
from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)
from postprocess.plots.annotation import AnnotationPlot
from postprocess.plots.contour import ContourPlot
from postprocess.plots.line import LinePlot
from postprocess.plots.mesh import MeshPlot
from postprocess.plots.streamline import StreamlinePlot
from postprocess.plots.vector import VectorPlot

INPUT_FILE = "data/zNormal.vtp"


def test_vtp_contour_workflow(tmp_path):

    # -----------------------------------------------------
    # Read
    # -----------------------------------------------------

    data = read_vtp(INPUT_FILE)

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=3.4,
        height=3.0,
    )

    figure = PublicationFigure(figure_config)

    # -----------------------------------------------------
    # Contour
    # -----------------------------------------------------

    contour_plot = ContourPlot(
        data,
        field="gammaDV",
    )

    contour = contour_plot.plot(figure.axes)

    assert contour is not None

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "example_01_vtp_contour"

    figure.export(
        str(output),
        formats=[
            "pdf",
            "pdf_tex",
        ],
    )

    # -----------------------------------------------------
    # Verify output
    # -----------------------------------------------------

    pdf = Path(str(output) + ".pdf")

    pdf_tex = Path(str(output) + ".pdf_tex")

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0


def test_vtp_contour_mesh_workflow(tmp_path):

    # -----------------------------------------------------
    # Read
    # -----------------------------------------------------

    data = read_vtp(INPUT_FILE)

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=3.4,
        height=3.0,
        dpi=600,
    )

    figure = PublicationFigure(figure_config)

    # -----------------------------------------------------
    # Contour
    # -----------------------------------------------------

    contour_plot = ContourPlot(
        data,
        field="gammaDV",
    )

    contour = contour_plot.plot(
        figure.axes,
        rasterize=True,
    )

    assert contour is not None

    # -----------------------------------------------------
    # Mesh
    # -----------------------------------------------------

    mesh_plot = MeshPlot(data)

    mesh = mesh_plot.plot(
        figure.axes,
        edgecolor="black",
        facecolor="none",
        linewidth=0.15,
        alpha=0.35,
    )

    assert mesh is not None

    assert mesh.get_rasterized() is False

    mesh.set_rasterized(True)

    assert mesh.get_rasterized() is True

    # -----------------------------------------------------
    # Labels
    # -----------------------------------------------------

    figure.set_labels(
        xlabel=r"$x\;(m)$",
        ylabel=r"$y\;(m)$",
    )

    figure.set_title(r"$\gamma_{\mathrm{DV}}$ distribution")

    # -----------------------------------------------------
    # Colorbar
    # -----------------------------------------------------

    colorbar = figure.add_colorbar(
        contour,
        label=r"$\gamma_{\mathrm{DV}}\;(1/s)$",
    )

    assert colorbar is not None

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "example_02_vtp_contour_mesh"

    figure.export(
        str(output),
        formats=[
            "pdf",
            "pdf_tex",
        ],
    )

    # -----------------------------------------------------
    # Verify output
    # -----------------------------------------------------

    pdf = Path(str(output) + ".pdf")

    pdf_tex = Path(str(output) + ".pdf_tex")

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0


def test_vtp_contour_vector_workflow(tmp_path):

    # -----------------------------------------------------
    # Read
    # -----------------------------------------------------

    data = read_vtp(INPUT_FILE)

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=3.4,
        height=3.0,
        dpi=600,
    )

    figure = PublicationFigure(figure_config)

    # -----------------------------------------------------
    # Contour
    # -----------------------------------------------------

    contour_plot = ContourPlot(
        data,
        field="gammaDV",
    )

    contour = contour_plot.plot(
        figure.axes,
        rasterize=True,
    )

    assert contour is not None

    # -----------------------------------------------------
    # Vectors
    # -----------------------------------------------------

    vector_plot = VectorPlot(
        data,
        field="U",
        association="cell",
    )

    vectors = vector_plot.plot(
        figure.axes,
        normalize=False,
        density=20,
        scale=20,
        width=0.002,
        color="black",
    )

    assert vectors is not None

    # -----------------------------------------------------
    # Labels
    # -----------------------------------------------------

    figure.set_labels(
        xlabel=r"$x\;(m)$",
        ylabel=r"$y\;(m)$",
    )

    figure.set_title(
        r"$\gamma_{\mathrm{DV}}$ distribution "
        r"with velocity field"
    )

    # -----------------------------------------------------
    # Colorbar
    # -----------------------------------------------------

    colorbar = figure.add_colorbar(
        contour,
        label=r"$\gamma_{\mathrm{DV}}\;(1/s)$",
    )

    assert colorbar is not None

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "example_03_vtp_contour_vector"

    figure.export(
        str(output),
        formats=[
            "pdf",
            "pdf_tex",
        ],
    )

    # -----------------------------------------------------
    # Verify output
    # -----------------------------------------------------

    pdf = Path(str(output) + ".pdf")

    pdf_tex = Path(str(output) + ".pdf_tex")

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0


def test_vtp_combined_flow_workflow(
    tmp_path,
):

    # -----------------------------------------------------
    # Read
    # -----------------------------------------------------

    data = read_vtp(INPUT_FILE)

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=3.4,
        height=3.0,
    )

    figure = PublicationFigure(figure_config)

    # -----------------------------------------------------
    # Contour
    # -----------------------------------------------------

    contour_plot = ContourPlot(
        data,
        field="gammaDV",
        association="cell",
    )

    contour = contour_plot.plot(figure.axes)

    assert contour is not None

    # -----------------------------------------------------
    # Mesh
    # -----------------------------------------------------

    mesh_plot = MeshPlot(data)

    mesh = mesh_plot.plot(
        figure.axes,
        edgecolor="black",
        facecolor="none",
        linewidth=0.15,
        alpha=0.35,
    )

    assert mesh is not None

    # -----------------------------------------------------
    # Vector
    # -----------------------------------------------------

    vector_plot = VectorPlot(
        data,
        field="U",
        association="cell",
    )

    vectors = vector_plot.plot(
        figure.axes,
        normalize=False,
        density=20,
        scale=20,
        width=0.002,
        color="black",
    )

    assert vectors is not None

    # -----------------------------------------------------
    # Streamlines
    # -----------------------------------------------------

    streamline_plot = StreamlinePlot(
        data,
        field="U",
    )

    streamline_plot.plot(
        figure.axes,
        n_seeds=10,
        seed_axis="y",
        integration_direction="forward",
        integrator_type=45,
        surface_streamlines=True,
        color="black",
        linewidth=0.7,
        arrowsize=0,
    )

    # Streamlines are plotted as Matplotlib lines.
    assert len(figure.axes.lines) > 0

    # -----------------------------------------------------
    # Annotation
    # -----------------------------------------------------

    annotation = AnnotationPlot.add_text(
        figure.axes,
        x=0.15,
        y=0.85,
        text="Flow direction",
        fontsize=9,
        ha="left",
    )

    assert annotation is not None

    # -----------------------------------------------------
    # Labels
    # -----------------------------------------------------

    figure.set_labels(
        xlabel=r"$x\;(m)$",
        ylabel=r"$y\;(m)$",
    )

    figure.set_title(r"$\gamma_{\mathrm{DV}}$ distribution")

    # -----------------------------------------------------
    # Colorbar
    # -----------------------------------------------------

    colorbar = figure.add_colorbar(
        contour,
        label=r"$\gamma_{\mathrm{DV}}$",
    )

    assert colorbar is not None

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "example_04_vtp_combined_flow"

    figure.export(
        str(output),
        formats=[
            "pdf",
            "pdf_tex",
        ],
    )

    # -----------------------------------------------------
    # Verify output
    # -----------------------------------------------------

    pdf = Path(str(output) + ".pdf")

    pdf_tex = Path(str(output) + ".pdf_tex")

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0

    # -----------------------------------------------------
    # Close
    # -----------------------------------------------------

    plt.close(figure.figure)


def test_vtp_contour_geometry_annotation_workflow(
    tmp_path,
):

    data = read_vtp(INPUT_FILE)

    figure_config = FigureConfig(
        width=3.4,
        height=3.0,
    )

    figure = PublicationFigure(figure_config)

    # -----------------------------------------------------
    # Contour
    # -----------------------------------------------------

    contour_plot = ContourPlot(
        data,
        field="gammaDV",
        association="cell",
    )

    contour = contour_plot.plot(figure.axes)

    assert contour is not None

    # -----------------------------------------------------
    # Geometry
    # -----------------------------------------------------

    geometry = AnnotationPlot.add_rectangle(
        figure.axes,
        xy=(3.5, 3.5),
        width=1.0,
        height=1.0,
        edgecolor="black",
        facecolor="none",
        linewidth=1.0,
    )

    assert geometry is not None

    # -----------------------------------------------------
    # Dimension line
    # -----------------------------------------------------

    dimension_line = AnnotationPlot.add_line(
        figure.axes,
        start=(3.5, 3.3),
        end=(4.5, 3.3),
        color="black",
        linewidth=0.8,
    )

    assert dimension_line is not None

    # -----------------------------------------------------
    # Dimension label
    # -----------------------------------------------------

    dimension_text = AnnotationPlot.add_text(
        figure.axes,
        x=4.0,
        y=3.15,
        text=r"$L = 1.0\;m$",
        fontsize=8,
    )

    assert dimension_text is not None

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "example_05_contour_geometry"

    figure.export(
        str(output),
        formats=[
            "pdf",
            "pdf_tex",
        ],
    )

    pdf = Path(str(output) + ".pdf")

    pdf_tex = Path(str(output) + ".pdf_tex")

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0

    plt.close(figure.figure)


def test_basic_line_workflow(
    tmp_path,
):

    # -----------------------------------------------------
    # Data
    # -----------------------------------------------------

    x = np.linspace(
        0.0,
        1.0,
        100,
    )

    y = np.sin(2.0 * np.pi * x)

    data = Data1D(
        x=x,
        y=y,
        label="Numerical",
        x_label=r"$x$",
        y_label=r"$f(x)$",
        x_unit="m",
    )

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=3.4,
        height=2.8,
        dpi=600,
    )

    figure = PublicationFigure(figure_config)

    # -----------------------------------------------------
    # Line
    # -----------------------------------------------------

    line_plot = LinePlot()

    line_plot.add(
        data,
        label="Numerical",
        role="numerical",
        color="black",
        linewidth=1.5,
        linestyle="-",
    )

    lines = line_plot.plot(figure.axes)

    assert len(lines) == 1

    line = lines[0]

    assert line is not None

    # -----------------------------------------------------
    # Verify plotted data
    # -----------------------------------------------------

    assert np.allclose(
        line.get_xdata(),
        x,
    )

    assert np.allclose(
        line.get_ydata(),
        y,
    )

    assert line.get_label() == "Numerical"

    assert np.isclose(
        line.get_linewidth(),
        1.5,
    )

    assert line.get_linestyle() == "-"

    # -----------------------------------------------------
    # Labels
    # -----------------------------------------------------

    figure.set_labels(
        xlabel=r"$x\;(m)$",
        ylabel=r"$f(x)$",
    )

    assert figure.axes.get_xlabel() == r"$x\;(m)$"

    assert figure.axes.get_ylabel() == r"$f(x)$"

    # -----------------------------------------------------
    # Title
    # -----------------------------------------------------

    figure.set_title(r"Basic 1D line plot")

    assert figure.axes.get_title() == r"Basic 1D line plot"

    # -----------------------------------------------------
    # Legend
    # -----------------------------------------------------

    legend = figure.axes.legend(
        frameon=False,
    )

    assert legend is not None

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "example_06_basic_line"

    figure.export(
        str(output),
        formats=[
            "pdf",
            "pdf_tex",
        ],
    )

    # -----------------------------------------------------
    # Verify files
    # -----------------------------------------------------

    pdf = Path(str(output) + ".pdf")

    pdf_tex = Path(str(output) + ".pdf_tex")

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0

    # -----------------------------------------------------
    # Close
    # -----------------------------------------------------

    plt.close(figure.figure)


def test_multiple_line_workflow(
    tmp_path,
):

    # -----------------------------------------------------
    # Data
    # -----------------------------------------------------

    x = np.linspace(
        0.0,
        1.0,
        100,
    )

    y1 = np.sin(2.0 * np.pi * x)

    y2 = np.sin(2.0 * np.pi * x) * np.exp(-0.8 * x)

    y3 = np.sin(4.0 * np.pi * x) * 0.5

    data_1 = Data1D(
        x=x,
        y=y1,
        label="Case 1",
        x_label=r"$x$",
        y_label=r"$f(x)$",
        x_unit="m",
    )

    data_2 = Data1D(
        x=x,
        y=y2,
        label="Case 2",
        x_label=r"$x$",
        y_label=r"$f(x)$",
        x_unit="m",
    )

    data_3 = Data1D(
        x=x,
        y=y3,
        label="Case 3",
        x_label=r"$x$",
        y_label=r"$f(x)$",
        x_unit="m",
    )

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=3.4,
        height=2.8,
        dpi=600,
    )

    figure = PublicationFigure(figure_config)

    # -----------------------------------------------------
    # Line plot
    # -----------------------------------------------------

    line_plot = LinePlot()

    line_plot.add(
        data_1,
        label="Case 1",
        role="numerical",
    )

    line_plot.add(
        data_2,
        label="Case 2",
        role="numerical",
    )

    line_plot.add(
        data_3,
        label="Case 3",
        role="numerical",
    )

    assert line_plot.number_of_datasets == 3

    # -----------------------------------------------------
    # Plot
    # -----------------------------------------------------

    lines = line_plot.plot(figure.axes)

    assert len(lines) == 3

    # -----------------------------------------------------
    # Verify plotted data
    # -----------------------------------------------------

    assert np.allclose(
        lines[0].get_xdata(),
        x,
    )

    assert np.allclose(
        lines[0].get_ydata(),
        y1,
    )

    assert np.allclose(
        lines[1].get_xdata(),
        x,
    )

    assert np.allclose(
        lines[1].get_ydata(),
        y2,
    )

    assert np.allclose(
        lines[2].get_xdata(),
        x,
    )

    assert np.allclose(
        lines[2].get_ydata(),
        y3,
    )

    # -----------------------------------------------------
    # Verify labels
    # -----------------------------------------------------

    assert lines[0].get_label() == "Case 1"

    assert lines[1].get_label() == "Case 2"

    assert lines[2].get_label() == "Case 3"

    # -----------------------------------------------------
    # Axis labels
    # -----------------------------------------------------

    figure.set_labels(
        xlabel=r"$x\;(m)$",
        ylabel=r"$f(x)$",
    )

    assert figure.axes.get_xlabel() == r"$x\;(m)$"

    assert figure.axes.get_ylabel() == r"$f(x)$"

    # -----------------------------------------------------
    # Title
    # -----------------------------------------------------

    figure.set_title(r"Comparison of numerical cases")

    assert figure.axes.get_title() == r"Comparison of numerical cases"

    # -----------------------------------------------------
    # Legend
    # -----------------------------------------------------

    legend = figure.axes.legend(
        frameon=False,
    )

    assert legend is not None

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "example_07_multiple_lines"

    figure.export(
        str(output),
        formats=[
            "pdf",
            "pdf_tex",
        ],
    )

    # -----------------------------------------------------
    # Verify exported files
    # -----------------------------------------------------

    pdf = Path(str(output) + ".pdf")

    pdf_tex = Path(str(output) + ".pdf_tex")

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0

    # -----------------------------------------------------
    # Close
    # -----------------------------------------------------

    plt.close(figure.figure)


def test_numerical_experimental_line_workflow(
    tmp_path,
):

    # -----------------------------------------------------
    # Numerical data
    # -----------------------------------------------------

    x_numerical = np.linspace(
        0.0,
        1.0,
        200,
    )

    y_numerical = np.sin(2.0 * np.pi * x_numerical)

    numerical = Data1D(
        x=x_numerical,
        y=y_numerical,
        label="Numerical",
        x_label=r"$x$",
        y_label=r"$f(x)$",
        x_unit="m",
    )

    # -----------------------------------------------------
    # Experimental data
    # -----------------------------------------------------

    x_experimental = np.array(
        [
            0.00,
            0.10,
            0.20,
            0.30,
            0.40,
            0.50,
            0.60,
            0.70,
            0.80,
            0.90,
            1.00,
        ]
    )

    y_experimental = np.sin(2.0 * np.pi * x_experimental) + np.array(
        [
            0.02,
            -0.015,
            0.01,
            -0.02,
            0.015,
            -0.01,
            0.02,
            -0.015,
            0.01,
            -0.02,
            0.015,
        ]
    )

    experimental = Data1D(
        x=x_experimental,
        y=y_experimental,
        label="Experiment",
        x_label=r"$x$",
        y_label=r"$f(x)$",
        x_unit="m",
    )

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=3.4,
        height=2.8,
        dpi=600,
    )

    figure = PublicationFigure(figure_config)

    # -----------------------------------------------------
    # Line plot
    # -----------------------------------------------------

    line_plot = LinePlot()

    line_plot.add(
        numerical,
        label="Numerical",
        role="numerical",
    )

    line_plot.add(
        experimental,
        label="Experiment",
        role="experimental",
    )

    # -----------------------------------------------------
    # Verify datasets
    # -----------------------------------------------------

    assert line_plot.number_of_datasets == 2

    # -----------------------------------------------------
    # Plot
    # -----------------------------------------------------

    lines = line_plot.plot(figure.axes)

    assert len(lines) == 2

    # -----------------------------------------------------
    # Verify numerical data
    # -----------------------------------------------------

    assert np.allclose(
        lines[0].get_xdata(),
        x_numerical,
    )

    assert np.allclose(
        lines[0].get_ydata(),
        y_numerical,
    )

    assert lines[0].get_label() == "Numerical"

    # -----------------------------------------------------
    # Verify experimental data
    # -----------------------------------------------------

    assert np.allclose(
        lines[1].get_xdata(),
        x_experimental,
    )

    assert np.allclose(
        lines[1].get_ydata(),
        y_experimental,
    )

    assert lines[1].get_label() == "Experiment"

    # -----------------------------------------------------
    # Verify different data resolution
    # -----------------------------------------------------

    assert len(lines[0].get_xdata()) == 200

    assert len(lines[1].get_xdata()) == 11

    # -----------------------------------------------------
    # Axis labels
    # -----------------------------------------------------

    figure.set_labels(
        xlabel=r"$x\;(m)$",
        ylabel=r"$f(x)$",
    )

    assert figure.axes.get_xlabel() == r"$x\;(m)$"

    assert figure.axes.get_ylabel() == r"$f(x)$"

    # -----------------------------------------------------
    # Title
    # -----------------------------------------------------

    figure.set_title(r"Numerical and experimental comparison")

    assert figure.axes.get_title() == r"Numerical and experimental comparison"

    # -----------------------------------------------------
    # Legend
    # -----------------------------------------------------

    legend = figure.axes.legend(
        frameon=False,
    )

    assert legend is not None

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "example_08_numerical_experimental"

    figure.export(
        str(output),
        formats=[
            "pdf",
            "pdf_tex",
        ],
    )

    # -----------------------------------------------------
    # Verify exported files
    # -----------------------------------------------------

    pdf = Path(str(output) + ".pdf")

    pdf_tex = Path(str(output) + ".pdf_tex")

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0

    # -----------------------------------------------------
    # Close
    # -----------------------------------------------------

    plt.close(figure.figure)


def test_two_panel_workflow(
    tmp_path,
):

    # -----------------------------------------------------
    # Data
    # -----------------------------------------------------

    x = np.linspace(
        0.0,
        1.0,
        200,
    )

    y1 = np.sin(2.0 * np.pi * x)

    y2 = np.cos(2.0 * np.pi * x)

    data_1 = Data1D(
        x=x,
        y=y1,
        x_label=r"$x$",
        y_label=r"$f(x)$",
    )

    data_2 = Data1D(
        x=x,
        y=y2,
        x_label=r"$x$",
        y_label=r"$g(x)$",
    )

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=6.8,
        height=3.2,
        dpi=600,
    )

    figure = PublicationFigure(figure_config)

    # -----------------------------------------------------
    # Create 1 x 2 layout
    # -----------------------------------------------------

    figure.figure.clear()

    ax1, ax2 = figure.figure.subplots(
        1,
        2,
    )

    figure.figure.subplots_adjust(
        wspace=0.35,
    )

    # -----------------------------------------------------
    # Panel (a)
    # -----------------------------------------------------

    plot_1 = LinePlot()

    plot_1.add(
        data_1,
        label="sin",
        role="numerical",
    )

    lines_1 = plot_1.plot(ax1)

    assert len(lines_1) == 1

    ax1.set_xlabel(r"$x$")

    ax1.set_ylabel(r"$f(x)$")

    ax1.set_title(r"(a) Sine function")

    # -----------------------------------------------------
    # Panel (b)
    # -----------------------------------------------------

    plot_2 = LinePlot()

    plot_2.add(
        data_2,
        label="cos",
        role="numerical",
    )

    lines_2 = plot_2.plot(ax2)

    assert len(lines_2) == 1

    ax2.set_xlabel(r"$x$")

    ax2.set_ylabel(r"$g(x)$")

    ax2.set_title(r"(b) Cosine function")

    # -----------------------------------------------------
    # Verify figure structure
    # -----------------------------------------------------

    axes = figure.figure.axes

    assert len(axes) == 2

    assert axes[0] is ax1
    assert axes[1] is ax2

    assert ax1 is not ax2

    # -----------------------------------------------------
    # Verify panel (a) data
    # -----------------------------------------------------

    assert np.allclose(
        lines_1[0].get_xdata(),
        x,
    )

    assert np.allclose(
        lines_1[0].get_ydata(),
        y1,
    )

    assert lines_1[0].get_label() == "sin"

    # -----------------------------------------------------
    # Verify panel (b) data
    # -----------------------------------------------------

    assert np.allclose(
        lines_2[0].get_xdata(),
        x,
    )

    assert np.allclose(
        lines_2[0].get_ydata(),
        y2,
    )

    assert lines_2[0].get_label() == "cos"

    # -----------------------------------------------------
    # Verify labels
    # -----------------------------------------------------

    assert ax1.get_xlabel() == r"$x$"

    assert ax1.get_ylabel() == r"$f(x)$"

    assert ax2.get_xlabel() == r"$x$"

    assert ax2.get_ylabel() == r"$g(x)$"

    # -----------------------------------------------------
    # Verify titles
    # -----------------------------------------------------

    assert ax1.get_title() == r"(a) Sine function"

    assert ax2.get_title() == r"(b) Cosine function"

    # -----------------------------------------------------
    # Layout
    # -----------------------------------------------------

    figure.figure.tight_layout(
        pad=1.2,
    )

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "example_10a_two_panel"

    figure.export(
        str(output),
        formats=[
            "pdf",
            "pdf_tex",
        ],
    )

    # -----------------------------------------------------
    # Verify exported files
    # -----------------------------------------------------

    pdf = Path(str(output) + ".pdf")

    pdf_tex = Path(str(output) + ".pdf_tex")

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0

    # -----------------------------------------------------
    # Close
    # -----------------------------------------------------

    plt.close(figure.figure)


def test_shared_x_workflow(
    tmp_path,
):

    # -----------------------------------------------------
    # Data
    # -----------------------------------------------------

    x = np.linspace(
        0.0,
        1.0,
        200,
    )

    temperature = 300.0 + 50.0 * np.sin(2.0 * np.pi * x)

    pressure = 100.0 + 20.0 * np.cos(2.0 * np.pi * x)

    temperature_data = Data1D(
        x=x,
        y=temperature,
        x_label=r"$x$",
        y_label=r"$T$",
    )

    pressure_data = Data1D(
        x=x,
        y=pressure,
        x_label=r"$x$",
        y_label=r"$p$",
    )

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=3.4,
        height=5.2,
        dpi=600,
    )

    figure = PublicationFigure(figure_config)

    # -----------------------------------------------------
    # Create shared-x layout
    # -----------------------------------------------------

    figure.figure.clear()

    ax1, ax2 = figure.figure.subplots(
        2,
        1,
        sharex=True,
    )

    # -----------------------------------------------------
    # Temperature
    # -----------------------------------------------------

    temperature_plot = LinePlot()

    temperature_plot.add(
        temperature_data,
        label="Temperature",
        role="numerical",
    )

    temperature_lines = temperature_plot.plot(ax1)

    assert len(temperature_lines) == 1

    ax1.set_ylabel(r"$T\;(\mathrm{K})$")

    ax1.set_title(r"(a) Temperature distribution")

    temperature_plot.legend(
        ax1,
        location="best",
        frameon=False,
    )

    # -----------------------------------------------------
    # Pressure
    # -----------------------------------------------------

    pressure_plot = LinePlot()

    pressure_plot.add(
        pressure_data,
        label="Pressure",
        role="numerical",
    )

    pressure_lines = pressure_plot.plot(ax2)

    assert len(pressure_lines) == 1

    ax2.set_ylabel(r"$p\;(\mathrm{Pa})$")

    ax2.set_xlabel(r"$x\;(\mathrm{m})$")

    ax2.set_title(r"(b) Pressure distribution")

    pressure_plot.legend(
        ax2,
        location="best",
        frameon=False,
    )

    # -----------------------------------------------------
    # Verify figure structure
    # -----------------------------------------------------

    axes = figure.figure.axes

    assert len(axes) == 2

    assert axes[0] is ax1
    assert axes[1] is ax2

    # -----------------------------------------------------
    # Verify shared x-axis
    # -----------------------------------------------------

    assert ax1.get_shared_x_axes().joined(
        ax1,
        ax2,
    )

    # -----------------------------------------------------
    # Verify temperature data
    # -----------------------------------------------------

    assert np.allclose(
        temperature_lines[0].get_xdata(),
        x,
    )

    assert np.allclose(
        temperature_lines[0].get_ydata(),
        temperature,
    )

    assert temperature_lines[0].get_label() == "Temperature"

    # -----------------------------------------------------
    # Verify pressure data
    # -----------------------------------------------------

    assert np.allclose(
        pressure_lines[0].get_xdata(),
        x,
    )

    assert np.allclose(
        pressure_lines[0].get_ydata(),
        pressure,
    )

    assert pressure_lines[0].get_label() == "Pressure"

    # -----------------------------------------------------
    # Verify labels
    # -----------------------------------------------------

    assert ax1.get_ylabel() == r"$T\;(\mathrm{K})$"

    assert ax2.get_ylabel() == r"$p\;(\mathrm{Pa})$"

    assert ax2.get_xlabel() == r"$x\;(\mathrm{m})$"

    # -----------------------------------------------------
    # Verify titles
    # -----------------------------------------------------

    assert ax1.get_title() == r"(a) Temperature distribution"

    assert ax2.get_title() == r"(b) Pressure distribution"

    # -----------------------------------------------------
    # Layout
    # -----------------------------------------------------

    figure.figure.tight_layout(
        pad=1.2,
    )

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "example_10b_shared_x"

    figure.export(
        str(output),
        formats=[
            "pdf",
            "pdf_tex",
        ],
    )

    # -----------------------------------------------------
    # Verify exported files
    # -----------------------------------------------------

    pdf = Path(str(output) + ".pdf")

    pdf_tex = Path(str(output) + ".pdf_tex")

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0

    # -----------------------------------------------------
    # Close
    # -----------------------------------------------------

    plt.close(figure.figure)


def test_four_panel_workflow(
    tmp_path,
):

    # -----------------------------------------------------
    # Data
    # -----------------------------------------------------

    x = np.linspace(
        0.0,
        1.0,
        200,
    )

    temperature = 300.0 + 50.0 * np.sin(2.0 * np.pi * x)

    pressure = 100.0 + 20.0 * np.cos(2.0 * np.pi * x)

    velocity = 2.0 + 0.5 * np.sin(4.0 * np.pi * x)

    residual = 1.0e-1 * np.exp(-5.0 * x)

    temperature_data = Data1D(
        x=x,
        y=temperature,
    )

    pressure_data = Data1D(
        x=x,
        y=pressure,
    )

    velocity_data = Data1D(
        x=x,
        y=velocity,
    )

    residual_data = Data1D(
        x=x,
        y=residual,
    )

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=6.8,
        height=5.6,
        dpi=600,
    )

    figure = PublicationFigure(figure_config)

    # -----------------------------------------------------
    # Create 2 x 2 layout
    # -----------------------------------------------------

    figure.figure.clear()

    axes = figure.figure.subplots(
        2,
        2,
    )

    ax1 = axes[0, 0]
    ax2 = axes[0, 1]
    ax3 = axes[1, 0]
    ax4 = axes[1, 1]

    # -----------------------------------------------------
    # Panel (a) — Temperature
    # -----------------------------------------------------

    temperature_plot = LinePlot()

    temperature_plot.add(
        temperature_data,
        label="Temperature",
        role="numerical",
    )

    temperature_lines = temperature_plot.plot(ax1)

    assert len(temperature_lines) == 1

    ax1.set_xlabel(r"$x\;(\mathrm{m})$")

    ax1.set_ylabel(r"$T\;(\mathrm{K})$")

    ax1.set_title(r"(a) Temperature")

    temperature_plot.legend(
        ax1,
        frameon=False,
    )

    # -----------------------------------------------------
    # Panel (b) — Pressure
    # -----------------------------------------------------

    pressure_plot = LinePlot()

    pressure_plot.add(
        pressure_data,
        label="Pressure",
        role="numerical",
    )

    pressure_lines = pressure_plot.plot(ax2)

    assert len(pressure_lines) == 1

    ax2.set_xlabel(r"$x\;(\mathrm{m})$")

    ax2.set_ylabel(r"$p\;(\mathrm{Pa})$")

    ax2.set_title(r"(b) Pressure")

    pressure_plot.legend(
        ax2,
        frameon=False,
    )

    # -----------------------------------------------------
    # Panel (c) — Velocity
    # -----------------------------------------------------

    velocity_plot = LinePlot()

    velocity_plot.add(
        velocity_data,
        label="Velocity",
        role="numerical",
    )

    velocity_lines = velocity_plot.plot(ax3)

    assert len(velocity_lines) == 1

    ax3.set_xlabel(r"$x\;(\mathrm{m})$")

    ax3.set_ylabel(r"$U\;(\mathrm{m/s})$")

    ax3.set_title(r"(c) Velocity")

    velocity_plot.legend(
        ax3,
        frameon=False,
    )

    # -----------------------------------------------------
    # Panel (d) — Residual
    # -----------------------------------------------------

    residual_plot = LinePlot()

    residual_plot.add(
        residual_data,
        label="Residual",
        role="numerical",
    )

    residual_lines = residual_plot.plot(ax4)

    assert len(residual_lines) == 1

    ax4.set_xlabel(r"$x\;(\mathrm{m})$")

    ax4.set_ylabel(r"$R$")

    ax4.set_title(r"(d) Residual")

    residual_plot.legend(
        ax4,
        frameon=False,
    )

    # -----------------------------------------------------
    # Verify figure structure
    # -----------------------------------------------------

    figure_axes = figure.figure.axes

    assert len(figure_axes) == 4

    assert figure_axes[0] is ax1
    assert figure_axes[1] is ax2
    assert figure_axes[2] is ax3
    assert figure_axes[3] is ax4

    assert ax1 is not ax2
    assert ax1 is not ax3
    assert ax1 is not ax4
    assert ax2 is not ax3
    assert ax2 is not ax4
    assert ax3 is not ax4

    # -----------------------------------------------------
    # Verify temperature data
    # -----------------------------------------------------

    assert np.allclose(
        temperature_lines[0].get_xdata(),
        x,
    )

    assert np.allclose(
        temperature_lines[0].get_ydata(),
        temperature,
    )

    assert temperature_lines[0].get_label() == "Temperature"

    # -----------------------------------------------------
    # Verify pressure data
    # -----------------------------------------------------

    assert np.allclose(
        pressure_lines[0].get_xdata(),
        x,
    )

    assert np.allclose(
        pressure_lines[0].get_ydata(),
        pressure,
    )

    assert pressure_lines[0].get_label() == "Pressure"

    # -----------------------------------------------------
    # Verify velocity data
    # -----------------------------------------------------

    assert np.allclose(
        velocity_lines[0].get_xdata(),
        x,
    )

    assert np.allclose(
        velocity_lines[0].get_ydata(),
        velocity,
    )

    assert velocity_lines[0].get_label() == "Velocity"

    # -----------------------------------------------------
    # Verify residual data
    # -----------------------------------------------------

    assert np.allclose(
        residual_lines[0].get_xdata(),
        x,
    )

    assert np.allclose(
        residual_lines[0].get_ydata(),
        residual,
    )

    assert residual_lines[0].get_label() == "Residual"

    # -----------------------------------------------------
    # Verify labels
    # -----------------------------------------------------

    assert ax1.get_xlabel() == r"$x\;(\mathrm{m})$"

    assert ax1.get_ylabel() == r"$T\;(\mathrm{K})$"

    assert ax2.get_xlabel() == r"$x\;(\mathrm{m})$"

    assert ax2.get_ylabel() == r"$p\;(\mathrm{Pa})$"

    assert ax3.get_xlabel() == r"$x\;(\mathrm{m})$"

    assert ax3.get_ylabel() == r"$U\;(\mathrm{m/s})$"

    assert ax4.get_xlabel() == r"$x\;(\mathrm{m})$"

    assert ax4.get_ylabel() == r"$R$"

    # -----------------------------------------------------
    # Verify titles
    # -----------------------------------------------------

    assert ax1.get_title() == r"(a) Temperature"

    assert ax2.get_title() == r"(b) Pressure"

    assert ax3.get_title() == r"(c) Velocity"

    assert ax4.get_title() == r"(d) Residual"

    # -----------------------------------------------------
    # Layout
    # -----------------------------------------------------

    figure.figure.tight_layout(
        pad=1.2,
    )

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "example_10c_four_panel"

    figure.export(
        str(output),
        formats=[
            "pdf",
            "pdf_tex",
        ],
    )

    # -----------------------------------------------------
    # Verify exported files
    # -----------------------------------------------------

    pdf = Path(str(output) + ".pdf")

    pdf_tex = Path(str(output) + ".pdf_tex")

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0

    # -----------------------------------------------------
    # Close
    # -----------------------------------------------------

    plt.close(figure.figure)


def test_dual_y_axis_workflow(
    tmp_path,
):

    # -----------------------------------------------------
    # Data
    # -----------------------------------------------------

    x = np.linspace(
        0.0,
        1.0,
        200,
    )

    temperature = 300.0 + 50.0 * np.sin(2.0 * np.pi * x)

    pressure = 100.0 + 20.0 * np.cos(2.0 * np.pi * x)

    temperature_data = Data1D(
        x=x,
        y=temperature,
    )

    pressure_data = Data1D(
        x=x,
        y=pressure,
    )

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=3.4,
        height=3.0,
        dpi=600,
    )

    figure = PublicationFigure(figure_config)

    # -----------------------------------------------------
    # Primary axis
    # -----------------------------------------------------

    ax = figure.axes

    temperature_plot = LinePlot()

    temperature_plot.add(
        temperature_data,
        label="Temperature",
        role="numerical",
    )

    temperature_lines = temperature_plot.plot(ax)

    assert len(temperature_lines) == 1

    ax.set_xlabel(r"$x\;(\mathrm{m})$")

    ax.set_ylabel(r"$T\;(\mathrm{K})$")

    ax.set_title(r"Temperature and pressure")

    # -----------------------------------------------------
    # Secondary axis
    # -----------------------------------------------------

    ax_right = ax.twinx()

    pressure_plot = LinePlot()

    pressure_plot.add(
        pressure_data,
        label="Pressure",
        role="experimental",
    )

    pressure_lines = pressure_plot.plot(ax_right)

    assert len(pressure_lines) == 1

    ax_right.set_ylabel(r"$p\;(\mathrm{Pa})$")

    # -----------------------------------------------------
    # Verify two axes exist
    # -----------------------------------------------------

    axes = figure.figure.axes

    assert len(axes) == 2

    assert ax in axes
    assert ax_right in axes

    assert ax is not ax_right

    # -----------------------------------------------------
    # Verify shared x-axis
    # -----------------------------------------------------

    assert ax.get_shared_x_axes().joined(
        ax,
        ax_right,
    )

    # -----------------------------------------------------
    # Verify temperature data
    # -----------------------------------------------------

    assert np.allclose(
        temperature_lines[0].get_xdata(),
        x,
    )

    assert np.allclose(
        temperature_lines[0].get_ydata(),
        temperature,
    )

    assert temperature_lines[0].get_label() == "Temperature"

    # -----------------------------------------------------
    # Verify pressure data
    # -----------------------------------------------------

    assert np.allclose(
        pressure_lines[0].get_xdata(),
        x,
    )

    assert np.allclose(
        pressure_lines[0].get_ydata(),
        pressure,
    )

    assert pressure_lines[0].get_label() == "Pressure"

    # -----------------------------------------------------
    # Verify labels
    # -----------------------------------------------------

    assert ax.get_xlabel() == r"$x\;(\mathrm{m})$"

    assert ax.get_ylabel() == r"$T\;(\mathrm{K})$"

    assert ax_right.get_ylabel() == r"$p\;(\mathrm{Pa})$"

    assert ax.get_title() == r"Temperature and pressure"

    # -----------------------------------------------------
    # Common legend
    # -----------------------------------------------------

    handles_left, labels_left = ax.get_legend_handles_labels()

    handles_right, labels_right = ax_right.get_legend_handles_labels()

    handles = handles_left + handles_right

    labels = labels_left + labels_right

    legend = figure.figure.legend(
        handles,
        labels,
        loc="lower center",
        ncol=2,
        frameon=False,
        bbox_to_anchor=(
            0.5,
            -0.02,
        ),
    )

    assert legend is not None

    assert labels == [
        "Temperature",
        "Pressure",
    ]

    # -----------------------------------------------------
    # Layout
    # -----------------------------------------------------

    figure.figure.tight_layout(
        pad=1.2,
        rect=(
            0.0,
            0.08,
            1.0,
            1.0,
        ),
    )

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "example_11_dual_y_axis"

    figure.export(
        str(output),
        formats=[
            "pdf",
            "pdf_tex",
        ],
    )

    # -----------------------------------------------------
    # Verify exported files
    # -----------------------------------------------------

    pdf = Path(str(output) + ".pdf")

    pdf_tex = Path(str(output) + ".pdf_tex")

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0

    # -----------------------------------------------------
    # Close
    # -----------------------------------------------------

    plt.close(figure.figure)


def test_multiple_dual_y_axis_workflow(
    tmp_path,
):

    # -----------------------------------------------------
    # Data
    # -----------------------------------------------------

    x = np.linspace(
        0.0,
        1.0,
        200,
    )

    temperature_1 = 300.0 + 50.0 * np.sin(2.0 * np.pi * x)

    temperature_2 = 310.0 + 40.0 * np.sin(2.0 * np.pi * x + 0.2)

    pressure_1 = 100.0 + 20.0 * np.cos(2.0 * np.pi * x)

    pressure_2 = 110.0 + 15.0 * np.cos(2.0 * np.pi * x + 0.3)

    temperature_data_1 = Data1D(
        x=x,
        y=temperature_1,
    )

    temperature_data_2 = Data1D(
        x=x,
        y=temperature_2,
    )

    pressure_data_1 = Data1D(
        x=x,
        y=pressure_1,
    )

    pressure_data_2 = Data1D(
        x=x,
        y=pressure_2,
    )

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=3.4,
        height=3.2,
        dpi=600,
    )

    figure = PublicationFigure(figure_config)

    # -----------------------------------------------------
    # Left axis
    # -----------------------------------------------------

    ax_left = figure.axes

    left_plot = LinePlot()

    left_plot.add(
        temperature_data_1,
        label="Temperature — Case 1",
        role="numerical",
    )

    left_plot.add(
        temperature_data_2,
        label="Temperature — Case 2",
        role="experimental",
    )

    left_lines = left_plot.plot(ax_left)

    assert len(left_lines) == 2

    # -----------------------------------------------------
    # Right axis
    # -----------------------------------------------------

    ax_right = ax_left.twinx()

    right_plot = LinePlot()

    right_plot.add(
        pressure_data_1,
        label="Pressure — Case 1",
        role="numerical",
    )

    right_plot.add(
        pressure_data_2,
        label="Pressure — Case 2",
        role="experimental",
    )

    right_lines = right_plot.plot(ax_right)

    assert len(right_lines) == 2

    # -----------------------------------------------------
    # Verify axes
    # -----------------------------------------------------

    axes = figure.figure.axes

    assert len(axes) == 2

    assert ax_left is not ax_right

    # -----------------------------------------------------
    # Verify shared X-axis
    # -----------------------------------------------------

    assert ax_left.get_shared_x_axes().joined(
        ax_left,
        ax_right,
    )

    # -----------------------------------------------------
    # Verify left-axis datasets
    # -----------------------------------------------------

    assert np.allclose(
        left_lines[0].get_xdata(),
        x,
    )

    assert np.allclose(
        left_lines[0].get_ydata(),
        temperature_1,
    )

    assert np.allclose(
        left_lines[1].get_xdata(),
        x,
    )

    assert np.allclose(
        left_lines[1].get_ydata(),
        temperature_2,
    )

    # -----------------------------------------------------
    # Verify right-axis datasets
    # -----------------------------------------------------

    assert np.allclose(
        right_lines[0].get_xdata(),
        x,
    )

    assert np.allclose(
        right_lines[0].get_ydata(),
        pressure_1,
    )

    assert np.allclose(
        right_lines[1].get_xdata(),
        x,
    )

    assert np.allclose(
        right_lines[1].get_ydata(),
        pressure_2,
    )

    # -----------------------------------------------------
    # Verify labels
    # -----------------------------------------------------

    ax_left.set_xlabel(r"$x\;(\mathrm{m})$")

    ax_left.set_ylabel(r"$T\;(\mathrm{K})$")

    ax_right.set_ylabel(r"$p\;(\mathrm{Pa})$")

    assert ax_left.get_xlabel() == r"$x\;(\mathrm{m})$"

    assert ax_left.get_ylabel() == r"$T\;(\mathrm{K})$"

    assert ax_right.get_ylabel() == r"$p\;(\mathrm{Pa})$"

    # -----------------------------------------------------
    # Verify labels in legend
    # -----------------------------------------------------

    left_handles, left_labels = ax_left.get_legend_handles_labels()

    right_handles, right_labels = ax_right.get_legend_handles_labels()

    handles = left_handles + right_handles

    labels = left_labels + right_labels

    assert labels == [
        "Temperature — Case 1",
        "Temperature — Case 2",
        "Pressure — Case 1",
        "Pressure — Case 2",
    ]

    legend = figure.figure.legend(
        handles,
        labels,
        loc="lower center",
        ncol=2,
        frameon=False,
        bbox_to_anchor=(
            0.5,
            -0.04,
        ),
    )

    assert legend is not None

    # -----------------------------------------------------
    # Layout
    # -----------------------------------------------------

    figure.figure.tight_layout(
        pad=1.2,
        rect=(
            0.0,
            0.14,
            1.0,
            1.0,
        ),
    )

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "example_11b_multiple_dual_y_axis"

    figure.export(
        str(output),
        formats=[
            "pdf",
            "pdf_tex",
        ],
    )

    # -----------------------------------------------------
    # Verify files
    # -----------------------------------------------------

    pdf = Path(str(output) + ".pdf")

    pdf_tex = Path(str(output) + ".pdf_tex")

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0

    # -----------------------------------------------------
    # Close
    # -----------------------------------------------------

    plt.close(figure.figure)


def test_multiple_dual_y_axis_grouped_legend_workflow(
    tmp_path,
):
    """
    Regression test for a multi-dataset dual-Y-axis
    workflow with a grouped/table-style legend.
    """

    # -----------------------------------------------------
    # Data
    # -----------------------------------------------------

    x = np.linspace(
        0.0,
        1.0,
        100,
    )

    temperature_1 = 300.0 + 50.0 * np.sin(2.0 * np.pi * x)

    temperature_2 = 310.0 + 40.0 * np.sin(2.0 * np.pi * x + 0.2)

    pressure_1 = 100.0 + 20.0 * np.cos(2.0 * np.pi * x)

    pressure_2 = 110.0 + 15.0 * np.cos(2.0 * np.pi * x + 0.3)

    temperature_data_1 = Data1D(
        x=x,
        y=temperature_1,
    )

    temperature_data_2 = Data1D(
        x=x,
        y=temperature_2,
    )

    pressure_data_1 = Data1D(
        x=x,
        y=pressure_1,
    )

    pressure_data_2 = Data1D(
        x=x,
        y=pressure_2,
    )

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=3.4,
        height=3.2,
        dpi=600,
    )

    figure = PublicationFigure(figure_config)

    ax_left = figure.axes

    # -----------------------------------------------------
    # Left Y-axis
    # -----------------------------------------------------

    left_plot = LinePlot()

    left_plot.add(
        temperature_data_1,
        label="Case 1",
        role="numerical",
    )

    left_plot.add(
        temperature_data_2,
        label="Case 2",
        role="experimental",
    )

    left_lines = left_plot.plot(ax_left)

    assert len(left_lines) == 2

    ax_left.set_xlabel(r"$x\;(\mathrm{m})$")

    ax_left.set_ylabel(r"$T\;(\mathrm{K})$")

    # -----------------------------------------------------
    # Right Y-axis
    # -----------------------------------------------------

    ax_right = ax_left.twinx()

    right_plot = LinePlot()

    right_plot.add(
        pressure_data_1,
        label="Case 1",
        role="numerical",
    )

    right_plot.add(
        pressure_data_2,
        label="Case 2",
        role="experimental",
    )

    right_lines = right_plot.plot(ax_right)

    assert len(right_lines) == 2

    ax_right.set_ylabel(r"$p\;(\mathrm{Pa})$")

    # -----------------------------------------------------
    # Grouped legend
    # -----------------------------------------------------

    groups = {
        "Temperature": {
            "Case 1": left_lines[0],
            "Case 2": left_lines[1],
        },
        "Pressure": {
            "Case 1": right_lines[0],
            "Case 2": right_lines[1],
        },
    }

    legend = left_plot.legend_table(
        ax_left,
        groups,
        location="lower center",
        bbox_to_anchor=(
            0.5,
            -0.04,
        ),
        fontsize=8,
    )

    assert legend is not None

    # -----------------------------------------------------
    # Basic structural checks
    # -----------------------------------------------------

    assert len(groups) == 2

    assert list(groups.keys()) == [
        "Temperature",
        "Pressure",
    ]

    assert list(groups["Temperature"].keys()) == [
        "Case 1",
        "Case 2",
    ]

    assert list(groups["Pressure"].keys()) == [
        "Case 1",
        "Case 2",
    ]

    # -----------------------------------------------------
    # Verify marker preservation
    # -----------------------------------------------------

    assert left_lines[1].get_marker() != "None"

    assert right_lines[1].get_marker() != "None"

    # -----------------------------------------------------
    # Layout
    # -----------------------------------------------------

    figure.figure.tight_layout(
        pad=1.2,
        rect=(
            0.0,
            0.14,
            1.0,
            1.0,
        ),
    )

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "dual_y_axis_grouped_legend"

    figure.export(
        str(output),
        formats=[
            "pdf",
        ],
    )

    # -----------------------------------------------------
    # Verify export
    # -----------------------------------------------------

    assert output.with_suffix(".pdf").exists()


def test_vtp_cfd_geometry_dimensions_workflow(
    tmp_path,
):
    """
    Regression test for the complete CFD visualization
    with contour, mesh, vectors, streamlines, and
    geometry dimensions.
    """

    # -----------------------------------------------------
    # Read
    # -----------------------------------------------------

    data = read_vtp(INPUT_FILE)

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=3.4,
        height=3.4,
        dpi=600,
    )

    figure = PublicationFigure(figure_config)

    axes = figure.axes

    # -----------------------------------------------------
    # Contour
    # -----------------------------------------------------

    contour_plot = ContourPlot(
        data,
        field="gammaDV",
        association="cell",
    )

    contour = contour_plot.plot(axes)

    assert contour is not None

    # -----------------------------------------------------
    # Mesh
    # -----------------------------------------------------

    mesh_plot = MeshPlot(data)

    mesh = mesh_plot.plot(
        axes,
        edgecolor="black",
        facecolor="none",
        linewidth=0.15,
        alpha=0.35,
    )

    assert mesh is not None

    mesh.set_zorder(3)

    # -----------------------------------------------------
    # Vectors
    # -----------------------------------------------------

    vector_plot = VectorPlot(
        data,
        field="U",
        association="cell",
    )

    vectors = vector_plot.plot(
        axes,
        normalize=True,
        density=18,
        scale=25,
        width=0.002,
        color="black",
        alpha=0.85,
        pivot="mid",
        zorder=5,
    )

    assert vectors is not None

    # -----------------------------------------------------
    # Streamlines
    # -----------------------------------------------------

    streamline_plot = StreamlinePlot(
        data,
        field="U",
        association="cell",
    )

    streamlines = streamline_plot.plot(
        axes,
        n_seeds=20,
        seed_axis="y",
        seed_position=None,
        seed_margin=0.02,
        integration_direction="forward",
        integrator_type=45,
        surface_streamlines=True,
        initial_step_length=0.1,
        min_step_length=0.01,
        max_step_length=0.5,
        max_steps=2000,
        max_length=None,
        terminal_speed=1e-12,
        max_error=1e-6,
        interpolator_type="cell",
        color="black",
        linewidth=0.8,
        arrowsize=1.0,
        zorder=6,
    )

    assert streamlines is not None

    # -----------------------------------------------------
    # Geometry bounds
    # -----------------------------------------------------

    x_min, x_max, y_min, y_max = data.mesh.bounds

    geometry_width = x_max - x_min

    geometry_height = y_max - y_min

    # -----------------------------------------------------
    # Dimension positions
    # -----------------------------------------------------

    dimension_y = y_min - 0.10 * geometry_height

    dimension_x = x_min - 0.10 * geometry_width

    # -----------------------------------------------------
    # Horizontal dimension
    # -----------------------------------------------------

    AnnotationPlot.add_line(
        axes,
        start=(
            x_min,
            dimension_y,
        ),
        end=(
            x_max,
            dimension_y,
        ),
        color="black",
        linewidth=0.8,
        zorder=10,
    )

    AnnotationPlot.add_line(
        axes,
        start=(
            x_min,
            y_min,
        ),
        end=(
            x_min,
            dimension_y,
        ),
        color="black",
        linewidth=0.8,
        zorder=10,
    )

    AnnotationPlot.add_line(
        axes,
        start=(
            x_max,
            y_min,
        ),
        end=(
            x_max,
            dimension_y,
        ),
        color="black",
        linewidth=0.8,
        zorder=10,
    )

    AnnotationPlot.add_arrow(
        axes,
        start=(
            x_min + 0.10 * geometry_width,
            dimension_y,
        ),
        end=(
            x_min,
            dimension_y,
        ),
        color="black",
        linewidth=0.8,
        headwidth=0.04,
        headlength=0.07,
        zorder=10,
    )

    AnnotationPlot.add_arrow(
        axes,
        start=(
            x_max - 0.10 * geometry_width,
            dimension_y,
        ),
        end=(
            x_max,
            dimension_y,
        ),
        color="black",
        linewidth=0.8,
        headwidth=0.04,
        headlength=0.07,
        zorder=10,
    )

    AnnotationPlot.add_text(
        axes,
        x=(x_min + 0.50 * geometry_width),
        y=(dimension_y - 0.025 * geometry_height),
        text=r"$L$",
        fontsize=10,
        ha="center",
        va="top",
        zorder=11,
    )

    # -----------------------------------------------------
    # Vertical dimension
    # -----------------------------------------------------

    AnnotationPlot.add_line(
        axes,
        start=(
            dimension_x,
            y_min,
        ),
        end=(
            dimension_x,
            y_max,
        ),
        color="black",
        linewidth=0.8,
        zorder=10,
    )

    AnnotationPlot.add_line(
        axes,
        start=(
            x_min,
            y_min,
        ),
        end=(
            dimension_x,
            y_min,
        ),
        color="black",
        linewidth=0.8,
        zorder=10,
    )

    AnnotationPlot.add_line(
        axes,
        start=(
            x_min,
            y_max,
        ),
        end=(
            dimension_x,
            y_max,
        ),
        color="black",
        linewidth=0.8,
        zorder=10,
    )

    AnnotationPlot.add_arrow(
        axes,
        start=(
            dimension_x,
            y_min + 0.10 * geometry_height,
        ),
        end=(
            dimension_x,
            y_min,
        ),
        color="black",
        linewidth=0.8,
        headwidth=0.04,
        headlength=0.07,
        zorder=10,
    )

    AnnotationPlot.add_arrow(
        axes,
        start=(
            dimension_x,
            y_max - 0.10 * geometry_height,
        ),
        end=(
            dimension_x,
            y_max,
        ),
        color="black",
        linewidth=0.8,
        headwidth=0.04,
        headlength=0.07,
        zorder=10,
    )

    AnnotationPlot.add_text(
        axes,
        x=(dimension_x - 0.025 * geometry_width),
        y=(y_min + 0.50 * geometry_height),
        text=r"$H$",
        fontsize=10,
        ha="right",
        va="center",
        rotation=90,
        zorder=11,
    )

    # -----------------------------------------------------
    # Geometry annotation
    # -----------------------------------------------------

    annotation = AnnotationPlot.add_text(
        axes,
        x=(x_min + 0.50 * geometry_width),
        y=(y_max + 0.035 * geometry_height),
        text=r"Computational domain",
        fontsize=8,
        ha="center",
        va="bottom",
        zorder=11,
    )

    assert annotation is not None

    # -----------------------------------------------------
    # Axes
    # -----------------------------------------------------

    axes.set_xlabel(r"$x\;(\mathrm{m})$")

    axes.set_ylabel(r"$y\;(\mathrm{m})$")

    axes.set_aspect(
        "equal",
        adjustable="box",
    )

    axes.grid(False)

    # -----------------------------------------------------
    # Expanded limits
    # -----------------------------------------------------

    axes.set_xlim(
        x_min - 0.16 * geometry_width,
        x_max + 0.02 * geometry_width,
    )

    axes.set_ylim(
        y_min - 0.16 * geometry_height,
        y_max + 0.08 * geometry_height,
    )

    # -----------------------------------------------------
    # Layout
    # -----------------------------------------------------

    figure.figure.tight_layout(
        pad=1.0,
    )

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "cfd_geometry_dimensions"

    figure.export(
        str(output),
        formats=[
            "pdf",
        ],
    )

    # -----------------------------------------------------
    # Verify export
    # -----------------------------------------------------

    assert output.with_suffix(".pdf").exists()


def test_color_schemes_and_custom_palettes_workflow(
    tmp_path,
):
    """
    Regression test for Example 17.

    Verifies the categorical color schemes, custom
    categorical palette, custom contour colormap,
    and final PDF export.
    """

    import numpy as np
    from matplotlib.colors import (
        LinearSegmentedColormap,
    )

    from postprocess.data.data1d import (
        Data1D,
    )
    from postprocess.layout.figure import (
        FigureConfig,
        PublicationFigure,
    )
    from postprocess.plots.line import (
        LinePlot,
    )
    from postprocess.style.publication import (
        PublicationStyle,
    )

    # -----------------------------------------------------
    # Data
    # -----------------------------------------------------

    x = np.linspace(
        0.0,
        1.0,
        100,
    )

    datasets = [
        Data1D(
            x=x,
            y=np.sin(2.0 * np.pi * x),
            label="Case 1",
        ),
        Data1D(
            x=x,
            y=np.cos(2.0 * np.pi * x),
            label="Case 2",
        ),
        Data1D(
            x=x,
            y=np.sin(4.0 * np.pi * x),
            label="Case 3",
        ),
    ]

    # -----------------------------------------------------
    # Custom categorical palette
    # -----------------------------------------------------

    custom_palette = [
        "#264653",
        "#2A9D8F",
        "#E9C46A",
        "#F4A261",
        "#E76F51",
    ]

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=7.0,
        height=7.0,
        dpi=600,
    )

    figure = PublicationFigure(
        figure_config,
        nrows=2,
        ncols=2,
        sharex=True,
    )

    # -----------------------------------------------------
    # Test built-in schemes
    # -----------------------------------------------------

    schemes = [
        "default",
        "colorblind",
        "grayscale",
        "blackwhite",
    ]

    for index, scheme in enumerate(schemes):
        row = index // 2
        col = index % 2

        axes = figure.panel(
            row,
            col,
        )

        style = PublicationStyle(
            color_scheme=scheme,
        )

        plot = LinePlot(
            style=style,
        )

        for data in datasets:
            plot.add(
                data,
                label=data.label,
            )

        artists = plot.plot(axes)

        assert len(artists) == 3

        # Verify the actual colors came from
        # the selected style.

        for i, artist in enumerate(artists):
            assert artist.get_color() == style.color(i)

    # -----------------------------------------------------
    # Custom palette
    # -----------------------------------------------------

    custom_style = PublicationStyle(
        color_scheme=custom_palette,
    )

    custom_plot = LinePlot(
        style=custom_style,
    )

    for data in datasets:
        custom_plot.add(
            data,
            label=data.label,
        )

    custom_axes = figure.panel(
        1,
        1,
    )

    custom_artists = custom_plot.plot(custom_axes)

    assert len(custom_artists) == 3

    for i, artist in enumerate(custom_artists):
        assert artist.get_color() == custom_palette[i]

    # -----------------------------------------------------
    # Custom contour colormap
    # -----------------------------------------------------

    custom_cmap = LinearSegmentedColormap.from_list(
        "test_custom_palette",
        [
            "#132B43",
            "#1F77B4",
            "#2A9D8F",
            "#E9C46A",
            "#E76F51",
        ],
    )

    # Verify that the colormap can be used
    # as a Matplotlib colormap.

    assert custom_cmap.name == "test_custom_palette"

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "color_schemes"

    figure.export(
        str(output),
        formats=[
            "pdf",
        ],
    )

    # -----------------------------------------------------
    # Verify export
    # -----------------------------------------------------

    assert output.with_suffix(".pdf").exists()

    # -----------------------------------------------------
    # Close
    # -----------------------------------------------------

    figure.close()


def test_multiple_scalar_fields_workflow(
    tmp_path,
):
    """
    Regression test for Example 18.

    Verifies:

        - one common scalar scale
        - independent scalar scale
        - two shared colorbars
        - 2x2 publication layout
        - PDF export
    """

    import numpy as np
    from matplotlib.collections import (
        PolyCollection,
    )

    from postprocess.io.vtp import (
        read_vtp,
    )
    from postprocess.layout.colors import (
        ColorScale,
    )
    from postprocess.layout.figure import (
        FigureConfig,
        PublicationFigure,
    )
    from postprocess.plots.contour import (
        ContourPlot,
    )
    from postprocess.plots.mesh import (
        MeshPlot,
    )

    # -----------------------------------------------------
    # Read
    # -----------------------------------------------------

    data = read_vtp("data/zNormal.vtp")

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=7.0,
        height=7.2,
        dpi=600,
        aspect="equal",
    )

    figure = PublicationFigure(
        figure_config,
        nrows=2,
        ncols=2,
        sharex=True,
        sharey=True,
    )

    ax00 = figure.panel(
        0,
        0,
    )

    ax01 = figure.panel(
        0,
        1,
    )

    ax10 = figure.panel(
        1,
        0,
    )

    ax11 = figure.panel(
        1,
        1,
    )

    # -----------------------------------------------------
    # Primary scalar
    # -----------------------------------------------------

    gamma = np.asarray(
        data.get_field(
            "gammaDV",
            "cell",
        )
    )

    gamma_scale = ColorScale(
        levels=30,
        cmap="viridis",
    )

    gamma_scale.resolve(gamma)

    contour_a = ContourPlot(
        data,
        field="gammaDV",
        association="cell",
    ).plot(
        ax00,
        scale=gamma_scale,
    )

    contour_b = ContourPlot(
        data,
        field="gammaDV",
        association="cell",
    ).plot(
        ax01,
        scale=gamma_scale,
    )

    assert contour_a is not None
    assert contour_b is not None

    # -----------------------------------------------------
    # Derived scalar
    # -----------------------------------------------------

    gamma_min = np.nanmin(gamma)

    gamma_max = np.nanmax(gamma)

    gamma_normalized = (gamma - gamma_min) / (gamma_max - gamma_min)

    phi = gamma_normalized**2

    phi_scale = ColorScale(
        levels=30,
        cmap="plasma",
    )

    phi_scale.resolve(phi)

    polygons = data.mesh.polygons

    phi_c = ax10.add_collection(
        PolyCollection(
            polygons,
            array=phi,
            cmap=phi_scale.colormap,
            norm=phi_scale.norm,
            edgecolors="none",
        )
    )

    phi_d = ax11.add_collection(
        PolyCollection(
            polygons,
            array=phi,
            cmap=phi_scale.colormap,
            norm=phi_scale.norm,
            edgecolors="none",
        )
    )

    assert phi_c is not None
    assert phi_d is not None

    # -----------------------------------------------------
    # Mesh
    # -----------------------------------------------------

    mesh = MeshPlot(data)

    assert (
        mesh.plot(
            ax01,
            edgecolor="black",
            facecolor="none",
            linewidth=0.15,
            alpha=0.35,
        )
        is not None
    )

    assert (
        mesh.plot(
            ax11,
            edgecolor="black",
            facecolor="none",
            linewidth=0.15,
            alpha=0.35,
        )
        is not None
    )

    # -----------------------------------------------------
    # Colorbars
    # -----------------------------------------------------

    gamma_cb = figure.add_shared_colorbar(
        contour_a,
        axes=[
            ax00,
            ax01,
        ],
        label=r"$\gamma_{\mathrm{DV}}$",
        orientation="horizontal",
        fraction=0.045,
        pad=0.08,
        shrink=0.75,
    )

    phi_cb = figure.add_shared_colorbar(
        phi_c,
        axes=[
            ax10,
            ax11,
        ],
        label=r"$\phi$",
        orientation="horizontal",
        fraction=0.045,
        pad=0.18,
        shrink=0.75,
    )

    assert gamma_cb is not None
    assert phi_cb is not None

    # -----------------------------------------------------
    # Panel labels
    # -----------------------------------------------------

    figure.label_panels(
        labels=[
            "(a)",
            "(b)",
            "(c)",
            "(d)",
        ]
    )

    # -----------------------------------------------------
    # Common labels
    # -----------------------------------------------------

    figure.set_common_xlabel(r"$x\;(\mathrm{m})$")

    figure.set_common_ylabel(r"$y\;(\mathrm{m})$")

    # -----------------------------------------------------
    # Layout
    # -----------------------------------------------------

    figure.adjust_layout(
        left=0.09,
        right=0.97,
        bottom=0.23,
        top=0.97,
        wspace=0.08,
        hspace=0.08,
    )

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = tmp_path / "multiple_scalar_fields"

    figure.export(
        str(output),
        formats=[
            "pdf",
        ],
    )

    assert output.with_suffix(".pdf").exists()

    figure.close()


def test_example_18_multiple_scalar_fields(
    tmp_path,
):

    import numpy as np
    from matplotlib.collections import (
        PolyCollection,
    )

    from postprocess.io.vtp import (
        read_vtp,
    )
    from postprocess.layout.colors import (
        ColorScale,
    )
    from postprocess.layout.figure import (
        FigureConfig,
        PublicationFigure,
    )
    from postprocess.plots.contour import (
        ContourPlot,
    )
    from postprocess.plots.mesh import (
        MeshPlot,
    )

    # =====================================================
    # Read input
    # =====================================================

    data = read_vtp("data/zNormal.vtp")

    # =====================================================
    # Geometry
    # =====================================================

    x_min, x_max, y_min, y_max = data.mesh.bounds

    # =====================================================
    # gammaDV
    # =====================================================

    gamma = np.asarray(
        data.get_field(
            "gammaDV",
            "cell",
        )
    )

    gamma_min = np.nanmin(gamma)

    gamma_max = np.nanmax(gamma)

    gamma_scale = ColorScale(
        levels=30,
        cmap="viridis",
        vmin=gamma_min,
        vmax=gamma_max,
    )

    gamma_scale.resolve(gamma)

    # =====================================================
    # Derived scalar
    # =====================================================

    gamma_normalized = (gamma - gamma_min) / (gamma_max - gamma_min)

    phi = gamma_normalized**2

    phi_min = np.nanmin(phi)

    phi_max = np.nanmax(phi)

    phi_scale = ColorScale(
        levels=30,
        cmap="plasma",
        vmin=phi_min,
        vmax=phi_max,
    )

    phi_scale.resolve(phi)

    # =====================================================
    # Verify independent scales
    # =====================================================

    assert gamma_scale.limits == (
        gamma_min,
        gamma_max,
    )

    assert phi_scale.limits == (
        phi_min,
        phi_max,
    )

    assert gamma_scale.colormap.name == "viridis"

    assert phi_scale.colormap.name == "plasma"

    # =====================================================
    # Figure
    # =====================================================

    figure_config = FigureConfig(
        width=7.0,
        height=8.0,
        dpi=600,
        aspect="equal",
    )

    figure = PublicationFigure(
        figure_config,
        nrows=2,
        ncols=2,
        sharex=True,
        sharey=True,
    )

    axes = [
        figure.panel(0, 0),
        figure.panel(0, 1),
        figure.panel(1, 0),
        figure.panel(1, 1),
    ]

    ax00 = axes[0]
    ax01 = axes[1]
    ax10 = axes[2]
    ax11 = axes[3]

    # =====================================================
    # gammaDV panels
    # =====================================================

    contour_a = ContourPlot(
        data,
        field="gammaDV",
        association="cell",
    ).plot(
        ax00,
        scale=gamma_scale,
    )

    contour_b = ContourPlot(
        data,
        field="gammaDV",
        association="cell",
    ).plot(
        ax01,
        scale=gamma_scale,
    )

    assert contour_a is not None
    assert contour_b is not None

    # =====================================================
    # Mesh
    # =====================================================

    mesh = MeshPlot(data)

    assert (
        mesh.plot(
            ax01,
            edgecolor="black",
            facecolor="none",
            linewidth=0.15,
            alpha=0.35,
        )
        is not None
    )

    # =====================================================
    # phi panels
    # =====================================================

    polygons = data.mesh.polygons

    phi_collection_c = ax10.add_collection(
        PolyCollection(
            polygons,
            array=phi,
            cmap=phi_scale.colormap,
            norm=phi_scale.norm,
            edgecolors="none",
            linewidths=0.0,
            antialiased=True,
        )
    )

    phi_collection_d = ax11.add_collection(
        PolyCollection(
            polygons,
            array=phi,
            cmap=phi_scale.colormap,
            norm=phi_scale.norm,
            edgecolors="none",
            linewidths=0.0,
            antialiased=True,
        )
    )

    assert phi_collection_c is not None
    assert phi_collection_d is not None

    # =====================================================
    # Mesh on phi panel
    # =====================================================

    assert (
        mesh.plot(
            ax11,
            edgecolor="black",
            facecolor="none",
            linewidth=0.15,
            alpha=0.35,
        )
        is not None
    )

    # =====================================================
    # Axes
    # =====================================================

    for ax in axes:
        ax.set_xlim(
            x_min,
            x_max,
        )

        ax.set_ylim(
            y_min,
            y_max,
        )

        ax.set_aspect(
            "equal",
            adjustable="box",
        )

        ax.grid(False)

    # =====================================================
    # Layout
    # =====================================================

    figure.adjust_layout(
        left=0.09,
        right=0.97,
        bottom=0.17,
        top=0.97,
        wspace=0.08,
        hspace=0.42,
    )

    # =====================================================
    # Colorbar axes
    # =====================================================

    gamma_cbar_ax = figure.figure.add_axes(
        [
            0.20,
            0.45,
            0.60,
            0.018,
        ]
    )

    phi_cbar_ax = figure.figure.add_axes(
        [
            0.20,
            0.08,
            0.60,
            0.018,
        ]
    )

    # =====================================================
    # Colorbars
    # =====================================================

    gamma_colorbar = figure.figure.colorbar(
        contour_a,
        cax=gamma_cbar_ax,
        orientation="horizontal",
    )

    phi_colorbar = figure.figure.colorbar(
        phi_collection_c,
        cax=phi_cbar_ax,
        orientation="horizontal",
    )

    gamma_colorbar.set_ticks(
        np.linspace(
            gamma_min,
            gamma_max,
            5,
        )
    )

    phi_colorbar.set_ticks(
        np.linspace(
            phi_min,
            phi_max,
            5,
        )
    )

    gamma_colorbar.set_label(r"$\gamma_{\mathrm{DV}}$")

    phi_colorbar.set_label(r"$\phi$")

    # =====================================================
    # Assertions
    # =====================================================

    assert gamma_colorbar.orientation == "horizontal"

    assert phi_colorbar.orientation == "horizontal"

    assert gamma_cbar_ax is gamma_colorbar.ax

    assert phi_cbar_ax is phi_colorbar.ax

    assert gamma_cbar_ax.get_position().y0 != phi_cbar_ax.get_position().y0

    # =====================================================
    # Export
    # =====================================================

    output = tmp_path / "example_18_multiple_scalar_fields"

    figure.export(
        str(output),
        formats=[
            "png",
        ],
    )

    assert output.with_suffix(".png").exists()

    figure.close()


def test_example_19_final_publication_figure(
    tmp_path,
):

    import numpy as np

    from postprocess.data.data1d import (
        Data1D,
    )
    from postprocess.io.vtp import (
        read_vtp,
    )
    from postprocess.layout.colors import (
        ColorScale,
    )
    from postprocess.layout.figure import (
        FigureConfig,
        PublicationFigure,
    )
    from postprocess.plots.contour import (
        ContourPlot,
    )
    from postprocess.plots.line import (
        LinePlot,
    )
    from postprocess.plots.mesh import (
        MeshPlot,
    )
    from postprocess.style.publication import (
        PublicationStyle,
    )

    # =====================================================
    # Input
    # =====================================================

    vtp = read_vtp("data/zNormal.vtp")

    numerical = np.loadtxt("data/numerical.dat")

    analytical = np.loadtxt("data/analytical.dat")

    experiment = np.loadtxt("data/experiment.dat")

    # =====================================================
    # Data1D
    # =====================================================

    numerical_data = Data1D(
        x=numerical[:, 0],
        y=numerical[:, 1],
    )

    analytical_data = Data1D(
        x=analytical[:, 0],
        y=analytical[:, 1],
    )

    experiment_data = Data1D(
        x=experiment[:, 0],
        y=experiment[:, 1],
    )

    # =====================================================
    # gammaDV
    # =====================================================

    gamma = np.asarray(
        vtp.get_field(
            "gammaDV",
            "cell",
        )
    )

    gamma_min = np.nanmin(gamma)

    gamma_max = np.nanmax(gamma)

    gamma_scale = ColorScale(
        levels=30,
        cmap="viridis",
        vmin=gamma_min,
        vmax=gamma_max,
    )

    gamma_scale.resolve(gamma)

    # =====================================================
    # Figure
    # =====================================================

    figure_config = FigureConfig(
        width=7.0,
        height=7.2,
        dpi=600,
        aspect="auto",
    )

    figure = PublicationFigure(
        figure_config,
        nrows=2,
        ncols=2,
        sharex=False,
        sharey=False,
    )

    ax00 = figure.panel(
        0,
        0,
    )

    ax01 = figure.panel(
        0,
        1,
    )

    ax10 = figure.panel(
        1,
        0,
    )

    ax11 = figure.panel(
        1,
        1,
    )

    # =====================================================
    # Panel (a)
    # =====================================================

    contour_a = ContourPlot(
        vtp,
        field="gammaDV",
        association="cell",
    ).plot(
        ax00,
        scale=gamma_scale,
    )

    assert contour_a is not None

    # =====================================================
    # Panel (b)
    # =====================================================

    contour_b = ContourPlot(
        vtp,
        field="gammaDV",
        association="cell",
    ).plot(
        ax01,
        scale=gamma_scale,
    )

    assert contour_b is not None

    mesh = MeshPlot(vtp)

    assert (
        mesh.plot(
            ax01,
            edgecolor="black",
            facecolor="none",
            linewidth=0.15,
            alpha=0.35,
        )
        is not None
    )

    # =====================================================
    # Panel (c)
    # =====================================================

    style = PublicationStyle(
        color_scheme="colorblind",
    )

    comparison_plot = LinePlot(
        style=style,
    )

    comparison_plot.add(
        numerical_data,
        label="Numerical",
    )

    comparison_plot.add(
        experiment_data,
        label="Experiment",
    )

    comparison_artists = comparison_plot.plot(ax10)

    assert len(comparison_artists) == 2

    legend_c = comparison_plot.legend(
        ax10,
        location="best",
        frameon=False,
        ncol=1,
        fontsize=8,
    )

    assert legend_c is not None

    # =====================================================
    # Panel (d)
    # =====================================================

    analytical_plot = LinePlot(
        style=style,
    )

    analytical_plot.add(
        numerical_data,
        label="Numerical",
    )

    analytical_plot.add(
        analytical_data,
        label="Analytical",
    )

    analytical_artists = analytical_plot.plot(ax11)

    assert len(analytical_artists) == 2

    legend_d = analytical_plot.legend(
        ax11,
        location="best",
        frameon=False,
        ncol=1,
        fontsize=8,
    )

    assert legend_d is not None

    # =====================================================
    # CFD geometry
    # =====================================================

    x_min, x_max, y_min, y_max = vtp.mesh.bounds

    for ax in (
        ax00,
        ax01,
    ):
        ax.set_xlim(
            x_min,
            x_max,
        )

        ax.set_ylim(
            y_min,
            y_max,
        )

        ax.set_aspect(
            "equal",
            adjustable="box",
        )

    # =====================================================
    # Panel labels
    # =====================================================

    figure.label_panels(
        labels=[
            "(a)",
            "(b)",
            "(c)",
            "(d)",
        ],
        x=0.02,
        y=0.97,
        fontsize=10,
    )

    # =====================================================
    # Shared colorbar
    # =====================================================

    colorbar = figure.add_shared_colorbar(
        contour_a,
        axes=[
            ax00,
            ax01,
        ],
        label=r"$\gamma_{\mathrm{DV}}$",
        orientation="horizontal",
        fraction=0.045,
        pad=0.08,
        shrink=0.75,
    )

    assert colorbar is not None

    colorbar.set_ticks(
        np.linspace(
            gamma_min,
            gamma_max,
            5,
        )
    )

    # =====================================================
    # Layout
    # =====================================================

    figure.adjust_layout(
        left=0.10,
        right=0.97,
        bottom=0.10,
        top=0.97,
        wspace=0.25,
        hspace=0.35,
    )

    # =====================================================
    # Export
    # =====================================================

    output = tmp_path / "example_19_final_publication_figure"

    figure.export(
        str(output),
        formats=[
            "png",
        ],
    )

    assert output.with_suffix(".png").exists()

    # =====================================================
    # Close
    # =====================================================

    figure.close()
