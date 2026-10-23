# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: regular-expressions_s29
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\regular-expressions.R
# lines: 6

suppressPackageStartupMessages(library(stringr))
x <- c("1 piece", "2 pieces", "3")
str_extract(x, "\\d+(?= pieces?)")

y <- c("100", "$400")
str_extract(y, "(?<=\\$)\\d+")