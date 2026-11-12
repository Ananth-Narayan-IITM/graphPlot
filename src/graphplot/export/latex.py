"""LaTeX text escaping and PDF_TeX helpers."""

from __future__ import annotations

import re

_MATH_RE = re.compile(r"(\$[^$]*\$)")

_ESCAPE = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}

_UNICODE = {
    "−": "$-$",
    "–": "--",
    "—": "---",
    "°": r"$^\circ$",
    "±": r"$\pm$",
    "×": r"$\times$",
    "·": r"$\cdot$",
    "≤": r"$\leq$",
    "≥": r"$\geq$",
    "≈": r"$\approx$",
    "≠": r"$\neq$",
    "μ": r"$\mu$",
    "α": r"$\alpha$",
    "β": r"$\beta$",
    "γ": r"$\gamma$",
    "δ": r"$\delta$",
    "ε": r"$\epsilon$",
    "ζ": r"$\zeta$",
    "η": r"$\eta$",
    "θ": r"$\theta$",
    "κ": r"$\kappa$",
    "λ": r"$\lambda$",
    "ν": r"$\nu$",
    "ξ": r"$\xi$",
    "π": r"$\pi$",
    "ρ": r"$\rho$",
    "σ": r"$\sigma$",
    "τ": r"$\tau$",
    "φ": r"$\phi$",
    "χ": r"$\chi$",
    "ψ": r"$\psi$",
    "ω": r"$\omega$",
    "Γ": r"$\Gamma$",
    "Δ": r"$\Delta$",
    "Θ": r"$\Theta$",
    "Λ": r"$\Lambda$",
    "Ξ": r"$\Xi$",
    "Π": r"$\Pi$",
    "Σ": r"$\Sigma$",
    "Φ": r"$\Phi$",
    "Ψ": r"$\Psi$",
    "Ω": r"$\Omega$",
}


def escape_latex(text: str, *, raw: bool = False) -> str:
    """Escape plain text while leaving ``$...$`` math untouched."""
    if raw:
        return text
    parts = _MATH_RE.split(text)
    escaped: list[str] = []
    for part in parts:
        if part.startswith("$") and part.endswith("$") and len(part) >= 2:
            escaped.append(part)
        else:
            escaped.append(_escape_plain(part))
    return "".join(escaped)


def format_latex_text(text: str, *, raw: bool = False) -> str:
    """Format a possibly multi-line text for a LaTeX text box."""
    lines = str(text).split("\n")
    escaped = [escape_latex(line, raw=raw) for line in lines]
    if len(escaped) == 1:
        return escaped[0]
    return r"\begin{tabular}[t]{@{}c@{}}" + r"\\".join(escaped) + r"\end{tabular}"


def color_command(rgb: tuple[float, float, float], content: str) -> str:
    """Wrap ``content`` in a text color command when it is not black."""
    red, green, blue = rgb
    if red < 1e-6 and green < 1e-6 and blue < 1e-6:
        return content
    return rf"\textcolor[rgb]{{{red:.3f},{green:.3f},{blue:.3f}}}{{{content}}}"


def _escape_plain(text: str) -> str:
    output: list[str] = []
    for char in text:
        if char in _UNICODE:
            output.append(_UNICODE[char])
        else:
            output.append(_ESCAPE.get(char, char))
    return "".join(output)
