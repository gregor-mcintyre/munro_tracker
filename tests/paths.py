"""Paths shared across the test suite."""

from types import SimpleNamespace

MUNRO_DB_BUILDER_PACKAGE = "munro_db_builder"

_api_package = "api"
_api_sqlite_package = _api_package + ".sqlite"
_api_sqlite_query_package = _api_sqlite_package + ".query"

api = SimpleNamespace(
    PACKAGE=_api_package,
    sqlite=SimpleNamespace(
        PACKAGE=_api_sqlite_package,
        query=SimpleNamespace(PACKAGE=_api_sqlite_query_package),
    ),
)
