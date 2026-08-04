from unittest.mock import call, patch

from munro_db_builder._mapper import (
    _map_to_internal_schema,
    _normalize_field_value,
    map_to_internal_schema_and_add_classification,
)
from tests.helpers import MUNRO_DB_BUILDER_PACKAGE_PATH

_MODULE_PATH = MUNRO_DB_BUILDER_PACKAGE_PATH + "._mapper"


class TestNormalizeFieldValue:
    _RAW_VALUE = "test"

    def test_name_field_returns_raw_value_unchanged(self):
        result = _normalize_field_value(
            field_name="name",
            raw_value=self._RAW_VALUE,
        )

        assert result is self._RAW_VALUE

    @patch(_MODULE_PATH + ".normalize_int")
    def test_other_field_returns_normalize_int_result(
        self,
        mock_normalize_int,
    ):
        result = _normalize_field_value(
            field_name="other",
            raw_value=self._RAW_VALUE,
        )

        mock_normalize_int.assert_called_once_with(self._RAW_VALUE)

        assert result == mock_normalize_int.return_value


@patch(_MODULE_PATH + "._normalize_field_value")
class TestMapToInternalSchema:
    _CSV_ROW = {"DoBIH Number": "1", "Name": "2", "Height (ft)": "3"}

    def test_calls_normalize_field_value_per_column(
        self,
        mock_normalize_field_value,
    ):
        _map_to_internal_schema(self._CSV_ROW)

        assert mock_normalize_field_value.call_args_list == [
            call(field_name="id", raw_value="1"),
            call(field_name="name", raw_value="2"),
            call(field_name="height_ft", raw_value="3"),
        ]

    def test_columns_not_in_internal_schema_are_omitted(self, _):
        csv_row = self._CSV_ROW | {
            "not_include_1": "4",
            "not_include_2": "5",
        }

        result = _map_to_internal_schema(csv_row)

        assert result.keys() == {"id", "name", "height_ft"}

    def test_returns_csv_row_mapped_to_internal_schema(
        self,
        mock_normalize_field_value,
    ):
        mock_normalize_field_value.side_effect = [1, "2", 3]

        result = _map_to_internal_schema(self._CSV_ROW)

        assert result == {"id": 1, "name": "2", "height_ft": 3}


@patch(_MODULE_PATH + "._map_to_internal_schema")
class TestMapToInternalSchemaAndAddClassification:
    _CSV_ROW = {"1": "MUN"}

    def test_calls_map_to_internal_schema_with_csv_row(
        self,
        mock_map_to_internal_schema,
    ):
        map_to_internal_schema_and_add_classification(
            self._CSV_ROW,
            latest_year_column="1",
        )

        mock_map_to_internal_schema.assert_called_once_with(self._CSV_ROW)

    def test_returns_row_mapped_to_internal_schema_with_classification_added(
        self,
        mock_map_to_internal_schema,
    ):
        mock_map_to_internal_schema.return_value = {
            "id": 1,
            "name": "2",
            "height_ft": 3,
        }

        result = map_to_internal_schema_and_add_classification(
            self._CSV_ROW,
            latest_year_column="1",
        )

        assert result == {
            "id": 1,
            "name": "2",
            "height_ft": 3,
            "classification": "MUN",
        }
