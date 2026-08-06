"""Integration tests for loading and normalizing the DoBIH Munros and Tops CSV file."""

import pytest

from munro_db_builder.csv.loader import load_munros_and_tops_from_dobih_csv
from munro_db_builder.csv.row_type import CSVRow

# What `load_munros_and_tops_from_dobih_csv` is expected to return after it loads
# `tests.helpers.REALISTIC_DOBIH_CSV_FILE_CONTENT` from the temporary CSV file
EXPECTED_DOBIH_CSV_ROWS: list[CSVRow] = [
    {
        "Running No": "1",
        "DoBIH Number": "1",
        "Name": "Ben Chonzie",
        "Height (m)": "931",
        "Height (ft)": "3054",
        "1891": "MUN",
        "1921": "MUN",
        "2021": "MUN",
        "Comments": "",
    },
    {
        "Running No": "17",
        "DoBIH Number": "36",
        "Name": "Beinn a' Chroin East Top",
        "Height (m)": "940.1",
        "Height (ft)": "3084",
        "1891": "MUN",
        "1921": "MUN",
        "2021": "TOP",
        "Comments": "",
    },
    {
        "Running No": "16",
        "DoBIH Number": "2925",
        "Name": "Beinn a' Chroin",
        "Height (m)": "941.4",
        "Height (ft)": "3089",
        "1891": "",
        "1921": "",
        "2021": "MUN",
        "Comments": "",
    },
    {
        "Running No": "603",
        "DoBIH Number": "1301",
        "Name": "Ben More",
        "Height (m)": "966",
        "Height (ft)": "3169",
        "1891": "MUN",
        "1921": "MUN",
        "2021": "MUN",
        "Comments": "",
    },
    {
        "Running No": "334",
        "DoBIH Number": "550",
        "Name": "Leabaidh an Daimh Bhuidhe (Ben Avon) - Stuc Gharbh Mhor (old GR)",
        "Height (m)": "1112",
        "Height (ft)": "3648",
        "1891": "TOP",
        "1921": "TOP",
        "2021": "",
        "Comments": "on the O.S. name Stùc Gharbh Mhòr, corresponds to the 3625' spot",
    },
    {
        "Running No": "",
        "DoBIH Number": "",
        "Name": "",
        "Height (m)": "",
        "Height (ft)": "",
        "1891": "283",
        "1921": "276",
        "2021": "282",
        "Comments": "",
    },
    {
        "Running No": "",
        "DoBIH Number": "",
        "Name": "",
        "Height (m)": "",
        "Height (ft)": "",
        "1891": "",
        "1921": "",
        "2021": "",
        "Comments": "",
    },
]


@pytest.mark.usefixtures("write_realistic_content_to_temporary_dobih_csv_file")
class TestCSVLoadingAndNormalizing:
    def test_height_ft_column_name_is_normalized(
        self,
        temporary_dobih_csv_file_path,
    ):
        result = load_munros_and_tops_from_dobih_csv(path=temporary_dobih_csv_file_path)

        first_row = result[0]

        assert "Height (ft)" in first_row and "Height\n(ft)" not in first_row

    def test_cp1252_special_character_is_decoded_correctly(
        self,
        temporary_dobih_csv_file_path,
    ):
        result = load_munros_and_tops_from_dobih_csv(path=temporary_dobih_csv_file_path)

        assert result[4]["Comments"] == (
            "on the O.S. name Stùc Gharbh Mhòr, corresponds to the 3625' spot"
        )

    def test_full_csv_file_is_loaded_as_expected(
        self,
        temporary_dobih_csv_file_path,
    ):
        result = load_munros_and_tops_from_dobih_csv(path=temporary_dobih_csv_file_path)

        assert result == EXPECTED_DOBIH_CSV_ROWS
