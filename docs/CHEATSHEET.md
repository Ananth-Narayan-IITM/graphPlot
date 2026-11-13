# graphPlot Cheat Sheet {#cheatsheet}

This page is the quick-reference version of the API guide. It is written for
the moment when you know the figure you want but not the exact call.

---

## Remember five things

```text
1. load      → get the data
2. figure    → create the canvas
3. add       → contour / line / vectors / streamlines / mesh
4. annotate  → labels / colorbar / legend
5. save      → project.save(...)
```

A complete figure usually looks like this:

```python
import graphplot as gp
from figureSettings import project

data = gp.load("data/zNormal.vtp")

fig = project.figure()
fig.contour(data, "gammaDV", levels=32)
fig.mesh(data, linewidth=0.1, alpha=0.3)
fig.colorbar(label=r"$\gamma_{\mathrm{DV}}$ [1/s]")
fig.xlabel("$x$", unit="m")
fig.ylabel("$y$", unit="m")

project.save(fig, "gamma")
fig.close()
```

---

## Data type → method

| Your data | Use |
|---|---|
| VTP/VTU scalar field | `contour(data, "field")` |
| VTP/VTU vector field `U` | `vectors(data, "U")` |
| VTP/VTU velocity field `U` | `streamlines(data, "U")` |
| VTP/VTU mesh | `mesh(data)` |
| CSV/DAT/XY table | `line("file.dat", x=..., y=...)` |
| NumPy arrays | `line(x, y)` |
| Error bars | `errorbar(x, y, yerr=...)` |
| Several panels | `fig[row, column]` |

Do not use `contour(data, "U")`: `U` is a vector. Use `vectors` or
`streamlines`, or select a scalar component:

```python
fig.contour(data, "U", component="x")
```

---

## Plot patterns

### Scalar contour

```python
fig.contour(
    data,
    "gammaDV",
    levels=32,
    cmap="viridis",
    vmin=None,
    vmax=None,
)
```

### Tabular / scattered contour

```python
table = gp.load("data/contour.dat")

fig.contour(
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
```

### Contour lines and labels

```python
fig.contour(
    data,
    "gammaDV",
    levels=8,
    show_lines=True,
    contour_labels=True,
    line_width=0.6,
    label_fontsize=7,
)
```

### Reference image

```python
fig.image("data/ref1.jpg", show_axes=False)
```

Side-by-side comparison with a reference figure:

```python
fig = project.figure(nrows=1, ncols=2)
fig[0, 0].contour(data, "gammaDV")
fig[0, 1].image("data/ref1.jpg")
fig[0, 0].title("(a) Present work", loc="left")
fig[0, 1].title("(b) Reference", loc="left")
```

### Velocity arrows

```python
fig.vectors(
    data,
    "U",
    density=18,
    scale="auto",
    length=0.12,
    min_magnitude=0.03,
    color="black",
)
```

- `density` controls how many arrows.
- `length` controls the reference arrow length.
- `min_magnitude` hides near-zero arrows.
- `normalize=True` gives equal-length arrows.

### Streamlines

```python
fig.streamlines(
    data,
    "U",
    seed_axis="y",
    seed_position=2.5,
    n_seeds=16,
    integration_direction="both",
    linewidth=0.7,
    arrowsize=0.9,
)
```

- `seed_axis="y"` distributes seeds along y at a fixed x.
- `seed_position` is that fixed x.
- `integration_direction="both"` integrates upstream and downstream.
- Set `arrowsize=0` to remove direction arrows.

### 1D comparison

```python
fig.line("data/numerical.dat", label="Numerical", role="numerical")
fig.line("data/experiment.dat", label="Experiment", role="experimental")
fig.legend(loc="best")
```

### Grouped legend

```python
fig.legend(
    groups=[
        {"title": "Numerical", "labels": ["Case 1", "Case 2"]},
        {"title": "Experiment", "labels": ["Exp. 1", "Exp. 2"]},
    ],
    ncol=2,
)
```

### LaTeX macros and citations

Document macros and `\cite` cannot be rendered by Matplotlib. Pass them through
with `gp.tex`:

```python
# LaTeX preamble:
# \newcommand{\Nu}{\mathbb{Nu}}
# \newcommand{\RaE}{\text{Ra}_E}

fig.ylabel(gp.tex(r"\Nu", math=True))
fig.line(..., label=gp.tex(r"\RaE = 0", plain="RaE = 0", math=True))
fig.legend(
    groups=[
        {"title": "Present work", "labels": [...]},
        {
            "title": gp.tex(r"Wu et al.\ \cite{Wu2015}", "Wu et al. [Wu2015]"),
            "labels": [...],
        },
    ]
)
```

`plain=` is the PNG fallback. Use `r"..."` so Python does not warn about
`\R` or `\N`.

### Dual axis

```python
left = fig.line(x, temperature, label="Case 1", color="black")
right = fig.twinx().line(x, pressure, label="Case 1", color="#D55E00")
right.ylabel("$p$", unit="Pa")
```

### Multi-panel

```python
fig = project.figure(nrows=2, ncols=2, sharex=True, sharey=True)
fig[0, 0].contour(data, "gammaDV")
fig[0, 1].contour(data, "gammaDV").mesh(data)
fig[1, 0].line("numerical.dat", label="Numerical")
fig[1, 1].line("experiment.dat", label="Experiment")
fig.label_panels()
```

---

## Build a figure step by step

1. Load the data and print it:

   ```python
   data = gp.load("data/zNormal.vtp")
   print(data)
   ```

2. Make the simplest plot:

   ```python
   fig = project.figure()
   fig.contour(data, "gammaDV")
   project.save(fig, "test", formats=("png",))
   ```

3. Add one thing at a time: mesh, colorbar, labels, vectors, streamlines.

4. Only when the PNG looks right, switch on `pdf_tex`:

   ```python
   project.save(fig, "gamma", formats=("pdf_tex", "png"))
   ```

5. Check the result in the LaTeX gallery:

   ```bash
   bash scripts/latexPreview.sh
   ```

---

## Copy the closest example

| I want | Start from |
|---|---|
| VTP contour | `examples/vtpContours.py` |
| contour + mesh | `examples/vtpContourMesh.py` |
| velocity arrows | `examples/velocityVectors.py` |
| streamlines | `examples/streamlines.py` |
| 1D comparison | `examples/linePlot.py` |
| grouped legend | `examples/groupedLegend.py` |
| dual axis + table legend | `examples/dualAxis.py` |
| parameter comparison grid | `examples/comparisonTable.py` |

Change the data path, field name and one style option. Run it. Then add the
next feature.

---

## Color schemes

```python
style = gp.Style.from_preset("paper", color_scheme="blackwhite")
fig = project.figure(style=style)
```

| Scheme | Use for |
|---|---|
| `colorblind` | screen and color-safe publication |
| `grayscale` | grayscale printing with several levels |
| `blackwhite` | strict black-and-white print |
| `default` | ordinary Matplotlib colors |
| custom | `colors=("...", "...")` |

`blackwhite` uses black lines plus different line styles and markers.
Contours automatically use `Greys` for `grayscale` and `blackwhite`, and
`viridis` otherwise.

## Common mistakes

| Symptom | Cause / fix |
|---|---|
| `Field 'U' has 3 components` | `U` is a vector. Use `vectors`, `streamlines`, or `component="x"`. |
| Arrows are invisible | Increase `length`, lower `min_magnitude`, or use `normalize=True`. |
| Too many arrows | Decrease `density`. |
| No streamlines | Check `seed_position`; it must lie inside the flow region. |
| Colorbar missing | `fig.colorbar()` must come after a contour. |
| `fig.save` not found | Use `project.save(fig, "name")` when using `Project`. |
| Wrong canvas size | Edit `width`/`height` in `figureSettings.py`. |
| Text size changes in PDF | `pdf_tex` inherits the LaTeX font size; wrap the include in a small-font group or set a local font size. |
| PDF_TeX file looks empty | Include the generated graphics PDF next to it; do not delete it. |
| `SyntaxWarning: invalid escape sequence '\R'` | Write the label as a raw string: `r"\RaE = 0"`. |
| `\RaE` or `\cite` missing from PDF | Use `gp.tex(...)`; matplotlib text cannot pass custom macros through. |
| `\mathbb` is used outside math mode | Add `math=True` to `gp.tex(...)`, or wrap the macro in `$...$`. |

---

## The one-line mental model

```text
VTP scalar   → contour
VTP vector   → vectors or streamlines
mesh         → overlay
table/arrays → line or errorbar
everything   → labels, legend, colorbar, save
```
