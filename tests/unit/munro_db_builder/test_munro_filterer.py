from unittest.mock import call, patch

from munro_db_builder._mapper import MappedRow
from munro_db_builder._munro_filterer import (
    _filter_to_munros,
    _is_munro,
    map_and_filter_to_munros,
)
from tests.helpers import MUNRO_DB_BUILDER_PACKAGE_PATH

_MODULE_PATH = MUNRO_DB_BUILDER_PACKAGE_PATH + "._munro_filterer"


class TestIsMunro:
    def test_unclassified_returns_false(self):
        assert _is_munro({"classification": ""}) is False

    def test_top_returns_false(self):
        assert _is_munro({"classification": "TOP"}) is False

    def test_munro_returns_true(self):
        assert _is_munro({"classification": "MUN"}) is True


@patch(_MODULE_PATH + "._is_munro")
class TestFilterToMunros:
    _MAPPED_ROWS: list[MappedRow] = [{"id": 1}, {"id": 2}]

    def test_no_munros_returns_empty(self, mock_is_munro):
        mock_is_munro.return_value = False

        result = _filter_to_munros(self._MAPPED_ROWS)

        assert list(result) == []

    def test_mix_returns_only_munros(self, mock_is_munro):
        mock_is_munro.side_effect = [False, True]

        result = _filter_to_munros(self._MAPPED_ROWS)

        assert list(result) == [{"id": 2}]

    def test_all_munros_returns_all(self, mock_is_munro):
        mock_is_munro.return_value = True

        result = _filter_to_munros(self._MAPPED_ROWS)

        assert list(result) == self._MAPPED_ROWS


@patch(_MODULE_PATH + ".map_to_internal_schema_and_add_classification")
class TestMapAndFilterToMunros:
    _CSV_ROWS = [{"DoBIH Number": "1"}, {"DoBIH Number": "2"}]

    def test_map_function_called_correctly(self, mock_map):
        list(map_and_filter_to_munros(self._CSV_ROWS, latest_year_column="1"))

        assert mock_map.call_args_list == [
            call({"DoBIH Number": "1"}, latest_year_column="1"),
            call({"DoBIH Number": "2"}, latest_year_column="1"),
        ]

    @patch(_MODULE_PATH + "._filter_to_munros")
    def test_calls_filter_to_munros_and_returns_its_result(
        self,
        mock_filter_to_munros,
        mock_map,
    ):
        def _map_row_side_effect(row, latest_year_column):
            return f"mapped_row_{row['DoBIH Number']}"

        mock_map.side_effect = _map_row_side_effect

        result = map_and_filter_to_munros(self._CSV_ROWS, latest_year_column="1")

        assert list(mock_filter_to_munros.call_args.args[0]) == [
            "mapped_row_1",
            "mapped_row_2",
        ]
        assert result is mock_filter_to_munros.return_value
