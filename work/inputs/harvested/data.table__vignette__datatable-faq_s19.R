# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-faq_s19
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-faq.R
# lines: 7

suppressPackageStartupMessages(library(data.table))
DT = data.table(a = c(1,1,2,2,2), b = c(1,2,2,2,1))
DT
DT[ , list(.N = .N), list(a, b)]   # show intermediate result for exposition
cat(try(
    DT[ , list(.N = .N), by = list(a, b)][ , unique(.N), by = a]   # compound query more typical
, silent = TRUE))