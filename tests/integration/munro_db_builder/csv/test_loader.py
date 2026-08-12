"""Integration tests for `load_munros_and_tops_from_dobih_csv`.

Exercises the `normalize_column_names` and `_normalize_height_ft` collaboration with a
real CSV file.
"""

import pytest

from munro_db_builder.csv.loader import load_munros_and_tops_from_dobih_csv
from tests.helpers import REALISTIC_DOBIH_CSV_ROWS


@pytest.mark.usefixtures("write_realistic_content_to_temporary_dobih_csv_file")
class TestCSVLoadingAndNormalizing:
    def test_height_ft_column_name_is_normalized(
        self,
        temporary_dobih_csv_file_path,
    ):
        result = load_munros_and_tops_from_dobih_csv(temporary_dobih_csv_file_path)

        first_row = result[0]

        assert "Height (ft)" in first_row and "Height\n(ft)" not in first_row

    def test_cp1252_special_character_is_decoded_correctly(
        self,
        temporary_dobih_csv_file_path,
    ):
        result = load_munros_and_tops_from_dobih_csv(temporary_dobih_csv_file_path)

        assert result[4]["Comments"] == (
            "on the O.S. name Stùc Gharbh Mhòr, corresponds to the 3625' spot"
        )

    def test_full_csv_file_is_loaded_as_expected(
        self,
        temporary_dobih_csv_file_path,
    ):
        result = load_munros_and_tops_from_dobih_csv(temporary_dobih_csv_file_path)

        assert result == REALISTIC_DOBIH_CSV_ROWS
