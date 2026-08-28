"""`pytest` fixture shared across tests in `tests.integration.munro_db_builder`."""

from pathlib import Path

import pytest

from tests.integration.munro_db_builder._csv_to_sqlite_test_data import (
    REALISTIC_DOBIH_CSV_FILE_CONTENT,
)


@pytest.fixture
def write_realistic_content_to_temporary_dobih_csv_file(
    temporary_dobih_csv_file_path: Path,
) -> None:
    """Writes realistic content to the temporary DoBIH Munros and Tops CSV file.

    Uses `encoding="cp1252"` and `newline=""` to match the real file.

    Args:
        temporary_dobih_csv_file_path: The path to the temporary CSV file.
    """
    temporary_dobih_csv_file_path.write_text(
        REALISTIC_DOBIH_CSV_FILE_CONTENT,
        encoding="cp1252",
        newline="",
    )
