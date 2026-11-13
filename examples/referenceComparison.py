"""Reference comparison: comment, present work and reference image.

Run from anywhere:

    graphPlot examples/referenceComparison.py
"""

import textwrap

from figureSettings import project

import graphplot as gp

DATA = gp.load("data/zNormal.vtp")
values = DATA.field("gammaDV")
vmin = float(values.min())
vmax = float(values.max())

references = ("data/ref1.jpg", "data/ref2.jpg")
comments = (
    (
        "$T = 0$",
        "Reference case. The present-work panel is a placeholder "
        "using zNormal.vtp; replace it with the actual case later.",
    ),
    (
        "$T = 10$",
        "Second parameter case. The two present-work panels use the "
        "same zNormal.vtp field for now.",
    ),
)

fig = project.figure(
    width=7.2,
    height=4.8,
    nrows=2,
    ncols=3,
    gridspec_kw={"width_ratios": [1.35, 1.0, 1.0]},
)

for row, ((label, comment), reference) in enumerate(
    zip(comments, references, strict=True)
):
    comment_panel = fig[row, 0]
    comment_panel.axis_off()
    comment_panel.ax.text(
        0.0,
        0.5,
        f"{label}\n\n{textwrap.fill(comment, width=32)}",
        transform=comment_panel.ax.transAxes,
        ha="left",
        va="center",
        fontsize=fig.style.label_size,
    )

    fig[row, 1].contour(
        DATA,
        "gammaDV",
        levels=24,
        cmap="viridis",
        vmin=vmin,
        vmax=vmax,
    )
    fig[row, 2].image(reference)

fig[0, 0].title("Comment", loc="left")
fig[0, 1].title("(a) Present work", loc="left")
fig[0, 2].title("(b) Reference 1", loc="left")
fig[1, 1].title("(c) Present work", loc="left")
fig[1, 2].title("(d) Reference 2", loc="left")

fig[0, 1].ylabel("$y$", unit="m")
fig[1, 1].ylabel("$y$", unit="m")
fig[1, 1].xlabel("$x$", unit="m")

project.save(fig, "referenceComparison")
fig.close()
