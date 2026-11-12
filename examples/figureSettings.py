"""Master settings shared by the example figure scripts.

Change the canvas size, formats, DPI or output directory here once and every
example picks up the new values. Individual scripts may still override a field
with ``project.figure(...)`` or ``project.save(...)``.
"""

import graphplot as gp

project = gp.Project(
    width=3.4,
    height=2.8,
    dpi=600,
    style="paper",
    formats=("pdf_tex", "png"),
    output_dir="output",
)

# Larger canvas for tabular/parameter-comparison grids.
comparison = project.with_(width=6.8, height=10.5)
