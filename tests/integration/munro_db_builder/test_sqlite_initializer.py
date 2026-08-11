"""Integration tests for `initialize`.

Exercises the `_delete_existing`, `_create_table`, and `_populate` collaboration with a
temporary SQLite database file.
"""

from pathlib import Path
import sqlite3
from typing import cast

from munro_db_builder._sqlite_initializer import initialize
from tests.helpers import (
    EXPECTED_MUNRO_SQLITE_DB_ROWS,
    REALISTIC_MAPPED_MUNRO_ROWS,
    MunroSQLiteDBRow,
)


def _read_munros(path: Path) -> MunroSQLiteDBRow:
    """Reads rows from the `munro` table within the temporary Munro SQLite database.

    Uses a new connection to prove data was persisted.

    Args:
        path: The path to the database file to read from.

    Returns:
        Each row in the `munro` table.
    """
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row

    try:
        query_result = connection.execute("SELECT * FROM munro").fetchall()

        return cast(MunroSQLiteDBRow, [dict(row) for row in query_result])
    finally:
        connection.close()


def _run_initialize_and_assert_munros_persisted_to_database(path: Path) -> None:
    """Runs `initialize` and asserts the expected Munros were persisted.

    Calls `initialize` with realistic examples of rows mapped to the internal schema
    that are classified as Munros and the path to the temporary SQLite Munro database
    file.

    Then asserts `initialize` returns the number of rows that was passed to it, and the
    expected rows were persisted to the database.

    Args:
        path: The path to the database file.
    """
    result = initialize(REALISTIC_MAPPED_MUNRO_ROWS, path)

    assert result == len(REALISTIC_MAPPED_MUNRO_ROWS)
    assert _read_munros(path) == EXPECTED_MUNRO_SQLITE_DB_ROWS


class TestInitialize:
    def test_existing_database_is_replaced(self, temporary_munro_sqlite_db_file_path):
        temporary_munro_sqlite_db_file_path.write_text("")  # Create existing db file

        _run_initialize_and_assert_munros_persisted_to_database(
            temporary_munro_sqlite_db_file_path,
        )

    def test_all_munros_persisted_to_database(
        self,
        temporary_munro_sqlite_db_file_path,
    ):
        _run_initialize_and_assert_munros_persisted_to_database(
            temporary_munro_sqlite_db_file_path,
        )
