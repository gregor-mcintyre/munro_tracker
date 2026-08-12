from pathlib import Path
from unittest.mock import patch

import pytest

from munro_db_builder.csv.loader import load_munros_and_tops_from_dobih_csv
from tests.helpers import MUNRO_DB_BUILDER_PACKAGE_PATH


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

    @patch(MUNRO_DB_BUILDER_PACKAGE_PATH + ".csv.loader.normalize_column_names")
    def test_normalize_column_names_is_called_with_correct_column_names(
        self,
        mock_normalize_column_names,
        temporary_dobih_csv_file_path,
    ):
        _write_to_file_using_cp1252(
            temporary_dobih_csv_file_path,
            "name,height\nmunro_1,1",
        )

        load_munros_and_tops_from_dobih_csv(temporary_dobih_csv_file_path)

        mock_normalize_column_names.assert_called_once_with(["name", "height"])

    def test_special_chars_from_cp1252_encoded_file_are_read_properly(
        self,
        temporary_dobih_csv_file_path,
    ):
        _write_to_file_using_cp1252(temporary_dobih_csv_file_path, "name,height\n’,1")

        result = load_munros_and_tops_from_dobih_csv(temporary_dobih_csv_file_path)

        assert result[0]["name"] == "’"

    def test_munros_and_tops_returned(self, temporary_dobih_csv_file_path):
        _write_to_file_using_cp1252(
            temporary_dobih_csv_file_path,
            "name,height\nmunro_1,1\ntop_1,2",
        )

        result = load_munros_and_tops_from_dobih_csv(temporary_dobih_csv_file_path)

        expected = [
            {"name": "munro_1", "height": "1"},
            {"name": "top_1", "height": "2"},
        ]

        assert result == expected
