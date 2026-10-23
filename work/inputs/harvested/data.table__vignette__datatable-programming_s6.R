# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-programming_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-programming.R
# lines: 9

suppressPackageStartupMessages(library(data.table))
my_subset = function(data, col, val) {
  data = deparse(substitute(data))
  col  = deparse(substitute(col))
  val  = paste0("'", val, "'")
  text = paste0("subset(", data, ", ", col, " == ", val, ")")
  eval(parse(text = text)[[1L]])
}
my_subset(iris, Species, "setosa")