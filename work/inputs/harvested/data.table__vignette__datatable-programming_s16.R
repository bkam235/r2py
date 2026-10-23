# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-programming_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-programming.R
# lines: 9

suppressPackageStartupMessages(library(data.table))
substitute2(   # all are symbols
  f(v1, v2),
  list(v1 = "a", v2 = list("b", list("c", "d")))
)
substitute2(   # 'a' and 'd' should stay as character
  f(v1, v2),
  list(v1 = I("a"), v2 = list("b", list("c", I("d"))))
)