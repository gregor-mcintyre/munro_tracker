"""Enums defining accepted values for the API's query parameters."""

from enum import StrEnum


class MunroSortBy(StrEnum):
    """A field that Munro list results can be sorted by."""

    NAME = "name"
    HEIGHT_FT = "height_ft"


class SortOrder(StrEnum):
    """A direction to sort Munro list results in."""

    ASC = "asc"
    DESC = "desc"
