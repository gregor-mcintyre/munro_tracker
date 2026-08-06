"""Fixtures shared across the test suite."""

from pathlib import Path

import pytest

import paths
from tests.helpers import REALISTIC_DOBIH_CSV_FILE_CONTENT


@pytest.fixture
def temporary_dobih_csv_file_path(tmp_path: Path) -> Path:
    """Returns the path to a temporary DoBIH Munros and Tops CSV file.

    Ensures the parent directory exists.

    Args:
        tmp_path: The path to the temporary directory for a test invocation.

    Returns:
        The path to the temporary CSV file.
    """
    actual_dobih_csv_file_path = paths.DOBIH_MUNROS_CSV_FILE

    path = (
        tmp_path
        / actual_dobih_csv_file_path.parent.name
        / actual_dobih_csv_file_path.name
    )

    path.parent.mkdir(parents=True, exist_ok=True)

    return path


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
