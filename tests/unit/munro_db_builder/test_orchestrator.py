from unittest.mock import patch

from munro_db_builder.orchestrator import run_pipeline
from tests.helpers import MUNRO_DB_BUILDER_PACKAGE_PATH

_MODULE_PATH = MUNRO_DB_BUILDER_PACKAGE_PATH + ".orchestrator"


@patch(_MODULE_PATH + ".initialize")
@patch(_MODULE_PATH + ".map_and_filter_to_munros")
@patch(_MODULE_PATH + ".find_latest_year_column")
@patch(_MODULE_PATH + ".load_munros_and_tops_from_dobih_csv")
class TestRunPipeline:
    def test_calls_dependencies_with_expected_arguments(
        self,
        mock_load_munros_and_tops,
        mock_find_latest_year_column,
        mock_map_and_filter_to_munros,
        mock_initialize,
    ):
        munros_and_tops_csv_rows = [
            {
                "DoBIH Number": "1",
                "Name": "Munro 1",
                "Height (ft)": "3",
                "1": "MUN",
                "2": "MUN",
            },
        ]
        mock_load_munros_and_tops.return_value = munros_and_tops_csv_rows

        run_pipeline()

        mock_load_munros_and_tops.assert_called_once_with()
        mock_find_latest_year_column.assert_called_once_with(
            {"DoBIH Number", "Name", "Height (ft)", "1", "2"}
        )
        mock_map_and_filter_to_munros.assert_called_once_with(
            mock_load_munros_and_tops.return_value,
            latest_year_column=mock_find_latest_year_column.return_value,
        )
        mock_initialize.assert_called_once_with(
            mock_map_and_filter_to_munros.return_value,
        )

    def test_returns_number_of_rows_written_from_initialize(
        self,
        mock_load_munros_and_tops,
        mock_find_latest_year_column,
        mock_map_and_filter_to_munros,
        mock_initialize,
    ):
        result = run_pipeline()

        assert result is mock_initialize.return_value
