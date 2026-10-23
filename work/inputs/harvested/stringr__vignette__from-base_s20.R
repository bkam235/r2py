# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: from-base_s20
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\from-base.R
# lines: 6

suppressPackageStartupMessages(library(stringr))
x <- c("\u00fc", "u\u0308")
x

nchar(x)
str_length(x)