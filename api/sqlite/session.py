"""SQLAlchemy session management for the SQLite database of Munros."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from paths import MUNRO_SQLITE_DB

_DATABASE_URL = f"sqlite:///file:{MUNRO_SQLITE_DB}?mode=ro&uri=true"
_engine = create_engine(_DATABASE_URL, connect_args={"check_same_thread": False})
_session_factory = sessionmaker(bind=_engine, autoflush=False, autocommit=False)


def get_sqlite_session() -> Generator[Session]:
    """Yields a read-only SQLAlchemy session to the SQLite database of Munros.

    The session is scoped to a single request.

    Yields:
        The read-only SQLAlchemy session to the SQLite database of Munros.
    """
    with _session_factory() as session:
        yield session
