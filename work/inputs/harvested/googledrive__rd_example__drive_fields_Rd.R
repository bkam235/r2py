# r2py crawler metadata
# package: googledrive
# source_type: rd_example
# topic: drive_fields.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\googledrive\help
# lines: 9

suppressPackageStartupMessages(library(googledrive))
# get a tibble of all fields for the Files resource + indicator of defaults
drive_fields(expose())

# invalid fields are removed and throw warning
drive_fields(c("name", "parents", "ownedByMe", "pancakes!"))

# prepare fields for query
prep_fields(c("name", "parents", "kind"))