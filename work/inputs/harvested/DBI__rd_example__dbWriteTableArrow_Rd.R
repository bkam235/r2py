# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: dbWriteTableArrow.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 9

suppressPackageStartupMessages(library(DBI))
if (requireNamespace("RSQLite", quietly = TRUE) && requireNamespace("nanoarrow", quietly = TRUE)) withAutoprint({ # examplesIf
con <- dbConnect(RSQLite::SQLite(), ":memory:")

dbWriteTableArrow(con, "mtcars", nanoarrow::as_nanoarrow_array_stream(mtcars[1:5, ]))
dbReadTable(con, "mtcars")

dbDisconnect(con)
}) # examplesIf