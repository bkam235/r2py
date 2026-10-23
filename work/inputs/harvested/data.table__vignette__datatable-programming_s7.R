# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-programming_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-programming.R
# lines: 5

suppressPackageStartupMessages(library(data.table))
my_subset = function(data, col, val) {
  eval(substitute(subset(data, col == val)))
}
my_subset(iris, Species, "setosa")