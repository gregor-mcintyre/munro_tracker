"""`pytest` fixture shared across tests in `tests.unit.api.sqlite.query`."""

from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_sqlalchemy_query() -> MagicMock:
    """Mock SQLAlchemy query."""
    return MagicMock()
