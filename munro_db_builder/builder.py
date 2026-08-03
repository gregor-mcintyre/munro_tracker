"""Builds the SQLite database.

Populates the database with Munros filtered from the DoBIH Munros and
Tops CSV file.
"""

from collections.abc import Iterable
from contextlib import closing
from pathlib import Path
import sqlite3

from munro_db_builder.mapper import MappedRow
import paths


def _delete_existing(path: Path) -> None:
    """Deletes the file at `path`, if it exists.

    Args:
        path: The path to the file to be deleted.
    """
    if path.exists():
        path.unlink()


def _create_table(connection: sqlite3.Connection) -> None:
    """Creates the `munro` table.

    Args:
        connection: An open SQLite connection to create the table on.
    """
    connection.execute("""
        CREATE TABLE munro (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            height_ft INTEGER NOT NULL
        )
        """)


def _populate(
    connection: sqlite3.Connection,
    mapped_rows: Iterable[MappedRow],
) -> None:
    """Populates the `munro` table with Munros filtered from the CSV file.

    All rows are inserted in bulk as a single transaction.

    Args:
        connection: An open SQLite connection to insert the rows on.
        mapped_rows: Rows mapped to the internal schema.
    """
    connection.executemany(
        """
        INSERT INTO munro (id, name, height_ft)
        VALUES (?, ?, ?)
        """,
        ((row["id"], row["name"], row["height_ft"]) for row in mapped_rows),
    )


def build(
    mapped_rows: Iterable[MappedRow],
    path: Path = paths.MUNRO_SQLITE_DB,
) -> None:
    """Builds a new SQLite database file for Munros.

    Executes the following steps:

    1. Deletes any existing file at `db_path`.
    2. Opens a connection to `db_path`, creating the database file.
    3. Creates the `munro` table.
    4. Inserts Munros filtered from the CSV file, as a single transaction.
    5. Commits the transaction and closes the connection.

    Args:
        mapped_rows: Rows mapped to the internal schema.
        path: The path to where the SQLite database file should be built.
    """
    _delete_existing(path)

    with (
        closing(sqlite3.connect(path)) as connection,
        connection,
    ):
        _create_table(connection)
        _populate(connection, mapped_rows)
