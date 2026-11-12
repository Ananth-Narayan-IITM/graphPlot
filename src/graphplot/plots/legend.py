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
    available = {
        label: handle
        for handle, label in zip(handles, labels, strict=False)
        if label and not label.startswith("_")
    }

    if isinstance(groups, dict):
        groups = [
            {"title": heading, "labels": group_labels}
            for heading, group_labels in groups.items()
        ]

    legend_handles = []
    legend_labels = []
    for group in groups:
        heading = group.get("title")
        if heading:
            legend_handles.append(Line2D([], [], linestyle="none", marker=None))
            legend_labels.append(heading)
        for label in group.get("labels", []):
            if label not in available:
                raise ValueError(
                    f"Legend label {label!r} was not found among plotted artists."
                )
            legend_handles.append(available[label])
            legend_labels.append(label)

    if not legend_handles:
        return None
    return axes.legend(
        legend_handles,
        legend_labels,
        loc=loc,
        ncol=ncol,
        frameon=frameon,
        fontsize=fontsize,
        title=title,
        **kwargs,
    )


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
    case_names = list(first_group)
    for group_name in group_names:
        if list(groups[group_name]) != case_names:
            raise ValueError(
                "All legend groups must contain the same case names in the same order."
            )

    def make_text(text, bold=False):
        return TextArea(
            str(text),
            textprops={
                "fontsize": fontsize,
                "fontweight": "bold" if bold else "normal",
                "ha": "center",
                "va": "center",
            },
        )

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
    for case_name in case_names:
        cells = [make_text(case_name)]
        cells.extend(
            make_handle(groups[group_name][case_name]) for group_name in group_names
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
