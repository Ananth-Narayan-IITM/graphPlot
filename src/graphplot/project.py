"""Shared project-level figure settings.

A :class:`Project` keeps the canvas size, export formats, DPI, style and output
directory in one place. Figure scripts import one project object and use
``project.figure()`` and ``project.save(...)`` so a single edit propagates to
every script.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

from graphplot.figure import Figure
from graphplot.style import Style


@dataclass(frozen=True)
class Project:
    """Shared defaults for a collection of publication figures.

    Parameters
    ----------
    width, height
        Canvas size in inches. If ``height`` is ``None``, the figure derives it
        from ``height_ratio`` in :class:`graphplot.Figure`.
    dpi
        Raster resolution for PNG/PDF export.
    style
        A :class:`graphplot.Style`, a preset name such as ``"paper"``, or
        ``None`` for the default.
    formats
        Default export formats, for example ``("pdf_tex", "png")``.
    output_dir
        Default directory for :meth:`save`.
    pad_inches, transparent, pdf_tex_text_size
        Export defaults forwarded to :meth:`graphplot.Figure.save`.
    """

    width: float = 3.4
    height: float | None = None
    dpi: int = 600
    style: Style | str | None = None
    formats: tuple[str, ...] = ("pdf_tex", "png")
    output_dir: str | Path = "output"
    pad_inches: float = 0.02
    transparent: bool = False
    pdf_tex_text_size: str = "inherit"

    def __post_init__(self) -> None:
        object.__setattr__(self, "formats", tuple(self.formats))
        object.__setattr__(self, "output_dir", Path(self.output_dir))
        if isinstance(self.style, str):
            object.__setattr__(self, "style", Style.from_preset(self.style))

    def figure(self, **overrides) -> Figure:
        """Create a figure using the project defaults.

        Any keyword accepted by :class:`graphplot.Figure` can be overridden,
        for example ``project.figure(height=3.0, layout=None)``.
        """
        kwargs = {
            "width": self.width,
            "height": self.height,
            "dpi": self.dpi,
            "style": self.style,
        }
        kwargs.update(overrides)
        return Figure(**kwargs)

    def save(self, figure: Figure, name: str | Path, **overrides) -> dict[str, Path]:
        """Save a figure under ``output_dir`` using the project defaults."""
        kwargs = {
            "formats": self.formats,
            "dpi": self.dpi,
            "transparent": self.transparent,
            "pad_inches": self.pad_inches,
            "pdf_tex_text_size": self.pdf_tex_text_size,
        }
        kwargs.update(overrides)
        return figure.save(self.output_dir / name, **kwargs)

    def with_(self, **overrides) -> Project:
        """Return a copy with selected fields changed."""
        return replace(self, **overrides)

    def __getattr__(self, name: str):
        if name.startswith("_"):
            raise AttributeError(name)
        raise AttributeError(
            "Project is a settings object, not a figure. "
            f"Use project.figure() before calling {name!r}."
        )
