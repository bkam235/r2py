# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: dbGetRowsAffected.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 12

suppressPackageStartupMessages(library(DBI))
if (requireNamespace("RSQLite", quietly = TRUE)) withAutoprint({ # examplesIf
con <- dbConnect(RSQLite::SQLite(), ":memory:")

dbWriteTable(con, "mtcars", mtcars)
rs <- dbSendStatement(con, "DELETE FROM mtcars")
dbGetRowsAffected(rs)
nrow(mtcars)

dbClearResult(rs)
dbDisconnect(con)
}) # examplesIf