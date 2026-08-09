"""Integration tests for `map_to_internal_schema_and_add_classification`.

Exercises the `_map_to_internal_schema`, `_normalize_field_value`, and `normalize_int`
collaboration with realistic CSV rows.
"""

from munro_db_builder._latest_year_finder import find_latest_year_column
from munro_db_builder._mapper import map_to_internal_schema_and_add_classification
from tests.helpers import REALISTIC_DOBIH_CSV_ROWS, REALISTIC_MAPPED_ROWS

_REALISTIC_CSV_COLUMN_NAMES = REALISTIC_DOBIH_CSV_ROWS[0].keys()
_LATEST_YEAR_COLUMN = find_latest_year_column(_REALISTIC_CSV_COLUMN_NAMES)


class TestMapToInternalSchemaAndAddClassification:
    def test_row_with_differently_formatted_columns_to_hill_rows(self):
        result = map_to_internal_schema_and_add_classification(
            REALISTIC_DOBIH_CSV_ROWS[5],
            latest_year_column=_LATEST_YEAR_COLUMN,
        )

        assert result == REALISTIC_MAPPED_ROWS[5]

    def test_hill_row_with_blank_latest_year_classification_maps_to_empty_string(
        self,
    ):
        result = map_to_internal_schema_and_add_classification(
            REALISTIC_DOBIH_CSV_ROWS[4],
            latest_year_column=_LATEST_YEAR_COLUMN,
        )

        assert result == REALISTIC_MAPPED_ROWS[4]

    def test_loaded_csv_rows_map_to_internal_schema_and_have_a_classification(self):
        result = [
            map_to_internal_schema_and_add_classification(
                csv_row,
                latest_year_column=_LATEST_YEAR_COLUMN,
            )
            for csv_row in REALISTIC_DOBIH_CSV_ROWS
        ]

        assert result == REALISTIC_MAPPED_ROWS
