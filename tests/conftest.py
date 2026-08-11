"""Fixtures shared across the test suite."""

from collections.abc import Callable
from pathlib import Path
from typing import cast

import pytest

import paths
from tests.helpers import REALISTIC_DOBIH_CSV_FILE_CONTENT


def _create_temporary_path_fixture(
    actual_path: Path,
    *,
    name: str,
) -> Callable[..., Path]:
    """Creates a `pytest` fixture for providing a temporary path.

    Args:
        actual_path: The actual path to base the temporary path's parent-directory and
            filename on.
        name: The name to register the fixture under. Must match the variable it's
            assigned to, since `pytest` identifies fixtures by this name, not by the
            name of the variable it's assigned to.

    Returns:
        `_temporary_path` decorated as a fixture named `name`.
    """

    @pytest.fixture(name=name)
    def _temporary_path(tmp_path: Path) -> Path:
        """Provides a temporary path.

        Bases the temporary path on the parent-directory and filename of `actual_path`,
        ensuring the parent-directory exists.

        Args:
            tmp_path: The path to the temporary directory for a test invocation.

        Returns:
            A temporary path with the same parent-directory and filename as
            `actual_path`.
        """
        path = tmp_path / actual_path.parent.name / actual_path.name
        path.parent.mkdir(parents=True, exist_ok=True)

        return path

    return cast(Callable[..., Path], _temporary_path)


temporary_dobih_csv_file_path = _create_temporary_path_fixture(
    paths.DOBIH_MUNROS_CSV_FILE,
    name="temporary_dobih_csv_file_path",
)

temporary_munro_sqlite_db_file_path = _create_temporary_path_fixture(
    paths.MUNRO_SQLITE_DB,
    name="temporary_munro_sqlite_db_file_path",
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
