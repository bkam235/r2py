# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: dbAppendTableArrow.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 8

suppressPackageStartupMessages(library(DBI))
if (requireNamespace("RSQLite", quietly = TRUE) && requireNamespace("nanoarrow", quietly = TRUE)) withAutoprint({ # examplesIf
con <- dbConnect(RSQLite::SQLite(), ":memory:")
dbCreateTableArrow(con, "iris", iris[0, ])
dbAppendTableArrow(con, "iris", iris[1:5, ])
dbReadTable(con, "iris")
dbDisconnect(con)
}) # examplesIf