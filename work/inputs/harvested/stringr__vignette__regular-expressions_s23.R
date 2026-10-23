# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: regular-expressions_s23
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\regular-expressions.R
# lines: 4

suppressPackageStartupMessages(library(stringr))
x <- c("apple", "banana", "pear")
str_extract(x, "^a")
str_extract(x, "a$")