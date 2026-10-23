# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: dbDisconnect.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 5

suppressPackageStartupMessages(library(DBI))
if (requireNamespace("RSQLite", quietly = TRUE)) withAutoprint({ # examplesIf
con <- dbConnect(RSQLite::SQLite(), ":memory:")
dbDisconnect(con)
}) # examplesIf