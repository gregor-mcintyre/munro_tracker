from pathlib import Path
from unittest.mock import patch

import pytest

from munro_db_builder.munros_and_tops_loader import (
    load_munros_and_tops_from_dobih_csv,
)
from tests.helpers import MUNRO_DB_BUILDER_PACKAGE_PATH


@pytest.fixture
def _temporary_csv_file(tmp_path) -> Path:
    """Returns the path to a temporary CSV file.

    Args:
        tmp_path: The path to the temporary directory for a test invocation.

    Returns:
        The path to the temporary CSV file.
    """
    return tmp_path / "test.csv"


def _write_to_file_using_cp1252(path: Path, content: str) -> None:
    """Writes content to the file at the provided path.

    Uses the `cp1252` encoding.

    Args:
        path: The path to the file to write to.
        content: The content to write to the file.
    """
    path.write_text(content, encoding="cp1252", newline="")


class TestLoadMunrosAndTopsFromDoBIHCSV:
    def test_missing_file_raises_file_not_found_error(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load_munros_and_tops_from_dobih_csv(tmp_path / "does_not_exist")

    @patch(
        MUNRO_DB_BUILDER_PACKAGE_PATH
        + ".munros_and_tops_loader.normalize_column_names"
    )
    def test_normalize_column_names_is_called_with_correct_column_names(
        self,
        mock_normalize_column_names,
        _temporary_csv_file,
    ):
        _write_to_file_using_cp1252(
            _temporary_csv_file,
            "name,height\nmunro_1,1",
        )

        load_munros_and_tops_from_dobih_csv(_temporary_csv_file)

        mock_normalize_column_names.assert_called_once_with(["name", "height"])

    def test_special_chars_from_cp1252_encoded_file_are_read_properly(
        self,
        _temporary_csv_file,
    ):
        _write_to_file_using_cp1252(_temporary_csv_file, "name,height\n’,1")

        result = load_munros_and_tops_from_dobih_csv(_temporary_csv_file)

        assert result[0]["name"] == "’"

    def test_munros_and_tops_returned(self, _temporary_csv_file):
        _write_to_file_using_cp1252(
            _temporary_csv_file,
            "name,height\nmunro_1,1\ntop_1,2",
        )

        result = load_munros_and_tops_from_dobih_csv(_temporary_csv_file)

        expected = [
            {"name": "munro_1", "height": "1"},
            {"name": "top_1", "height": "2"},
        ]

        assert result == expected
