# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-programming_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-programming.R
# lines: 10

suppressPackageStartupMessages(library(data.table))
substitute2(
  outer(inner(var1) + inner(var2)),
  env = list(
    outer = "sqrt",
    inner = "square",
    var1 = "a",
    var2 = "b"
  )
)