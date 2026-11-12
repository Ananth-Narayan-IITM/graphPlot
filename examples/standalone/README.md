# Standalone examples (no figureSettings.py)

These examples do **not** import `figureSettings.py`. Each one creates its own
`Figure`, so you can copy a single file and change it.

Run them from the repository root with the project-aware runner:

```bash
graphPlot examples/standalone/vtpContour.py
graphPlot examples/standalone/linePlot.py
graphPlot examples/standalone/velocityVectors.py
graphPlot examples/standalone/tabularContour.py
graphPlot examples/standalone/streamlines.py
```

Or run all of them:

```bash
bash scripts/runStandaloneExamples.sh
```

`graphPlot` runs the script from the project root, so `data/...` and `output/...`
work regardless of the directory where you invoke the command.

## Why `gp.Project(...).contour()` fails

`gp.Project` is a **settings object**, not a figure. It stores width, height,
DPI, style, formats and output directory. Plot methods belong to `Figure` or
`Panel`.

Wrong:

```python
fig = gp.Project(width=3.4, dpi=600).contour(...)  # Project has no contour()
project.save(fig, "from")  # project is not defined
```

Two correct patterns:

### Standalone `Figure`

```python
import graphplot as gp

fig = gp.Figure(width=3.4, height=3.0)
fig.contour("data/zNormal.vtp", "gammaDV")
fig.save("output/figureName")
fig.close()
```

### Shared `Project` settings

```python
import graphplot as gp

project = gp.Project(width=3.4, height=3.0, formats=("pdf_tex", "png"))
fig = project.figure()
fig.contour("data/zNormal.vtp", "gammaDV")
project.save(fig, "figureName")
fig.close()
```

The examples directly in `examples/` use the shared
`examples/figureSettings.py`; these `standalone/` files are intentionally
self-contained.
