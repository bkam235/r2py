# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-programming_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-programming.R
# lines: 5

suppressPackageStartupMessages(library(data.table))
my_subset = function(data, col, val) {
  data[data[[col]] == val & !is.na(data[[col]]), ]
}
my_subset(iris, col = "Species", val = "setosa")