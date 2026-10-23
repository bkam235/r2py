# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: dbCreateTable.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 7

suppressPackageStartupMessages(library(DBI))
if (requireNamespace("RSQLite", quietly = TRUE)) withAutoprint({ # examplesIf
con <- dbConnect(RSQLite::SQLite(), ":memory:")
dbCreateTable(con, "iris", iris)
dbReadTable(con, "iris")
dbDisconnect(con)
}) # examplesIf