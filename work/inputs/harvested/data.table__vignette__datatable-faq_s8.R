# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-faq_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-faq.R
# lines: 4

suppressPackageStartupMessages(library(data.table))
DT = data.table(a = 1:3, b = c(4, 5, 6), d = c(7L,8L,9L))
DT[0]
sapply(DT[0], class)