"""Builds a SQLite database of Munros from the DoBIH Munros and Tops CSV file.

The pipeline for building the database consists of the following steps:

    1. Loads Munros and Tops from the CSV file.
    2. Filters to Munros based on the classification from the latest survey-year column.
    3. Initializes a new SQLite database of Munros.
"""

import logging

from munro_db_builder import orchestrator
import paths


def main() -> None:
    """Runs `orchestrator.run_pipeline` and logs."""
    logging.basicConfig(level=logging.INFO)

    rows_written = orchestrator.run_pipeline(
        csv_path=paths.DOBIH_MUNROS_CSV_FILE,
        db_path=paths.MUNRO_SQLITE_DB,
    )

    logging.info("Wrote %d Munros to the SQLite database.", rows_written)


if __name__ == "__main__":
    main()
