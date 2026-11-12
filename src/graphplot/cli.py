"""Command-line diagnostics for graphPlot."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from graphplot._checks import format_check
from graphplot.io.load import load


def main(argv: list[str] | None = None) -> int:
    """Run the ``graphplot`` command."""
    parser = argparse.ArgumentParser(
        prog="graphplot",
        description="Diagnostics for the graphPlot publication-figure toolkit.",
    )
    parser.add_argument("--version", action="version", version="graphPlot 2.0")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "check", help="check the Python environment and external tools"
    )

    info = subparsers.add_parser("info", help="print a summary of a data file")
    info.add_argument("file", type=Path, help="VTP, VTU or tabular data file")

    args = parser.parse_args(argv)

    if args.command in (None, "check"):
        print(format_check())
        return 0

    if args.command == "info":
        try:
            data = load(args.file)
        except Exception as exc:
            print(f"graphplot: {exc}", file=sys.stderr)
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

    parser.print_help()
    return 2
