"""Test data for the DoBIH Munros and Tops CSV file to Munro SQLite db pipeline."""

from munro_db_builder._mapper import MappedRow
from munro_db_builder.csv.row_type import CSVRow

# Realistic content in the DoBIH Munros and Tops CSV file
REALISTIC_DOBIH_CSV_FILE_CONTENT: str = (
    'Running No,DoBIH Number,Name,Height (m),"Height\n(ft)",1891,1921,2021,Comments\n'
    "1,1,Ben Chonzie,931,3054,MUN,MUN,MUN,\n"  # First hill row
    "17,36,Beinn a' Chroin East Top,940.1,3084,MUN,MUN,TOP,\n"  # Classification change
    "16,2925,Beinn a' Chroin,941.4,3089,,,MUN,\n"  # Only recently classified as a Munro
    "603,1301,Ben More,966,3169,MUN,MUN,MUN,\n"  # Last hill row
    "334,550,Leabaidh an Daimh Bhuidhe (Ben Avon) - Stuc Gharbh Mhor (old GR),"
    '1112,3648,TOP,TOP,,"on the O.S. name Stùc Gharbh Mhòr, corresponds to the'
    " 3625' spot\"\n"  # cp1252 special characters (ù, ò) in Comments
    ",,,,,283,276,282,\n"  # Non-hill row
    ",,,,,,,,\n"  # Empty row
)

# Realistic rows from the DoBIH Munros and Tops CSV file.
# Mapped to `REALISTIC_DOBIH_CSV_FILE_CONTENT`.
REALISTIC_DOBIH_CSV_ROWS: list[CSVRow] = [
    {
        "Running No": "1",
        "DoBIH Number": "1",
        "Name": "Ben Chonzie",
        "Height (m)": "931",
        "Height (ft)": "3054",
        "1891": "MUN",
        "1921": "MUN",
        "2021": "MUN",
        "Comments": "",
    },
    {
        "Running No": "17",
        "DoBIH Number": "36",
        "Name": "Beinn a' Chroin East Top",
        "Height (m)": "940.1",
        "Height (ft)": "3084",
        "1891": "MUN",
        "1921": "MUN",
        "2021": "TOP",
        "Comments": "",
    },
    {
        "Running No": "16",
        "DoBIH Number": "2925",
        "Name": "Beinn a' Chroin",
        "Height (m)": "941.4",
        "Height (ft)": "3089",
        "1891": "",
        "1921": "",
        "2021": "MUN",
        "Comments": "",
    },
    {
        "Running No": "603",
        "DoBIH Number": "1301",
        "Name": "Ben More",
        "Height (m)": "966",
        "Height (ft)": "3169",
        "1891": "MUN",
        "1921": "MUN",
        "2021": "MUN",
        "Comments": "",
    },
    {
        "Running No": "334",
        "DoBIH Number": "550",
        "Name": "Leabaidh an Daimh Bhuidhe (Ben Avon) - Stuc Gharbh Mhor (old GR)",
        "Height (m)": "1112",
        "Height (ft)": "3648",
        "1891": "TOP",
        "1921": "TOP",
        "2021": "",
        "Comments": "on the O.S. name Stùc Gharbh Mhòr, corresponds to the 3625' spot",
    },
    {
        "Running No": "",
        "DoBIH Number": "",
        "Name": "",
        "Height (m)": "",
        "Height (ft)": "",
        "1891": "283",
        "1921": "276",
        "2021": "282",
        "Comments": "",
    },
    {
        "Running No": "",
        "DoBIH Number": "",
        "Name": "",
        "Height (m)": "",
        "Height (ft)": "",
        "1891": "",
        "1921": "",
        "2021": "",
        "Comments": "",
    },
]

# Realistic rows mapped to the internal schema. Includes non-hill and non-munro rows.
# Mapped to `REALISTIC_DOBIH_CSV_ROWS`.
REALISTIC_MAPPED_ROWS: list[MappedRow] = [
    {
        "dobih_number": 1,
        "name": "Ben Chonzie",
        "height_ft": 3054,
        "classification": "MUN",
    },
    {
        "dobih_number": 36,
        "name": "Beinn a' Chroin East Top",
        "height_ft": 3084,
        "classification": "TOP",
    },
    {
        "dobih_number": 2925,
        "name": "Beinn a' Chroin",
        "height_ft": 3089,
        "classification": "MUN",
    },
    {
        "dobih_number": 1301,
        "name": "Ben More",
        "height_ft": 3169,
        "classification": "MUN",
    },
    {
        "dobih_number": 550,
        "name": "Leabaidh an Daimh Bhuidhe (Ben Avon) - Stuc Gharbh Mhor (old GR)",
        "height_ft": 3648,
        "classification": "",
    },
    {
        "dobih_number": None,
        "name": "",
        "height_ft": None,
        "classification": "282",
    },
    {
        "dobih_number": None,
        "name": "",
        "height_ft": None,
        "classification": "",
    },
]

# Realistic rows mapped to the internal schema that are classified as Munros based on
# the latest survey-year.
# Extracted from `REALISTIC_MAPPED_ROWS`.
REALISTIC_MAPPED_MUNRO_ROWS: list[MappedRow] = [
    REALISTIC_MAPPED_ROWS[index] for index in (0, 2, 3)
]
