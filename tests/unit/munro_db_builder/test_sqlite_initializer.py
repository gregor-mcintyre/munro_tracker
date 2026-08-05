from collections.abc import Callable, Iterator
from pathlib import Path
import sqlite3
from typing import Literal, cast
from unittest.mock import patch

import pytest

from munro_db_builder._mapper import MappedRow
from munro_db_builder._sqlite_initializer import (
    _create_table,
    _delete_existing,
    _populate,
    initialize,
)
from tests.helpers import MUNRO_DB_BUILDER_PACKAGE_PATH

_MODULE_PATH = MUNRO_DB_BUILDER_PACKAGE_PATH + "._sqlite_initializer"

type _FixtureScope = Literal["session", "package", "module", "class", "function"]


@pytest.fixture
def _path_to_temporary_sqlite_db_file(tmp_path: Path) -> Path:
    """Returns the path to a temporary SQLite database file.

    Args:
        tmp_path: The path to the temporary directory for a test invocation.

    Returns:
        The path to the temporary SQLite database file.
    """
    return tmp_path / "test.db"


def _create_connection_fixture(
    scope: _FixtureScope = "class",
) -> Callable[..., Iterator[sqlite3.Connection]]:
    """Creates a `pytest` fixture for providing an open in-memory connection.

    Args:
        scope: The scope to apply to the fixture.

    Returns:
        `_connection` decorated as a fixture scoped to `scope`.
    """

    @pytest.fixture(scope=scope)
    def _connection(self) -> Iterator[sqlite3.Connection]:
        """Provides an open in-memory SQLite connection.

        Args:
            self: The test class instance. Unused, but required for
                binding as a class attribute.

        Yields:
            An open connection to an in-memory SQLite database.
        """
        connection = sqlite3.connect(":memory:")

        try:
            yield connection
        finally:
            connection.close()

    return cast(Callable[..., Iterator[sqlite3.Connection]], _connection)


@pytest.fixture
def _mapped_rows() -> list[MappedRow]:
    """Sample rows mapped to the internal schema."""
    return [
        {"id": 1, "name": "Munro 1", "height_ft": 3},
        {"id": 2, "name": "Munro 2", "height_ft": 4},
    ]


class TestDeleteExisting:
    def test_missing_file_does_not_raise(self, _path_to_temporary_sqlite_db_file):
        _delete_existing(_path_to_temporary_sqlite_db_file)

        assert not _path_to_temporary_sqlite_db_file.exists()

    def test_existing_file_is_deleted(self, _path_to_temporary_sqlite_db_file):
        _path_to_temporary_sqlite_db_file.write_text("")

        _delete_existing(_path_to_temporary_sqlite_db_file)

        assert not _path_to_temporary_sqlite_db_file.exists()


class TestCreateTable:
    _connection = _create_connection_fixture()

    @pytest.fixture(scope="class")
    def _run_create_table_and_get_column_metadata(
        self,
        _connection,
    ) -> list[tuple[str, str, bool, bool]]:
        """Runs `_create_table` and gets column metadata for the `munro` table.

        Args:
            _connection: An open connection to an in-memory SQLite database.

        Returns:
            For each column in the `munro` table within the `munro` database created by
            `_create_table`:
                - Column name.
                - Data type.
                - `True` if there is a NOT NULL constraint, otherwise `False`.
                - `True` if the column is part of the PRIMARY KEY, otherwise `False`.
        """
        _create_table(_connection)

        return [
            (name, data_type, bool(not_null), bool(pk))
            for _, name, data_type, not_null, _, pk in _connection.execute(
                "PRAGMA table_info(munro)"
            )
        ]

    def test_creates_munro_table(
        self,
        _connection,
        _run_create_table_and_get_column_metadata,
    ):
        result = _connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name='munro'
            """).fetchall()

        assert result == [("munro",)]

    def test_creates_expected_columns(self, _run_create_table_and_get_column_metadata):
        metadata = _run_create_table_and_get_column_metadata
        column_names = [name for name, _, _, _ in metadata]

        assert column_names == ["id", "name", "height_ft"]

    def test_columns_are_expected_data_type(
        self,
        _run_create_table_and_get_column_metadata,
    ):
        metadata = _run_create_table_and_get_column_metadata
        column_data_types = {name: data_type for name, data_type, _, _ in metadata}

        assert column_data_types == {
            "id": "INTEGER",
            "name": "TEXT",
            "height_ft": "INTEGER",
        }

    def test_id_column_is_the_primary_key(
        self,
        _run_create_table_and_get_column_metadata,
    ):
        name_to_pk_map = {
            name: pk for name, _, _, pk in _run_create_table_and_get_column_metadata
        }

        assert name_to_pk_map == {"id": True, "name": False, "height_ft": False}

    def test_name_and_height_ft_columns_are_not_null(
        self,
        _run_create_table_and_get_column_metadata,
    ):
        metadata = _run_create_table_and_get_column_metadata
        name_to_not_null_map = {
            name: not_null
            for name, _, not_null, _ in metadata
            if name in ("name", "height_ft")
        }

        assert name_to_not_null_map == {"name": True, "height_ft": True}


class TestPopulate:
    _connection = _create_connection_fixture(scope="function")

    @pytest.fixture
    def _create_munro_table(self, _connection) -> None:
        """Creates the `munro` table.

        Args:
            _connection: An open connection to an in-memory SQLite database.
        """
        _connection.execute("""
            CREATE TABLE munro (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                height_ft INTEGER NOT NULL
            )
            """)

    def test_inserted_rows_match_mapped_rows(
        self,
        _connection,
        _create_munro_table,
        _mapped_rows,
    ):
        _populate(_connection, _mapped_rows)

        _connection.row_factory = sqlite3.Row
        query_result = _connection.execute("SELECT * FROM munro").fetchall()
        dict_rows = [dict(row) for row in query_result]

        assert dict_rows == _mapped_rows

    def test_returns_number_of_rows_written(
        self,
        _connection,
        _create_munro_table,
        _mapped_rows,
    ):
        result = _populate(_connection, _mapped_rows)

        assert result == len(_mapped_rows)


@patch(_MODULE_PATH + "._populate")
@patch(_MODULE_PATH + "._create_table")
@patch(_MODULE_PATH + ".sqlite3.connect")
@patch(_MODULE_PATH + "._delete_existing")
class TestInitialize:
    _connection = _create_connection_fixture()

    def test_calls_dependencies_with_expected_arguments(
        self,
        mock_delete_existing,
        mock_sqlite3_connect,
        mock_create_table,
        mock_populate,
        _connection,
        _mapped_rows,
        _path_to_temporary_sqlite_db_file,
    ):
        mock_sqlite3_connect.return_value = _connection

        initialize(_mapped_rows, _path_to_temporary_sqlite_db_file)

        mock_delete_existing.assert_called_once_with(_path_to_temporary_sqlite_db_file)
        mock_sqlite3_connect.assert_called_once_with(_path_to_temporary_sqlite_db_file)
        mock_create_table.assert_called_once_with(_connection)
        mock_populate.assert_called_once_with(_connection, _mapped_rows)

    def test_returns_number_of_rows_written_from_populate(
        self,
        mock_delete_existing,
        mock_sqlite3_connect,
        mock_create_table,
        mock_populate,
        _connection,
        _mapped_rows,
        _path_to_temporary_sqlite_db_file,
    ):
        result = initialize(_mapped_rows, _path_to_temporary_sqlite_db_file)

        assert result is mock_populate.return_value

    def test_closes_connection_after_use(
        self,
        mock_delete_existing,
        mock_sqlite3_connect,
        mock_create_table,
        mock_populate,
        _connection,
        _mapped_rows,
        _path_to_temporary_sqlite_db_file,
    ):
        initialize(_mapped_rows, _path_to_temporary_sqlite_db_file)

        with pytest.raises(sqlite3.ProgrammingError):
            _connection.execute("SELECT 1")
