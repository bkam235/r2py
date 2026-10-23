# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-joins_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-joins.R
# lines: 8

suppressPackageStartupMessages(library(data.table))
NewTax = data.table(
  unit = c("unit", "ounce"),
  type = "processed",
  tax_prop = c(0.65, 0.20)
)

NewTax