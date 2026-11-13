# graphPlot

Compact, publication-quality figures from OpenFOAM VTP files and tabular data.

`graphPlot` is a Python 3.10+ package built on Matplotlib and PyVista. It is
designed for papers: figures export as vector PDF plus a `.pdf_tex` file whose
text is typeset by LaTeX, so labels, ticks, legends and math match the document.

## Install

On a normal Python installation:

```bash
pip install .
```

On this machine the system Python is externally managed (PEP 668), so
`pip install .` is refused. Use the one-time local installer instead. It creates
a persistent environment at `~/.venvs/graphPlot`, installs the package and its
development tools there, and links the `graphPlot` command into `~/.local/bin`:

```bash
bash scripts/installLocal.sh
```

After that, **do not activate or create an environment**. The command works
directly:

```bash
graphPlot --version
graphPlot check
graphPlot examples/vtpContours.py
```

The installer is idempotent: running it again upgrades/repairs the persistent
environment.

### Verify the installation

Run the test suite and every example:

```bash
bash scripts/runTests.sh
bash scripts/runExamples.sh
```

Or run both in one step:

```bash
bash scripts/verifyAll.sh
```

### Optional development setup

Only needed if you want to modify the source in an editable checkout:

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python -m pytest
```

## Quick start: VTP contour

```python
import graphplot as gp

fig = (
    gp.Figure(width=3.4, height=3.0)
    .contour("data/zNormal.vtp", "gammaDV", levels=32)
    .xlabel("$x$", unit="m")
    .ylabel("$y$", unit="m")
)

fig.colorbar(label=r"$\gamma_{\mathrm{DV}}$ [1/s]")
fig.save("output/vtpContours", formats=["png", "pdf_tex"])
fig.close()
```

The export writes:

- `vtpContours.png` — quick preview
- `vtpContours.pdf` — text-free graphics layer
- `vtpContours.pdf_tex` — LaTeX text overlay

Include it in a paper with:

```latex
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{xcolor}

\begin{figure}[htbp]
  \centering
  \def\svgwidth{\columnwidth}
  \input{output/vtpContours.pdf_tex}
  \caption{...}
\end{figure}
```

## Tabular / scattered contours

```python
table = gp.load("data/contour.dat")

fig = (
    project.figure(width=4.2, height=3.4)
    .contour(
        table,
        x="Ra",
        y="Pr",
        field="nusseltNumber",
        xscale="log",
        yscale="log",
        levels=8,
        show_points=True,
        show_lines=True,
        contour_labels=True,
    )
    .xlabel("$Ra$")
    .ylabel("$Pr$")
)
fig.colorbar(label="$Nu$")
project.save(fig, "tabularContour")
```

`grid="auto"` uses a regular grid when possible and triangulates otherwise.
`max_triangle_edge` masks triangles that bridge large gaps.

## Quick start: line plots and grouped legends

```python
import graphplot as gp

fig = (
    gp.Figure(width=3.4, height=2.6)
    .line("data/numerical.dat", label="Numerical", role="numerical")
    .line("data/experiment.dat", label="Experiment", role="experimental")
    .xlabel("$x$", unit="m")
    .ylabel("$u$", unit="m/s")
    .legend(loc="best")
)
fig.save("output/line", formats=["png", "pdf_tex"])
```

Grouped legend:

```python
fig.legend(
    groups=[
        {"title": "Numerical", "labels": ["Case 1", "Case 2"]},
        {"title": "Experiment", "labels": ["Exp. 1", "Exp. 2"]},
    ],
    ncol=2,
)
```

Dual y-axis with a table legend:

```python
left = fig.line(x, temperature, label="Case 1", color="black")
right = fig.twinx().line(x, pressure, label="Case 1", color="#D55E00")

left.legend_table(
    {
        "Temperature": {"Case 1": left.last_artist},
        "Pressure": {"Case 1": right.last_artist},
    }
)
```

## Velocity arrows and streamlines

```python
data = gp.load("data/zNormal.vtp")

fig = (
    project.figure(height=3.0)
    .mesh(data, edgecolor="0.8", linewidth=0.06, alpha=0.35)
    .vectors(data, "U", density=18, length=0.12, min_magnitude=0.03)
    .xlabel("$x$", unit="m")
    .ylabel("$y$", unit="m")
)
project.save(fig, "velocityVectors")
```

```python
fig = (
    project.figure(height=3.0)
    .mesh(data, edgecolor="0.8", linewidth=0.06, alpha=0.35)
    .streamlines(
        data,
        "U",
        seed_axis="y",
        seed_position=2.5,
        n_seeds=16,
        integration_direction="both",
    )
    .xlabel("$x$", unit="m")
    .ylabel("$y$", unit="m")
)
project.save(fig, "streamlines")
```

- `vectors` uses automatic arrow scaling; tune `length`, `density` and
  `min_magnitude`.
- `streamlines` uses PyVista/VTK integration; place seeds inside the flow
  region with `seed_position`.
- Use `integration_direction="both"` for recirculating flows.

## Design

```python
import graphplot as gp

data = gp.load("case.vtp")     # FieldData
table = gp.load("data.dat")    # Table
series = table.series("x", "y")

fig = gp.Figure(width=3.4, height=2.6)
fig.contour(data, "gammaDV")
fig.colorbar(label=r"$\gamma_{\mathrm{DV}}$ [1/s]")
fig.save("figures/gamma")
```

- One `Figure`, one `Panel`, one `load()`.
- Single-panel figures forward plotting methods directly to the panel.
- Multi-panel figures use `fig[0, 0]`.
- Plot methods return the panel, so calls chain.
- Extra keyword arguments pass through to Matplotlib.
- Color schemes are selectable: `colorblind`, `grayscale`, `blackwhite`,
  `default`, or a custom `colors=(...)` palette.
- Figures are written as Python scripts; there is no YAML configuration layer.

## Contours first

The current development focus is:

1. VTP/VTU contours, mesh overlays, colorbars and PDF+TeX export.
2. 2D line plots, multi-axis layouts, grouped legends and table legends.
3. Vectors, streamlines, annotations and extra plot types.

## Paths in scripts

When you run a script with `graphPlot`, the command temporarily changes to the
project root — the nearest directory containing `pyproject.toml` or `.git` — and
restores your original directory afterwards. This means relative paths in a
figure script are always project-relative:

```python
fig.contour("data/zNormal.vtp", "gammaDV")
fig.save("output/vtpContours")
```

works whether you invoke:

```bash
graphPlot examples/vtpContours.py
```

from the repository root, from `examples/`, or from `/tmp` with an absolute
script path.

If no project root is found, the command keeps the invocation directory. When
running a script with plain `python script.py`, normal Python path rules apply.
Use `Path(__file__)` only when a path must be relative to the script file itself.

## One master file for canvas size and formats

Create a single `figureSettings.py` in your figure project:

```python
import graphplot as gp

project = gp.Project(
    width=3.4,
    height=2.8,
    dpi=600,
    style="paper",
    formats=("pdf_tex", "png"),
    output_dir="output",
)
```

Each figure script imports it:

```python
from figureSettings import project

fig = project.figure()
fig.line("data/numerical.dat", label="Numerical")
fig.xlabel("$x$", unit="m")
fig.ylabel("$u$", unit="m/s")
fig.legend()

project.save(fig, "linePlot")
fig.close()
```

Change the width, height, formats or DPI in `figureSettings.py` once and every
script follows. Individual figures can still override a field:

```python
fig = project.figure(height=3.0)          # taller figure
project.save(fig, "wide", formats=("png",))  # one-off format
```

Named variants are also possible:

```python
DOUBLE = project.with_(width=6.8)
SINGLE = project
```

The examples use this pattern in `examples/figureSettings.py`.

## Run all examples

One command runs the main examples and the standalone examples:

```bash
bash scripts/runExamples.sh
```

Outputs are written to:

```text
output/              # main examples using figureSettings.py
output/standalone/   # standalone examples without figureSettings.py
```

To remove previously generated figures first:

```bash
bash scripts/runExamples.sh --clean
```

The script uses the persistent `~/.venvs/graphPlot` installation and prints the
generated files when it finishes. To run only the standalone set:

```bash
bash scripts/runStandaloneExamples.sh
```

## Standalone examples

The scripts in `examples/standalone/` do not import `figureSettings.py`. They are
useful when you want to copy one file and change it directly.

```bash
bash scripts/runStandaloneExamples.sh
```

See [`examples/standalone/README.md`](examples/standalone/README.md) for the
`Project` versus `Figure` distinction and the standalone patterns.

## CLI

The `graphPlot` command runs a figure script directly. No environment
activation or YAML file is needed:

```bash
graphPlot examples/vtpContours.py
graphPlot examples/vtpContourMesh.py
graphPlot examples/linePlot.py
graphPlot examples/groupedLegend.py
graphPlot examples/dualAxis.py
graphPlot examples/comparisonTable.py
graphPlot examples/velocityVectors.py
graphPlot examples/streamlines.py
graphPlot examples/colorSchemes.py
graphPlot examples/tabularContour.py
graphPlot examples/referenceComparison.py
```

Diagnostics:

```bash
graphPlot check
graphPlot info data/zNormal.vtp
graphPlot --version
```

`graphPlot check` reports Python, NumPy, Matplotlib, PyVista, LaTeX and Doxygen
availability. Scripts use the non-interactive Agg backend by default, so they
can run from a terminal without a display.

## API documentation

The practical guide is [`docs/API_GUIDE.md`](docs/API_GUIDE.md). It explains
which object and method to use for each task, with a decision table, signatures,
recipes and common pitfalls. The one-page quick reference is
[`docs/CHEATSHEET.md`](docs/CHEATSHEET.md). The pre-submission checklist for
journals is [`docs/JOURNAL_CHECKLIST.md`](docs/JOURNAL_CHECKLIST.md).

Generated Doxygen documentation:

```bash
bash scripts/buildDocs.sh
```

The generated site is written to `docs/html/index.html`.

## LaTeX preview

Build a document containing every `output/*.pdf_tex` file, one figure per page,
with a title page and a font-size reference page:

```bash
bash scripts/latexPreview.sh
```

The result is:

```text
output/latexPreview.pdf
```

Use it to check that figure labels, ticks, legends and math match the paper
font. The preview includes reference paragraphs at 8, 9, 10 and 11 pt.

PDF_TeX files do not hard-code font sizes; their text inherits the surrounding
document size. Control the size where the figure is included:

```latex
{\small \input{output/vtpContours.pdf_tex}}
```

or, for a 24 pt test:

```latex
{\fontsize{24}{28.8}\selectfont
 \def\svgwidth{\columnwidth}
 \input{output/vtpContours.pdf_tex}}
```

If you want the PDF_TeX file to keep the Matplotlib point sizes instead, use
`fig.save(..., pdf_tex_text_size="figure")`.

## Tests

Use the persistent installation created by `scripts/installLocal.sh`:

```bash
bash scripts/runTests.sh
```

This runs the tests with `~/.venvs/graphPlot/bin/python -m pytest`; it does not
depend on an activated `.venv`. You can also run pytest directly:

```bash
~/.venvs/graphPlot/bin/python -m pytest
```

The PDF+TeX test compiles a small LaTeX document when `pdflatex` is available
and checks that the rendered figure contains actual graphics.

`bash scripts/verifyAll.sh` runs both the tests and all examples.

## Legacy v1

The complete previous implementation is preserved on the local `v1` branch
(tag `v1-final`). The `master` branch is the clean v2 rewrite.
