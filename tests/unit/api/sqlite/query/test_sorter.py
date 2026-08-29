from unittest.mock import patch

from sqlalchemy import asc, desc

from api.request_params import MunroSortBy, SortOrder
from api.sqlite.models import Munro
from api.sqlite.query._sorter import (
    _apply_sort_direction,
    _resolve_sorted_column,
    sort_munros,
)
from tests import paths

_MODULE_PATH = paths.api.sqlite.query.PACKAGE + "._sorter"


class TestApplySortDirection:
    def test_column_ordered_ascending_when_sort_order_is_ascending(self):
        assert _apply_sort_direction(Munro.name, SortOrder.ASC).compare(asc(Munro.name))

    def test_column_ordered_descending_when_sort_order_is_descending(self):
        assert _apply_sort_direction(Munro.name, SortOrder.DESC).compare(
            desc(Munro.name)
        )


@patch(_MODULE_PATH + "._apply_sort_direction")
class TestResolveSortedColumn:
    def test_name_column_used_when_sorting_by_name(self, mock_apply_sort_direction):
        sort_order = SortOrder.ASC

        result = _resolve_sorted_column(MunroSortBy.NAME, sort_order)

        mock_apply_sort_direction.assert_called_once_with(Munro.name, sort_order)
        assert result is mock_apply_sort_direction.return_value

    def test_height_ft_column_used_when_sorting_by_height(
        self,
        mock_apply_sort_direction,
    ):
        sort_order = SortOrder.DESC

        result = _resolve_sorted_column(MunroSortBy.HEIGHT_FT, sort_order)

        mock_apply_sort_direction.assert_called_once_with(Munro.height_ft, sort_order)
        assert result is mock_apply_sort_direction.return_value


@patch(_MODULE_PATH + "._resolve_sorted_column")
class TestSortMunros:
    def test_resolves_sorted_column_with_sort_by_and_sort_order(
        self,
        mock_resolve_sorted_column,
        mock_sqlalchemy_query,
    ):
        sort_by = MunroSortBy.HEIGHT_FT
        sort_order = SortOrder.DESC

        sort_munros(mock_sqlalchemy_query, sort_by=sort_by, sort_order=sort_order)

        mock_resolve_sorted_column.assert_called_once_with(sort_by, sort_order)

    def test_returned_query_is_ordered_by_sorted_column(
        self,
        mock_resolve_sorted_column,
        mock_sqlalchemy_query,
    ):
        result = sort_munros(
            mock_sqlalchemy_query,
            sort_by=MunroSortBy.HEIGHT_FT,
            sort_order=SortOrder.DESC,
        )

        mock_query_with_order_by = mock_sqlalchemy_query.order_by

        mock_query_with_order_by.assert_called_once_with(
            mock_resolve_sorted_column.return_value
        )

        assert result is mock_query_with_order_by.return_value
