# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: dbFetchArrow.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 13

suppressPackageStartupMessages(library(DBI))
if (requireNamespace("RSQLite", quietly = TRUE) && requireNamespace("nanoarrow", quietly = TRUE)) withAutoprint({ # examplesIf
con <- dbConnect(RSQLite::SQLite(), ":memory:")

dbWriteTable(con, "mtcars", mtcars)

# Fetch all results
rs <- dbSendQueryArrow(con, "SELECT * FROM mtcars WHERE cyl = 4")
as.data.frame(dbFetchArrow(rs))
dbClearResult(rs)

dbDisconnect(con)
}) # examplesIf