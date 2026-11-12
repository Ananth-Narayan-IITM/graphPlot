"""Publication style presets and categorical cycles."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, replace

import matplotlib as mpl

COLORBLIND = (
    "#0072B2",
    "#E69F00",
    "#009E73",
    "#D55E00",
    "#CC79A7",
    "#56B4E9",
    "#F0E442",
    "#000000",
)

DEFAULT_COLORS = (
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
)

GRAYSCALE = ("#000000", "#404040", "#707070", "#999999", "#BFBFBF", "#D9D9D9")

MARKERS = ("o", "s", "^", "D", "v", "<", ">", "P", "X")
LINESTYLES = ("-", "--", "-.", ":")


@dataclass(frozen=True)
class Style:
    """Visual defaults shared by every figure and panel.

    A style is immutable. Use :meth:`with_` to create a modified copy.
    """

    preset: str = "paper"
    font_family: str = "serif"
    font_size: float = 9.0
    label_size: float = 9.0
    title_size: float = 9.0
    tick_size: float = 8.0
    legend_size: float = 8.0

    line_width: float = 1.2
    axes_line_width: float = 0.8
    tick_width: float = 0.8
    tick_length: float = 3.0
    marker_size: float = 4.0

    colors: tuple[str, ...] = COLORBLIND
    markers: tuple[str, ...] = MARKERS
    linestyles: tuple[str, ...] = LINESTYLES

    dpi: int = 600
    grid: bool = False
    mathtext: str = "stix"

    @classmethod
    def from_preset(cls, preset: str = "paper", **overrides) -> Style:
        """Return a style preset with optional field overrides."""
        preset = preset.lower()
        if preset == "paper":
            base = cls()
        elif preset == "ieee":
            base = cls(
                preset="ieee",
                font_size=8.0,
                label_size=8.0,
                title_size=8.0,
                tick_size=7.0,
                legend_size=7.0,
                line_width=1.0,
                dpi=600,
            )
        elif preset == "elsevier":
            base = cls(
                preset="elsevier",
                font_family="serif",
                font_size=9.0,
                label_size=9.0,
                title_size=9.0,
                tick_size=8.0,
                legend_size=8.0,
                line_width=1.1,
                dpi=600,
            )
        elif preset == "thesis":
            base = cls(
                preset="thesis",
                font_size=10.0,
                label_size=10.0,
                title_size=10.0,
                tick_size=9.0,
                legend_size=9.0,
                line_width=1.3,
                dpi=300,
            )
        elif preset == "screen":
            base = cls(
                preset="screen",
                font_family="sans-serif",
                font_size=10.0,
                label_size=10.0,
                title_size=11.0,
                tick_size=9.0,
                legend_size=9.0,
                line_width=1.5,
                dpi=150,
            )
        else:
            available = "paper, ieee, elsevier, thesis, screen"
            raise ValueError(
                f"Unknown style preset {preset!r}. Available: {available}."
            )
        return replace(base, **overrides) if overrides else base

    def with_(self, **overrides) -> Style:
        """Return a modified copy of this style."""
        return replace(self, **overrides)

    def rc(self) -> dict[str, object]:
        """Return the Matplotlib rcParams implied by this style."""
        return {
            "font.family": self.font_family,
            "font.size": self.font_size,
            "axes.labelsize": self.label_size,
            "axes.titlesize": self.title_size,
            "xtick.labelsize": self.tick_size,
            "ytick.labelsize": self.tick_size,
            "legend.fontsize": self.legend_size,
            "lines.linewidth": self.line_width,
            "lines.markersize": self.marker_size,
            "axes.linewidth": self.axes_line_width,
            "xtick.major.width": self.tick_width,
            "ytick.major.width": self.tick_width,
            "xtick.minor.width": self.tick_width * 0.8,
            "ytick.minor.width": self.tick_width * 0.8,
            "xtick.major.size": self.tick_length,
            "ytick.major.size": self.tick_length,
            "xtick.minor.size": self.tick_length * 0.6,
            "ytick.minor.size": self.tick_length * 0.6,
            "axes.grid": self.grid,
            "axes.unicode_minus": False,
            "mathtext.fontset": self.mathtext,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "savefig.dpi": self.dpi,
        }

    def apply(self) -> None:
        """Apply this style to the current Matplotlib session."""
        mpl.rcParams.update(self.rc())

    @contextmanager
    def context(self) -> Iterator[None]:
        """Temporarily apply this style."""
        with mpl.rc_context(self.rc()):
            yield

    def color(self, index: int) -> str:
        """Return the categorical color at ``index``."""
        return self.colors[index % len(self.colors)]

    def marker(self, index: int) -> str:
        """Return the marker at ``index``."""
        return self.markers[index % len(self.markers)]

    def linestyle(self, index: int) -> str:
        """Return the line style at ``index``."""
        return self.linestyles[index % len(self.linestyles)]
