# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-faq_s18
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-faq.R
# lines: 7

suppressPackageStartupMessages(library(data.table))
DT = data.table(a = rep(1:3, 1:3), b = 1:6, c = 7:12)
DT
DT[ , { mySD = copy(.SD)
      mySD[1, b := 99L]
      mySD},
    by = a]