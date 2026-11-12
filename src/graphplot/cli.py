"""Command-line runner and diagnostics.

Usage:
    graphPlot figure.py [arguments...]
    graphPlot check
    graphPlot info case.vtp
"""

from __future__ import annotations

import argparse
import os
import runpy
import sys
import traceback
from pathlib import Path

from graphplot import __version__
from graphplot._checks import format_check
from graphplot.io.load import load


def main(argv: list[str] | None = None) -> int:
    """Run a figure script or a diagnostic command."""
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        _print_help()
        return 0

    first = args[0]
    if first in ("-h", "--help"):
        _print_help()
        return 0
    if first in ("-V", "--version"):
        print(f"graphPlot {__version__}")
        return 0
    if first == "check":
        print(format_check())
        return 0
    if first == "info":
        return _info(args[1:])
    if first.startswith("-"):
        print(f"graphPlot: error: unknown option {first!r}", file=sys.stderr)
        _print_help()
        return 2
    return run_script(first, args[1:])


def run_script(filename: str | Path, args: list[str] | None = None) -> int:
    """Execute a Python figure script as ``__main__``.

    The script directory is placed on ``sys.path`` and ``sys.argv`` is set to
    the script path followed by the remaining arguments. Matplotlib uses the
    non-interactive Agg backend unless ``MPLBACKEND`` is already set.
    """
    path = Path(filename).expanduser()
    if not path.is_file():
        print(f"graphPlot: error: Python script not found: {filename}", file=sys.stderr)
        return 2
    path = path.resolve()

    os.environ.setdefault("MPLBACKEND", "Agg")
    old_argv = list(sys.argv)
    old_path = list(sys.path)
    try:
        sys.argv = [str(path), *(args or [])]
        sys.path.insert(0, str(path.parent))
        runpy.run_path(str(path), run_name="__main__")
    except SystemExit as exc:
        code = exc.code
        if code is None:
            return 0
        return int(code) if isinstance(code, int) else 1
    except Exception:
        traceback.print_exc()
        return 1
    finally:
        sys.argv = old_argv
        sys.path[:] = old_path
    return 0


def _info(args: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="graphPlot info")
    parser.add_argument("file", type=Path, help="VTP, VTU or tabular data file")
    namespace = parser.parse_args(args)
    try:
        data = load(namespace.file)
    except Exception as exc:
        print(f"graphPlot: error: {exc}", file=sys.stderr)
        return 1

    print(data)
    if hasattr(data, "fields"):
        print("fields:")
        for name, association in data.fields.items():
            print(f"  {name} ({association})")
        print(f"bounds: {data.bounds}")
    elif hasattr(data, "info"):
        print(data.info())
    return 0


def _print_help() -> None:
    print(
        "graphPlot 2.0 — publication figures from VTP and tabular data\n"
        "\n"
        "Usage:\n"
        "  graphPlot <script.py> [arguments...]   run a figure script\n"
        "  graphPlot check                        check the environment\n"
        "  graphPlot info <file>                  summarize a data file\n"
        "  graphPlot --version                    show the version\n"
        "  graphPlot --help                       show this message"
    )
