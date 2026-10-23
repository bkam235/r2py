# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: regular-expressions_s24
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\regular-expressions.R
# lines: 5

suppressPackageStartupMessages(library(stringr))
x <- "Line 1\nLine 2\nLine 3\n"
str_extract_all(x, "^Line..")[[1]]
str_extract_all(x, regex("^Line..", multiline = TRUE))[[1]]
str_extract_all(x, regex("\\ALine..", multiline = TRUE))[[1]]