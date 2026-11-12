# graphPlot v2 — Design and Implementation Plan

## Status

- The complete v1 implementation is preserved on the local `v1` branch
  (tag `v1-final`, commit `2e60876`).
- `master` has been rebooted with the v2 package.
- First milestone complete: VTP contour, mesh overlay, colorbar,
  native PDF+TeX export, tabular reader, CLI diagnostics, tests and examples.

## Decisions

| Decision | Choice |
|---|---|
| Language | Python 3.10+ |
| Distribution name | `graphPlot` |
| Import name | `graphplot` |
| CLI | `graphplot` |
| PDF+TeX backend | Native Matplotlib PDF+TeX writer (no Inkscape required) |
| Backward compatibility | New API only; examples and scripts are rewritten |
| Tooling | Python API + diagnostics CLI; figures are written as Python scripts, not YAML |

---

## 1. Goals

- Compact, readable user code for publication figures.
- One `Figure`, one `Panel`, one `load()`.
- Line plots, VTP contours, tabular contours, mesh, vectors, streamlines,
  annotations, and arbitrary combinations.
- Robust readers for `.csv`, `.xy`, `.dat`, `.txt`, OpenFOAM probes,
  VTP/VTU, and raw NumPy arrays.
- High-quality PDF + PDF_TeX output that uses the document font and math font.
- `pip install .` with a working `graphplot` command.
- Tests, examples, and documentation that stay in sync.

---

## 2. Public API

### Line plot

```python
import graphplot as gp

fig = (
    gp.Figure(width=3.4, height=2.6)
      .line("data/numerical.dat", label="Numerical")
      .line("data/experiment.dat", label="Experiment", marker="o", ls="none")
      .xlabel("$x$", unit="m")
      .ylabel("$u$", unit="m/s")
      .legend(loc="best")
      .save("figures/u_profile")
)
```

### VTP contour

```python
fig = (
    gp.Figure(width=3.4, height=3.0)
      .contour("data/zNormal.vtp", "gammaDV", levels=32, cmap="viridis")
      .xlabel("$x$", unit="m")
      .ylabel("$y$", unit="m")
)
fig.colorbar(label=r"$\gamma_{\mathrm{DV}}$ [1/s]")
fig.save("figures/gamma")
```

### Multipanel combination

```python
fig = gp.Figure(width=6.8, height=6.0, nrows=2, ncols=2)

fig[0, 0].contour("case.vtp", "gammaDV").mesh(alpha=0.3).label("(a)")
fig[0, 1].contour("case.vtp", "gammaDV").vectors("U", density=18).label("(b)")
fig[1, 0].line("numerical.dat", label="Numerical").line("experiment.dat", label="Experiment")
fig[1, 1].line("numerical.dat", label="Numerical").line("analytical.dat", label="Analytical")

fig.common_labels(x="$x$ [m]", y="$y$ [m]")
fig.colorbar(label=r"$\gamma_{\mathrm{DV}}$ [1/s]", axes=[fig[0, 0], fig[0, 1]])
fig.save("figures/combined")
```

### Design rules

- Plot methods return the panel for chaining.
- The underlying Matplotlib artist is available as `panel.last_artist` / `panel.artists`.
- Extra keyword arguments pass through to Matplotlib.
- Defaults come from `Style`; per-call arguments always override.
- `fig.colorbar()` uses the last contour mappable when `mappable` is omitted.

---

## 3. Package layout

```text
src/graphplot/
├── __init__.py          # Figure, Panel, load, Style, check
├── figure.py            # grid, shared labels, colorbars, save
├── panel.py             # axes-level plotting API
├── style.py             # Style dataclass, presets, rcParams context
├── data/
│   ├── series.py        # Data1D
│   ├── table.py         # Table with named columns and units
│   └── field.py         # FieldData: VTP/VTU mesh + fields
├── io/
│   ├── load.py          # unified load() dispatcher
│   ├── tabular.py       # csv/dat/xy/txt/OpenFOAM readers
│   └── vtk.py           # VTP/VTU reader via PyVista
├── plots/
│   ├── line.py
│   ├── contour.py
│   ├── mesh.py
│   ├── vector.py
│   ├── streamline.py
│   └── annotation.py
├── export/
│   ├── pdftex.py        # native PDF+TeX writer
│   ├── latex.py         # escaping, Unicode mapping, snippets
│   └── inkscape.py      # optional fallback backend
├── cli.py               # check/info only
└── _checks.py           # dependency and tool diagnostics
```

---

## 4. Data layer

### Unified loader

```python
data = gp.load("file.xy")          # Table
data = gp.load("case.vtp")         # FieldData
data = gp.load("postProcessing/probes/0/U")  # Table
```

Supported formats:

- whitespace tables: `.dat`, `.txt`, `.xy`, no suffix
- `.csv`, `.tsv` with delimiter and header detection
- OpenFOAM probes, including vector columns `(ux uy uz)`
- OpenFOAM sample lines
- `.npy`, `.npz`
- `.vtp`, `.vtu`, `.vtk`
- raw NumPy arrays passed directly to plotting methods

Table reader requirements:

- auto-detect comma, semicolon, tab, whitespace
- auto-detect headers such as `# Time 0 1 2` and `x [m] y [m]`
- extract units from headers
- handle comments, blank lines, `NaN`, `--`, and empty cells
- expand OpenFOAM vector tuples into `Ux`, `Uy`, `Uz`
- no mandatory pandas dependency
- useful errors listing available columns

`FieldData` requirements:

- point and cell association detection
- vector-component extraction, e.g. `U` -> `Ux`
- `fields`, `bounds`, `n_cells`, `n_points`
- optional 3D slicing

---

## 5. Plot layer

### Line plots

- lines, markers, error bars, fill-between
- automatic styles and optional roles
- standard, grouped, and table legends

### Contours

One unified API for VTP and tabular data:

```python
fig.contour("case.vtp", "gammaDV", levels=32)
fig.contour("contour.dat", x="Ra", y="Pr", field="Nu", xscale="log", yscale="log")
fig.contour(table, x="x", y="y", field="T", grid="auto")
```

Features:

- cell-centred polygons and point-centred triangulation
- int or explicit levels
- `vmin`, `vmax`, `norm`, `extend`, `under`, `over`, `bad`
- optional isolines, labels, and sample points
- sparse-data triangle masking
- correct logarithmic axes for tabular data
- automatic rasterization for large meshes

### Mesh, vectors, streamlines

```python
fig.mesh("case.vtp", alpha=0.35)
fig.vectors("case.vtp", "U", density=18)
fig.streamlines("case.vtp", "U", n_seeds=20)
```

### Annotations

- text, arrows, dimensions, rectangles, panel labels
- data and axes coordinate systems
- LaTeX text support

---

## 6. Style and layout

```python
style = gp.Style(
    preset="paper",
    font_size=9,
    line_width=1.2,
    colors=["#0072B2", "#E69F00", "#009E73"],
    markers=["o", "s", "^"],
    dpi=600,
)
```

Presets: `paper`, `ieee`, `elsevier`, `thesis`, `screen`.

Layout:

- constrained layout by default
- `fig[0, 0]`, `fig.panel(0, 0)`, `fig.axes`
- shared x/y axes
- `fig.label_panels()`, `fig.common_labels()`
- `fig.twinx()`
- `fig.colorbar(mappable=None, label=..., axes=..., location=...)`

---

## 7. Export: native PDF+TeX writer

### Why the old pipeline is replaced

The old `SVG -> Inkscape --export-latex` pipeline produces a multi-page PDF
for Matplotlib SVGs. When the generated `.pdf_tex` is compiled, later pages
contain white axes backgrounds that cover the contour. This was verified by
compiling the existing `example_01_vtp_contour.pdf_tex`: the contour fill is
missing.

### New pipeline

1. Draw the figure and collect every `Text` artist with its position and
   bounding box.
2. Hide all text.
3. Save a single-page, text-free vector PDF containing only graphics.
4. Write `.pdf_tex` with `\put(...)` commands that recreate every label in
   LaTeX at the exact position.

Output shape:

```latex
\begingroup
\setlength{\unitlength}{230.4bp}   % or \svgwidth when defined
\begin{picture}(1,0.75)
\put(0,0){\includegraphics[width=\unitlength]{\detokenize{fig.pdf}}}
\put(0.615,0.129){\makebox(0,0)[ct]{\fontsize{10}{12}\selectfont $x\;(\mathrm{m})$}}
...
\end{picture}
\endgroup
```

Requirements:

- single-page PDF
- correct placement for axis labels, titles, ticks, legends, colorbars,
  panel labels, annotations, and figure text
- LaTeX escaping for plain text
- pass-through for `$...$` math
- bold/italic, rotation, multi-line text, colored text
- Unicode-to-LaTeX mapping
- support `\def\svgwidth{\columnwidth}`
- no Inkscape dependency

`pdf` format remains a normal Matplotlib PDF with embedded text. When both
`pdf` and `pdf_tex` are requested, the `.pdf_tex` references a separate
graphics-only PDF so the two outputs do not overwrite each other.

---

## 8. CLI and scripts

Figures are written as compact Python scripts. YAML is deliberately not used:
it would add a second configuration language, hide Matplotlib control, and
make debugging harder. The CLI is limited to diagnostics.

```bash
graphplot check          # Python, PyVista, LaTeX and Doxygen availability
graphplot info case.vtp  # fields, associations, bounds
graphplot --version
```

A typical figure is a short, readable Python file:

```python
import graphplot as gp

fig = (
    gp.Figure(width=3.4, height=3.0)
      .contour("case.vtp", "gammaDV")
      .xlabel("$x$", unit="m")
      .ylabel("$y$", unit="m")
)
fig.colorbar(label=r"$\gamma_{\mathrm{DV}}$ [1/s]")
fig.save("figures/gamma")
```

---

## 9. Packaging

```toml
[project]
name = "graphPlot"
requires-python = ">=3.10"
dependencies = [
    "numpy>=1.23",
    "matplotlib>=3.7",
    "pyvista>=0.43",
    "scipy>=1.9",
]

[project.scripts]
graphplot = "graphplot.cli:main"
```

Install:

```bash
pip install .
pip install -e ".[dev]"
```

`graphplot check` reports Python, package, PyVista/VTK, LaTeX, and Inkscape
availability.

---

## 10. Implementation phases

0. Freeze `v1.1`, create `v2` branch, remove generated artifacts.
1. Scaffold package, `pyproject.toml`, CLI, `Style`.
2. Implement readers and data containers with tests.
3. Implement `Figure`/`Panel`, line plots, PNG/PDF/SVG export.
4. Implement and validate the native PDF+TeX writer.
5. Implement VTP contours, mesh, colorbars, multipanel.
6. Merge tabular contours into the unified contour API.
7. Port vectors, streamlines, annotations, dimensions.
8. Rewrite examples, README, Doxygen documentation, migration guide.
9. QA: fresh install, examples, LaTeX compilation, lint, tests, release.

Phase 4 is deliberately early because it is the highest-risk component.

---

## 11. Acceptance criteria

- `pip install .` succeeds in a clean environment.
- `graphplot check` reports a healthy setup.
- A 10-line script produces a publication-ready line plot or VTP contour.
- A 25-line script produces a mixed multipanel figure.
- `pdf_tex` output compiles in LaTeX with visible graphics and document text.
- All readers handle `.csv`, `.dat`, `.xy`, whitespace, headers, units, and
  OpenFOAM probes.
- Tests pass without a display.
- No build artifacts are committed.

---

## 12. Scope

Primary:

- 2D line plots
- VTP/VTU surface and cell contours
- mesh, vectors, streamlines
- multipanel layouts
- annotations and dimensions

Secondary:

- 3D VTP slices
- regular-grid contours
- Doxygen API documentation

Out of scope for v2:

- interactive 3D rendering
- animations
- volume rendering
- GUI
