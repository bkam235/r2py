# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-faq_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-faq.R
# lines: 4

suppressPackageStartupMessages(library(data.table))
DT = data.table(x = rep(c("a", "b"), c(2, 3)), y = 1:5)
DT
DT[ , {z = sum(y); z + 3}, by = x]