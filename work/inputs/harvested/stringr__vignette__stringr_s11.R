# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: stringr_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\stringr.R
# lines: 8

suppressPackageStartupMessages(library(stringr))
x <- "I like horses."
str_to_upper(x)
str_to_title(x)

str_to_lower(x)
# Turkish has two sorts of i: with and without the dot
str_to_lower(x, "tr")