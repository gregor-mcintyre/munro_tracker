"""Filters for querying for Munros."""

from sqlalchemy.orm import Query

from api.sqlite.models import Munro


def _filter_by_min_height(
    query: Query[Munro],
    min_height_ft: int | None,
) -> Query[Munro]:
    """Applies a minimum height filter to `query`, if `min_height_ft` is provided.

    Args:
        query: The query to apply the filter to.
        min_height_ft: The minimum height in feet a Munro must be to be included in the
            query result, or `None` to skip this filter.

    Returns:
        `query` with the minimum height filter applied if `min_height_ft` was provided,
        otherwise `query` unchanged.
    """
    if min_height_ft is None:
        return query

    return query.filter(Munro.height_ft >= min_height_ft)


def _filter_by_max_height(
    query: Query[Munro],
    max_height_ft: int | None,
) -> Query[Munro]:
    """Applies a maximum height filter to `query`, if `max_height_ft` is provided.

    Args:
        query: The query to apply the filter to.
        max_height_ft: The maximum height in feet a Munro must be to be included in the
            query result, or `None` to skip this filter.

    Returns:
        `query` with the maximum height filter applied if `max_height_ft` was provided,
        otherwise `query` unchanged.
    """
    if max_height_ft is None:
        return query

    return query.filter(Munro.height_ft <= max_height_ft)


def _filter_by_name(
    query: Query[Munro],
    name: str | None,
) -> Query[Munro]:
    """Applies a name filter to `query`, if `name` is provided.

    Args:
        query: The query to apply the filter to.
        name: A substring (not case-sensitive) that a Munro's name must contain to
            be included in the query result, or `None` to skip this filter.

    Returns:
        `query` with the name filter applied if `name` was provided, otherwise `query`
        unchanged.
    """
    if name is None:
        return query

    return query.filter(Munro.name.ilike(f"%{name}%"))


def filter_munros(
    query: Query[Munro],
    *,
    min_height_ft: int | None,
    max_height_ft: int | None,
    name: str | None,
) -> Query[Munro]:
    """Applies optional height and/or name filters to `query`.

    Args:
        query: The query to apply the filter to.
        min_height_ft: The minimum height in feet a Munro must be to be included in the
            query result, or `None` to skip this filter.
        max_height_ft: The maximum height in feet a Munro must be to be included in the
            query result, or `None` to skip this filter.
        name: A substring (not case-sensitive) that a Munro's name must contain to
            be included in the query result, or `None` to skip this filter.

    Returns:
        `query` with all optional filters applied to it.
    """
    query = _filter_by_min_height(query, min_height_ft)
    query = _filter_by_max_height(query, max_height_ft)

    return _filter_by_name(query, name)
