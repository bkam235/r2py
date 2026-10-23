# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: dbSendStatement.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 35

suppressPackageStartupMessages(library(DBI))
if (requireNamespace("RSQLite", quietly = TRUE)) withAutoprint({ # examplesIf
con <- dbConnect(RSQLite::SQLite(), ":memory:")

dbWriteTable(con, "cars", head(cars, 3))

rs <- dbSendStatement(
  con,
  "INSERT INTO cars (speed, dist) VALUES (1, 1), (2, 2), (3, 3)"
)
dbHasCompleted(rs)
dbGetRowsAffected(rs)
dbClearResult(rs)
dbReadTable(con, "cars")   # there are now 6 rows

# Pass one set of values directly using the param argument:
rs <- dbSendStatement(
  con,
  "INSERT INTO cars (speed, dist) VALUES (?, ?)",
  params = list(4L, 5L)
)
dbClearResult(rs)

# Pass multiple sets of values using dbBind():
rs <- dbSendStatement(
  con,
  "INSERT INTO cars (speed, dist) VALUES (?, ?)"
)
dbBind(rs, list(5:6, 6:7))
dbBind(rs, list(7L, 8L))
dbClearResult(rs)
dbReadTable(con, "cars")   # there are now 10 rows

dbDisconnect(con)
}) # examplesIf