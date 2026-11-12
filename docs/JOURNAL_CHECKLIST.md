# Journal Submission Checklist {#journal_checklist}

This page collects the practical checks needed before a figure set goes into a
journal submission, plus the technical documentation reviewers increasingly
expect.

---

## 1. Figure quality

- [ ] Figure width matches the journal column width (single, 1.5 or double).
- [ ] Fonts are 8–10 pt at final printed size, or explicitly matched to the
      manuscript.
- [ ] Vector formats are supplied (`pdf_tex`, `pdf`, `svg` or `eps`).
- [ ] PNG previews are only for checking; they are not the submission format.
- [ ] Axis labels include units, e.g. `$x$ [m]`, `$u$ [m/s]`.
- [ ] Tick labels are readable at final size.
- [ ] Line widths, marker sizes and arrowheads survive reduction.
- [ ] Panels are labelled consistently: `(a)`, `(b)`, ...
- [ ] Legends are inside or clearly attached to the figure.
- [ ] Colorbars have labels and meaningful tick values.
- [ ] No text overlaps, clipped labels or accidental whitespace.

---

## 2. Color and accessibility

- [ ] A colorblind-safe scheme is used for color figures.
- [ ] A black-and-white or grayscale version has been checked.
- [ ] Line styles and markers provide redundancy beyond color.
- [ ] No information is encoded by red/green alone.
- [ ] Contrast is sufficient for thin lines and small markers.
- [ ] Contour maps remain readable after grayscale conversion.
- [ ] The final figure has been viewed in grayscale print preview.

`graphPlot` color schemes:

```python
colorblind = gp.Style.from_preset("paper", color_scheme="colorblind")
grayscale = gp.Style.from_preset("paper", color_scheme="grayscale")
blackwhite = gp.Style.from_preset("paper", color_scheme="blackwhite")
```

`blackwhite` uses black lines with different line styles and markers.
`grayscale` uses gray levels plus line styles. Contours automatically use
`Greys` for both.

---

## 3. PDF_TeX checklist

- [ ] The `.pdf_tex` file and its graphics `.pdf` are kept together.
- [ ] The figure is included with `\input{...pdf_tex}`.
- [ ] The width is set with `\def\svgwidth{...}`.
- [ ] The LaTeX document compiles without missing-file errors.
- [ ] Figure text uses the document font and math font.
- [ ] Local text size is controlled where the file is included, not inside the
      `.pdf_tex`.
- [ ] `output/latexPreview.pdf` has been inspected page by page.
- [ ] The PDF was checked at 100 % and at final print size.

Recommended include:

```latex
\begin{figure}[htbp]
  \centering
  \def\svgwidth{\columnwidth}
  \input{figures/figureName.pdf_tex}
  \caption{...}
  \label{fig:figureName}
\end{figure}
```

---

## 4. Technical documentation package

Keep these items together with the manuscript:

- [ ] Figure scripts (`*.py`).
- [ ] Master settings file (`figureSettings.py`).
- [ ] Input data or data-availability statement.
- [ ] `graphPlot` version (`graphPlot --version`).
- [ ] Python version and package versions (`graphPlot check`).
- [ ] Exact command used to generate each figure.
- [ ] Generated figure files and their directory structure.
- [ ] A short README for the figure set.
- [ ] Commit hash or archive DOI of the analysis code.
- [ ] License for the code and data.
- [ ] Any permissions for third-party data or reproduced figures.

A reproducible figure should be reconstructible with:

```bash
graphPlot figures/vtpContours.py
bash scripts/latexPreview.sh
```

Avoid manual post-processing of exported figures. If a figure is edited after
export, record the edit in the documentation.

---

## 5. Figure manifest

For a submission package, record at least:

| Item | Example |
|---|---|
| Figure name | `vtpContours` |
| Script | `figures/vtpContours.py` |
| Data | `data/zNormal.vtp` |
| Field | `gammaDV` |
| Command | `graphPlot figures/vtpContours.py` |
| Outputs | `output/vtpContours.pdf`, `.pdf_tex`, `.png` |
| graphPlot version | 2.0.0 |
| Commit | `921fdc3` |
| Notes | colorblind palette; shared vmin/vmax |

A future `Project.manifest()` helper is planned for generating this
automatically as JSON.

---

## 6. Caption and metadata

- [ ] Caption states what each panel shows.
- [ ] Caption defines every symbol, line style and color.
- [ ] Caption states the parameter values (`T = 0, 10, 20, 30`).
- [ ] Caption states normalization or non-dimensionalization.
- [ ] Caption states whether data are experimental, numerical or analytical.
- [ ] Panel labels match the caption order.
- [ ] Figure and table numbering is final.
- [ ] Cross-references in the text use the final labels.

---

## 7. Pre-submission commands

```bash
graphPlot check                 # environment and tool versions
bash scripts/runTests.sh        # package tests
bash scripts/runExamples.sh     # regenerate all examples
bash scripts/latexPreview.sh    # compile the figure gallery
bash scripts/buildDocs.sh       # API documentation
```

Check the generated gallery:

```text
output/latexPreview.pdf
```

Then inspect each figure at the final journal width.

---

## 8. Common journal pitfalls

| Problem | Prevention |
|---|---|
| Text too small after reduction | Design at final width; check the printed-size preview. |
| Colors indistinguishable in grayscale | Use `blackwhite` and line styles. |
| Missing units | Use `xlabel("$x$", unit="m")`. |
| Legend unreadable | Keep it inside the axes or use a grouped/table legend. |
| Raster contour in vector PDF | Use vector polygons or an intentional rasterization threshold. |
| Missing `.pdf` next to `.pdf_tex` | Copy both files together. |
| Font mismatch | Let PDF_TeX inherit the document font; avoid fixed sizes. |
| Irreproducible manual edit | Regenerate from the script and commit the settings. |
