"""Utility for loading the DoBIH Munros and Tops CSV file."""

import csv
from pathlib import Path

from munro_db_builder.csv_normalizers import normalize_column_names
import paths


def load_munros_and_tops_from_dobih_csv(
    path: Path = paths.DOBIH_MUNROS_CSV_FILE,
) -> list[dict[str, str]]:
    """Loads Munros and Tops from a CSV file.

    Opens the file with the `cp1252` encoding since it appears DoBIH
    have published the file with this encoding (common for Microsoft
    Excel on Windows).

    Normalizes column names where necessary.

    Args:
        path: The path to the CSV file to read.

    Returns:
        The Munros and Tops loaded from the CSV file.
    """
    with path.open(newline="", encoding="cp1252") as file:
        reader = csv.DictReader(file)

        reader.fieldnames = normalize_column_names(
            reader.fieldnames  # type: ignore
        )

        return list(reader)
