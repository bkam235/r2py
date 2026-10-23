# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: stringr_s24
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\stringr.R
# lines: 5

suppressPackageStartupMessages(library(stringr))
x <- "This is a sentence."
str_split(x, boundary("word"))
str_count(x, boundary("word"))
str_extract_all(x, boundary("word"))