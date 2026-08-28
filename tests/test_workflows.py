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