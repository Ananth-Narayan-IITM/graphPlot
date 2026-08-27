from pathlib import Path

from postprocess.export.latex import (
    LaTeXTextRegistry,
)

from postprocess.export.pdftex import (
    PDFTeXExporter,
)


SVG_FILE = Path(
    "/tmp/graphplot_placeholder.svg"
)

OUTPUT_FILE = Path(
    "output/placeholder.pdf"
)


# =========================================================
# Register LaTeX
# =========================================================

registry = LaTeXTextRegistry()

placeholder = registry.register(
    r"$\gamma_{\mathrm{DV}}$ (1/s)"
)


print(
    "Placeholder:",
    placeholder,
)


# =========================================================
# Create SVG
# =========================================================

svg = """\
<svg xmlns="http://www.w3.org/2000/svg"
     width="100mm"
     height="60mm"
     viewBox="0 0 100 60">

    <rect
        x="10"
        y="10"
        width="80"
        height="40"
        fill="none"
        stroke="black"
        stroke-width="0.5"
    />

    <text
        x="50"
        y="30"
        text-anchor="middle"
        font-size="5">
        {placeholder}
    </text>

</svg>
""".format(
    placeholder=placeholder
)


with open(
    SVG_FILE,
    "w",
    encoding="utf-8",
) as file:

    file.write(svg)


# =========================================================
# Inkscape export
# =========================================================

exporter = PDFTeXExporter()

pdf_file, pdf_tex_file = exporter.export(
    SVG_FILE,
    OUTPUT_FILE,
)


# =========================================================
# Replace placeholder
# =========================================================

registry.replace_in_file(
    pdf_tex_file
)


print(
    "PDF:",
    pdf_file,
)

print(
    "PDF_TeX:",
    pdf_tex_file,
)