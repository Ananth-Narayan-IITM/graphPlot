"""Raw LaTeX labels from document macros and a citation.

Run from the repository root:

    graphPlot examples/standalone/texLabels.py

The PDF_TeX output expects the LaTeX document to define the macros used here:

    \\usepackage{amsmath,amssymb}
    \\newcommand{\\Nu}{\\mathbb{Nu}}
    \\newcommand{\\RaE}{\\text{Ra}_E}

and to contain a bibliography entry for ``Wu2015``.
"""

import numpy as np

import graphplot as gp

x = np.linspace(0.0, 1.0, 120)
present = gp.tex(r"\RaE = 0", plain="RaE = 0", math=True)
reference = gp.tex(r"\RaE = 200", plain="RaE = 200", math=True)

fig = gp.Figure(width=5.0, height=2.6)
fig.line(x, np.sin(2 * np.pi * x), label=present, role="numerical")
fig.line(
    x[::12],
    np.cos(2 * np.pi * x[::12]),
    label=reference,
    role="experimental",
    marker="o",
    markerfacecolor="white",
)
fig.xlabel("$x$")
fig.ylabel(gp.tex(r"\Nu", math=True))
fig.legend(
    groups=[
        {"title": "Present work", "labels": [present]},
        {
            "title": gp.tex(r"Wu et al.\ \cite{Wu2015}", "Wu et al. [Wu2015]"),
            "labels": [reference],
        },
    ],
    loc="upper left",
    bbox_to_anchor=(1.02, 1.0),
    borderaxespad=0.0,
    ncol=1,
    fontsize=fig.style.font_size,
)
fig.save("output/standalone/texLabels", formats=["png", "pdf_tex"])
fig.close()
