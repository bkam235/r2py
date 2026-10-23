# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-intro_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-intro.R
# lines: 9

suppressPackageStartupMessages(library(data.table))
DT = data.table(
  ID = c("b","b","b","a","a","c"),
  a = 1:6,
  b = 7:12,
  c = 13:18
)
DT
class(DT$ID)