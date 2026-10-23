# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: regular-expressions_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\regular-expressions.R
# lines: 5

suppressPackageStartupMessages(library(stringr))
x <- "a\\b"
writeLines(x)

str_extract(x, "\\\\")