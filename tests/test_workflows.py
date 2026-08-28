import matplotlib

matplotlib.use(
    "Agg"
)

from pathlib import Path

from postprocess.io.vtp import read_vtp

from postprocess.plots.contour import (
    ContourPlot,
)

from postprocess.layout.figure import (
    FigureConfig,
    PublicationFigure,
)

from postprocess.plots.mesh import (
    MeshPlot,
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