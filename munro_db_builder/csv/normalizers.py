"""Utilities for normalizing cells from the DoBIH Munros and Tops CSV file."""

from collections.abc import Sequence


def _normalize_height_ft(column_name: str) -> str:
    r"""Normalizes the `Height\n(ft)` column name.

    Normalizes the name of the `Height\n(ft)` column to `Height (ft)`;
    returns all other column names unchanged.

    Args:
        column_name: The name of the column to be normalized.

    Returns:
        The normalized column name.
    """
    if column_name == "Height\n(ft)":
        return "Height (ft)"

    return column_name


def normalize_column_names(column_names: Sequence[str]) -> list[str]:
    """Normalizes column names.

    Applies `_normalize_height_ft` to each column name.

    Args:
        column_names: The column names to be normalized.

    Returns:
        The normalized column names.
    """
    return [_normalize_height_ft(column_name) for column_name in column_names]


def normalize_int(value: str) -> int | None:
    """Normalizes a column value to an `int`.

    Args:
        value: The column value to be normalized.

    Returns:
        The column value normalized as an `int` if it is numeric,
        or `None` if it is empty or not numeric.
    """
    try:
        return int(value)
    except ValueError:
        return None
