"""Queries the SQLite database of Munros."""

from sqlalchemy.orm import Session

from api.request_params import MunroSortBy, SortOrder
from api.sqlite.models import Munro
from api.sqlite.query._filterer import filter_munros
from api.sqlite.query._sorter import sort_munros


def query_munros(
    sqlite_session: Session,
    *,
    min_height_ft: int | None,
    max_height_ft: int | None,
    name: str | None,
    sort_by: MunroSortBy,
    sort_order: SortOrder,
    limit: int,
    offset: int,
) -> list[Munro]:
    """Queries the SQLite database for Munros.

    Optionally filters by height and/or name, sorts by height or name, and
    paginates based on `limit` and `offset`.

    Args:
        sqlite_session: An SQLAlchemy session to the SQLite database of Munros.
        min_height_ft: The minimum height in feet a Munro must be to be included in the
            query result, or `None` to skip this filter.
        max_height_ft: The maximum height in feet a Munro must be to be included in the
            query result, or `None` to skip this filter.
        name: A substring (not case-sensitive) that a Munro's name must contain to
            be included in the query result, or `None` to skip this filter.
        sort_by: The column to sort results by.
        sort_order: The order in which to sort results.
        limit: The maximum number of rows the query returns.
        offset: The number of rows the query skips before returning results.

    Returns:
        Munros from the SQLite database, after optional filtering, sorting, and
        pagination have been applied.
    """
    query = sqlite_session.query(Munro)
    query = filter_munros(
        query,
        min_height_ft=min_height_ft,
        max_height_ft=max_height_ft,
        name=name,
    )
    query = sort_munros(query, sort_by=sort_by, sort_order=sort_order)

    return query.offset(offset).limit(limit).all()


def query_munro_by_dobih_number(
    sqlite_session: Session,
    dobih_number: int,
) -> Munro | None:
    """Queries the SQLite database for a single Munro by its DoBIH number.

    Args:
        sqlite_session: An SQLAlchemy session to the SQLite database of Munros.
        dobih_number: The DoBIH number of the Munro.

    Returns:
        The Munro with a matching DoBIH number to `dobih_number`, or `None` if no Munro
        is found.
    """
    return sqlite_session.get(Munro, dobih_number)
