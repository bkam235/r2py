# r2py crawler metadata
# package: stringr
# source_type: vignette
# topic: regular-expressions_s21
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\stringr\doc\regular-expressions.R
# lines: 4

suppressPackageStartupMessages(library(stringr))
date_string <- "Today's date is 2025-09-19."
pattern <- "(?<year>\\d{4})-(?<month>\\d{2})-(?<day>\\d{2})"
str_match(date_string, pattern)