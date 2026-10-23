# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: regular-expressions_s22
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\regular-expressions.R
# lines: 5

suppressPackageStartupMessages(library(stringr))
text <- "This is is a test test with duplicates duplicates"
pattern <- "(?<word>\\b\\w+\\b)\\s+\\k<word>"
str_subset(text, pattern)
str_match_all(text, pattern)