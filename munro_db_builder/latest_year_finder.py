"""Find the latest survey-year column in the DoBIH Munros and Tops CSV file."""

from collections.abc import Iterable


def find_latest_year_column(column_names: Iterable[str]) -> str:
    """Finds the latest survey-year column.

    The latest survey-year column is extracted from column names from
    the DoBIH Munros and Tops CSV file.

    DoBIH classifies Munros and Tops in a single column per survey-year.
    Automatically finding the column of the latest survey-year allows
    for new years added to future files to be handled appropriately,
    assuming the format of the file does not change.

    Args:
        column_names: The column names from the CSV file.

    Returns:
        The column name representing the latest survey-year.
    """
    year_columns = [name for name in column_names if name.isdigit()]

    return max(year_columns, key=int)
