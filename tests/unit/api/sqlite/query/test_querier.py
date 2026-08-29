from unittest.mock import patch

from api.request_params import MunroSortBy, SortOrder
from api.sqlite.models import Munro
from api.sqlite.query.querier import query_munro_by_dobih_number, query_munros
from tests import paths

_MODULE_PATH = paths.api.sqlite.query.PACKAGE + ".querier"


@patch(_MODULE_PATH + ".sort_munros")
@patch(_MODULE_PATH + ".filter_munros")
class TestQueryMunros:
    def test_queries_the_munro_table(
        self,
        mock_filter_munros,
        mock_sort_munros,
        mock_sqlalchemy_session,
    ):
        query_munros(
            mock_sqlalchemy_session,
            min_height_ft=None,
            max_height_ft=None,
            name=None,
            sort_by=MunroSortBy.HEIGHT_FT,
            sort_order=SortOrder.DESC,
            limit=10,
            offset=0,
        )

        mock_sqlalchemy_session.query.assert_called_once_with(Munro)

    def test_filters_the_query(
        self,
        mock_filter_munros,
        mock_sort_munros,
        mock_sqlalchemy_session,
    ):
        min_height_ft = 0
        max_height_ft = 1
        name = "Test"

        query_munros(
            mock_sqlalchemy_session,
            min_height_ft=min_height_ft,
            max_height_ft=max_height_ft,
            name=name,
            sort_by=MunroSortBy.HEIGHT_FT,
            sort_order=SortOrder.DESC,
            limit=10,
            offset=0,
        )

        mock_filter_munros.assert_called_once_with(
            mock_sqlalchemy_session.query.return_value,
            min_height_ft=min_height_ft,
            max_height_ft=max_height_ft,
            name=name,
        )

    def test_sorts_the_filtered_query(
        self,
        mock_filter_munros,
        mock_sort_munros,
        mock_sqlalchemy_session,
    ):
        sort_by = MunroSortBy.HEIGHT_FT
        sort_order = SortOrder.DESC

        query_munros(
            mock_sqlalchemy_session,
            min_height_ft=None,
            max_height_ft=None,
            name=None,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=10,
            offset=0,
        )

        mock_sort_munros.assert_called_once_with(
            mock_filter_munros.return_value,
            sort_by=sort_by,
            sort_order=sort_order,
        )

    def test_paginates_and_returns_query_result(
        self,
        mock_filter_munros,
        mock_sort_munros,
        mock_sqlalchemy_session,
    ):
        limit = 10
        offset = 5

        result = query_munros(
            mock_sqlalchemy_session,
            min_height_ft=None,
            max_height_ft=None,
            name=None,
            sort_by=MunroSortBy.HEIGHT_FT,
            sort_order=SortOrder.DESC,
            limit=limit,
            offset=offset,
        )

        mock_query_with_offset = mock_sort_munros.return_value.offset
        mock_query_with_limit = mock_query_with_offset.return_value.limit
        mock_query_with_all = mock_query_with_limit.return_value.all

        mock_query_with_offset.assert_called_once_with(offset)
        mock_query_with_limit.assert_called_once_with(limit)
        mock_query_with_all.assert_called_once_with()

        assert result is mock_query_with_all.return_value


def test_query_munro_by_dobih_number_returns_sqlite_session_get_result(
    mock_sqlalchemy_session,
):
    dobih_number = 1

    result = query_munro_by_dobih_number(mock_sqlalchemy_session, dobih_number)

    mock_sqlalchemy_session_get = mock_sqlalchemy_session.get

    mock_sqlalchemy_session_get.assert_called_once_with(Munro, dobih_number)
    assert result is mock_sqlalchemy_session_get.return_value
