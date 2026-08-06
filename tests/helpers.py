"""Helpers shared across the test suite."""

MUNRO_DB_BUILDER_PACKAGE_PATH = "munro_db_builder"

REALISTIC_DOBIH_CSV_FILE_CONTENT = (
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
