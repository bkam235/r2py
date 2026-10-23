# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: dbCreateTableArrow.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 8

suppressPackageStartupMessages(library(DBI))
if (requireNamespace("RSQLite", quietly = TRUE) && requireNamespace("nanoarrow", quietly = TRUE)) withAutoprint({ # examplesIf
con <- dbConnect(RSQLite::SQLite(), ":memory:")
ptype <- data.frame(a = numeric())
dbCreateTableArrow(con, "df", nanoarrow::infer_nanoarrow_schema(ptype))
dbReadTable(con, "df")
dbDisconnect(con)
}) # examplesIf