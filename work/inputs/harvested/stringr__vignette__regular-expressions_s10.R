# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: regular-expressions_s10
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\regular-expressions.R
# lines: 4

suppressPackageStartupMessages(library(stringr))
x <- "a\u0301"
str_extract(x, ".")
str_extract(x, "\\X")