# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: dbGetQueryArrow.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 10

suppressPackageStartupMessages(library(DBI))
if (requireNamespace("RSQLite", quietly = TRUE) && requireNamespace("nanoarrow", quietly = TRUE)) withAutoprint({ # examplesIf
# Retrieve data as arrow table
con <- dbConnect(RSQLite::SQLite(), ":memory:")

dbWriteTable(con, "mtcars", mtcars)
dbGetQueryArrow(con, "SELECT * FROM mtcars")

dbDisconnect(con)
}) # examplesIf