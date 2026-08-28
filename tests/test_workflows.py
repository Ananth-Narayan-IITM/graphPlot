import matplotlib

matplotlib.use(
    "Agg"
)

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from postprocess.io.vtp import read_vtp

from postprocess.plots.contour import ContourPlot
from postprocess.plots.mesh import MeshPlot
from postprocess.plots.vector import VectorPlot
from postprocess.plots.streamline import StreamlinePlot
from postprocess.plots.annotation import AnnotationPlot
from postprocess.data.data1d import Data1D
from postprocess.plots.line import LinePlot
from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)
INPUT_FILE = "data/zNormal.vtp"


def test_vtp_contour_workflow(
    tmp_path
):

    # -----------------------------------------------------
    # Read
    # -----------------------------------------------------

    data = read_vtp(
        INPUT_FILE
    )

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=3.4,
        height=3.0,
    )

    figure = PublicationFigure(
        figure_config
    )

    # -----------------------------------------------------
    # Contour
    # -----------------------------------------------------

    contour_plot = ContourPlot(
        data,
        field="gammaDV",
    )

    contour = contour_plot.plot(
        figure.axes
    )

    assert contour is not None

    # -----------------------------------------------------
    # Export
    # -----------------------------------------------------

    output = (
        tmp_path /
        "example_01_vtp_contour"
    )

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

    pdf = Path(
        str(output) + ".pdf"
    )

    pdf_tex = Path(
        str(output) + ".pdf_tex"
    )

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0

def test_vtp_contour_mesh_workflow(
    tmp_path
):

    # -----------------------------------------------------
    # Read
    # -----------------------------------------------------

    data = read_vtp(
        INPUT_FILE
    )

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=3.4,
        height=3.0,
        dpi=600,
    )

    figure = PublicationFigure(
        figure_config
    )

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

    mesh_plot = MeshPlot(
        data
    )

    mesh = mesh_plot.plot(
        figure.axes,
        edgecolor="black",
        facecolor="none",
        linewidth=0.15,
        alpha=0.35,
    )

    assert mesh is not None

    assert mesh.get_rasterized() is False

    mesh.set_rasterized(
        True
    )

    assert mesh.get_rasterized() is True

    # -----------------------------------------------------
    # Labels
    # -----------------------------------------------------

    figure.set_labels(
        xlabel=r"$x\;(m)$",
        ylabel=r"$y\;(m)$",
    )

    figure.set_title(
        r"$\gamma_{\mathrm{DV}}$ distribution"
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

    output = (
        tmp_path /
        "example_02_vtp_contour_mesh"
    )

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

    pdf = Path(
        str(output) + ".pdf"
    )

    pdf_tex = Path(
        str(output) + ".pdf_tex"
    )

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0

def test_vtp_contour_vector_workflow(
    tmp_path
):

    # -----------------------------------------------------
    # Read
    # -----------------------------------------------------

    data = read_vtp(
        INPUT_FILE
    )

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=3.4,
        height=3.0,
        dpi=600,
    )

    figure = PublicationFigure(
        figure_config
    )

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

    output = (
        tmp_path /
        "example_03_vtp_contour_vector"
    )

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

    pdf = Path(
        str(output) + ".pdf"
    )

    pdf_tex = Path(
        str(output) + ".pdf_tex"
    )

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

    data = read_vtp(
        INPUT_FILE
    )

    # -----------------------------------------------------
    # Figure
    # -----------------------------------------------------

    figure_config = FigureConfig(
        width=3.4,
        height=3.0,
    )

    figure = PublicationFigure(
        figure_config
    )

    # -----------------------------------------------------
    # Contour
    # -----------------------------------------------------

    contour_plot = ContourPlot(
        data,
        field="gammaDV",
        association="cell",
    )

    contour = contour_plot.plot(
        figure.axes
    )

    assert contour is not None

    # -----------------------------------------------------
    # Mesh
    # -----------------------------------------------------

    mesh_plot = MeshPlot(
        data
    )

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
    assert len(
        figure.axes.lines
    ) > 0

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

    figure.set_title(
        r"$\gamma_{\mathrm{DV}}$ distribution"
    )

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

    output = (
        tmp_path /
        "example_04_vtp_combined_flow"
    )

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

    pdf = Path(
        str(output) + ".pdf"
    )

    pdf_tex = Path(
        str(output) + ".pdf_tex"
    )

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0

    # -----------------------------------------------------
    # Close
    # -----------------------------------------------------

    plt.close(
        figure.figure
    )
def test_vtp_contour_geometry_annotation_workflow(
    tmp_path,
):

    data = read_vtp(
        INPUT_FILE
    )

    figure_config = FigureConfig(
        width=3.4,
        height=3.0,
    )

    figure = PublicationFigure(
        figure_config
    )

    # -----------------------------------------------------
    # Contour
    # -----------------------------------------------------

    contour_plot = ContourPlot(
        data,
        field="gammaDV",
        association="cell",
    )

    contour = contour_plot.plot(
        figure.axes
    )

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

    output = (
        tmp_path /
        "example_05_contour_geometry"
    )

    figure.export(
        str(output),
        formats=[
            "pdf",
            "pdf_tex",
        ],
    )

    pdf = Path(
        str(output) + ".pdf"
    )

    pdf_tex = Path(
        str(output) + ".pdf_tex"
    )

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0

    plt.close(
        figure.figure
    )
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

    y = np.sin(
        2.0 * np.pi * x
    )

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

    figure = PublicationFigure(
        figure_config
    )

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

    lines = line_plot.plot(
        figure.axes
    )

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

    assert (
        figure.axes.get_xlabel()
        == r"$x\;(m)$"
    )

    assert (
        figure.axes.get_ylabel()
        == r"$f(x)$"
    )

    # -----------------------------------------------------
    # Title
    # -----------------------------------------------------

    figure.set_title(
        r"Basic 1D line plot"
    )

    assert (
        figure.axes.get_title()
        == r"Basic 1D line plot"
    )

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

    output = (
        tmp_path /
        "example_06_basic_line"
    )

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

    pdf = Path(
        str(output) + ".pdf"
    )

    pdf_tex = Path(
        str(output) + ".pdf_tex"
    )

    assert pdf.exists()
    assert pdf.stat().st_size > 0

    assert pdf_tex.exists()
    assert pdf_tex.stat().st_size > 0

    # -----------------------------------------------------
    # Close
    # -----------------------------------------------------

    plt.close(
        figure.figure
    )