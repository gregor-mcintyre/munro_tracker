from unittest.mock import call, patch

from munro_db_builder.csv.normalizers import (
    _normalize_height_ft,
    normalize_column_names,
    normalize_int,
)
from tests.helpers import MUNRO_DB_BUILDER_PACKAGE_PATH


class TestNormalizeHeightFt:
    def test_height_ft_with_newline_is_normalized(self):
        assert _normalize_height_ft("Height\n(ft)") == "Height (ft)"

    def test_other_column_name_is_returned_unchanged(self):
        column_name = "Other Column Name"

        assert _normalize_height_ft(column_name) is column_name


@patch(MUNRO_DB_BUILDER_PACKAGE_PATH + ".csv.normalizers._normalize_height_ft")
class TestNormalizeColumnNames:
    def test_normalize_height_ft_called_for_every_column(
        self,
        mock_normalize_height_ft,
    ):
        normalize_column_names(["column_1", "column_2"])

        assert mock_normalize_height_ft.call_count == 2
        mock_normalize_height_ft.assert_has_calls(
            [call("column_1"), call("column_2")]
        )

    def test_returns_every_column_name_normalized(
        self,
        mock_normalize_height_ft,
    ):
        mock_normalize_height_ft.side_effect = ["normalized_1", "normalized_2"]

        result = normalize_column_names(["column_1", "column_2"])

        assert result == ["normalized_1", "normalized_2"]


class TestNormalizeInt:
    def test_empty_string_returns_none(self):
        assert normalize_int("") is None

    def test_non_numeric_string_returns_none(self):
        assert normalize_int("not_a_number") is None

    def test_numeric_string_returns_int(self):
        assert normalize_int("1") == 1
