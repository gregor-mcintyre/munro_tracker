"""Runs the DoBIH Munros and Tops CSV file to SQLite database pipeline."""

from munro_db_builder._latest_year_finder import find_latest_year_column
from munro_db_builder._munro_filterer import map_and_filter_to_munros
from munro_db_builder._sqlite_initializer import initialize
from munro_db_builder.csv.loader import (
    load_munros_and_tops_from_dobih_csv,
)


def run_pipeline() -> int:
    """Runs the CSV file to SQLite database pipeline.

    The pipeline consists of the following steps:

        1. Loads Munros and Tops from the CSV file.
        2. Finds the latest survey-year column.
        3. Maps CSV rows to the internal schema and filters to Munros based
           on the classification from the latest survey-year column.
        4. Initializes a new SQLite database of Munros.

    Returns:
        The number of rows written to the database.
    """
    munros_and_tops_csv_rows = load_munros_and_tops_from_dobih_csv()

    normalized_csv_column_names = munros_and_tops_csv_rows[0].keys()
    latest_year_column = find_latest_year_column(normalized_csv_column_names)

    munros = map_and_filter_to_munros(
        munros_and_tops_csv_rows,
        latest_year_column=latest_year_column,
    )

    return initialize(munros)
