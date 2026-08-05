"""Paths to files throughout the project."""

from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent / "data"

DOBIH_MUNROS_CSV_FILE = _DATA_DIR / "dobih_munros_and_tops.csv"
MUNRO_SQLITE_DB = _DATA_DIR / "munro.db"
