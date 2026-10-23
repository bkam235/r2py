# r2py crawler metadata
# package: data.table
# source_type: vignette
# topic: datatable-faq_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\doc\datatable-faq.R
# lines: 9

suppressPackageStartupMessages(library(data.table))
DT = data.table(a = 1:5, b = 1:5)
suppressWarnings(
DT[2, b := 6]         # works (slower) with warning
)
class(6)              # numeric not integer
DT[2, b := 7L]        # works (faster) without warning
class(7L)             # L makes it an integer
DT[ , b := rnorm(5)]  # 'replace' integer column with a numeric column