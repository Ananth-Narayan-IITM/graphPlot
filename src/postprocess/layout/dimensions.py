SINGLE_COLUMN_WIDTH = 3.5
DOUBLE_COLUMN_WIDTH = 7.0


def get_width(name):
    """
    Return a standard publication figure width.
    """

    if name == "single_column":
        return SINGLE_COLUMN_WIDTH

    if name == "double_column":
        return DOUBLE_COLUMN_WIDTH

    raise ValueError(
        f"Unknown figure width '{name}'. Use 'single_column' or 'double_column'."
    )
