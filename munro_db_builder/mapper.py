"""Utilities for mapping rows from the DoBIH Munros and Tops CSV file.

Normalizes values and maps rows to this project's internal schema,
which is consistent with the SQLite database.
"""

from munro_db_builder.csv.normalizers import normalize_int
from munro_db_builder.csv.row_type import CSVRow

type _NormalizedValue = str | int | None
type _MappedRow = dict[str, _NormalizedValue]

# Mapping of normalized CSV column names to internal schema.
# ADJUST KEYS if a future release of the CSV file renames them
_CSV_COLUMN_TO_INTERNAL_SCHEMA_MAP: dict[str, str] = {
    "DoBIH Number": "id",  # Assumed stable identifier across future releases
    "Name": "name",
    "Height (ft)": "height_ft",
}


def _normalize_field_value(
    field_name: str,
    raw_value: str,
) -> _NormalizedValue:
    """Normalizes a value based on a field mapped to the internal schema.

    Values for the `name` field are unchanged, but values for every
    other field are passed through `normalize_int`.

    Args:
        field_name: The internal schema field name of the raw value.
        raw_value: The raw value that is to be normalized.

    Returns:
        `raw_value` unchanged if `field_name` is `name`, or the value
        passed through `normalize_int` for any other field.
    """
    if field_name == "name":
        return raw_value

    return normalize_int(raw_value)


def _map_to_internal_schema(csv_row: CSVRow) -> _MappedRow:
    """Maps the columns of a CSV row to the internal schema.

    Columns not included in the internal schema are omitted.

    Args:
        csv_row: A CSV row with original normalized column names.

    Returns:
        The row with column names mapped to the internal schema,
        excluding columns not included in the internal schema.
    """
    map_items = _CSV_COLUMN_TO_INTERNAL_SCHEMA_MAP.items()

    return {
        internal_schema_field_name: _normalize_field_value(
            field_name=internal_schema_field_name,
            raw_value=csv_row[csv_column_name],
        )
        for csv_column_name, internal_schema_field_name in map_items
    }


def map_to_internal_schema_and_add_classification(
    csv_row: CSVRow,
    latest_year_column: str,
) -> _MappedRow:
    """Maps a CSV row and adds a classification key-value pair.

    Passes `csv_row` through `_map_to_internal_schema` and adds a
    `classification` key where the value is the classification for the
    latest survey-year.

    Args:
        csv_row: A CSV row with original normalized column names.
        latest_year_column: The column name of the latest survey-year in the
            CSV file. This is where the classification is to be extracted from.

    Returns:
        The CSV row after it has been passed through `_map_to_internal_schema`,
        plus an additional classification key-value pair.
    """
    mapped_row = _map_to_internal_schema(csv_row)
    mapped_row["classification"] = csv_row[latest_year_column]

    return mapped_row
