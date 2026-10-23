# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: dbConnect.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 17

suppressPackageStartupMessages(library(DBI))
if (requireNamespace("RSQLite", quietly = TRUE)) withAutoprint({ # examplesIf
# SQLite only needs a path to the database. (Here, ":memory:" is a special
# path that creates an in-memory database.) Other database drivers
# will require more details (like user, password, host, port, etc.)
con <- dbConnect(RSQLite::SQLite(), ":memory:")
con

dbListTables(con)

dbDisconnect(con)

# Bad, for subtle reasons:
# This code fails when RSQLite isn't loaded yet,
# because dbConnect() doesn't know yet about RSQLite.
dbListTables(con <- dbConnect(RSQLite::SQLite(), ":memory:"))
}) # examplesIf