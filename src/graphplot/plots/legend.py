"""Standard, grouped and table-style legends."""

from __future__ import annotations

from matplotlib.lines import Line2D
from matplotlib.offsetbox import (
    AnchoredOffsetbox,
    DrawingArea,
    HPacker,
    TextArea,
    VPacker,
)

from graphplot.tex import TeX, as_latex, as_plain, tag_latex


def grouped_legend(
    axes,
    groups,
    *,
    loc="best",
    ncol=1,
    frameon=False,
    fontsize=None,
    title=None,
    **kwargs,
):
    """Create a legend with optional group headings."""
    handles, labels = axes.get_legend_handles_labels()
    available: dict[str, list[tuple[object, str | None]]] = {}
    for handle, label in zip(handles, labels, strict=False):
        if label and not label.startswith("_"):
            available.setdefault(label, []).append(
                (handle, getattr(handle, "_graphplot_latex", None))
            )

    if isinstance(groups, dict):
        groups = [
            {"title": heading, "labels": group_labels}
            for heading, group_labels in groups.items()
        ]

    legend_handles = []
    legend_labels = []
    legend_latex = []
    for group in groups:
        heading = group.get("title")
        heading_text = "" if heading is None else as_plain(heading)
        if heading_text:
            legend_handles.append(Line2D([], [], linestyle="none", marker=None))
            legend_labels.append(heading_text)
            legend_latex.append(as_latex(heading))
        for label in group.get("labels", []):
            label_text = as_plain(label)
            matches = available.get(label_text)
            if not matches:
                raise ValueError(
                    f"Legend label {label_text!r} was not found among plotted artists."
                )
            handle, handle_latex = matches.pop(0)
            legend_handles.append(handle)
            legend_labels.append(label_text)
            legend_latex.append(as_latex(label) or handle_latex)

    if not legend_handles:
        return None
    legend = axes.legend(
        legend_handles,
        legend_labels,
        loc=loc,
        ncol=ncol,
        frameon=frameon,
        fontsize=fontsize,
        title=None if title is None else as_plain(title),
        **kwargs,
    )
    for text_artist, raw in zip(legend.get_texts(), legend_latex, strict=False):
        if raw is not None:
            tag_latex(text_artist, TeX(raw, text_artist.get_text()))
    tag_latex(legend.get_title(), title)
    return legend


def table_legend(
    figure,
    groups,
    *,
    location="lower center",
    bbox_to_anchor=(0.5, -0.12),
    fontsize=8,
    handle_length=32,
    column_spacing=30,
    row_spacing=5,
):
    """Create a table-style legend.

    ``groups`` maps a group heading (for example ``"Experiment"``) to a
    mapping of case names to Matplotlib line artists.
    """
    if not groups:
        return None

    group_names = list(groups)
    first_group = groups[group_names[0]]
    case_keys = list(first_group)
    case_names = [as_plain(case) for case in case_keys]
    mappings = {}
    for group_name in group_names:
        mapping = {as_plain(case): value for case, value in groups[group_name].items()}
        if list(mapping) != case_names:
            raise ValueError(
                "All legend groups must contain the same case names in the same order."
            )
        mappings[group_name] = mapping

    def make_text(value, bold=False):
        area = TextArea(
            as_plain(value),
            textprops={
                "fontsize": fontsize,
                "fontweight": "bold" if bold else "normal",
                "ha": "center",
                "va": "center",
            },
        )
        tag_latex(area._text, value)
        return area

    def make_handle(handle):
        drawing = DrawingArea(handle_length, 12, 0, 0)
        line = _as_line(handle)
        color = line.get_color()
        drawing.add_artist(
            Line2D(
                [0, handle_length],
                [6, 6],
                color=color,
                linewidth=line.get_linewidth(),
                linestyle=line.get_linestyle(),
                marker=line.get_marker(),
                markersize=line.get_markersize(),
                markerfacecolor=line.get_markerfacecolor(),
                markeredgecolor=line.get_markeredgecolor(),
                markeredgewidth=line.get_markeredgewidth(),
            )
        )
        return drawing

    header_cells = [make_text("")]
    header_cells.extend(make_text(name) for name in group_names)
    header = HPacker(children=header_cells, align="center", sep=column_spacing)

    rows = []
    for case_key, case_name in zip(case_keys, case_names, strict=True):
        cells = [make_text(case_key)]
        cells.extend(
            make_handle(mappings[group_name][case_name]) for group_name in group_names
        )
        rows.append(HPacker(children=cells, align="center", sep=column_spacing))

    table = VPacker(children=[header, *rows], align="center", sep=row_spacing)
    legend = AnchoredOffsetbox(
        loc=location,
        child=table,
        frameon=False,
        bbox_to_anchor=bbox_to_anchor,
        bbox_transform=figure.transFigure,
        borderpad=0.0,
        pad=0.0,
    )
    figure.add_artist(legend)
    return legend


def _as_line(handle) -> Line2D:
    if isinstance(handle, Line2D):
        return handle
    lines = getattr(handle, "lines", None)
    if lines:
        return lines[0]
    raise TypeError(
        "Table legends require line artists; error-bar containers are not supported."
    )
