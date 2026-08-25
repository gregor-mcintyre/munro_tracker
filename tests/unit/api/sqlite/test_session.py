from unittest.mock import MagicMock, patch

from api.sqlite.session import get_sqlite_session
from tests import paths


@patch(paths.SQLITE_PACKAGE + ".session._session_factory")
class TestGetSqliteSession:
    def test_yields_session_from_session_factory(self, mock_session_factory):
        mock_session = MagicMock()
        mock_session_factory.return_value.__enter__.return_value = mock_session

        result = next(get_sqlite_session())

        assert result is mock_session

    def test_closes_session_after_use(self, mock_session_factory):
        list(get_sqlite_session())

        mock_session_factory.return_value.__exit__.assert_called_once()
