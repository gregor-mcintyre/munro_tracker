from munro_db_builder.latest_year_finder import find_latest_year_column


class TestFindLatestYearColumn:
    def test_single_year_returns_that_year(self):
        column_names = ["1"]

        result = find_latest_year_column(column_names)

        assert result == "1"

    def test_multiple_years_returns_latest(self):
        column_names = ["1", "2", "3"]

        result = find_latest_year_column(column_names)

        assert result == "3"

    def test_non_year_columns_are_ignored(self):
        column_names = ["A", "B", "1"]

        result = find_latest_year_column(column_names)

        assert result == "1"

    def test_unsorted_years_returns_latest(self):
        column_names = ["1", "3", "2"]

        result = find_latest_year_column(column_names)

        assert result == "3"
