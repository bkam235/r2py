# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: regular-expressions_chunk2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\regular-expressions.Rmd
# lines: 6

suppressPackageStartupMessages(library(stringr))
#| eval = FALSE
# The regular call:
str_extract(fruit, "nana")
# Is shorthand for
str_extract(fruit, regex("nana"))