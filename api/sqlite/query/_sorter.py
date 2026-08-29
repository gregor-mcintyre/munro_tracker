"""Orders a query for Munros."""

from sqlalchemy import UnaryExpression, asc, desc
from sqlalchemy.orm import InstrumentedAttribute, Query

from api.request_params import MunroSortBy, SortOrder
from api.sqlite.models import Munro


def _apply_sort_direction[SortColumnT: (str, int)](
    column: InstrumentedAttribute[SortColumnT],
    sort_order: SortOrder,
) -> UnaryExpression[SortColumnT]:
    """Applies the order in which `column` is to be sorted.

    Args:
        column: The column to sort.
        sort_order: The order in which to sort.

    Returns:
        `column` ordered ascending or descending, determined by `sort_order`.
    """
    return asc(column) if sort_order == SortOrder.ASC else desc(column)


def _resolve_sorted_column(
    sort_by: MunroSortBy,
    sort_order: SortOrder,
) -> UnaryExpression[str] | UnaryExpression[int]:
    """Resolves what column to sort by, with `_apply_sort_direction` applied.

    Args:
        sort_by: The column to sort by.
        sort_order: The order in which to sort.

    Returns:
        The column to sort by, with `_apply_sort_direction` applied.
    """
    if sort_by == MunroSortBy.NAME:
        return _apply_sort_direction(Munro.name, sort_order)

    return _apply_sort_direction(Munro.height_ft, sort_order)


def sort_munros(
    query: Query[Munro],
    *,
    sort_by: MunroSortBy,
    sort_order: SortOrder,
) -> Query[Munro]:
    """Applies sorting to `query`.

    Args:
        query: The query to sort.
        sort_by: The column to sort by.
        sort_order: The order in which to sort.

    Returns:
        `query` ordered by `sort_by`, in the direction of `sort_order`.
    """
    sorted_column = _resolve_sorted_column(sort_by, sort_order)

    return query.order_by(sorted_column)
