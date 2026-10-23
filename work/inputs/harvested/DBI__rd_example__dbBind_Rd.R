# r2py crawler metadata
# package: DBI
# source_type: rd_example
# topic: dbBind.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\DBI\help
# lines: 58

suppressPackageStartupMessages(library(DBI))
if (requireNamespace("RSQLite", quietly = TRUE)) withAutoprint({ # examplesIf
# Data frame flow:
con <- dbConnect(RSQLite::SQLite(), ":memory:")

dbWriteTable(con, "iris", iris)

# Using the same query for different values
iris_result <- dbSendQuery(con, "SELECT * FROM iris WHERE [Petal.Width] > ?")
dbBind(iris_result, list(2.3))
dbFetch(iris_result)
dbBind(iris_result, list(3))
dbFetch(iris_result)
dbClearResult(iris_result)

# Executing the same statement with different values at once
iris_result <- dbSendStatement(con, "DELETE FROM iris WHERE [Species] = $species")
dbBind(iris_result, list(species = c("setosa", "versicolor", "unknown")))
dbGetRowsAffected(iris_result)
dbClearResult(iris_result)

nrow(dbReadTable(con, "iris"))

dbDisconnect(con)
}) # examplesIf
if (requireNamespace("RSQLite", quietly = TRUE) && requireNamespace("nanoarrow", quietly = TRUE)) withAutoprint({ # examplesIf

# Arrow flow:
con <- dbConnect(RSQLite::SQLite(), ":memory:")

dbWriteTable(con, "iris", iris)

# Using the same query for different values
iris_result <- dbSendQueryArrow(con, "SELECT * FROM iris WHERE [Petal.Width] > ?")
dbBindArrow(
  iris_result,
  nanoarrow::as_nanoarrow_array_stream(data.frame(2.3, fix.empty.names = FALSE))
)
as.data.frame(dbFetchArrow(iris_result))
dbBindArrow(
  iris_result,
  nanoarrow::as_nanoarrow_array_stream(data.frame(3, fix.empty.names = FALSE))
)
as.data.frame(dbFetchArrow(iris_result))
dbClearResult(iris_result)

# Executing the same statement with different values at once
iris_result <- dbSendStatement(con, "DELETE FROM iris WHERE [Species] = $species")
dbBindArrow(iris_result, nanoarrow::as_nanoarrow_array_stream(data.frame(
  species = c("setosa", "versicolor", "unknown")
)))
dbGetRowsAffected(iris_result)
dbClearResult(iris_result)

nrow(dbReadTable(con, "iris"))

dbDisconnect(con)
}) # examplesIf