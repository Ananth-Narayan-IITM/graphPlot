# graphPlot API Guide {#api_guide}

This is the practical guide to the public API. It answers two questions:

1. **Which object or method should I use for a given task?**
2. **What are the exact signatures and conventions?**

For generated class/method pages, run `bash scripts/buildDocs.sh` and open
`docs/html/index.html`.

---

## 1. The 30-second decision table

| I want to… | Use |
|---|---|
| Load a VTP/VTU/VTK file | `gp.load("case.vtp")` or pass the path directly to `contour`/`mesh` |
| Load a CSV, DAT, XY, TXT or OpenFOAM probe file | `gp.load("data.dat")` → `Table` |
| Plot a scalar field from VTP/VTU | `fig.contour(data, "field")` |
| Overlay the computational mesh | `fig.mesh(data)` |
| Plot one or more 1D curves | `fig.line(...)` |
| Add error bars | `fig.errorbar(...)` |
| Shade a band | `fig.fill_between(...)` |
| Add a colorbar | `fig.colorbar(...)` |
| Add a normal legend | `fig.legend()` |
| Add a grouped legend | `fig.legend(groups=[...])` |
| Add a table-style legend | `fig.legend_table({...})` |
| Use two y-axes | `right = fig.twinx()` |
| Use several panels | `fig[row, column]` |
| Set axis labels | `fig.xlabel(...)`, `fig.ylabel(...)` |
| Set limits, scales, ticks | `fig.xlim`, `fig.ylim`, `fig.xscale`, `fig.yscale`, `fig.ticks` |
| Add a panel label | `fig.label("(a)")` or `fig.label_panels()` |
| Save a publication figure | `fig.save("output/name", formats=["pdf_tex", "png"])` |
| Change fonts, colors or line widths | `gp.Style` / `gp.Figure(style="paper")` |
| Run a figure script | `graphPlot script.py` |

---

## 2. Which data object do I have?

```text
path ending in .vtp / .vtu / .vtk
    └── FieldData
          ├── contour()   scalar field → filled contour
          └── mesh()      mesh overlay

path ending in .csv / .dat / .xy / .txt / OpenFOAM probe
    └── Table
          └── table.series(x, y) → Data1D
                ├── line()
                └── errorbar()

NumPy arrays (x, y)
    └── line(x, y) or errorbar(x, y, yerr=...)
```

### `FieldData`

Use for VTP/VTU data.

```python
data = gp.load("case.vtp")

data.fields                     # {'gammaDV': 'cell', 'U': 'cell', ...}
data.bounds                     # (xmin, xmax, ymin, ymax, zmin, zmax)
data.bounds2d                   # (xmin, xmax, ymin, ymax)
data.n_points
data.n_cells
data.field("gammaDV")           # NumPy array
data.field("U", component="x")  # scalar component of a vector field
```

You rarely need to construct `FieldData` yourself; `gp.load` returns it.

### `Table`

Use for named-column text data.

```python
table = gp.load("contour.dat")

table.columns                   # ('Pr', 'Ra', 'nusseltNumber')
table.units                     # {'x': 'm', ...} when units are in the header
table["Ra"]                     # NumPy array
table.series("Ra", "nusseltNumber")
```

`Table` reads headers, units such as `x [m]`, OpenFOAM probe headers and vector
tuples such as `(ux uy uz)`.

### `Data1D`

Use when you already have `x` and `y` arrays or when you want to transform a
series.

```python
series = gp.Data1D(x, y, label="Numerical", yerr=sigma)
series.scale_x(1e-3)
series.finite()
series.sorted()
```

---

## 3. Single panel versus multiple panels

### Single panel

For a `1 × 1` figure, plotting methods are forwarded from the figure to its
only panel. This is the compact form:

```python
fig = gp.Figure(width=3.4, height=3.0)
fig.contour("case.vtp", "gammaDV")
fig.xlabel("$x$", unit="m")
fig.save("output/gamma")
```

### Multiple panels

Use `fig[row, column]` (or `fig.panel(row, column)`) and plot on each panel:

```python
fig = gp.Figure(width=7.0, height=5.0, nrows=2, ncols=2)

fig[0, 0].contour("case.vtp", "gammaDV")
fig[0, 1].contour("case.vtp", "gammaDV").mesh("case.vtp")
fig[1, 0].line("numerical.dat", label="Numerical")
fig[1, 1].line("experimental.dat", label="Experiment")

fig.label_panels()
fig.colorbar(axes=[fig[0, 0], fig[0, 1]], label=r"$\gamma$")
fig.save("output/combined")
```

---

## 4. Choosing the right plot method

### `contour` — scalar field from VTP/VTU

```python
fig.contour(
    data_or_path,
    "field",
    *,
    association="auto",     # "auto", "cell" or "point"
    component=None,         # "x", "y", "z" for vector fields
    levels=32,              # int or explicit list of levels
    cmap="viridis",
    vmin=None,
    vmax=None,
    norm=None,
    extend="neither",
    rasterize="auto",
    **matplotlib_kwargs,
)
```

Use when the data is a 2D scalar field on a mesh. With `association="auto"`,
cell data is preferred when a field exists in both cell and point data.

### `mesh` — computational mesh

```python
fig.mesh(
    data_or_path,
    *,
    edgecolor="black",
    facecolor="none",
    linewidth=0.15,
    alpha=0.3,
)
```

Use as an overlay after `contour`, or alone to inspect the mesh.

### `line` — 1D curves

```python
fig.line(
    data,                    # path, Table, Data1D or x array
    y=None,                  # y array, or column name/index for Table
    *,
    x=None,                  # x column name/index for Table
    label=None,
    role=None,               # "numerical", "experimental", "analytical", ...
    color=None,
    linestyle=None,
    marker=None,
    **matplotlib_kwargs,
)
```

Examples:

```python
fig.line("data/numerical.dat", label="Numerical")
fig.line("data/numerical.dat", x="t", y="U")
fig.line(table, x="t", y=["Ux", "Uy"])
fig.line(x_array, y_array, label="Case 1", marker="o")
```

When a path or `Table` has no `x`/`y` selection, column `0` and column `1` are
used.

### `errorbar`

```python
fig.errorbar(
    data,
    y=None,
    *,
    x=None,
    yerr=None,
    xerr=None,
    label=None,
    marker="o",
    linestyle="none",
    capsize=3.0,
    **matplotlib_kwargs,
)
```

If `yerr` is omitted, `Data1D.yerr` is used.

### `fill_between`

```python
fig.fill_between(x, y1, y2=0.0, label=None, **matplotlib_kwargs)
```

---

## 5. Legends: which style and when

### Standard legend

Use for a small number of simple series.

```python
fig.line(...).line(...)
fig.legend(loc="best", ncol=1)
```

### Grouped legend

Use when series belong to categories such as **Numerical** and **Experiment**.

```python
fig.legend(
    groups=[
        {"title": "Numerical", "labels": ["Case 1", "Case 2"]},
        {"title": "Experiment", "labels": ["Exp. 1", "Exp. 2"]},
    ],
    ncol=2,
    loc="upper right",
)
```

The labels must match the `label=` values used in `line`/`errorbar`.

### Table legend

Use when the same cases appear in multiple quantities, for example temperature
and pressure, or left and right axes.

```python
fig.legend_table(
    {
        "Temperature": {"Case 1": left_artist},
        "Pressure": {"Case 1": right_artist},
    },
    fontsize=8,
)
```

All groups must contain the same case names in the same order. The values must
be line artists. For a `twinx()` panel, use the artists returned by the
corresponding `last_artist`:

```python
left = fig.line(x, temperature, label="Case 1")
right = fig.twinx().line(x, pressure, label="Case 1")

left.legend_table(
    {
        "Temperature": {"Case 1": left.last_artist},
        "Pressure": {"Case 1": right.last_artist},
    }
)
```

`legend()` and `legend_table()` return the panel, so they can be chained. The
actual Matplotlib legend is available as `panel.last_legend`.

---

## 6. Colorbars

```python
colorbar = fig.colorbar(
    mappable=None,          # defaults to the last contour
    *,
    label=None,
    axes=None,              # one Panel, one Axes, or a list
    location="right",       # "right", "left", "top", "bottom"
    **matplotlib_kwargs,
)
```

- With one contour, `fig.colorbar(label=...)` is enough.
- With several contours, pass the desired mappable explicitly.
- For a shared colorbar, pass multiple panels:

```python
fig.colorbar(
    contour,
    axes=[fig[0, 0], fig[0, 1]],
    label=r"$\gamma_{\mathrm{DV}}$ [1/s]",
    location="right",
)
```

`colorbar` returns a Matplotlib `Colorbar`, so you can call `set_ticks` on it.

---

## 7. Axis controls

```python
fig.xlabel("$x$", unit="m")
fig.ylabel("$u$", unit="m/s")
fig.title("Comparison")
fig.xlim(0, 1)
fig.ylim(-1, 1)
fig.xscale("log")
fig.yscale("log")
fig.ticks(x=[0, 0.5, 1], y=[-1, 0, 1])
fig.grid(True, linestyle=":")
fig.tick_params(labelsize=8, direction="in")
fig.aspect("equal")
fig.axis_off()
```

For a multi-panel figure, call these on a panel:

```python
fig[0, 0].xlabel("$x$", unit="m")
fig[0, 0].xlim(0, 1)
```

Figure-level labels:

```python
fig.common_labels(x="$x$ [m]", y="$y$ [m]")
fig.label_panels()
fig.suptitle("Overall title")
```

---

## 8. Styling

```python
style = gp.Style.from_preset(
    "paper",             # paper, ieee, elsevier, thesis, screen
    font_size=10,
    line_width=1.2,
    dpi=600,
)

fig = gp.Figure(width=3.4, height=2.6, style=style)
```

The `paper` preset uses 10 pt for axis labels and titles, and 9 pt for ticks
and legends. Changing `font_size` updates those related sizes automatically
unless `label_size`, `title_size`, `tick_size` or `legend_size` is set
explicitly.

Use the same size as your manuscript if you want the figure text to match the
body text exactly:

```python
style = gp.Style.from_preset("paper", font_size=11)
fig = gp.Figure(width=3.4, height=2.6, style=style)
```

Per-call Matplotlib keywords always override the style:

```python
fig.line("data.dat", color="black", linewidth=1.0, linestyle="--")
```

Roles provide quick defaults:

| Role | Default line | Default marker |
|---|---|---|
| `numerical` | solid | none |
| `analytical` | dashed | none |
| `experimental` | none | marker cycle |
| `reference` | dash-dot | marker cycle |

A style is immutable; use `style.with_(font_size=10)` to create a modified copy.

---

## 9. Export

```python
paths = fig.save(
    "output/figureName",
    formats=["pdf_tex", "png"],
    dpi=600,
    transparent=False,
)
```

| Format | Output |
|---|---|
| `pdf_tex` | `figureName.pdf` (text-free graphics) + `figureName.pdf_tex` |
| `pdf` | `figureName.pdf` with embedded text |
| `png` | `figureName.png` |
| `svg` | `figureName.svg` |
| `eps` | `figureName.eps` |

When both `pdf` and `pdf_tex` are requested, the PDF_TeX graphics layer is
written as `figureName_tex.pdf` so the standalone PDF is not overwritten.

### Font size in PDF_TeX

By default, `pdf_tex` **does not contain a font size command**. Every label,
tick, legend and math expression inherits the font size in effect where the
file is included. This is the intended PDF_TeX behaviour:

```latex
\input{output/figureName.pdf_tex}                    % 10 pt document → 10 pt text
{\small \input{output/figureName.pdf_tex}}           % locally smaller
{\fontsize{24}{28}\selectfont
 \input{output/figureName.pdf_tex}}                  % locally 24 pt
```

If you instead want the PDF_TeX file to preserve the Matplotlib point sizes,
use:

```python
fig.save(
    "output/figureName",
    formats=["pdf_tex"],
    pdf_tex_text_size="figure",
)
```

`pdf_tex_text_size="inherit"` is the default.

LaTeX inclusion:

```latex
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{xcolor}

\begin{figure}[htbp]
  \centering
  \def\svgwidth{\columnwidth}
  \input{output/figureName.pdf_tex}
  \caption{...}
\end{figure}
```

`fig.save` returns a dictionary of generated paths. `fig.close()` releases the
Matplotlib figure; a `with gp.Figure(...) as fig:` block closes it automatically.

---

## 10. Common recipes

### VTP contour with colorbar

```python
import graphplot as gp

fig = (
    gp.Figure(width=3.4, height=3.0)
    .contour("data/zNormal.vtp", "gammaDV", levels=32)
    .xlabel("$x$", unit="m")
    .ylabel("$y$", unit="m")
)
fig.colorbar(label=r"$\gamma_{\mathrm{DV}}$ [1/s]")
fig.save("output/gamma", formats=["png", "pdf_tex"])
```

### VTP contour with mesh

```python
fig = (
    gp.Figure(width=3.4, height=3.0)
    .contour("data/zNormal.vtp", "gammaDV")
    .mesh("data/zNormal.vtp", linewidth=0.12, alpha=0.3)
    .xlabel("$x$", unit="m")
    .ylabel("$y$", unit="m")
)
```

### Numerical/experimental comparison with grouped legend

```python
fig = (
    gp.Figure(width=3.8, height=2.8)
    .line(x, numerical_1, label="Case 1", role="numerical")
    .line(x, numerical_2, label="Case 2", role="numerical")
    .line(xe, experiment_1, label="Exp. 1", role="experimental")
    .line(xe, experiment_2, label="Exp. 2", role="experimental")
    .xlabel("$x$", unit="m")
    .ylabel("$u$", unit="m/s")
)
fig.legend(
    groups=[
        {"title": "Numerical", "labels": ["Case 1", "Case 2"]},
        {"title": "Experiment", "labels": ["Exp. 1", "Exp. 2"]},
    ],
    ncol=2,
)
```

### Error bars

```python
fig.errorbar(x, y, yerr=sigma, label="Experiment", capsize=3)
```

### Dual axes with table legend

```python
left = fig.line(x, temperature, label="Case 1", color="black")
right = fig.twinx().line(x, pressure, label="Case 1", color="#D55E00")

left.xlabel("$x$", unit="m")
left.ylabel("$T$", unit="K")
right.ylabel("$p$", unit="Pa")

left.legend_table(
    {
        "Temperature": {"Case 1": left.last_artist},
        "Pressure": {"Case 1": right.last_artist},
    }
)
```

### Multi-panel

```python
fig = gp.Figure(width=7.0, height=5.0, nrows=2, ncols=2)
fig[0, 0].contour("case.vtp", "gammaDV")
fig[0, 1].contour("case.vtp", "gammaDV").mesh("case.vtp")
fig[1, 0].line("numerical.dat", label="Numerical")
fig[1, 1].line("experimental.dat", label="Experiment")
fig.label_panels()
fig.save("output/combined")
```

---

## 11. Running scripts

```bash
graphPlot examples/vtpContours.py
graphPlot examples/linePlot.py
```

`graphPlot` runs the script from the project root — the nearest directory
containing `pyproject.toml` or `.git` — so relative paths such as
`data/zNormal.vtp` and `output/figureName` work regardless of the shell
directory.

Diagnostics:

```bash
graphPlot check
graphPlot info data/zNormal.vtp
```

---

## 12. Conventions and gotchas

- **Plot methods return the panel.** Use `panel.last_artist` for the Matplotlib
  artist, `panel.last_mappable` for the most recent contour, and
  `panel.last_legend` for the most recent legend.
- **`fig.colorbar()` uses the last contour** when `mappable` is omitted.
- **`legend()` returns the panel**, not the legend object.
- **Single-panel figures implement forwarding.** `fig.contour(...)` is shorthand
  for `fig[0, 0].contour(...)`; this forwarding is disabled for multi-panel
  figures.
- **Association matters.** `association="auto"` prefers cell data when a field
  exists in both cell and point data. Use `association="point"` explicitly for
  point-centred fields.
- **Vector fields need a component.** `U` is a vector; use
  `component="x"` to plot a scalar component.
- **No YAML.** Figures are Python scripts.
- **2D is the current focus.** VTP/VTU contours and mesh overlays are supported;
  tabular contours, vectors, streamlines and annotations are on the roadmap.
- **PDF_TeX text is LaTeX text.** Use `$...$` for math. Plain text is escaped
  automatically.

---

## 13. Roadmap

Already implemented:

- VTP/VTU cell and point contours
- mesh overlays
- 1D line and error-bar plots
- grouped and table legends
- dual y-axes
- colorbars
- multipanel figures
- native PDF+TeX export

Planned:

- tabular/scattered contour plots
- vector fields and streamlines
- annotations and dimensions
- shared colorbar helpers for complex layouts

For generated class and method pages, run:

```bash
bash scripts/buildDocs.sh
```
