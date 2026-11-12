"""Figure export helpers."""

from __future__ import annotations

from pathlib import Path

from graphplot.export.pdftex import save_pdf_tex


def save_figure(
    figure,
    filename: str | Path,
    *,
    formats: str | tuple[str, ...] | list[str] = ("pdf_tex", "png"),
    dpi: int | None = None,
    transparent: bool = False,
    pad_inches: float = 0.02,
    **savefig_kwargs,
) -> dict[str, Path]:
    """Save a figure in one or more formats.

    Supported formats are ``pdf_tex``, ``pdf``, ``png``, ``svg`` and ``eps``.
    """
    if isinstance(formats, str):
        formats = (formats,)
    formats = tuple(dict.fromkeys(formats))
    base = Path(filename)
    if base.suffix in {".pdf", ".png", ".svg", ".eps"}:
        base = base.with_suffix("")
    base.parent.mkdir(parents=True, exist_ok=True)

    fig = figure.figure if hasattr(figure, "figure") else figure
    dpi = dpi or getattr(figure, "dpi", 600)
    paths: dict[str, Path] = {}

    if "pdf_tex" in formats:
        graphics_pdf = base.with_name(base.name + "_tex") if "pdf" in formats else base
        pdf_path, tex_path = save_pdf_tex(
            figure,
            base,
            pdf_filename=graphics_pdf,
            pad_inches=pad_inches,
            transparent=transparent,
        )
        paths["pdf_tex"] = tex_path
        paths["pdf_tex_graphics"] = pdf_path

    if "pdf" in formats:
        path = base.with_suffix(".pdf")
        fig.savefig(
            path,
            bbox_inches="tight",
            pad_inches=pad_inches,
            dpi=dpi,
            transparent=transparent,
            **savefig_kwargs,
        )
        paths["pdf"] = path

    if "png" in formats:
        path = base.with_suffix(".png")
        fig.savefig(
            path,
            bbox_inches="tight",
            pad_inches=pad_inches,
            dpi=dpi,
            transparent=transparent,
            **savefig_kwargs,
        )
        paths["png"] = path

    if "svg" in formats:
        path = base.with_suffix(".svg")
        fig.savefig(
            path,
            bbox_inches="tight",
            pad_inches=pad_inches,
            transparent=transparent,
            **savefig_kwargs,
        )
        paths["svg"] = path

    if "eps" in formats:
        path = base.with_suffix(".eps")
        fig.savefig(path, bbox_inches="tight", **savefig_kwargs)
        paths["eps"] = path

    unknown = set(formats) - {"pdf_tex", "pdf", "png", "svg", "eps"}
    if unknown:
        raise ValueError(f"Unsupported format(s): {', '.join(sorted(unknown))}")
    return paths
