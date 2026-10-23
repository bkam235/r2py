# r2py crawler metadata
# package: haven
# source_type: vignette
# topic: semantics_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\haven\doc\semantics.R
# lines: 6

suppressPackageStartupMessages(library(haven))
x1 <- labelled_spss(c(1:10, 99), c(Missing = 99), na_value = 99)
x2 <- labelled_spss(c(1:10, 99), c(Missing = 99), na_range = c(90, Inf))

x1
x2