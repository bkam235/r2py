# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: dbDriver.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 9

suppressPackageStartupMessages(library(DBI))
if (requireNamespace("RSQLite", quietly = TRUE)) withAutoprint({ # examplesIf
# Create a RSQLite driver with a string
d <- dbDriver("SQLite")
d

# But better, access the object directly
RSQLite::SQLite()
}) # examplesIf