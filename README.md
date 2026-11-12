# graphPlot

Compact, publication-quality figures from OpenFOAM VTP files and tabular data.

`graphPlot` is a Python 3.10+ package built on Matplotlib and PyVista. It is
designed for papers: figures export as vector PDF plus a `.pdf_tex` file whose
text is typeset by LaTeX, so labels, ticks, legends and math match the document.

## Install

```bash
cd graphPlot
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

Normal installation:

```bash
pip install .
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
fig.save("output/01_vtp_contour", formats=["png", "pdf_tex"])
fig.close()
```

The export writes:

- `01_vtp_contour.png` — quick preview
- `01_vtp_contour.pdf` — text-free graphics layer
- `01_vtp_contour.pdf_tex` — LaTeX text overlay

Include it in a paper with:

```latex
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{xcolor}

\begin{figure}[htbp]
  \centering
  \def\svgwidth{\columnwidth}
  \input{output/01_vtp_contour.pdf_tex}
  \caption{...}
\end{figure}
```

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
- Figures are written as Python scripts; there is no YAML configuration layer.

## Contours first

The current development focus is:

1. VTP/VTU contours, mesh overlays, colorbars and PDF+TeX export.
2. 2D line plots, multi-axis layouts, grouped legends and table legends.
3. Vectors, streamlines, annotations and extra plot types.

## CLI

```bash
graphplot check
graphplot info data/zNormal.vtp
graphplot --version
```

`graphplot check` reports Python, NumPy, Matplotlib, PyVista, LaTeX and Doxygen
availability.

## Documentation

API documentation is generated with Doxygen:

```bash
doxygen Doxyfile
```

The generated site is written to `docs/html/index.html`.

## Tests

```bash
.venv/bin/python -m pytest
```

The PDF+TeX test compiles a small LaTeX document when `pdflatex` is available
and checks that the rendered figure contains actual graphics.

## Legacy v1

The complete previous implementation is preserved on the local `v1` branch
(tag `v1-final`). The `master` branch is the clean v2 rewrite.
