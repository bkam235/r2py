# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s35
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 4

suppressPackageStartupMessages(library(stringr))
x <- c("å", "a", "z")
str_sort(x)
str_sort(x, locale = "no")