# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: dbColumnInfo.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 11

suppressPackageStartupMessages(library(DBI))
if (requireNamespace("RSQLite", quietly = TRUE)) withAutoprint({ # examplesIf
con <- dbConnect(RSQLite::SQLite(), ":memory:")

rs <- dbSendQuery(con, "SELECT 1 AS a, 2 AS b")
dbColumnInfo(rs)
dbFetch(rs)

dbClearResult(rs)
dbDisconnect(con)
}) # examplesIf