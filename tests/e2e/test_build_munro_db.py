"""End-to-end test for `build_munro_db.py`.

Runs the script as a subprocess, which uses the real DoBIH Munros and Tops CSV file and
creates an actual Munro SQLite database.

A future DoBIH release could affect the expected values for this test.
"""

from contextlib import closing
import sqlite3
import subprocess
import sys

import paths


def _assert_total_and_well_known_munros_in_sqlite_database() -> None:
    """Asserts the total and two well known Munros exist in the SQLite database."""
    with closing(sqlite3.connect(paths.MUNRO_SQLITE_DB)) as connection:
        munros_total = connection.execute("SELECT COUNT(*) FROM munro").fetchone()[0]

        ben_nevis = connection.execute(
            "SELECT name, height_ft FROM munro WHERE id = ?", (278,)
        ).fetchone()
        ben_lomond = connection.execute(
            "SELECT name, height_ft FROM munro WHERE id = ?", (32,)
        ).fetchone()

    assert munros_total == 282

    assert ben_nevis == ("Ben Nevis", 4411)
    assert ben_lomond == ("Ben Lomond", 3195)


def test_build_munro_db_writes_munros_to_sqlite_database():
    result = subprocess.run(
        [sys.executable, "build_munro_db.py"],
        cwd=paths.REPO_ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert result.stderr.splitlines() == [
        "INFO:root:Wrote 282 Munros to the SQLite database."
    ]

    _assert_total_and_well_known_munros_in_sqlite_database()
