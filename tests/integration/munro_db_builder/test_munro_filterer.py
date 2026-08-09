"""Integration tests for `map_and_filter_to_munros`.

Exercises the `map_to_internal_schema_and_add_classification`, `_filter_to_munros`,
and `_is_munro` collaboration with realistic CSV rows.
"""

from munro_db_builder._latest_year_finder import find_latest_year_column
from munro_db_builder._mapper import MappedRow
from munro_db_builder._munro_filterer import map_and_filter_to_munros
from tests.helpers import REALISTIC_DOBIH_CSV_ROWS, REALISTIC_MAPPED_ROWS

_REALISTIC_CSV_COLUMN_NAMES = REALISTIC_DOBIH_CSV_ROWS[0].keys()
_LATEST_YEAR_COLUMN = find_latest_year_column(_REALISTIC_CSV_COLUMN_NAMES)

# The rows in `REALISTIC_MAPPED_ROWS` that are classified as Munros based on the latest
# survey-year
_EXPECTED_MUNRO_ROWS: list[MappedRow] = [
    REALISTIC_MAPPED_ROWS[index] for index in (0, 2, 3)
]


class TestMapAndFilterToMunros:
    def test_row_with_differently_formatted_columns_to_hill_rows_is_excluded(self):
        result = map_and_filter_to_munros(
            [REALISTIC_DOBIH_CSV_ROWS[5]],
            latest_year_column=_LATEST_YEAR_COLUMN,
        )

        assert list(result) == []

    def test_hill_row_with_blank_latest_year_classification_is_excluded(self):
        result = map_and_filter_to_munros(
            [REALISTIC_DOBIH_CSV_ROWS[4]],
            latest_year_column=_LATEST_YEAR_COLUMN,
        )

        assert list(result) == []

    def test_hill_row_with_top_classification_is_excluded(self):
        result = map_and_filter_to_munros(
            [REALISTIC_DOBIH_CSV_ROWS[1]],
            latest_year_column=_LATEST_YEAR_COLUMN,
        )

        assert list(result) == []

    def test_rows_are_mapped_and_filtered_to_munros(self):
        result = map_and_filter_to_munros(
            REALISTIC_DOBIH_CSV_ROWS,
            latest_year_column=_LATEST_YEAR_COLUMN,
        )

        assert list(result) == _EXPECTED_MUNRO_ROWS
