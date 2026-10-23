# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: regular-expressions_s25
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\regular-expressions.R
# lines: 5

suppressPackageStartupMessages(library(stringr))
x <- "1888 is the longest year in Roman numerals: MDCCCLXXXVIII"
str_extract(x, "CC?")
str_extract(x, "CC+")
str_extract(x, 'C[LX]+')