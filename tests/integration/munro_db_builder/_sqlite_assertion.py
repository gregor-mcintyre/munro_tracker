"""Helpers shared across the test suite."""

from pathlib import Path
import sqlite3
from typing import cast

from tests.integration.munro_db_builder._csv_to_sqlite_test_data import (
    REALISTIC_MAPPED_MUNRO_ROWS,
)

type MunroSQLiteDBRows = list[dict[str, int | str]]

# Expected rows in the `munro` table of the SQLite database for Munros.
# Mapped to `REALISTIC_MAPPED_MUNRO_ROWS`.
EXPECTED_MUNRO_SQLITE_DB_ROWS: MunroSQLiteDBRows = [
    {"dobih_number": 1, "name": "Ben Chonzie", "height_ft": 3054},
    {"dobih_number": 1301, "name": "Ben More", "height_ft": 3169},
    {"dobih_number": 2925, "name": "Beinn a' Chroin", "height_ft": 3089},
]


def _read_munro_rows_from_sqlite_database(*, path: Path) -> MunroSQLiteDBRows:
    """Reads all rows from the `munro` table of a SQLite database file.

    Creates and uses a new connection so that it can be proved that data was persisted
    to disk.

    Args:
        path: The path to the database file to read from.

    Returns:
        Each row in the `munro` table.
    """
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row

    try:
        query_result = connection.execute("SELECT * FROM munro").fetchall()

        return cast(MunroSQLiteDBRows, [dict(row) for row in query_result])
    finally:
        connection.close()


def assert_munros_persisted_to_sqlite_database(
    *,
    path: Path,
    sqlite_initialization_result: int,
) -> None:
    """Asserts the expected Munros were persisted to the SQLite Munro database.

    Asserts the SQLite initialization result equals the number of realistic examples of
    rows mapped to the internal schema that are classified as Munros, and the rows in
    the SQLite database are the expected rows.

    Args:
        path: The path to the database file to read from.
        sqlite_initialization_result: The value returned by the operation that
            initializes the SQLite database.
    """
    assert sqlite_initialization_result == len(REALISTIC_MAPPED_MUNRO_ROWS)
    assert _read_munro_rows_from_sqlite_database(path=path) == (
        EXPECTED_MUNRO_SQLITE_DB_ROWS
    )
