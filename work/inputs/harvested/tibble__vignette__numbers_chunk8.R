# r2py crawler metadata
# package: tibble
# source_type: vignette
# topic: numbers_chunk8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tibble\doc\numbers.Rmd
# lines: 6

suppressPackageStartupMessages(library(tibble))
#| label: numbers-15
num(1:3 + 0.125, digits = 4)
transf <- 10^num(1:3 + 0.125, digits = 4)
transf
num(transf, sigfig = 3)