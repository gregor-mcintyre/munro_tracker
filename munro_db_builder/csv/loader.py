"""Utility for loading the DoBIH Munros and Tops CSV file."""

import csv
from pathlib import Path

from munro_db_builder.csv.normalizers import normalize_column_names
from munro_db_builder.csv.row_type import CSVRow
import paths


def load_munros_and_tops_from_dobih_csv(
    *,
    path: Path = paths.DOBIH_MUNROS_CSV_FILE,
) -> list[CSVRow]:
    r"""Loads Munros and Tops from a CSV file.

    Opens the file with the `cp1252` encoding since it appears this is what DoBIH have
    published it with (common for Microsoft Excel on Windows). Also opens it with `""`
    for newlines so the newline in the `Height\n(ft)` column name is handled correctly.

    Normalizes column names where necessary.

    Args:
        path: The path to the CSV file to read.

    Returns:
        The Munros and Tops loaded from the CSV file.
    """
    with path.open(encoding="cp1252", newline="") as file:
        reader = csv.DictReader(file)

        reader.fieldnames = normalize_column_names(reader.fieldnames)  # type: ignore

        return list(reader)
