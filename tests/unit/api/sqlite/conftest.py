"""`pytest` fixture shared across tests in `tests.unit.api.sqlite`."""

from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_sqlalchemy_session() -> MagicMock:
    """Mock SQLAlchemy session."""
    return MagicMock()
