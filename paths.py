"""Paths to files throughout the project."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

_DATA_DIR = REPO_ROOT / "data"
DOBIH_MUNROS_CSV_FILE = _DATA_DIR / "dobih_munros_and_tops.csv"
MUNRO_SQLITE_DB = _DATA_DIR / "munro.db"
