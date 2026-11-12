"""Readers for scientific tabular data."""

from __future__ import annotations

import csv
import re
from pathlib import Path

import numpy as np

from graphplot.data.series import Data1D
from graphplot.data.table import Table

_NUMBER_RE = re.compile(r"^[+-]?(?:\d+\.?\d*|\.\d+)(?:[eEdD][+-]?\d+)?$")
_VECTOR_RE = re.compile(r"\(([^()]*)\)")
_UNIT_RE = re.compile(r"^(.*?)\s*(?:\[([^\]]+)\]|\(([^)]+)\))$")


def read_table(
    filename: str | Path,
    *,
    delimiter: str | None = None,
    comments: str = "#",
    skiprows: int = 0,
    names: list[str] | tuple[str, ...] | None = None,
    header: bool | None = None,
) -> Table:
    """Read a CSV or whitespace-delimited numeric table.

    The reader is deliberately flexible: it detects the delimiter, detects a
    header line (including OpenFOAM ``# Time 0 1 2`` comments), expands
    OpenFOAM vector tuples such as ``(ux uy uz)`` into separate columns, and
    extracts units from headers like ``x [m]``.
    """
    path = Path(filename)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")

    raw_lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    raw_lines = raw_lines[skiprows:]
    comment_lines = [line.strip() for line in raw_lines if _is_comment(line, comments)]
    data_lines = [
        line.strip()
        for line in raw_lines
        if line.strip() and not _is_comment(line, comments)
    ]
    if not data_lines:
        raise ValueError(f"No data rows found in {path}")

    if delimiter is None:
        delimiter = _detect_delimiter(data_lines[0], comments)

    first_tokens = _split_line(data_lines[0], delimiter, comments)
    column_names: list[str] | None = None

    if names is not None:
        column_names = [str(name) for name in names]
    elif header is True:
        column_names = first_tokens
        data_lines = data_lines[1:]
    elif header is None:
        if _looks_like_header(first_tokens):
            column_names = first_tokens
            data_lines = data_lines[1:]
        else:
            column_names = _header_from_comments(
                comment_lines, len(first_tokens), delimiter
            )

    if not data_lines:
        raise ValueError(f"No data rows found in {path}")

    first_tokens = _split_line(data_lines[0], delimiter, comments)
    rows, expanded_names = _parse_rows(data_lines, first_tokens, delimiter, comments)
    values = np.asarray(rows, dtype=float)

    if column_names is None:
        column_names = _default_names(expanded_names, values.shape[1])
    else:
        column_names = _expand_header(column_names, expanded_names, values.shape[1])

    names_with_units, units = _split_units(column_names)
    names_with_units = _deduplicate(names_with_units)
    columns = {name: values[:, i] for i, name in enumerate(names_with_units)}

    return Table(columns, units=units, metadata={"filename": str(path.resolve())})


def read_1d(
    filename: str | Path,
    *,
    x: str | int = 0,
    y: str | int = 1,
    label: str | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
    **kwargs,
) -> Data1D:
    """Read two columns as a :class:`Data1D` series."""
    table = read_table(filename, **kwargs)
    return table.series(x, y, label=label, x_label=x_label, y_label=y_label)


def read_numpy(filename: str | Path) -> Table:
    """Read a ``.npy`` or ``.npz`` file as a table."""
    path = Path(filename)
    data = np.load(path, allow_pickle=False)
    if isinstance(data, np.lib.npyio.NpzFile):
        if len(data.files) != 1:
            raise ValueError(
                f"{path} contains multiple arrays: {', '.join(data.files)}. "
                "Extract the desired array with numpy.load directly."
            )
        data = data[data.files[0]]

    array = np.asarray(data)
    if array.ndim == 1:
        array = array.reshape(-1, 1)
    if array.ndim != 2:
        raise ValueError(f"Expected a 1D or 2D array in {path}, got {array.shape}.")

    columns = {f"column_{i}": array[:, i] for i in range(array.shape[1])}
    return Table(columns, metadata={"filename": str(path.resolve())})


def _is_comment(line: str, comments: str) -> bool:
    stripped = line.lstrip()
    if not stripped:
        return False
    if comments is None:
        return False
    markers = [comments] if isinstance(comments, str) else list(comments)
    return any(stripped.startswith(marker) for marker in markers if marker)


def _strip_comment(line: str, comments: str) -> str:
    if comments is None:
        return line
    markers = [comments] if isinstance(comments, str) else list(comments)
    positions = [
        line.find(marker) for marker in markers if marker and line.find(marker) >= 0
    ]
    if positions:
        return line[: min(positions)]
    return line


def _detect_delimiter(line: str, comments: str) -> str | None:
    line = _strip_comment(line, comments)
    candidates = [",", ";", "\t"]
    counts = {candidate: line.count(candidate) for candidate in candidates}
    best = max(counts, key=counts.get)
    return best if counts[best] > 0 else None


def _split_line(line: str, delimiter: str | None, comments: str) -> list[str]:
    line = _strip_comment(line, comments).strip()
    if not line:
        return []
    if delimiter in (None, " ", "whitespace"):
        return _split_whitespace(line)
    return [
        token.strip()
        for token in next(csv.reader([line], delimiter=delimiter))
        if token.strip()
    ]


def _split_whitespace(line: str) -> list[str]:
    tokens: list[str] = []
    index = 0
    while index < len(line):
        if line[index].isspace():
            index += 1
            continue
        if line[index] == "(":
            end = line.find(")", index)
            if end == -1:
                raise ValueError(f"Unclosed vector tuple in line: {line!r}")
            tokens.append(line[index : end + 1])
            index = end + 1
            continue
        end = index
        while end < len(line) and not line[end].isspace():
            end += 1
        tokens.append(line[index:end])
        index = end
    return tokens


def _is_number(token: str) -> bool:
    return bool(_NUMBER_RE.match(token))


def _is_data_token(token: str) -> bool:
    if _is_number(token):
        return True
    match = _VECTOR_RE.fullmatch(token)
    if match:
        return all(_is_number(component) for component in match.group(1).split())
    return False


def _looks_like_header(tokens: list[str]) -> bool:
    return bool(tokens) and not all(_is_data_token(token) for token in tokens)


def _header_from_comments(
    comment_lines: list[str], n_tokens: int, delimiter: str | None
) -> list[str] | None:
    for line in reversed(comment_lines):
        content = re.sub(r"^[#%]+\s*", "", line).strip()
        tokens = _split_line(content, delimiter, None)
        if len(tokens) == n_tokens:
            return tokens
    return None


def _parse_rows(
    data_lines: list[str],
    first_tokens: list[str],
    delimiter: str | None,
    comments: str,
) -> tuple[list[list[float]], list[str]]:
    first_values, first_expanded = _parse_row(first_tokens)
    rows = [first_values]
    expanded_count = len(first_expanded)
    for line_number, line in enumerate(data_lines[1:], start=2):
        tokens = _split_line(line, delimiter, comments)
        try:
            values, expanded = _parse_row(tokens)
        except ValueError as exc:
            raise ValueError(f"Could not parse data row {line_number}: {exc}") from exc
        if len(values) != expanded_count:
            raise ValueError(
                f"Row {line_number} has {len(values)} columns; expected {expanded_count}."
            )
        rows.append(values)
    return rows, first_expanded


def _parse_row(tokens: list[str]) -> tuple[list[float], list[str]]:
    values: list[float] = []
    expanded: list[str] = []
    for token in tokens:
        match = _VECTOR_RE.fullmatch(token)
        if match:
            components = match.group(1).split()
            if not components:
                raise ValueError(f"Empty vector tuple {token!r}.")
            suffixes = ("x", "y", "z")
            for index, component in enumerate(components):
                if not _is_number(component):
                    raise ValueError(f"Non-numeric vector component {component!r}.")
                values.append(float(component))
                expanded.append(suffixes[index] if index < 3 else f"c{index}")
        else:
            if not _is_number(token):
                raise ValueError(f"Non-numeric token {token!r}.")
            values.append(float(token))
            expanded.append("")
    return values, expanded


def _default_names(expanded: list[str], n_columns: int) -> list[str]:
    names: list[str] = []
    for index in range(n_columns):
        suffix = expanded[index] if index < len(expanded) else ""
        names.append(f"column_{index}" + (f"_{suffix}" if suffix else ""))
    return names


def _expand_header(header: list[str], expanded: list[str], n_columns: int) -> list[str]:
    # A header token may describe a whole vector group. Match header tokens to
    # groups of expanded components (for example "0" -> 0_x, 0_y, 0_z).
    if len(header) == n_columns:
        return header

    group_sizes = _group_sizes(expanded)
    if len(header) == len(group_sizes):
        names: list[str] = []
        index = 0
        for token, size in zip(header, group_sizes, strict=False):
            if size == 1:
                names.append(token)
            else:
                for suffix in expanded[index : index + size]:
                    names.append(f"{token}_{suffix}")
            index += size
        return names

    # Fall back to header names where possible and generated names elsewhere.
    names = []
    for index in range(n_columns):
        suffix = expanded[index] if index < len(expanded) else ""
        if index < len(header):
            names.append(header[index] + (f"_{suffix}" if suffix else ""))
        else:
            names.append(f"column_{index}" + (f"_{suffix}" if suffix else ""))
    return names


def _group_sizes(expanded: list[str]) -> list[int]:
    sizes: list[int] = []
    vector_size = 0
    for suffix in expanded:
        if suffix == "x" and vector_size:
            # A new x component starts a new vector tuple.
            sizes.append(vector_size)
            vector_size = 0
        if suffix:
            vector_size += 1
        else:
            if vector_size:
                sizes.append(vector_size)
                vector_size = 0
            sizes.append(1)
    if vector_size:
        sizes.append(vector_size)
    return sizes


def _split_units(names: list[str]) -> tuple[list[str], dict[str, str]]:
    cleaned: list[str] = []
    units: dict[str, str] = {}
    for name in names:
        match = _UNIT_RE.match(name.strip())
        if match:
            base = match.group(1).strip()
            unit = (match.group(2) or match.group(3) or "").strip()
            if base and unit:
                cleaned.append(base)
                units[base] = unit
                continue
        cleaned.append(name.strip())
    return cleaned, units


def _deduplicate(names: list[str]) -> list[str]:
    counts: dict[str, int] = {}
    result: list[str] = []
    for name in names:
        if name not in counts:
            counts[name] = 1
            result.append(name)
        else:
            counts[name] += 1
            result.append(f"{name}_{counts[name]}")
    return result
