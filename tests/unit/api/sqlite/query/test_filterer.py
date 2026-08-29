from unittest.mock import patch

from api.sqlite.models import Munro
from api.sqlite.query._filterer import (
    _filter_by_max_height,
    _filter_by_min_height,
    _filter_by_name,
    filter_munros,
)
from tests import paths

_MODULE_PATH = paths.api.sqlite.query.PACKAGE + "._filterer"


class TestFilterByMinHeight:
    def test_query_returned_unchanged_when_no_filter_value_provided(
        self, mock_sqlalchemy_query
    ):
        result = _filter_by_min_height(mock_sqlalchemy_query, None)

        mock_sqlalchemy_query.filter.assert_not_called()
        assert result is mock_sqlalchemy_query

    def test_query_filtered_by_minimum_height_when_filter_value_provided(
        self,
        mock_sqlalchemy_query,
    ):
        min_height_ft = 0

        result = _filter_by_min_height(mock_sqlalchemy_query, min_height_ft)

        query_filter = mock_sqlalchemy_query.filter.call_args.args[0]
        assert query_filter.compare(Munro.height_ft >= min_height_ft)

        assert result is mock_sqlalchemy_query.filter.return_value


class TestFilterByMaxHeight:
    def test_query_returned_unchanged_when_no_filter_value_provided(
        self, mock_sqlalchemy_query
    ):
        result = _filter_by_max_height(mock_sqlalchemy_query, None)

        mock_sqlalchemy_query.filter.assert_not_called()
        assert result is mock_sqlalchemy_query

    def test_query_filtered_by_maximum_height_when_filter_value_provided(
        self,
        mock_sqlalchemy_query,
    ):
        max_height_ft = 1

        result = _filter_by_max_height(mock_sqlalchemy_query, max_height_ft)

        query_filter = mock_sqlalchemy_query.filter.call_args.args[0]
        assert query_filter.compare(Munro.height_ft <= max_height_ft)

        assert result is mock_sqlalchemy_query.filter.return_value


class TestFilterByName:
    def test_query_returned_unchanged_when_no_filter_value_provided(
        self, mock_sqlalchemy_query
    ):
        result = _filter_by_name(mock_sqlalchemy_query, None)

        mock_sqlalchemy_query.filter.assert_not_called()
        assert result is mock_sqlalchemy_query

    def test_query_filtered_by_name_when_filter_value_provided(
        self, mock_sqlalchemy_query
    ):
        name = "Test"

        result = _filter_by_name(mock_sqlalchemy_query, name)

        query_filter = mock_sqlalchemy_query.filter.call_args.args[0]
        assert query_filter.compare(Munro.name.ilike(f"%{name}%"))

        assert result is mock_sqlalchemy_query.filter.return_value


@patch(_MODULE_PATH + "._filter_by_name")
@patch(_MODULE_PATH + "._filter_by_max_height")
@patch(_MODULE_PATH + "._filter_by_min_height")
class TestFilterMunros:
    def test_filters_by_min_height(
        self,
        mock_filter_by_min_height,
        mock_filter_by_max_height,
        mock_filter_by_name,
        mock_sqlalchemy_query,
    ):
        min_height_ft = 0

        filter_munros(
            mock_sqlalchemy_query,
            min_height_ft=min_height_ft,
            max_height_ft=None,
            name=None,
        )

        mock_filter_by_min_height.assert_called_once_with(
            mock_sqlalchemy_query, min_height_ft
        )

    def test_filters_by_max_height(
        self,
        mock_filter_by_min_height,
        mock_filter_by_max_height,
        mock_filter_by_name,
        mock_sqlalchemy_query,
    ):
        max_height_ft = 1

        filter_munros(
            mock_sqlalchemy_query,
            min_height_ft=None,
            max_height_ft=max_height_ft,
            name=None,
        )

        mock_filter_by_max_height.assert_called_once_with(
            mock_filter_by_min_height.return_value,
            max_height_ft,
        )

    def test_result_of_filter_by_name_is_returned(
        self,
        mock_filter_by_min_height,
        mock_filter_by_max_height,
        mock_filter_by_name,
        mock_sqlalchemy_query,
    ):
        name = "Test"

        result = filter_munros(
            mock_sqlalchemy_query,
            min_height_ft=None,
            max_height_ft=None,
            name=name,
        )

        mock_filter_by_name.assert_called_once_with(
            mock_filter_by_max_height.return_value,
            name,
        )
        assert result is mock_filter_by_name.return_value
