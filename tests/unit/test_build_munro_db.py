import logging
from unittest.mock import patch

from build_munro_db import main
import paths


@patch("build_munro_db.orchestrator.run_pipeline")
class TestMain:
    def test_calls_run_pipeline(self, mock_run_pipeline):
        main()

        mock_run_pipeline.assert_called_once_with(
            csv_path=paths.DOBIH_MUNROS_CSV_FILE,
            db_path=paths.MUNRO_SQLITE_DB,
        )

    def test_number_of_munros_written_to_db_is_logged_as_info(
        self,
        mock_run_pipeline,
        caplog,
    ):
        mock_run_pipeline.return_value = 282

        with caplog.at_level(logging.INFO):
            main()

        log = caplog.records[-1]
        assert log.levelname == "INFO"
        assert log.getMessage() == "Wrote 282 Munros to the SQLite database."
