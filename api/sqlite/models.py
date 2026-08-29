"""SQLAlchemy ORM models mapped to tables in the SQLite database of Munros."""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """The declarative base class for SQLAlchemy ORM models."""


class Munro(Base):
    """The SQLAlchemy ORM model representing a row in the `munro` table.

    Attributes:
        dobih_number: The DoBIH number of the Munro.
        name: The name of the Munro.
        height_ft: The height of the Munro in feet.
    """

    __tablename__ = "munro"

    dobih_number: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    height_ft: Mapped[int]
