"""Integration tests for `initialize`.

Exercises the `_delete_existing`, `_create_table`, and `_populate` collaboration with a
temporary SQLite database file.
"""

from pathlib import Path

from munro_db_builder._sqlite_initializer import initialize
from tests.csv_to_sqlite_test_data import REALISTIC_MAPPED_MUNRO_ROWS
from tests.integration._sqlite_assertion import (
    assert_munros_persisted_to_sqlite_database,
)


def _run_initialize_and_assert_munros_persisted_to_database(*, path: Path) -> None:
    """Runs `initialize` and asserts the expected Munros were persisted to disk.

    Calls `initialize` with the path to the temporary SQLite Munro database file and
    realistic examples of rows mapped to the internal schema that are classified as
    Munros.

    Then calls `assert_munros_persisted_to_database`.

    Args:
        path: The path to the database file.
    """
    result = initialize(path=path, mapped_rows=REALISTIC_MAPPED_MUNRO_ROWS)

    assert_munros_persisted_to_sqlite_database(
        path=path,
        sqlite_initialization_result=result,
    )


class TestInitialize:
    def test_existing_database_is_replaced(self, temporary_munro_sqlite_db_file_path):
        temporary_munro_sqlite_db_file_path.write_text("")  # Create existing db file

        _run_initialize_and_assert_munros_persisted_to_database(
            path=temporary_munro_sqlite_db_file_path,
        )

    def test_all_munros_persisted_to_database(
        self,
        temporary_munro_sqlite_db_file_path,
    ):
        _run_initialize_and_assert_munros_persisted_to_database(
            path=temporary_munro_sqlite_db_file_path,
        )
