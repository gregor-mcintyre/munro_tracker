"""Filters to Munros from the DoBIH Munros and Tops CSV file.

Maps CSV rows to the internal schema and filters to Munros based on the classification
from the latest survey-year.
"""

from collections.abc import Iterable, Iterator

from munro_db_builder._mapper import (
    MappedRow,
    map_to_internal_schema_and_add_classification,
)
from munro_db_builder.csv.row_type import CSVRow


def _is_munro(mapped_row: MappedRow) -> bool:
    """Determines whether a row is a Munro row.

    A row is defined as a Munro row if its classification is `MUN`. Munro Top and
    unclassified rows are rejected, as well as non-mountain rows.

    Args:
        mapped_row: A row mapped to the internal schema.

    Returns:
        `True` if the row classification is `MUN`, otherwise `False`.
    """
    return mapped_row["classification"] == "MUN"


def _filter_to_munros(mapped_rows: Iterable[MappedRow]) -> Iterator[MappedRow]:
    """Filters to Munros.

    Args:
        mapped_rows: The rows mapped to the internal schema that are to be filtered.

    Returns:
        Mapped rows where `_is_munro` is `True`.
    """
    return (row for row in mapped_rows if _is_munro(row))


def map_and_filter_to_munros(
    csv_rows: Iterable[CSVRow],
    *,
    latest_year_column: str,
) -> Iterator[MappedRow]:
    """Maps CSV rows to the internal schema and filters to Munros.

    Args:
        csv_rows: CSV rows with original normalized column names.
        latest_year_column: The column name of the latest survey-year in the CSV file.
            This is where the classification is to be extracted from.

    Returns:
        Mapped rows classified as Munros.
    """
    mapped_rows = (
        map_to_internal_schema_and_add_classification(
            csv_row,
            latest_year_column=latest_year_column,
        )
        for csv_row in csv_rows
    )

    return _filter_to_munros(mapped_rows)
