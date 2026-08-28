"""Integration test for `run_pipeline`.

Exercises the `load_munros_and_tops_from_dobih_csv`, `find_latest_year_column`,
`map_and_filter_to_munros`, and `initialize` collaboration with temporary SQLite
database and CSV files.
"""

import pytest

from munro_db_builder.orchestrator import run_pipeline
from tests.integration.munro_db_builder._sqlite_assertion import (
    assert_munros_persisted_to_sqlite_database,
)


@pytest.mark.usefixtures("write_realistic_content_to_temporary_dobih_csv_file")
def test_run_pipeline_writes_all_munros_from_csv_to_sqlite_database(
    temporary_dobih_csv_file_path,
    temporary_munro_sqlite_db_file_path,
):
    result = run_pipeline(
        csv_path=temporary_dobih_csv_file_path,
        db_path=temporary_munro_sqlite_db_file_path,
    )

    assert_munros_persisted_to_sqlite_database(
        path=temporary_munro_sqlite_db_file_path,
        sqlite_initialization_result=result,
    )
