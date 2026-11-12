"""Environment diagnostics used by the ``graphplot check`` command."""

from __future__ import annotations

import importlib
import shutil
import sys
from dataclasses import dataclass


@dataclass
class CheckResult:
    """Result of one environment check."""

    name: str
    ok: bool
    detail: str


def check() -> list[CheckResult]:
    """Check Python, package and external tool availability."""
    results: list[CheckResult] = []

    results.append(
        CheckResult("Python", sys.version_info >= (3, 10), sys.version.split()[0])
    )

    for module in ("numpy", "matplotlib", "pyvista"):
        try:
            imported = importlib.import_module(module)
            version = getattr(imported, "__version__", "unknown")
            results.append(CheckResult(module, True, version))
        except Exception as exc:  # pragma: no cover - environment dependent
            results.append(CheckResult(module, False, str(exc)))

    for tool in ("pdflatex", "latexmk", "doxygen"):
        path = shutil.which(tool)
        results.append(CheckResult(tool, path is not None, path or "not found"))

    return results


def format_check(results: list[CheckResult] | None = None) -> str:
    """Return a printable diagnostic report."""
    results = results or check()
    lines = ["graphPlot environment check", "=" * 30]
    for result in results:
        status = "OK" if result.ok else "MISSING"
        lines.append(f"{status:8} {result.name:12} {result.detail}")
    return "\n".join(lines)
