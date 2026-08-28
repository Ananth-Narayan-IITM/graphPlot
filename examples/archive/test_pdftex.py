from pathlib import Path

from postprocess.export.pdftex import (
    PDFTeXExporter,
)

SVG_FILE = Path("/tmp/graphplot_pdftex_test.svg")

OUTPUT_FILE = Path("output/test_pdftex.pdf")


exporter = PDFTeXExporter()

pdf_file, pdf_tex_file = exporter.export(
    SVG_FILE,
    OUTPUT_FILE,
)

print(
    "PDF:",
    pdf_file,
)

print(
    "PDF_TeX:",
    pdf_tex_file,
)
