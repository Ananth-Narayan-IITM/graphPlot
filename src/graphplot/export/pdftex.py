"""Native Matplotlib to PDF + PDF_TeX export.

The writer saves a single-page, text-free PDF and writes a ``.pdf_tex`` file
that recreates every text label with LaTeX. This avoids the multi-page PDF
problem produced by the Inkscape PDF+LaTeX extension for Matplotlib SVGs.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from matplotlib.colors import to_rgb
from matplotlib.text import Text
from matplotlib.transforms import Bbox

from graphplot.export.latex import color_command, format_latex_text


@dataclass
class _TextRecord:
    text: str
    x: float
    y: float
    ha: str
    va: str
    size: float
    rotation: float
    color: tuple[float, float, float]
    weight: str
    style: str
    raw: bool


def save_pdf_tex(
    figure,
    filename: str | Path,
    *,
    pdf_filename: str | Path | None = None,
    pad_inches: float = 0.02,
    transparent: bool = False,
) -> tuple[Path, Path]:
    """Save a text-free PDF and a ``.pdf_tex`` file.

    Parameters
    ----------
    filename
        Output base path, for example ``figures/fig``. The PDF_TeX file is
        written as ``figures/fig.pdf_tex``.
    pdf_filename
        Optional base path for the graphics PDF. Use this when a separate
        native PDF is also requested, so the two PDFs do not overwrite each
        other.

    Returns
    -------
    tuple of pathlib.Path
        PDF and PDF_TeX paths.
    """
    base = Path(filename)
    if base.suffix == ".pdf":
        base = base.with_suffix("")
    tex_path = Path(str(base) + ".pdf_tex")
    pdf_base = Path(pdf_filename) if pdf_filename is not None else base
    if pdf_base.suffix == ".pdf":
        pdf_base = pdf_base.with_suffix("")
    pdf_path = Path(str(pdf_base) + ".pdf")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    fig = figure.figure if hasattr(figure, "figure") else figure
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    bbox = _tight_bbox_inches(fig, renderer, pad_inches)
    records = _collect_text(fig, renderer, bbox)

    old_alphas = [
        (record_artist, record_artist.get_alpha())
        for record_artist in _text_artists(fig)
    ]
    try:
        for artist in _text_artists(fig):
            artist.set_alpha(0.0)
        fig.savefig(
            pdf_path,
            bbox_inches=bbox,
            pad_inches=0,
            dpi=fig.dpi,
            facecolor="none" if transparent else "white",
            edgecolor="none",
            metadata={"Creator": "graphPlot"},
        )
    finally:
        for artist, alpha in old_alphas:
            artist.set_alpha(alpha)

    _write_pdf_tex(tex_path, pdf_path, bbox, records)
    return pdf_path, tex_path


def _text_artists(fig) -> list[Text]:
    return [
        artist
        for artist in fig.findobj(match=Text)
        if artist.get_visible() and artist.get_text().strip()
    ]


def _collect_text(fig, renderer, bbox: Bbox) -> list[_TextRecord]:
    records: list[_TextRecord] = []
    tick_limits = _tick_label_limits(fig)
    for artist in _text_artists(fig):
        tick = tick_limits.get(id(artist))
        if tick is not None:
            low, high, location = tick
            tolerance = 1e-9 * max(1.0, abs(low), abs(high))
            if location < low - tolerance or location > high + tolerance:
                continue

        window = artist.get_window_extent(renderer)
        if window.width <= 0 or window.height <= 0:
            continue

        rotation = float(artist.get_rotation())
        if abs(rotation) > 1e-9:
            # Use the visual centre for rotated text. This is exact for the
            # common 90-degree axis labels and avoids anchor drift.
            x_display = (window.x0 + window.x1) / 2
            y_display = (window.y0 + window.y1) / 2
            ha, va = "center", "center"
        else:
            ha = artist.get_ha()
            va = artist.get_va()
            x_display = {
                "left": window.x0,
                "center": (window.x0 + window.x1) / 2,
                "right": window.x1,
            }.get(ha, (window.x0 + window.x1) / 2)
            y_display = {
                "bottom": window.y0,
                "center": (window.y0 + window.y1) / 2,
                "top": window.y1,
                "baseline": window.y0,
                "center_baseline": (window.y0 + window.y1) / 2,
            }.get(va, (window.y0 + window.y1) / 2)

        x_inches = x_display / fig.dpi
        y_inches = y_display / fig.dpi
        x_fraction = (x_inches - bbox.x0) / bbox.width
        y_fraction = (y_inches - bbox.y0) / bbox.width

        records.append(
            _TextRecord(
                text=artist.get_text(),
                x=x_fraction,
                y=y_fraction,
                ha=ha,
                va=va,
                size=float(artist.get_fontsize()),
                rotation=rotation,
                color=tuple(to_rgb(artist.get_color())),
                weight=str(artist.get_fontweight()),
                style=str(artist.get_fontstyle()),
                raw=bool(artist.get_usetex()),
            )
        )
    return records


def _tick_label_limits(fig) -> dict[int, tuple[float, float, float]]:
    """Map tick-label artists to their axis limits and tick location."""
    limits: dict[int, tuple[float, float, float]] = {}
    for axes in fig.axes:
        for axis, (low, high) in (
            (axes.xaxis, axes.get_xlim()),
            (axes.yaxis, axes.get_ylim()),
        ):
            ticks = list(axis.get_major_ticks()) + list(axis.get_minor_ticks())
            for tick in ticks:
                location = float(tick.get_loc())
                for label in (tick.label1, tick.label2):
                    if label is not None:
                        limits[id(label)] = (float(low), float(high), location)
    return limits


def _write_pdf_tex(
    tex_path: Path,
    pdf_path: Path,
    bbox: Bbox,
    records: list[_TextRecord],
) -> None:
    width_points = bbox.width * 72.0
    height_points = bbox.height * 72.0
    if width_points <= 0 or height_points <= 0:
        raise ValueError("The figure has an empty bounding box.")

    picture_height = height_points / width_points
    pdf_name = pdf_path.as_posix()

    lines = [
        "% Generated by graphPlot. Include this file with \\input{...}.",
        "\\begingroup",
        "\\providecommand{\\textcolor}[2]{#2}% fall back if xcolor is not loaded",
        "\\ifx\\svgwidth\\undefined",
        f"  \\setlength{{\\unitlength}}{{{width_points:.6f}bp}}%",
        "\\else",
        "  \\setlength{\\unitlength}{\\svgwidth}%",
        "\\fi",
        f"\\begin{{picture}}(1,{picture_height:.8f})%",
        "  \\put(0,0){\\includegraphics[width=\\unitlength]{"
        "\\detokenize{" + pdf_name + "}}}%",
    ]

    for record in records:
        body = _format_record(record)
        align = _alignment(record.ha, record.va)
        lines.append(
            f"  \\put({record.x:.8f},{record.y:.8f})"
            f"{{\\makebox(0,0)[{align}]{{\\fontsize{{{record.size:.4f}}}"
            f"{{{record.size * 1.2:.4f}}}\\selectfont {body}}}}}%"
        )

    lines.extend(["\\end{picture}%", "\\endgroup%", ""])
    tex_path.write_text("\n".join(lines), encoding="utf-8")


def _format_record(record: _TextRecord) -> str:
    body = format_latex_text(record.text, raw=record.raw)
    commands: list[str] = []
    if record.weight.lower() in ("bold", "600", "700", "800", "900"):
        commands.append("\\bfseries")
    if record.style.lower() in ("italic", "oblique"):
        commands.append("\\itshape")
    if commands:
        body = "{" + " ".join(commands) + " " + body + "}"
    body = color_command(record.color, body)
    if abs(record.rotation) > 1e-9:
        body = f"\\rotatebox[origin=c]{{{record.rotation:.4f}}}{{{body}}}"
    return body


def _alignment(ha: str, va: str) -> str:
    horizontal = {"left": "l", "center": "c", "right": "r"}.get(ha, "c")
    vertical = {
        "bottom": "b",
        "baseline": "b",
        "center": "c",
        "center_baseline": "c",
        "top": "t",
    }.get(va, "c")
    return horizontal + vertical


def _tight_bbox_inches(fig, renderer, pad_inches: float) -> Bbox:
    bbox = fig.get_tightbbox(renderer)
    if bbox is None:
        bbox = fig.bbox_inches
    # Some Matplotlib versions return display pixels from get_tightbbox.
    if bbox.width > fig.get_figwidth() * 2:
        bbox = Bbox.from_bounds(
            bbox.x0 / fig.dpi,
            bbox.y0 / fig.dpi,
            bbox.width / fig.dpi,
            bbox.height / fig.dpi,
        )
    if pad_inches:
        bbox = bbox.padded(pad_inches)
    return bbox
