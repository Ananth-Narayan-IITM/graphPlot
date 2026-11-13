"""Raw LaTeX labels for PDF_TeX export.

Matplotlib only understands a subset of LaTeX through mathtext. Labels that use
macros from the surrounding LaTeX document, such as ``\\RaE`` or ``\\cite``,
cannot be rendered by Matplotlib. :class:`TeX` stores the raw LaTeX for the
PDF_TeX writer and a plain fallback for PNG, SVG and native PDF output.
"""

from __future__ import annotations

import re

_CITE_RE = re.compile(r"\\cite[a-zA-Z]*\{(?P<key>[^}]*)\}")
_FORMAT_RE = re.compile(
    r"\\(?:mathbb|mathrm|mathbf|mathit|mathcal|mathsf|mathtt|text|textrm|"
    r"textbf|textit|textsf|texttt)\{([^{}]*)\}"
)
_COMMAND_RE = re.compile(r"\\([A-Za-z]+)")
_ESCAPED_RE = re.compile(r"\\([%&#$_{}])")
_BRACES_RE = re.compile(r"[{}]")


class TeX:
    """A label that is written as raw LaTeX in ``.pdf_tex`` output.

    Parameters
    ----------
    latex
        The exact LaTeX source, for example ``r"\\RaE = 0"``.
    plain
        Optional fallback used for PNG, SVG and native PDF output. When it is
        omitted, a readable approximation is derived from ``latex``.
    math
        Wrap the source in ``$...$`` unless it is already math. Use this for
        macros such as ``\\Nu`` that expand to math-mode commands.
    """

    __slots__ = ("latex", "plain")

    def __init__(
        self,
        latex: str,
        plain: str | None = None,
        *,
        math: bool = False,
    ) -> None:
        if not isinstance(latex, str):
            raise TypeError("TeX latex source must be a string.")
        if plain is not None and not isinstance(plain, str):
            raise TypeError("TeX plain fallback must be a string or None.")
        stripped = latex.strip()
        if (
            math
            and stripped
            and not (stripped.startswith("$") and stripped.endswith("$"))
        ):
            latex = f"${latex}$"
        self.latex = latex
        self.plain = plain

    def __str__(self) -> str:
        return self.plain if self.plain is not None else latex_to_plain(self.latex)

    def __repr__(self) -> str:
        if self.plain is None:
            return f"TeX({self.latex!r})"
        return f"TeX({self.latex!r}, plain={self.plain!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TeX):
            return NotImplemented
        return (self.latex, self.plain) == (other.latex, other.plain)

    def __hash__(self) -> int:
        return hash((self.latex, self.plain))


def tex(latex: str, plain: str | None = None, *, math: bool = False) -> TeX:
    """Return a raw-LaTeX label with an optional plain-text fallback.

    Use ``math=True`` for macros that expand to math-mode commands, such as
    ``\\newcommand{\\Nu}{\\mathbb{Nu}}``.

    Examples
    --------
    >>> label = tex(r"\\RaE = 0", plain="RaE = 0")
    >>> label.latex
    '\\\\RaE = 0'
    >>> str(label)
    'RaE = 0'
    >>> tex(r"\\Nu", math=True).latex
    '$\\\\Nu$'
    """
    return TeX(latex, plain, math=math)


def as_plain(value) -> str:
    """Return the text Matplotlib should use for ``value``."""
    return str(value)


def as_latex(value) -> str | None:
    """Return raw LaTeX when ``value`` is a :class:`TeX` object."""
    return value.latex if isinstance(value, TeX) else None


def tag_latex(artist, value) -> None:
    """Attach raw LaTeX to a Matplotlib artist for the PDF_TeX writer."""
    latex = as_latex(value)
    if latex is not None and artist is not None:
        artist._graphplot_latex = latex


def with_unit(value, unit: str | None):
    """Append a unit to a label while preserving raw LaTeX."""
    if unit is None:
        return value
    plain = as_plain(value)
    if plain.endswith("]"):
        return value
    latex = as_latex(value)
    if latex is None:
        return f"{plain} [{unit}]"
    return TeX(f"{latex} [{unit}]", f"{plain} [{unit}]")


def latex_to_plain(source: str) -> str:
    """Derive a readable fallback from simple LaTeX source."""
    text = _CITE_RE.sub(lambda match: f"[{match.group('key')}]", source)
    text = re.sub(r"\\(?:ref|eqref)\{([^}]*)\}", r"\1", text)
    text = _FORMAT_RE.sub(r"\1", text)
    text = _COMMAND_RE.sub(r"\1", text)
    text = _ESCAPED_RE.sub(r"\1", text)
    text = _BRACES_RE.sub("", text)
    return " ".join(text.split())
