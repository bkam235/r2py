# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: numbers_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\numbers.R
# lines: 8

suppressPackageStartupMessages(library(tibble))
num(1) + 2
1 + num(2)
1L + num(2)
num(3.23456, sigfig = 4) - num(2)
num(4, sigfig = 2) * num(3, digits = 2)
num(3, digits = 2) * num(4, sigfig = 2)
-num(2)