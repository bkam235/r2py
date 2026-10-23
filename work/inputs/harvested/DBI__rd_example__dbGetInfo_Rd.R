# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: dbGetInfo.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 4

suppressPackageStartupMessages(library(DBI))
if (requireNamespace("RSQLite", quietly = TRUE)) withAutoprint({ # examplesIf
dbGetInfo(RSQLite::SQLite())
}) # examplesIf