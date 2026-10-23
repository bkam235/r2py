# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: data.table-condition-classes.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 10

suppressPackageStartupMessages(library(data.table))
# Handle missing column errors specifically
DT <- data.table(a = 1:3, b = 4:6)
tryCatch({
  setkey(DT, nonexistent_col)
}, dt_missing_column_error = function(e) {
  cat("Missing column detected:", conditionMessage(e), "\n")
}, error = function(e) {
  cat("Other error:", conditionMessage(e), "\n")
})